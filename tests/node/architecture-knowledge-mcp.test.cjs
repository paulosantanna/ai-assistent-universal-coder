const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { spawn } = require("node:child_process");
const yaml = require("js-yaml");

const repoRoot = path.resolve(__dirname, "../..");
const SERVER = path.join(repoRoot, "aeos/mcp-servers/architecture-knowledge-mcp.mjs");

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
    const match = /Content-Length:\s*(\d+)/i.exec(rest.slice(0, headerEnd).toString("utf8"));
    if (!match) break;
    const start = headerEnd + 4;
    const length = Number(match[1]);
    if (rest.length < start + length) break;
    responses.push(JSON.parse(rest.slice(start, start + length).toString("utf8")));
    rest = rest.slice(start + length);
  }
  return responses;
}

function session(messages, { lines = false } = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [SERVER], { cwd: repoRoot, stdio: ["pipe", "pipe", "pipe"] });
    const expected = messages.filter((message) => message.id !== undefined).length;
    let stdout = Buffer.alloc(0);
    let stderr = "";
    const parse = () => {
      if (!lines) return parseFrames(stdout);
      const complete = stdout.toString("utf8").split("\n");
      complete.pop();
      return complete.filter(Boolean).map((line) => JSON.parse(line));
    };
    const timer = setTimeout(() => {
      child.kill();
      reject(new Error(`architecture-knowledge timed out. stderr=${stderr}`));
    }, 5000);
    child.stdout.on("data", (chunk) => {
      stdout = Buffer.concat([stdout, chunk]);
      const responses = parse();
      if (responses.length >= expected) {
        clearTimeout(timer);
        child.kill();
        resolve(responses);
      }
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString("utf8");
    });
    child.on("error", reject);
    for (const message of messages) child.stdin.write(lines ? `${JSON.stringify(message)}\n` : framed(message));
  });
}

function call(id, name, args = {}) {
  return { jsonrpc: "2.0", id, method: "tools/call", params: { name, arguments: args } };
}

function json(response, block = 0) {
  return JSON.parse(response.result.content[block].text);
}

function byId(responses, id) {
  return responses.find((response) => response.id === id);
}

describe("Architecture Knowledge MCP", () => {
  it("lists ten tools over Content-Length frames and over newline-delimited JSON", async () => {
    const init = { jsonrpc: "2.0", id: 1, method: "initialize", params: { protocolVersion: "2025-06-18" } };
    const list = { jsonrpc: "2.0", id: 2, method: "tools/list", params: {} };
    for (const lines of [false, true]) {
      const responses = await session([init, { jsonrpc: "2.0", method: "notifications/initialized" }, list], { lines });
      assert.equal(byId(responses, 1).result.protocolVersion, "2025-06-18");
      const tools = byId(responses, 2).result.tools.map((tool) => tool.name);
      assert.equal(tools.length, 10);
      for (const name of ["search_skills", "read_skill", "fetch_skill_files", "list_skills", "adr_lint", "adl_index", "asr_test"]) {
        assert.ok(tools.includes(`architecture_knowledge.${name}`), name);
      }
    }
  });

  it("ranks skills by intent in English and Portuguese and drops weak matches", async () => {
    const responses = await session([
      call(1, "architecture_knowledge.search_skills", { query: "write an ADR for choosing PostgreSQL" }),
      call(2, "architecture_knowledge.search_skills", { query: "requisito arquiteturalmente significativo" }),
      call(3, "architecture_knowledge.search_skills", { query: "próximo número de ADR" }),
      call(4, "architecture_knowledge.search_skills", { query: "gestão do conhecimento arquitetural" }),
      call(5, "architecture_knowledge.search_skills", { query: "bake a chocolate cake" }),
      call(6, "architecture_knowledge.search_skills", { query: " " })
    ]);
    assert.equal(json(byId(responses, 1)).results[0].name, "architecture-decision-record");
    assert.equal(json(byId(responses, 2)).results[0].name, "architecturally-significant-requirement");
    assert.equal(json(byId(responses, 3)).results[0].name, "architecture-decision-log");
    assert.equal(json(byId(responses, 4)).results[0].name, "architecture-knowledge-management");
    for (const result of json(byId(responses, 1)).results) assert.ok(result.score >= 20);
    assert.equal(json(byId(responses, 5)).status, "NO_MATCH");
    assert.equal(byId(responses, 6).result.isError, true);
  });

  it("reads a skill without frontmatter and fetches only declared files within budget", async () => {
    const responses = await session([
      call(1, "architecture_knowledge.read_skill", { skill_name: "architecture-decision-record" }),
      call(2, "architecture_knowledge.fetch_skill_files", { skill_name: "architecture-decision-record", file_paths: ["references/adr-practices.md", "assets/madr-template.md"] }),
      call(3, "architecture_knowledge.fetch_skill_files", { skill_name: "architecture-decision-record", file_paths: ["../../AGENTS.md"] }),
      call(4, "architecture_knowledge.fetch_skill_files", { skill_name: "architecture-decision-record", file_paths: ["a", "b", "c", "d", "e", "f"] }),
      call(5, "architecture_knowledge.read_skill", { skill_name: "create-adr" }),
      call(6, "architecture_knowledge.list_skills", {}),
      call(7, "architecture_knowledge.list_skills", { explicit_request: true })
    ]);
    const read = byId(responses, 1).result.content;
    assert.equal(read.length, 2);
    assert.doesNotMatch(read[0].text, /^---/);
    assert.match(read[0].text, /^# Architecture Decision Record/);
    const meta = JSON.parse(read[1].text);
    assert.equal(meta.skill_dir, "skills/architecture-decision-record");
    assert.ok(meta.files.includes("scripts/adr_lint.mjs"));
    const fetched = byId(responses, 2).result.content;
    assert.match(fetched[0].text, /--- references\/adr-practices\.md ---/);
    assert.match(fetched[0].text, /--- assets\/madr-template\.md ---/);
    assert.ok(fetched[0].text.length <= 50000);
    assert.deepEqual(JSON.parse(fetched[1].text).fetched, ["references/adr-practices.md", "assets/madr-template.md"]);
    assert.equal(byId(responses, 3).result.isError, true);
    assert.equal(json(byId(responses, 3)).reason, "INVALID_FILE_PATHS");
    assert.equal(json(byId(responses, 4)).reason, "TOO_MANY_FILES");
    assert.equal(json(byId(responses, 5)).reason, "SKILL_NOT_FOUND");
    assert.equal(json(byId(responses, 6)).reason, "EXPLICIT_REQUEST_REQUIRED");
    assert.equal(json(byId(responses, 7)).total_skills, 4);
  });

  it("runs the skills' deterministic checks and confines paths to the workspace", async () => {
    const responses = await session([
      call(1, "architecture_knowledge.adr_lint", { path: "aeos/docs/adr/ADR-0001-WORKSPACE-OS-STRANGLER.md" }),
      call(2, "architecture_knowledge.adr_lint", { path: "../../etc/passwd" }),
      call(3, "architecture_knowledge.adl_index", { directory: "aeos/docs/adr", today: "2026-10-07", next_title: "Architecture knowledge MCP" }),
      call(4, "architecture_knowledge.adl_index", { directory: "/" }),
      call(5, "architecture_knowledge.asr_test", { requirement: "Retain customer data for 10 years", criteria: { C1: "Y", C2: "Y", C4: "Y", C5: "Y" } }),
      call(6, "architecture_knowledge.adr_lint", { content: "x", path: "y" })
    ]);
    const lint = json(byId(responses, 1));
    assert.equal(lint.format, "aeos-template");
    assert.equal(lint.source, "aeos/docs/adr/ADR-0001-WORKSPACE-OS-STRANGLER.md");
    assert.ok(["PATH_OUTSIDE_WORKSPACE", "PATH_NOT_FOUND"].includes(json(byId(responses, 2)).reason));
    const log = json(byId(responses, 3));
    assert.equal(log.directory, "aeos/docs/adr");
    assert.equal(log.next.file, "ADR-0002-ARCHITECTURE-KNOWLEDGE-MCP.md");
    assert.equal(json(byId(responses, 4)).reason, "PATH_OUTSIDE_WORKSPACE");
    assert.equal(json(byId(responses, 5)).band, "high");
    assert.equal(json(byId(responses, 6)).reason, "CONTENT_OR_PATH_REQUIRED");
  });

  it("serves AKM vocabulary, dated sources and the TLC baseline deltas", async () => {
    const responses = await session([
      call(1, "architecture_knowledge.concepts", { term: "ADR" }),
      call(2, "architecture_knowledge.concepts", { term: "requisito arquiteturalmente significativo" }),
      call(3, "architecture_knowledge.sources", {}),
      call(4, "architecture_knowledge.health", {})
    ]);
    assert.deepEqual(json(byId(responses, 1)).definitions.map((item) => item.term), ["ADR"]);
    assert.equal(json(byId(responses, 2)).definitions[0].term, "ASR");
    const sources = json(byId(responses, 3));
    assert.equal(sources.templates.find((item) => item.id === "madr").version, "4.0.0");
    assert.equal(sources.tlc_baseline.skill, "create-adr");
    assert.ok(sources.tlc_baseline.deltas_to_current_guidance.length >= 5);
    assert.ok(sources.sources.every((source) => source.checked));
    const health = json(byId(responses, 4));
    assert.equal(health.network_access, false);
    assert.equal(health.write_access, false);
    assert.equal(health.skills.length, 4);
  });

  it("is registered as a read-only adapter governed by architecture-knowledge-management", () => {
    const fragment = yaml.load(fs.readFileSync(path.join(repoRoot, "aeos/registries/mcps.architecture-knowledge.additions.yaml"), "utf8"));
    const entry = fragment.mcps[0];
    assert.equal(entry.id, "architecture-knowledge");
    assert.equal(entry.governing_skill, "architecture-knowledge-management");
    assert.equal(entry.skill_enforced, true);
    assert.equal(entry.write_allowed, false);
    const definition = yaml.load(fs.readFileSync(path.join(repoRoot, entry.config), "utf8"));
    assert.equal(definition.mcp.security.network_access, false);
    assert.equal(definition.mcp.security.workspace_only, true);
    assert.ok(definition.mcp.capabilities.tools.every((tool) => tool.security === "read-only"));
    assert.deepEqual(definition.mcp.capabilities.tools.map((tool) => tool.name).sort(), [...entry.tools].sort());
  });
});
