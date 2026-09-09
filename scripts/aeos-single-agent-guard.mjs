#!/usr/bin/env node
import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { basename, extname, resolve } from "node:path";
import yaml from "js-yaml";

const { load, loadAll } = yaml;
const ROOT = resolve(process.cwd());
const CANONICAL_AGENT = "codenavi-agent";
const CANONICAL_AGENT_PATH = "AGENT.md";
const SELF = "scripts/aeos-single-agent-guard.mjs";

const join = (...parts) => parts.join("");
const OLD = Object.freeze({
  rootFile: join("ROOT", "_AGENT.md"),
  parentFile: join("PARENT", "_AGENT.md"),
  childFile: join("CHILD", "_AGENT.md"),
  oldPromptSuffix: join(".", "agent", ".md"),
  oldManifestSuffixYaml: join(".", "agent", ".yaml"),
  oldManifestSuffixYml: join(".", "agent", ".yml"),
  subordinateWord: join("sub", "agent"),
  subordinatePlural: join("sub", "agents")
});

const NEGATIVE_POLICY_ALLOWLIST = new Set([
  "AGENT.md",
  "AGENTS.md",
  "references/CODENAVI_FULL_WORKSPACE_STANDARD.md",
  "references/CODENAVI_WORKSPACE_STANDARD.md",
  SELF
]);

const TEXT_EXTENSIONS = new Set([
  ".md", ".mdx", ".yaml", ".yml", ".json", ".jsonl", ".ts", ".tsx", ".js", ".mjs", ".cjs",
  ".py", ".java", ".kt", ".kts", ".sh", ".ps1", ".toml", ".xml", ".properties", ".txt"
]);

function trackedFiles() {
  return execFileSync("git", ["ls-files", "-z"], { cwd: ROOT, encoding: "utf8" })
    .split("\0")
    .filter(Boolean)
    .map((path) => path.replaceAll("\\", "/"));
}

function read(path) {
  return readFileSync(resolve(ROOT, path), "utf8");
}

function push(errors, file, reason) {
  errors.push(`${file}: ${reason}`);
}

function fail(errors) {
  console.error(JSON.stringify({
    status: "FAIL",
    standard: "CodENavi Single Agent",
    canonicalAgent: CANONICAL_AGENT,
    violationCount: errors.length,
    errors
  }, null, 2));
  process.exit(1);
}

function isTextFile(file) {
  if (file === "Dockerfile" || basename(file).startsWith("Dockerfile.")) return true;
  return TEXT_EXTENSIONS.has(extname(file).toLowerCase());
}

function parseStructured(file, text) {
  const ext = extname(file).toLowerCase();
  if (ext === ".json") return [JSON.parse(text)];
  if (ext === ".yaml" || ext === ".yml") {
    const docs = [];
    loadAll(text, (doc) => docs.push(doc));
    return docs;
  }
  return [];
}

function scalarArray(value) {
  return Array.isArray(value) ? value.filter((item) => typeof item === "string") : [];
}

function walkStructured(node, file, errors, path = "$", seen = new Set()) {
  if (!node || typeof node !== "object") return;
  if (seen.has(node)) return;
  seen.add(node);

  if (Array.isArray(node)) {
    node.forEach((value, index) => walkStructured(value, file, errors, `${path}[${index}]`, seen));
    return;
  }

  const forbiddenKeys = new Set([
    join("parent", "_agent"),
    join("child", "_agent"),
    join("root", "_agent"),
    join("judge", "_agent"),
    join("can_delegate", "_to"),
    join("max_", OLD.subordinatePlural, "_per_task"),
    join("max_delegation", "_depth"),
    join("require_delegation", "_policy"),
    join("context_broadcast_to_all_", OLD.subordinatePlural)
  ]);

  for (const [key, value] of Object.entries(node)) {
    const keyPath = `${path}.${key}`;

    if (forbiddenKeys.has(key)) {
      push(errors, file, `${keyPath}: obsolete multi-agent key '${key}' is forbidden`);
    }

    if (key === "owner_agent" && value !== CANONICAL_AGENT) {
      push(errors, file, `${keyPath}: owner_agent must be '${CANONICAL_AGENT}', found '${String(value)}'`);
    }

    if (key === "required_agents") {
      const values = scalarArray(value);
      if (values.length !== 1 || values[0] !== CANONICAL_AGENT) {
        push(errors, file, `${keyPath}: required_agents must be [${CANONICAL_AGENT}], found [${values.join(", ")}]`);
      }
    }

    if (key === OLD.subordinatePlural) {
      if (!Array.isArray(value) || value.length !== 0) {
        push(errors, file, `${keyPath}: subordinate agent collections must be empty`);
      } else if (file !== "aeos/registries/agents.registry.yaml") {
        push(errors, file, `${keyPath}: obsolete subordinate-agent schema key is forbidden outside the canonical registry`);
      }
    }

    if (key === "agents" && file === "aeos/config/critical-thinking-governance.config.json") {
      push(errors, file, `${keyPath}: critical-thinking must use lenses, never agent identities`);
    }

    walkStructured(value, file, errors, keyPath, seen);
  }
}

const files = trackedFiles();
const errors = [];

const forbiddenPathRules = [
  { test: (file) => basename(file).toLowerCase() === OLD.rootFile.toLowerCase(), reason: `${OLD.rootFile} is forbidden` },
  { test: (file) => basename(file).toLowerCase() === OLD.parentFile.toLowerCase(), reason: `${OLD.parentFile} is forbidden` },
  { test: (file) => basename(file).toLowerCase() === OLD.childFile.toLowerCase(), reason: `${OLD.childFile} is forbidden` },
  { test: (file) => /(^|\/)aeos\/agents\//i.test(file), reason: "aeos/agents persona tree is forbidden" },
  { test: (file) => /(^|\/)aeos\/subagents\//i.test(file), reason: "aeos subordinate-agent tree is forbidden" },
  { test: (file) => /(^|\/)playbooks\/[^/]+\/agents\//i.test(file), reason: "playbook-specific agent persona tree is forbidden" },
  { test: (file) => file.toLowerCase().endsWith(join(".", OLD.subordinateWord, ".md")), reason: "subordinate-agent prompt file is forbidden" },
  { test: (file) => file.toLowerCase().endsWith(OLD.oldPromptSuffix), reason: "specialist agent prompt file is forbidden" },
  { test: (file) => file.toLowerCase().endsWith(OLD.oldManifestSuffixYaml) || file.toLowerCase().endsWith(OLD.oldManifestSuffixYml), reason: "specialist agent manifest is forbidden" },
  { test: (file) => /agents\.registry\.overlay\.ya?ml$/i.test(file), reason: "agent overlay registry is forbidden" }
];

for (const file of files) {
  for (const rule of forbiddenPathRules) {
    if (rule.test(file)) push(errors, file, rule.reason);
  }
}

const agentsRegistryPath = "aeos/registries/agents.registry.yaml";
try {
  const registry = load(read(agentsRegistryPath));
  const agents = Array.isArray(registry?.agents) ? registry.agents : [];
  const subordinateAgents = Array.isArray(registry?.[OLD.subordinatePlural]) ? registry[OLD.subordinatePlural] : [];
  if (agents.length !== 1) push(errors, agentsRegistryPath, `expected exactly one agent, found ${agents.length}`);
  const agent = agents[0] ?? {};
  if (agent.id !== CANONICAL_AGENT) push(errors, agentsRegistryPath, `only ${CANONICAL_AGENT} is allowed`);
  if (agent.path !== CANONICAL_AGENT_PATH) push(errors, agentsRegistryPath, `canonical agent must point to ${CANONICAL_AGENT_PATH}`);
  if (Number(agent.max_subagents) !== 0) push(errors, agentsRegistryPath, "max_subagents must be 0");
  if (agent.can_delegate === true) push(errors, agentsRegistryPath, "can_delegate must remain false");
  if (subordinateAgents.length !== 0) push(errors, agentsRegistryPath, "subordinate agent registry must be empty");
} catch (error) {
  push(errors, agentsRegistryPath, `cannot validate registry: ${error instanceof Error ? error.message : String(error)}`);
}

for (const file of files) {
  if (!isTextFile(file)) continue;

  let text;
  try {
    text = read(file);
  } catch (error) {
    push(errors, file, `cannot read tracked text file: ${error instanceof Error ? error.message : String(error)}`);
    continue;
  }

  const ext = extname(file).toLowerCase();
  if (ext === ".json" || ext === ".yaml" || ext === ".yml") {
    try {
      for (const document of parseStructured(file, text)) walkStructured(document, file, errors);
    } catch (error) {
      push(errors, file, `cannot parse structured file: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  if (file === SELF) continue;

  const exactArtifacts = [OLD.rootFile, OLD.parentFile, OLD.childFile];
  for (const artifact of exactArtifacts) {
    if (text.toLowerCase().includes(artifact.toLowerCase())) {
      push(errors, file, `obsolete agent artifact reference '${artifact}' is forbidden`);
    }
  }

  if (!NEGATIVE_POLICY_ALLOWLIST.has(file)) {
    const subordinateRe = new RegExp(`\\b${OLD.subordinateWord}s?\\b`, "i");
    if (subordinateRe.test(text)) push(errors, file, "obsolete subordinate-agent model reference is forbidden");

    const personaPatterns = [
      /\b(?:root|parent|child|judge)\s+agent\b/i,
      /\bagent\s+hierarch(?:y|ies|ical)\b/i,
      /\bparent[- ]child\s+(?:agent|delegation|hierarch)/i,
      /\bquality[- ]judge\b/i,
      /\btarget_role\s*:\s*(?:ROOT|PARENT|CHILD|JUDGE)\b/i,
      /\bdelegat(?:e|ion)\s+(?:to|between)\s+agents?\b/i
    ];
    for (const pattern of personaPatterns) {
      if (pattern.test(text)) {
        push(errors, file, `obsolete multi-agent persona/delegation reference matched ${pattern}`);
        break;
      }
    }
  }
}

const criticalConfigPath = "aeos/config/critical-thinking-governance.config.json";
if (files.includes(criticalConfigPath)) {
  try {
    const config = JSON.parse(read(criticalConfigPath));
    if (!Array.isArray(config.lenses) || config.lenses.length !== 20) push(errors, criticalConfigPath, "expected exactly 20 critical-thinking lenses");
    for (const lens of config.lenses ?? []) {
      if ("path" in lens) push(errors, criticalConfigPath, `lens '${lens.id ?? "?"}' must not point to an agent prompt path`);
    }
  } catch (error) {
    push(errors, criticalConfigPath, `invalid JSON: ${error instanceof Error ? error.message : String(error)}`);
  }
}

const uniqueErrors = [...new Set(errors)].sort();
if (uniqueErrors.length > 0) fail(uniqueErrors);

console.log(JSON.stringify({
  status: "PASS",
  standard: "CodENavi Single Agent",
  canonicalAgent: CANONICAL_AGENT,
  trackedFiles: files.length,
  obsoleteAgentArtifacts: 0,
  subordinateAgentModels: 0,
  historicalOwners: 0,
  historicalRequiredAgents: 0
}, null, 2));
