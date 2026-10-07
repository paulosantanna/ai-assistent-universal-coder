#!/usr/bin/env node
// adr_lint — deterministic structure check for one Architecture Decision Record (ADR).
// Zero dependencies. The exported parser is shared with architecture-decision-log and
// the architecture-knowledge MCP so the three never disagree about what an ADR contains.
//
// Usage: node adr_lint.mjs <adr.md> [--strict]
// Exit codes: 0 PASS, 1 FAIL, 2 usage or read error.

import { readFileSync, statSync } from "node:fs";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

export const MAX_ADR_BYTES = 512 * 1024;
export const STATUS_VALUES = ["proposed", "accepted", "rejected", "deprecated", "superseded"];

const STATUS_ALIASES = new Map([
  ["proposed", "proposed"], ["proposto", "proposed"], ["proposta", "proposed"], ["propuesto", "proposed"], ["propuesta", "proposed"],
  ["accepted", "accepted"], ["aceito", "accepted"], ["aceita", "accepted"], ["aceptado", "accepted"], ["aceptada", "accepted"],
  ["rejected", "rejected"], ["rejeitado", "rejected"], ["rejeitada", "rejected"], ["rechazado", "rejected"], ["rechazada", "rejected"],
  ["deprecated", "deprecated"], ["depreciado", "deprecated"], ["depreciada", "deprecated"], ["obsoleto", "deprecated"], ["obsoleta", "deprecated"],
  ["superseded", "superseded"], ["substituido", "superseded"], ["substituida", "superseded"], ["reemplazado", "superseded"],
  ["reemplazada", "superseded"], ["sustituido", "superseded"], ["sustituida", "superseded"]
]);

// Order matters: specific headings ("decision drivers") must win over generic prefixes ("decision").
const HEADING_RULES = [
  ["drivers", /^(decision drivers?|fatores de decisao|direcionadores( da decisao)?|drivers de decisao|impulsores( de la decision)?|factores de decision)\b/],
  ["options", /^(considered options|options considered|opcoes consideradas|alternativas consideradas|opciones consideradas)\b/],
  ["pros_cons", /^(pros and cons|pros e contras|pros y contras)\b/],
  ["outcome", /^(decision outcome|resultado da decisao|resultado de la decision)\b/],
  ["consequences_negative", /^(negative consequences|consequencias negativas|consecuencias negativas|negativas|negativos|negative)\b/],
  ["consequences_positive", /^(positive consequences|consequencias positivas|consecuencias positivas|positivas|positivos|positive)\b/],
  ["consequences", /^(consequences|consequencias|consecuencias)\b/],
  ["confirmation", /^(confirmation|confirmacao|confirmacion)\b/],
  ["context", /^(context|contexto)\b/],
  ["problem", /^(problem|problema)\b/],
  ["decision", /^(decision|decisao)\b/],
  ["status", /^(status|estado|situacao)\b/],
  ["validation", /^(validation plan|plano de validacao|plan de validacion)\b/],
  ["review_trigger", /^(review trigger|gatilho de revisao|disparador de revision)\b/],
  ["rationale", /^(rationale|justificativa|justificacion|fundamentacao)\b/],
  ["more_information", /^(more information|mais informacoes|mas informacion|links)\b/],
  ["date", /^(date|data|fecha)\b/]
];

const Y_STATEMENT_PARTS = [
  ["context", ["in the context of", "no contexto de", "no contexto do", "no contexto da", "en el contexto de"]],
  ["facing", ["facing", "diante de", "diante do", "diante da", "enfrentando", "frente a", "face a"]],
  ["decided", ["we decided", "decidimos"]],
  ["achieve", ["to achieve", "para alcancar", "para atingir", "para obter", "para lograr", "para alcanzar", "para conseguir"]],
  ["accepting", ["accepting", "aceitando", "aceptando"]]
];

const REQUIRED_SECTIONS = {
  madr: ["context", "options", "outcome", "consequences"],
  nygard: ["context", "decision", "consequences"],
  "aeos-template": ["context", "decision", "consequences"],
  "y-statement": []
};

// Promoted to errors with --strict: the skill requires them for every ADR it authors.
const STRICT_CODES = new Set([
  "DATE_MISSING", "DATE_NOT_ISO", "STATUS_UNRECOGNIZED", "SUPERSEDED_WITHOUT_REFERENCE",
  "NO_NEGATIVE_CONSEQUENCE", "CONFIRMATION_MISSING"
]);

export function normalizeText(value) {
  return String(value ?? "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
}

function stripComments(text) {
  return String(text ?? "").replace(/<!--[\s\S]*?-->/g, "");
}

function cleanHeading(text) {
  return normalizeText(stripComments(text))
    .replace(/[`*_~]/g, "")
    .replace(/^\s*(\d+|[a-z])[.)]\s+/, "")
    .replace(/[:\s]+$/, "")
    .trim();
}

export function classifyHeading(text) {
  const cleaned = cleanHeading(text);
  for (const [key, pattern] of HEADING_RULES) if (pattern.test(cleaned)) return key;
  return null;
}

function parseFrontmatter(lines) {
  if (lines[0]?.trim() !== "---") return { data: {}, end: 0 };
  const closing = lines.findIndex((line, index) => index > 0 && line.trim() === "---");
  if (closing < 0) return { data: {}, end: 0 };
  const data = {};
  for (const line of lines.slice(1, closing)) {
    const match = /^([A-Za-z][\w-]*)\s*:\s*(.*)$/.exec(line);
    if (match) data[match[1].toLowerCase()] = match[2].trim().replace(/^(["'])(.*)\1$/, "$2");
  }
  return { data, end: closing + 1 };
}

function extractSupersededBy(raw) {
  const reference = /\badr[-_ ]?(\d{1,6})\b/i.exec(raw);
  if (reference) return `ADR-${reference[1]}`;
  const link = /\]\(([^)\s]+)\)/.exec(raw);
  if (link) {
    const fileName = link[1].split(/[\\/]/).pop() ?? "";
    const number = /^(?:adr[-_]?)?(\d{1,6})/i.exec(fileName);
    if (number) return `ADR-${number[1]}`;
  }
  return null;
}

export function normalizeStatus(raw) {
  const text = stripComments(raw).trim();
  if (!text) return null;
  const first = normalizeText(text).replace(/[`*_"'{}[\]]/g, " ").trim().split(/[\s,.;:|()]+/)[0] ?? "";
  const value = STATUS_ALIASES.get(first);
  return {
    raw: text,
    value: value ?? first,
    known: Boolean(value),
    superseded_by: value === "superseded" ? extractSupersededBy(text) : null
  };
}

function firstContentLine(bodyLines) {
  for (const line of bodyLines) {
    const value = stripComments(line).replace(/^\s*[-*+]\s+/, "").trim();
    if (value) return value;
  }
  return "";
}

// Header fields such as "- **Status**: Accepted" or "**Date**: 2026-10-07 | **Status**: Accepted".
function inlineField(lines, names) {
  const leading = new RegExp(`^\\s*(?:[-*+]\\s*)?(?:\\*\\*|__)?(?:${names})(?:\\*\\*|__)?\\s*:\\s*(?:\\*\\*|__)?\\s*(.+)$`, "i");
  const piped = new RegExp(`(?:\\*\\*|__)(?:${names})(?:\\*\\*|__)\\s*:\\s*([^|\\n]+)`, "i");
  for (const line of lines) {
    const match = leading.exec(line) || piped.exec(line);
    if (match) return match[1].split("|")[0].replace(/\*\*|__/g, "").trim();
  }
  return "";
}

function parse(markdown) {
  const text = String(markdown ?? "").replace(/^\uFEFF/, "").replace(/\r\n?/g, "\n");
  const lines = text.split("\n");
  const { data: frontmatter, end } = parseFrontmatter(lines);
  const headings = [];
  const contentLines = [];
  let fenced = false;
  for (let index = end; index < lines.length; index += 1) {
    const line = lines[index];
    if (/^\s*(```|~~~)/.test(line)) {
      fenced = !fenced;
      continue;
    }
    if (fenced) continue;
    contentLines.push({ index, line });
    const match = /^(#{1,6})\s+(.*?)\s*#*\s*$/.exec(line);
    if (match) headings.push({ level: match[1].length, text: match[2], line: index, key: classifyHeading(match[2]) });
  }
  const bodyOf = (heading) => {
    const next = headings.find((item) => item.line > heading.line && item.level <= heading.level);
    return lines.slice(heading.line + 1, next ? next.line : lines.length);
  };

  const titleHeading = headings.find((heading) => heading.level === 1);
  const titleRaw = titleHeading ? stripComments(titleHeading.text).trim() : "";
  const decisionTitle = titleRaw.replace(/^(?:adr[-_ ]?\d+|\d+)\s*[:.\-–—]\s*/i, "").trim();
  const sections = headings
    .filter((heading) => heading.level >= 2 && heading.key)
    .map((heading) => ({ key: heading.key, level: heading.level, heading: heading.text, line: heading.line + 1, body: bodyOf(heading).join("\n") }));
  const keys = new Set(sections.map((section) => section.key));

  const firstSection = headings.find((heading) => heading.level >= 2);
  const headerStart = titleHeading ? titleHeading.line + 1 : end;
  const headerZone = lines.slice(headerStart, firstSection ? firstSection.line : lines.length);

  const statusSection = sections.find((section) => section.key === "status");
  const statusRaw = frontmatter.status
    || (statusSection ? firstContentLine(statusSection.body.split("\n")) : "")
    || inlineField(headerZone, "status|estado|situa[çc][ãa]o");
  const dateSection = sections.find((section) => section.key === "date");
  const dateRaw = frontmatter.date
    || (dateSection ? firstContentLine(dateSection.body.split("\n")) : "")
    || inlineField(headerZone, "date|data|fecha");

  return {
    title: decisionTitle || null,
    title_raw: titleRaw || null,
    frontmatter,
    sections,
    keys: [...keys],
    format: detectFormat(keys, text),
    status: normalizeStatus(statusRaw),
    date: dateRaw ? dateRaw.trim() : null,
    text,
    contentLines
  };
}

/** Parse one ADR into title, metadata and classified sections without judging it. */
export function parseAdr(markdown) {
  const { text, contentLines, ...parsed } = parse(markdown);
  return { ...parsed, sections: parsed.sections.map(({ body, ...section }) => section) };
}

function yStatementParts(text) {
  const normalized = normalizeText(text).replace(/\s+/g, " ");
  const present = [];
  const missing = [];
  for (const [part, phrases] of Y_STATEMENT_PARTS) {
    (phrases.some((phrase) => normalized.includes(phrase)) ? present : missing).push(part);
  }
  return { present, missing };
}

function detectFormat(keys, text) {
  if (keys.has("outcome")) return "madr";
  if (keys.has("decision") && (keys.has("validation") || keys.has("review_trigger"))) return "aeos-template";
  if (keys.has("decision") && keys.has("context")) return "nygard";
  if (yStatementParts(text).present.length >= 3) return "y-statement";
  return "unknown";
}

function hasContent(body) {
  return stripComments(body).replace(/^#{1,6}\s.*$/gm, "").trim().length > 0;
}

function sectionBodies(parsed, keys) {
  return parsed.sections.filter((section) => keys.includes(section.key));
}

function countOptions(parsed) {
  const section = parsed.sections.find((item) => item.key === "options");
  if (!section) return 0;
  const bullets = section.body
    .split("\n")
    .filter((line) => /^[-*+]\s+\S/.test(line))
    .filter((line) => !/^[-*+]\s+(…|\.\.\.)\s*(<!--.*-->)?\s*$/.test(line.trim()));
  if (bullets.length) return bullets.length;
  return section.body.split("\n").filter((line) => /^#{3,6}\s+\S/.test(line)).length;
}

function hasNegativeConsequence(parsed) {
  if (sectionBodies(parsed, ["consequences_negative"]).some((section) => hasContent(section.body))) return true;
  return sectionBodies(parsed, ["consequences", "outcome"]).some((section) => {
    const body = normalizeText(section.body);
    return /^\s*[-*+]\s*(bad|ruim|malo|negativ\w*)\b/m.test(body) || body.includes("\u274c");
  });
}

// Template guidance is a braced phrase ("{title of option 1}") or a known token ("{Title}");
// single-word identifiers such as "/orders/{orderId}" are legitimate content.
function isPlaceholder(text) {
  return [...String(text).matchAll(/\{([^{}\n]+)\}/g)]
    .some(([, inner]) => /\s/.test(inner.trim()) || /^(title|nnnn?|yyyy-mm-dd|date|status|link)$/i.test(inner.trim()));
}

function placeholderLine(parsed) {
  if (Object.values(parsed.frontmatter).some(isPlaceholder)) return 1;
  for (const { index, line } of parsed.contentLines) {
    if (isPlaceholder(stripComments(line).replace(/`[^`]*`/g, ""))) return index + 1;
  }
  return 0;
}

/** Lint one ADR. strict=true is the bar for ADRs authored by the skill. */
export function lintAdr(markdown, { strict = false } = {}) {
  const parsed = parse(markdown);
  const errors = [];
  const warnings = [];
  const flag = (code, message) => {
    (strict && STRICT_CODES.has(code) ? errors : warnings).push({ code, message });
  };
  const fail = (code, message) => errors.push({ code, message });

  if (!parsed.title) fail("TITLE_MISSING", "Add a level-1 heading that names the decision.");
  else if (parsed.title.endsWith("?")) fail("TITLE_IS_QUESTION", "State the decision as a noun phrase, not a question (e.g. 'Use Redis for session storage').");

  if (!parsed.status) fail("STATUS_MISSING", "Record a status: proposed, accepted, rejected, deprecated or superseded by ADR-NNNN.");
  else if (!parsed.status.known) flag("STATUS_UNRECOGNIZED", `Status '${parsed.status.raw}' is not one of ${STATUS_VALUES.join(", ")}.`);
  else if (parsed.status.value === "superseded" && !parsed.status.superseded_by) {
    flag("SUPERSEDED_WITHOUT_REFERENCE", "A superseded ADR must name its replacement (superseded by ADR-NNNN).");
  }

  if (!parsed.date) flag("DATE_MISSING", "Add the decision date as YYYY-MM-DD.");
  else if (!/^\d{4}-\d{2}-\d{2}$/.test(parsed.date) || Number.isNaN(Date.parse(`${parsed.date}T00:00:00Z`))) {
    flag("DATE_NOT_ISO", `Date '${parsed.date}' is not a valid YYYY-MM-DD date.`);
  }

  const format = parsed.format;
  if (format === "unknown") {
    fail("UNRECOGNIZED_FORMAT", "Structure matches no supported template (MADR, Nygard, Y-statement, AEOS ADR_TEMPLATE).");
  }

  for (const key of REQUIRED_SECTIONS[format] ?? []) {
    const accepted = key === "consequences" ? ["consequences", "consequences_positive", "consequences_negative"] : [key];
    const found = sectionBodies(parsed, accepted);
    if (!found.length) fail(`${key.toUpperCase()}_MISSING`, `Add the ${key} section required by the ${format} format.`);
    else if (!found.some((section) => hasContent(section.body))) fail(`${key.toUpperCase()}_EMPTY`, `The ${key} section is empty.`);
  }

  if (format === "y-statement") {
    const { missing } = yStatementParts(parsed.text);
    if (missing.length) fail("Y_STATEMENT_INCOMPLETE", `Y-statement lacks: ${missing.join(", ")}.`);
  }

  let optionsCount = null;
  if (format === "madr" || format === "aeos-template") {
    optionsCount = countOptions(parsed);
    if (optionsCount < 2) {
      warnings.push({ code: "OPTIONS_LT_2", message: "Fewer than two considered options; justify a single viable option instead of adding a dummy alternative." });
    }
    if (!hasNegativeConsequence(parsed)) flag("NO_NEGATIVE_CONSEQUENCE", "List at least one honest negative consequence (avoid the Free Lunch Coupon anti-pattern).");
  }
  if (format === "madr") {
    const outcome = sectionBodies(parsed, ["outcome"]).map((section) => normalizeText(section.body)).join("\n");
    if (outcome && !/(chosen option|opcao escolhida|opcion elegida)/.test(outcome)) {
      warnings.push({ code: "CHOSEN_OPTION_MISSING", message: "Name the chosen option in the outcome: Chosen option: \"X\", because ..." });
    }
    if (!parsed.keys.includes("confirmation")) flag("CONFIRMATION_MISSING", "Add a Confirmation section stating how compliance with the decision will be checked (MADR 4.0.0).");
  }

  const placeholder = placeholderLine(parsed);
  if (placeholder) fail("PLACEHOLDER_LEFT", `Template placeholder left near line ${placeholder}; replace or delete it.`);

  return {
    status: errors.length ? "FAIL" : "PASS",
    format,
    title: parsed.title,
    adr_status: parsed.status,
    date: parsed.date,
    options_count: optionsCount,
    strict: Boolean(strict),
    errors,
    warnings
  };
}

function main(argv) {
  const args = argv.slice(2);
  const strict = args.includes("--strict");
  const files = args.filter((arg) => !arg.startsWith("--"));
  if (files.length !== 1) {
    console.error("usage: node adr_lint.mjs <adr.md> [--strict]");
    return 2;
  }
  let text;
  try {
    const path = resolve(files[0]);
    if (statSync(path).size > MAX_ADR_BYTES) throw new Error(`file exceeds ${MAX_ADR_BYTES} bytes`);
    text = readFileSync(path, "utf8");
  } catch (error) {
    console.error(JSON.stringify({ status: "ERROR", reason: "READ_FAILED", file: files[0], message: error.message }));
    return 2;
  }
  const result = { file: files[0], ...lintAdr(text, { strict }) };
  console.log(JSON.stringify(result, null, 2));
  return result.status === "PASS" ? 0 : 1;
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  process.exitCode = main(process.argv);
}
