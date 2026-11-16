// Persistência local do progresso (door 3 do spec): IndexedDB via idb-keyval com
// espelho em localStorage. Exporta/importa JSON para backup do jogador.

import { get, set } from 'idb-keyval'
import { emptyGameState, type GameState } from './types'

export const STORAGE_KEY = 'aierpg/progress/v1'

export async function loadProgress(): Promise<GameState | null> {
  let raw: unknown = null
  try {
    raw = (await get(STORAGE_KEY)) ?? null
  } catch {
    raw = null
  }
  if (raw === null && typeof localStorage !== 'undefined') {
    try {
      const text = localStorage.getItem(STORAGE_KEY)
      raw = text ? JSON.parse(text) : null
    } catch {
      raw = null
    }
  }
  if (raw === null) return null
  try {
    return normalizeProgress(raw)
  } catch {
    return null
  }
}

export async function saveProgress(state: GameState): Promise<void> {
  const payload = JSON.parse(JSON.stringify(state)) as GameState
  try {
    await set(STORAGE_KEY, payload)
  } catch {
    // Indisponibilidade de IDB não deve abortar o jogo; o espelho cobre.
  }
  if (typeof localStorage !== 'undefined') {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(payload))
    } catch {
      // quota cheia: o jogador usa export/import manual
    }
  }
}

/** valida e normaliza a forma do estado (importação e leitura) */
export function normalizeProgress(raw: unknown): GameState {
  if (typeof raw !== 'object' || raw === null) throw new Error('Progresso inválido: não é objeto')
  const r = raw as Record<string, unknown>
  if (r.version !== 1) throw new Error(`Progresso de versão incompatível: ${String(r.version)}`)
  const gs = emptyGameState()
  gs.playerName = typeof r.playerName === 'string' ? r.playerName : ''
  if (Array.isArray(r.ledger)) {
    gs.ledger = (r.ledger as GameState['ledger']).filter(
      (e) => e && typeof e.id === 'string' && typeof e.delta === 'number',
    )
  }
  if (typeof r.questions === 'object' && r.questions !== null) {
    for (const [qid, qs] of Object.entries(r.questions as Record<string, unknown>)) {
      const o = qs as Record<string, unknown>
      gs.questions[qid] = {
        status: o.status === 'correct' ? 'correct' : 'open',
        via: o.via === 'd20' ? 'd20' : o.via === 'answer' ? 'answer' : undefined,
        hintBought: o.hintBought === true,
        d20Used: o.d20Used === true,
      }
    }
  }
  if (typeof r.capstone === 'object' && r.capstone !== null) {
    const c = r.capstone as Record<string, unknown>
    gs.capstone = {
      scores: (c.scores as Record<string, number>) ?? {},
      essays: (c.essays as Record<string, string>) ?? {},
      dissertation: typeof c.dissertation === 'string' ? c.dissertation : '',
      finalScore: typeof c.finalScore === 'number' ? c.finalScore : 0,
      compScores: (c.compScores as Record<string, number>) ?? {},
      passed: c.passed === true,
    }
  }
  if (typeof r.certificate === 'object' && r.certificate !== null) {
    const c = r.certificate as Record<string, unknown>
    gs.certificate = {
      code: String(c.code ?? ''),
      hash: String(c.hash ?? ''),
      issuedAt: String(c.issuedAt ?? ''),
      score: typeof c.score === 'number' ? c.score : 0,
      name: String(c.name ?? ''),
    }
  }
  return gs
}

export function exportProgressJson(state: GameState): string {
  return JSON.stringify({ ...state, exportedAt: new Date().toISOString() }, null, 2)
}
