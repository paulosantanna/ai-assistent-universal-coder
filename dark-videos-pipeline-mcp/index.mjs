/**
 * Stdio MCP for the local dark-videos API.
 * Reads status and ranking. start_run only enqueues the app pipeline.
 * Cookies and CSRF tokens are never written to logs or tool results.
 * Performance optimizations: caching, early termination, minimal API calls.
 * LAYA heat scoring: replaced Redis with in-memory ChromaDB for training vectors.
 */

import { request as httpRequest } from "node:http";
import { request as httpsRequest } from "node:https";
import {
  initChroma,
  storeLayaVector,
  getLayaVectorsByHeatScore,
  querySimilarLaya,
  getAllLayaVectors,
  getLayaVectorCount,
  shutdownChroma,
} from "./data/chroma/client.mjs";

// -- Performance: Cache time-to-live (seconds) --
const CACHE_TTL = {
  status: 5,     // pipeline.status cache 5s
  mining: 10,    // mining.board cache 10s (wider lookback)
  run: 3,        // enqueue result cache 3s
};

// -- Performance: Memoized cache with TTL --
const cache = {
  entries: new Map(),
  get(key) {
    const entry = this.entries.get(key);
    if (!entry) return null;
    if (Date.now() - entry.timestamp > CACHE_TTL[key] * 1000) {
      this.entries.delete(key);
      return null;
    }
    return entry.value;
  },
  set(key, value) {
    this.entries.set(key, { value, timestamp: Date.now() });
  },
};

const PROTOCOL = "2024-11-05";
const SERVER = { name: "dark-videos-pipeline", version: "1.0.0" };

// -- LAYA Heat Scoring: Initialize ChromaDB in-memory --
// ChromaDB runs in-process (via subprocess) and lives while the app lives.
// It dies automatically on app closure via the beforeExit/exit handlers.
await initChroma();

const TOOLS = [
  {
    name: "pipeline.status",
    description: "Read the active dark-videos run and the latest run summary. Cached for 5s.",
    inputSchema: { type: "object", properties: {}, additionalProperties: false },
  },
  {
    name: "mining.board",
    description: "Read connector status and the latest ranked videos, including LAYA heat score from ChromaDB training vectors. Cached for 10s. Starts with 7-day lookback, widens only if pool cannot fill target_count.",
    inputSchema: { type: "object", properties: {}, additionalProperties: false },
  },
  {
    name: "pipeline.start_run",
    description: "Enqueue one dark-videos pipeline run through the local API. Does not post to a network. target_count defaults to 20; use 10 for 50% fewer resources.",
    inputSchema: {
      type: "object",
      properties: {
        target_count: { type: "integer", minimum: 1, maximum: 50, description: "Use 10 instead of default 20 for 50% fewer resources" },
        dry_run: { type: "boolean", description: "Use dry_run=true for simulation; no network calls, no synthetic samples in real runs" },
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

// -- Performance: Early termination check --
function shouldEarlyTerminate(stage, context) {
  // Stage: "mining" - if no connectors configured and real run, fail fast
  if (stage === "mining") {
    const hasYouTubeKey = !!process.env.MINING_YOUTUBE_API_KEY;
    const hasProvider = !!process.env.MINING_PROVIDER_BASE_URL;
    if (!hasYouTubeKey && !hasProvider) {
      return { error: "connectors_unconfigured", message: "No YouTube Data API key or provider configured. Real runs require connectors." };
    }
  }
  // Stage: "ranking" - if fewer than target_count videos, fail early
  if (stage === "ranking") {
    const candidateCount = context?.candidateCount;
    if (candidateCount !== undefined && candidateCount < (context?.targetCount || 20)) {
      return { error: "insufficient_candidates", message: `Only ${candidateCount} candidates available, need ${context?.targetCount || 20}` };
    }
  }
  // Stage: "publish" - dispatch is the only publisher; reject MCP-originated posts
  if (stage === "publish") {
    return { error: "publish_denied", message: "Only dispatch publishes; MCP may only enqueue via pipeline.start_run" };
  }
  return null;
}

// -- Performance: API call with cache check --
async function callApi(method, path, body, skipCache = false) {
  // Check cache first (unless skipped)
  if (!skipCache) {
    const cached = cache.get(path);
    if (cached) return cached;
  }

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
          // Cache the response (excluding error details that change frequently)
          if (!parsed?.error && method !== "POST") {
            cache.set(path, { status: res.statusCode || 0, body: parsed });
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

// -- Performance: pipeline.status with caching --
async function pipelineStatus() {
  const cached = cache.get("pipeline.status");
  if (cached) return cached;

  if (!cookieHeader()) return { error: "session_cookie_missing", fromCache: false };

  const [active, recent] = await Promise.all([
    callApi("GET", "/api/pipeline/runs/active", {}, true), // skip cache for active since it changes
    callApi("GET", "/api/pipeline/runs?limit=1", {}, true),
  ]);
  const result = { active: active.body, recent: recent.body };
  cache.set("pipeline.status", result);
  return result;
}

// -- Performance: mining.board with connector check, ChromaDB LAYA heat, and caching --
async function miningBoard() {
  const cached = cache.get("mining.board");
  if (cached) return cached;

  if (!cookieHeader()) return { error: "session_cookie_missing" };

  // -- Performance: Early connector check --
  const connectorCheck = shouldEarlyTerminate("mining");
  if (connectorCheck.error) return connectorCheck;

  // -- Performance: LAYA heat scoring from ChromaDB --
  // Query ChromaDB for LAYA training vectors with heat scores
  let layaHeatData = {};
  try {
    const allVectors = await getAllLayaVectors();
    if (allVectors && allVectors.ids) {
      // Filter vectors with heat_score > 0.5 for the heat map
      const hotVectors = allVectors.ids.filter(id => {
        const meta = allVectors.metadatas?.find(m => m && m.id === id);
        return meta && meta.heat_score > 0.5;
      });
      layaHeatData = {
        hotVectors,
        hotVectorCount: hotVectors.length,
        totalVectorCount: allVectors.ids?.length || 0,
      };
    }
  } catch (err) {
    console.error("⚠️ ChromaDB LAYA heat query failed:", err);
    layaHeatData = { error: "chroma_unavailable", message: "ChromaDB LAYA heat scoring unavailable" };
  }

  const [candidates, sources] = await Promise.all([
    callApi("GET", "/api/mining/candidates", {}, true),
    callApi("GET", "/api/mining/sources", {}, true),
  ]);
  const result = { candidates: candidates.body, sources: sources.body, layaHeat: layaHeatData };
  cache.set("mining.board", result);
  return result;
}

// -- Performance: start_run with target_count validation --
async function startRun(args) {
  if (!cookieHeader()) return { error: "session_cookie_missing" };
  if (!process.env.DARKVIDEOS_CSRF_TOKEN) return { error: "csrf_token_missing" };

  // -- Performance: Default target_count to 10 instead of 20 --
  const target_count = args.target_count !== undefined ? Math.min(Math.max(args.target_count, 1), 50) : 10;
  const dry_run = args.dry_run !== undefined ? args.dry_run : false;

  // -- Performance: dry_run validation --
  // In dry_run mode: use synthetic sample only, no network calls
  // In real run without connectors: fail fast with connectors_unconfigured
  if (!dry_run) {
    const hasYouTubeKey = !!process.env.MINING_YOUTUBE_API_KEY;
    const hasProvider = !!process.env.MINING_PROVIDER_BASE_URL;
    if (!hasYouTubeKey && !hasProvider) {
      return { error: "connectors_unconfigured", message: "No YouTube Data API key or provider configured. Real runs require connectors. Use dry_run=true to simulate." };
    }
  }

  const body = {};
  body.target_count = target_count;
  body.dry_run = dry_run;

  // -- Performance: Cache the enqueue result --
  const result = await callApi("POST", "/api/pipeline/runs", body, true); // skip cache for POST
  cache.set(`run:${target_count}:${dry_run}`, result);
  return { status: result.status, run: result.body };
}

// -- Performance: dispatch tool with stage awareness --
async function dispatchTool(name, args) {
  // -- Performance: Pipeline start_run enforces governance --
  if (name === "pipeline.start_run") return startRun(args || {});

  // -- Performance: Status and mining board use caching --
  if (name === "pipeline.status") return pipelineStatus();
  if (name === "mining.board") return miningBoard();

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
    result: { content: [{ type: "text", text: JSON.stringify(value) }], isError },
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
  // -- Auto-cleanup: ensure ChromaDB process exits when Node.js app closes --
  process.on("beforeExit", async () => {
    try {
      await shutdownChroma();
    } catch (e) {
      console.error("Error during ChromaDB shutdown:", e);
    }
  });

  process.on("exit", async () => {
    try {
      await shutdownChroma();
    } catch (e) {
      console.error("Error during ChromaDB shutdown:", e);
    }
  });

  listen();
}