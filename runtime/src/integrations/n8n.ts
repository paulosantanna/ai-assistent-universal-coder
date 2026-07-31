import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";

export interface N8nConfig {
  baseUrl: string;
  webhookPath: string;
  allowedWorkflows: string[];
  dryRun: boolean;
  timeoutMs: number;
}

export interface N8nTriggerRequest {
  workflowId: string;
  payload: Record<string, unknown>;
  correlationId?: string;
}

export interface N8nTriggerResult {
  workflowId: string;
  correlationId: string;
  dryRun: boolean;
  accepted: boolean;
  status?: number;
  response?: unknown;
}

export const N8N_WORKFLOW_TEMPLATES = [
  { id: "aeos-quality-gates", purpose: "Execute allowlisted AEOS quality gates" },
  { id: "aeos-observability-bootstrap", purpose: "Provision governed observability workflows" },
  { id: "spec-driven-delivery", purpose: "Orchestrate an approved specification delivery" }
] as const;

const CONFIG_FILE = join(".aeos-runtime", "n8n", "config.json");

function writeJson(path: string, value: unknown): void {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}

function validateUrl(raw: string): URL {
  const url = new URL(raw);
  if (!['http:', 'https:'].includes(url.protocol)) throw new Error("N8N URL must use HTTP(S).");
  if (url.username || url.password) throw new Error("Credentials must not be embedded in the N8N URL.");
  const local = new Set(["localhost", "127.0.0.1", "::1"]);
  if (url.protocol !== "https:" && !local.has(url.hostname)) {
    throw new Error("Remote N8N endpoints must use HTTPS.");
  }
  return url;
}

function normalize(config: N8nConfig): N8nConfig {
  const baseUrl = validateUrl(config.baseUrl).toString().replace(/\/$/, "");
  const webhookPath = config.webhookPath.startsWith("/") ? config.webhookPath : `/${config.webhookPath}`;
  const allowedWorkflows = [...new Set([
    ...config.allowedWorkflows,
    ...N8N_WORKFLOW_TEMPLATES.map((item) => item.id)
  ])].sort();
  if (!Number.isInteger(config.timeoutMs) || config.timeoutMs < 100 || config.timeoutMs > 120_000) {
    throw new Error("N8N timeout must be between 100 and 120000 ms.");
  }
  return { ...config, baseUrl, webhookPath, allowedWorkflows };
}

export function configureN8n(projectPath: string, config: N8nConfig): N8nConfig {
  const normalized = normalize(config);
  writeJson(join(projectPath, CONFIG_FILE), normalized);
  return normalized;
}

export function readN8nConfig(projectPath: string): N8nConfig {
  const path = join(projectPath, CONFIG_FILE);
  if (!existsSync(path)) throw new Error("N8N is not configured for this project.");
  return normalize(JSON.parse(readFileSync(path, "utf8")) as N8nConfig);
}

export function listN8nTemplates(): typeof N8N_WORKFLOW_TEMPLATES {
  return N8N_WORKFLOW_TEMPLATES;
}

export async function triggerN8n(projectPath: string, request: N8nTriggerRequest): Promise<N8nTriggerResult> {
  const config = readN8nConfig(projectPath);
  if (!config.allowedWorkflows.includes(request.workflowId)) {
    throw new Error(`N8N workflow is not allowlisted: ${request.workflowId}`);
  }
  const correlationId = request.correlationId ?? createHash("sha256")
    .update(`${request.workflowId}:${JSON.stringify(request.payload)}:${Date.now()}`)
    .digest("hex").slice(0, 24);
  if (config.dryRun) return { workflowId: request.workflowId, correlationId, dryRun: true, accepted: true };

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), config.timeoutMs);
  try {
    const endpoint = new URL(`${config.webhookPath}/${encodeURIComponent(request.workflowId)}`, `${config.baseUrl}/`);
    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "content-type": "application/json", "x-aeos-correlation-id": correlationId },
      body: JSON.stringify({ correlationId, payload: request.payload }),
      signal: controller.signal
    });
    const text = await response.text();
    let body: unknown = text;
    try { body = text ? JSON.parse(text) : null; } catch { /* response may be plain text */ }
    if (!response.ok) throw new Error(`N8N request failed with HTTP ${response.status}.`);
    return { workflowId: request.workflowId, correlationId, dryRun: false, accepted: true, status: response.status, response: body };
  } finally {
    clearTimeout(timer);
  }
}
