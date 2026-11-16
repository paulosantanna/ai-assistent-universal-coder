import { useMemo, useState } from 'react'
import type { GameState, Mission } from '../engine/types'
import { pack } from '../content/pack'
import { missionById, missionUnlocked, questionState } from '../engine/progress'
import { balance, HINT_COST } from '../engine/economy'
import { store, type D20Outcome } from '../store/gameStore'

interface Props {
  missionId: string
  gs: GameState
  onBack: () => void
}

export function MissionView(props: Props): JSX.Element {
  const { missionId, gs } = props
  const mission = missionById(pack, missionId) as Mission | undefined
  const [chosen, setChosen] = useState<number | null>(null)
  const [d20Banner, setD20Banner] = useState<string | null>(null)
  // revisão: questões corretas desta missão ficam visualizáveis; abre por padrão ao entrar numa missão já completa
  const [reviewOpen, setReviewOpen] = useState(
    () => !!mission && mission.questionIds.length > 0 && mission.questionIds.every((qid) => questionState(gs, qid).status === 'correct'),
  )
  const realm = useMemo(() => pack.realms.find((r) => r.missions.some((m) => m.id === missionId)), [missionId])

  if (!mission || !realm) {
    return <section><p>Missão não encontrada.</p><button className="btn" onClick={props.onBack}>Voltar ao mapa</button></section>
  }
  if (!missionUnlocked(pack, gs, realm, mission)) {
    return (
      <section>
        <p className="locked-note">Portão fechado: complete as missões anteriores deste reino.</p>
        <button className="btn" onClick={props.onBack}>Voltar ao mapa</button>
      </section>
    )
  }

  const lesson = realm.lessons.find((l) => l.id === mission.lessonId)
  const glos = (id: string) => pack.glossary.find((g) => g.id === id)
  const doneMask = mission.questionIds.map((qid) => questionState(gs, qid).status === 'correct')
  const curIdx = doneMask.findIndex((d) => !d)
  const curQid = curIdx === -1 ? null : mission.questionIds[curIdx]
  const curQ = curQid ? (realm.questions ?? []).find((q) => q.id === curQid) : undefined
  const qsState = curQid ? questionState(gs, curQid) : null
  const answeredQids = mission.questionIds.filter((_, i) => doneMask[i])
  const bal = balance(gs.ledger)
  const allDone = curIdx === -1

  function choose(i: number): void {
    if (!curQ || wrongLocked) return
    setChosen(i)
  }
  function submit(): void {
    if (curQ && curQid && chosen !== null) store.answerQuestion(curQid, chosen, curQ.correct)
    setChosen(null)
  }
  function roll(): void {
    if (!curQid) return
    const out: D20Outcome | null = store.rollD20(curQid)
    if (!out) return
    setD20Banner(
      out.success
        ? `⚄ D20 = ${out.roll} — 15 ou mais! A questão ficou marcada como correta (selo D20, +20).`
        : `⚄ D20 = ${out.roll} — abaixo de 15: a mesa cobra 10 pontos (saldo nunca fica negativo).`,
    )
  }

  const justAnswered = qsState?.status === 'correct' && chosen === null
  const wrongLocked = chosen !== null && curQ !== undefined && chosen !== curQ.correct

  return (
    <section className="mission">
      <button className="mini" onClick={props.onBack}>← Voltar ao mapa</button>
      <h2 className="section-title">
        {mission.kind === 'boss' ? '☠ ' : '⚔ '}
        {mission.title}
        <span className="chip realm-chip">{realm.name}</span>
      </h2>

      {lesson && (
        <article className="lesson">
          <h3>{lesson.title}</h3>
          {lesson.body.map((p, i) => (
            <p key={i}>{p}</p>
          ))}
          <div className="terms">
            {lesson.terms.map((t) => {
              const g = glos(t)
              if (!g) return null
              return (
                <span key={g.id} className="term" tabIndex={0}>
                  {g.en} <em>· {g.pt}</em>
                  <span className="tip-card" role="tooltip">
                    <h5>{g.en} · {g.pt}</h5>
                    <p>{g.def}</p>
                    {g.formula && <p className="tip-formula">{g.formula}</p>}
                    {g.example && <p className="tip-example">Exemplo: {g.example}</p>}
                  </span>
                </span>
              )
            })}
          </div>
          <p className="muted">Passe o mouse (ou o foco) sobre um termo para ver definição, fórmula e exemplo prático.</p>
        </article>
      )}

      <div className="q-track">
        {mission.questionIds.map((qid, i) => (
          <span key={qid} className={doneMask[i] ? 'dot done' : i === curIdx ? 'dot cur' : 'dot'} />
        ))}
      </div>

      {answeredQids.length > 0 && (
        <div className="action-row">
          <span className="muted">✅ Respondidas nesta missão: {answeredQids.length} de {mission.questionIds.length}</span>
          <button className="mini" onClick={() => setReviewOpen(!reviewOpen)}>
            {reviewOpen ? 'Esconder revisão' : 'Ver revisão'}
          </button>
        </div>
      )}
      {reviewOpen &&
        mission.questionIds.map((qid, qi) => {
          if (!doneMask[qi]) return null
          const q = (realm.questions ?? []).find((x) => x.id === qid)
          if (!q) return null
          const qst = questionState(gs, qid)
          return (
            <div key={qid} className="panel question">
              <h3>
                ✅ Questão {qi + 1}
                <span className="chip realm-chip">{qst.via === 'd20' ? 'selo D20' : 'via acerto'}</span>
              </h3>
              <p className="prompt">{q.prompt}</p>
              <ul className="options">
                {q.options.map((opt, oi) => (
                  <li key={oi}>
                    <button className={oi === q.correct ? 'opt good reveal' : 'opt'} disabled>
                      <b>{'ABCD'[oi]}</b> {opt}
                    </button>
                  </li>
                ))}
              </ul>
              {qst.hintBought && <span className="hint-box">💡 Dica: {q.hint}</span>}
              <div className="panel ok"><p>{q.explanation}</p></div>
            </div>
          )
        })}

      {allDone ? (
        <div className="panel ok">
          <h3>Missão completa! ✦</h3>
          <p>Todas as questões marcadas corretas. Volte ao mapa e siga para a próxima parada.</p>
          <button className="btn" onClick={props.onBack}>Voltar ao mapa</button>
        </div>
      ) : curQ && qsState ? (
        <div className="panel question">
          <h3>Questão {curIdx + 1} de {mission.questionIds.length}</h3>
          <p className="prompt">{curQ.prompt}</p>
          <ul className="options">
            {curQ.options.map((opt, i) => {
              const isCorrect = i === curQ.correct
              const pick = chosen === i
              const cls =
                justAnswered && isCorrect
                  ? 'opt good reveal'
                  : pick && wrongLocked
                    ? 'opt bad'
                    : pick
                      ? 'opt pick'
                      : 'opt'
              return (
                <li key={i}>
                  <button className={cls} onClick={() => choose(i)} disabled={wrongLocked || justAnswered}>
                    <b>{'ABCD'[i]}</b> {opt}
                  </button>
                </li>
              )
            })}
          </ul>

          {justAnswered ? (
            <div className="panel ok">
              <p>{curQ.explanation}</p>
              <p className="plus">+20 ◈ pago pela mesa</p>
            </div>
          ) : wrongLocked ? (
            <div className="panel bad">
              <p>Tentativa diferente da esperada. Passe novamente: respostas erradas não penalizam.</p>
              <button className="btn" onClick={() => setChosen(null)}>Tentar de novo</button>
            </div>
          ) : (
            <>
              <div className="action-row">
                <button className="btn" onClick={submit} disabled={chosen === null}>
                  Responder
                </button>
                {qsState.hintBought ? (
                  <span className="hint-box">💡 Dica: {curQ.hint}</span>
                ) : (
                  <button className="mini" onClick={() => store.buyHint(curQid!)} disabled={bal < HINT_COST}>
                    💡 Comprar dica ({HINT_COST})
                  </button>
                )}
              </div>
              {d20Banner && <p className="d20-banner">{d20Banner}</p>}
              {!qsState.hintBought && (
                <div className="d20-row">
                  {bal < HINT_COST && !qsState.d20Used && (
                    <button className="btn d20" onClick={roll}>
                      ⚄ Rolar D20 (saldo {"<"} 100)
                    </button>
                  )}
                  {!qsState.d20Used && bal >= HINT_COST && <p className="muted">O D20 só entra em jogo quando o saldo fica abaixo de {HINT_COST}.</p>}
                  {qsState.d20Used && <p className="muted">Jogada do D20 já usada nesta questão.</p>}
                </div>
              )}
            </>
          )}
        </div>
      ) : null}
    </section>
  )
}
