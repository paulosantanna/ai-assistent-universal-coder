#!/usr/bin/env node
import { readFileSync } from "node:fs";
import { extname, resolve } from "node:path";
import yaml from "js-yaml";
import { listGitTrackedFiles } from "./lib/git-tracked-files.mjs";

const { load } = yaml;
const ROOT = resolve(process.cwd());
const CANONICAL_AGENT = "codenavi-agent";
const CANONICAL_AGENT_PATH = "AGENT.md";

function trackedFiles() {
  return listGitTrackedFiles({ cwd: ROOT });
}

function read(path) {
  return readFileSync(resolve(ROOT, path), "utf8");
}

function fail(errors) {
  console.error(JSON.stringify({
    status: "FAIL",
    standard: "CodENavi Single Agent",
    canonicalAgent: CANONICAL_AGENT,
    errors
  }, null, 2));
  process.exit(1);
}

const files = trackedFiles();
const errors = [];

const forbiddenPathRules = [
  { re: /(^|\/)ROOT_AGENT\.md$/i, reason: "ROOT_AGENT legacy constitution is forbidden" },
  { re: /(^|\/)PARENT_AGENT\.md$/i, reason: "PARENT_AGENT legacy constitution is forbidden" },
  { re: /(^|\/)CHILD_AGENT\.md$/i, reason: "CHILD_AGENT legacy constitution is forbidden" },
  { re: /(^|\/)aeos\/agents\//i, reason: "aeos/agents personas are forbidden" },
  { re: /(^|\/)aeos\/subagents\//i, reason: "aeos/subagents are forbidden" },
  { re: /(^|\/)playbooks\/[^/]+\/agents\//i, reason: "playbook-specific agent personas are forbidden" },
  { re: /\.subagent\.md$/i, reason: "subagent prompt files are forbidden" },
  { re: /\.agent\.md$/i, reason: "specialist agent prompt files are forbidden" },
  { re: /\.agent\.ya?ml$/i, reason: "specialist agent manifests are forbidden" },
  { re: /agents\.registry\.overlay\.ya?ml$/i, reason: "agent overlay registries are forbidden" }
];

for (const file of files) {
  for (const rule of forbiddenPathRules) {
    if (rule.re.test(file)) errors.push(`${file}: ${rule.reason}`);
  }
}

const agentsRegistryPath = "aeos/registries/agents.registry.yaml";
try {
  const registry = load(read(agentsRegistryPath));
  const agents = Array.isArray(registry?.agents) ? registry.agents : [];
  const subagents = Array.isArray(registry?.subagents) ? registry.subagents : [];
  if (agents.length !== 1) errors.push(`${agentsRegistryPath}: expected exactly one agent, found ${agents.length}`);
  const agent = agents[0] ?? {};
  if (agent.id !== CANONICAL_AGENT) errors.push(`${agentsRegistryPath}: only ${CANONICAL_AGENT} is allowed`);
  if (agent.path !== CANONICAL_AGENT_PATH) errors.push(`${agentsRegistryPath}: canonical agent must point to ${CANONICAL_AGENT_PATH}`);
  if (Number(agent.max_subagents) !== 0) errors.push(`${agentsRegistryPath}: max_subagents must be 0`);
  if (agent.can_delegate === true) errors.push(`${agentsRegistryPath}: can_delegate must not enable subagent delegation`);
  if (subagents.length !== 0) errors.push(`${agentsRegistryPath}: subagents must be empty`);
} catch (error) {
  errors.push(`${agentsRegistryPath}: cannot validate registry: ${error instanceof Error ? error.message : String(error)}`);
}

const registryLike = files.filter((file) => {
  const extension = extname(file).toLowerCase();
  if (extension !== ".yaml" && extension !== ".yml" && extension !== ".json") return false;
  return file.startsWith("aeos/registries/") || file.includes("/registries/") || file.startsWith("aeos/config/");
});

for (const file of registryLike) {
  let text;
  try {
    text = read(file);
  } catch {
    continue;
  }

  for (const match of text.matchAll(/^\s*owner_agent:\s*([^\s#]+).*$/gm)) {
    const owner = match[1];
    if (owner !== CANONICAL_AGENT) errors.push(`${file}: legacy owner_agent '${owner}'`);
  }

  for (const match of text.matchAll(/^\s*required_agents:\s*\[([^\]]*)\].*$/gm)) {
    const values = match[1].split(",").map((value) => value.trim().replace(/^['"]|['"]$/g, "")).filter(Boolean);
    if (values.length !== 1 || values[0] !== CANONICAL_AGENT) {
      errors.push(`${file}: required_agents must be [${CANONICAL_AGENT}], found [${values.join(", ")}]`);
    }
  }

  if (/^\s*subagents:\s*\n\s*-\s+/m.test(text)) errors.push(`${file}: non-empty subagents block is forbidden`);
}

const permissionsPath = "aeos/config/permissions.yaml";
if (files.includes(permissionsPath)) {
  const text = read(permissionsPath);
  const forbiddenRoles = [
    "root", "architect", "coder", "tester", "security", "devops", "judge", "documenter",
    "planner", "orchestrator", "researcher", "incident", "ops", "packaging", "generated", "governance"
  ];
  for (const role of forbiddenRoles) {
    if (new RegExp(`^\\s{2}${role}:\\s*$`, "m").test(text)) errors.push(`${permissionsPath}: legacy role '${role}' remains`);
  }
}

const criticalConfigPath = "aeos/config/critical-thinking-governance.config.json";
if (files.includes(criticalConfigPath)) {
  try {
    const config = JSON.parse(read(criticalConfigPath));
    if (!Array.isArray(config.lenses) || config.lenses.length !== 20) errors.push(`${criticalConfigPath}: expected 20 lenses`);
    if ("agents" in config || "baseline_agents" in config || "min_agents" in config || "max_agents" in config) {
      errors.push(`${criticalConfigPath}: critical-thinking agents are forbidden; use lenses`);
    }
    for (const lens of config.lenses ?? []) {
      if ("path" in lens) errors.push(`${criticalConfigPath}: lens '${lens.id ?? "?"}' must not point to an agent prompt path`);
    }
  } catch (error) {
    errors.push(`${criticalConfigPath}: invalid JSON: ${error instanceof Error ? error.message : String(error)}`);
  }
}

if (errors.length > 0) fail(errors);

console.log(JSON.stringify({
  status: "PASS",
  standard: "CodENavi Single Agent",
  canonicalAgent: CANONICAL_AGENT,
  trackedFiles: files.length,
  forbiddenLegacyAgentFiles: 0,
  subagents: 0
}, null, 2));
