import { describe, expect, it } from 'vitest'
import {
  CORRECT_POINTS,
  HINT_COST,
  D20_FAIL_PENALTY,
  balance,
  canBuyHint,
  canRollD20,
  entryCorrect,
  entryD20Penalty,
  entryD20Win,
  entryHint,
  xpEarned,
} from '../src/engine/economy'
import type { LedgerEntry } from '../src/engine/types'

let seq = 0
function entry(delta: number, kind: LedgerEntry['kind'] = 'hint_cost'): LedgerEntry {
  seq += 1
  return { id: `t-${seq}`, kind, delta, ref: 'r', at: '2026-01-01T00:00:00Z' }
}

function ledgerOf(...deltas: number[]): LedgerEntry[] {
  return deltas.map((d) => entry(d))
}

describe('economia: correta = +20, dica = 100', () => {
  it('entrada de resposta certa vale +20 e xp soma só positivos', () => {
    expect(entryCorrect('q').delta).toBe(CORRECT_POINTS)
    expect(CORRECT_POINTS).toBe(20)
    const l = ledgerOf(20, -100, 20)
    expect(xpEarned(l)).toBe(40)
  })
  it('HINT_COST e D20_FAIL_PENALTY são as regras do usuário', () => {
    expect(HINT_COST).toBe(100)
    expect(D20_FAIL_PENALTY).toBe(10)
  })
})

describe('limites de saldo (<= 100): compra e D20', () => {
  it('saldo 100 permite dica; 99 NÃO permite dica mas LIBERA o D20', () => {
    expect(canBuyHint(ledgerOf(100))).toBe(true)
    expect(canBuyHint(ledgerOf(99))).toBe(false)
    expect(canRollD20(ledgerOf(99))).toBe(true)
  })
  it('saldo >= 100 bloqueia a rolagem: D20 existe para quem não tem dica', () => {
    expect(canRollD20(ledgerOf(100))).toBe(false)
    expect(canRollD20(ledgerOf(101))).toBe(false)
    expect(canRollD20(ledgerOf(20))).toBe(true)
  })
  it('comprar a dica debita 100: 100 -> 0', () => {
    const l = [...ledgerOf(120), entryHint('q')]
    expect(balance(l)).toBe(20)
    const l2 = [...ledgerOf(100), entryHint('q')]
    expect(balance(l2)).toBe(0)
  })
})

describe('rolagem de vitória e penalidade com clamp', () => {
  it('d20_win paga +20 com selo S/L', () => {
    expect(entryD20Win('q').delta).toBe(20)
    expect(entryD20Win('q').kind).toBe('d20_win')
  })
  it('penalidade nunca deixa o saldo negativo: saldo 5 -> -5 registrado', () => {
    const delta = entryD20Penalty(ledgerOf(5), 'q').delta
    expect(delta).toBe(-5)
  })
  it('saldo 0: penalidade aplicada é 0 (clamp)', () => {
    expect(entryD20Penalty(ledgerOf(0), 'q').delta).toBe(-0)
  })
  it('saldo 99 fica 89 após penalidade cheia', () => {
    const l = [...ledgerOf(99), entryD20Penalty(ledgerOf(99), 'q')]
    expect(balance(l)).toBe(89)
  })
})
