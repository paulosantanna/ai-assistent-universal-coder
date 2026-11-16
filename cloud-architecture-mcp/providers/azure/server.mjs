#!/usr/bin/env node
// Azure architecture MCP: governed, read-only advisor over verified Azure patterns, pitfalls, prices and rules.
// Runs on stdio. No Azure credentials are needed or read. The official Azure MCP server is developed in
// microsoft/mcp; this server complements it with architecture review, pitfalls and cost checks.
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { createKb } from "../../shared/engine.mjs";
import { createMcpServer, serveStdio } from "../../shared/stdio-mcp.mjs";
import { createTools } from "../../shared/tools.mjs";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..", "..");

export function createAzureServer(root = ROOT) {
  const kb = createKb(root);
  const { tools, handlers } = createTools(kb, "azure");
  return createMcpServer({ name: "azure-architecture-mcp", version: "0.1.0", tools, handlers });
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  serveStdio(createAzureServer());
}
