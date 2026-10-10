/**
 * Stdio MCP for the local dark-videos API.
 * Reads status and ranking. start_run only enqueues the app pipeline.
 * Cookies and CSRF tokens are never written to logs or tool results.
 */

import { request as httpRequest } from "node:http";
import { request as httpsRequest } from "node:https";

const PROTOCOL = "2024-11-05";
const SERVER = { name: "dark-videos-pipeline", version: "1.0.0" };

const TOOLS = [
  {
    name: "pipeline.status",
    description: "Read the active dark-videos run and the latest run summary.",
    inputSchema: { type: "object", properties: {}, additionalProperties: false },
  },
  {
    name: "mining.board",
    description: "Read connector status and the latest ranked videos, including JEV heat.",
    inputSchema: { type: "object", properties: {}, additionalProperties: false },
  },
  {
    name: "pipeline.start_run",
    description: "Enqueue one dark-videos pipeline run through the local API. Does not post to a network.",
    inputSchema: {
      type: "object",
      properties: {
        target_count: { type: "integer", minimum: 1, maximum: 50 },
        dry_run: { type: "boolean" },
      },
      additionalProperties: false,
    },
  },
];

function apiBase() {
  return (process.env.DARKVIDEOS_API_BASE || "http://127.0.0.1:8000").replace(/\/$/, "");
}

function cookieHeader() {
  const token = process.env.DARKVIDEOS_SESSION_COOKIE || "";
  if (!token) return "";
  const name = process.env.DARKVIDEOS_COOKIE_NAME || "dv_session";
  return `${name}=${token}`;
}

function callApi(method, path, body) {
  const target = new URL(path, `${apiBase()}/`);
  const payload = body === undefined ? null : Buffer.from(JSON.stringify(body));
  const headers = { accept: "application/json" };
  const cookie = cookieHeader();
  if (cookie) headers.cookie = cookie;
  if (payload) {
    headers["content-type"] = "application/json";
    headers["content-length"] = String(payload.length);
    const csrf = process.env.DARKVIDEOS_CSRF_TOKEN || "";
    if (csrf) headers["x-csrf-token"] = csrf;
    headers.origin = process.env.DARKVIDEOS_ORIGIN || "http://localhost:3000";
  }
  const transport = target.protocol === "https:" ? httpsRequest : httpRequest;
  return new Promise((resolve) => {
    const req = transport(
      target,
      { method, headers },
      (res) => {
        const chunks = [];
        res.on("data", (chunk) => chunks.push(chunk));
        res.on("end", () => {
          const text = Buffer.concat(chunks).toString("utf8");
          let parsed = text;
          try {
            parsed = text ? JSON.parse(text) : null;
          } catch {
            parsed = { raw: "unreadable_response" };
          }
          resolve({ status: res.statusCode || 0, body: parsed });
        });
      },
    );
    req.on("error", () => resolve({ status: 0, body: { detail: "api_unreachable" } }));
    if (payload) req.write(payload);
    req.end();
  });
}

function missingSession() {
  return { error: "session_cookie_missing" };
}

async function pipelineStatus() {
  if (!cookieHeader()) return missingSession();
  const [active, recent] = await Promise.all([
    callApi("GET", "/api/pipeline/runs/active"),
    callApi("GET", "/api/pipeline/runs?limit=1"),
  ]);
  return { active: active.body, recent: recent.body };
}

async function miningBoard() {
  if (!cookieHeader()) return missingSession();
  const [candidates, sources] = await Promise.all([
    callApi("GET", "/api/mining/candidates"),
    callApi("GET", "/api/mining/sources"),
  ]);
  return { candidates: candidates.body, sources: sources.body };
}

async function startRun(args) {
  if (!cookieHeader()) return missingSession();
  if (!process.env.DARKVIDEOS_CSRF_TOKEN) return { error: "csrf_token_missing" };
  const body = {};
  if (Number.isInteger(args.target_count)) body.target_count = args.target_count;
  if (typeof args.dry_run === "boolean") body.dry_run = args.dry_run;
  const result = await callApi("POST", "/api/pipeline/runs", body);
  return { status: result.status, run: result.body };
}

async function dispatchTool(name, args) {
  if (name === "pipeline.status") return pipelineStatus();
  if (name === "mining.board") return miningBoard();
  if (name === "pipeline.start_run") return startRun(args || {});
  return { error: "unknown_tool" };
}

function send(message) {
  const json = JSON.stringify(message);
  const header = `Content-Length: ${Buffer.byteLength(json)}\r\n\r\n`;
  process.stdout.write(header + json);
}

function resultFor(id, value, isError = false) {
  send({
    jsonrpc: "2.0",
    id,
    result: {
      content: [{ type: "text", text: JSON.stringify(value) }],
      isError,
    },
  });
}

async function handle(message) {
  const { id, method, params } = message;
  if (method === "initialize") {
    send({
      jsonrpc: "2.0",
      id,
      result: { protocolVersion: PROTOCOL, capabilities: { tools: {} }, serverInfo: SERVER },
    });
    return;
  }
  if (method === "notifications/initialized" || method === "initialized") return;
  if (method === "tools/list") {
    send({ jsonrpc: "2.0", id, result: { tools: TOOLS } });
    return;
  }
  if (method === "tools/call") {
    const name = params?.name;
    const args = params?.arguments || {};
    const value = await dispatchTool(name, args);
    const isError = Boolean(value && value.error);
    resultFor(id, value, isError);
    return;
  }
  if (method === "ping") {
    send({ jsonrpc: "2.0", id, result: {} });
    return;
  }
  if (id !== undefined) {
    send({ jsonrpc: "2.0", id, error: { code: -32601, message: "method_not_found" } });
  }
}

function listen() {
  let buffer = Buffer.alloc(0);
  process.stdin.on("data", (chunk) => {
    buffer = Buffer.concat([buffer, chunk]);
    for (;;) {
      const headerEnd = buffer.indexOf("\r\n\r\n");
      if (headerEnd === -1) return;
      const header = buffer.slice(0, headerEnd).toString("utf8");
      const match = /content-length:\s*(\d+)/i.exec(header);
      if (!match) {
        buffer = buffer.slice(headerEnd + 4);
        continue;
      }
      const length = Number(match[1]);
      const start = headerEnd + 4;
      if (buffer.length < start + length) return;
      const body = buffer.slice(start, start + length).toString("utf8");
      buffer = buffer.slice(start + length);
      try {
        void handle(JSON.parse(body));
      } catch {
        send({ jsonrpc: "2.0", id: null, error: { code: -32700, message: "parse_error" } });
      }
    }
  });
}

async function selfTest() {
  delete process.env.DARKVIDEOS_SESSION_COOKIE;
  delete process.env.DARKVIDEOS_CSRF_TOKEN;
  const names = TOOLS.map((tool) => tool.name);
  if (names.join(",") !== "pipeline.status,mining.board,pipeline.start_run") {
    throw new Error("tool list drifted");
  }
  const blocked = await startRun({});
  if (blocked.error !== "session_cookie_missing") throw new Error("start_run must require a session");
  const rendered = JSON.stringify(blocked);
  if (rendered.includes("dv_session") || rendered.includes("csrf")) {
    throw new Error("tool error leaked a credential field");
  }
  process.stdout.write("ok\n");
}

if (process.argv.includes("--self-test")) {
  void selfTest();
} else {
  listen();
}
