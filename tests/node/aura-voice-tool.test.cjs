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
    expect(res.success).toBe(true);
    expect(res.data.asr).toBe('whisper.cpp');
    expect(res.data.media).toContain('.mp4');
    expect(res.data.transcripts).toContain('.tft');
  });

  it('preserves technical nomenclature and separates humor from serious content', async () => {
    const text = [
      'A arquitetura precisa ser end-to-end e o fluxo B2C precisa ter rollback.',
      'Se der erro a gente joga o servidor pela janela, tô brincando kkk.',
      'We must monitor latency and production errors before deploy.'
    ].join('\n');
    const res = await callAura('aura.analyze.transcript', { text });
    expect(res.success).toBe(true);
    expect(res.data.serious_text).toContain('end-to-end');
    expect(res.data.serious_text).toContain('B2C');
    expect(res.data.statistics.serious).toBeGreaterThanOrEqual(2);
    expect(res.data.statistics.humor).toBeGreaterThanOrEqual(1);
  });

  it('does not ingest corpus without explicit authorization', async () => {
    const res = await callAura('aura.corpus.ingest', { source: 'youtube:test', path: 'missing.txt', authorized: false });
    expect(res.success).toBe(false);
    expect(res.error).toMatch(/authorized=true/i);
  });
});
