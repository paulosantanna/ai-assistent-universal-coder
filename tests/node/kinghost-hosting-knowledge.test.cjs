const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

describe('KingHost full hosting knowledge pack', () => {
  const root = path.resolve(__dirname, '../..');

  it('registers KingHost control MCP 1.3 with video corroboration and panel-only safety rules', () => {
    const text = fs.readFileSync(path.join(root, 'aeos/mcps/kinghost-control.mcp.yaml'), 'utf8');
    assert.match(text, /version: "1\.3\.0"/);
    assert.match(text, /backup\/recovery/);
    assert.match(text, /antivirus\/WAF/);
    assert.match(text, /Varnish\/performance/);
    assert.match(text, /official @kinghost videos/i);
    assert.match(text, /undocumented private endpoints/i);
  });

  it('indexes official KingHost channel learning and current hosting documentation', () => {
    const sources = fs.readFileSync(path.join(root, 'aeos/knowledge/kinghost-control.sources.yaml'), 'utf8');
    assert.match(sources, /youtube\.com\/@kinghost/);
    assert.match(sources, /dyrH9JIi5Ug/);
    assert.match(sources, /6cqy_R7OGu8/);
    assert.match(sources, /OzTvUGCMLtg/);
    assert.match(sources, /escanear-seu-site-antivirus/);
    assert.match(sources, /varnish-cache/);
    assert.match(sources, /como-solicitar-backup/);
    assert.match(sources, /como-integrar-github-ao-painel-kinghost/);
  });

  it('searches backup, security, DNS, email, performance and publish knowledge', async () => {
    const mod = await import(pathToFileURL(path.join(root, 'kinghost-control-mcp/index.mjs')).href);
    const result = await mod.dispatch('kinghost_control.knowledge_search', {
      query: 'backup antivirus waf dns email varnish performance git mysql wordpress ftp'
    });
    assert.equal(result.success, true);
    const ids = result.data.matches.map((item) => item.id);
    assert.ok(ids.includes('backup-recovery'));
    assert.ok(ids.includes('antivirus-malware'));
    assert.ok(ids.includes('performance-varnish'));
    const blob = JSON.stringify(result.data).toLowerCase();
    assert.match(blob, /youtube\.com\/@kinghost/);
    assert.match(blob, /undocumented private panel apis|undocumented private/);

    const catalog = await mod.dispatch('kinghost_control.plugin.catalog', {});
    const toolIds = catalog.data.panel_tools.map((item) => item.id);
    for (const expected of ['dns', 'ssl', 'backup', 'antivirus', 'waf', 'varnish', 'performance', 'email', 'git-deploy', 'mysql', 'wordpress']) {
      assert.ok(toolIds.includes(expected), `missing panel tool ${expected}`);
    }
  });

  it('registers the specialized KingHost skills under codenavi-agent', () => {
    const registry = fs.readFileSync(path.join(root, 'aeos/registries/skills.kinghost-expert.additions.yaml'), 'utf8');
    for (const skill of [
      'kinghost-backup-recovery-expert',
      'kinghost-security-expert',
      'kinghost-domain-dns-ssl-expert',
      'kinghost-email-expert',
      'kinghost-performance-expert',
      'kinghost-database-expert'
    ]) {
      assert.match(registry, new RegExp(`id: ${skill}`));
      assert.ok(fs.existsSync(path.join(root, 'skills', skill, 'SKILL.md')), `missing ${skill}/SKILL.md`);
    }
    assert.match(registry, /version: 1\.3\.0/);
    assert.match(registry, /owner_agent: codenavi-agent/);
  });

  it('defines fail-closed hosting operations and video provenance', () => {
    const ops = fs.readFileSync(path.join(root, 'skills/kinghost-expert/HOSTING_OPERATIONS.md'), 'utf8');
    assert.match(ops, /documented UI surface, not as an undocumented private API/i);
    assert.match(ops, /Video-derived instructions are learning evidence/i);
    assert.match(ops, /Backup and recovery/);
    assert.match(ops, /Antivirus and malware response/);
    assert.match(ops, /DNS, SSL and domains/);
    assert.match(ops, /Performance/);
    assert.match(ops, /E-mail operations/);
  });
});
