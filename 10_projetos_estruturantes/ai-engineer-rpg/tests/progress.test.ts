import { describe, expect, it } from 'vitest'
import { pack } from '../src/content/pack'
import { emptyGameState, type GameState } from '../src/engine/types'
import {
  capstoneUnlocked,
  heroTier,
  missionComplete,
  missionUnlocked,
  realmComplete,
  realmUnlocked,
} from '../src/engine/progress'

function stateWithCorrect(...qids: string[]): GameState {
  const gs = emptyGameState()
  for (const qid of qids) gs.questions[qid] = { status: 'correct', via: 'answer', hintBought: false, d20Used: false }
  return gs
}

function correctAllRealm(index: number): string[] {
  const realm = pack.realms[index]
  return realm.missions.flatMap((m) => m.questionIds)
}

describe('cadeia de destravamento: reino n precisa do reino n-1 completo', () => {
  it('reino 0 sempre aberto; reino 1 fechado sem reino 0', () => {
    const gs = stateWithCorrect()
    expect(realmUnlocked(pack, gs, pack.realms[0])).toBe(true)
    expect(realmUnlocked(pack, gs, pack.realms[1])).toBe(false)
  })
  it('completar todas as missões do reino 0 abre o reino 1', () => {
    const gs = stateWithCorrect(...correctAllRealm(0))
    expect(realmComplete(pack, gs, pack.realms[0])).toBe(true)
    expect(realmUnlocked(pack, gs, pack.realms[1])).toBe(true)
    expect(realmUnlocked(pack, gs, pack.realms[2])).toBe(false)
  })
  it('missão é linear: m2 exige m1 completa', () => {
    const realm = pack.realms[0]
    const [m1, m2] = realm.missions
    const gsPartial = stateWithCorrect(...m1.questionIds.slice(0, 2))
    expect(missionUnlocked(pack, gsPartial, realm, m1)).toBe(true)
    expect(missionUnlocked(pack, gsPartial, realm, m2)).toBe(false)
    const gsFull = stateWithCorrect(...m1.questionIds)
    expect(missionComplete(pack, gsFull, m1)).toBe(true)
    expect(missionUnlocked(pack, gsFull, realm, m2)).toBe(true)
  })
  it('capstone requiere todos os 7 reinos', () => {
    let gs = stateWithCorrect()
    expect(capstoneUnlocked(pack, gs)).toBe(false)
    for (let i = 6; i >= 0; i -= 1) {
      gs = stateWithCorrect(...correctAllRealm(i), ...Object.keys(gs.questions).filter((q) => gs.questions[q].status === 'correct'))
    }
    expect(capstoneUnlocked(pack, gs)).toBe(true)
  })
})

describe('níveis do herói', () => {
  it('regras dos degraus do XP', () => {
    expect(heroTier(0)).toBe('Novato do Tabuleiro')
    expect(heroTier(199)).toBe('Novato do Tabuleiro')
    expect(heroTier(200)).toBe('Aprendiz de Dados')
    expect(heroTier(999)).toBe('Artesão dos Modelos')
    expect(heroTier(1400)).toBe('Examinando do Capstone')
  })
})
