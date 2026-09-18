#!/usr/bin/env node
// RAG Node.js MCP — governed offline implementation of the TLC RAG-com-Node.js pipeline.
// Covers: document processing + chunking, vector-style retrieval, grounded generation,
// Express API shape and SSE streaming plan. No network, no external embedding calls.

const VERSION = "1.0.0";
const DEFAULT_CHUNK_SIZE = 800;
const DEFAULT_OVERLAP = 120;
const DEFAULT_TOP_K = 5;
const MAX_DOCUMENTS = 50;
const MAX_TEXT_CHARS = 200_000;
const REFUSAL_THRESHOLD = 0.08;
const EXCERPT_CHARS = 500;

const CURRICULUM = {
  source: "https://www.techleads.club/c/rag-com-node-js",
  course: "RAG com Node.js (Tech Leads Club)",
  scope: "public-outline-only",
  sections: [
    {
      title: "Introdução",
      lessons: [
        { title: "Apresentação do Projeto", maps_to: ["rag_node.curriculum", "rag_node.express_plan"] },
        { title: "Código fonte do curso", maps_to: ["rag_node.express_plan"] },
        { title: "Setup do ambiente", maps_to: ["rag_node.health", "rag_node.express_plan"] }
      ]
    },
    {
      title: "Desenvolvimento",
      lessons: [
        { title: "Iniciando o processamento de documentos e vetorização", maps_to: ["rag_node.ingest"] },
        { title: "Busca Vetorial e Recuperação de Chunks", maps_to: ["rag_node.search"] },
        { title: "Geração de respostas com RAG", maps_to: ["rag_node.chat"] },
        { title: "Implementação da API com Express", maps_to: ["rag_node.express_plan"] },
        { title: "Streaming de respostas com Server-Sent Events", maps_to: ["rag_node.express_plan"] }
      ]
    },
    {
      title: "Próximos passos",
      lessons: [{ title: "Ajustes finais e sugestões", maps_to: ["rag_node.chat", "rag_node.express_plan"] }]
    }
  ],
  transcript_policy: "Full lesson video transcripts require user-supplied authorized media via voiceai or aura-voice. This MCP answers from the public outline until that evidence exists."
};

const store = { documents: new Map(), chunks: [] };

function tool(name, description, properties = {}) {
  return { name, description, inputSchema: { type: "object", properties, additionalProperties: false } };
}

function listTools() {
  return [
    tool("rag_node.health", "Verify RAG Node MCP status and defaults."),
    tool("rag_node.curriculum", "Return the absorbed public TLC curriculum outline and tool mapping."),
    tool("rag_node.ingest", "Chunk authorized documents into stable retrievable units.", {
      documents: { type: "array" },
      chunk_size: { type: "integer" },
      overlap: { type: "integer" }
    }),
    tool("rag_node.search", "Retrieve top-k chunks with hybrid lexical plus TF-IDF cosine scores.", {
      query: { type: "string" },
      top_k: { type: "integer" },
      document_id: { type: "string" }
    }),
    tool("rag_node.chat", "Pack a grounded extractive answer with citations or refuse when support is weak.", {
      question: { type: "string" },
      top_k: { type: "integer" }
    }),
    tool("rag_node.express_plan", "Return the governed Express plus SSE API plan.")
  ];
}

function tokenize(text) {
  return String(text || "")
    .toLowerCase()
    .replace(/[^a-z0-9à-ú\s]/gi, " ")
    .split(/\s+/)
    .filter((t) => t.length > 1);
}

function termVector(tokens) {
  const vec = new Map();
  for (const t of tokens) vec.set(t, (vec.get(t) || 0) + 1);
  return vec;
}

function cosine(a, b) {
  let dot = 0;
  let na = 0;
  let nb = 0;
  for (const v of a.values()) na += v * v;
  for (const v of b.values()) nb += v * v;
  if (!na || !nb) return 0;
  const [small, large] = a.size <= b.size ? [a, b] : [b, a];
  for (const [k, v] of small) if (large.has(k)) dot += v * large.get(k);
  return dot / (Math.sqrt(na) * Math.sqrt(nb));
}

function chunkText(text, chunkSize, overlap) {
  const clean = String(text || "").replace(/\r\n?/g, "\n").trim();
  if (!clean) return [];
  const chunks = [];
  let start = 0;
  let index = 0;
  while (start < clean.length) {
    const end = Math.min(start + chunkSize, clean.length);
    chunks.push({ index: index++, start, end, text: clean.slice(start, end) });
    if (end >= clean.length) break;
    start = Math.max(end - overlap, start + 1);
  }
  return chunks;
}

function health() {
  return {
    status: "PASS",
    mcp: "rag-node",
    version: VERSION,
    mode: "offline-deterministic",
    network_access: false,
    defaults: { chunk_size: DEFAULT_CHUNK_SIZE, overlap: DEFAULT_OVERLAP, top_k: DEFAULT_TOP_K },
    corpus: { documents: store.documents.size, chunks: store.chunks.length }
  };
}

function curriculum() {
  return {
    status: "CURRICULUM",
    ...CURRICULUM,
    intake_lenses: [
      "voiceai: literal transcript plus relevance classification plus AEOS handoff when authorized lesson media is supplied",
      "aura-voice: media inspection plus local transcription plus technical-term preservation plus humor versus serious separation"
    ],
    evidence_required_for_verbatim: true
  };
}

function ingest(input = {}) {
  const documents = input.documents;
  if (!Array.isArray(documents) || documents.length === 0) {
    return { status: "BLOCKED", reason: "DOCUMENTS_REQUIRED" };
  }
  if (documents.length > MAX_DOCUMENTS) return { status: "BLOCKED", reason: "TOO_MANY_DOCUMENTS", max: MAX_DOCUMENTS };
  const chunkSize = Math.max(200, Math.min(Number(input.chunk_size || DEFAULT_CHUNK_SIZE), 4000));
  const overlap = Math.max(0, Math.min(Number(input.overlap ?? DEFAULT_OVERLAP), Math.floor(chunkSize / 2)));

  store.documents.clear();
  store.chunks = [];
  const ingested = [];
  for (const doc of documents) {
    const id = String(doc?.id || "").trim();
    const text = String(doc?.text || "");
    if (!id) return { status: "BLOCKED", reason: "DOCUMENT_ID_REQUIRED" };
    if (!text.trim()) return { status: "BLOCKED", reason: "DOCUMENT_TEXT_REQUIRED", document_id: id };
    if (text.length > MAX_TEXT_CHARS) return { status: "BLOCKED", reason: "DOCUMENT_TOO_LARGE", document_id: id };
    const parts = chunkText(text, chunkSize, overlap);
    store.documents.set(id, { id, chars: text.length, chunks: parts.length, metadata: doc?.metadata || {} });
    for (const part of parts) {
      store.chunks.push({
        document_id: id,
        chunk_id: `${id}#c${part.index}`,
        start: part.start,
        end: part.end,
        text: part.text,
        vector: termVector(tokenize(part.text))
      });
    }
    ingested.push({ document_id: id, chunks: parts.length });
  }
  return { status: "INGESTED", chunk_size: chunkSize, overlap, documents: ingested, total_chunks: store.chunks.length };
}

function scoreChunk(queryTokens, queryVec, chunk) {
  const cos = cosine(queryVec, chunk.vector);
  const chunkTerms = new Set(tokenize(chunk.text));
  const hits = queryTokens.filter((t) => chunkTerms.has(t)).length;
  const lexical = queryTokens.length ? hits / queryTokens.length : 0;
  return 0.7 * cos + 0.3 * lexical;
}

function search(input = {}) {
  const query = String(input.query || "").trim();
  if (!query) return { status: "BLOCKED", reason: "QUERY_REQUIRED" };
  if (!store.chunks.length) return { status: "BLOCKED", reason: "EMPTY_CORPUS_INGEST_FIRST" };
  const topK = Math.max(1, Math.min(Number(input.top_k || DEFAULT_TOP_K), 20));
  const documentId = String(input.document_id || "").trim();
  const queryTokens = tokenize(query);
  const queryVec = termVector(queryTokens);
  const pool = documentId ? store.chunks.filter((c) => c.document_id === documentId) : store.chunks;
  if (!pool.length) return { status: "BLOCKED", reason: "DOCUMENT_ID_NOT_FOUND", document_id: documentId };
  const ranked = pool
    .map((chunk) => ({ chunk, score: scoreChunk(queryTokens, queryVec, chunk) }))
    .sort((a, b) => b.score - a.score)
    .slice(0, topK)
    .map(({ chunk, score }, i) => ({
      rank: i + 1,
      document_id: chunk.document_id,
      chunk_id: chunk.chunk_id,
      score: Number(score.toFixed(4)),
      start: chunk.start,
      end: chunk.end,
      excerpt: chunk.text.slice(0, EXCERPT_CHARS)
    }));
  return { status: "RESULTS", query, top_k: topK, results: ranked, top_score: ranked[0]?.score ?? 0 };
}

function chat(input = {}) {
  const question = String(input.question || "").trim();
  if (!question) return { status: "BLOCKED", reason: "QUESTION_REQUIRED" };
  const found = search({ query: question, top_k: Number(input.top_k || DEFAULT_TOP_K) });
  if (found.status !== "RESULTS") return found;
  if (!found.results.length || found.top_score < REFUSAL_THRESHOLD) {
    return {
      status: "REFUSED",
      reason: "WEAK_GROUNDING",
      question,
      top_score: found.top_score,
      guidance: "Do not hallucinate. Improve chunking, add metadata filters, ingest the supporting lesson/document, or rerank before answering."
    };
  }
  const citations = found.results.map((r, i) => ({
    ref: `[${i + 1}]`,
    document_id: r.document_id,
    chunk_id: r.chunk_id,
    score: r.score,
    excerpt: r.excerpt
  }));
  const answer = found.results.map((r, i) => `[${i + 1}] (${r.chunk_id}) ${r.excerpt}`).join("\n\n---\n\n");
  return {
    status: "GROUNDED",
    question,
    top_score: found.top_score,
    answer,
    citations,
    note: "Extractive context packing only. Full LLM generation and SSE streaming happen in the Express app via rag_node.express_plan."
  };
}

function expressPlan() {
  return {
    status: "PLAN",
    runtime: "node>=18",
    routes: [
      { method: "POST", path: "/api/ingest", body: "{ documents: [{id, text, metadata?}], chunk_size?, overlap? }", via: "rag_node.ingest" },
      { method: "GET", path: "/api/search?q=...&top_k=5&document_id=...", via: "rag_node.search" },
      { method: "POST", path: "/api/chat", body: "{ question, top_k? }", via: "rag_node.chat" },
      { method: "POST", path: "/api/chat/stream", body: "{ question, top_k? }", response: "text/event-stream", via: "rag_node.chat plus SSE framing" }
    ],
    sse_framing: [
      'res.setHeader("Content-Type", "text/event-stream")',
      'res.setHeader("Cache-Control", "no-cache")',
      'res.setHeader("Connection", "keep-alive")',
      'res.write(`data: ${JSON.stringify({ delta })}\\n\\n`) per token or citation block',
      'res.write("data: [DONE]\\n\\n") then res.end()'
    ],
    chunk_defaults: { chunk_size: DEFAULT_CHUNK_SIZE, overlap: DEFAULT_OVERLAP },
    refusal_policy: { threshold: REFUSAL_THRESHOLD, on_weak_support: "HTTP 409 plus WEAK_GROUNDING guidance, never hallucinated prose" },
    evidence: { curriculum: CURRICULUM.source, scope: CURRICULUM.scope }
  };
}

function call(name, input = {}) {
  if (name === "rag_node.health") return health();
  if (name === "rag_node.curriculum") return curriculum();
  if (name === "rag_node.ingest") return ingest(input);
  if (name === "rag_node.search") return search(input);
  if (name === "rag_node.chat") return chat(input);
  if (name === "rag_node.express_plan") return expressPlan();
  return { status: "ERROR", reason: "UNKNOWN_TOOL", tool: name };
}

function resultContent(value) {
  return [{ type: "text", text: JSON.stringify(value, null, 2) }];
}

function listToolsResponse() {
  return listTools().map((t) => ({ name: t.name, description: t.description, inputSchema: t.inputSchema }));
}

function handle(message) {
  if (Array.isArray(message)) return message.map(handle).filter(Boolean);
  const { id, method, params = {} } = message || {};
  if (method === "initialize") {
    return {
      jsonrpc: "2.0",
      id,
      result: {
        protocolVersion: params.protocolVersion || "2024-11-05",
        capabilities: { tools: { listChanged: false } },
        serverInfo: { name: "aeos-rag-node", version: VERSION },
        instructions: "Offline governed RAG Node.js MCP mirroring the TLC public curriculum."
      }
    };
  }
  if (method === "notifications/initialized") return null;
  if (method === "tools/list") return { jsonrpc: "2.0", id, result: { tools: listToolsResponse() } };
  if (method === "tools/call") {
    return { jsonrpc: "2.0", id, result: { content: resultContent(call(params.name, params.arguments || {})), isError: false } };
  }
  if (method === "ping") return { jsonrpc: "2.0", id, result: {} };
  if (id == null) return null;
  return { jsonrpc: "2.0", id, error: { code: -32601, message: `Unknown method: ${method}` } };
}

function send(message) {
  if (!message) return;
  const payload = JSON.stringify(message);
  process.stdout.write(`Content-Length: ${Buffer.byteLength(payload, "utf8")}\r\n\r\n${payload}`);
}

let buffer = Buffer.alloc(0);
process.stdin.on("data", (chunk) => {
  buffer = Buffer.concat([buffer, chunk]);
  parse();
});

function parse() {
  while (buffer.length) {
    let headerEnd = buffer.indexOf("\r\n\r\n");
    let sep = 4;
    if (headerEnd < 0) {
      headerEnd = buffer.indexOf("\n\n");
      sep = 2;
    }
    if (headerEnd >= 0) {
      const header = buffer.slice(0, headerEnd).toString("utf8");
      const match = /Content-Length:\s*(\d+)/i.exec(header);
      if (!match) {
        buffer = buffer.slice(headerEnd + sep);
        continue;
      }
      const length = Number(match[1]);
      const start = headerEnd + sep;
      if (buffer.length < start + length) return;
      const body = buffer.slice(start, start + length).toString("utf8");
      buffer = buffer.slice(start + length);
      dispatch(body);
      continue;
    }
    const newline = buffer.indexOf("\n");
    if (newline < 0) return;
    const line = buffer.slice(0, newline).toString("utf8").trim();
    buffer = buffer.slice(newline + 1);
    if (line) dispatch(line);
  }
}

function dispatch(raw) {
  try {
    send(handle(JSON.parse(raw)));
  } catch {
    send({ jsonrpc: "2.0", id: null, error: { code: -32700, message: "Invalid JSON" } });
  }
}
