import assert from "node:assert/strict";
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import { configureN8n, listN8nTemplates, readN8nConfig, triggerN8n } from "./n8n.js";

const project = (): string => mkdtempSync(join(tmpdir(), "aeos-n8n-"));

test("configures N8N with safe defaults and built-in workflows", () => {
  const root = project();
  const config = configureN8n(root, { baseUrl: "http://localhost:5678", webhookPath: "webhook/aeos", allowedWorkflows: [], dryRun: true, timeoutMs: 5000 });
  assert.equal(config.baseUrl, "http://localhost:5678");
  assert.ok(config.allowedWorkflows.includes("spec-driven-delivery"));
  assert.deepEqual(readN8nConfig(root), config);
});

test("rejects insecure remote endpoints", () => {
  assert.throws(() => configureN8n(project(), { baseUrl: "http://example.com", webhookPath: "/x", allowedWorkflows: [], dryRun: true, timeoutMs: 5000 }), /HTTPS/);
});

test("rejects embedded credentials", () => {
  assert.throws(() => configureN8n(project(), { baseUrl: "https://user:pass@example.com", webhookPath: "/x", allowedWorkflows: [], dryRun: true, timeoutMs: 5000 }), /Credentials/);
});

test("blocks workflows outside the allowlist", async () => {
  const root = project();
  configureN8n(root, { baseUrl: "http://localhost:5678", webhookPath: "/webhook", allowedWorkflows: [], dryRun: true, timeoutMs: 5000 });
  await assert.rejects(triggerN8n(root, { workflowId: "unknown", payload: {} }), /allowlisted/);
});

test("dry-run returns traceable result without network access", async () => {
  const root = project();
  configureN8n(root, { baseUrl: "http://localhost:5678", webhookPath: "/webhook", allowedWorkflows: [], dryRun: true, timeoutMs: 5000 });
  const result = await triggerN8n(root, { workflowId: "spec-driven-delivery", payload: { spec: "checkout" }, correlationId: "corr-1" });
  assert.deepEqual(result, { workflowId: "spec-driven-delivery", correlationId: "corr-1", dryRun: true, accepted: true });
});

test("publishes governed workflow templates", () => {
  assert.deepEqual(listN8nTemplates().map((item) => item.id), ["aeos-quality-gates", "aeos-observability-bootstrap", "spec-driven-delivery"]);
});
