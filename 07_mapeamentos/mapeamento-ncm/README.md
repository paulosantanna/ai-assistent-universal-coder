# Mapeamento NCM — Next-Concept Modeling em três níveis (Alpha → Beta → Celta)

**Updated:** 2026-10-21
**Entry point:** este README + `alpha.md` + `beta.md` + `celta.md` + `matriz-comparativa-ncm.csv`
**Alvo:** `E:\Github\ai-assistent-universal-coder\02_repositorios\ncm` — clone de `https://github.com/HazyResearch/ncm.git`, commit `c70274273f489abc73832b2b98584a8483b6b203` (2026-10-14), licença MIT, working tree limpo. **Somente leitura; nenhum arquivo do alvo foi modificado.**
**Procedência:** exploração estática do código local (~2.580 linhas de Python, 10 configs de avaliação, README) + contexto externo declarado: paper arXiv:2610.14162 v1 (2026-10-09) e blogs oficiais Hazy Research / Stanford SAIL (2026-10-12), consultados em 2026-10-21.

---

## 1. Por que este mapeamento existe

O NCM (**Next-Concept Modeling**) é um paradigma de geração de texto que **não é um LLM autoregressivo nem um diffusion LM**: um tokenizer residual VQ-VAE multiescala comprime o texto numa hierarquia de códigos discretos (grosso → fino), e um transformer gera **um nível por vez, com todas as posições de um nível em paralelo**.

Este é o 17º repositório de `02_repositorios` e o primeiro mapeado sob a lente "alternativa a LLM" — o mapeamento anterior (`07_mapeamentos/mapeamento-beta-2.0/`, 2026-10-20) cobriu 16 repositórios de fine-tuning/RAG/pós-treino e não incluía o NCM.

O pacote responde, em três passadas que se aprofundam: **o que é** (Alpha), **como está construído** (Beta) e **como funciona por dentro, com vantagens e desvantagens** (Celta).

## 2. Como os três níveis se aprofundam

| Nível | Pergunta que responde | Conteúdo |
|-------|-----------------------|----------|
| **Alpha** | O que é? Onde está? O que promete? | Identidade e procedência, inventário físico, fluxo ponta a ponta, claims com fonte, glossário inicial, perguntas abertas |
| **Beta** | Como está construído? | Cada módulo com responsabilidade e ponteiros `arquivo:linha`, configs por task, pipeline de avaliação, fluxo exato de dados, gotchas de engenharia |
| **Celta** | Como funciona por dentro? Vale a pena? | Mecânica matemática dos dois estágios, contagem de avaliações (NFE), comparação AR × Diffusion × NCM, vantagens e desvantagens com evidência e incertezas explícitas |

Cada nível pressupõe o anterior. Nenhum substitui o outro.

## 3. Regras de evidência (valem para todo o pacote)

- **[C]** evidência de código local — ponteiro `arquivo:linha` verificável no commit acima.
- **[R]** declaração do README/manifesto do repo — é claim, não comportamento verificado.
- **[X]** fonte externa oficial (paper arXiv:2610.14162 v1 / blogs Hazy e SAIL) — claim de paper, não reproduzido localmente.
- **[I]** inferência/análise deste mapeamento — não executada, marcada como tal.
- **Execução**: o mapeamento foi somente leitura; a reprodução local cobre apenas 1 task (sudoku-hard, `[REP]` — ver `.work/ncm-repro/RESULTADO.md`). Os demais números de qualidade/velocidade continuam claims das fontes, **não reproduzidos**.
- Versões de dependências do `requirements.txt` (torch, numpy, omegaconf, hydra, transformers>=4.51, …) são declarações; compatibilidade real de runtime não foi verificada.
- CVE/EOL, segurança de runtime e licenças de terceiros não foram auditados além da licença MIT do próprio repo.

## 4. Conteúdo do pacote

- `README.md` — este arquivo: escopo, método, regras e limites.
- `alpha.md` — **Mapeamento Alpha**: visão panorâmica e orientação.
- `beta.md` — **Mapeamento Beta**: estrutura e componentes com ponteiros.
- `celta.md` — **Mapeamento Celta**: mecanismo profundo, comparação com LLMs atuais, vantagens e desvantagens.
- `matriz-comparativa-ncm.csv` — matriz dimensão × (autoregressivo / diffusion LM / NCM) legível por planilha.

## 5. Limites conhecidos

- O repositório é um **release de inferência/avaliação**: não há código de treino do tokenizer nem do gerador (ver Beta §9); a análise interna de treino apoia-se no par código+paper.
- Os checkpoints e datasets vivem no Hugging Face (`hazyresearch/ncm-checkpoints`, `hazyresearch/ncm-datasets`). O subconjunto `sudoku/hard` foi baixado (sha256 == LFS oids) e a task **reproduzida em 2026-10-21**: solved 86,25% (1725/2000) vs 86,1% do blog — evidência em `.work/ncm-repro/RESULTADO.md`. As demais tasks não foram baixadas.
- O clone omite artefatos citados no `.gitignore` (baseline MDLM vendorizado, checkpoints de baseline ~29 GB, experimentos) — não foram inspecionados.
- Alegações de exatidão textual (BLEU/ROUGE/sudoku) dependem de protocolos de avaliação do próprio repo; não há prova independente neste pacote.

## 6. Verificação e regeneração

- Identidade conferida por `git log`/`git status` em 2026-10-21 (commit, data, `origin`, tree limpo).
- Ponteiros `arquivo:linha` deste pacote foram escritos a partir de leitura direta dos fontes locais; spot-check final registrado em `.notebook/PROGRESS.md`.
- Não há build automático: após mudança de commit no repo alvo, este pacote deve ser revisado manualmente e o campo `Updated:` renovado.
