import { useCallback, useEffect, useState } from 'react'
import { store, useGameState } from './store/gameStore'
import { pack } from './content/pack'
import { realmProgressList, missionById } from './engine/progress'
import { balance, xpEarned } from './engine/economy'
import { heroTier } from './engine/progress'
import { HUD } from './ui/HUD'
import { MapView } from './ui/MapView'
import { MissionView } from './ui/MissionView'
import { CapstoneView } from './ui/CapstoneView'
import { CertificateView } from './ui/CertificateView'
import { GlossaryView } from './ui/GlossaryView'
import { GuildaView } from './ui/GuildaView'

export type Tab = 'mapa' | 'missao' | 'capstone' | 'certificado' | 'glossario' | 'guilda'

interface Selection {
  missionId: string
}

export default function App(): JSX.Element {
  const gs = useGameState()
  const [tab, setTab] = useState<Tab>('mapa')
  const [sel, setSel] = useState<Selection | null>(null)
  const [ready, setReady] = useState(false)

  useEffect(() => {
    void store.hydrate().then(() => setReady(true))
  }, [])

  const openMission = useCallback((missionId: string) => {
    setSel({ missionId })
    setTab('missao')
  }, [])

  if (!ready) return <div className="loading">Preparando a mesa…</div>

  const mission = sel ? missionById(pack, sel.missionId) : undefined

  return (
    <div className="frame">
      <HUD
        name={gs.playerName}
        onName={(n) => store.setName(n)}
        bal={balance(gs.ledger)}
        xp={xpEarned(gs.ledger)}
        tier={heroTier(xpEarned(gs.ledger))}
        tab={tab}
        onTab={setTab}
        onExport={() => {
          const blob = new Blob([store.exportJson()], { type: 'application/json' })
          const a = document.createElement('a')
          a.href = URL.createObjectURL(blob)
          a.download = 'progresso-aie.json'
          a.click()
          URL.revokeObjectURL(a.href)
        }}
        onImport={(text) => store.importJson(text)}
        onReset={() => store.reset()}
      />
      <main className="board">
        {tab === 'mapa' && <MapView gs={gs} onTab={setTab} onSelMission={openMission} />}
        {tab === 'missao' && mission && <MissionView missionId={mission.id} gs={gs} onBack={() => setTab('mapa')} />}
        {tab === 'missao' && !mission && <MapView gs={gs} onTab={setTab} onSelMission={openMission} />}
        {tab === 'capstone' && <CapstoneView gs={gs} onCert={() => setTab('certificado')} />}
        {tab === 'certificado' && <CertificateView gs={gs} />}
        {tab === 'glossario' && <GlossaryView />}
        {tab === 'guilda' && <GuildaView />}
      </main>
      <footer className="corner-note">
        Reinos: {realmProgressList(pack, gs).filter((r) => r.complete).length}/{pack.realms.length} completos ·
        pack {pack.version} com curadoria JEV · progresso salvo neste dispositivo
      </footer>
    </div>
  )
}
