# NVIDIA skills no padrão TLC

Updated: 2026-11-25
Entry point: `00_skills/INDEX.md`

- Fonte: https://github.com/NVIDIA/skills commit `e34173c2efbe5ced223f39903bd4806d8ac13d7d`. Não passaram pelo instalador NVIDIA. A adaptação não herda a assinatura OMS.
- Temas: `(rag-systems)`, `(gpu-data)`, `(synthetic-data)`, `(inference-serving)`, `(video-analytics)`, `(physical-ai)`, `(distributed-training)`, `(clinical-ai)`, `(agent-memory)`.
- Cada pacote: `SKILL.md` ≤ 100 linhas, `references/procedure.md`, `examples.md`, `defects.md`, `provenance.md`, `NOTICE`. Markdown operacional longo fica em `references/upstream/`.
- Fora do pacote: `skill.oms.sig`, `BENCHMARK.md`, `evals/`, scripts `.py`/`.sh` e fixtures. O procedimento cita o caminho upstream quando o comando depende deles.
- Gates que vencem o texto upstream: confirmação antes de deploy, `sbatch` ou job pago; sem PHI em git; VSS só em deployment que o usuário administra; irmãos NuRec e TAO platform não instalados são nomeados e a skill para.
- `nemo-rl-session-memory` não substitui `.notebook/` neste workspace.
- Verificação desta missão: estrutura e distribuição. Sem execução de GPU, cluster, DICOM ou câmera.
