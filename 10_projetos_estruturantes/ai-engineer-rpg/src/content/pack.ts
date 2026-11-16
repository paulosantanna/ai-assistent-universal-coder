import type { ContentPack, ContentRealm, Question } from '../engine/types'
import { realm0 } from './realms/realm0'
import { realm1 } from './realms/realm1'
import { realm2 } from './realms/realm2'
import { realm3 } from './realms/realm3'
import { realm4 } from './realms/realm4'
import { realm5 } from './realms/realm5'
import { realm6 } from './realms/realm6'
import { capstone } from './capstone'
import { glossary } from './glossary'

export const pack: ContentPack = {
  version: '1.2.0',
  organ: 'Guilda da Trilha — RPG da Formação em IA',
  realms: [realm0, realm1, realm2, realm3, realm4, realm5, realm6],
  capstone,
  glossary,
}

export function allQuestions(): Array<Question & { realmId: string }> {
  const out: Array<Question & { realmId: string }> = []
  for (const r of pack.realms) {
    for (const q of (r as ContentRealm).questions) out.push({ ...q, realmId: r.id })
  }
  return out
}

const questionIndex: Map<string, Question> = new Map(
  pack.realms.flatMap((r) => (r as ContentRealm).questions.map((q) => [q.id, q] as const)),
)

export function questionById(id: string): Question | undefined {
  return questionIndex.get(id)
}

export function totalQuestions(): number {
  return questionIndex.size
}
