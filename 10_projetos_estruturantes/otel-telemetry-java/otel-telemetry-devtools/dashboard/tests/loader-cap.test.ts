import { describe, expect, it } from 'vitest';
import { MAX_RECORDS, loadJsonlLines } from '../src/loader';

/** C22: JSONL enorme carrega janela limitada sem travar (AC 20).
 *  O loader preserva os registros mais RECENTES (janela deslizante) e nunca estoura MAX_RECORDS. */
describe('loader cap', () => {
  it('capsLoadedWindow', () => {
    const extra = 1234;
    const total = MAX_RECORDS + extra;
    const lines: string[] = [];
    for (let i = 0; i < total; i++) {
      lines.push(JSON.stringify({
        resourceSpans: [{
          scopeSpans: [{
            spans: [{
              name: 'span-' + i,
              traceId: 'AAAAAAAAAAAAAAAAAAAAAA==',
              spanId: 'AAAAAAAAAAI=',
              startTimeUnixNano: String(1_700_000_000_000_000_000n + BigInt(i) * 1_000_000n),
              endTimeUnixNano: String(1_700_000_000_000_000_001n + BigInt(i) * 1_000_000n),
            }],
          }],
        }],
      }));
    }

    const records = loadJsonlLines(lines);

    expect(records.length).toBe(MAX_RECORDS);
    // janela deslizante: os mais recentes sobrevivem; o primeiro é o record #extra
    const first = records[0] as { kind: string; name: string };
    const last = records[records.length - 1] as { kind: string; name: string };
    expect(first.kind).toBe('span');
    expect(last.name).toBe('span-' + (total - 1));
    expect(first.name).toBe('span-' + extra);
  });

  it('ignoraLinhasInvalidasSemLancar', () => {
    const records = loadJsonlLines([
      'nao-e-json',
      '',
      '{"resourceSpans":[{"scopeSpans":[{"spans":[{"name":"ok","traceId":"t","spanId":"s",'
        + '"startTimeUnixNano":"1700000000000000000","endTimeUnixNano":"1700000000000000001"}]}]}]}',
    ]);
    expect(records.length).toBe(1);
    expect((records[0] as { name: string }).name).toBe('ok');
  });
});
