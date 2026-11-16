import { pack } from '../content/pack'

const kindLabel: Record<string, string> = {
  book: 'livro',
  course: 'curso',
  docs: 'documentação',
  paper: 'paper',
  cookbook: 'cookbook',
}

export function GuildaView(): JSX.Element {
  return (
    <section>
      <h2 className="section-title">Guilda: fontes com selo JEV</h2>
      <p className="section-sub">
        Curação JEV: presença ≥ 0.7 selo <b>auto</b>; entre 0.5 e 0.7 selo <b>revisar</b> (pode ser usada, mas exige
        revalidação); abaixo de 0.5 é proibida no pack. checkedAt prova a data da verificação.
      </p>
      {pack.realms.map((r) => (
        <div key={r.id} className="panel guild-panel">
          <h3>
            R{r.index} · {r.name} <span className="chip">peso JEV {(r.jevWeight * 100).toFixed(0)}%</span>
          </h3>
          <ul className="sources">
            {r.sources.map((s) => (
              <li key={s.id}>
                <div className="src-head">
                  <a href={s.url} target="_blank" rel="noreferrer">{s.title}</a>
                  <span className={`flag ${s.flag === 'auto' ? 'auto' : 'revisar'}`}>
                    {s.flag === 'auto' ? 'auto ≥ 0.7' : 'revisar 0.5–0.7'} · {s.confidence.toFixed(2)}
                  </span>
                </div>
                <p className="src-meta">
                  {kindLabel[s.kind]} · conferido em {s.checkedAt}
                  {s.note ? ` — ${s.note}` : ''}
                </p>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </section>
  )
}
