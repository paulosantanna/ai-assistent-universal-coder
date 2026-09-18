const assert = require("node:assert/strict");
const { spawn } = require("node:child_process");
const { join } = require("node:path");

const SERVER = join(process.cwd(), "aeos/mcp-servers/rag-node-mcp.mjs");

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
    responses.push(JSON.parse(rest.slice(start, start + length).toString("utf8")));
    rest = rest.slice(start + length);
  }
  return responses;
}

function session(messages) {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [SERVER], { stdio: ["pipe", "pipe", "pipe"] });
    let stdout = Buffer.alloc(0);
    let stderr = "";
    const timer = setTimeout(() => {
      child.kill();
      reject(new Error(`rag-node timed out. stderr=${stderr}`));
    }, 5000);
    child.stdout.on("data", (chunk) => {
      stdout = Buffer.concat([stdout, chunk]);
      if (parseFrames(stdout).length >= messages.filter((m) => m.id !== undefined).length) {
        clearTimeout(timer);
        child.kill();
        resolve(parseFrames(stdout));
      }
    });
    child.stderr.on("data", (c) => {
      stderr += c.toString("utf8");
    });
    child.on("error", reject);
    for (const message of messages) child.stdin.write(framed(message));
  });
}

function payload(response) {
  const text = response?.result?.content?.[0]?.text || "{}";
  return JSON.parse(text);
}

describe("RAG Node MCP", () => {
  it("lists six governed tools", async () => {
    const responses = await session([
      { jsonrpc: "2.0", id: 1, method: "initialize", params: { protocolVersion: "2024-11-05" } },
      { jsonrpc: "2.0", id: 2, method: "tools/list", params: {} }
    ]);
    const tools = responses.find((r) => r.id === 2)?.result?.tools || [];
    assert.equal(tools.length, 6);
    assert.ok(tools.some((t) => t.name === "rag_node.ingest"));
    assert.ok(tools.some((t) => t.name === "rag_node.express_plan"));
  });

  it("serves the TLC public curriculum without claiming video transcripts", async () => {
    const responses = await session([
      { jsonrpc: "2.0", id: 1, method: "tools/call", params: { name: "rag_node.curriculum", arguments: {} } }
    ]);
    const data = payload(responses[0]);
    assert.equal(data.scope, "public-outline-only");
    assert.ok(data.sections.length >= 3);
    assert.match(data.transcript_policy, /voiceai/);
  });

  it("ingests, retrieves and grounds answers with citations", async () => {
    const child = spawn(process.execPath, [SERVER], { stdio: ["pipe", "pipe", "pipe"] });
    const calls = [
      { jsonrpc: "2.0", id: 1, method: "tools/call", params: { name: "rag_node.ingest", arguments: { documents: [{ id: "tlc-intro", text: "RAG com Node.js usa vetorização e busca vetorial para recuperar chunks antes de gerar respostas com Express e Server-Sent Events." }] } } },
      { jsonrpc: "2.0", id: 2, method: "tools/call", params: { name: "rag_node.search", arguments: { query: "busca vetorial chunks Express" } } },
      { jsonrpc: "2.0", id: 3, method: "tools/call", params: { name: "rag_node.chat", arguments: { question: "Como recuperar chunks com busca vetorial no Express?" } } }
    ];
    const responses = await new Promise((resolve, reject) => {
      let stdout = Buffer.alloc(0);
      const timer = setTimeout(() => {
        child.kill();
        reject(new Error("rag-node pipeline timed out"));
      }, 5000);
      child.stdout.on("data", (chunk) => {
        stdout = Buffer.concat([stdout, chunk]);
        if (parseFrames(stdout).length >= 3) {
          clearTimeout(timer);
          child.kill();
          resolve(parseFrames(stdout));
        }
      });
      child.on("error", reject);
      for (const message of calls) child.stdin.write(framed(message));
    });
    assert.equal(payload(responses[0]).status, "INGESTED");
    const search = payload(responses[1]);
    assert.equal(search.status, "RESULTS");
    assert.ok(search.results[0].chunk_id.includes("tlc-intro#c"));
    const chat = payload(responses[2]);
    assert.equal(chat.status, "GROUNDED");
    assert.ok(chat.citations.length >= 1);
  });

  it("refuses weakly supported questions instead of hallucinating", async () => {
    const child = spawn(process.execPath, [SERVER], { stdio: ["pipe", "pipe", "pipe"] });
    const calls = [
      { jsonrpc: "2.0", id: 1, method: "tools/call", params: { name: "rag_node.ingest", arguments: { documents: [{ id: "d1", text: "Vetorização converte documentos em embeddings para busca semântica com Node.js." }] } } },
      { jsonrpc: "2.0", id: 2, method: "tools/call", params: { name: "rag_node.chat", arguments: { question: "xyzzy qwerty plugh blorp zxx" } } }
    ];
    const responses = await new Promise((resolve, reject) => {
      let stdout = Buffer.alloc(0);
      const timer = setTimeout(() => {
        child.kill();
        reject(new Error("rag-node refusal timed out"));
      }, 5000);
      child.stdout.on("data", (chunk) => {
        stdout = Buffer.concat([stdout, chunk]);
        if (parseFrames(stdout).length >= 2) {
          clearTimeout(timer);
          child.kill();
          resolve(parseFrames(stdout));
        }
      });
      child.on("error", reject);
      for (const message of calls) child.stdin.write(framed(message));
    });
    assert.equal(payload(responses[0]).status, "INGESTED");
    assert.equal(payload(responses[1]).status, "REFUSED");
  });
});
