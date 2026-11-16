// Validador do ContentPack v1 — o contrato do conteúdo é o one-way door do jogo:
// consumidores (mapa 2D, missões, certificado, curadoria futura) dependem destes campos.

import type { ContentPack, ContentRealm, RealmSource } from './types'

export function validateSource(src: RealmSource): string[] {
  const errs: string[] = []
  if (src.confidence < 0 || src.confidence > 1) errs.push(`${src.id}: confiança fora de 0..1`)
  if (src.confidence < 0.5) errs.push(`${src.id}: confiança < 0.5 é proibida no pack (política JEV)`)
  const auto = src.confidence >= 0.7
  if (auto && src.flag !== 'auto') errs.push(`${src.id}: confiança >= 0.7 deve ser flag auto`)
  if (!auto && src.flag !== 'revisar') errs.push(`${src.id}: confiança 0.5..0.7 deve ser flag revisar`)
  if (!src.checkedAt) errs.push(`${src.id}: checkedAt obrigatório (prova da curadoria)`)
  return errs
}

export interface PackStats {
  realms: number
  lessons: number
  missions: number
  questions: number
  sources: number
  glossary: number
}

export function validateContentPack(pack: ContentPack): { errors: string[]; stats: PackStats } {
  const errors: string[] = []
  const seenIds = new Set<string>()
  const termRefs: Array<{ lessonId: string; termId: string }> = []

  if (!/^1\./.test(pack.version)) errors.push('pack.version deve ser 1.x (schema v1)')
  if (!pack.organ) errors.push('pack.organ obrigatório')
  if (pack.realms.length !== 7) errors.push(`7 reinos obrigatórios (tem ${pack.realms.length})`)

  const weightSum = pack.realms.reduce((s, r) => s + r.jevWeight, 0)
  if (Math.abs(weightSum - 1) > 1e-6) errors.push(`pesos JEV dos reinos somam ${weightSum}, esperado 1.0`)

  const questionPool: Array<{ id: string } & ContentRealm['questions'][number]> = []
  const missionQids: string[] = []

  pack.realms.forEach((realm, i) => {
    if (realm.index !== i) errors.push(`reino ${realm.id}: index ${realm.index} fora de ordem (esperado ${i})`)
    if (realm.blurb.length < 20) errors.push(`reino ${realm.id}: blurb muito curto`)

    const lessonIds = new Set<string>()
    for (const l of realm.lessons) {
      if (seenIds.has(l.id)) errors.push(`id duplicado: ${l.id}`)
      seenIds.add(l.id)
      lessonIds.add(l.id)
      if (l.body.length < 2) errors.push(`lição ${l.id}: corpo deve ter >= 2 parágrafos`)
      for (const t of l.terms) termRefs.push({ lessonId: l.id, termId: t })
    }
    for (const m of realm.missions) {
      if (seenIds.has(m.id)) errors.push(`id duplicado: ${m.id}`)
      seenIds.add(m.id)
      if (!lessonIds.has(m.lessonId)) errors.push(`missão ${m.id}: lessonId ${m.lessonId} fora do reino ${realm.id}`)
      if (m.questionIds.length < 3) errors.push(`missão ${m.id}: >= 3 questões obrigatórias (tem ${m.questionIds.length})`)
      missionQids.push(...m.questionIds)
    }
    for (const s of realm.sources) for (const e of validateSource(s)) errors.push(`[reino ${realm.id}] ${e}`)
    for (const q of realm.questions) {
      questionPool.push(q)
      if (seenIds.has(q.id)) errors.push(`id duplicado: ${q.id}`)
      seenIds.add(q.id)
      if (q.correct < 0 || q.correct >= q.options.length) errors.push(`questão ${q.id}: índice correct fora do range`)
      if (!q.hint || q.hint.length < 8) errors.push(`questão ${q.id}: dica obrigatória >= 8 caracteres`)
      if (q.options.length < 3) errors.push(`questão ${q.id}: >= 3 opções obrigatórias`)
    }
  })

  const qidSet = new Set(questionPool.map((q) => q.id))
  for (const qid of missionQids) {
    if (!qidSet.has(qid)) errors.push(`missão referencia questão inexistente: ${qid}`)
  }
  const missionSet = new Set(missionQids)
  for (const q of questionPool) {
    if (!missionSet.has(q.id)) errors.push(`questão órfã (fora de qualquer missão): ${q.id}`)
  }

  const termIds = new Set(pack.glossary.map((g) => g.id))
  const enSet = new Set(pack.glossary.map((g) => g.en.toLowerCase()))
  if (enSet.size !== pack.glossary.length) errors.push('termos EN duplicados no glossário')
  for (const ref of termRefs) {
    if (!termIds.has(ref.termId)) errors.push(`lição ${ref.lessonId} usa termo inexistente: ${ref.termId}`)
  }

  const capSum = pack.capstone.tasks.reduce((s, t) => s + t.weight, 0)
  if (pack.capstone.tasks.length !== 8) errors.push(`capstone: 8 competências obrigatórias (tem ${pack.capstone.tasks.length})`)
  if (Math.abs(capSum - 1) > 1e-6) errors.push(`pesos do capstone somam ${capSum}, esperado 1.0`)
  if (pack.capstone.dissertation.minChars < 200) errors.push('capstone.dissertation.minChars < 200')

  const lessons = pack.realms.reduce((s, r) => s + r.lessons.length, 0)
  const missions = pack.realms.reduce((s, r) => s + r.missions.length, 0)
  const stats: PackStats = {
    realms: pack.realms.length,
    lessons,
    missions,
    questions: questionPool.length,
    sources: pack.realms.reduce((s, r) => s + r.sources.length, 0),
    glossary: pack.glossary.length,
  }
  if (stats.lessons < 36) errors.push(`mínimo de 36 lições (tem ${stats.lessons})`)
  if (stats.questions < 120) errors.push(`mínimo de 120 questões (tem ${stats.questions})`)

  return { errors, stats }
}
