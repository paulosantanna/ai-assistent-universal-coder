import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { dirname, resolve } from "node:path";
import { test } from "node:test";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");

// Drives a real stdio server process with newline-delimited JSON-RPC, exactly as an MCP client would.
async function talk(script, lines) {
  const child = spawn(process.execPath, [resolve(ROOT, script)], { stdio: ["pipe", "pipe", "pipe"] });
  let stdout = "";
  let stderr = "";
  child.stdout.setEncoding("utf8");
  child.stderr.setEncoding("utf8");
  child.stdout.on("data", (chunk) => { stdout += chunk; });
  child.stderr.on("data", (chunk) => { stderr += chunk; });
  for (const line of lines) child.stdin.write(`${line}\n`);
  child.stdin.end();
  const timeout = setTimeout(() => child.kill(), 20000);
  const code = await new Promise((done) => child.on("close", done));
  clearTimeout(timeout);
  assert.equal(stderr, "", `server wrote to stderr: ${stderr}`);
  return { code, messages: stdout.trim().split("\n").filter(Boolean).map((line) => JSON.parse(line)) };
}

const call = (id, name, args = {}) => JSON.stringify({ jsonrpc: "2.0", id, method: "tools/call", params: { name, arguments: args } });

test("AWS server: handshake, tool catalogue, read-only annotations and a real tool call", async () => {
  const { code, messages } = await talk("providers/aws/server.mjs", [
    JSON.stringify({ jsonrpc: "2.0", id: 1, method: "initialize", params: { protocolVersion: "2025-11-25", capabilities: {}, clientInfo: { name: "test", version: "0" } } }),
    JSON.stringify({ jsonrpc: "2.0", method: "notifications/initialized" }),
    JSON.stringify({ jsonrpc: "2.0", id: 2, method: "tools/list" }),
    call(3, "list_patterns", {}),
    call(4, "get_pattern", { id: "aws.nope" }),
  ]);
  assert.equal(code, 0);
  assert.equal(messages.length, 4, "notifications get no response");
  const init = messages.find((m) => m.id === 1);
  assert.equal(init.result.protocolVersion, "2025-11-25");
  assert.equal(init.result.serverInfo.name, "aws-architecture-mcp");
  const tools = messages.find((m) => m.id === 2).result.tools;
  assert.deepEqual(tools.map((t) => t.name).sort(), ["estimate_monthly_cost", "get_pattern", "list_patterns", "list_pitfalls", "map_local_api", "review_architecture"]);
  for (const tool of tools) {
    assert.equal(tool.inputSchema.type, "object", tool.name);
    assert.equal(tool.annotations.readOnlyHint, true, tool.name);
  }
  const listed = messages.find((m) => m.id === 3).result;
  assert.ok(listed.structuredContent.patterns.length >= 8);
  assert.equal(listed.isError, false);
  const failed = messages.find((m) => m.id === 4).result;
  assert.equal(failed.isError, true, "unknown pattern is reported as a tool error");
});

test("Azure server: rejects an AWS SKU and returns pitfalls", async () => {
  const { messages } = await talk("providers/azure/server.mjs", [
    call(1, "list_pitfalls", {}),
    call(2, "estimate_monthly_cost", { items: [{ sku: "aws.sa-east-1.alb_hour", units_per_month: 1 }] }),
    call(3, "estimate_monthly_cost", { items: [{ sku: "azure.brazilsouth.invented", units_per_month: 1 }] }),
  ]);
  const pitfalls = messages.find((m) => m.id === 1).result.structuredContent.pitfalls;
  assert.ok(pitfalls.length >= 12);
  assert.equal(messages.find((m) => m.id === 2).result.isError, true, "cross-provider SKU is refused");
  const unknown = messages.find((m) => m.id === 3).result;
  assert.equal(unknown.isError, true);
  assert.match(unknown.content[0].text, /Unknown SKU/);
});

test("protocol errors: parse error, invalid request and unknown method use JSON-RPC codes", async () => {
  const { messages } = await talk("providers/aws/server.mjs", [
    "{not json",
    JSON.stringify({ jsonrpc: "2.0", id: 9, method: "resources/list" }),
  ]);
  assert.equal(messages[0].error.code, -32700);
  assert.equal(messages[1].error.code, -32601);
  assert.equal(messages[1].id, 9);
});
