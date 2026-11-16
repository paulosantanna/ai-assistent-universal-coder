import { describe, expect, it } from 'vitest'
import { pack } from '../src/content/pack'
import { validateContentPack } from '../src/engine/packValidator'
import { evaluateCapstone } from '../src/engine/capstone'

describe('contrato do ContentPack v1', () => {
  const result = validateContentPack(pack)

  it('não tem erros de validação', () => {
    expect(result.errors).toEqual([])
  })

  it('atende os mínimos: 7 reinos, >= 36 lições, >= 120 questões', () => {
    expect(result.stats.realms).toBe(7)
    expect(result.stats.lessons).toBeGreaterThanOrEqual(36)
    expect(result.stats.missions).toBeGreaterThanOrEqual(30)
    expect(result.stats.questions).toBeGreaterThanOrEqual(120)
    expect(result.stats.sources).toBeGreaterThanOrEqual(20)
    expect(result.stats.glossary).toBeGreaterThanOrEqual(50)
  })

  it('pesos JEV dos reinos somam 1.0', () => {
    const sum = pack.realms.reduce((s, r) => s + r.jevWeight, 0)
    expect(Math.abs(sum - 1)).toBeLessThan(1e-6)
  })

  it('regras de selo JEV nas fontes (auto >= 0.7; revisar só entre 0.5 e 0.7)', () => {
    const sources = pack.realms.flatMap((r) => r.sources)
    const auto = sources.filter((s) => s.flag === 'auto')
    const revisar = sources.filter((s) => s.flag === 'revisar')
    expect(auto.length).toBeGreaterThan(0)
    for (const s of auto) expect(s.confidence).toBeGreaterThanOrEqual(0.7)
    for (const s of revisar) {
      expect(s.confidence).toBeGreaterThanOrEqual(0.5)
      expect(s.confidence).toBeLessThan(0.7)
    }
    for (const s of sources) expect(s.checkedAt.length).toBeGreaterThanOrEqual(10)
  })

  it('cada questão tem dica >= 8 caracteres e >= 3 opções com índice válido', () => {
    let count = 0
    for (const realm of pack.realms) {
      for (const q of realm.questions) {
        count += 1
        expect(q.hint.length).toBeGreaterThanOrEqual(8)
        expect(q.options.length).toBeGreaterThanOrEqual(3)
        expect(q.correct).toBeGreaterThanOrEqual(0)
        expect(q.correct).toBeLessThan(q.options.length)
      }
    }
    expect(count).toBe(result.stats.questions)
  })

  it('capstone: 8 competências com pesos somando 1.0 e rubricas 0..4', () => {
    expect(pack.capstone.tasks).toHaveLength(8)
    const sum = pack.capstone.tasks.reduce((s, t) => s + t.weight, 0)
    expect(Math.abs(sum - 1)).toBeLessThan(1e-6)
    for (const t of pack.capstone.tasks) {
      expect(t.options).toHaveLength(5)
      t.options.forEach((o, i) => expect(o.score).toBe(i))
    }
    expect(pack.capstone.dissertation.minChars).toBeGreaterThanOrEqual(400)
  })

  it('banca do capstone: tudo em 4 aprova; dm pisar competência pesada reprova', () => {
    const scoresAllFour: Record<string, number> = {}
    for (const t of pack.capstone.tasks) scoresAllFour[t.id] = 4
    const good = evaluateCapstone(pack.capstone, scoresAllFour, 'x'.repeat(400))
    expect(good.passed).toBe(true)
    expect(good.finalScore).toBe(1)

    const heaviest = [...pack.capstone.tasks].sort((a, b) => b.weight - a.weight)[0]
    const scoresWeak: Record<string, number> = {}
    for (const t of pack.capstone.tasks) scoresWeak[t.id] = t.id === heaviest.id ? 1 : 4
    const bad = evaluateCapstone(pack.capstone, scoresWeak, 'x'.repeat(400))
    expect(bad.passed).toBe(false)
  })

  it('ids de questões são únicos entre reinos', () => {
    const ids = pack.realms.flatMap((r) => r.questions.map((q) => q.id))
    expect(new Set(ids).size).toBe(ids.length)
  })
})
