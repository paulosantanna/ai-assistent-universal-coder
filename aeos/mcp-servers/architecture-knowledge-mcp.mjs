#!/usr/bin/env node
// Architecture Knowledge MCP — governed offline server for the ADR, ADL, ASR and AKM skills.
// Mirrors the TLC agent-skills-mcp progressive disclosure (search_skills -> read_skill ->
// fetch_skill_files) over the local skill folders and exposes the skills' deterministic checks.
// Tool logic lives in the skills' scripts; this module only validates input and routes.
// Read-only, workspace-only, no network. stdout carries JSON-RPC only.

import { existsSync, readdirSync, readFileSync, realpathSync, statSync } from "node:fs";
import { dirname, join, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";
import { lintAdr, MAX_ADR_BYTES, normalizeText } from "../../skills/architecture-decision-record/scripts/adr_lint.mjs";
import { scanLog } from "../../skills/architecture-decision-log/scripts/adl_index.mjs";
import { assessAsr } from "../../skills/architecturally-significant-requirement/scripts/asr_test.mjs";

const VERSION = "1.0.0";
const WORKSPACE_ROOT = realpathSync(resolve(dirname(fileURLToPath(import.meta.url)), "..", ".."));
const SKILLS_ROOT = join(WORKSPACE_ROOT, "skills");
const SKILL_IDS = [
  "architecture-decision-record",
  "architecture-decision-log",
  "architecturally-significant-requirement",
  "architecture-knowledge-management"
];
const CATEGORY = "architecture";
// Budgets copied from TLC agent-skills-mcp: five ranked results, weak matches (score < 20) dropped
// so agents do not act on near-zero hits, and at most five files / 50,000 characters (~12.5k
// tokens) per fetch so a response stays under the tool-response caps agents apply.
const MAX_SEARCH_RESULTS = 5;
const MATCH_FLOOR = 20;
const MAX_FETCH_FILES = 5;
const RESPONSE_BUDGET_CHARS = 50_000;
const MAX_LISTED_FILES = 50;
const WEIGHTS = { name: 0.45, triggers: 0.3, description: 0.2, category: 0.05 };
const STOPWORDS = new Set([
  "a", "an", "the", "and", "or", "for", "of", "to", "in", "on", "with", "my", "our", "we", "is", "it", "this", "that",
  "be", "how", "what", "do", "me", "please", "de", "da", "das", "dos", "e", "o", "os", "as", "um", "uma", "para",
  "por", "com", "no", "na", "nos", "nas", "em", "que", "se", "ao", "meu", "minha", "nosso", "nossa", "el", "la", "los", "las", "y"
]);
const KNOWLEDGE = JSON.parse(readFileSync(new URL("../knowledge/architecture-knowledge-map.json", import.meta.url), "utf8"));
const RAW = Symbol("raw-content");

function toPosix(path) {
  return path.split(sep).join("/");
}

function tokenize(text) {
  return normalizeText(text).split(/[^a-z0-9]+/).filter((token) => token.length >= 2 && !STOPWORDS.has(token));
}

function firstSentence(text, max = 200) {
  const sentence = text.split(/(?<=\.)\s/)[0];
  if (sentence.length <= max) return sentence;
  return `${sentence.slice(0, sentence.lastIndexOf(" ", max - 1))}…`;
}

function yamlScalar(raw) {
  const value = String(raw ?? "").trim();
  if (value.startsWith("'") && value.endsWith("'")) return value.slice(1, -1).replace(/''/g, "'");
  if (value.startsWith('"') && value.endsWith('"')) return value.slice(1, -1).replace(/\\"/g, '"');
  return value;
}

function listFiles(directory, base = directory) {
  const files = [];
  for (const entry of readdirSync(directory, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
    if (entry.name.startsWith(".")) continue;
    const full = join(directory, entry.name);
    if (entry.isDirectory()) files.push(...listFiles(full, base));
    else if (entry.isFile()) files.push(toPosix(relative(base, full)));
  }
  return files;
}

// Skills are read on every call: four small local folders, so the catalog never goes stale.
function loadSkill(id) {
  const directory = join(SKILLS_ROOT, id);
  const text = readFileSync(join(directory, "SKILL.md"), "utf8").replace(/\r\n?/g, "\n");
  const lines = text.split("\n");
  const closing = lines.indexOf("---", 1);
  const frontmatter = lines.slice(1, closing);
  const field = (key) => yamlScalar(frontmatter.find((line) => line.startsWith(`${key}:`))?.slice(key.length + 1));
  const description = field("description");
  const lower = description.toLowerCase();
  const useWhen = lower.indexOf("use when");
  const doNot = lower.indexOf("do not use");
  const triggers = useWhen >= 0
    ? [...description.slice(useWhen, doNot > useWhen ? doNot : undefined).matchAll(/"([^"]+)"/g)].map((match) => match[1])
    : [];
  const positive = doNot >= 0 ? description.slice(0, doNot) : description;
  const nameParts = field("name").split("-");
  return {
    name: field("name"),
    description,
    usage_hint: firstSentence(description),
    body: lines.slice(closing + 1).join("\n").replace(/^\n+/, ""),
    directory,
    files: listFiles(directory).filter((file) => file !== "SKILL.md"),
    index: {
      name: [...nameParts, nameParts.map((part) => part[0]).join("")],
      triggers: tokenize(triggers.join(" ")),
      description: tokenize(positive),
      category: [CATEGORY]
    }
  };
}

function loadSkills() {
  return SKILL_IDS.map(loadSkill);
}

function tokenMatches(query, candidates) {
  return candidates.some((token) => token === query
    || (query.length >= 4 && token.length >= 4 && (token.startsWith(query) || query.startsWith(token))));
}

function scoreSkill(skill, queryTokens) {
  let score = 0;
  for (const [field, weight] of Object.entries(WEIGHTS)) {
    const matched = queryTokens.filter((token) => tokenMatches(token, skill.index[field])).length;
    score += weight * (matched / queryTokens.length);
  }
  return Math.round(score * 100);
}

function matchQuality(score) {
  if (score >= 45) return "exact";
  if (score >= 30) return "strong";
  if (score >= MATCH_FLOOR) return "partial";
  return "weak";
}

function blocked(reason, extra = {}) {
  return { status: "BLOCKED", reason, ...extra };
}

function findSkill(name) {
  const wanted = String(name ?? "").trim();
  if (!SKILL_IDS.includes(wanted)) return null;
  return loadSkill(wanted);
}

function resolveInsideWorkspace(input, kind) {
  const raw = String(input ?? "").trim();
  if (!raw) return { error: "PATH_REQUIRED" };
  const candidate = resolve(WORKSPACE_ROOT, raw);
  if (!existsSync(candidate)) return { error: "PATH_NOT_FOUND" };
  const real = realpathSync(candidate);
  if (real !== WORKSPACE_ROOT && !real.startsWith(`${WORKSPACE_ROOT}${sep}`)) return { error: "PATH_OUTSIDE_WORKSPACE" };
  const stat = statSync(real);
  if (kind === "file" && !stat.isFile()) return { error: "NOT_A_FILE" };
  if (kind === "directory" && !stat.isDirectory()) return { error: "NOT_A_DIRECTORY" };
  return { path: real, relative: toPosix(relative(WORKSPACE_ROOT, real)) || ".", size: stat.size };
}

function health() {
  const skills = loadSkills();
  return {
    status: "PASS",
    mcp: "architecture-knowledge",
    version: VERSION,
    mode: "offline-deterministic",
    network_access: false,
    write_access: false,
    skills: skills.map((skill) => ({ name: skill.name, files: skill.files.length })),
    knowledge_updated: KNOWLEDGE.updated,
    tools: listTools().length
  };
}

function listSkills(input = {}) {
  if (input.explicit_request !== true) {
    return blocked("EXPLICIT_REQUEST_REQUIRED", { guidance: "Call list_skills only when the user asks to browse; use search_skills for intent." });
  }
  const limit = Math.max(40, Math.min(Number(input.description_max_chars ?? 120) || 120, 240));
  const skills = loadSkills().map((skill) => ({
    name: skill.name,
    description: skill.description.length > limit ? `${skill.description.slice(0, limit - 1)}…` : skill.description
  }));
  return { status: "CATALOG", categories: [{ category: CATEGORY, skills }], total_skills: skills.length, total_categories: 1 };
}

function searchSkills(input = {}) {
  const query = String(input.query ?? "").trim();
  if (!query) return blocked("QUERY_REQUIRED", { message: "Query cannot be empty." });
  const queryTokens = tokenize(query);
  if (!queryTokens.length) return { status: "NO_MATCH", query, results: [], message: "The query has no searchable terms." };
  const results = loadSkills()
    .map((skill) => ({ skill, score: scoreSkill(skill, queryTokens) }))
    .filter(({ score }) => score >= MATCH_FLOOR)
    .sort((a, b) => b.score - a.score || a.skill.name.localeCompare(b.skill.name))
    .slice(0, MAX_SEARCH_RESULTS)
    .map(({ skill, score }) => ({ name: skill.name, category: CATEGORY, usage_hint: skill.usage_hint, score, match_quality: matchQuality(score) }));
  if (!results.length) return { status: "NO_MATCH", query, results: [], message: "No architecture knowledge skill applies to this query." };
  return { status: "RESULTS", query, results, next: "Call architecture_knowledge.read_skill with the best match." };
}

function readSkill(input = {}) {
  const skill = findSkill(input.skill_name);
  if (!skill) return blocked("SKILL_NOT_FOUND", { message: `Skill '${input.skill_name ?? ""}' not found. Use search_skills to find valid names.` });
  const meta = {
    skill: skill.name,
    skill_dir: toPosix(relative(WORKSPACE_ROOT, skill.directory)),
    files: skill.files.slice(0, MAX_LISTED_FILES),
    next: "Fetch only the files the instructions ask for with fetch_skill_files; run scripts from skill_dir."
  };
  return { [RAW]: [skill.body, JSON.stringify(meta, null, 2)] };
}

function fetchSkillFiles(input = {}) {
  const skill = findSkill(input.skill_name);
  if (!skill) return blocked("SKILL_NOT_FOUND", { message: `Skill '${input.skill_name ?? ""}' not found. Use search_skills to find valid names.` });
  const paths = input.file_paths;
  if (!Array.isArray(paths) || !paths.length || paths.some((path) => typeof path !== "string")) {
    return blocked("FILE_PATHS_REQUIRED", { valid_paths: skill.files });
  }
  if (paths.length > MAX_FETCH_FILES) return blocked("TOO_MANY_FILES", { max: MAX_FETCH_FILES });
  const invalid = paths.filter((path) => !skill.files.includes(path));
  if (invalid.length) return blocked("INVALID_FILE_PATHS", { invalid, valid_paths: skill.files });

  let remaining = RESPONSE_BUDGET_CHARS;
  const parts = [];
  const fetched = [];
  const truncated = [];
  const omitted = [];
  for (const path of paths) {
    const full = realpathSync(join(skill.directory, path));
    if (!full.startsWith(`${realpathSync(skill.directory)}${sep}`)) {
      omitted.push(path);
      continue;
    }
    if (remaining <= 0) {
      omitted.push(path);
      continue;
    }
    const header = `--- ${path} ---\n`;
    const content = readFileSync(full, "utf8");
    if (header.length + content.length > remaining) {
      parts.push(header + content.slice(0, Math.max(0, remaining - header.length)));
      truncated.push(path);
      remaining = 0;
    } else {
      parts.push(header + content);
      fetched.push(path);
      remaining -= header.length + content.length;
    }
  }
  const meta = { skill: skill.name, fetched, truncated, omitted, budget_chars: RESPONSE_BUDGET_CHARS };
  if (truncated.length || omitted.length) meta.next = "Request the truncated or omitted files in a follow-up call.";
  return { [RAW]: [parts.join("\n"), JSON.stringify(meta, null, 2)] };
}

function adrLint(input = {}) {
  const hasContent = typeof input.content === "string" && input.content.length > 0;
  const hasPath = typeof input.path === "string" && input.path.trim().length > 0;
  if (hasContent === hasPath) return blocked("CONTENT_OR_PATH_REQUIRED", { message: "Pass exactly one of content or path." });
  let text = input.content;
  let source = "inline";
  if (hasPath) {
    const target = resolveInsideWorkspace(input.path, "file");
    if (target.error) return blocked(target.error, { path: input.path });
    if (target.size > MAX_ADR_BYTES) return blocked("CONTENT_TOO_LARGE", { max_bytes: MAX_ADR_BYTES });
    text = readFileSync(target.path, "utf8");
    source = target.relative;
  } else if (Buffer.byteLength(text, "utf8") > MAX_ADR_BYTES) {
    return blocked("CONTENT_TOO_LARGE", { max_bytes: MAX_ADR_BYTES });
  }
  return { source, ...lintAdr(text, { strict: input.strict === true }) };
}

function adlIndex(input = {}) {
  const target = resolveInsideWorkspace(input.directory, "directory");
  if (target.error) return blocked(target.error, { directory: input.directory ?? null });
  if (input.today !== undefined && !/^\d{4}-\d{2}-\d{2}$/.test(String(input.today))) return blocked("TODAY_NOT_ISO");
  if (input.stale_days !== undefined && (!Number.isInteger(input.stale_days) || input.stale_days < 0)) return blocked("STALE_DAYS_INVALID");
  try {
    const result = scanLog(target.path, {
      today: input.today,
      staleDays: input.stale_days,
      nextTitle: typeof input.next_title === "string" ? input.next_title : undefined,
      nextCategory: typeof input.next_category === "string" ? input.next_category : ""
    });
    return { ...result, directory: target.relative };
  } catch (error) {
    return blocked("SCAN_FAILED", { message: error.message });
  }
}

function asrTest(input = {}) {
  return assessAsr({ requirement: input.requirement, criteria: input.criteria, rationale: input.rationale, scenario: input.scenario });
}

function sourceRefs(ids = []) {
  return ids.map((id) => {
    const source = KNOWLEDGE.sources.find((item) => item.id === id);
    return source ? { id, title: source.title, url: source.url ?? null } : { id };
  });
}

function concepts(input = {}) {
  const wanted = normalizeText(input.term ?? "").trim();
  const all = KNOWLEDGE.definitions;
  if (!wanted) {
    return { status: "KNOWLEDGE", definitions: all.map(({ term, name, pt, definition, skill }) => ({ term, name, pt: pt ?? null, definition, skill })) };
  }
  const labels = (entry) => [entry.term, entry.name, entry.pt].filter(Boolean).map(normalizeText);
  const exact = all.filter((entry) => labels(entry).includes(wanted));
  const matches = exact.length ? exact : all.filter((entry) => labels(entry).some((label) => label.includes(wanted)));
  if (!matches.length) return { status: "NOT_FOUND", term: input.term, available: all.map((entry) => entry.term) };
  return { status: "KNOWLEDGE", term: input.term, definitions: matches.map((entry) => ({ ...entry, sources: sourceRefs(entry.sources) })) };
}

function sources() {
  return {
    status: "KNOWLEDGE",
    sources: KNOWLEDGE.sources,
    templates: KNOWLEDGE.templates,
    lifecycle: KNOWLEDGE.lifecycle,
    tlc_baseline: KNOWLEDGE.tlc_baseline,
    tlc_pattern: KNOWLEDGE.tlc_pattern,
    workspace_conventions: KNOWLEDGE.workspace_conventions,
    freshness: {
      checked: KNOWLEDGE.evidence_checked,
      policy: "Recheck the latest MADR release and the TLC create-adr version before relying on template details."
    }
  };
}

function tool(name, description, properties = {}, required = []) {
  return { name, description, inputSchema: { type: "object", properties, required, additionalProperties: false } };
}

function listTools() {
  return [
    tool("architecture_knowledge.health", "Report server status, skills served, knowledge date and offline mode."),
    tool("architecture_knowledge.search_skills", "Step 1 of 3: find the ADR, ADL, ASR or AKM skill for an intent phrase; returns ranked names with a usage hint.", {
      query: { type: "string", description: "Short intent phrase, e.g. 'write an ADR' or 'requisito arquiteturalmente significativo'." }
    }, ["query"]),
    tool("architecture_knowledge.read_skill", "Step 2 of 3: load a skill's SKILL.md instructions (frontmatter stripped) and its bundled file list. Call search_skills first.", {
      skill_name: { type: "string" }
    }, ["skill_name"]),
    tool("architecture_knowledge.fetch_skill_files", "Step 3 of 3: fetch up to five files listed by read_skill, within a 50,000-character budget. Never guess paths.", {
      skill_name: { type: "string" },
      file_paths: { type: "array", items: { type: "string" }, maxItems: MAX_FETCH_FILES }
    }, ["skill_name", "file_paths"]),
    tool("architecture_knowledge.list_skills", "Browse the catalog grouped by category. Only when the user explicitly asks to list skills.", {
      explicit_request: { type: "boolean" },
      description_max_chars: { type: "integer", minimum: 40, maximum: 240 }
    }, ["explicit_request"]),
    tool("architecture_knowledge.adr_lint", "Lint one ADR (MADR, Nygard, Y-statement or AEOS template) from inline content or a workspace path; strict is the authoring gate.", {
      content: { type: "string" },
      path: { type: "string" },
      strict: { type: "boolean" }
    }),
    tool("architecture_knowledge.adl_index", "Read-only decision log scan of a workspace directory: index, integrity findings, lifecycle summary and next number.", {
      directory: { type: "string" },
      today: { type: "string", description: "YYYY-MM-DD used for stale proposal checks." },
      stale_days: { type: "integer", minimum: 0 },
      next_title: { type: "string" },
      next_category: { type: "string" }
    }, ["directory"]),
    tool("architecture_knowledge.asr_test", "Qualitative seven-criteria ASR Test plus quality attribute scenario completeness for one requirement.", {
      requirement: { type: "string" },
      criteria: { type: "object", description: "Keys C1..C7 or value_risk, key_concern, new_qos, external_dependency, cross_cutting, first_of_a_kind, past_problems." },
      rationale: { type: "object" },
      scenario: { type: "object", description: "source, stimulus, environment, artifact, response, response_measure." }
    }, ["requirement", "criteria"]),
    tool("architecture_knowledge.concepts", "Definitions of AD, ASR, ADR, ADL, AKM, MADR, Y-statement, MRM, START, ecADR, QAS and the adoption model with sources.", {
      term: { type: "string" }
    }),
    tool("architecture_knowledge.sources", "Dated sources, template versions, lifecycle rules, the TLC create-adr baseline and its deltas to current guidance.")
  ];
}

const HANDLERS = {
  "architecture_knowledge.health": health,
  "architecture_knowledge.search_skills": searchSkills,
  "architecture_knowledge.read_skill": readSkill,
  "architecture_knowledge.fetch_skill_files": fetchSkillFiles,
  "architecture_knowledge.list_skills": listSkills,
  "architecture_knowledge.adr_lint": adrLint,
  "architecture_knowledge.adl_index": adlIndex,
  "architecture_knowledge.asr_test": asrTest,
  "architecture_knowledge.concepts": concepts,
  "architecture_knowledge.sources": sources
};

export function callTool(name, input = {}) {
  const handler = HANDLERS[name];
  if (!handler) return { status: "ERROR", reason: "UNKNOWN_TOOL", tool: name };
  try {
    return handler(input ?? {});
  } catch (error) {
    return { status: "ERROR", reason: "TOOL_FAILED", tool: name, message: error.message };
  }
}

function toolResult(value) {
  if (value && value[RAW]) return { content: value[RAW].map((text) => ({ type: "text", text })), isError: false };
  return { content: [{ type: "text", text: JSON.stringify(value, null, 2) }], isError: ["BLOCKED", "ERROR"].includes(value?.status) };
}

export function handle(message) {
  if (Array.isArray(message)) return message.map(handle).filter(Boolean);
  const { id, method, params = {} } = message || {};
  if (method === "initialize") {
    return {
      jsonrpc: "2.0",
      id,
      result: {
        protocolVersion: params.protocolVersion || "2024-11-05",
        capabilities: { tools: { listChanged: false } },
        serverInfo: { name: "aeos-architecture-knowledge", version: VERSION },
        instructions: "Search, read, then fetch the ADR, ADL, ASR and AKM skills; lint ADRs, scan decision logs and run the ASR Test offline."
      }
    };
  }
  if (method === "notifications/initialized") return null;
  if (method === "ping") return { jsonrpc: "2.0", id, result: {} };
  if (method === "tools/list") return { jsonrpc: "2.0", id, result: { tools: listTools() } };
  if (method === "tools/call") return { jsonrpc: "2.0", id, result: toolResult(callTool(params.name, params.arguments || {})) };
  if (id == null) return null;
  return { jsonrpc: "2.0", id, error: { code: -32601, message: `Unknown method: ${method}` } };
}

// Replies use the framing of the request: newline-delimited JSON is the MCP stdio transport used by
// MCP clients, while the AEOS smoke and test harnesses send Content-Length frames.
function send(message, framed) {
  if (!message) return;
  const payload = JSON.stringify(message);
  process.stdout.write(framed ? `Content-Length: ${Buffer.byteLength(payload, "utf8")}\r\n\r\n${payload}` : `${payload}\n`);
}

function dispatch(raw, framed) {
  let message;
  try {
    message = JSON.parse(raw);
  } catch {
    send({ jsonrpc: "2.0", id: null, error: { code: -32700, message: "Invalid JSON" } }, framed);
    return;
  }
  send(handle(message), framed);
}

let buffer = Buffer.alloc(0);

function parse() {
  while (buffer.length) {
    const text = buffer.toString("utf8", 0, Math.min(buffer.length, 64));
    if (/^Content-Length:/i.test(text)) {
      let headerEnd = buffer.indexOf("\r\n\r\n");
      let separator = 4;
      if (headerEnd < 0) {
        headerEnd = buffer.indexOf("\n\n");
        separator = 2;
      }
      if (headerEnd < 0) return;
      const match = /Content-Length:\s*(\d+)/i.exec(buffer.slice(0, headerEnd).toString("utf8"));
      const start = headerEnd + separator;
      if (!match) {
        buffer = buffer.slice(start);
        continue;
      }
      const length = Number(match[1]);
      if (buffer.length < start + length) return;
      const body = buffer.slice(start, start + length).toString("utf8");
      buffer = buffer.slice(start + length);
      dispatch(body, true);
      continue;
    }
    const newline = buffer.indexOf("\n");
    if (newline < 0) return;
    const line = buffer.slice(0, newline).toString("utf8").trim();
    buffer = buffer.slice(newline + 1);
    if (line) dispatch(line, false);
  }
}

if (process.argv[1] && realpathSync(resolve(process.argv[1])) === fileURLToPath(import.meta.url)) {
  process.stdin.on("data", (chunk) => {
    buffer = Buffer.concat([buffer, chunk]);
    parse();
  });
}
