const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

describe('KingHost control MCP contracts', () => {
  const root = path.resolve(__dirname, '../..');

  it('registers deterministic control tools without persisting credentials', () => {
    const text = fs.readFileSync(path.join(root, 'aeos/mcps/kinghost-control.mcp.yaml'), 'utf8');
    assert.match(text, /id: kinghost-control/);
    assert.match(text, /kinghost_control\.environment\.select/);
    assert.match(text, /kinghost_control\.credential\.bind/);
    assert.match(text, /kinghost_control\.ftp\.upload/);
    assert.match(text, /storage: forbidden/);
  });

  it('defines kinghost-expert FSM, cookie and Playwright production rules', () => {
    const skill = fs.readFileSync(path.join(root, 'skills/kinghost-expert/SKILL.md'), 'utf8');
    assert.match(skill, /ENV_SELECTED/);
    assert.match(skill, /external runtime cookie\/cookie-jar/i);
    assert.match(skill, /Playwright/);
    assert.match(skill, /already created/i);
    const permissions = fs.readFileSync(path.join(root, 'skills/kinghost-expert/PERMISSIONS.yaml'), 'utf8');
    assert.match(permissions, /kinghost\.credential\.discover_or_scrape/);
    assert.match(permissions, /permanently_denied:/);
  });

  it('binds env credentials as opaque refs and never returns the password', async () => {
    process.env.KINGHOST_TEST_FTP_USER = 'ftp-user';
    process.env.KINGHOST_TEST_FTP_PASSWORD = 'super-secret-ftp-password';
    const mod = await import(pathToFileURL(path.join(root, 'kinghost-control-mcp/index.mjs')).href);
    const bound = await mod.dispatch('kinghost_control.credential.bind', {
      kind: 'ftp',
      source_class: 'env_reference',
      username_env: 'KINGHOST_TEST_FTP_USER',
      password_env: 'KINGHOST_TEST_FTP_PASSWORD',
      host: 'ftp.example.king.host'
    });
    assert.equal(bound.success, true);
    assert.match(bound.data.credential_ref, /^cred_/);
    assert.equal(bound.data.username, 'ftp-user');
    assert.equal(bound.data.has_secret, true);
    assert.equal(JSON.stringify(bound).includes('super-secret-ftp-password'), false);
    delete process.env.KINGHOST_TEST_FTP_USER;
    delete process.env.KINGHOST_TEST_FTP_PASSWORD;
  });

  it('enforces production FSM order and dry-run FTP uploads', async () => {
    const mod = await import(pathToFileURL(path.join(root, 'kinghost-control-mcp/index.mjs')).href);
    const selected = await mod.dispatch('kinghost_control.environment.select', { environment_id: 'production' });
    assert.equal(selected.success, true);
    const skip = await mod.dispatch('kinghost_control.fsm.advance', { change_id: selected.data.change_id, to_state: 'APPLY' });
    assert.equal(skip.success, false);
    const next = await mod.dispatch('kinghost_control.fsm.advance', { change_id: selected.data.change_id, to_state: 'CREDENTIALS_BOUND' });
    assert.equal(next.success, true);

    const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'kinghost-ftp-'));
    const local = path.join(temp, 'style.css');
    fs.writeFileSync(local, 'body{color:gold}');
    const upload = await mod.handleEnvelope({
      request_id: "ftp-missing",
      action: "kinghost_control.ftp.upload",
      params: {
        session_ref: "missing",
        local_path: "style.css",
        remote_path: "wp-content/themes/demo/style.css",
        workspace_root: temp,
        approved: true,
        change_id: selected.data.change_id,
        rollback_ref: "rollback-1"
      }
    });
    assert.equal(upload.success, false);
    assert.match(String(upload.error), /Unknown or expired ftp session_ref/);
    fs.rmSync(temp, { recursive: true, force: true });
  });
});
