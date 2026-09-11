const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

describe('WordPress knowledge MCP contracts', () => {
  const root = path.resolve(__dirname, '../..');
  it('registers official WordPress and Reddit sources without write credentials', () => {
    const text = fs.readFileSync(path.join(root, 'aeos/mcps/wordpress-knowledge.mcp.yaml'), 'utf8');
    assert.match(text, /developer\.wordpress\.org/);
    assert.match(text, /reddit\.com\/r\/Wordpress/);
    assert.match(text, /write_allowed: false/);
    assert.match(text, /credentials_allowed: false/);
  });

  it('defines first-run-only Beta Mapping and cookie runtime semantics', () => {
    const skill = fs.readFileSync(path.join(root, 'skills/wordpress-expert/SKILL.md'), 'utf8');
    assert.match(skill, /One-shot invariant/i);
    assert.match(skill, /external runtime cookie\/cookie-jar/i);
    assert.match(skill, /never fully regenerated automatically/i);
  });

  it('keeps WordPress core feature edits prohibited', () => {
    const permissions = fs.readFileSync(path.join(root, 'skills/wordpress-expert/PERMISSIONS.yaml'), 'utf8');
    assert.match(permissions, /wordpress\.core\.edit_for_feature_work/);
    assert.match(permissions, /permanently_denied:/);
  });
});
