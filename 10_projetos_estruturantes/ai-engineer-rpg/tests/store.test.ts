import { describe, expect, it } from 'vitest'
import { GameStore } from '../src/store/gameStore'
import type { Die } from '../src/engine/d20'
import type { GameState } from '../src/engine/types'
import { pack } from '../src/content/pack'
import { balance } from '../src/engine/economy'

function fixedDie(...rolls: number[]): Die {
  let i = 0
  return { roll20: () => rolls[Math.min(i += 1, rolls.length) - 1] ?? rolls[rolls.length - 1] }
}

const m0 = pack.realms[0].missions[0]
const [q1] = m0.questionIds

describe('store: economia nas questões', () => {
  it('resposta certa paga +20; errada não altera o ledger', () => {
    const store = new GameStore()
    const before = store.getState().ledger.length
    store.answerQuestion(q1, 9, 0) // errado (índice inexistente)
    expect(store.getState().ledger.length).toBe(before)
    store.answerQuestion(q1, 0, 0) // certo
    expect(balance(store.getState().ledger)).toBe(20)
    expect(store.getState().questions[q1].via).toBe('answer')
  })

  it('dica custa 100: precisa acumular, compra deixa 0', () => {
    const store = new GameStore()
    const q2 = m0.questionIds[1]
    for (let k = 0; k < 5; k += 1) store.answerQuestion(`pad-${k}`, 0, 0) // +100 de outras? não: qids aleatórios distintos
    expect(balance(store.getState().ledger)).toBe(100)
    store.buyHint(q2)
    expect(store.getState().questions[q2].hintBought).toBe(true)
    expect(balance(store.getState().ledger)).toBe(0)
    store.buyHint(q2) // repetida: nada muda
    expect(balance(store.getState().ledger)).toBe(0)
  })

  it('dica só com saldo >= 100: bloqueia abaixo', () => {
    const store = new GameStore()
    store.buyHint('qualquer') // saldo 0: negado
    expect(store.getState().questions['qualquer']?.hintBought ?? false).toBe(false)
  })
})

describe('store: D20 (uma tentativa por questão, saldo < 100)', () => {
  it('com saldo >= 100 a rolagem é negada', () => {
    const store = new GameStore(fixedDie(20))
    store.answerQuestion('outro', 0, 0) // +20 não alcança 100; mas força: injeta entradas
    for (let k = 0; k < 5; k += 1) store.answerQuestion(`pad-${k}`, 0, 0)
    expect(store.rollD20(q1)).toBeNull()
  })

  it('rolagem 20 marca correta via d20 e paga +20', () => {
    const store = new GameStore(fixedDie(20))
    const out = store.rollD20(q1)
    expect(out).toEqual({ roll: 20, success: true })
    expect(store.getState().questions[q1].via).toBe('d20')
    expect(balance(store.getState().ledger)).toBe(20)
  })

  it('rolagem 5 não penaliza saldo vazio e consome a tentativa', () => {
    const store = new GameStore(fixedDie(5))
    const out = store.rollD20(q1)
    expect(out).toEqual({ roll: 5, success: false })
    expect(balance(store.getState().ledger)).toBe(0)
    expect(store.getState().questions[q1].status).toBe('open')
    // segunda tentativa: bloqueada (uma por questão)
    expect(store.rollD20(q1)).toBeNull()
  })

  it('clamp do desconto: as três falhas registram penalidade com clamp em 0', () => {
    const store = new GameStore(fixedDie(3))
    store.answerQuestion('w1', 0, 0) // +20: saldo alimentado por questão separada
    store.rollD20('r1') // fail: saldo 20 -> 10
    store.rollD20('r2') // fail: saldo 10 -> 0
    store.rollD20('r3') // fail com saldo 0: penalidade -0 registrada (clamp)
    expect(balance(store.getState().ledger)).toBe(0)
    const penalties = store.getState().ledger.filter((e) => e.kind === 'd20_penalty')
    expect(penalties).toHaveLength(3)
    expect(penalties.reduce((s, e) => s + e.delta, 0)).toBe(-20)
  })
})

describe('store: capstone e certificado', () => {
  it('submissão registrada com nota e pass; reprovação igualmente registrada', () => {
    const store = new GameStore()
    const scores: Record<string, number> = {}
    for (const t of pack.capstone.tasks) scores[t.id] = 2
    const v = store.submitCapstone(pack.capstone, scores, '')
    expect(v.passed).toBe(false)
    expect(store.getState().capstone?.finalScore).toBe(v.finalScore)
  })

  it('emite certificado após trilha completa + capstone aprovado', async () => {
    const store = new GameStore(fixedDie(20))
    for (const realm of pack.realms) {
      for (const m of realm.missions) for (const qid of m.questionIds) store.answerQuestion(qid, 0, 0)
    }
    const scores: Record<string, number> = {}
    for (const t of pack.capstone.tasks) scores[t.id] = 4
    const dissertation = 'a'.repeat(400)
    const verdict = store.submitCapstone(pack.capstone, scores, dissertation)
    expect(verdict.passed).toBe(true)
    store.setName('Mesa Notável')
    const ok = await store.issueCertificate(pack)
    expect(ok).toBe(true)
    const cert = store.getState().certificate
    expect(cert).not.toBeNull()
    expect(cert!.code).toMatch(/^AIE-\d{4}-[0-9A-F]{8}$/)
  })

  it('import/export roundtrip preserva o estado', () => {
    const store = new GameStore()
    store.answerQuestion(q1, 0, 0)
    const text = store.exportJson()
    const clone = new GameStore()
    expect(clone.importJson(text)).toBe(true)
    expect(clone.getState().questions[q1].status).toBe('correct')
    expect(balance(clone.getState().ledger)).toBe(20)
    expect(clone.importJson('{nada')).toBe(false)
  })

  it('reset volta ao estado vazio', () => {
    const store = new GameStore()
    store.answerQuestion(q1, 0, 0)
    store.reset()
    const gs: GameState = store.getState()
    expect(gs.ledger).toHaveLength(0)
    expect(Object.keys(gs.questions)).toHaveLength(0)
  })
})
