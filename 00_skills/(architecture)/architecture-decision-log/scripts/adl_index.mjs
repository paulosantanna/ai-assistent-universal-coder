#!/usr/bin/env node
// adl_index — Architecture Decision Log view of an ADR directory: ordered index, integrity
// findings, lifecycle summary and the next free number. Read-only unless --write-index is given.
//
// Usage: node adl_index.mjs <adr-dir> [--today YYYY-MM-DD] [--stale-days N] [--next "Decision title"] [--write-index <file>]
// Exit codes: 0 no error findings, 1 error findings, 2 usage or read error.

import { existsSync, readdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { dirname, join, relative, resolve, sep } from "node:path";
import { pathToFileURL } from "node:url";
import { lintAdr, MAX_ADR_BYTES, normalizeText } from "../../architecture-decision-record/scripts/adr_lint.mjs";

export const MAX_LOG_FILES = 2000;
export const MAX_DEPTH = 3;
export const DEFAULT_STALE_DAYS = 30;
export const INDEX_START = "<!-- adl:index:start -->";
export const INDEX_END = "<!-- adl:index:end -->";

const NON_RECORD = /^(readme|index|template|decision-log|toc)\.md$|^adr-template/i;
const FILENAME_PATTERNS = [
  { id: "ADR-NNNN-title", re: /^(adr)[-_](\d{1,6})[-_](.+)\.md$/i },
  { id: "adr-NNNN", re: /^(adr)[-_](\d{1,6})\.md$/i },
  { id: "NNNN-title", re: /^()(\d{1,6})[-_](.+)\.md$/i }
];
const DAY_MS = 24 * 60 * 60 * 1000;

export function parseAdrFilename(fileName) {
  if (NON_RECORD.test(fileName)) return null;
  for (const { id, re } of FILENAME_PATTERNS) {
    const match = re.exec(fileName);
    if (!match) continue;
    const slug = match[3] ?? "";
    return {
      pattern: id,
      number: Number(match[2]),
      digits: match[2],
      width: match[2].length,
      prefix: match[1] || null,
      upper_slug: /[A-Z]/.test(slug) && slug === slug.toUpperCase(),
      slug
    };
  }
  return null;
}

function toPosix(path) {
  return path.split(sep).join("/");
}

/** Read candidate ADR files under root (bounded depth and count). */
export function collectRecords(root) {
  const records = [];
  const ignored = [];
  const oversized = [];
  const walk = (directory, depth) => {
    const entries = readdirSync(directory, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name));
    for (const entry of entries) {
      if (entry.name.startsWith(".") || entry.name === "node_modules") continue;
      const full = join(directory, entry.name);
      if (entry.isDirectory()) {
        if (depth < MAX_DEPTH) walk(full, depth + 1);
        continue;
      }
      if (!entry.isFile() || !entry.name.toLowerCase().endsWith(".md")) continue;
      const file = toPosix(relative(root, full));
      const name = parseAdrFilename(entry.name);
      if (!name) {
        ignored.push(file);
        continue;
      }
      if (records.length >= MAX_LOG_FILES) throw new Error(`more than ${MAX_LOG_FILES} ADR files under ${root}`);
      if (statSync(full).size > MAX_ADR_BYTES) {
        oversized.push(file);
        continue;
      }
      records.push({ file, category: toPosix(relative(root, directory)), name, content: readFileSync(full, "utf8") });
    }
  };
  walk(root, 0);
  return { records, ignored, oversized };
}

function adrId(number, width) {
  return `ADR-${String(number).padStart(width, "0")}`;
}

function refNumber(reference) {
  const match = /(\d+)/.exec(String(reference ?? ""));
  return match ? Number(match[1]) : null;
}

function mentions(content, number, file) {
  const pattern = new RegExp(`\\badr[-_ ]?0*${number}\\b`, "i");
  return pattern.test(content) || content.includes(file.split("/").pop());
}

function slugify(title, upper) {
  const slug = normalizeText(title).replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 80) || "decision";
  return upper ? slug.toUpperCase() : slug;
}

function dominant(values) {
  const counts = new Map();
  for (const value of values) counts.set(value, (counts.get(value) ?? 0) + 1);
  return [...counts.entries()].sort((a, b) => b[1] - a[1])[0]?.[0];
}

/** Next free number of a category; gaps are never reused. */
export function nextRecord(entries, { category = "", title = "" } = {}) {
  const scoped = entries.filter((entry) => entry.category === category);
  const pattern = dominant(scoped.map((entry) => entry.pattern)) ?? "NNNN-title";
  const width = Math.max(4, ...scoped.map((entry) => entry.width));
  const number = scoped.reduce((max, entry) => Math.max(max, entry.number), 0) + 1;
  const sample = scoped.find((entry) => entry.pattern === pattern);
  const padded = String(number).padStart(width, "0");
  const prefix = sample?.prefix ?? "ADR";
  let fileName;
  if (pattern === "adr-NNNN") fileName = `${prefix}-${padded}.md`;
  else if (pattern === "ADR-NNNN-title") fileName = `${prefix}-${padded}-${slugify(title, sample?.upper_slug)}.md`;
  else fileName = `${padded}-${slugify(title, false)}.md`;
  return { category, number, id: adrId(number, width), pattern, file: category ? `${category}/${fileName}` : fileName };
}

/** Build index entries, integrity findings and lifecycle summary from collected records. */
export function buildLog(records, { today = new Date().toISOString().slice(0, 10), staleDays = DEFAULT_STALE_DAYS } = {}) {
  const findings = [];
  const finding = (severity, code, message, extra = {}) => findings.push({ severity, code, message, ...extra });
  const entries = records
    .map(({ file, category, name, content }) => {
      const lint = lintAdr(content);
      return {
        file,
        category,
        number: name.number,
        width: name.width,
        pattern: name.pattern,
        prefix: name.prefix,
        upper_slug: name.upper_slug,
        title: lint.title,
        status: lint.adr_status?.value ?? null,
        status_raw: lint.adr_status?.raw ?? null,
        superseded_by: lint.adr_status?.superseded_by ?? null,
        date: lint.date,
        format: lint.format,
        lint: { errors: lint.errors.map((item) => item.code), warnings: lint.warnings.map((item) => item.code) },
        content
      };
    })
    .sort((a, b) => a.category.localeCompare(b.category) || a.number - b.number || a.file.localeCompare(b.file));

  const categories = [...new Set(entries.map((entry) => entry.category))];
  for (const category of categories) {
    const scoped = entries.filter((entry) => entry.category === category);
    const where = category || "the log root";
    const byNumber = new Map();
    for (const entry of scoped) byNumber.set(entry.number, [...(byNumber.get(entry.number) ?? []), entry.file]);
    for (const [number, files] of byNumber) {
      if (files.length > 1) finding("error", "DUPLICATE_NUMBER", `Number ${number} is used by ${files.length} records in ${where}.`, { category, files });
    }
    const numbers = [...byNumber.keys()].sort((a, b) => a - b);
    const gaps = [];
    for (let number = numbers[0]; number < numbers[numbers.length - 1] && gaps.length < 20; number += 1) {
      if (!byNumber.has(number)) gaps.push(number);
    }
    if (gaps.length) finding("warning", "NUMBER_GAP", `Missing numbers in ${where}: ${gaps.join(", ")}. Never reuse them.`, { category, numbers: gaps });
    if (new Set(scoped.map((entry) => entry.pattern)).size > 1) {
      finding("warning", "MIXED_FILENAME_PATTERNS", `Records in ${where} use more than one filename pattern.`, { category });
    }
    if (new Set(scoped.map((entry) => entry.width)).size > 1) {
      finding("warning", "MIXED_NUMBER_WIDTH", `Records in ${where} use more than one number width.`, { category });
    }
  }

  const resolveTarget = (entry) => {
    const number = refNumber(entry.superseded_by);
    if (number === null) return null;
    const local = entries.filter((candidate) => candidate.category === entry.category && candidate.number === number);
    if (local.length) return local[0];
    const elsewhere = entries.filter((candidate) => candidate.number === number);
    return elsewhere.length === 1 ? elsewhere[0] : null;
  };

  for (const entry of entries) {
    if (entry.lint.errors.length) {
      finding("error", "RECORD_LINT_ERRORS", `${entry.file}: ${entry.lint.errors.join(", ")}.`, { file: entry.file });
    }
    if (entry.status === "superseded" && entry.superseded_by) {
      const target = resolveTarget(entry);
      if (!target) {
        finding("error", "SUPERSEDED_TARGET_MISSING", `${entry.file} is superseded by ${entry.superseded_by}, which is not in the log.`, { file: entry.file });
      } else if (target.file === entry.file) {
        finding("error", "SUPERSEDED_BY_SELF", `${entry.file} names itself as its replacement.`, { file: entry.file });
      } else {
        if (["rejected", "deprecated"].includes(target.status)) {
          finding("warning", "SUPERSEDED_BY_INACTIVE", `${entry.file} is superseded by ${target.file}, whose status is ${target.status}.`, { file: entry.file });
        }
        if (!mentions(target.content, entry.number, entry.file)) {
          finding("warning", "SUPERSEDE_BACKLINK_MISSING", `${target.file} does not link back to the record it supersedes (${entry.file}).`, { file: target.file });
        }
      }
    }
  }

  const reported = new Set();
  for (const start of entries) {
    const seen = [];
    let current = start;
    while (current && current.status === "superseded" && current.superseded_by) {
      if (seen.includes(current.file)) {
        const cycle = seen.slice(seen.indexOf(current.file));
        const key = [...cycle].sort().join("|");
        if (!reported.has(key)) {
          reported.add(key);
          finding("error", "SUPERSESSION_CYCLE", `Supersession cycle: ${[...cycle, current.file].join(" -> ")}.`, { files: cycle });
        }
        break;
      }
      seen.push(current.file);
      const next = resolveTarget(current);
      if (!next || next.file === current.file) break;
      current = next;
    }
  }

  const todayMs = Date.parse(`${today}T00:00:00Z`);
  const byStatus = {};
  const lifecycle = { by_status: byStatus, current_decisions: [], stale_proposals: [], undated: [], without_confirmation: [] };
  for (const entry of entries) {
    const key = entry.status ?? "missing";
    byStatus[key] = (byStatus[key] ?? 0) + 1;
    const id = adrId(entry.number, entry.width);
    const label = entry.category ? `${entry.category}/${id}` : id;
    if (entry.status === "accepted") lifecycle.current_decisions.push(label);
    if (!entry.date) lifecycle.undated.push(label);
    if (entry.status === "accepted" && entry.lint.warnings.includes("CONFIRMATION_MISSING")) lifecycle.without_confirmation.push(label);
    const dateMs = entry.date ? Date.parse(`${entry.date}T00:00:00Z`) : Number.NaN;
    if (entry.status === "proposed" && !Number.isNaN(dateMs) && !Number.isNaN(todayMs) && (todayMs - dateMs) / DAY_MS > staleDays) {
      lifecycle.stale_proposals.push(label);
      finding("warning", "STALE_PROPOSAL", `${entry.file} has been proposed since ${entry.date} (more than ${staleDays} days).`, { file: entry.file });
    }
  }

  const publicEntries = entries.map(({ content, prefix, upper_slug, ...entry }) => ({ id: adrId(entry.number, entry.width), ...entry }));
  return {
    status: findings.some((item) => item.severity === "error") ? "FAIL" : "PASS",
    today,
    stale_days: staleDays,
    categories,
    records: publicEntries,
    integrity: findings,
    lifecycle,
    internal: entries
  };
}

function escapeCell(value) {
  return String(value ?? "").replace(/\|/g, "\\|").replace(/\s+/g, " ").trim();
}

/** Markdown index table(s), links relative to the log root. */
export function renderIndex(records) {
  const categories = [...new Set(records.map((record) => record.category))];
  const blocks = categories.map((category) => {
    const rows = records
      .filter((record) => record.category === category)
      .map((record) => `| [${record.id}](${encodeURI(record.file)}) | ${escapeCell(record.title)} | ${escapeCell(record.status ?? "missing")} | ${escapeCell(record.date)} | ${escapeCell(record.superseded_by)} |`);
    const table = ["| ADR | Title | Status | Date | Superseded by |", "| --- | --- | --- | --- | --- |", ...rows].join("\n");
    return categories.length > 1 ? `### ${category || "(root)"}\n\n${table}` : table;
  });
  return blocks.join("\n\n");
}

/** Read-only scan used by the CLI and the architecture-knowledge MCP. */
export function scanLog(directory, { today, staleDays, nextTitle, nextCategory = "" } = {}) {
  const root = resolve(directory);
  if (!existsSync(root) || !statSync(root).isDirectory()) throw new Error(`not a directory: ${directory}`);
  const { records, ignored, oversized } = collectRecords(root);
  const { internal, ...log } = buildLog(records, { today, staleDays });
  for (const file of oversized) log.integrity.push({ severity: "error", code: "FILE_TOO_LARGE", message: `${file} exceeds ${MAX_ADR_BYTES} bytes.`, file });
  if (oversized.length) log.status = "FAIL";
  return {
    ...log,
    directory,
    ignored,
    next: nextTitle !== undefined ? nextRecord(internal, { category: nextCategory, title: nextTitle }) : null,
    index_markdown: renderIndex(log.records)
  };
}

/** Idempotently replace the marked index block inside a file that lives in the log directory. */
export function writeIndex(directory, indexFile, markdown) {
  const root = resolve(directory);
  const target = resolve(indexFile);
  if (target !== root && !target.startsWith(`${root}${sep}`)) throw new Error("index file must live inside the ADR directory");
  const block = `${INDEX_START}\n${markdown}\n${INDEX_END}`;
  const current = existsSync(target) ? readFileSync(target, "utf8") : null;
  let next;
  if (current === null) next = `# Architecture Decision Log\n\n${block}\n`;
  else if (current.includes(INDEX_START) && current.includes(INDEX_END)) {
    next = current.slice(0, current.indexOf(INDEX_START)) + block + current.slice(current.indexOf(INDEX_END) + INDEX_END.length);
  } else next = `${current.replace(/\s*$/, "")}\n\n${block}\n`;
  if (next === current) return { written: false, file: indexFile };
  writeFileSync(target, next);
  return { written: true, file: indexFile };
}

function option(args, name) {
  const index = args.indexOf(name);
  return index >= 0 ? args[index + 1] : undefined;
}

function main(argv) {
  const args = argv.slice(2);
  const valued = new Set(["--today", "--stale-days", "--next", "--write-index"]);
  const positional = args.filter((arg, index) => !arg.startsWith("--") && !valued.has(args[index - 1]));
  if (positional.length !== 1) {
    console.error('usage: node adl_index.mjs <adr-dir> [--today YYYY-MM-DD] [--stale-days N] [--next "Decision title"] [--write-index <file>]');
    return 2;
  }
  const staleRaw = option(args, "--stale-days");
  const staleDays = staleRaw === undefined ? DEFAULT_STALE_DAYS : Number(staleRaw);
  if (!Number.isInteger(staleDays) || staleDays < 0) {
    console.error("--stale-days must be a non-negative integer");
    return 2;
  }
  const today = option(args, "--today");
  if (today !== undefined && !/^\d{4}-\d{2}-\d{2}$/.test(today)) {
    console.error("--today must be YYYY-MM-DD");
    return 2;
  }
  try {
    const result = scanLog(positional[0], { today, staleDays, nextTitle: option(args, "--next") });
    const indexFile = option(args, "--write-index");
    if (indexFile) result.index_written = writeIndex(positional[0], indexFile, result.index_markdown);
    console.log(JSON.stringify(result, null, 2));
    return result.status === "PASS" ? 0 : 1;
  } catch (error) {
    console.error(JSON.stringify({ status: "ERROR", reason: "SCAN_FAILED", directory: positional[0], message: error.message }));
    return 2;
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  process.exitCode = main(process.argv);
}
