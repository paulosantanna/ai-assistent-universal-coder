// Economia do jogo — regras fixas do usuário:
//  - resposta certa = +20
//  - saldo >= 100 compra 1 dica (debita 100)
//  - saldo < 100 libera 1 tentativa de D20 por questão:
//      rolagem >= 15 garante a questão correta (+20 com selo D20)
//      rolagem < 15 desconta 10 do saldo (nunca deixa saldo negativo)

import type { LedgerEntry, LedgerKind } from './types'

export const CORRECT_POINTS = 20
export const HINT_COST = 100
export const D20_THRESHOLD = 15
export const D20_FAIL_PENALTY = 10
export const D20_SIDES = 20

export function balance(ledger: LedgerEntry[]): number {
  let total = 0
  for (const e of ledger) total += e.delta
  return total
}

/** XP = total bruto já ganho (positivos), não descontado por dicas/penalidades */
export function xpEarned(ledger: LedgerEntry[]): number {
  let total = 0
  for (const e of ledger) if (e.delta > 0) total += e.delta
  return total
}

export function canBuyHint(ledger: LedgerEntry[]): boolean {
  return balance(ledger) >= HINT_COST
}

/** O D20 só substitui a dica quando o jogador NÃO tem saldo para comprá-la */
export function canRollD20(ledger: LedgerEntry[]): boolean {
  return balance(ledger) < HINT_COST
}

let seq = 0
export function makeEntry(kind: LedgerKind, delta: number, ref: string): LedgerEntry {
  seq += 1
  return { id: `e${Date.now().toString(36)}-${seq}`, kind, delta, ref, at: new Date().toISOString() }
}

export function entryCorrect(ref: string): LedgerEntry {
  return makeEntry('answer', CORRECT_POINTS, ref)
}

export function entryHint(ref: string): LedgerEntry {
  return makeEntry('hint_cost', -HINT_COST, ref)
}

export function entryD20Win(ref: string): LedgerEntry {
  return makeEntry('d20_win', CORRECT_POINTS, ref)
}

/** penalidade do D20 com clamp: o debitado real nunca deixa o saldo negativo */
export function entryD20Penalty(ledger: LedgerEntry[], ref: string): LedgerEntry {
  const current = Math.max(0, balance(ledger))
  const applied = Math.min(D20_FAIL_PENALTY, current)
  return makeEntry('d20_penalty', -applied, ref)
}
