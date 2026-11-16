# ncm — beta 3.0.0

Updated: 2026-10-27
Entry point: [índice](../README.md) · [mapa estruturado](../mapa.json)

Arquivos com hash: 32; fingerprint: `ba14d6f31c6971defd8321b964987d71a1bd01b2dbfb972661772817e62e263e`.
Git próprio: True; HEAD: `c70274273f489abc73832b2b98584a8483b6b203`; branch: `main`.
Estado local: limpo; detalhes em inventory.json.

## Atualizações e reconciliação

Novo em relação à lista de 16 do beta 2; já possuía estudo separado. Incorporado ao mapa geral com tokenizer e gerador, mantendo treino completo não demonstrado.

## Dimensões e evidências

### Propósito

**documentado** — Geração coarse-to-fine por conceitos multiescala; release de avaliação/inferência.

[ncm/README.md:91](../../../02_repositorios/ncm/README.md)

### Arquitetura

**código presente** — Tokenizer VQ-VAE e gerador NextConceptTransformer são módulos distintos.

[ncm/models/next_concept.py:65](../../../02_repositorios/ncm/models/next_concept.py)

### Fluxo

**código presente** — Entrypoint de avaliação coordena geração e medição; não é pipeline completo de treino.

[ncm/evaluate.py:9](../../../02_repositorios/ncm/evaluate.py)

### Dados

**código presente** — Quantizador residual multiescala representa sequências por níveis e codebooks.

[ncm/models/quant.py:228](../../../02_repositorios/ncm/models/quant.py)

### Interfaces

**código presente** — Tokenizador liga pré-tokenização e VQ-VAE.

[ncm/tokenization/vqvae_tokenizer.py:7](../../../02_repositorios/ncm/tokenization/vqvae_tokenizer.py)

### Configuração/deploy

**documentado** — README recomenda Python/CUDA e download separado de checkpoints e dados.

[ncm/README.md:66](../../../02_repositorios/ncm/README.md)

### Operação

**documentado** — Avaliação reporta métricas por tarefa, incluindo Sudoku, tradução e linguagem.

[ncm/README.md:87](../../../02_repositorios/ncm/README.md)

### Fine-tuning

**não demonstrado na amostra** — Sem conclusão positiva nesta revisão estática; não equivale a ausência universal.


### RAG

**não demonstrado na amostra** — Sem conclusão positiva nesta revisão estática; não equivale a ausência universal.


### Pós-treino

**não demonstrado na amostra** — Sem conclusão positiva nesta revisão estática; não equivale a ausência universal.


### Inferência

**código presente** — Gerador NextConceptTransformer prediz níveis; não presumir código completo de treino nesta release.

[ncm/models/next_concept.py:521](../../../02_repositorios/ncm/models/next_concept.py)

### Tecnologias/versões

**declarado** — Ver declarações extraídas e manifests; versões instaladas e compatibilidade não verificadas.

[ncm/requirements.txt:1](../../../02_repositorios/ncm/requirements.txt)
[ncm/requirements.txt:2](../../../02_repositorios/ncm/requirements.txt)
[ncm/requirements.txt:3](../../../02_repositorios/ncm/requirements.txt)
[ncm/requirements.txt:4](../../../02_repositorios/ncm/requirements.txt)
[ncm/requirements.txt:5](../../../02_repositorios/ncm/requirements.txt)
[ncm/requirements.txt:6](../../../02_repositorios/ncm/requirements.txt)
[ncm/requirements.txt:7](../../../02_repositorios/ncm/requirements.txt)
[ncm/requirements.txt:8](../../../02_repositorios/ncm/requirements.txt)

### Vulnerabilidades

**não verificado** — Sem consulta de CVE/EOL nesta missão.


### Obsolescência

**não verificado** — Sem consulta de CVE/EOL nesta missão.


## Declarações de versão

| Manifest / declaração | Valor | Evidência |
|---|---|---|
| dependency | torch | [ncm/requirements.txt:1](../../../02_repositorios/ncm/requirements.txt) |
| dependency | numpy | [ncm/requirements.txt:2](../../../02_repositorios/ncm/requirements.txt) |
| dependency | omegaconf | [ncm/requirements.txt:3](../../../02_repositorios/ncm/requirements.txt) |
| dependency | hydra-core | [ncm/requirements.txt:4](../../../02_repositorios/ncm/requirements.txt) |
| dependency | transformers>=4.51 | [ncm/requirements.txt:5](../../../02_repositorios/ncm/requirements.txt) |
| dependency | huggingface_hub[cli] | [ncm/requirements.txt:6](../../../02_repositorios/ncm/requirements.txt) |
| dependency | regex | [ncm/requirements.txt:7](../../../02_repositorios/ncm/requirements.txt) |
| dependency | rouge_score | [ncm/requirements.txt:8](../../../02_repositorios/ncm/requirements.txt) |
| dependency | sacrebleu | [ncm/requirements.txt:9](../../../02_repositorios/ncm/requirements.txt) |

## Qualidade e limites

Workflows: 0; arquivos candidatos a testes: 0. Não executados.

- Amostra semântica seletiva; hash e busca textual não equivalem a auditoria integral.
- Nenhum runtime, treino, publicação ou sincronização remota executado.
- Fontes modificadas/não rastreadas fazem parte deste snapshot local.
