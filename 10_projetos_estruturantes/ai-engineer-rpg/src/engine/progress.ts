// Progressão na trilha 2D: estado derivado do pack (lições/missões/questões) e
// do mapa de questões respondidas. Missões são lineares dentro do reino;
// reinos liberam sequencialmente; capstone exige os 7 reinos completos.

import type { ContentPack, GameState, Mission, QuestionState, Realm } from './types'
import { emptyGameState } from './types'

export function questionState(gs: GameState, qid: string): QuestionState {
  return gs.questions[qid] ?? { status: 'open', hintBought: false, d20Used: false }
}

export function isQuestionCorrect(gs: GameState, qid: string): boolean {
  return questionState(gs, qid).status === 'correct'
}

export function realmById(pack: ContentPack, realmId: string): Realm | undefined {
  return pack.realms.find((r) => r.id === realmId)
}

export function missionById(pack: ContentPack, missionId: string): Mission | undefined {
  for (const r of pack.realms) {
    const m = r.missions.find((x) => x.id === missionId)
    if (m) return m
  }
  return undefined
}

export function missionComplete(_pack: ContentPack, gs: GameState, mission: Mission): boolean {
  return mission.questionIds.every((qid) => isQuestionCorrect(gs, qid))
}

export function realmComplete(pack: ContentPack, gs: GameState, realm: Realm): boolean {
  return realm.missions.every((m) => missionComplete(pack, gs, m))
}

export function realmUnlocked(pack: ContentPack, gs: GameState, realm: Realm): boolean {
  if (realm.index === 0) return true
  const prev = pack.realms.find((r) => r.index === realm.index - 1)
  if (!prev) return true
  return realmComplete(pack, gs, prev)
}

/** missão linear: a primeira do reino abre com o reino; as demais exigem a anterior */
export function missionUnlocked(pack: ContentPack, gs: GameState, realm: Realm, mission: Mission): boolean {
  if (!realmUnlocked(pack, gs, realm)) return false
  const idx = realm.missions.findIndex((m) => m.id === mission.id)
  if (idx <= 0) return true
  return missionComplete(pack, gs, realm.missions[idx - 1])
}

export function capstoneUnlocked(pack: ContentPack, gs: GameState): boolean {
  return pack.realms.every((r) => realmComplete(pack, gs, r))
}

export function certificatesReady(pack: ContentPack, gs: GameState): boolean {
  return !!gs.capstone && gs.capstone.passed && capstoneUnlocked(pack, gs)
}

export interface RealmProgress {
  realm: Realm
  unlocked: boolean
  complete: boolean
  missionsDone: number
  missionsTotal: number
}

export function realmProgressList(pack: ContentPack, gs: GameState): RealmProgress[] {
  return pack.realms.map((realm) => {
    const missionsDone = realm.missions.filter((m) => missionComplete(pack, gs, m)).length
    return {
      realm,
      unlocked: realmUnlocked(pack, gs, realm),
      complete: realmComplete(pack, gs, realm),
      missionsDone,
      missionsTotal: realm.missions.length,
    }
  })
}

// ---------- níveis do herói (XP bruto) ----------

export interface HeroTier {
  min: number
  name: string
}

export const HERO_TIERS: HeroTier[] = [
  { min: 0, name: 'Novato do Tabuleiro' },
  { min: 200, name: 'Aprendiz de Dados' },
  { min: 600, name: 'Artesão dos Modelos' },
  { min: 1000, name: 'Arquiteto de IA' },
  { min: 1400, name: 'Examinando do Capstone' },
]

export function heroTier(xp: number): string {
  let name = HERO_TIERS[0].name
  for (const t of HERO_TIERS) if (xp >= t.min) name = t.name
  return name
}

export function answeredCount(gs: GameState): number {
  return Object.values(gs.questions).filter((q) => q.status === 'correct').length
}

export function emptyProgress(): GameState {
  return emptyGameState()
}
