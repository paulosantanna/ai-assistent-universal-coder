// Store do jogo: fonte única de verdade observable. Regras puras moram no engine;
// o store apenas orquestra ações do usuário e persistência. Die injetável para testes.

import { useSyncExternalStore } from 'react'
import {
  balance,
  entryCorrect,
  entryD20Penalty,
  entryD20Win,
  entryHint,
  canBuyHint,
  canRollD20,
  xpEarned,
} from '../engine/economy'
import type { Die } from '../engine/d20'
import { browserRng, isD20Success } from '../engine/d20'
import { emptyGameState, type Capstone, type GameState } from '../engine/types'
import { capstoneUnlocked } from '../engine/progress'
import { evaluateCapstone, type CapstoneVerdict } from '../engine/capstone'
import { computeCertificate } from '../engine/certificate'
import { loadProgress, normalizeProgress, saveProgress, exportProgressJson, STORAGE_KEY } from '../engine/persistence'
import type { ContentPack } from '../engine/types'

export interface D20Outcome {
  roll: number
  success: boolean
}

export class GameStore {
  private state: GameState
  private listeners = new Set<() => void>()
  private die: Die

  constructor(die: Die = browserRng, initial: GameState | null = null) {
    this.die = die
    this.state = initial ?? emptyGameState()
  }

  getState = (): GameState => this.state

  subscribe = (cb: () => void): (() => void) => {
    this.listeners.add(cb)
    return () => {
      this.listeners.delete(cb)
    }
  }

  private set(next: GameState): void {
    this.state = next
    for (const l of this.listeners) l()
    void saveProgress(next)
  }

  private patch(fn: (draft: GameState) => void): void {
    const next: GameState = JSON.parse(JSON.stringify(this.state)) as GameState
    fn(next)
    this.set(next)
  }

  /** carrega progresso salvo (IndexedDB/localStorage) sem gravar de volta */
  async hydrate(): Promise<void> {
    const loaded = await loadProgress()
    if (loaded) {
      this.state = loaded
      for (const l of this.listeners) l()
    }
  }

  setName(name: string): void {
    this.patch((d) => {
      d.playerName = name
    })
  }

  /** resposta certa soma +20; resposta errada não penaliza (regra A4 do plano) */
  answerQuestion(qid: string, optIndex: number, correctIndex: number): void {
    const qs = this.state.questions[qid] ?? { status: 'open', hintBought: false, d20Used: false }
    if (qs.status === 'correct') return
    if (optIndex !== correctIndex) return
    this.patch((d) => {
      d.questions[qid] = { status: 'correct', via: 'answer', hintBought: qs.hintBought, d20Used: qs.d20Used }
      d.ledger.push(entryCorrect(qid))
    })
  }

  /** dica custa 100 pontos; só com saldo suficiente */
  buyHint(qid: string): void {
    if (!canBuyHint(this.state.ledger)) return
    const qs = this.state.questions[qid] ?? { status: 'open', hintBought: false, d20Used: false }
    if (qs.hintBought) return
    this.patch((d) => {
      d.questions[qid] = { ...qs, hintBought: true }
      d.ledger.push(entryHint(qid))
    })
  }

  /** D20: apenas 1 tentativa por questão, disponível somente com saldo < 100 */
  rollD20(qid: string): D20Outcome | null {
    const qs = this.state.questions[qid] ?? { status: 'open', hintBought: false, d20Used: false }
    if (qs.status === 'correct' || qs.d20Used) return null
    if (!canRollD20(this.state.ledger)) return null
    const roll = this.die.roll20()
    if (isD20Success(roll)) {
      this.patch((d) => {
        d.questions[qid] = { status: 'correct', via: 'd20', hintBought: qs.hintBought, d20Used: true }
        d.ledger.push(entryD20Win(qid))
      })
      return { roll, success: true }
    }
    this.patch((d) => {
      d.questions[qid] = { ...qs, d20Used: true }
      d.ledger.push(entryD20Penalty(this.getState().ledger, qid))
    })
    return { roll, success: false }
  }

  submitCapstone(cap: Capstone, scores: Record<string, number>, dissertation: string): CapstoneVerdict {
    const verdict = evaluateCapstone(cap, scores, dissertation)
    this.patch((d) => {
      d.capstone = {
        scores,
        essays: {},
        dissertation,
        finalScore: verdict.finalScore,
        compScores: verdict.compScores,
        passed: verdict.passed,
      }
    })
    return verdict
  }

  /** certificado: exige capstone aprovado e todos os reinos completos */
  async issueCertificate(pack: ContentPack): Promise<boolean> {
    const gs = this.state
    if (!gs.capstone || !gs.capstone.passed) return false
    if (!capstoneUnlocked(pack, gs)) return false
    const { issuedAt, hash, code } = await computeCertificate(pack, gs)
    this.patch((d) => {
      d.certificate = { code, hash, issuedAt, score: gs.capstone!.finalScore, name: gs.playerName || 'Examinando' }
    })
    return true
  }

  exportJson(): string {
    return exportProgressJson(this.state)
  }

  importJson(text: string): boolean {
    try {
      const parsed = normalizeProgress(JSON.parse(text))
      this.set(parsed)
      return true
    } catch {
      return false
    }
  }

  reset(): void {
    this.set(emptyGameState())
  }
}

export const storageKey = STORAGE_KEY

// instância singleton para a UI; testes instanciam a classe direto
export const store = new GameStore()

export function useGameState(): GameState {
  return useSyncExternalStore(store.subscribe, store.getState)
}

export { balance, xpEarned }
