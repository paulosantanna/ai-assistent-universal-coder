#!/usr/bin/env node
import { readFileSync } from "node:fs";

const args = process.argv.slice(2);
const mode = valueAfter("--mode") || "generic";
const profile = valueAfter("--profile") || mode;

function valueAfter(flag) {
  const index = args.indexOf(flag);
  return index >= 0 ? args[index + 1] : "";
}

function tool(name, description, inputSchema = {}) {
  return {
    name,
    description,
    inputSchema: {
      type: "object",
      properties: inputSchema,
      additionalProperties: true
    }
  };
}

function toolsForMode() {
  if (mode === "language-docs") {
    return [
      tool("language_docs.search", "Search governed language documentation for the active profile.", { query: { type: "string" }, max_results: { type: "integer" } }),
      tool("language_docs.fetch", "Return a governed fetch plan for an allowed documentation URL.", { url: { type: "string" }, max_bytes: { type: "integer" } }),
      tool("language_docs.lookup_symbol", "Look up an API, symbol, module, package, flag or framework concept.", { symbol: { type: "string" }, scope: { type: "string" } }),
      tool("language_docs.version_status", "Return release, support and documentation status for the active profile."),
      tool("language_docs.migration_delta", "Compare source and target versions using governed docs and release notes.", { source_version: { type: "string" }, target_version: { type: "string" }, topic: { type: "string" } }),
      tool("language_docs.source_policy", "Return source authority, freshness and citation policy.")
    ];
  }
  if (mode === "complete-docs") {
    return [
      tool("docs.plan", "Create an evidence-first documentation plan.", { scope: { type: "string" }, audience: { type: "string" }, depth: { type: "string" } }),
      tool("docs.mermaid_template", "Return a safe Mermaid template.", { diagram_type: { type: "string" }, title: { type: "string" } }),
      tool("docs.validate_mermaid", "Validate Mermaid source for size and sensitive terms.", { source: { type: "string" } }),
      tool("docs.package", "Create a documentation package plan.", { scope: { type: "string" }, audience: { type: "string" }, include_diagrams: { type: "boolean" } }),
      tool("docs.architecture_package", "Create an architecture documentation package plan.", { scope: { type: "string" }, audience: { type: "string" }, maturity_target: { type: "string" } })
    ];
  }
  if (mode === "universal-project") {
    return [
      tool("project.plan", "Create a zero-to-production project plan.", { objective: { type: "string" }, architecture: { type: "string" } }),
      tool("project.stack_matrix", "Return required runtime, language and database decisions.", { languages: { type: "array" }, databases: { type: "array" } }),
      tool("project.production_checklist", "Return production gates.", { architecture: { type: "string" }, deployment_target: { type: "string" } }),
      tool("project.scaffold_manifest", "Return a sandbox-only scaffold manifest.", { project_name: { type: "string" }, architecture: { type: "string" } }),
      tool("project.scaffold_package", "Return a sandbox-first scaffold package plan.", { project_name: { type: "string" }, objective: { type: "string" } })
    ];
  }
  if (mode === "continuous-training") {
    return [
      tool("web_search", "Return a governed web-search plan for continuous training research.", { query: { type: "string" }, max_results: { type: "integer" } }),
      tool("arxiv_search", "Return an arXiv-search plan.", { query: { type: "string" }, max_results: { type: "integer" } }),
      tool("paperswithcode_search", "Return a Papers with Code search plan.", { query: { type: "string" }, max_results: { type: "integer" } }),
      tool("github_search", "Return a GitHub search plan.", { query: { type: "string" }, max_results: { type: "integer" } }),
      tool("reddit_search", "Return a Reddit search plan.", { query: { type: "string" }, max_results: { type: "integer" } }),
      tool("web_fetch", "Return a governed fetch plan.", { url: { type: "string" }, timeout: { type: "integer" } }),
      tool("curated_sources", "Return curated source policy.", { filters: { type: "object" } })
    ];
  }
  if (mode === "medical-research") {
    return [
      tool("qualified_medical_sources", "Return governed medical source categories."),
      tool("diabetes_staff_expertise_map", "Return diabetes AI research expertise map."),
      tool("diabetes_ai_project_review_gate", "Return diabetes AI project review checklist."),
      tool("build_disease_research_query", "Build a reproducible disease research query.", { profile: { type: "object" }, methods: { type: "array" } }),
      tool("build_research_method_queries", "Build method discovery queries.", { profile: { type: "object" } }),
      tool("medical_evidence_screening_policy", "Return evidence screening policy."),
      tool("repository_scan", "Return a repository scan plan.")
    ];
  }
  return [tool("aeos.ping", "Return MCP server health.")];
}

function callTool(name, input = {}) {
  if (name === "docs.validate_mermaid") {
    const source = String(input.source || "");
    const hasSecret = /(password|secret|token|credential|private[_-]?key)\s*[=:]/i.test(source);
    return { valid: !hasSecret && source.length <= 12000, has_secret_like_text: hasSecret, length: source.length };
  }
  if (name === "docs.mermaid_template") {
    const diagramType = String(input.diagram_type || "flowchart");
    const title = String(input.title || "AEOS View");
    return { diagram_type: diagramType, title, source: `${diagramType} TD\n  A[${title}] --> B[Evidence]\n  B --> C[Decision]` };
  }
  if (name === "language_docs.version_status") {
    return { profile, status: "configured", evidence_required: true };
  }
  if (name === "language_docs.source_policy") {
    return { profile, authority: "official-or-governed", freshness_required: true, redact_outputs: true };
  }
  return {
    mode,
    profile,
    tool: name,
    status: "PLAN",
    input,
    note: "Read-only local AEOS MCP fallback. Use official sources/evidence before making material claims."
  };
}

function resultContent(value) {
  return [{ type: "text", text: JSON.stringify(value, null, 2) }];
}

function handle(message) {
  if (Array.isArray(message)) {
    const responses = message.map(handle).filter(Boolean);
    return responses.length ? responses : null;
  }
  const { id, method, params = {} } = message;
  if (method === "initialize") {
    return {
      jsonrpc: "2.0",
      id,
      result: {
        protocolVersion: params.protocolVersion || "2024-11-05",
        capabilities: {
          tools: { listChanged: false },
          prompts: { listChanged: false },
          resources: { subscribe: false, listChanged: false }
        },
        serverInfo: { name: `aeos-readonly-${mode}`, version: "1.0.1" },
        instructions: "Read-only AEOS fallback MCP. No credential access, no mutation, no network side effects."
      }
    };
  }
  if (method === "notifications/initialized") return null;
  if (method === "tools/list") return { jsonrpc: "2.0", id, result: { tools: toolsForMode() } };
  if (method === "tools/call") {
    return { jsonrpc: "2.0", id, result: { content: resultContent(callTool(params.name, params.arguments || {})), isError: false } };
  }
  if (method === "prompts/list") return { jsonrpc: "2.0", id, result: { prompts: [] } };
  if (method === "resources/list") return { jsonrpc: "2.0", id, result: { resources: [] } };
  if (method === "ping") return { jsonrpc: "2.0", id, result: {} };
  if (id === undefined || id === null) return null;
  return { jsonrpc: "2.0", id, error: { code: -32601, message: `Unknown method: ${method}` } };
}

function send(message) {
  if (!message) return;
  const payload = JSON.stringify(message);
  process.stdout.write(`Content-Length: ${Buffer.byteLength(payload, "utf8")}\r\n\r\n${payload}`);
}

let buffer = Buffer.alloc(0);
process.stdin.on("data", chunk => {
  buffer = Buffer.concat([buffer, chunk]);
  parseBuffer();
});

function parseBuffer() {
  while (buffer.length) {
    let headerEnd = buffer.indexOf("\r\n\r\n");
    let separatorLength = 4;
    if (headerEnd < 0) {
      headerEnd = buffer.indexOf("\n\n");
      separatorLength = 2;
    }
    if (headerEnd >= 0) {
      const header = buffer.slice(0, headerEnd).toString("utf8");
      const match = /Content-Length:\s*(\d+)/i.exec(header);
      if (!match) {
        buffer = buffer.slice(headerEnd + separatorLength);
        continue;
      }
      const length = Number(match[1]);
      const start = headerEnd + separatorLength;
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
  } catch (error) {
    send({ jsonrpc: "2.0", id: null, error: { code: -32700, message: "Invalid JSON" } });
  }
}

process.on("uncaughtException", error => {
  process.stderr.write(`aeos-readonly-mcp error: ${error.message}\n`);
});
