const assert = require("node:assert/strict");
const { execFileSync } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");

describe("AEOS skill-first routing", () => {
  it("requires all MCP and LSP adapters to declare governing skills", () => {
    const output = execFileSync(
      "node",
      ["scripts/aeos-skill-adapter-guard.mjs"],
      { cwd: path.resolve(__dirname, "../.."), encoding: "utf8" }
    );
    const result = JSON.parse(output);

    assert.equal(result.status, "PASS");
    assert.equal(result.mcpsChecked > 0, true);
    assert.equal(result.lspProfilesChecked > 0, true);
    assert.equal(result.governingSkills.includes("tool-adapter-governor"), true);
  });

  it("blocks direct MCP calls without an active skill context", () => {
    const script = `
      import { ToolRouter } from "./runtime/dist/kernel/tool-router.js";
      import { EvidenceStore } from "./runtime/dist/kernel/evidence-store.js";
      const router = new ToolRouter(new EvidenceStore(".aeos/test-evidence/direct-mcp-block"));
      router.registerMCP({
        id: "filesystem-readonly",
        type: "filesystem",
        config: "aeos/mcps/filesystem-readonly.mcp.yaml",
        risk_level: "low",
        capabilities: ["file_exists"],
        governing_skill: "repo-scanner",
        skill_enforced: true
      });
      const blocked = await router.callTool("filesystem-readonly", "file_exists", { path: "package.json" });
      router.setActiveSkill("repo-scanner");
      const allowed = await router.callTool("filesystem-readonly", "file_exists", { path: "package.json" });
      console.log(JSON.stringify({ blocked, allowed }));
    `;
    const output = execFileSync(
      "node",
      ["--input-type=module", "--eval", script],
      { cwd: path.resolve(__dirname, "../.."), encoding: "utf8" }
    );
    const result = JSON.parse(output);

    assert.equal(result.blocked.success, false);
    assert.match(result.blocked.error, /skill context/);
    assert.equal(result.allowed.success, true);
  });

  it("routes explicit Java bug requests to Java before JavaScript", () => {
    const output = execFileSync(
      "node",
      ["scripts/aeos-skill-router.mjs", "corrigir bug Java com testes e sem alterar arquitetura"],
      { cwd: path.resolve(__dirname, "../.."), encoding: "utf8" }
    );
    const result = JSON.parse(output);
    const ids = result.selectedSkills.map((skill) => skill.id);

    assert.equal(ids[0], "java-docs-bug-solver");
    assert.equal(ids.includes("javascript-bug-solver"), false);
    assert.equal(result.gates.chromaticMemoryPersisted, true);
  });

  it("persists mandatory Chromatic memory files", () => {
    const output = execFileSync(
      "node",
      ["scripts/aeos-chromatic-memory.mjs", "node test memory persistence"],
      { cwd: path.resolve(__dirname, "../.."), encoding: "utf8" }
    );
    const result = JSON.parse(output);

    for (const file of ["MEMORY.md", "LEARNING.md", "HANDOFF.md", "PROGRESS.md"]) {
      const fullPath = path.join(result.memoryRoot, file);
      assert.equal(fs.existsSync(fullPath), true);
      assert.match(fs.readFileSync(fullPath, "utf8"), /node test memory persistence/);
    }
  });
});
