const assert = require('node:assert/strict');
const { existsSync, readFileSync } = require('node:fs');

describe('CodENavi workspace governance', () => {
  it('keeps AGENT and AGENTS aligned through canonical delegation', () => {
    const agent = readFileSync('AGENT.md', 'utf8');
    const agents = readFileSync('AGENTS.md', 'utf8');
    assert.match(agent, /BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF/);
    assert.match(agent, /CODENAVI_WORKSPACE_STANDARD\.md/);
    assert.match(agents, /AGENT\.md/);
    assert.match(agents, /CODENAVI_WORKSPACE_STANDARD\.md/);
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
});
