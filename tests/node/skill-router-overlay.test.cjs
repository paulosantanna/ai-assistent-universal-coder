const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { pathToFileURL } = require("node:url");

const repoRoot = path.resolve(__dirname, "../..");
function moduleUrl(relativePath) {
  return pathToFileURL(path.join(repoRoot, relativePath)).href;
}

describe("AEOS active overlay skill routing", () => {
  it("loads github-operations and devops-pipeline-engineering from active fragments", async () => {
    const { loadActiveSkills } = await import(moduleUrl("scripts/aeos-skill-router.mjs"));
    const skills = loadActiveSkills();
    const byId = new Map(skills.map((skill) => [skill.id, skill]));

    assert.equal(byId.has("github-operations"), true);
    assert.equal(byId.has("devops-pipeline-engineering"), true);
    assert.equal(byId.get("github-operations").ownerAgent, "codenavi-agent");
    assert.equal(byId.get("devops-pipeline-engineering").ownerAgent, "codenavi-agent");
    assert.equal(byId.get("github-operations").registryFragment, "skills.github-operations.additions.yaml");
    assert.equal(byId.get("devops-pipeline-engineering").registryFragment, "skills.devops-pipeline-engineering.additions.yaml");
    assert.equal(byId.has("spec-driven"), true);
    assert.equal(byId.has("spec-driven-lean"), true);
    assert.equal(byId.get("spec-driven").ownerAgent, "codenavi-agent");
    assert.equal(byId.get("spec-driven-lean").ownerAgent, "codenavi-agent");
    assert.equal(byId.get("spec-driven").registryFragment, "skills.spec-driven.additions.yaml");
    assert.equal(byId.get("spec-driven-lean").registryFragment, "skills.spec-driven.additions.yaml");
    for (const id of [
      "not-your-babysitter",
      "cursor-subagent-creator",
      "skill-architect",
      "technical-design-doc-creator",
      "best-practices",
      "the-fool",
      "the-jury",
      "ai-seo",
      "nx-workspace",
      "subagent-creator",
      "tlc-plan",
      "learning-opportunities",
      "perf-astro",
      "core-web-vitals",
      "perf-lighthouse",
      "perf-web-optimization",
      "security-best-practices",
      "security-ownership-map",
      "security-threat-model",
      "web-quality-audit"
    ]) {
      assert.equal(byId.has(id), true, id);
      assert.equal(byId.get(id).ownerAgent, "codenavi-agent", id);
      assert.equal(byId.get(id).registryFragment, "skills.tlc-catalog.additions.yaml", id);
    }
  });

  it("routes GitHub Actions recovery intent to the DevOps skill", async () => {
    const { routeRequest } = await import(moduleUrl("scripts/aeos-skill-router.mjs"));
    const sandbox = fs.mkdtempSync(path.join(os.tmpdir(), "aeos-devops-route-"));
    try {
      const result = routeRequest(
        "monitore todas as github actions, corrija a esteira recursivamente e prepare o merge",
        { memoryRoot: path.join(sandbox, "memory"), outputDir: path.join(sandbox, "router"), limit: 8 }
      );
      const ids = result.selectedSkills.map((skill) => skill.id);
      assert.equal(ids.includes("devops-pipeline-engineering"), true);
      assert.equal(result.gates.overlayRegistryResolved, true);
    } finally {
      fs.rmSync(sandbox, { recursive: true, force: true });
    }
  });

  it("routes spec-driven feature intent to assimilated TLC skills", async () => {
    const { routeRequest } = await import(moduleUrl("scripts/aeos-skill-router.mjs"));
    const sandbox = fs.mkdtempSync(path.join(os.tmpdir(), "aeos-spec-route-"));
    try {
      const full = routeRequest(
        "use spec-driven to specify this feature with EARS acceptance criteria",
        { memoryRoot: path.join(sandbox, "memory-full"), outputDir: path.join(sandbox, "router-full"), limit: 8 }
      );
      const lean = routeRequest(
        "use spec-driven-lean and write the checks for this plan",
        { memoryRoot: path.join(sandbox, "memory-lean"), outputDir: path.join(sandbox, "router-lean"), limit: 8 }
      );
      assert.equal(full.selectedSkills.map((skill) => skill.id).includes("spec-driven"), true);
      assert.equal(lean.selectedSkills.map((skill) => skill.id).includes("spec-driven-lean"), true);
    } finally {
      fs.rmSync(sandbox, { recursive: true, force: true });
    }
  });
});
