#!/usr/bin/env node
// asr_test — qualitative triage of one requirement with Zimmermann's seven-criteria ASR Test plus a
// completeness check of its six-part quality attribute scenario. It counts criteria met; it is
// deliberately not a weight calculator (the method warns against pseudo-accuracy).
//
// Usage: node asr_test.mjs <input.json>   (use "-" to read the JSON from stdin)
// Exit codes: 0 assessed, 1 blocked input, 2 usage or read error.

import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

export const ASR_CRITERIA = [
  { id: "C1", key: "value_risk", label: "High business value (benefit versus cost) or business risk" },
  { id: "C2", key: "key_concern", label: "Concern of a particularly important stakeholder, such as the sponsor or a compliance auditor" },
  { id: "C3", key: "new_qos", label: "Runtime quality of service that deviates substantially from what the architecture already satisfies" },
  { id: "C4", key: "external_dependency", label: "New or existing external dependency with unpredictable, unreliable or uncontrollable behavior" },
  { id: "C5", key: "cross_cutting", label: "Cross-cutting nature with impact on several parts of the system, possibly system-wide" },
  { id: "C6", key: "first_of_a_kind", label: "First of a kind: the team has never built something that satisfies it" },
  { id: "C7", key: "past_problems", label: "Caused critical situations, budget overruns or client dissatisfaction on a similar past project" }
];

export const QAS_PARTS = ["source", "stimulus", "environment", "artifact", "response", "response_measure"];

const MAX_REQUIREMENT_CHARS = 2000;
const MET = new Set(["y", "yes", "s", "sim", "si", "h", "m", "true"]);
const NOT_MET = new Set(["n", "no", "nao", "l", "n/a", "na", "false"]);
const UNKNOWN = new Set(["?", "unknown", "desconhecido", "desconocido"]);

const RECOMMENDATIONS = {
  significant: "Treat it as an ASR: record it in the ASR register and capture every architectural decision it drives as an ADR that cites the ASR id.",
  open: "Unknown criteria could make it significant: ask the stakeholders, prototype or spike, and keep it in the decision backlog until resolved.",
  borderline: "Team-level concern: discuss it with the team; an ADR is optional unless a hard-to-reverse decision follows.",
  "not-significant": "Not architecturally significant: handle it in normal design and code review without an ADR."
};

function key(value) {
  return String(value).normalize("NFD").replace(/[\u0300-\u036f]/g, "").trim().toLowerCase();
}

function criterionFor(name) {
  const wanted = key(name);
  return ASR_CRITERIA.find((criterion) => criterion.id.toLowerCase() === wanted || criterion.key === wanted) ?? null;
}

function interpret(value) {
  if (typeof value === "boolean") return { met: value, unknown: false, count: value ? 1 : 0 };
  if (typeof value === "number") {
    return Number.isInteger(value) && value >= 0 ? { met: value > 0, unknown: false, count: value } : null;
  }
  if (value === null || value === undefined) return { met: false, unknown: true, count: 0 };
  const text = key(value);
  if (/^\d+$/.test(text)) return interpret(Number(text));
  if (MET.has(text)) return { met: true, unknown: false, count: 1 };
  if (NOT_MET.has(text)) return { met: false, unknown: false, count: 0 };
  if (UNKNOWN.has(text)) return { met: false, unknown: true, count: 0 };
  return null;
}

function band(metCount) {
  if (metCount >= 4) return "high";
  if (metCount >= 2) return "medium-high";
  if (metCount === 1) return "low-medium";
  return "low";
}

function significance(metCount, unknownCount) {
  if (metCount >= 2) return "significant";
  if (metCount + unknownCount >= 2) return "open";
  if (metCount === 1) return "borderline";
  return "not-significant";
}

function checkScenario(scenario) {
  if (!scenario || typeof scenario !== "object") return null;
  const missing = QAS_PARTS.filter((part) => !String(scenario[part] ?? "").trim());
  const measure = String(scenario.response_measure ?? "");
  return {
    complete: missing.length === 0,
    missing,
    measurable_response: /\d/.test(measure) || /\b(zero|none|nenhum|nenhuma|cero|ninguno|ninguna)\b/i.test(measure)
  };
}

/** Assess one requirement; returns BLOCKED with a reason for malformed input. */
export function assessAsr(input = {}) {
  const requirement = String(input.requirement ?? "").trim();
  if (!requirement) return { status: "BLOCKED", reason: "REQUIREMENT_REQUIRED" };
  if (requirement.length > MAX_REQUIREMENT_CHARS) return { status: "BLOCKED", reason: "REQUIREMENT_TOO_LONG", max: MAX_REQUIREMENT_CHARS };
  const criteriaInput = input.criteria;
  if (!criteriaInput || typeof criteriaInput !== "object" || Array.isArray(criteriaInput) || !Object.keys(criteriaInput).length) {
    return { status: "BLOCKED", reason: "CRITERIA_REQUIRED", criteria: ASR_CRITERIA.map(({ id, key: name, label }) => ({ id, key: name, label })) };
  }

  const values = new Map();
  const unknownNames = [];
  const invalid = [];
  for (const [name, value] of Object.entries(criteriaInput)) {
    const criterion = criterionFor(name);
    if (!criterion) {
      unknownNames.push(name);
      continue;
    }
    const parsed = interpret(value);
    if (!parsed) invalid.push(name);
    else values.set(criterion.id, { value, ...parsed });
  }
  if (unknownNames.length) return { status: "BLOCKED", reason: "UNKNOWN_CRITERION", criteria: unknownNames };
  if (invalid.length) {
    return { status: "BLOCKED", reason: "INVALID_CRITERION_VALUE", criteria: invalid, accepted: "Y, N, ?, H, M, L, n/a, true, false or a non-negative count" };
  }

  const rationale = input.rationale && typeof input.rationale === "object" ? input.rationale : {};
  const rationaleFor = (criterion) => {
    const entry = Object.entries(rationale).find(([name]) => criterionFor(name)?.id === criterion.id);
    return entry ? String(entry[1]) : null;
  };
  const criteria = ASR_CRITERIA.map((criterion) => {
    const assessed = values.get(criterion.id) ?? { value: null, met: false, unknown: true, count: 0 };
    return { ...criterion, ...assessed, assessed: values.has(criterion.id), rationale: rationaleFor(criterion) };
  });
  const met = criteria.filter((criterion) => criterion.met).map((criterion) => criterion.id);
  const unknown = criteria.filter((criterion) => criterion.unknown).map((criterion) => criterion.id);
  const level = band(met.length);
  const verdict = significance(met.length, unknown.length);
  const scenario = checkScenario(input.scenario);

  const nextSteps = [RECOMMENDATIONS[verdict]];
  if (level === "high") nextSteps.push("Its most responsible moment is probably now: decisions it drives are early, big decisions.");
  if (met.includes("C3") && (!scenario || !scenario.complete || !scenario.measurable_response)) {
    nextSteps.push("Express the quality requirement as a six-part quality attribute scenario with a measurable response measure.");
  }
  if (unknown.length) nextSteps.push(`Resolve the unknown criteria: ${unknown.join(", ")}.`);

  return {
    status: "ASSESSED",
    requirement,
    criteria,
    met,
    unknown,
    instances: criteria.reduce((sum, criterion) => sum + criterion.count, 0),
    band: level,
    significance: verdict,
    open: unknown.length > 0,
    next_steps: nextSteps,
    scenario,
    method: "Zimmermann ASR Test (ECSA 2020): qualitative triage that makes tacit relevance judgments explicit; not a weight calculator."
  };
}

function main(argv) {
  const target = argv[2];
  if (!target || argv.length > 3) {
    console.error("usage: node asr_test.mjs <input.json | ->");
    return 2;
  }
  let input;
  try {
    input = JSON.parse(readFileSync(target === "-" ? 0 : resolve(target), "utf8"));
  } catch (error) {
    console.error(JSON.stringify({ status: "ERROR", reason: "INPUT_UNREADABLE", message: error.message }));
    return 2;
  }
  const result = assessAsr(input);
  console.log(JSON.stringify(result, null, 2));
  return result.status === "ASSESSED" ? 0 : 1;
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  process.exitCode = main(process.argv);
}
