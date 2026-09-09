const assert = require('node:assert/strict');
const { existsSync, readFileSync } = require('node:fs');

describe('CodENavi workspace governance', () => {
  it('keeps AGENT and AGENTS aligned through canonical delegation', () => {
    const agent = readFileSync('AGENT.md', 'utf8');
    const agents = readFileSync('AGENTS.md', 'utf8');
    assert.match(agent, /BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF/);
    assert.match(agent, /CODENAVI_WORKSPACE_STANDARD\.md/);
    assert.match(agent, /codenavi-artifact-contract\.v1\.json/);
    assert.match(agents, /AGENT\.md/);
    assert.match(agents, /CODENAVI_WORKSPACE_STANDARD\.md/);
  });

  it('enforces one canonical agent and zero subagents/personas', () => {
    const registry = readFileSync('aeos/registries/agents.registry.yaml', 'utf8');
    const ids = [...registry.matchAll(/^\s*- id:\s*([^\n]+)/gm)].map((match) => match[1].trim());
    assert.deepEqual(ids, ['codenavi-agent']);
    assert.match(registry, /max_subagents:\s*0/);
    assert.match(registry, /subagents:\s*\[\s*\]/);
    assert.equal(existsSync('aeos/agents'), false, 'legacy aeos/agents directory must not exist');
    assert.equal(existsSync('aeos/subagents'), false, 'legacy aeos/subagents directory must not exist');
  });

  it('uses lenses rather than critical-thinking agent personas', () => {
    const config = JSON.parse(readFileSync('aeos/config/critical-thinking-governance.config.json', 'utf8'));
    assert.equal(Array.isArray(config.lenses), true);
    assert.equal(config.lenses.length, 20);
    assert.equal(Object.prototype.hasOwnProperty.call(config, 'agents'), false);
    assert.equal(Object.prototype.hasOwnProperty.call(config, 'baseline_agents'), false);
    assert.equal(config.baseline_lenses.length, 4);
  });

  it('collapses permission identity to the canonical agent', () => {
    const permissions = readFileSync('aeos/config/permissions.yaml', 'utf8');
    assert.match(permissions, /default_policy:\s*deny-all/);
    assert.match(permissions, /agent:\s*codenavi-agent/);
    assert.doesNotMatch(permissions, /^roles:/m);
    for (const legacy of ['root:', 'architect:', 'coder:', 'tester:', 'security:', 'devops:', 'judge:', 'documenter:']) {
      assert.equal(permissions.includes(legacy), false, `legacy permission persona leaked: ${legacy}`);
    }
  });

  it('provides progressive notebook intelligence', () => {
    assert.equal(existsSync('.notebook/INDEX.md'), true);
    assert.equal(existsSync('references/CODENAVI_NOTEBOOK_SPEC.md'), true);
    const index = readFileSync('.notebook/INDEX.md', 'utf8');
    assert.match(index, /Project intelligence/);
  });

  it('registers new skills with explicit CodENavi governance', () => {
    const paths = [
      'skills/codenavi/SKILL.md',
      'skills/notebook-intelligence/SKILL.md',
      'skills/dependency-updater/SKILL.md',
      'skills/pr-reviewer/SKILL.md',
      'skills/docs-writer/SKILL.md',
      'skills/local-secret-vault/SKILL.md',
      'skills/jira-confluence-assistant/SKILL.md',
      'skills/java-version-expert/SKILL.md'
    ];
    for (const path of paths) {
      assert.equal(existsSync(path), true, `${path} missing`);
      assert.match(readFileSync(path, 'utf8'), /Governance: CodENavi v1/);
    }
  });

  it('defines a machine-readable contract for every governed artifact class', () => {
    const path = 'aeos/governance/codenavi-artifact-contract.v1.json';
    assert.equal(existsSync(path), true);
    const contract = JSON.parse(readFileSync(path, 'utf8'));
    assert.equal(contract.standard, 'CodENavi Artifact Contract v1');
    assert.deepEqual(contract.lifecycle, ['BRIEFING', 'RECON', 'PLAN', 'EXECUTE', 'VERIFY', 'DEBRIEF']);
    for (const type of ['agent','skill','playbook','mcp','lcp','lsp','registry','blueprint','eval','memory_knowledge','runtime_tool','ci_release','documentation']) {
      assert.ok(contract.artifact_types[type], `missing artifact contract for ${type}`);
      assert.ok(contract.artifact_types[type].required_contracts.length > 0, `empty artifact contract for ${type}`);
    }
  });
});
