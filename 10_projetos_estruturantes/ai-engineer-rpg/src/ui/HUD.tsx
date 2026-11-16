import { useRef } from 'react'
import type { Tab } from '../App'

interface Props {
  name: string
  onName: (n: string) => void
  bal: number
  xp: number
  tier: string
  tab: Tab
  onTab: (t: Tab) => void
  onExport: () => void
  onImport: (text: string) => void
  onReset: () => void
}

const TABS: Array<{ id: Tab; label: string }> = [
  { id: 'mapa', label: 'Mapa' },
  { id: 'capstone', label: 'Capstone' },
  { id: 'certificado', label: 'Certificado' },
  { id: 'glossario', label: 'Dicionário' },
  { id: 'guilda', label: 'Guilda (fontes)' },
]

export function HUD(props: Props): JSX.Element {
  const fileRef = useRef<HTMLInputElement>(null)
  return (
    <header className="hud">
      <div className="hud-row">
        <div className="brand">
          <span className="brand-die">⚄</span>
          <div>
            <h1>Engenheira(o) de IA — RPG da Formação</h1>
            <p className="brand-sub">Do zero ao certificado: trilha de mesa, economia de pontos e Capstone juizado</p>
          </div>
        </div>
        <div className="hero-card">
          <label className="name-label">
            Herói:
            <input
              value={props.name}
              onChange={(e) => props.onName(e.target.value)}
              placeholder="seu nome de mesa"
              maxLength={40}
            />
          </label>
          <div className="chips">
            <span className="chip chip-bal" title="Respostas certas valem +20; dica custa 100">
              ◈ {props.bal} pts
            </span>
            <span className="chip chip-xp" title="XP bruto defina o nível do herói">
              ✦ {props.xp} XP · {props.tier}
            </span>
          </div>
        </div>
      </div>
      <nav className="tabs">
        {TABS.map((t) => (
          <button key={t.id} className={t.id === props.tab ? 'tab active' : 'tab'} onClick={() => props.onTab(t.id)}>
            {t.label}
          </button>
        ))}
        <span className="spacer" />
        <button className="mini" onClick={props.onExport}>Exportar</button>
        <button className="mini" onClick={() => fileRef.current?.click()}>Importar</button>
        <button
          className="mini danger"
          onClick={() => {
            if (confirm('Reiniciar progresso? Exporte antes para garantir.')) props.onReset()
          }}
        >
          Zerar
        </button>
        <input
          ref={fileRef}
          type="file"
          accept="application/json"
          hidden
          onChange={(e) => {
            const f = e.target.files?.[0]
            if (!f) return
            void f.text().then(props.onImport)
            e.target.value = ''
          }}
        />
      </nav>
    </header>
  )
}
