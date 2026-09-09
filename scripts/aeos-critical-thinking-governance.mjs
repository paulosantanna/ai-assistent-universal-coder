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
  const lenses = Array.isArray(config?.lenses) ? config.lenses : [];
  const ids = lenses.map((lens) => lens.id);
  const promptIds = lenses.map((lens) => lens.prompt_id);
  const orders = lenses.map((lens) => lens.order).sort((a, b) => a - b);
  const expectedOrders = Array.from({ length: 20 }, (_, index) => index + 1);
  const lensIds = new Set(ids);

  if (config?.scope !== "all_registered_skills") errors.push("scope must be all_registered_skills");
  if (config?.fail_closed !== true) errors.push("fail_closed must be true");
  if (lenses.length !== 20) errors.push(`expected 20 critical-thinking lenses, found ${lenses.length}`);
  if (new Set(ids).size !== ids.length) errors.push("lens ids must be unique");
  if (new Set(promptIds).size !== promptIds.length) errors.push("lens prompt ids must be unique");
  if (JSON.stringify(orders) !== JSON.stringify(expectedOrders)) errors.push("lens orders must be the complete range 1..20");

  for (const [index, lens] of lenses.entries()) {
    const expectedPromptId = `CT-${String(index + 1).padStart(2, "0")}`;
    if (lens.prompt_id !== expectedPromptId) errors.push(`lens order ${index + 1} must use ${expectedPromptId}`);
    if (!Array.isArray(lens.triggers) || lens.triggers.length === 0) {
      errors.push(`lens ${lens.id ?? "?"} must declare triggers`);
    }
  }

  const baseline = Array.isArray(config?.baseline_lenses) ? config.baseline_lenses : [];
  if (baseline.length !== 4) errors.push("baseline_lenses must contain exactly four lenses");
  for (const id of baseline) if (!lensIds.has(id)) errors.push(`unknown baseline lens: ${id}`);

  if (!Number.isInteger(config?.min_lenses) || config.min_lenses < baseline.length) {
    errors.push("min_lenses must be an integer greater than or equal to the baseline size");
  }
  if (!Number.isInteger(config?.max_lenses) || config.max_lenses < config.min_lenses || config.max_lenses >= lenses.length) {
    errors.push("max_lenses must be an integer >= min_lenses and < 20");
  }

  for (const risk of VALID_RISK_LEVELS) {
    const overlay = config?.risk_overlays?.[risk];
    if (!Array.isArray(overlay)) errors.push(`missing risk overlay: ${risk}`);
    for (const id of overlay ?? []) if (!lensIds.has(id)) errors.push(`unknown ${risk} risk lens: ${id}`);
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
      selectedLenses: [],
      blockingConditions: validation.errors,
      planHash: hash(JSON.stringify(validation.errors))
    };
  }

  if (!skillId) {
    return {
      status: "FAIL",
      skillId: "",
      riskLevel: normalizedRisk,
      selectedLenses: [],
      blockingConditions: ["skillId is required"],
      planHash: hash("missing-skill-id")
    };
  }

  if (!VALID_RISK_LEVELS.has(normalizedRisk)) {
    return {
      status: "FAIL",
      skillId,
      riskLevel: normalizedRisk,
      selectedLenses: [],
      blockingConditions: [`unsupported risk level: ${riskLevel}`],
      planHash: hash(`unsupported-risk:${riskLevel}`)
    };
  }

  const byId = new Map(config.lenses.map((lens) => [lens.id, lens]));
  const riskLenses = config.risk_overlays[normalizedRisk];
  const requiredIds = unique([...config.baseline_lenses, ...riskLenses]);
  const reasons = new Map([
    ...config.baseline_lenses.map((id) => [id, "baseline"]),
    ...riskLenses.map((id) => [id, `risk:${normalizedRisk}`])
  ]);

  const triggered = config.lenses
    .filter((lens) => !requiredIds.includes(lens.id))
    .map((lens) => {
      const matches = lens.triggers.filter((trigger) => includesTerm(context, trigger));
      const explicit = includesTerm(context, lens.id) || includesTerm(context, lens.name);
      const score = matches.reduce((total, trigger) => total + normalize(trigger).length, 0) + (explicit ? 1000 : 0);
      return { lens, matches, score };
    })
    .filter((candidate) => candidate.score > 0)
    .sort((left, right) => right.score - left.score || left.lens.order - right.lens.order);

  const selectedIds = [...requiredIds];
  for (const candidate of triggered) {
    if (selectedIds.length >= config.max_lenses) break;
    selectedIds.push(candidate.lens.id);
    reasons.set(candidate.lens.id, `trigger:${candidate.matches.join("|") || "explicit"}`);
  }

  for (const lens of config.lenses) {
    if (selectedIds.length >= config.min_lenses) break;
    if (!selectedIds.includes(lens.id)) {
      selectedIds.push(lens.id);
      reasons.set(lens.id, "minimum-set");
    }
  }

  const selectedLenses = selectedIds
    .map((id) => byId.get(id))
    .filter(Boolean)
    .sort((left, right) => left.order - right.order)
    .map((lens) => ({
      id: lens.id,
      promptId: lens.prompt_id,
      name: lens.name,
      reason: reasons.get(lens.id) ?? "selected"
    }));

  const blockingConditions = [];
  if (selectedLenses.length < config.min_lenses) blockingConditions.push("selected lens count is below min_lenses");
  if (selectedLenses.length > config.max_lenses) blockingConditions.push("selected lens count exceeds max_lenses");
  for (const id of requiredIds) {
    if (!selectedLenses.some((lens) => lens.id === id)) blockingConditions.push(`required lens missing: ${id}`);
  }

  const planData = {
    version: config.version,
    governingSkill: config.governing_skill,
    skillId,
    riskLevel: normalizedRisk,
    selectedLenses,
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
