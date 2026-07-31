const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { pathToFileURL } = require("node:url");

const repoRoot = path.resolve(__dirname, "../..");

function moduleUrl(relativePath) {
  return pathToFileURL(path.join(repoRoot, relativePath)).href;
}

describe("AEOS skill-first routing", () => {
  it("requires all MCP and LSP adapters to declare governing skills", async () => {
    const { validateSkillAdapters } = await import(moduleUrl("scripts/aeos-skill-adapter-guard.mjs"));
    const result = validateSkillAdapters();

    assert.equal(result.status, "PASS");
    assert.equal(result.mcpsChecked > 0, true);
    assert.equal(result.lspProfilesChecked > 0, true);
    assert.equal(result.governingSkills.includes("tool-adapter-governor"), true);
  });

  it("blocks direct MCP calls without an active skill context", async () => {
    const { ToolRouter } = await import(moduleUrl("runtime/dist/kernel/tool-router.js"));
    const { EvidenceStore } = await import(moduleUrl("runtime/dist/kernel/evidence-store.js"));

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

    assert.equal(blocked.success, false);
    assert.match(blocked.error, /skill context/);
    assert.equal(allowed.success, true);
  });

  it("routes explicit Java bug requests to Java before JavaScript", async () => {
    const { routeRequest } = await import(moduleUrl("scripts/aeos-skill-router.mjs"));
    const result = routeRequest("corrigir bug Java com testes e sem alterar arquitetura");
    const ids = result.selectedSkills.map((skill) => skill.id);

    assert.equal(ids[0], "chromatic-mega-brain");
    assert.equal(ids.find((id) => id !== "chromatic-mega-brain"), "java-docs-bug-solver");
    assert.equal(ids.includes("javascript-bug-solver"), false);
    assert.equal(result.gates.chromaticMemoryPersisted, true);
  });

  it("persists mandatory Chromatic memory files", async () => {
    const { persistChromaticMemory } = await import(moduleUrl("scripts/aeos-chromatic-memory.mjs"));
    const result = persistChromaticMemory({
      request: "node test memory persistence",
      selectedSkills: ["chromatic-mega-brain"]
    });

    for (const file of ["MEMORY.md", "LEARNING.md", "HANDOFF.md", "PROGRESS.md"]) {
      const fullPath = path.join(result.memoryRoot, file);
      assert.equal(fs.existsSync(fullPath), true);
      assert.match(fs.readFileSync(fullPath, "utf8"), /node test memory persistence/);
    }
  });
});


