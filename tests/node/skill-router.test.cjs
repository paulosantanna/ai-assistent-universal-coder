const assert = require("node:assert/strict");
const { execFileSync } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");

describe("AEOS skill-first routing", () => {
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
