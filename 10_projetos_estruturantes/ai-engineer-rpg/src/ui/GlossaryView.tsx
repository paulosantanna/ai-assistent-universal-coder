import { useState } from 'react'
import { pack } from '../content/pack'

export function GlossaryView(): JSX.Element {
  const [q, setQ] = useState('')
  const needle = q.trim().toLowerCase()
  const terms = pack.glossary.filter(
    (g) =>
      !needle ||
      g.en.toLowerCase().includes(needle) ||
      g.pt.toLowerCase().includes(needle) ||
      g.def.toLowerCase().includes(needle) ||
      (g.formula ?? '').toLowerCase().includes(needle) ||
      (g.example ?? '').toLowerCase().includes(needle),
  )
  return (
    <section>
      <h2 className="section-title">Dicionário técnico</h2>
      <p className="section-sub">
        Palavras técnicas do ofício com exemplos práticos e fáceis de entender: definição, fórmula central e um exemplo do dia a dia. Os
        mesmos conteúdos aparecem como dica ao passar o mouse nos termos destacados das lições.
      </p>
      <input
        className="search"
        placeholder="filtrar… (ex.: L2, deriva, cosseno, SMOTE, derivada)"
        value={q}
        onChange={(e) => setQ(e.target.value)}
      />
      <div className="gloss-grid">
        {terms.map((g) => (
          <div key={g.id} className="gloss-card">
            <h4>
              {g.en} <em>· {g.pt}</em>
            </h4>
            <p>{g.def}</p>
            {g.formula && <p className="gloss-formula">{g.formula}</p>}
            {g.example && <p className="gloss-example">Exemplo: {g.example}</p>}
          </div>
        ))}
        {terms.length === 0 && <p className="muted">Nada encontrado: ajuste o filtro.</p>}
      </div>
    </section>
  )
}
