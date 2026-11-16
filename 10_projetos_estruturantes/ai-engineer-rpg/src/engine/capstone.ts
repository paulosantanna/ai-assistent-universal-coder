// Juiz determinístico do Capstone — peso JEV por competência (composite scoring:
// pesos fixados em código; scores atômicos 0..4 normalized/4). Stake Critical do
// modulo 11 de confiança (>= 0.95 humano) se reflete na nota mínima conservadora.

import type { Capstone, GameState } from './types'

export const CAPSTONE_PASS_SCORE = 0.85
export const CAPSTONE_MIN_COMP = 0.5
export const SCORE_MAX = 4

export interface CapstoneVerdict {
  compScores: Record<string, number>
  finalScore: number
  passed: boolean
  failures: string[]
}

export function validateCapstoneShape(cap: Capstone): string[] {
  const errors: string[] = []
  if (cap.tasks.length !== 8) errors.push(`capstone deve ter 8 tarefas (tem ${cap.tasks.length})`)
  const total = cap.tasks.reduce((s, t) => s + t.weight, 0)
  if (Math.abs(total - 1) > 1e-6) errors.push(`pesos do capstone somam ${total}, esperado 1.0`)
  cap.tasks.forEach((t) => {
    if (t.weight <= 0) errors.push(`peso invalido em ${t.id}`)
    if (t.options.length < 5) errors.push(`${t.id}: rubrica precisa de 5 niveis Score 0..4 (tem ${t.options.length})`)
    t.options.forEach((o, i) => {
      if (o.score !== i) errors.push(`${t.id}: opção ${i} deve ter Score ${i}`)
    })
  })
  if (cap.dissertation.minChars < 200) errors.push('dissertação precisa de minChars >= 200')
  return errors
}

/** pontua a submissão; falhas de forma viram itens em failures */
export function evaluateCapstone(
  cap: Capstone,
  scores: Record<string, number>,
  dissertation: string,
): CapstoneVerdict {
  const compScores: Record<string, number> = {}
  const failures: string[] = []
  let final = 0

  for (const task of cap.tasks) {
    const s = scores[task.id]
    if (s === undefined || s === null) {
      failures.push(`Competência pendente: ${task.competency} (${task.id})`)
      compScores[task.id] = 0
      continue
    }
    const norm = Math.min(SCORE_MAX, Math.max(0, s)) / SCORE_MAX
    compScores[task.id] = norm
    final += task.weight * norm
    if (norm < CAPSTONE_MIN_COMP) {
      failures.push(`Abaixo do mínimo (0.50): ${task.competency} (${task.id})`)
    }
  }

  // arredonda a 4 casas para que o limite 0.85 seja determinístico em float
  final = Math.round(final * 10000) / 10000
  if (final < CAPSTONE_PASS_SCORE) {
    failures.push(`Nota final ${final.toFixed(4)} < ${CAPSTONE_PASS_SCORE}`)
  }
  if (!dissertation || dissertation.length < cap.dissertation.minChars) {
    failures.push(`Dissertação de arquitetura precisa de >= ${cap.dissertation.minChars} caracteres`)
  }

  return { compScores, finalScore: final, passed: failures.length === 0, failures }
}

export function capstoneFromState(gs: GameState) {
  return gs.capstone
}
