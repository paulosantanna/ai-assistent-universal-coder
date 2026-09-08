const assert = require('node:assert/strict');
const { spawn } = require('node:child_process');
const { join } = require('node:path');

function callAura(action, params = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [join(process.cwd(), 'aura-voice-tool', 'index.mjs')], { stdio: ['pipe','pipe','pipe'] });
    let out = '';
    let err = '';
    child.stdout.on('data', c => out += c.toString());
    child.stderr.on('data', c => err += c.toString());
    child.on('error', reject);
    child.on('exit', code => {
      if (code !== 0 && !out.trim()) return reject(new Error(err || `exit ${code}`));
      try { resolve(JSON.parse(out.trim().split(/\r?\n/)[0])); } catch (e) { reject(e); }
    });
    child.stdin.end(JSON.stringify({ request_id: 'test', action, params }) + '\n');
  });
}

describe('Aura Voice tool', () => {
  it('reports supported capabilities', async () => {
    const res = await callAura('aura.health');
    assert.equal(res.success, true);
    assert.equal(res.data.asr, 'whisper.cpp');
    assert.ok(res.data.media.includes('.mp4'));
    assert.ok(res.data.transcripts.includes('.tft'));
  });

  it('preserves technical nomenclature and separates humor from serious content', async () => {
    const text = [
      'A arquitetura precisa ser end-to-end e o fluxo B2C precisa ter rollback.',
      'Se der erro a gente joga o servidor pela janela, tô brincando kkk.',
      'We must monitor latency and production errors before deploy.'
    ].join('\n');
    const res = await callAura('aura.analyze.transcript', { text });
    assert.equal(res.success, true);
    assert.match(res.data.serious_text, /end-to-end/);
    assert.match(res.data.serious_text, /B2C/);
    assert.ok(res.data.statistics.serious >= 2);
    assert.ok(res.data.statistics.humor >= 1);
  });

  it('does not ingest corpus without explicit authorization', async () => {
    const res = await callAura('aura.corpus.ingest', { source: 'youtube:test', path: 'missing.txt', authorized: false });
    assert.equal(res.success, false);
    assert.match(res.error, /authorized=true/i);
  });
});
