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
});
