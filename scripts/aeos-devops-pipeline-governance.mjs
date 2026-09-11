#!/usr/bin/env node
import { createHash } from "node:crypto";

const TERMINAL_SUCCESS = new Set(["success"]);
const TERMINAL_FAILURE = new Set(["failure", "cancelled", "timed_out", "action_required", "startup_failure"]);
const NON_REQUIRED_ACCEPTABLE = new Set(["success", "neutral", "skipped"]);

export const PERMANENTLY_DENIED_OPERATIONS = new Set([
  "repository.delete",
  "github.repository.delete",
  "secret.read_value",
  "secret.export",
  "pat.scope_escalation",
  "branch_protection.bypass",
  "audit_trail.delete",
  "evidence.finalized.rewrite"
]);

function stable(value) {
  return JSON.stringify(value, Object.keys(value).sort());
}

function sha256(value) {
  return createHash("sha256").update(String(value)).digest("hex");
}

export function redactSecrets(value, secrets = []) {
  let text = String(value ?? "");
  const candidates = secrets.filter((item) => typeof item === "string" && item.length >= 4);
  for (const secret of candidates) text = text.split(secret).join("[REDACTED]");
  text = text.replace(/(authorization\s*:\s*(?:bearer|token)\s+)[^\s]+/gi, "$1[REDACTED]");
  text = text.replace(/\b(gh[pousr]_[A-Za-z0-9_]{10,}|github_pat_[A-Za-z0-9_]{10,})\b/g, "[REDACTED]");
  return text;
}

export function authorizeOperation(operation) {
  if (PERMANENTLY_DENIED_OPERATIONS.has(operation)) {
    return {
      decision: "DENY_PERMANENT",
      operation,
      reasonCode: operation.includes("repository.delete")
        ? "REPOSITORY_DELETION_MANUAL_ONLY"
        : "PERMANENTLY_DENIED_OPERATION",
      overridable: false,
      approvalAllowed: false,
      delegationAllowed: false
    };
  }
  return { decision: "REQUIRES_POLICY", operation, overridable: true };
}

function normalizeRequired(item) {
  return item.required !== false;
}

function normalizeConclusion(item) {
  return String(item.conclusion ?? "").toLowerCase();
}

function normalizeStatus(item) {
  return String(item.status ?? "").toLowerCase();
}

function evaluateItem(item, latestSha) {
  const required = normalizeRequired(item);
  const sha = item.head_sha ?? item.headSha ?? item.sha ?? latestSha;
  const status = normalizeStatus(item);
  const conclusion = normalizeConclusion(item);
  const stale = Boolean(latestSha && sha && sha !== latestSha);
  const completed = status === "completed" || Boolean(conclusion);

  let acceptable = false;
  if (!stale && completed) {
    acceptable = required ? TERMINAL_SUCCESS.has(conclusion) : NON_REQUIRED_ACCEPTABLE.has(conclusion);
  }

  return {
    id: item.id ?? item.name ?? null,
    name: item.name ?? String(item.id ?? "unknown"),
    required,
    sha,
    status,
    conclusion,
    stale,
    completed,
    acceptable,
    failed: required && !stale && completed && TERMINAL_FAILURE.has(conclusion),
    pending: required && !stale && !completed
  };
}

export function evaluatePipelineState({ latestSha, apiHealthy = true, runs = [], jobs = [], checks = [] }) {
  if (!latestSha) {
    return {
      status: "BLOCKED",
      reason: "LATEST_SHA_REQUIRED",
      apiHealthy: Boolean(apiHealthy),
      latestSha: null,
      runs: [], jobs: [], checks: []
    };
  }

  const evaluatedRuns = runs.map((item) => evaluateItem(item, latestSha));
  const evaluatedJobs = jobs.map((item) => evaluateItem(item, latestSha));
  const evaluatedChecks = checks.map((item) => evaluateItem(item, latestSha));
  const required = [...evaluatedRuns, ...evaluatedJobs, ...evaluatedChecks].filter((item) => item.required && !item.stale);
  const staleRequired = [...evaluatedRuns, ...evaluatedJobs, ...evaluatedChecks].filter((item) => item.required && item.stale);
  const pending = required.filter((item) => item.pending);
  const failed = required.filter((item) => item.failed || (item.completed && !item.acceptable));
  const passed = required.filter((item) => item.acceptable);

  let status = "PASS";
  let reason = "ALL_REQUIRED_CHECKS_SUCCESS";
  if (!apiHealthy) {
    status = "BLOCKED";
    reason = "GITHUB_API_UNHEALTHY";
  } else if (required.length === 0) {
    status = "BLOCKED";
    reason = staleRequired.length > 0 ? "ONLY_STALE_SHA_EVIDENCE" : "NO_REQUIRED_CHECK_EVIDENCE";
  } else if (failed.length > 0) {
    status = "BLOCKED";
    reason = "REQUIRED_CHECK_FAILED";
  } else if (pending.length > 0) {
    status = "REVIEW";
    reason = "REQUIRED_CHECK_PENDING";
  } else if (passed.length !== required.length) {
    status = "BLOCKED";
    reason = "REQUIRED_CHECK_NOT_SUCCESSFUL";
  }

  return {
    status,
    reason,
    apiHealthy: Boolean(apiHealthy),
    latestSha,
    summary: {
      required: required.length,
      passed: passed.length,
      failed: failed.length,
      pending: pending.length,
      staleRequired: staleRequired.length
    },
    runs: evaluatedRuns,
    jobs: evaluatedJobs,
    checks: evaluatedChecks
  };
}

export function buildGuardianMap({ latestSha, runs = [], jobs = [] }) {
  const workflows = runs
    .filter((run) => (run.head_sha ?? run.headSha ?? run.sha ?? latestSha) === latestSha)
    .map((run) => ({
      guardianType: "WorkflowGuardianLens",
      guardianId: `workflow:${run.id}`,
      workflowRunId: run.id,
      workflowName: run.name ?? `workflow-${run.id}`,
      headSha: latestSha,
      status: run.status ?? null,
      conclusion: run.conclusion ?? null,
      required: normalizeRequired(run)
    }));

  const jobUnits = jobs
    .filter((job) => (job.head_sha ?? job.headSha ?? job.sha ?? latestSha) === latestSha)
    .map((job) => ({
      guardianType: "JobGuardianWorkUnit",
      guardianId: `job:${job.id}`,
      workflowRunId: job.run_id ?? job.runId ?? null,
      jobId: job.id,
      jobName: job.name ?? `job-${job.id}`,
      matrix: job.matrix ?? null,
      headSha: latestSha,
      status: job.status ?? null,
      conclusion: job.conclusion ?? null,
      required: normalizeRequired(job)
    }));

  return { ownerAgent: "codenavi-agent", workflows, jobs: jobUnits };
}

export function normalizeFailure(failure = {}) {
  const message = redactSecrets(failure.message ?? failure.log ?? "", failure.secrets ?? [])
    .replace(/\b[0-9a-f]{7,40}\b/gi, "<sha>")
    .replace(/\b\d+(?:\.\d+){1,3}\b/g, "<version>")
    .replace(/\b\d+ms\b/gi, "<duration>")
    .replace(/\s+/g, " ")
    .trim();
  const basis = [failure.category ?? "unknown", failure.step ?? "unknown", failure.file ?? "", message].join("|").toLowerCase();
  return {
    ...failure,
    normalizedMessage: message,
    fingerprint: sha256(basis).slice(0, 24)
  };
}

export function groupRootCauses(failures = []) {
  const groups = new Map();
  for (const raw of failures) {
    const failure = raw.fingerprint ? raw : normalizeFailure(raw);
    const current = groups.get(failure.fingerprint) ?? {
      fingerprint: failure.fingerprint,
      category: failure.category ?? "unknown",
      failures: [],
      jobIds: new Set(),
      workflowRunIds: new Set()
    };
    current.failures.push(failure);
    if (failure.jobId != null) current.jobIds.add(failure.jobId);
    if (failure.workflowRunId != null) current.workflowRunIds.add(failure.workflowRunId);
    groups.set(failure.fingerprint, current);
  }
  return [...groups.values()].map((group) => ({
    fingerprint: group.fingerprint,
    category: group.category,
    failures: group.failures,
    jobIds: [...group.jobIds],
    workflowRunIds: [...group.workflowRunIds],
    affectedCount: group.failures.length
  }));
}

export function assessRecoveryProgress(previous = {}, current = {}) {
  const prevFailures = new Set(previous.activeFingerprints ?? []);
  const currFailures = new Set(current.activeFingerprints ?? []);
  const resolved = [...prevFailures].filter((item) => !currFailures.has(item));
  const introduced = [...currFailures].filter((item) => !prevFailures.has(item));
  const previousFailedJobs = Number(previous.failedJobs ?? 0);
  const currentFailedJobs = Number(current.failedJobs ?? 0);
  const previousPassedChecks = Number(previous.passedChecks ?? 0);
  const currentPassedChecks = Number(current.passedChecks ?? 0);

  const positive = resolved.length > 0 || currentFailedJobs < previousFailedJobs || currentPassedChecks > previousPassedChecks;
  const sameFingerprintSet = stable([...prevFailures].sort()) === stable([...currFailures].sort());
  const noProgress = !positive && sameFingerprintSet && currentFailedJobs >= previousFailedJobs;

  return {
    status: positive ? "POSITIVE" : noProgress ? "NONE" : "CHANGED",
    resolvedFingerprints: resolved,
    introducedFingerprints: introduced,
    failedJobsDelta: currentFailedJobs - previousFailedJobs,
    passedChecksDelta: currentPassedChecks - previousPassedChecks
  };
}

export function evaluateRecoveryLimits({ cycle = 0, rootCauseCycles = 0, totalCommits = 0, sameFingerprintRepetitions = 0, elapsedMinutes = 0, tokenUsed = 0, tokenBudget = 240000, progress = "POSITIVE", oscillating = false }, limits = {}) {
  const cfg = {
    maxCycles: limits.maxCycles ?? 10,
    maxCyclesPerRootCause: limits.maxCyclesPerRootCause ?? 3,
    maxTotalCommits: limits.maxTotalCommits ?? 20,
    maxSameFingerprintRepetitions: limits.maxSameFingerprintRepetitions ?? 2,
    monitorTimeoutMinutes: limits.monitorTimeoutMinutes ?? 180
  };
  if (cycle >= cfg.maxCycles) return { decision: "BLOCKED", reason: "RECOVERY_CYCLE_LIMIT_REACHED" };
  if (rootCauseCycles >= cfg.maxCyclesPerRootCause) return { decision: "BLOCKED", reason: "ROOT_CAUSE_RETRY_LIMIT_REACHED" };
  if (totalCommits >= cfg.maxTotalCommits) return { decision: "BLOCKED", reason: "RECOVERY_COMMIT_LIMIT_REACHED" };
  if (sameFingerprintRepetitions >= cfg.maxSameFingerprintRepetitions && progress === "NONE") return { decision: "BLOCKED", reason: "REPEATED_FAILURE_WITHOUT_PROGRESS" };
  if (oscillating) return { decision: "BLOCKED", reason: "RECOVERY_OSCILLATION_DETECTED" };
  if (elapsedMinutes >= cfg.monitorTimeoutMinutes) return { decision: "TIMEOUT", reason: "MONITOR_TIMEOUT" };
  if (tokenUsed >= tokenBudget) return { decision: "BLOCKED", reason: "TOKEN_BUDGET_EXCEEDED" };
  return { decision: "CONTINUE", reason: "WITHIN_LIMITS" };
}

export function mergeReadiness({ expectedHeadSha, actualHeadSha, pipeline, judge = "BLOCKED", evidenceVerify = "BLOCKED", secretScan = "BLOCKED", approval = "REQUIRED", protectionSatisfied = false }) {
  if (!expectedHeadSha || expectedHeadSha !== actualHeadSha) return { decision: "MERGE_DENIED", reason: "HEAD_SHA_CHANGED" };
  if (pipeline?.status !== "PASS") return { decision: "MERGE_DENIED", reason: "PIPELINE_NOT_GREEN" };
  if (judge !== "PASS") return { decision: "MERGE_DENIED", reason: "JUDGE_NOT_PASS" };
  if (evidenceVerify !== "PASS") return { decision: "MERGE_DENIED", reason: "EVIDENCE_NOT_PASS" };
  if (secretScan !== "PASS") return { decision: "MERGE_DENIED", reason: "SECRET_SCAN_NOT_PASS" };
  if (!protectionSatisfied) return { decision: "MERGE_DENIED", reason: "BRANCH_PROTECTION_NOT_SATISFIED" };
  if (approval !== "GRANTED") return { decision: "READY_FOR_APPROVAL", reason: "EXPLICIT_APPROVAL_REQUIRED" };
  return { decision: "MERGE_ALLOWED", reason: "ALL_GATES_PASS" };
}

if (process.argv[1]?.endsWith("aeos-devops-pipeline-governance.mjs")) {
  console.log(JSON.stringify({
    status: "PASS",
    module: "aeos-devops-pipeline-governance",
    ownerAgent: "codenavi-agent",
    repositoryDeletion: authorizeOperation("repository.delete")
  }, null, 2));
}
