// Mapping tests for the local APIs and the architecture models. They run the same deterministic engine that the
// MCP servers expose, so a regression here means the MCP would give a wrong answer to a user.
import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { test } from "node:test";
import { fileURLToPath } from "node:url";
import { createKb, estimateMonthlyCost, mapLocalApi, reviewArchitecture, validateKnowledge } from "../../cloud-architecture-mcp/shared/engine.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const MCP_ROOT = resolve(HERE, "..", "..", "cloud-architecture-mcp");
const MODELS = resolve(HERE, "..", "models");
const kb = createKb(MCP_ROOT);
const apis = JSON.parse(readFileSync(resolve(HERE, "..", "local-apis.json"), "utf8")).apis;
const byId = (id) => apis.find((api) => api.id === id);
const load = (relative) => JSON.parse(readFileSync(join(MODELS, relative), "utf8"));
const flatten = (value) => JSON.stringify(value).toLowerCase();

test("knowledge base is consistent before any mapping", () => {
  assert.deepEqual(validateKnowledge(kb), []);
});

test("every local API maps on both clouds, and no external LLM service is ever a target", () => {
  for (const api of apis) {
    for (const provider of ["aws", "azure"]) {
      const mapping = mapLocalApi(api, provider);
      assert.equal(mapping.provider, provider);
      assert.ok(Object.keys(mapping.target).length > 0, `${api.id} ${provider} has no target`);
      if (api.external_llm_allowed !== true) {
        const targets = flatten(mapping.target);
        assert.doesNotMatch(targets, /bedrock|openai|foundry|amazon q/, `${api.id} ${provider}`);
      }
    }
  }
});

test("AIHealthResearch API: ECS Express on private subnets with an internal ALB, Aurora, OpenSearch and Object Lock archive", () => {
  const aws = mapLocalApi(byId("aihealthresearch-api"), "aws");
  assert.equal(aws.target.compute, "ecs-express");
  assert.match(aws.target.load_balancer, /internal-alb/);
  assert.match(aws.target.data, /aurora-postgresql/);
  assert.match(aws.target.search, /opensearch-managed/, "latency 50 ms must not go to S3 Vectors");
  assert.match(aws.target.archive, /object lock/i);
  assert.ok(aws.forbidden.includes("Amazon Bedrock"));
  assert.ok(aws.claims.includes("aws-ecs-express-no-charge"));
});

test("AIHealthResearch API on Azure: internal Container Apps, same-zone HA in Brazil South, AI Search hybrid, WORM archive", () => {
  const azure = mapLocalApi(byId("aihealthresearch-api"), "azure");
  assert.equal(azure.target.compute, "container-apps (consumo ou dedicado)");
  assert.match(azure.target.ingress, /internal/);
  assert.match(azure.target.ha, /mesma zona/);
  assert.match(azure.target.search, /ai-search-hybrid/);
  assert.match(azure.target.archive, /blob-immutable/);
  assert.ok(azure.constraints.some((c) => c.id === "region-brazilsouth" && c.status === "risk"));
  assert.ok(azure.forbidden.includes("Azure OpenAI"));
});

test("model server: 15 s p95 forbids scale-to-zero, so it is scheduled capacity on AWS and an online endpoint on Azure", () => {
  const aws = mapLocalApi(byId("aihealthresearch-model-server"), "aws");
  assert.match(aws.target.ml, /sagemaker-realtime com agenda/);
  assert.ok(aws.constraints.some((c) => c.id === "latency-vs-scale-to-zero"));
  const azure = mapLocalApi(byId("aihealthresearch-model-server"), "azure");
  assert.match(azure.target.ml, /azure-ml-online-endpoint/);
});

test("workers: EventBridge Scheduler and Lambda on AWS; Container Apps Jobs on Azure", () => {
  assert.equal(mapLocalApi(byId("aihealthresearch-workers"), "aws").target.scheduler, "eventbridge-scheduler");
  assert.equal(mapLocalApi(byId("aihealthresearch-workers"), "azure").target.scheduler, "container-apps-jobs (agendado)");
});

test("OTLP sink: CloudWatch agent on AWS (port must change from 14318 to 4318 default) and the Azure Monitor distro on Azure", () => {
  const aws = mapLocalApi(byId("otel-telemetry-sink"), "aws");
  assert.match(aws.target.telemetry, /cloudwatch-agent-otlp/);
  assert.ok(aws.rationale.some((line) => line.includes("14318") && line.includes("4318")));
  assert.match(mapLocalApi(byId("otel-telemetry-sink"), "azure").target.telemetry, /azure-monitor-opentelemetry-distro-java/);
});

test("desktop companion: S3 and CloudFront distribution with OIDC CI and no runtime; Artifact Signing flagged for Brazil", () => {
  const aws = mapLocalApi(byId("mydigitalbuddy-desktop"), "aws");
  assert.match(aws.target.distribution, /s3 privado/);
  assert.equal(aws.target.runtime, "nenhum: aplicativo local, sem rede");
  const azure = mapLocalApi(byId("mydigitalbuddy-desktop"), "azure");
  assert.match(azure.target.signing, /Brasil nao consta/);
});

test("unknown kinds and states fail closed instead of guessing a mapping", () => {
  assert.throws(() => mapLocalApi({ ...byId("aihealthresearch-api"), kind: "soap-service" }, "aws"), /Unknown API kind/);
  assert.throws(() => mapLocalApi({ ...byId("aihealthresearch-api"), state: "mainframe" }, "azure"), /Unknown state kind/);
});

test("AIHealthResearch as-is model: findings and monthly cost reproduce the hand calculation (about US$ 6.047)", () => {
  const model = load("aws/aihealthresearch.as-is.model.json");
  assert.equal(reviewArchitecture(kb, model).status, "pass_with_findings");
  const cost = estimateMonthlyCost(kb.prices.aws, model.cost_items);
  assert.ok(Math.abs(cost.total_usd - 6046.85) < 0.05, `as-is total ${cost.total_usd}`);
  const sagemaker = cost.lines.find((line) => line.sku.endsWith("sagemaker_hosting_ml_g5_xlarge_hour"));
  assert.ok(Math.abs(sagemaker.monthly_usd - 3495.24) < 0.01, "always-on endpoint is the largest single line");
});

test("AIHealthResearch target model: about US$ 2.736 per month, a 55% reduction, with the same production database and search", () => {
  const asIs = estimateMonthlyCost(kb.prices.aws, load("aws/aihealthresearch.as-is.model.json").cost_items);
  const target = estimateMonthlyCost(kb.prices.aws, load("aws/aihealthresearch.target.model.json").cost_items);
  assert.ok(Math.abs(target.total_usd - 2735.53) < 0.05, `target total ${target.total_usd}`);
  const saving = (asIs.total_usd - target.total_usd) / asIs.total_usd;
  assert.ok(saving > 0.5 && saving < 0.6, `saving ${saving}`);
  const auroraLines = target.lines.filter((line) => line.sku.includes("aurora_pg"));
  const asIsAurora = asIs.lines.filter((line) => line.sku.includes("aurora_pg"));
  assert.equal(auroraLines.reduce((s, l) => s + l.monthly_usd, 0).toFixed(2), asIsAurora.reduce((s, l) => s + l.monthly_usd, 0).toFixed(2));
});

test("MyDigitalBuddy model: passes review, has no runtime and costs about US$ 0,05 per month in measured S3 storage", () => {
  const model = load("aws/mydigitalbuddy.model.json");
  assert.equal(reviewArchitecture(kb, model).status, "pass");
  const cost = estimateMonthlyCost(kb.prices.aws, model.cost_items);
  assert.ok(Math.abs(cost.total_usd - 0.05) < 0.01, `desktop total ${cost.total_usd}`);
  assert.equal(model.compute.length, 0, "no compute: the app has no backend");
});

test("Azure AIHealthResearch model: passes review with the Brazil South caveats recorded as configuration, not hidden", () => {
  const model = load("azure/aihealthresearch.target.model.json");
  const result = reviewArchitecture(kb, model);
  assert.equal(result.status, "pass");
  assert.ok(model.unverified_costs.some((item) => item.includes("GPU Azure NV36ads")));
});

test("science-studio dark API: ECS Express or Container Apps for the job API, object storage for project files", () => {
  const aws = mapLocalApi(byId("science-studio-dark-api"), "aws");
  assert.equal(aws.target.compute, "ecs-express");
  assert.match(aws.target.storage, /s3 privado/);
  assert.ok(aws.forbidden.includes("Amazon Bedrock"));
  const azure = mapLocalApi(byId("science-studio-dark-api"), "azure");
  assert.match(azure.target.compute, /container-apps/);
  assert.match(azure.target.storage, /blob privado/);
});

test("rag-graph-laya model server: 15 s p95 keeps capacity scheduled on AWS and an online endpoint on Azure", () => {
  assert.match(mapLocalApi(byId("rag-graph-laya-model-server"), "aws").target.ml, /sagemaker-realtime com agenda/);
  assert.match(mapLocalApi(byId("rag-graph-laya-model-server"), "azure").target.ml, /azure-ml-online-endpoint/);
});

test("inventory: the eight local APIs from the 2026-11-14 workspace scan are described, and every source file exists", () => {
  assert.deepEqual(apis.map((api) => api.id).sort(), [
    "aihealthresearch-api",
    "aihealthresearch-model-server",
    "aihealthresearch-workers",
    "mydigitalbuddy-desktop",
    "otel-telemetry-sink",
    "rag-graph-laya-model-server",
    "rag-graph-laya-web",
    "science-studio-dark-api",
  ]);
  for (const api of apis) {
    const sourcePath = api.source.split(" (")[0];
    assert.ok(existsSync(resolve(HERE, "..", "..", sourcePath)), `${api.id}: source not found: ${sourcePath}`);
  }
});
