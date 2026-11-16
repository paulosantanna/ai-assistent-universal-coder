# DeepSeek V4.1 Flash UNCENSORED FP8
Updated: 2026-11-03. Entry point: `D:/Git/DeepSeek-V4.1-Flash-1017-UNCENSORED-FP8/trainer/README.md`.

- Continual trainer em `trainer/`. A matriz do shard fica congelada em bf16; só o LoRA treina. EWC, replay, gate `1/(1+F)` depois do Adam e teto `||ΔW||_F/||W||_F` (padrão 0,02). Shards não são abertos para escrita. Experts FP4 roteados e Engram ficam de fora.
- Verificado em 2026-11-03: `python -m unittest trainer.tests.test_continual` — 15 testes OK. Fumaça CPU em `layers.10.attn.wo_b.weight` (`model-00013`, `[5120, 8192]` F8_E4M3): 1 passo, drift 0,000114, base sem gradiente. `model-00003` continua ausente; a camada 0 desse nome não inicializa neste checkout. 29 shards presentes. Não é avaliação de qualidade do modelo.

- Checkpoint multimodal + inferência de referência Python/CUDA em `D:/Git/DeepSeek-V4.1-Flash-1017-UNCENSORED-FP8`; configuração e `inference/model.py` são as fontes para arquitetura.
- Em 2026-10-31: índice cita 48 shards, 29 presentes; Git index vazio apesar de HEAD e arquivos físicos; 49 testes de encoding passaram e 6 falharam por goldens ausentes em UTF-8. Estado pode mudar; consultar `.aeos/evidence/deepseek-v41-flash-inventario.json` e repetir inventário antes de uso.
- Fluxo CLI é autoregressivo; forward DSpark não prova execução especulativa. Inferência e qualidade do modelo não foram verificadas; veja abaixo os hashes calculados.
- Relatório contém as dez camadas, limitações, riscos e prioridades; manifesto em `.aeos/evidence/deepseek-v41-flash-manifest.json`.
- Ampliação: `.aeos/reports/deepseek-v41-flash-analise-ampliada.md` e `DeepSeek-V4.1-Flash-1017-UNCENSORED-FP8-threat-model.md`. Usuário confirmou uso local sem terceiros; interpretação de riscos depende desse contexto.
- Snapshot adicional: cabeçalhos dos 29 shards presentes coincidem em nomes com o índice e offsets inspecionados cabem nos arquivos, sem hash nem validação numérica. Python padrão reportou PyTorch CPU, CUDA/NCCL indisponíveis e TileLang ausente; outro ambiente pode diferir. Evidência: `.aeos/evidence/deepseek-v41-analise-ampliada.json`.
- Aprofundamento com metodologia REA: `.aeos/reports/deepseek-v41-engenharia-reversa-aprofundamento.md`; relatório histórico da análise de 42 cabeçalhos. O resultado atualizado abaixo inclui os seis parciais.
- Cabeçalhos dos shards 47/48 descrevem tabelas Engram e escalas de cerca de 189,13 GiB no total da categoria; não é medição de RAM ou VRAM. Evidência `.aeos/evidence/deepseek-v41-rea-forensics.json`.
- Mapeamento consolidado: 48 cabeçalhos, 96.085 tensores, banco `.aeos/evidence/deepseek-v41-tensors.sqlite3` e explorador `.aeos/reports/deepseek-v41-explorador.html`. Os 42 objetos completos passaram SHA-256 contra HEAD; seis parciais têm apenas hash de prefixo. Evidência e validação em `.aeos/evidence/deepseek-v41-{lfs-hashes,final-validation}.json`.
- Os 55 testes de encoding passaram em cópia isolada com goldens oficiais da base, não na árvore original incompleta. Comparação de OIDs com base: 21 shards iguais e 27 diferentes; não identifica tensores modificados individualmente.
