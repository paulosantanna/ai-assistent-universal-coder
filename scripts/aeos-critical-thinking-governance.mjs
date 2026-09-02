#!/usr/bin/env node
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

export const CRITICAL_THINKING_CONFIG_PATH = join(
  "aeos",
  "config",
  "critical-thinking-governance.config.json"
);

const VALID_RISK_LEVELS = new Set(["low", "medium", "high", "critical"]);
const REQUIRED_OUTPUT_FIELDS = [
  "facts",
  "assumptions",
  "evidence_refs",
  "risks",
  "recommendation",
  "confidence",
  "limitations",
  "blocking_conditions"
];

function unique(values) {
  return [...new Set(values)];
}

function normalize(value) {
  return String(value ?? "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
}

function includesTerm(context, term) {
  const normalizedTerm = normalize(term).trim();
  if (!normalizedTerm) return false;
  const escaped = normalizedTerm
    .replace(/[.*+?^${}()|[\]\\]/g, "\\$&")
    .replace(/\s+/g, "\\s+");
  return new RegExp(`(^|[^a-z0-9])${escaped}($|[^a-z0-9])`).test(context);
}

function hash(value) {
  return createHash("sha256").update(value).digest("hex");
}

export function loadCriticalThinkingConfig(repoRoot = resolve(process.cwd())) {
  return JSON.parse(readFileSync(join(repoRoot, CRITICAL_THINKING_CONFIG_PATH), "utf8"));
}

export function validateCriticalThinkingConfig(config) {
  const errors = [];
  const agents = Array.isArray(config?.agents) ? config.agents : [];
  const ids = agents.map((agent) => agent.id);
  const promptIds = agents.map((agent) => agent.prompt_id);
  const paths = agents.map((agent) => agent.path);
  const orders = agents.map((agent) => agent.order).sort((a, b) => a - b);
  const expectedOrders = Array.from({ length: 20 }, (_, index) => index + 1);
  const agentIds = new Set(ids);

  if (config?.scope !== "all_registered_skills") errors.push("scope must be all_registered_skills");
  if (config?.fail_closed !== true) errors.push("fail_closed must be true");
  if (agents.length !== 20) errors.push(`expected 20 specialist agents, found ${agents.length}`);
  if (new Set(ids).size !== ids.length) errors.push("agent ids must be unique");
  if (new Set(promptIds).size !== promptIds.length) errors.push("prompt ids must be unique");
  if (new Set(paths).size !== paths.length) errors.push("agent paths must be unique");
  if (JSON.stringify(orders) !== JSON.stringify(expectedOrders)) errors.push("agent orders must be the complete range 1..20");

  for (const [index, agent] of agents.entries()) {
    const expectedPromptId = `CT-${String(index + 1).padStart(2, "0")}`;
    if (agent.prompt_id !== expectedPromptId) errors.push(`agent order ${index + 1} must use ${expectedPromptId}`);
    if (!String(agent.path ?? "").startsWith("skills/critical-thinking-governor/agents/")) {
      errors.push(`agent ${agent.id ?? "?"} has an invalid package path`);
    }
    if (!Array.isArray(agent.triggers) || agent.triggers.length === 0) {
      errors.push(`agent ${agent.id ?? "?"} must declare triggers`);
    }
  }

  const baseline = Array.isArray(config?.baseline_agents) ? config.baseline_agents : [];
  if (baseline.length !== 4) errors.push("baseline_agents must contain exactly four agents");
  for (const id of baseline) if (!agentIds.has(id)) errors.push(`unknown baseline agent: ${id}`);

  if (!Number.isInteger(config?.min_agents) || config.min_agents < baseline.length) {
    errors.push("min_agents must be an integer greater than or equal to the baseline size");
  }
  if (!Number.isInteger(config?.max_agents) || config.max_agents < config.min_agents || config.max_agents >= agents.length) {
    errors.push("max_agents must be an integer >= min_agents and < 20");
  }

  for (const risk of VALID_RISK_LEVELS) {
    const overlay = config?.risk_overlays?.[risk];
    if (!Array.isArray(overlay)) errors.push(`missing risk overlay: ${risk}`);
    for (const id of overlay ?? []) if (!agentIds.has(id)) errors.push(`unknown ${risk} risk agent: ${id}`);
  }

  const outputFields = new Set(config?.required_output_fields ?? []);
  for (const field of REQUIRED_OUTPUT_FIELDS) {
    if (!outputFields.has(field)) errors.push(`missing required output field: ${field}`);
  }

  return { status: errors.length === 0 ? "PASS" : "FAIL", errors };
}

export function buildCriticalThinkingPlan({
  skillId,
  riskLevel = "medium",
  request = "",
  mission = "",
  config = loadCriticalThinkingConfig()
}) {
  const validation = validateCriticalThinkingConfig(config);
  const normalizedRisk = normalize(riskLevel);
  const context = normalize(`${skillId} ${mission} ${request}`);

  if (validation.status !== "PASS") {
    return {
      status: "FAIL",
      skillId,
      riskLevel: normalizedRisk,
      selectedAgents: [],
      blockingConditions: validation.errors,
      planHash: hash(JSON.stringify(validation.errors))
    };
  }

  if (!skillId) {
    return {
      status: "FAIL",
      skillId: "",
      riskLevel: normalizedRisk,
      selectedAgents: [],
      blockingConditions: ["skillId is required"],
      planHash: hash("missing-skill-id")
    };
  }

  if (!VALID_RISK_LEVELS.has(normalizedRisk)) {
    return {
      status: "FAIL",
      skillId,
      riskLevel: normalizedRisk,
      selectedAgents: [],
      blockingConditions: [`unsupported risk level: ${riskLevel}`],
      planHash: hash(`unsupported-risk:${riskLevel}`)
    };
  }

  const byId = new Map(config.agents.map((agent) => [agent.id, agent]));
  const riskAgents = config.risk_overlays[normalizedRisk];
  const requiredIds = unique([...config.baseline_agents, ...riskAgents]);
  const reasons = new Map([
    ...config.baseline_agents.map((id) => [id, "baseline"]),
    ...riskAgents.map((id) => [id, `risk:${normalizedRisk}`])
  ]);

  const triggered = config.agents
    .filter((agent) => !requiredIds.includes(agent.id))
    .map((agent) => {
      const matches = agent.triggers.filter((trigger) => includesTerm(context, trigger));
      const explicit = includesTerm(context, agent.id) || includesTerm(context, agent.name);
      const score = matches.reduce((total, trigger) => total + normalize(trigger).length, 0) + (explicit ? 1000 : 0);
      return { agent, matches, score };
    })
    .filter((candidate) => candidate.score > 0)
    .sort((left, right) => right.score - left.score || left.agent.order - right.agent.order);

  const selectedIds = [...requiredIds];
  for (const candidate of triggered) {
    if (selectedIds.length >= config.max_agents) break;
    selectedIds.push(candidate.agent.id);
    reasons.set(candidate.agent.id, `trigger:${candidate.matches.join("|") || "explicit"}`);
  }

  for (const agent of config.agents) {
    if (selectedIds.length >= config.min_agents) break;
    if (!selectedIds.includes(agent.id)) {
      selectedIds.push(agent.id);
      reasons.set(agent.id, "minimum-set");
    }
  }

  const selectedAgents = selectedIds
    .map((id) => byId.get(id))
    .filter(Boolean)
    .sort((left, right) => left.order - right.order)
    .map((agent) => ({
      id: agent.id,
      promptId: agent.prompt_id,
      name: agent.name,
      path: agent.path,
      reason: reasons.get(agent.id) ?? "selected"
    }));

  const blockingConditions = [];
  if (selectedAgents.length < config.min_agents) blockingConditions.push("selected agent count is below min_agents");
  if (selectedAgents.length > config.max_agents) blockingConditions.push("selected agent count exceeds max_agents");
  for (const id of requiredIds) {
    if (!selectedAgents.some((agent) => agent.id === id)) blockingConditions.push(`required agent missing: ${id}`);
  }

  const planData = {
    version: config.version,
    governingSkill: config.governing_skill,
    skillId,
    riskLevel: normalizedRisk,
    selectedAgents,
    requiredOutputFields: config.required_output_fields,
    failClosed: config.fail_closed
  };

  return {
    status: blockingConditions.length === 0 ? "PASS" : "FAIL",
    ...planData,
    blockingConditions,
    planHash: hash(JSON.stringify(planData))
  };
}

function parseCliArguments(args) {
  const options = { skillId: "manual-request", riskLevel: "medium", request: "" };
  const requestParts = [];
  for (let index = 0; index < args.length; index += 1) {
    if (args[index] === "--skill") options.skillId = args[++index] ?? "";
    else if (args[index] === "--risk") options.riskLevel = args[++index] ?? "";
    else requestParts.push(args[index]);
  }
  options.request = requestParts.join(" ").trim();
  return options;
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  const options = parseCliArguments(process.argv.slice(2));
  if (!options.request) {
    console.error("Usage: node scripts/aeos-critical-thinking-governance.mjs [--skill id] [--risk level] \"request\"");
    process.exit(2);
  }
  const result = buildCriticalThinkingPlan(options);
  console.log(JSON.stringify(result, null, 2));
  if (result.status !== "PASS") process.exit(1);
}
