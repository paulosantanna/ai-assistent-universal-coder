const assert = require("node:assert/strict");
const { spawnSync } = require("node:child_process");
const path = require("node:path");
const { pathToFileURL } = require("node:url");

const repoRoot = path.resolve(__dirname, "../..");

function moduleUrl(relativePath) {
  return pathToFileURL(path.join(repoRoot, relativePath)).href;
}

describe("AEOS critical-thinking governance", () => {
  it("governs every registered skill with exactly 20 registered specialists", async () => {
    const { validateCriticalThinkingGovernance } = await import(
      moduleUrl("scripts/aeos-critical-thinking-guard.mjs")
    );
    const result = validateCriticalThinkingGovernance(repoRoot);

    assert.deepEqual(result.errors, []);
    assert.equal(result.status, "PASS");
    assert.equal(result.specialistAgentsChecked, 20);
    assert.equal(result.skillsChecked >= 100, true);
    assert.equal(result.baselineAgents.length, 4);
    assert.equal(result.maxAgentsPerPlan < 20, true);
  });

  it("uses only the four-agent baseline for a simple low-risk task", async () => {
    const { buildCriticalThinkingPlan } = await import(
      moduleUrl("scripts/aeos-critical-thinking-governance.mjs")
    );
    const plan = buildCriticalThinkingPlan({
      skillId: "simple-skill",
      riskLevel: "low",
      request: "executar uma tarefa simples e determinística"
    });

    assert.equal(plan.status, "PASS");
    assert.deepEqual(
      plan.selectedAgents.map((agent) => agent.id),
      ["ct-first-principles", "ct-assumption-auditor", "ct-evidence-hierarchy", "ct-meta-reflection"]
    );
  });

  it("adds critical-risk and explicit Bayesian agents without activating all agents", async () => {
    const { buildCriticalThinkingPlan } = await import(
      moduleUrl("scripts/aeos-critical-thinking-governance.mjs")
    );
    const plan = buildCriticalThinkingPlan({
      skillId: "clinical-release",
      riskLevel: "critical",
      request: "estime com Bayes a probabilidade de falha antes do release clínico"
    });
    const ids = plan.selectedAgents.map((agent) => agent.id);

    assert.equal(plan.status, "PASS");
    assert.equal(ids.includes("ct-pre-mortem"), true);
    assert.equal(ids.includes("ct-ethics-compass"), true);
    assert.equal(ids.includes("ct-bayesian-updater"), true);
    assert.equal(ids.length, 7);
    assert.equal(ids.length < 20, true);
  });

  it("does not match the counterfactual phrase 'e se' inside 'seleção'", async () => {
    const { buildCriticalThinkingPlan } = await import(
      moduleUrl("scripts/aeos-critical-thinking-governance.mjs")
    );
    const plan = buildCriticalThinkingPlan({
      skillId: "critical-thinking-governor",
      riskLevel: "high",
      request: "aplicar seleção proporcional de agentes"
    });

    assert.equal(plan.status, "PASS");
    assert.equal(plan.selectedAgents.some((agent) => agent.id === "ct-counterfactual-mirror"), false);
  });

  it("fails configuration validation when an agent id is duplicated", async () => {
    const { loadCriticalThinkingConfig, validateCriticalThinkingConfig } = await import(
      moduleUrl("scripts/aeos-critical-thinking-governance.mjs")
    );
    const config = structuredClone(loadCriticalThinkingConfig(repoRoot));
    config.agents[19].id = config.agents[0].id;

    const result = validateCriticalThinkingConfig(config);
    assert.equal(result.status, "FAIL");
    assert.equal(result.errors.some((error) => error.includes("unique")), true);
  });

  it("keeps script and runtime selection behavior equivalent", async () => {
    const { buildCriticalThinkingPlan } = await import(
      moduleUrl("scripts/aeos-critical-thinking-governance.mjs")
    );
    const { CriticalThinkingGovernor } = await import(
      moduleUrl("runtime/dist/kernel/critical-thinking-governor.js")
    );
    const request = "comparar opções de arquitetura e mapear causalidade e risco";
    const skill = {
      id: "architecture-mapper",
      path: "aeos/skills/core/architecture-mapper.skill.md",
      version: "1.0.0",
      owner_agent: "architect",
      risk_level: "high",
      capabilities: ["MAP_ARCHITECTURE"],
      mission: "Map architecture and dependencies"
    };

    const scriptPlan = buildCriticalThinkingPlan({
      skillId: skill.id,
      riskLevel: skill.risk_level,
      mission: skill.mission,
      request
    });
    const runtimePlan = new CriticalThinkingGovernor(repoRoot).planForSkill(skill, request);

    assert.equal(runtimePlan.status, "PASS");
    assert.deepEqual(
      runtimePlan.selectedAgents.map((agent) => agent.id),
      scriptPlan.selectedAgents.map((agent) => agent.id)
    );
  });

  it("makes the runtime fail closed when an agent contract path is corrupted", async () => {
    const { loadCriticalThinkingConfig } = await import(
      moduleUrl("scripts/aeos-critical-thinking-governance.mjs")
    );
    const { CriticalThinkingGovernor } = await import(
      moduleUrl("runtime/dist/kernel/critical-thinking-governor.js")
    );
    const config = structuredClone(loadCriticalThinkingConfig(repoRoot));
    config.agents[0].path = "skills/critical-thinking-governor/agents/missing.agent.md";
    const skill = {
      id: "repo-scanner",
      path: "aeos/skills/core/repo-scanner.skill.md",
      version: "1.0.0",
      owner_agent: "architect",
      risk_level: "low",
      capabilities: ["READ_REPOSITORY"]
    };

    const plan = new CriticalThinkingGovernor(repoRoot, config).planForSkill(skill, "scan");
    assert.equal(plan.status, "FAIL");
    assert.equal(plan.blockingConditions.some((condition) => condition.includes("not found")), true);
  });

  it("blocks a direct SkillExecutor call without a valid governance plan", async () => {
    const { SkillExecutor } = await import(moduleUrl("runtime/dist/kernel/skill-executor.js"));
    const executor = new SkillExecutor();

    await assert.rejects(
      executor.execute("repo-scanner", {}),
      /Critical-thinking governance is missing or invalid/
    );
  });

  it("allows governance modules to be imported when process.argv[1] is absent", () => {
    const script = "import('./scripts/aeos-skill-router.mjs').then(() => console.log('IMPORTED'))";
    const result = spawnSync(process.execPath, ["--input-type=module", "-e", script], {
      cwd: repoRoot,
      encoding: "utf8"
    });

    assert.equal(result.status, 0, result.stderr);
    assert.match(result.stdout, /IMPORTED/);
  });
});
