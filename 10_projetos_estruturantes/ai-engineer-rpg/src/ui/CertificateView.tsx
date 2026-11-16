import { useState } from 'react'
import type { GameState } from '../engine/types'
import { pack } from '../content/pack'
import { certificatesReady } from '../engine/progress'
import { store } from '../store/gameStore'
import { buildEvidenceDossier, canonicalJson, renderCertificatePdf, sha256Hex } from '../engine/certificate'

interface Props {
  gs: GameState
}

export function CertificateView(props: Props): JSX.Element {
  const { gs } = props
  const ready = certificatesReady(pack, gs)
  const [busy, setBusy] = useState(false)
  const [verify, setVerify] = useState<'ok' | 'mismatch' | null>(null)

  async function issue(): Promise<void> {
    setBusy(true)
    try {
      const ok = await store.issueCertificate(pack)
      if (!ok) alert('Emissão bloqueada: capstone precisa estar aprovado com 7 reinos completos.')
    } finally {
      setBusy(false)
    }
  }

  async function download(): Promise<void> {
    const cert = gs.certificate
    if (!cert) return
    const blob = await renderCertificatePdf({
      name: cert.name,
      code: cert.code,
      hash: cert.hash,
      score: cert.score,
      issuedAt: cert.issuedAt,
      organ: pack.organ,
      typology: 'Curso livre de formação em engenharia de IA (client-side, verificação por SHA-256)',
      realms: pack.realms.map((r) => ({ name: r.name, tier: r.tier })),
    })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `certificado-${cert.code}.pdf`
    a.click()
    URL.revokeObjectURL(url)
  }

  async function verifyNow(): Promise<void> {
    const cert = gs.certificate
    if (!cert) return
    const dossier = buildEvidenceDossier(pack, gs, cert.issuedAt)
    const hash = await sha256Hex(canonicalJson(dossier))
    setVerify(hash === cert.hash ? 'ok' : 'mismatch')
  }

  const cert = gs.certificate

  return (
    <section>
      <h2 className="section-title">Certificado verificável</h2>
      {!ready && !cert && (
        <p className="locked-note">
          Portão fechado: emita após passar no Capstone com os 7 reinos completos. O código AIE-AAAA-HASH8 nasce do
          SHA-256 do dossiê de evidências.
        </p>
      )}
      {ready && !cert && (
        <div className="panel ok">
          <h3>Tudo pronto para emissão</h3>
          <p>Nome declarado: {gs.playerName || '(preencha o nome do herói no HUD)'}</p>
          <button className="btn primary" onClick={() => void issue()} disabled={busy}>
            {busy ? 'Selando…' : 'Emitir certificado'}
          </button>
        </div>
      )}
      {cert && (
        <div className="cert-card">
          <p className="cert-organ">{pack.organ}</p>
          <h3>Certificado de Conclusão</h3>
          <p className="cert-line">
            {cert.name} concluiu a trilha dos 7 Reinos e o Capstone com nota <b>{cert.score.toFixed(2)} / 1.00</b>
          </p>
          <p className="cert-code">{cert.code}</p>
          <p className="cert-hash" title={cert.hash}>
            SHA-256 do dossiê: {cert.hash.slice(0, 16)}…{cert.hash.slice(-8)}
          </p>
          <p className="muted">Emitido em {cert.issuedAt}</p>
          <div className="action-row">
            <button className="btn primary" onClick={() => void download()}>⬇ Baixar PDF</button>
            <button className="btn" onClick={() => void verifyNow()}>Verificar agora</button>
          </div>
          {verify === 'ok' && <p className="panel ok">✓ Hash recalculado da mesma página: dossiê intacto.</p>}
          {verify === 'mismatch' && (
            <p className="panel bad">✗ Hash diferente: o progresso mudou desde a emissão (ex.: nova rolagem). Registro emitido preservado.</p>
          )}
        </div>
      )}
    </section>
  )
}
