#!/usr/bin/env node
// Freezes the user request as the only oracle and refuses a later edit that
// would make a failing application look successful. Zero dependencies.
//
// Exit codes: 0 frozen or PASS, 1 invalid input, 2 oracle tamper or an open
// failure blocking a new request, 3 application failure recorded for the next window.

import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, rmSync, statSync, writeFileSync } from "node:fs";
import { dirname, isAbsolute, relative, resolve } from "node:path";
import { pathToFileURL } from "node:url";

export const SURFACES = new Set(["browser", "http", "cli", "job"]);
export const STATE_VERSION = 1;
const MAX_EVIDENCE_BYTES = 1_000_000;
const MIN_CONTEXT_CHARS = 16;

const FORBIDDEN = [
  /teste\s+unit[aá]rio/i,
  /\bunit\s+tests?\b/i,
  /teste\s+de\s+classe/i,
  /\bclass\s+tests?\b/i,
  /para\s+(?:o\s+|que\s+o\s+)?teste\s+pass/i,
  /so\s+(?:that\s+)?the\s+test\s+passes/i,
  /\bmake\s+the\s+test\s+pass\b/i,
  /espelh(?:ar|a)\s+o\s+c[oó]digo/i,
  /basead[oa]\s+n[oa]\s+(?:c[oó]digo|implementa)/i,
  /match(?:es|ing)?\s+the\s+(?:current\s+)?(?:implementation|code)/i,
  /comportamento\s+atual\s+do\s+c[oó]digo/i,
  /oracle\s+is\s+the\s+(?:code|implementation)/i,
  /ajust(?:ar|e|ei)\s+o\s+teste/i,
  /weaken(?:ed)?\s+(?:the\s+)?expect/i
];

const SECRET_MARKERS = [
  /(?:api[_-]?key|client[_-]?secret|access[_-]?token|password|passwd|pwd|senha)\s*[:=]\s*['"][^'"\s]{8,}['"]/i,
  /\b(?:sk-|ghp_|github_pat_|AKIA|xox[baprs]-)[A-Za-z0-9]{8,}/
];

function sha(value) {
  return createHash("sha256").update(value).digest("hex");
}

function fail(code, errors) {
  return { ok: false, code, errors };
}

function asText(value) {
  return typeof value === "string" ? value.trim() : "";
}

export function canonicalCharter(charter) {
  return {
    oracle_source: "user_request",
    user_request: asText(charter.user_request),
    checks: (charter.checks ?? []).map((check) => ({
      id: asText(check.id),
      surface: asText(check.surface),
      requested_behavior: asText(check.requested_behavior),
      steps: Array.isArray(check.steps) ? check.steps.map((step) => asText(step)) : [],
      expect: asText(check.expect)
    }))
  };
}

export function validateCharter(charter) {
  const errors = [];
  if (!charter || typeof charter !== "object" || Array.isArray(charter)) {
    return { ok: false, errors: ["Charter must be an object."] };
  }
  if (charter.oracle_source !== "user_request") {
    errors.push("oracle_source must be user_request. The implementation is not an oracle.");
  }
  if (charter.derived_from !== undefined && charter.derived_from !== "user_request") {
    errors.push("derived_from must be user_request.");
  }

  const canonical = canonicalCharter(charter);
  const serialized = JSON.stringify(canonical);
  if (SECRET_MARKERS.some((pattern) => pattern.test(serialized))) {
    errors.push("Charter contains a credential-like value. Remove it before freezing.");
  }
  if (!canonical.user_request) errors.push("user_request is required.");
  if (!Array.isArray(charter.checks) || canonical.checks.length === 0) errors.push("At least one check is required.");

  const seen = new Set();
  for (const check of canonical.checks) {
    if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(check.id)) errors.push(`Check id '${check.id}' must be kebab-case.`);
    if (seen.has(check.id)) errors.push(`Duplicate check id '${check.id}'.`);
    seen.add(check.id);
    if (!SURFACES.has(check.surface)) errors.push(`Check '${check.id}' must use surface browser, http, cli, or job.`);
    if (check.requested_behavior.length < 12) errors.push(`Check '${check.id}' requested_behavior must describe the user-visible outcome.`);
    if (check.expect.length < 12) errors.push(`Check '${check.id}' expect must describe the outcome the user asked for.`);
    if (check.steps.length === 0 || check.steps.some((step) => !step)) errors.push(`Check '${check.id}' needs at least one concrete step.`);
    const haystack = `${check.requested_behavior}\n${check.expect}\n${check.steps.join("\n")}`;
    if (FORBIDDEN.some((pattern) => pattern.test(haystack))) {
      errors.push(`Check '${check.id}' derives its expectation from the implementation or from making the test pass.`);
    }
  }

  return errors.length === 0 ? { ok: true, charter: canonical } : { ok: false, errors };
}

function readableState(previous) {
  if (previous == null) return null;
  if (typeof previous !== "object" || previous.version !== STATE_VERSION) {
    return fail("INVALID_STATE", ["State file is not a tests-expert charter state."]);
  }
  if (typeof previous.charter_hash !== "string" || typeof previous.user_request_hash !== "string") {
    return fail("INVALID_STATE", ["State file is missing charter hashes."]);
  }
  return null;
}

export function freezeCharter(charter, previous = null, options = {}) {
  const invalid = readableState(previous);
  if (invalid) return invalid;
  const validation = validateCharter(charter);
  if (!validation.ok) return fail("INVALID_CHARTER", validation.errors);

  const canonical = validation.charter;
  const nextHash = sha(JSON.stringify(canonical));
  const requestHash = sha(canonical.user_request);

  if (previous && previous.user_request_hash === requestHash && previous.charter_hash !== nextHash) {
    return fail("ORACLE_TAMPERED", [
      "Frozen checks changed while the user request did not. Restore the frozen charter and fix the application."
    ]);
  }
  if (previous && previous.charter_hash === nextHash) return { ok: true, code: "UNCHANGED", state: previous };
  if (previous && previous.user_request_hash !== requestHash && !options.allowNewRequest) {
    return fail("OPEN_FAILURE_BLOCKING", [
      "The frozen user request cannot be replaced. Finish those checks, or pass --allow-new-request only when the user stated a new request."
    ]);
  }

  return {
    ok: true,
    code: "FROZEN",
    state: {
      version: STATE_VERSION,
      status: "pending",
      user_request: canonical.user_request,
      user_request_hash: requestHash,
      charter_hash: nextHash,
      charter: canonical,
      frozen_at: new Date().toISOString(),
      attempts: [],
      open_failure: null
    }
  };
}

function safeEvidencePath(root, ref) {
  if (typeof ref !== "string" || !ref.trim() || isAbsolute(ref)) return null;
  if (ref.replaceAll("\\", "/").split("/").includes("..")) return null;
  const base = resolve(root);
  const target = resolve(base, ref);
  const rel = relative(base, target);
  if (!rel || rel.startsWith("..") || isAbsolute(rel)) return null;
  return target;
}

function evidenceText(outcome, options, charter) {
  const errors = [];
  if (!options.evidenceRoot) errors.push("An evidence root is required.");
  const refs = Array.isArray(outcome.evidence_refs) ? outcome.evidence_refs : [];
  if (refs.length === 0) errors.push("At least one evidence file is required.");
  const chunks = [];
  for (const ref of refs) {
    const target = options.evidenceRoot ? safeEvidencePath(options.evidenceRoot, ref) : null;
    if (!target) {
      errors.push("Evidence paths must stay inside the evidence root.");
      continue;
    }
    const blocked = [options.statePath, options.charterPath].filter(Boolean).map((file) => resolve(file));
    if (blocked.includes(target)) {
      errors.push("Evidence cannot be the charter or the state file.");
      continue;
    }
    if (!existsSync(target) || !statSync(target).isFile()) {
      errors.push(`Evidence file is missing: ${ref}`);
      continue;
    }
    if (statSync(target).size > MAX_EVIDENCE_BYTES) {
      errors.push(`Evidence file is too large: ${ref}`);
      continue;
    }
    chunks.push(readFileSync(target, "utf8"));
  }
  if (errors.length > 0) return { ok: false, errors };

  const text = chunks.join("\n");
  let stripped = text;
  for (const check of charter.checks) {
    stripped = stripped.split(check.id).join("\n");
    stripped = stripped.split(check.expect).join("\n");
  }
  for (const check of outcome.checks ?? []) {
    if (typeof check?.observed === "string") stripped = stripped.split(check.observed.trim()).join("\n");
  }
  if (stripped.replace(/\s+/g, "").length < MIN_CONTEXT_CHARS) {
    errors.push("Evidence must include the command or request and the raw application output, not only the expectation.");
  }
  return errors.length === 0 ? { ok: true, text } : { ok: false, errors };
}

export function recordOutcome(charter, outcome, previous, options = {}) {
  const invalid = readableState(previous);
  if (invalid) return invalid;
  if (!previous) return fail("NOT_FROZEN", ["Freeze the charter before recording an outcome."]);
  const validation = validateCharter(charter);
  if (!validation.ok) return fail("INVALID_CHARTER", validation.errors);

  const canonical = validation.charter;
  if (sha(JSON.stringify(canonical)) !== previous.charter_hash) {
    return fail("ORACLE_TAMPERED", [
      "The recorded charter does not match the frozen checks. Restore the frozen charter and fix the application."
    ]);
  }
  if (!outcome || (outcome.status !== "pass" && outcome.status !== "fail")) {
    return fail("INVALID_OUTCOME", ["Outcome status must be pass or fail."]);
  }
  if (!Array.isArray(outcome.checks)) return fail("INVALID_OUTCOME", ["Outcome checks are required."]);

  const errors = [];
  const expectedIds = canonical.checks.map((check) => check.id);
  const gotIds = outcome.checks.map((check) => check?.id);
  if (gotIds.length !== expectedIds.length || expectedIds.some((id) => gotIds.filter((got) => got === id).length !== 1)) {
    errors.push("Outcome checks must list each frozen check id once.");
  }
  for (const check of outcome.checks) {
    if (check?.result !== "pass" && check?.result !== "fail") errors.push(`Check '${check?.id}' result must be pass or fail.`);
    if (asText(check?.observed).length < 1) errors.push(`Check '${check?.id}' needs an observed quote from the evidence.`);
  }
  const results = outcome.checks.map((check) => check?.result);
  if (outcome.status === "pass" && results.some((result) => result !== "pass")) errors.push("A pass outcome cannot include a failed check.");
  if (outcome.status === "fail" && results.every((result) => result === "pass")) errors.push("A fail outcome needs at least one failed check.");

  const evidence = evidenceText(outcome, options, canonical);
  if (!evidence.ok) errors.push(...evidence.errors);
  if (evidence.ok) {
    for (const check of outcome.checks) {
      if (!evidence.text.includes(check.id)) errors.push(`Evidence does not mention check '${check.id}'.`);
      const observed = asText(check.observed);
      if (observed && !evidence.text.includes(observed)) errors.push(`Observed text for '${check.id}' is not in the evidence.`);
    }
  }
  if (errors.length > 0) return fail("INVALID_OUTCOME", errors);

  const attempt = {
    at: new Date().toISOString(),
    status: outcome.status,
    evidence_refs: outcome.evidence_refs,
    checks: outcome.checks.map((check) => ({ id: check.id, result: check.result, observed: asText(check.observed) }))
  };
  const attempts = [...(previous.attempts ?? []), attempt];
  if (outcome.status === "pass") {
    return {
      ok: true,
      code: "PASSED",
      state: { ...previous, status: "passed", attempts, open_failure: null, passed_at: attempt.at }
    };
  }

  const failed = attempt.checks.filter((check) => check.result === "fail");
  return {
    ok: true,
    code: "FAILED",
    state: {
      ...previous,
      status: "open",
      attempts,
      open_failure: {
        failed_checks: failed,
        evidence_refs: outcome.evidence_refs,
        next_window: "Read this failure before editing. The user request stays frozen. Fix the application. Do not edit check expectations. Re-run the same checks and record the outcome."
      }
    }
  };
}

export function renderResume(state) {
  if (state?.status !== "open" || !state.open_failure) return "";
  const failed = state.open_failure.failed_checks
    .map((check) => `- \`${check.id}\`\n\n~~~text\n${check.observed}\n~~~`)
    .join("\n");
  const evidence = (state.open_failure.evidence_refs ?? []).map((ref) => `- \`${ref}\``).join("\n");
  return [
    "# tests-expert open failure",
    "",
    "Status: open",
    `Charter hash: \`${state.charter_hash}\``,
    "",
    "## Oracle",
    "",
    "~~~text",
    state.user_request,
    "~~~",
    "",
    "## Failed checks",
    "",
    failed,
    "",
    "## Evidence",
    "",
    evidence,
    "",
    "## Next window",
    "",
    "Fix the application. These checks stay frozen. Do not edit expectations and do not add a check that describes the broken behavior. Re-run the same surfaces and record the outcome with `node skills/tests-expert/scripts/charter.mjs record`.",
    "",
    "Read `skills/tests-expert/SKILL.md` before editing. Point `.notebook/HANDOFF.md` at this file. Do not copy this failure into `.notebook/MEMORY.md`.",
    ""
  ].join("\n");
}

function readJson(file) {
  return JSON.parse(readFileSync(file, "utf8"));
}

function writeState(statePath, state) {
  mkdirSync(dirname(statePath), { recursive: true });
  writeFileSync(statePath, `${JSON.stringify(state, null, 2)}\n`);
  const resumePath = resolve(dirname(statePath), "RESUME.md");
  if (state.status === "open") writeFileSync(resumePath, renderResume(state));
  else if (existsSync(resumePath)) rmSync(resumePath);
  return resumePath;
}

function parseArgs(argv) {
  const out = { allowNewRequest: false };
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (token === "--allow-new-request") {
      out.allowNewRequest = true;
      continue;
    }
    if (!token.startsWith("--")) throw new Error(`unexpected argument ${token}`);
    const value = argv[index + 1];
    if (!value || value.startsWith("--")) throw new Error(`missing value for ${token}`);
    out[token.slice(2)] = value;
    index += 1;
  }
  return out;
}

function emit(result, resumePath) {
  const payload = {
    ok: result.ok,
    code: result.code,
    status: result.state?.status ?? null,
    charter_hash: result.state?.charter_hash ?? null,
    errors: result.errors ?? [],
    resume_path: result.state?.status === "open" ? resumePath : null,
    failed_checks: result.state?.open_failure?.failed_checks?.map((check) => check.id) ?? []
  };
  const stream = result.ok ? process.stdout : process.stderr;
  stream.write(`${JSON.stringify(payload)}\n`);
  if (!result.ok) return result.code === "ORACLE_TAMPERED" || result.code === "OPEN_FAILURE_BLOCKING" ? 2 : 1;
  return result.code === "FAILED" ? 3 : 0;
}

function main() {
  const [command, ...rest] = process.argv.slice(2);
  if (!command || command === "--help") {
    process.stderr.write("Usage: node charter.mjs <freeze|record|resume> --state <file> [--charter <file>] [--outcome <file>] [--evidence-root <dir>] [--allow-new-request]\n");
    return 1;
  }
  const args = parseArgs(rest);
  if (!args.state) throw new Error("missing --state");
  const statePath = resolve(args.state);
  const previous = existsSync(statePath) ? readJson(statePath) : null;

  if (command === "resume") {
    if (!previous) return emit(fail("NO_STATE", ["No charter state exists yet."]));
    if (previous.status !== "open") return emit(fail("NO_OPEN_FAILURE", [`Charter status is ${previous.status}.`]));
    process.stdout.write(renderResume(previous));
    return 0;
  }

  if (!args.charter) throw new Error("missing --charter");
  const charterPath = resolve(args.charter);
  const charter = readJson(charterPath);

  if (command === "freeze") {
    const result = freezeCharter(charter, previous, { allowNewRequest: args.allowNewRequest });
    if (result.ok) writeState(statePath, result.state);
    return emit(result, resolve(dirname(statePath), "RESUME.md"));
  }

  if (command === "record") {
    if (!args.outcome) throw new Error("missing --outcome");
    const result = recordOutcome(charter, readJson(resolve(args.outcome)), previous, {
      evidenceRoot: resolve(args["evidence-root"] || process.cwd()),
      statePath,
      charterPath
    });
    if (result.ok) writeState(statePath, result.state);
    return emit(result, resolve(dirname(statePath), "RESUME.md"));
  }

  throw new Error(`unknown command ${command}`);
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  try {
    process.exit(main());
  } catch (error) {
    process.stderr.write(`${JSON.stringify({ ok: false, code: "INVALID_INPUT", errors: [error instanceof Error ? error.message : String(error)] })}\n`);
    process.exit(1);
  }
}
