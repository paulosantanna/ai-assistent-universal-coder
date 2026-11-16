#!/usr/bin/env node
// AWS architecture MCP: governed, read-only advisor over verified AWS patterns, pitfalls, prices and rules.
// Runs on stdio. No AWS credentials are needed or read.
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { createKb } from "../../shared/engine.mjs";
import { createMcpServer, serveStdio } from "../../shared/stdio-mcp.mjs";
import { createTools } from "../../shared/tools.mjs";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..", "..");

export function createAwsServer(root = ROOT) {
  const kb = createKb(root);
  const { tools, handlers } = createTools(kb, "aws");
  return createMcpServer({ name: "aws-architecture-mcp", version: "0.1.0", tools, handlers });
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  serveStdio(createAwsServer());
}
