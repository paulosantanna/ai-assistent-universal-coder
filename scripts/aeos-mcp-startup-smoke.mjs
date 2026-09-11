#!/usr/bin/env node
import { spawn } from "node:child_process";

const MCP_CASES = [
  ["complete-docs", ["--mode", "complete-docs"]],
  ["continuous-training", ["--mode", "continuous-training"]],
  ["docs-angular-current", ["--mode", "language-docs", "--profile", "docs-angular-current"]],
  ["docs-java-11", ["--mode", "language-docs", "--profile", "docs-java-11"]],
  ["docs-java-17", ["--mode", "language-docs", "--profile", "docs-java-17"]],
  ["docs-java-21", ["--mode", "language-docs", "--profile", "docs-java-21"]],
  ["docs-java-25", ["--mode", "language-docs", "--profile", "docs-java-25"]],
  ["docs-java-26", ["--mode", "language-docs", "--profile", "docs-java-26"]],
  ["docs-javascript-current", ["--mode", "language-docs", "--profile", "docs-javascript-current"]],
  ["docs-node-current", ["--mode", "language-docs", "--profile", "docs-node-current"]],
  ["docs-python-current", ["--mode", "language-docs", "--profile", "docs-python-current"]],
  ["docs-typescript-current", ["--mode", "language-docs", "--profile", "docs-typescript-current"]],
  ["medical-research", ["--mode", "medical-research"]],
  ["universal-project", ["--mode", "universal-project"]]
];

function framed(message) {
  const payload = JSON.stringify(message);
  return `Content-Length: ${Buffer.byteLength(payload, "utf8")}\r\n\r\n${payload}`;
}

function parseFrames(buffer) {
  const responses = [];
  let rest = buffer;
  while (rest.length) {
    const headerEnd = rest.indexOf("\r\n\r\n");
    if (headerEnd < 0) break;
    const header = rest.slice(0, headerEnd).toString("utf8");
    const match = /Content-Length:\s*(\d+)/i.exec(header);
    if (!match) break;
    const length = Number(match[1]);
    const start = headerEnd + 4;
    if (rest.length < start + length) break;
    const body = rest.slice(start, start + length).toString("utf8");
    responses.push(JSON.parse(body));
    rest = rest.slice(start + length);
  }
  return responses;
}

function request(name, args, messages) {
  return new Promise((resolve, reject) => {
    const child = spawn("node", ["aeos/mcp-servers/aeos-readonly-mcp.mjs", ...args], {
      cwd: process.cwd(),
      stdio: ["pipe", "pipe", "pipe"]
    });
    let stdout = Buffer.alloc(0);
    let stderr = "";
    const timer = setTimeout(() => {
      child.kill();
      reject(new Error(`${name} timed out. stderr=${stderr}`));
    }, 2500);

    child.stdout.on("data", (chunk) => {
      stdout = Buffer.concat([stdout, chunk]);
      const responses = parseFrames(stdout);
      if (responses.length >= messages.filter((item) => item.id !== undefined).length) {
        clearTimeout(timer);
        child.kill();
        resolve(responses);
      }
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString("utf8");
    });
    child.on("exit", (code) => {
      if (code !== null && code !== 0 && code !== 143 && code !== 130) {
        clearTimeout(timer);
        reject(new Error(`${name} exited with ${code}. stderr=${stderr}`));
      }
    });
    for (const message of messages) child.stdin.write(framed(message));
  });
}

async function main() {
  const failures = [];
  for (const [name, args] of MCP_CASES) {
    try {
      const responses = await request(name, args, [
        { jsonrpc: "2.0", id: 1, method: "initialize", params: { protocolVersion: "2025-06-18", capabilities: {}, clientInfo: { name: "aeos-smoke", version: "1" } } },
        { jsonrpc: "2.0", method: "notifications/initialized", params: {} },
        { jsonrpc: "2.0", id: 2, method: "tools/list", params: {} },
        { jsonrpc: "2.0", id: 3, method: "prompts/list", params: {} },
        { jsonrpc: "2.0", id: 4, method: "resources/list", params: {} }
      ]);
      const initialize = responses.find((item) => item.id === 1);
      const tools = responses.find((item) => item.id === 2);
      if (!initialize?.result?.serverInfo?.name) throw new Error("missing initialize serverInfo");
      if (!Array.isArray(tools?.result?.tools) || tools.result.tools.length === 0) throw new Error("missing tools");
      console.log(`${name}: PASS (${tools.result.tools.length} tools)`);
    } catch (error) {
      failures.push(`${name}: ${error.message}`);
    }
  }

  if (failures.length) {
    console.error(JSON.stringify({ status: "FAIL", failures }, null, 2));
    process.exitCode = 1;
    return;
  }
  console.log(JSON.stringify({ status: "PASS", checked: MCP_CASES.length }, null, 2));
}

await main();
