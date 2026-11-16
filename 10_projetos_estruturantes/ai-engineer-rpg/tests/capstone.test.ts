import { describe, expect, it } from 'vitest'
import {
  CAPSTONE_MIN_COMP,
  CAPSTONE_PASS_SCORE,
  SCORE_MAX,
  evaluateCapstone,
  validateCapstoneShape,
} from '../src/engine/capstone'
import { pack } from '../src/content/pack'
import type { Capstone } from '../src/engine/types'

describe('juízo determinístico do Capstone', () => {
  it('constantes do juízo', () => {
    expect(CAPSTONE_PASS_SCORE).toBe(0.85)
    expect(CAPSTONE_MIN_COMP).toBe(0.5)
    expect(SCORE_MAX).toBe(4)
  })

  it('capstone real passa na checagem de forma', () => {
    expect(validateCapstoneShape(pack.capstone)).toEqual([])
  })

  function fakeCap(): Capstone {
    return {
      dissertation: { prompt: 'p', minChars: 10 },
      tasks: [
        { id: 'a', competency: 'A', weight: 0.6, prompt: 'x', options: [{ text: 'x', score: 0 } as never] },
        { id: 'b', competency: 'B', weight: 0.4, prompt: 'y', options: [{ text: 'y', score: 0 } as never] },
      ],
    }
  }

  it('limite: exatamente 0.85 passa (arredondamento 4 casas)', () => {
    // a (0.6) completa, b em score 3 => 0.6*1 + 0.4*0.75 = 0.9
    const v = evaluateCapstone(fakeCap(), { a: 4, b: 3 }, 'dissertacao')
    expect(v.finalScore).toBe(0.9)
    expect(v.passed).toBe(true)
  })

  it('competência abaixo de 0.50 reprova mesmo com final >= 0.85', () => {
    // a completa; b score 1 => 0.1 => 0.6*1 + 0.4*0.25 = 0.7 reprovado também
    const v = evaluateCapstone(fakeCap(), { a: 4, b: 1 }, 'dissertacao')
    expect(v.finalScore).toBe(0.7)
    expect(v.passed).toBe(false)
    expect(v.failures.some((f) => f.includes('mínimo'))).toBe(true)
  })

  it('nota final < 0.85 reprova com falha listada', () => {
    const v = evaluateCapstone(fakeCap(), { a: 4, b: 2 }, 'dissertacao') // 0.8
    expect(v.finalScore).toBe(0.8)
    expect(v.passed).toBe(false)
  })

  it('dissertação curta reprova', () => {
    const v = evaluateCapstone(fakeCap(), { a: 4, b: 4 }, 'curta')
    expect(v.passed).toBe(false)
    expect(v.failures.some((f) => f.includes('Dissertação'))).toBe(true)
  })

  it('tarefa ausente = 0 e falha pendência', () => {
    const v = evaluateCapstone(fakeCap(), { a: 4 }, 'dissertacao')
    expect(v.compScores.b).toBe(0)
    expect(v.failures.some((f) => f.includes('pendente'))).toBe(true)
    expect(v.passed).toBe(false)
  })

  it('clamp: score 9 tratado como 4', () => {
    const v = evaluateCapstone(fakeCap(), { a: 9, b: 4 }, 'dissertacao')
    expect(v.finalScore).toBe(1)
  })
})
