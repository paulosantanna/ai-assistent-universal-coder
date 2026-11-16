import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join, resolve, dirname } from "node:path";
import { test } from "node:test";
import { fileURLToPath } from "node:url";
import {
  RULES,
  createKb,
  estimateMonthlyCost,
  getPattern,
  listPatterns,
  listPitfalls,
  reviewArchitecture,
  validateKnowledge,
} from "../shared/engine.mjs";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const MODELS = resolve(ROOT, "..", "cloud-architecture", "models");
const kb = createKb(ROOT);
const loadModel = (relative) => JSON.parse(readFileSync(join(MODELS, relative), "utf8"));

// Regression harness: each rule must fire on a minimal trap model. A trap is a learned error that must not return.
const TRAPS = {
  "AWS-001": { provider: "aws", compute: [{ name: "api", service: "app-runner" }] },
  "AWS-002": { provider: "aws", audience_regions: ["BR"], cdn: { service: "cloudfront", price_class: "PriceClass_200" } },
  "AWS-003": { provider: "aws", network: { interface_endpoints: 9, availability_zones: 2 } },
  "AWS-004": { provider: "aws", environment: "prod", data: [{ service: "opensearch-managed", dedicated_masters: 2 }] },
  "AWS-005": { provider: "aws", ml: [{ service: "sagemaker-realtime", always_on: true, traffic: "intermittent" }] },
  "AWS-006": { provider: "aws", identity: { ci_auth: "static-keys" } },
  "AWS-007": { provider: "aws", observability: { traces_destination: "xray", traces_auth: "bearer" } },
  "AWS-008": { provider: "aws", llm: { external_endpoint: true }, constraints: { external_llm_allowed: false } },
  "AWS-009": { provider: "aws", data: [{ public_access: true }] },
  "AWS-010": { provider: "aws", data_classification: "personal", data: [{ encryption: "sse-s3" }] },
  "AWS-011": { provider: "aws", environment: "prod", data: [{ service: "aurora-postgresql", multi_az: false, deletion_protection: true }] },
  "AWS-012": { provider: "aws", data: [{ service: "s3-vectors", latency_ms_target: 50 }] },
  "AWS-013": { provider: "aws", ml: [{ training_spot: true, checkpoints: false }] },
  "AWS-014": { provider: "aws", observability: { telemetry: "none" } },
  "AWS-015": { provider: "aws", compute: [{ service: "ecs-express", arch: "x86_64" }] },
  "AWS-016": { provider: "aws", project: { kind: "desktop-app" }, observability: { telemetry: "http" } },
  "AWS-017": { provider: "aws", data: [{ kind: "audit-archive", immutability: "governance" }] },
  "AZ-001": { provider: "azure", regions: { primary: "brazilsouth" }, data: [{ service: "postgres-flexible", ha: "zone-redundant" }] },
  "AZ-002": { provider: "azure", regions: { primary: "brazilsouth" }, data: [{ backup_geo_redundant: true }] },
  "AZ-003": { provider: "azure", signing: { windows_authenticode: "artifact-signing", publisher_country: "BR" } },
  "AZ-004": { provider: "azure", compute: [{ service: "container-apps", scale_to_zero: true, scale_metric: "cpu" }] },
  "AZ-005": { provider: "azure", ml: [{ service: "azure-ml-online", scale_to_zero: true }] },
  "AZ-006": { provider: "azure", data: [{ kind: "audit-archive", immutability: "unlocked" }] },
  "AZ-007": { provider: "azure", observability: { log_analytics_gb_month: 20 } },
  "AZ-008": { provider: "azure", data: [{ public_access: true }] },
  "AZ-009": { provider: "azure", llm: { external_endpoint: true }, constraints: { external_llm_allowed: false } },
  "AZ-011": { provider: "azure", data: [{ kind: "audit-archive", immutability: "locked", immutability_level: "version", versioning: false }] },
};

test("knowledge base: references resolve and labels agree with the evidence", () => {
  assert.deepEqual(validateKnowledge(kb), []);
});

test("evidence: every claim has an https source URL and a final label", () => {
  assert.ok(kb.claims.size >= 60, `claims: ${kb.claims.size}`);
  for (const claim of kb.claims.values()) {
    assert.match(claim.source_url, /^https:\/\//, claim.id);
    assert.ok(claim.final_label, claim.id);
  }
});

test("coverage: each provider has at least 8 patterns and 12 pitfalls, each pitfall with evidence", () => {
  for (const provider of ["aws", "azure"]) {
    assert.ok(listPatterns(kb, provider).length >= 8, `${provider} patterns`);
    const pitfalls = listPitfalls(kb, provider);
    assert.ok(pitfalls.length >= 12, `${provider} pitfalls`);
    for (const pitfall of pitfalls) {
      const hasEvidence = pitfall.claims.length + pitfall.rejected_claims.length > 0 || pitfall.evidence_note || pitfall.project_sources.length;
      assert.ok(hasEvidence, pitfall.id);
    }
  }
});

test("patterns resolve with their claims and reject unknown ids", () => {
  const pattern = getPattern(kb, "aws", "aws.db.aurora-postgresql");
  assert.ok(pattern.claims.length >= 3);
  assert.throws(() => getPattern(kb, "aws", "aws.unknown"), /Unknown pattern id/);
});

test("rules: unique ids, known providers, and one regression trap per rule", () => {
  const ids = RULES.map((rule) => rule.id);
  assert.equal(new Set(ids).size, ids.length, "duplicated rule id");
  for (const rule of RULES) assert.ok(["aws", "azure"].includes(rule.provider), rule.id);
  assert.deepEqual([...ids].sort(), Object.keys(TRAPS).sort());
});

for (const [ruleId, trap] of Object.entries(TRAPS)) {
  test(`regression trap: ${ruleId} fires on its learned error`, () => {
    const result = reviewArchitecture(kb, trap);
    const finding = result.findings.find((f) => f.rule_id === ruleId);
    assert.ok(finding, `${ruleId} did not fire; findings=${result.findings.map((f) => f.rule_id)}`);
    assert.equal(result.status, finding.severity === "error" ? "fail" : "pass_with_findings");
  });
}

test("good models: MyDigitalBuddy and the AIHealthResearch target pass without errors", () => {
  for (const relative of ["aws/mydigitalbuddy.model.json", "aws/aihealthresearch.target.model.json", "azure/aihealthresearch.target.model.json"]) {
    const result = reviewArchitecture(kb, loadModel(relative));
    assert.equal(result.errors, 0, relative);
    assert.notEqual(result.status, "fail", relative);
  }
  // The nine interface endpoints stay, so the fixed hourly cost per AZ is recorded as the only warning (AWS-003).
  assert.deepEqual(reviewArchitecture(kb, loadModel("aws/aihealthresearch.target.model.json")).findings.map((f) => f.rule_id), ["AWS-003"]);
});

test("as-is AIHealthResearch model: four findings, no error, each pointing to a fact or a source", () => {
  const result = reviewArchitecture(kb, loadModel("aws/aihealthresearch.as-is.model.json"));
  assert.equal(result.status, "pass_with_findings");
  assert.equal(result.errors, 0);
  const ids = result.findings.map((f) => f.rule_id).sort();
  assert.deepEqual(ids, ["AWS-003", "AWS-005", "AWS-015", "AWS-017"]);
  for (const finding of result.findings) {
    assert.ok(finding.claims.length > 0 || finding.sources.length > 0, finding.rule_id);
  }
});

test("cost: unknown SKU fails closed; units and factor are applied; total equals the sum of lines", () => {
  const prices = kb.prices.aws;
  assert.throws(() => estimateMonthlyCost(prices, [{ sku: "aws.sa-east-1.invented_sku", units_per_month: 1 }]), /Unknown SKU/);
  assert.throws(() => estimateMonthlyCost(prices, [{ sku: "aws.sa-east-1.alb_hour", units_per_month: -1 }]), /Invalid units/);
  const result = estimateMonthlyCost(prices, [
    { sku: "aws.sa-east-1.sagemaker_training_ml_g5_xlarge_hour", units_per_month: 10, factor: 0.5 },
    { sku: "aws.sa-east-1.alb_hour", units_per_month: 2 },
  ]);
  const expectedTraining = Math.round(10 * prices.skus["aws.sa-east-1.sagemaker_training_ml_g5_xlarge_hour"].usd * 0.5 * 100) / 100;
  assert.equal(result.lines[0].monthly_usd, expectedTraining);
  const sum = Math.round(result.lines.reduce((total, line) => total + line.monthly_usd, 0) * 100) / 100;
  assert.equal(result.total_usd, sum);
});

test("review rejects a model that declares another provider", () => {
  assert.throws(() => reviewArchitecture(kb, { provider: "gcp" }), /Unknown provider/);
});
