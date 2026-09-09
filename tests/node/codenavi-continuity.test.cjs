const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const yaml = require("js-yaml");

const root = path.resolve(__dirname, "../..");
const read = (p) => fs.readFileSync(path.join(root, p), "utf8");

describe("CodENavi continuity governance", () => {
  it("keeps AGENT and AGENTS identical and continuity-aware", () => {
    const agent = read("AGENT.md");
    assert.equal(agent, read("AGENTS.md"));
    for (const token of ["HANDOFF.md", "MEMORY.md", "PROGRESS.md", "LEARNING.md", "CODENAVI_CONTINUITY_STANDARD.md"]) {
      assert.ok(agent.includes(token), `missing ${token}`);
    }
  });

  it("ships the four continuity templates and active notebook artifacts", () => {
    for (const name of ["HANDOFF", "MEMORY", "PROGRESS", "LEARNING"]) {
      assert.ok(fs.existsSync(path.join(root, `templates/codenavi-continuity/${name}.md`)));
      assert.ok(fs.existsSync(path.join(root, `.notebook/${name}.md`)));
    }
  });

  it("registers the five continuity skills under codenavi-agent", () => {
    const registry = yaml.load(read("aeos/registries/skills.codenavi-continuity.additions.yaml"));
    const expected = new Set(["continuity-bootstrapper", "handoff-manager", "memory-curator", "progress-tracker", "learning-curator"]);
    for (const entry of registry.skills) {
      assert.equal(entry.owner_agent, "codenavi-agent");
      expected.delete(entry.id);
      assert.ok(fs.existsSync(path.join(root, entry.path)), entry.path);
    }
    assert.equal(expected.size, 0, `missing: ${[...expected].join(", ")}`);
  });

  it("indexes continuity artifacts before project notes", () => {
    const index = read(".notebook/INDEX.md");
    const positions = ["HANDOFF.md", "MEMORY.md", "PROGRESS.md", "LEARNING.md"].map((name) => index.indexOf(`(${name})`));
    positions.forEach((position) => assert.ok(position >= 0));
    assert.ok(positions.every((value, i) => i === 0 || value > positions[i - 1]));
  });
});
