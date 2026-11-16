import { useState } from 'react'
import type { GameState } from '../engine/types'
import { pack } from '../content/pack'
import { capstoneUnlocked } from '../engine/progress'
import { store } from '../store/gameStore'
import type { CapstoneVerdict } from '../engine/capstone'
import { CAPSTONE_PASS_SCORE } from '../engine/capstone'

interface Props {
  gs: GameState
  onCert: () => void
}

export function CapstoneView(props: Props): JSX.Element {
  const { gs } = props
  const open = capstoneUnlocked(pack, gs)
  const cap = pack.capstone
  const [scores, setScores] = useState<Record<string, number>>({})
  const [essay, setEssay] = useState('')
  const [verdict, setVerdict] = useState<CapstoneVerdict | null>(null)

  if (!open) {
    return (
      <section>
        <h2 className="section-title">★ Capstone: a banca final</h2>
        <p className="locked-note">
          Portão fechado: o Capstone abre apenas com os 7 reinos completos. Volte ao mapa e feche as missões pendentes.
        </p>
      </section>
    )
  }

  function submit(): void {
    const v = store.submitCapstone(cap, scores, essay)
    setVerdict(v)
  }

  const passed = verdict?.passed ?? false
  const alreadyPassed = gs.capstone?.passed ?? false

  return (
    <section>
      <h2 className="section-title">★ Capstone: a banca final</h2>
      <p className="section-sub">
        8 competências pesadas por rubrica JEV (Score 0..4) + dissertação de arquitetura. Aprovado com nota final ≥{' '}
        {CAPSTONE_PASS_SCORE} e nenhuma competência abaixo de 0.50. O juiz é determinístico.
      </p>

      {(alreadyPassed || passed) && (
        <div className="panel ok">
          <h3>Nota aprovada: {(gs.capstone?.finalScore ?? verdict?.finalScore ?? 0).toFixed(2)} / 1.00</h3>
          <p>Vá até a aba do Certificado para emitir o PDF com hash de evidências.</p>
          <button className="btn" onClick={props.onCert}>Ir ao Certificado</button>
        </div>
      )}

      {cap.tasks.map((t) => (
        <div key={t.id} className="panel rubric">
          <h3>
            {t.competency} <span className="chip">{(t.weight * 100).toFixed(0)}%</span>
          </h3>
          <p className="prompt">{t.prompt}</p>
          <ul className="options">
            {t.options.map((o) => (
              <li key={o.score}>
                <label className={scores[t.id] === o.score ? 'opt pick' : 'opt'}>
                  <input
                    type="radio"
                    name={t.id}
                    value={o.score}
                    checked={scores[t.id] === o.score}
                    onChange={() => setScores((s) => ({ ...s, [t.id]: o.score }))}
                  />
                  <b>Score {o.score}</b> — {o.text}
                </label>
              </li>
            ))}
          </ul>
        </div>
      ))}

      <div className="panel dissertation">
        <h3>Dissertação de arquitetura ({cap.dissertation.minChars}+ caracteres)</h3>
        <p className="prompt">{cap.dissertation.prompt}</p>
        <textarea
          rows={8}
          value={essay}
          onChange={(e) => setEssay(e.target.value)}
          placeholder="Descreva a arquitetura completa: dados, modelo, serviço, observabilidade, riscos e próximos passos com evidência…"
        />
        <p className="muted">{essay.length} / {cap.dissertation.minChars} caracteres</p>
      </div>

      <div className="action-row">
        <button className="btn primary" onClick={submit}>Submeter à banca</button>
      </div>

      {verdict && !verdict.passed && (
        <div className="panel bad">
          <h3>Banca não aprovada nesta submissão</h3>
          <p>Nota final: {verdict.finalScore.toFixed(4)}</p>
          <ul>
            {verdict.failures.map((f, i) => (
              <li key={i}>{f}</li>
            ))}
          </ul>
          <p className="muted">A submissão fica registrada; ajuste as autodeclarações e a dissertação e tente de novo.</p>
        </div>
      )}
    </section>
  )
}
