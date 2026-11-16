# Mapeamento Beta 2.0 — Repositórios de `02_repositorios` (Fine-Tuning / RAG / Pós-Treino de LLM)

**Updated:** 2026-10-20  
**Entry point:** este README + `MAPA_CONHECIMENTO_LLM.md` + `matriz-conhecimento.csv`  
**Escopo:** todos os 16 diretórios de `E:\Github\ai-assistent-universal-coder\02_repositorios`  
**Foco de conhecimento:** fine-tuning de LLMs (causal LM), Retrieval-Augmented Generation (RAG) e pós-treino/alignamento de LLMs (DPO, PPO, GRPO, RLHF, reward modeling).  
**Procedência:** exploração estática somente leitura dos fontes locais (`02_repositorios/*`). Nenhum projeto foi executado, treinado, publicado ou modificado.  
**Herança:** AGENTS.md (ciclo BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEV) + convenção do mapeamento anterior em `07_mapeamentos/repositorios-skills/` (Beta 1.x, 11 repos × 302 skills).  

---

## 1. Por que um Beta 2.0

O mapeamento anterior (Beta 1.x, 2026-10-13) cobriu 11 repositórios contra o catálogo de 302 skills do workspace, com foco em habilidades de engenharia (arquitetura, CI/CD, deploy, observabilidade). Ele **não** aprofundou os três domínios de LLM que interessam agora:

1. **Fine-tuning de LLMs** (SFT, LoRA, QLoRA, PEFT, full fine-tuning, adapters)
2. **RAG** (embeddings, vector stores, chunking, retrieval chains, hybrid search)
3. **Pós-treino / alinhamento** (DPO, PPO, GRPO, RLHF, reward modeling, identity alignment)

O Beta 2.0 re-mapeia **todos os 16 repositórios** sob essas três lentes, incluindo os **5 repositórios novos clonados na pasta** que ainda não estavam no Beta 1.x:

| # | Repositório | Status no Beta 1.x | Relevância LLM |
|---|-------------|--------------------|----------------|
| 1 | AIHealthResearch | mapeado | RAG (BM25/vetores), fine-tuning candidato (PEFT) |
| 2 | **Awesome-LLM-Post-training** | **NOVO** | pós-treino (survey arXiv:2502.21321, repositórios de fine-tuning/RL) |
| 3 | dark-videos | mapeado | RAG-lite (pgvector), aprendizado/classificação por LLM |
| 4 | dark-videos-mining-fix | mapeado | (pacote de correção; sem foco LLM próprio) |
| 5 | DiabeticsresearchJEV | mapeado | GraphRAG, QLoRA treino contínuo |
| 6 | Engenharia-Reversa | mapeado | (MCP/CLI; sem foco LLM próprio) |
| 7 | **enterprise-llm-finetuning** | **NOVO** | fine-tuning SFT + QLoRA/LoRA (bitsandbytes 4-bit, TRL/HF) |
| 8 | FreePDFReader | mapeado | (PDF local com QA; RAG/fine-tuning não inferidos) |
| 9 | ibunny | mapeado | (jogo educacional; sem foco LLM) |
| 10 | laya | mapeado | RAG (Chroma + FTS5), classificação por LLM |
| 11 | pdfcraft | mapeado | (workbench PDF; sem foco LLM) |
| 12 | **post_training_llms** | **NOVO** | pós-treino educacional (SFT, DPO, GRPO com TRL) |
| 13 | **rag-and-fine-tuning-demo** | **NOVO** | RAG (LangChain+Ollama+FAISS) + fine-tuning Gemma LoRA + híbrido |
| 14 | **rag-finetuning** | **NOVO** | fine-tuning de embeddings para RAG (Kubeflow+Feast+Milvus) |
| 15 | remove-onedrive | mapeado | (utilitário Windows; sem foco LLM) |
| 16 | RemoveWindowsAI | mapeado | (utilitário Windows; sem foco LLM) |

**5 dos 16 repositórios são novos e LLM-nativos:** `Awesome-LLM-Post-training`, `enterprise-llm-finetuning`, `post_training_llms`, `rag-and-fine-tuning-demo`, `rag-finetuning`.

---

## 2. Dimensões de conhecimento avaliadas

Para cada repositório, o Beta 2.0 registra (quando houver evidência local):

| Dimensão | O que registra |
|----------|----------------|
| **Propósito** | declaração no README e intenção de uso |
| **Stack** | linguagem, runtime, frameworks, versões declaradas nos manifests |
| **Fine-tuning LLM** | técnicas (SFT/LoRA/QLoRA/PEFT/full), modelos, datasets, bibliotecas (trl, peft, bitsandbytes, transformers) |
| **RAG** | embeddings, vector store (FAISS/Milvus/Chroma/pgvector), chunking, retrieval chain, hybrid search |
| **Pós-treino / alinhamento** | DPO, PPO, GRPO, RLHF, reward modeling, identity alignment |
| **Inferência / serving** | como o modelo é executado (generate, Ollama, vLLM planejado, API) |
| **Artefatos de treino** | configs YAML, datasets, checkpoints, tokenizer, saved models |
| **Evidência-chave** | ponteiros para arquivos e linhas locais |
| **Lacunas / limites** | o que NÃO está implementado ou não foi verificado |

**Regras de leitura (mesmas do Beta 1.x):**
- Declarações de manifest ≠ versões instaladas nem prova de compatibilidade.
- CVE/EOL, runtime/MCP instalado, testes aprovados e implantação real **não verificados**.
- Projetos permanecem somente leitura; o mapeamento não autoriza treino, execução ou publicação.
- Links para repositórios/papers externos são referências bibliográficas, não código local.

---

## 3. Cobertura das três lentes por repositório (resumo)

| Repositório | Fine-tuning LLM | RAG | Pós-treino / alinhamento | Modelo(s) citado(s) |
|-------------|-----------------|-----|--------------------------|---------------------|
| AIHealthResearch | candidato (PEFT, treino p/ AWS) | SIM (BM25 + vetores, OpenSearch/Chroma) | — | — |
| Awesome-LLM-Post-training | bibliográfico (TRL, LLaMA-Factory, trlX, veRL, RL4LMs) | bibliográfico (RAG-Gym) | bibliográfico (RLHF, DPO, PPO, PRM surveys) | LLaMA2/3, DeepSeek-R1, Kimi, Qwen, Mistral, GPT-4/o1/o3, BLOOM |
| dark-videos | — | pgvector | — | — |
| dark-videos-mining-fix | — | — | — | — |
| DiabeticsresearchJEV | QLoRA treino contínuo | GraphRAG (MongoDB+Chroma) | — | — |
| Engenharia-Reversa | — | — | — | — |
| enterprise-llm-finetuning | SIM (SFT + QLoRA/LoRA 4-bit, TRL/HF) | — | RLHF/PPO planejado p/ v2.0 (non-goal v1.0) | Qwen2.5-0.5B, Gemma-3-1B |
| FreePDFReader | — | (QA local não verificado como RAG) | — | — |
| ibunny | — | — | — | — |
| laya | — | SIM (Chroma + FTS5) | — | — |
| pdfcraft | — | — | — | — |
| post_training_llms | SIM (SFT, DPO, GRPO full-param via TRL) | — | SIM (DPO, GRPO; sem reward model separado) | SmolLM2-135M/1.7B, Qwen2.5-0.5B/1.5B |
| rag-and-fine-tuning-demo | SIM (Gemma-3-270m LoRA + SFTTrainer) | SIM (LangChain+Ollama+FAISS, all-MiniLM-L6-v2) | — | Gemma-3-270m, gpt-oss:20b |
| rag-finetuning | fine-tuning de **embeddings** (ContrastiveLoss, não LLM causal) | SIM (Milvus, Feast ODFV, 384-d) | — | all-MiniLM-L6-v2, all-mpnet-base-v2, paraphrase-multilingual-MiniLM-L12-v2 |
| remove-onedrive | — | — | — | — |
| RemoveWindowsAI | — | — | — | — |

---

## 4. Conteúdo do pacote Beta 2.0

- `README.md` — visão geral, escopo, método, cobertura e regras (este arquivo)
- `MAPA_CONHECIMENTO_LLM.md` — mapa detalhado por repositório, organizado nos três pilares (fine-tuning / RAG / pós-treino), com técnicas, modelos, datasets, evidências e lacunas
- `matriz-conhecimento.csv` — matriz repositório × dimensão de conhecimento (legível por planilha/script)
- `repositorios/<nome>.md` — notas detalhadas por repositório (apenas os 5 novos; os 11 do Beta 1.x permanecem em `07_mapeamentos/repositorios-skills/repositorios/`)

---

## 5. Limites do Beta 2.0

- Análise estática seletiva de fontes próprias; nenhum percentual de auditoria integral é alegado.
- Árvores excluídas, binários, datasets, credenciais, cookies, backups, caches e código de terceiros não foram analisados.
- CVE/EOL, runtime/MCP instalado, contas externas e testes dos projetos não verificados.
- Nenhum download, treino, publicação, commit/push ou utilitário de remoção foi executado.
- Repositórios permanecem somente leitura; associações não autorizam operações futuras.

---

## 6. Atualização e verificação

Após mudança de fontes, revisar este pacote e regenerar `matriz-conhecimento.csv`. Não há build automático vinculado; a atualização é manual, baseada em evidência de arquivo/linha. A data acima identifica o snapshot desta missão; nova missão deve atualizar `Updated:` após revisar evidências.

**Ponteiros para o Beta 1.x (mantido):** `07_mapeamentos/repositorios-skills/{mapa.json,evidencias.json,inventory.json,matriz.csv,relatorio.html,verificacao.json}` — 11 repos × 302 skills, 3322 decisões.
