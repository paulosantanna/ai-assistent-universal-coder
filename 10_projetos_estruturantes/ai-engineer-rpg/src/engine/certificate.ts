// Certificado: hash SHA-256 do dossiê de evidências (door 2 — formato estável) e
// PDF gerado no cliente com pdf-lib. Verificação local: recalcular o hash do
// progresso atual e comparar com o código impresso.

import { PDFDocument, StandardFonts, rgb } from 'pdf-lib'
import type { ContentPack, GameState } from './types'
import { balance, xpEarned } from './economy'
import { answeredCount } from './progress'

/** JSON canônico: chaves ordenadas recursivamente — hash estável entre runs */
export function canonicalJson(value: unknown): string {
  if (value === null || value === undefined) return 'null'
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(',')}]`
  if (typeof value === 'object') {
    const keys = Object.keys(value as Record<string, unknown>).sort()
    const pairs = keys.map((k) => `${JSON.stringify(k)}:${canonicalJson((value as Record<string, unknown>)[k])}`)
    return `{${pairs.join(',')}}`
  }
  return JSON.stringify(value)
}

export async function sha256Hex(text: string): Promise<string> {
  const bytes = new TextEncoder().encode(text)
  const digest = await crypto.subtle.digest('SHA-256', bytes)
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, '0')).join('')
}

export interface EvidenceDossier {
  packVersion: string
  name: string
  issuedAt: string
  finalScore: number
  xp: number
  balanceAtIssue: number
  questionsCorrect: number
  missionsCompleted: string[]
  realmsCompleted: string[]
  ledger: Array<{ kind: string; delta: number; ref: string; at: string }>
  capstone: { scores: Record<string, unknown>; dissertationChars: number }
}

export function buildEvidenceDossier(pack: ContentPack, gs: GameState, issuedAt: string): EvidenceDossier {
  const missionsCompleted: string[] = []
  const realmsCompleted: string[] = []
  for (const realm of pack.realms) {
    let realmDone = true
    for (const m of realm.missions) {
      const done = m.questionIds.every((qid) => gs.questions[qid]?.status === 'correct')
      if (done) missionsCompleted.push(m.id)
      else realmDone = false
    }
    if (realmDone) realmsCompleted.push(realm.id)
  }
  return {
    packVersion: pack.version,
    name: gs.playerName,
    issuedAt,
    finalScore: gs.capstone?.finalScore ?? 0,
    xp: xpEarned(gs.ledger),
    balanceAtIssue: balance(gs.ledger),
    questionsCorrect: answeredCount(gs),
    missionsCompleted,
    realmsCompleted,
    ledger: gs.ledger.map((e) => ({ kind: e.kind, delta: e.delta, ref: e.ref, at: e.at })),
    capstone: {
      scores: (gs.capstone?.scores ?? {}) as Record<string, unknown>,
      dissertationChars: (gs.capstone?.dissertation ?? '').length,
    },
  }
}

export function certCodeFromHash(hash: string, issuedAt: string): string {
  const year = new Date(issuedAt).getFullYear()
  return `AIE-${year}-${hash.slice(0, 8).toUpperCase()}`
}

export async function computeCertificate(pack: ContentPack, gs: GameState) {
  const issuedAt = new Date().toISOString()
  const dossier = buildEvidenceDossier(pack, gs, issuedAt)
  const hash = await sha256Hex(canonicalJson(dossier))
  return { issuedAt, dossier, hash, code: certCodeFromHash(hash, issuedAt) }
}

export interface PdfOptions {
  name: string
  code: string
  hash: string
  score: number
  issuedAt: string
  organ: string
  realms: Array<{ name: string; tier: string }>
  typology: string
}

export async function renderCertificatePdf(o: PdfOptions): Promise<Blob> {
  const doc = await PDFDocument.create()
  const page = doc.addPage()
  const { width, height } = page.getSize()
  const title = await doc.embedFont(StandardFonts.HelveticaBold)
  const body = await doc.embedFont(StandardFonts.Helvetica)

  const ink = rgb(0.13, 0.15, 0.24)
  const accent = rgb(0.29, 0.37, 0.94)

  page.drawRectangle({ x: 24, y: 24, width: width - 48, height: height - 48, borderColor: accent, borderWidth: 2 })
  page.drawRectangle({ x: 30, y: 30, width: width - 60, height: height - 60, borderColor: ink, borderWidth: 0.7 })

  const center = width / 2
  page.drawText('CERTIFICADO DE CONCLUSAO', { x: center - 118, y: height - 90, size: 20, font: title, color: ink })
  page.drawText('RPG da Formacao - Engenheira(o) de IA', { x: center - 92, y: height - 112, size: 11, font: body, color: accent })

  page.drawText('Certificamos que', { x: center - 44, y: height - 155, size: 11, font: body, color: ink })
  page.drawText(o.name.slice(0, 40), { x: center - Math.min(120, o.name.length * 4.2), y: height - 190, size: 20, font: title, color: ink })

  const lines = [
    `concluiu a trilha completa dos 7 Reinos e o Capstone com nota ${o.score.toFixed(2)} / 1.00,`,
    'demonstrando aptidao para conceber arquiteturas de IA (monoliticas ou hibridas), criar do zero,',
    'treinar, manter, melhorar e elevar performance, eficiencia energetica, predicao,',
    'estatistica e acuracia de sistemas de IA em qualquer segmento.',
  ]
  lines.forEach((line, i) => {
    page.drawText(line, { x: 70, y: height - 230 - i * 16, size: 10, font: body, color: ink })
  })

  // selos dos reinos
  const badgeY = height - 320
  o.realms.forEach((r, i) => {
    const col = i % 4
    const row = Math.floor(i / 4)
    const x = 64 + col * 118
    page.drawRectangle({ x, y: badgeY - row * 30, width: 110, height: 22, color: rgb(0.95, 0.96, 1) })
    page.drawText(`${i + 1}. ${r.name.slice(0, 18)}`, { x: x + 5, y: badgeY + 7 - row * 30, size: 7.4, font: body, color: ink })
  })

  page.drawText(`Emitido em: ${o.issuedAt}`, { x: 70, y: 110, size: 9, font: body, color: ink })
  page.drawText(`Organizacao: ${o.organ.slice(0, 45)} | ${o.typology}`, { x: 70, y: 94, size: 9, font: body, color: ink })
  page.drawText(`Codigo verificavel: ${o.code}`, { x: 70, y: 78, size: 11, font: title, color: accent })
  page.drawText(`Hash de evidencias (SHA-256): ${o.hash}`, { x: 70, y: 60, size: 7, font: body, color: ink })
  page.drawText('Verificacao: importar o progresso e recalcular o hash na tela do certificado.', { x: 70, y: 46, size: 7, font: body, color: ink })

  // metadados em texto puro (sem object streams): o código e o hash ficam
  // pesquisáveis no arquivo, permitindo verificação forense byte a byte.
  doc.setTitle('Certificado de Conclusao - RPG da Formacao em IA')
  doc.setSubject(`Hash de evidencias SHA-256: ${o.hash}`)
  doc.setKeywords([o.code, `AIE-${new Date(o.issuedAt).getFullYear()}`])
  doc.setProducer('ai-engineer-rpg')
  doc.setCreator('ai-engineer-rpg v1')

  const bytes = await doc.save({ useObjectStreams: false })
  return new Blob([new Uint8Array(bytes)], { type: 'application/pdf' })
}
