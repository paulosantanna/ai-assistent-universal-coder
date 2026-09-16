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
    assert.match(text, /kinghost_control\.panel\.session\.open_cookie_file/);
    assert.match(text, /kinghost_control\.domain\.list/);
    assert.match(text, /kinghost_control\.site\.clone/);
    assert.match(text, /kinghost_control\.publish\.preflight/);
    assert.match(text, /storage: forbidden/);
  });

  it('keeps kinghost overlay YAML parseable when skill_intent contains a colon', () => {
    const text = fs.readFileSync(path.join(root, 'aeos/registries/mcps.kinghost.additions.yaml'), 'utf8');
    const intent = text.match(/id: kinghost-control[\s\S]*?skill_intent:\s*(.+)/);
    assert.ok(intent, 'kinghost-control skill_intent must exist');
    assert.match(intent[1], /^['"].+['"]\s*$/);
  });

  it('defines kinghost-expert FSM, cookie and Playwright production rules', () => {
    const skill = fs.readFileSync(path.join(root, 'skills/kinghost-expert/SKILL.md'), 'utf8');
    assert.match(skill, /ENV_SELECTED/);
    assert.match(skill, /external runtime cookie\/cookie-jar/i);
    assert.match(skill, /Playwright/);
    assert.match(skill, /already created/i);
    assert.match(skill, /domain\.list/);
    assert.match(skill, /site\.clone/);
    assert.match(skill, /WooCommerce/);
    assert.match(skill, /kinghost-wordpress-publish/);
    assert.match(skill, /aeos:kinghost:publish/);
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

  it('searches KingHost Hospedagem knowledge for WordPress, MySQL, FTP and WooCommerce', async () => {
    const mod = await import(pathToFileURL(path.join(root, 'kinghost-control-mcp/index.mjs')).href);
    const result = await mod.dispatch('kinghost_control.knowledge_search', { query: 'woocommerce mysql ftp dominio cookie' });
    assert.equal(result.success, true);
    assert.ok(result.data.matches.length >= 3);
    const blob = JSON.stringify(result.data).toLowerCase();
    assert.match(blob, /woocommerce/);
    assert.match(blob, /painel\.kinghost\.com\.br/);
    assert.match(blob, /aeos:kinghost:publish|kinghost-wordpress-publish/);
    const plugins = await mod.dispatch('kinghost_control.plugin.catalog', {});
    assert.equal(plugins.success, true);
    assert.ok(plugins.data.wordpress_plugins.some((plugin) => plugin.slug === 'woocommerce'));
    assert.ok(plugins.data.panel_tools.some((tool) => tool.id === 'ftp'));
  });

  it('lists and selects existing domains from operator inventory', async () => {
    const mod = await import(pathToFileURL(path.join(root, 'kinghost-control-mcp/index.mjs')).href);
    process.env.KINGHOST_DOMAINS = 'reidoabc.com.br,loja.example.com.br';
    const listed = await mod.dispatch('kinghost_control.domain.list', {});
    assert.equal(listed.success, true);
    assert.ok(listed.data.domains.some((item) => item.domain === 'reidoabc.com.br'));
    const selected = await mod.dispatch('kinghost_control.domain.select', {
      domain: 'reidoabc.com.br',
      environment_id: 'production'
    });
    assert.equal(selected.success, true);
    assert.equal(selected.data.domain, 'reidoabc.com.br');
    assert.equal(selected.data.fsm_state, 'ENV_SELECTED');
    const unknown = await mod.dispatch('kinghost_control.domain.select', { domain: 'not-in-list.example' });
    assert.equal(unknown.success, false);
    delete process.env.KINGHOST_DOMAINS;
  });

  it('binds a panel cookie jar without returning cookie values', async () => {
    const mod = await import(pathToFileURL(path.join(root, 'kinghost-control-mcp/index.mjs')).href);
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'kinghost-cookie-'));
    const jar = path.join(dir, 'painel-cookies.txt');
    const secret = 'panel-cookie-secret-value-do-not-leak';
    fs.writeFileSync(jar, [
      '# Netscape HTTP Cookie File',
      `.kinghost.com.br\tTRUE\t/\tTRUE\t1893456000\tPHPSESSID\t${secret}`,
      'painel.kinghost.com.br\tFALSE\t/\tTRUE\t1893456000\tkh_session\tsecond-secret'
    ].join('\n'));
    const opened = await mod.dispatch('kinghost_control.panel.session.open_cookie_file', { cookie_file_path: jar });
    assert.equal(opened.success, true);
    assert.match(opened.data.panel_session_ref, /^panel_/);
    assert.equal(opened.data.cookie_count, 2);
    assert.equal(JSON.stringify(opened).includes(secret), false);
    assert.equal(JSON.stringify(opened).includes('second-secret'), false);

    const inside = path.join(root, '.tmp-kinghost-cookie-test.txt');
    fs.writeFileSync(inside, fs.readFileSync(jar));
    const blocked = await mod.dispatch('kinghost_control.panel.session.open_cookie_file', { cookie_file_path: inside });
    assert.equal(blocked.success, false);
    assert.match(String(blocked.error), /outside the tracked workspace/);
    fs.rmSync(inside, { force: true });
    fs.rmSync(dir, { recursive: true, force: true });
  });

  it('lists already-created users from bound credentials without passwords', async () => {
    const mod = await import(pathToFileURL(path.join(root, 'kinghost-control-mcp/index.mjs')).href);
    process.env.KINGHOST_TEST_FTP_USER = 'ftp-reidoabc';
    process.env.KINGHOST_TEST_FTP_PASSWORD = 'another-secret';
    await mod.dispatch('kinghost_control.credential.bind', {
      kind: 'ftp',
      source_class: 'env_reference',
      username_env: 'KINGHOST_TEST_FTP_USER',
      password_env: 'KINGHOST_TEST_FTP_PASSWORD',
      host: 'ftp.reidoabc.com.br'
    });
    const users = await mod.dispatch('kinghost_control.users.list', { usernames: 'wp-admin-already-created' });
    assert.equal(users.success, true);
    assert.ok(users.data.users.ftp.some((item) => item.username === 'ftp-reidoabc'));
    assert.ok(users.data.users.operator.some((item) => item.username === 'wp-admin-already-created'));
    assert.equal(JSON.stringify(users).includes('another-secret'), false);
    delete process.env.KINGHOST_TEST_FTP_USER;
    delete process.env.KINGHOST_TEST_FTP_PASSWORD;
  });

  it('plans clone and production deploy without an FTP session, and parses FTP listings', async () => {
    const mod = await import(pathToFileURL(path.join(root, 'kinghost-control-mcp/index.mjs')).href);
    const clone = await mod.dispatch('kinghost_control.site.clone', { session_ref: 'missing' });
    assert.equal(clone.success, false);
    const deploy = await mod.dispatch('kinghost_control.deploy.workspace_to_production', {
      workspace_root: root
    });
    assert.equal(deploy.success, true);
    assert.equal(deploy.data.status, 'PLAN');
    const tree = await import(pathToFileURL(path.join(root, 'kinghost-control-mcp/ftp-tree.mjs')).href);
    const parsed = tree.parseFtpListing([
      'drwxr-xr-x  12 user group 4096 Sep 16 12:00 public_html',
      '-rw-r--r--   1 user group  123 Sep 16 12:00 index.php',
      'type=dir;size=4096; woocommerce'
    ].join('\n'));
    assert.ok(parsed.some((entry) => entry.name === 'public_html' && entry.type === 'dir'));
    assert.ok(parsed.some((entry) => entry.name === 'index.php' && entry.type === 'file'));
    assert.ok(parsed.some((entry) => entry.name === 'woocommerce' && entry.type === 'dir'));
    const wp = await import(pathToFileURL(path.join(root, 'kinghost-control-mcp/wordpress-ops.mjs')).href);
    assert.equal(wp.maskEmail('owner@reidoabc.com.br'), 'o***@reidoabc.com.br');
    assert.deepEqual(
      wp.parsePhpSerializedPluginList('a:1:{i:0;s:27:"woocommerce/woocommerce.php";}'),
      ['woocommerce/woocommerce.php']
    );
  });

  it('preflights one-command publish for a local WordPress/WooCommerce tree', async () => {
    const mod = await import(pathToFileURL(path.join(root, 'kinghost-control-mcp/index.mjs')).href);
    const wp = await import(pathToFileURL(path.join(root, 'kinghost-control-mcp/wordpress-ops.mjs')).href);
    const tree = fs.mkdtempSync(path.join(os.tmpdir(), 'kinghost-wp-'));
    fs.mkdirSync(path.join(tree, 'wp-content', 'themes', 'demo'), { recursive: true });
    fs.mkdirSync(path.join(tree, 'wp-content', 'plugins', 'woocommerce'), { recursive: true });
    fs.mkdirSync(path.join(tree, 'wp-content', 'plugins', 'contact-form-7'), { recursive: true });
    fs.mkdirSync(path.join(tree, 'wp-content', 'mu-plugins'), { recursive: true });
    fs.writeFileSync(path.join(tree, 'wp-content', 'plugins', 'woocommerce', 'woocommerce.php'), "<?php\n/* Plugin Name: WooCommerce */");
    fs.writeFileSync(path.join(tree, 'wp-content', 'plugins', 'contact-form-7', 'contact-form-7.php'), "<?php\n/* Plugin Name: Contact Form 7 */");
    fs.writeFileSync(path.join(tree, 'wp-content', 'plugins', 'hello.php'), "<?php\n/* Plugin Name: Hello Dolly */");
    fs.writeFileSync(path.join(tree, 'wp-content', 'mu-plugins', 'site-guard.php'), "<?php\n/* Plugin Name: Site Guard */");
    fs.writeFileSync(path.join(tree, 'wp-config.php'), "define('DB_PASSWORD', 'must-not-upload');");
    process.env.KINGHOST_FTP_PASSWORD = 'never-return-this-ftp-secret';
    const preflight = await mod.dispatch('kinghost_control.publish.preflight', { workspace_root: tree });
    assert.equal(preflight.success, true);
    assert.equal(preflight.data.status, 'READY');
    assert.equal(preflight.data.playbook_id, 'kinghost-wordpress-publish');
    assert.equal(preflight.data.inspection.wordpress, true);
    assert.equal(preflight.data.inspection.woocommerce_plugin_present, true);
    assert.ok(preflight.data.plugins.slugs.includes('woocommerce'));
    assert.ok(preflight.data.plugins.slugs.includes('contact-form-7'));
    assert.ok(preflight.data.plugins.slugs.includes('hello'));
    assert.ok(preflight.data.plugins.slugs.includes('site-guard'));
    assert.equal(preflight.data.plugins.mu_plugin_count, 1);
    assert.equal(preflight.data.inspection.wp_config_present, true);
    assert.ok(preflight.data.inspection.excluded_by_default.includes('wp-config.php'));
    assert.equal(preflight.data.woocommerce.replace_database_allowed, false);
    assert.ok(preflight.data.woocommerce.preserve_on_production.some((item) => /orders/i.test(item)));
    assert.ok(preflight.data.credential_presence.present_env_names.includes('KINGHOST_FTP_PASSWORD'));
    assert.equal(JSON.stringify(preflight).includes('never-return-this-ftp-secret'), false);
    assert.equal(JSON.stringify(preflight).includes('must-not-upload'), false);
    const inspected = wp.inspectLocalWordpressTree(tree);
    assert.equal(inspected.layout, 'wordpress_root');
    fs.rmSync(tree, { recursive: true, force: true });
    delete process.env.KINGHOST_FTP_PASSWORD;
  });
});
