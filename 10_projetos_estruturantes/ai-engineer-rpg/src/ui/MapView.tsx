import type { GameState } from '../engine/types'
import { pack } from '../content/pack'
import { realmProgressList, capstoneUnlocked, missionComplete } from '../engine/progress'
import type { Tab } from '../App'

interface Props {
  gs: GameState
  onTab: (t: Tab) => void
  onSelMission: (missionId: string) => void
}

// coordenadas fixas da trilha 2D (viewBox 1040x260) — um caminho sinuoso de mesa
const NODE_XY: Array<{ x: number; y: number }> = [
  { x: 70, y: 200 },
  { x: 210, y: 110 },
  { x: 350, y: 190 },
  { x: 490, y: 95 },
  { x: 630, y: 185 },
  { x: 770, y: 100 },
  { x: 900, y: 190 },
]

export function MapView(props: Props): JSX.Element {
  const { gs, onSelMission, onTab } = props
  const list = realmProgressList(pack, gs)
  const capFree = capstoneUnlocked(pack, gs)
  const capPass = capFree && !!gs.capstone && gs.capstone.passed

  return (
    <section>
      <h2 className="section-title">Trilha de mesa: 7 Reinos + Capstone</h2>
      <p className="section-sub">
        Complete as missões de cada reino para abrir o próximo. Cada missão paga +20 pontos; dica custa 100; com saldo
        abaixo disso, um D20 pode salvar a questão (15 ou mais = acerto) ou custar 10.
      </p>
      <div className="map-wrap">
        <svg viewBox="0 0 980 250" className="map-svg" role="img" aria-label="Mapa da trilha com 7 reinos e capstone">
          <path
            d="M 70 200 C 140 130 170 110 210 110 C 300 110 300 190 350 190 C 430 190 430 95 490 95 C 560 95 560 185 630 185 C 700 185 710 100 770 100 C 840 100 850 190 900 190 C 930 190 940 80 965 60"
            fill="none"
            stroke="#c8bfa8"
            strokeWidth={5}
            strokeDasharray="1 9"
            strokeLinecap="round"
          />
          {list.map((rp, i) => {
            const { x, y } = NODE_XY[i]
            const cls = rp.complete ? 'node done' : rp.unlocked ? 'node open' : 'node locked'
            return (
              <g key={rp.realm.id} className={cls} transform={`translate(${x} ${y})`}>
                <circle r={30} />
                <text y={-42} textAnchor="middle" className="node-idx">
                  R{i}
                </text>
                <text y={4} textAnchor="middle" className="node-status">
                  {rp.complete ? '✓' : rp.unlocked ? `${rp.missionsDone}/${rp.missionsTotal}` : '🔒'}
                </text>
                <text y={52} textAnchor="middle" className="node-name">
                  {rp.realm.name}
                </text>
                <text y={68} textAnchor="middle" className="node-sub">
                  {rp.unlocked ? `curadoria JEV ${(rp.realm.jevWeight * 100).toFixed(0)}%` : 'fechado'}
                </text>
                {rp.unlocked &&
                  rp.realm.missions.map((m, mi) => {
                    const done = missionComplete(pack, gs, m)
                    return (
                      <g
                        key={m.id}
                        transform={`translate(0 ${90 + mi * 17})`}
                        className="mission-dot"
                        onClick={() => onSelMission(m.id)}
                        role="button"
                        aria-label={m.title}
                      >
                        <circle r={6} className={done ? 'md-done' : 'md-open'} />
                        <text x={10} y={4} className="mission-label">
                          {m.title.length > 26 ? m.title.slice(0, 25) + '…' : m.title}
                        </text>
                      </g>
                    )
                  })}
              </g>
            )
          })}
          <g
            className={capFree ? 'node capstone open' : 'node capstone locked'}
            transform="translate(965 40)"
            role="button"
            onClick={() => capFree && onTab('capstone')}
            aria-label="Capstone"
          >
            <rect x={-26} y={-26} width={52} height={52} rx={10} />
            <text y={-34} textAnchor="middle" className="node-idx">
              ★
            </text>
            <text textAnchor="middle" y={5} className="node-status">
              {capPass ? '✓' : capFree ? 'Capstone' : '—'}
            </text>
            <text y={44} textAnchor="middle" className="node-name">
              Capstone juiz
            </text>
          </g>
        </svg>
      </div>
      <div className="map-cards">
        {list.map((rp) => (
          <div key={rp.realm.id} className={`realm-card ${rp.complete ? 'done' : rp.unlocked ? 'open' : 'locked'}`}>
            <h3>
              R{rp.realm.index} · {rp.realm.name}
            </h3>
            <p className="realm-blurb">{rp.realm.blurb}</p>
            <div className="realm-meta">
              <span className="chip">JEV {(rp.realm.jevWeight * 100).toFixed(0)}%</span>
              <span className="chip">{rp.missionsDone}/{rp.missionsTotal} missões</span>
              <span className="chip">{rp.realm.lessons.length} lições</span>
            </div>
            {rp.unlocked && (
              <div className="mission-list">
                {rp.realm.missions.map((m) => (
                  <button key={m.id} className="mission-btn" onClick={() => onSelMission(m.id)}>
                    {m.kind === 'boss' ? '☠ ' : '⚔ '}{m.title}
                  </button>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </section>
  )
}
