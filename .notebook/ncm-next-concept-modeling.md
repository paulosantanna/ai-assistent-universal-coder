# ncm — Next-Concept Modeling (HazyResearch/Stanford)

Updated: 2026-10-21
Entry point: `07_mapeamentos/mapeamento-ncm/README.md` (pacote alpha/beta/celta + matriz CSV)

## O que é

Alternativa a LLM autoregressivo e a diffusion LM: um tokenizer VQ-VAE residual
**multiescala** representa o texto como hierarquia de códigos discretos
(grosso→fino) e um transformer gera **um nível por passo**, com todas as
posições do nível em paralelo — K passos, não L tokens. Dois estágios:
tokenizer (congelado no estágio 2) + gerador condicionado à reconstrução
acumulada dos níveis anteriores.

## Fatos duráveis (evidência)

- Clone local: `02_repositorios/ncm` @ `c702742` (2026-10-14), MIT, origem
  `github.com/HazyResearch/ncm`. É **release de inferência/avaliação**: sem
  código de treino, sem baselines (clone MDLM vendorizado e ckpts ~29G ficaram
  fora; `.gitignore:219-221`).
- Mecânica no código: `models/quant.py` (MultiscaleResidualVectorQuantizer:
  codebooks EMA por nível, blend residual `Phi`, `fine_drop`/nested dropout,
  straight-through só no nível 0); `models/next_concept.py` (atenção
  block-diagonal, RoPE por nível, level embedding, cabeças atadas ao codebook,
  CFG com rampa por nível).
- NFE ≈ nº de níveis (Sudoku 12 níveis = 12 NFE do blog; XSum 9; OWT 32).
- Claims do paper/blog (sudoku-hard reproduzido em 2026-10-21; os demais NÃO
  reproduzidos aqui): 21×/10×/31× mais rápido (LM1B/OWT/XSum), ~4–5× menos
  tokens de treino, Sudoku hard 86.1% vs AR 1.0% / MDLM 30.2% / FMLM+ 81.3%.
  `README.md:30` diz "9–31×" (divergência menor).
- Penalidades de frequência/adjacência + unigramas salvas no checkpoint são
  heurísticas de **avaliação** (`scripts/eval_shard.py:99-124`), não do modelo.
- `aux.code_corruption` e `fine_drop.dual/w_full/w_trunc` existem só nas
  configs; implementação de treino não liberada.

## Limites e riscos

- Escala demonstrada até 725M parâmetros; sem alinhamento/instrução/chat.
- Computação fixa por exemplo e treino conjunto tokenizer+gerador são
  "trabalho futuro" declarado pelo próprio time (blog).
- Amostragem crua frágil (daí as heurísticas); erros compõem entre níveis.
- Reprodução local feita apenas para sudoku-hard (seção abaixo); demais tasks e
  claims (21×/10×/31×; 4–5× menos tokens) não executados.

## Reprodução (2026-10-21)

- sudoku-hard com checkpoints oficiais (sha256 == LFS oids do HF) em
  `.work/ncm-repro/`: **solved 86,25% (1725/2000)**, cell 98,36% — blog 86,1%.
  RTX 5080, torch 2.11.0+cu128, Python 3.14.7; 12 forwards/tabuleiro.
- Evidência: `.work/ncm-repro/RESULTADO.md`.

## Aplicação (2026-10-21)

- Paradigma aplicado no dark-videos (`D:\Git\dark-videos\backend\app\modules\learning\ncm.py`):
  nível conceito (prior aprendido dos números por rede + conteúdo) pontua tudo numa passada e
  escolhe o shortlist; o Laya (nível fino) julga só o shortlist; ajuste ≤ ±10% no score;
  `ncm_concept` gravado na decisão. Modelo/checkpoints do NCM **não** usados (release de
  inferência, sem treino/domínio de vídeo) — só o paradigma coarse-to-fine.
- Evidência: `.work/ncm-selection/EVIDENCE.md`; `D:/Git/dark-videos/.specs/features/ncm-selection/`,
  `docs/rag-laya.md`, `.notebook/ncm-selection.md` do projeto.

## Mapa profundo

- `07_mapeamentos/mapeamento-ncm/alpha.md` — panorama, identidade, inventário, claims.
- `07_mapeamentos/mapeamento-ncm/beta.md` — todos os módulos com ponteiros `arquivo:linha`.
- `07_mapeamentos/mapeamento-ncm/celta.md` — mecânica, vantagens/desvantagens, incertezas.
- `07_mapeamentos/mapeamento-ncm/matriz-comparativa-ncm.csv` — AR × Diffusion × NCM.
