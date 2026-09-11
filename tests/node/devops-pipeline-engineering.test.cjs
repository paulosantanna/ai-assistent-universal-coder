const assert = require("node:assert/strict");
const path = require("node:path");
const { pathToFileURL } = require("node:url");

const repoRoot = path.resolve(__dirname, "../..");
function moduleUrl(relativePath) {
  return pathToFileURL(path.join(repoRoot, relativePath)).href;
}

describe("AEOS DevOps pipeline engineering governance", () => {
  let governance;

  before(async () => {
    governance = await import(moduleUrl("scripts/aeos-devops-pipeline-governance.mjs"));
  });

  it("does not confuse API health with pipeline success", () => {
    const result = governance.evaluatePipelineState({
      latestSha: "abc123",
      apiHealthy: true,
      runs: [{ id: 1, head_sha: "abc123", status: "completed", conclusion: "failure", required: true }]
    });
    assert.equal(result.status, "BLOCKED");
    assert.equal(result.reason, "REQUIRED_CHECK_FAILED");
  });

  it("requires every required latest-SHA check to be completed successfully", () => {
    const pending = governance.evaluatePipelineState({
      latestSha: "newsha",
      runs: [{ id: 1, head_sha: "newsha", status: "completed", conclusion: "success", required: true }],
      jobs: [{ id: 2, head_sha: "newsha", status: "in_progress", conclusion: null, required: true }]
    });
    assert.equal(pending.status, "REVIEW");
    assert.equal(pending.reason, "REQUIRED_CHECK_PENDING");

    const pass = governance.evaluatePipelineState({
      latestSha: "newsha",
      runs: [{ id: 1, head_sha: "newsha", status: "completed", conclusion: "success", required: true }],
      jobs: [{ id: 2, head_sha: "newsha", status: "completed", conclusion: "success", required: true }],
      checks: [{ id: 3, head_sha: "newsha", status: "completed", conclusion: "success", required: true }]
    });
    assert.equal(pass.status, "PASS");
    assert.equal(pass.summary.required, 3);
    assert.equal(pass.summary.passed, 3);
  });

  it("rejects stale-SHA evidence", () => {
    const result = governance.evaluatePipelineState({
      latestSha: "newsha",
      runs: [{ id: 1, head_sha: "oldsha", status: "completed", conclusion: "success", required: true }]
    });
    assert.equal(result.status, "BLOCKED");
    assert.equal(result.reason, "ONLY_STALE_SHA_EVIDENCE");
  });

  it("creates guardian coverage without creating agent identities", () => {
    const map = governance.buildGuardianMap({
      latestSha: "sha",
      runs: [
        { id: 11, name: "tests", head_sha: "sha", status: "in_progress", required: true },
        { id: 12, name: "security", head_sha: "sha", status: "queued", required: true }
      ],
      jobs: [
        { id: 21, run_id: 11, name: "py311", head_sha: "sha", matrix: { python: "3.11" } },
        { id: 22, run_id: 11, name: "py312", head_sha: "sha", matrix: { python: "3.12" } }
      ]
    });
    assert.equal(map.ownerAgent, "codenavi-agent");
    assert.equal(map.workflows.length, 2);
    assert.equal(map.jobs.length, 2);
    assert.equal(map.workflows.every((item) => item.guardianType === "WorkflowGuardianLens"), true);
    assert.equal(map.jobs.every((item) => item.guardianType === "JobGuardianWorkUnit"), true);
  });

  it("groups duplicate failures by normalized root-cause fingerprint", () => {
    const groups = governance.groupRootCauses([
      { workflowRunId: 1, jobId: 10, category: "unit_test", step: "pytest", file: "x.py", message: "AssertionError at abcdef1234567" },
      { workflowRunId: 1, jobId: 11, category: "unit_test", step: "pytest", file: "x.py", message: "AssertionError at 1234567abcdef" }
    ]);
    assert.equal(groups.length, 1);
    assert.equal(groups[0].affectedCount, 2);
  });

  it("stops repeated recovery without progress", () => {
    const result = governance.evaluateRecoveryLimits({
      cycle: 2,
      rootCauseCycles: 2,
      totalCommits: 2,
      sameFingerprintRepetitions: 2,
      progress: "NONE",
      tokenUsed: 1000
    });
    assert.equal(result.decision, "BLOCKED");
    assert.equal(result.reason, "REPEATED_FAILURE_WITHOUT_PROGRESS");
  });

  it("permanently denies repository deletion", () => {
    const decision = governance.authorizeOperation("repository.delete");
    assert.equal(decision.decision, "DENY_PERMANENT");
    assert.equal(decision.reasonCode, "REPOSITORY_DELETION_MANUAL_ONLY");
    assert.equal(decision.overridable, false);
    assert.equal(decision.approvalAllowed, false);
  });

  it("redacts PAT-like tokens and explicit secrets", () => {
    const explicit = "super-secret-value";
    const value = governance.redactSecrets(
      `Authorization: Bearer ${explicit} github_pat_1234567890ABCDEFGHIJK`,
      [explicit]
    );
    assert.equal(value.includes(explicit), false);
    assert.equal(value.includes("github_pat_"), false);
    assert.match(value, /\[REDACTED\]/);
  });

  it("requires approval and current SHA before merge", () => {
    const pipeline = governance.evaluatePipelineState({
      latestSha: "sha",
      runs: [{ id: 1, head_sha: "sha", status: "completed", conclusion: "success" }]
    });
    const stale = governance.mergeReadiness({
      expectedHeadSha: "old",
      actualHeadSha: "sha",
      pipeline,
      judge: "PASS",
      evidenceVerify: "PASS",
      secretScan: "PASS",
      protectionSatisfied: true,
      approval: "GRANTED"
    });
    assert.equal(stale.decision, "MERGE_DENIED");

    const ready = governance.mergeReadiness({
      expectedHeadSha: "sha",
      actualHeadSha: "sha",
      pipeline,
      judge: "PASS",
      evidenceVerify: "PASS",
      secretScan: "PASS",
      protectionSatisfied: true,
      approval: "REQUIRED"
    });
    assert.equal(ready.decision, "READY_FOR_APPROVAL");
  });
});
