import { describe, expect, it } from 'vitest'
import { PDFDocument } from 'pdf-lib'
import { blankPackLike } from './helpers'
import { canonicalJson, certCodeFromHash, renderCertificatePdf, sha256Hex } from '../src/engine/certificate'
import { emptyGameState, type GameState } from '../src/engine/types'
import { pack } from '../src/content/pack'
import { buildEvidenceDossier } from '../src/engine/certificate'

describe('hash canônico e código AIE', () => {
  it('canonicalJson ordena chaves: objetos com ordem diferente dão o mesmo hash', async () => {
    const a = canonicalJson({ b: 1, a: 2, c: { zz: 1, aa: 2 } })
    const b = canonicalJson({ a: 2, b: 1, c: { aa: 2, zz: 1 } })
    expect(a).toBe(b)
    expect(await sha256Hex(a)).toBe(await sha256Hex(b))
  })

  it('sha256 de "abc" é o valor de referência FIPS', async () => {
    expect(await sha256Hex('abc')).toBe('ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad')
  })

  it('código no formato AIE-YYYY-HASH8', () => {
    const code = certCodeFromHash('deadbeeff01234', '2026-11-10T00:00:00Z')
    expect(code).toMatch(/^AIE-\d{4}-[0-9A-F]{8}$/)
    expect(code.startsWith('AIE-2026-')).toBe(true)
  })

  it('dossiê cobre pontos-chave do progresso', () => {
    const gs: GameState = emptyGameState()
    gs.playerName = 'Mesa 7'
    gs.ledger.push({ id: 'e1', kind: 'answer', delta: 20, ref: 'q', at: 't' })
    const dossier = buildEvidenceDossier(pack, gs, '2026-11-10T00:00:00Z')
    expect(dossier.name).toBe('Mesa 7')
    expect(dossier.balanceAtIssue).toBe(20)
    expect(dossier.packVersion).toBe(pack.version)
  })
})

describe('PDF do certificado (pdf-lib)', () => {
  it('PDF válido: header %PDF, 1 página e código+hash recuperáveis dos metadados', async () => {
    const hash = '0'.repeat(64)
    const blob = await renderCertificatePdf({
      name: 'Mesa Vinte',
      code: 'AIE-2026-DEADBEEF',
      hash,
      score: 0.92,
      issuedAt: '2026-11-10T00:00:00Z',
      organ: 'Guilda da Trilha',
      typology: 'curso livre',
      realms: pack.realms.map((r) => ({ name: r.name, tier: r.tier })),
    })
    const bytes = new Uint8Array(await blob.arrayBuffer())
    const latin = new TextDecoder('latin1').decode(bytes)
    expect(latin.startsWith('%PDF')).toBe(true)
    expect(blankPackLike.test(latin)).toBe(false)
    // pdf-lib grava strings de Info como UTF-16BE hex (não ASCII cru):
    // a presença do código/hash se prova lendo o documento de volta.
    const loaded = await PDFDocument.load(bytes)
    expect(loaded.getPageCount()).toBe(1)
    expect(loaded.getKeywords() ?? '').toContain('AIE-2026-DEADBEEF')
    expect(loaded.getSubject() ?? '').toContain(hash)
  })
})

describe('estrutura mínima do estado (persistence sanity)', () => {
  it('normalizeProgress aceita estado vazio e rejeita versão estranha', async () => {
    const { normalizeProgress } = await import('../src/engine/persistence')
    const gs = normalizeProgress(emptyGameState())
    expect(gs.version).toBe(1)
    expect(() => normalizeProgress({ version: 99 })).toThrow()
  })
})
