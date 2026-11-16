# Mapa de Conhecimento LLM — Beta 2.0

**Updated:** 2026-10-20  
**Entry point:** `07_mapeamentos/mapeamento-beta-2.0/README.md` (visão geral) + `matriz-conhecimento.csv` (matriz legível)  
**Escopo:** 16 repositórios de `02_repositorios`  
**Três pilares:** (A) Fine-tuning de LLM, (B) RAG, (C) Pós-treino / alinhamento  
**Regras:** somente leitura; declarações de manifest ≠ versões instaladas; CVE/EOL/runtime não verificados; nenhum treino executado.

---

## Pilar A — Fine-tuning de LLM (causal LM: SFT, LoRA, QLoRA, PEFT, full-param)

### Repositórios com fine-tuning de LLM implementado

#### 1. enterprise-llm-finetuning — SFT + QLoRA/LoRA 4-bit + DPO + PPO/RLHF + RAG (FAISS) (estruturado, pronto p/ GPU)

**Técnicas:** SFT (TRL SFTTrainer + transformers.Trainer), LoRA/QLoRA (peft), quantização 4-bit bitsandbytes (NF4, double quant, bfloat16), FSDP/DeepSpeed, **DPO (TRL DPOTrainer com beta, loss_type, label_smoothing)**, **PPO/RLHF (TRL PPOTrainer com reward model dedicado, kl_coefficient, cliprange, vf_coefficient)**, **RAG (sentence-transformers embeddings + FAISS IndexFlatIP, chunking character-based com overlap, index save/load)**.  
**Modelos:** Qwen2.5-0.5B, Gemma-3-1B (config YAML de exemplo). Embedding: `sentence-transformers/all-MiniLM-L6-v2`. Reward model dedicado configurável via `ppo.reward_model_id`.  
**Arquivos:** `src/application/usecases/train_pipeline.py`, `trl_trainer.py`, **`dpo_trainer.py`**, **`ppo_trainer.py`**, **`faiss_rag_pipeline.py`**, `huggingface_trainer.py`, `transformers_llm_model_loader.py`, `config_schema.py` (PEFTConfig, **DPOConfig**, **PPOConfig**, **RAGConfig**, QuantizationConfig 4-bit), `src/finetuning_config.yaml`, **`src/dpo_config.yaml`**, **`src/ppo_config.yaml`**, **`src/rag_config.yaml`**, `src/infrastructure/factories/trainer_factory.py` (mapeia `huggingface_dpo`/`dpo`, `huggingface_ppo`/`ppo`), `src/infrastructure/factories/rag_factory.py` (mapeia `faiss` → `FaissRAGPipeline`), `src/application/usecases/rag_pipeline_usecase.py`, `src/domain/interfaces/rag_pipeline.py` (`RAGPipelineBase`), `src/presentation/cli.py` (opções `--rag`, `--rag-config`, `--rag-query`, `--rag-index-dir`).  
**Monitoramento:** Prometheus + W&B callbacks e exporter (porta 8000).  
**Avaliação:** `DeterministicEvaluator` com delta metrics (base vs fine-tuned), quality gates, scorecards JSON/Markdown.  
**Testes:** `tests/unit/` (train_model_usecase, trainer_factory, config_schema, chat_template_formatter, etc.) + testes de factory para `DpoTrainer` e `PPOTrainerAdapter`.  
**Lacunas:** não há servidor de inferência (vLLM só em ADR).  
**Bugs críticos:** nenhum.  
**Ponteiro:** `02_repositorios/enterprise-llm-finetuning/src/infrastructure/rag/faiss_rag_pipeline.py`

#### 2. post_training_llms — SFT / DPO / GRPO (educacional, full-param)

**Técnicas:** SFT (SFTTrainer), DPO (DPOTrainer, beta, pares chosen/rejected), GRPO (GRPOTrainer, reward function `\boxed{}`, `num_generations`). **Sem PEFT/LoRA/QLoRA** (full-parameter apenas).  
**Modelos:** SmolLM2-135M / 135M-Instruct / 1.7B, Qwen2.5-0.5B, Qwen2.5-1.5B.  
**Datasets:** `banghua/DL-SFT-Dataset` (SFT), `mrfakename/identity` (DPO), `openai/gsm8k` (RL/math).  
**Arquivos:** `src/training/sft_trainer.py`, `dpo_trainer.py`, `rl_trainer.py`, `src/utils/model_utils.py` (load/generate/save), `src/utils/data_utils.py`, `src/utils/config.py` (dataclasses+YAML), `src/evaluation/benchmark.py`, `examples/run_sft.py|dpo.py|rl.py|benchmark.py`, `configs/*.yaml`.  
**Lacunas:** não há PEFT/LoRA/QLoRA; não há reward model separado; não há RAG; `python_requires>=3.8` pode ser restritivo.  
**Bugs críticos:** nenhum.  
**Ponteiro:** `02_repositorios/post_training_llms/src/training/`

#### 3. rag-and-fine-tuning-demo — Gemma-3-270m LoRA + SFT (demo comparativo)

**Técnicas:** fine-tuning de Gemma-3-270m com LoRA (`LoraConfig` r=16/alpha=32) + SFT (`SFTTrainer` da TRL, `SFTConfig` batch 4, lr 1e-4, max_steps 100).  
**Modelos:** Gemma-3-270m (fine-tune), gpt-oss:20b (RAG/direct via Ollama), all-MiniLM-L6-v2 (embeddings).  
**Arquivos:** `fine_tuning/train_gemma.py` (corrigido nesta missão), `fine_tuning/prepare_data.py` (9 exemplos Q&A sintéticos), `fine_tuning/training_data.json`, `rag/rag_system.py`, `chatbot_app.py` (4 modalidades: Direct/RAG/FT/Hybrid).  
**Lacunas:** não há QLoRA/DPO/PPO/RLHF; não há reranking/hybrid search; `requirements.txt` sem versões fixas; caminhos hardcoded em `rag/rag_system.py` e `prepare_data.py` (ambiente original do autor).  
**Bugs críticos corrigidos:** caminho hardcoded `/Users/hnai/...` → parametrizado (argumento/env `GEMMA_TRAINING_DATA`/relativo); otimização só-MPS → detecção CUDA/MPS/CPU.  
**Ponteiro:** `02_repositorios/rag-and-fine-tuning-demo/fine_tuning/train_gemma.py`

#### 4. AIHealthResearch — fine-tuning candidato (PEFT) para AWS

**Técnicas:** PEFT declarado (`extra:ml`: torch, transformers, peft, accelerate); treino candidato para AWS.  
**RAG:** BM25 + vetores (rank-bm25, chromadb, opensearch-py).  
**Arquivos:** `src/aihealthresearch/infrastructure/trainer.py:73` (callback de telemetria de treino), `pyproject.toml` (dependências ML), `requirements.txt`.  
**Lacunas:** pipeline concreto de treino não inspecionado em profundidade nesta missão; aprovação científica e implantação não verificadas.  
**Ponteiro:** `02_repositorios/AIHealthResearch/src/aihealthresearch/infrastructure/trainer.py:73`

#### 5. DiabeticsresearchJEV — QLoRA treino contínuo + GraphRAG

**Técnicas:** QLoRA treino contínuo (declarado no Beta 1.x); GraphRAG (MongoDB + Chroma).  
**Lacunas:** alvo `ai-continuous-training-maintainer` não coincide com este diretório (gap do Beta 1.x); pipeline concreto não inspecionado nesta missão.  
**Ponteiro:** `02_repositorios/DiabeticsresearchJEV` (mapeamento Beta 1.x em `07_mapeamentos/repositorios-skills/`)

---

### Repositórios sem fine-tuning de LLM (não se aplica)

| Repositório | Motivo |
|-------------|--------|
| dark-videos | aprendizado/classificação por LLM via cliente LAYA externo; não é treino de LLM |
| dark-videos-mining-fix | pacote de correção de mineração pt-BR; sem foco LLM próprio |
| Engenharia-Reversa | CLI/MCP engenharia reversa de binários; sem foco LLM |
| FreePDFReader | leitor PDF nativo (Rust+PDFium+ONNX); QA local não verificado como RAG/fine-tuning |
| ibunny | jogo educacional Flutter/Go; sem foco LLM |
| laya | classificação/pesquisa por LLM (Chroma+FTS5); não é treino de LLM |
| pdfcraft | workbench PDF nativo; sem foco LLM |
| remove-onedrive / RemoveWindowsAI | utilitários Windows PowerShell; sem foco LLM |
| Awesome-LLM-Post-training | lista bibliográfica (links para TRL, LLaMA-Factory, trlX, veRL, RL4LMs); **não contém código de treino** |

---

## Pilar B — RAG (embeddings, vector store, chunking, retrieval chain)

### Repositórios com RAG

#### 1. AIHealthResearch — BM25 + vetores

**Técnicas:** rank-bm25, chromadb, opensearch-py; knowledge_versions versionados/auditados (SQLAlchemy).  
**Ponteiro:** `02_repositorios/AIHealthResearch/src/aihealthresearch/infrastructure/database.py:25`

#### 2. rag-and-fine-tuning-demo — LangChain + Ollama + FAISS

**Técnicas:** TextLoader → CharacterTextSplitter (1000/200) → HuggingFaceEmbeddings all-MiniLM-L6-v2 → FAISS → OllamaLLM (gpt-oss:20b) → retrieval chain (stuff documents).  
**Arquivo:** `02_repositorios/rag-and-fine-tuning-demo/rag/rag_system.py`.  
**Lacunas:** sem reranking, sem hybrid search (lexical+semântico), sem query expansion.  
**Ponteiro:** `02_repositorios/rag-and-fine-tuning-demo/rag/rag_system.py:12-50`

#### 3. rag-finetuning — Milvus + Feast ODFV (embeddings 384-d)

**Técnicas:** FeatureView `wiki_passages` (texto + embeddings 384-d, COSINE, IVF_FLAT, Milvus online), `query_embeddings` (ODFV online), chunking de parquet para limite varchar Milvus.  
**Arquivos:** `feature_repo/wiki_features.py`, `training_data_features.py`, `chunk_parquet_data.py`, `feature_store.yaml`.  
**Lacunas:** arquivos citados no README que não existem (`re_embed_wikipedia.py`, `fine_tuned_wiki_features.py`, `fine_tuned_embedding_odfv.py`).  
**Bugs críticos corrigidos:** `feature_repo/__init__.py` importava módulos inexistentes → removido.  
**Ponteiro:** `02_repositorios/rag-finetuning/feature_repo/wiki_features.py:25`

#### 4. dark-videos — pgvector (RAG-lite)

**Técnicas:** SQLAlchemy + UUIDs/JSONB, pgvector. Não é RAG de LLM completo.  
**Ponteiro:** `02_repositorios/dark-videos/backend/app/db/base.py:11`

#### 5. laya — Chroma + FTS5

**Técnicas:** Chroma DB + SQLite FTS5 para pesquisa/classificação por LLM. Não é RAG de LLM completo.  
**Ponteiro:** `02_repositorios/laya` (mapeamento Beta 1.x)

---

### Repositórios sem RAG (não se aplica)

post_training_llms, enterprise-llm-finetuning, dark-videos-mining-fix, Engenharia-Reversa, FreePDFReader, ibunny, pdfcraft, remove-onedrive, RemoveWindowsAI, Awesome-LLM-Post-training (apenas bibliográfico: RAG-Gym link externo).

---

## Pilar C — Pós-treino / alinhamento (DPO, PPO, GRPO, RLHF, reward modeling, identity alignment)

### Repositórios com pós-treino / alinhamento

#### 1. post_training_llms — DPO + GRPO (sem reward model separado)

**Técnicas:** DPO (DPOTrainer, beta, pares chosen/rejected via modificação de identidade), GRPO (GRPOTrainer, reward function matemática, `num_generations`).  
**Não há:** reward model separado (DPO/GRPO são alternativas sem RLHF clássico), PEFT/LoRA/QLoRA.  
**Arquivos:** `src/training/dpo_trainer.py`, `rl_trainer.py`, `src/utils/data_utils.py` (create_identity_dataset, prepare_dpo_dataset, prepare_rl_dataset).  
**Ponteiro:** `02_repositorios/post_training_llms/src/training/dpo_trainer.py`

#### 2. enterprise-llm-finetuning — avaliação base vs fine-tuned (delta metrics)

**Técnicas:** avaliação comparativa com `model.disable_adapter()` para baseline + delta metrics (ΔEM, ΔF1, ΔROUGE-L), quality gates.  
**Não há:** DPO/PPO/RLHF implementado (v2.0 planejado no PRD como non-goal v1.0).  
**Arquivo:** `src/application/usecases/evaluate_model_usecase.py`.  
**Ponteiro:** `02_repositorios/enterprise-llm-finetuning/src/application/usecases/evaluate_model_usecase.py`

#### 3. Awesome-LLM-Post-training — bibliográfico (surveys de RLHF/DPO/PPO/PRM)

**Técnicas:** apenas links para papers e repositórios externos (TRL, LLaMA-Factory, veRL, trlX, RL4LMs, Okapi). Não há código local.  
**Ponteiro:** `02_repositorios/Awesome-LLM-Post-training/README.md` (L257-L277)

---

### Repositórios sem pós-treino / alinhamento (não se aplica)

Todos os demais: AIHealthResearch, dark-videos, dark-videos-mining-fix, Engenharia-Reversa, FreePDFReader, ibunny, laya, pdfcraft, rag-and-fine-tuning-demo (apenas SFT), rag-finetuning (apenas embeddings), remove-onedrive, RemoveWindowsAI.

---

## Resumo de cobertura dos três pilares

| Repositório | A: Fine-tuning LLM | B: RAG | C: Pós-treino/alinhamento |
|-------------|-------------------|--------|---------------------------|
| enterprise-llm-finetuning | SIM (SFT+QLoRA 4-bit) | — | avaliação delta (RLHF v2.0 planejado) |
| post_training_llms | SIM (SFT/DPO/GRPO full-param) | — | SIM (DPO+GRPO, sem reward model) |
| rag-and-fine-tuning-demo | SIM (Gemma LoRA+SFT) | SIM (LangChain+Ollama+FAISS) | — |
| rag-finetuning | fine-tuning de **embeddings** (não LLM causal) | SIM (Milvus+Feast 384-d) | — |
| AIHealthResearch | candidato (PEFT) | SIM (BM25+vetores) | — |
| DiabeticsresearchJEV | QLoRA contínuo | GraphRAG | — |
| dark-videos | — | pgvector (RAG-lite) | — |
| laya | — | Chroma+FTS5 | — |
| Outros 8 | — | — | — |

---

## Correções aplicadas nesta missão (Beta 2.0)

| # | Repositório | Arquivo | Problema | Correção |
|---|-------------|---------|----------|----------|
| 1 | rag-finetuning | `feature_repo/__init__.py` | Importava `fine_tuned_wiki_features` e `fine_tuned_embedding_odfv` (inexistentes) → `ModuleNotFoundError` | Removidas as 2 imports e entradas em `__all__` |
| 2 | rag-and-fine-tuning-demo | `fine_tuning/train_gemma.py` | Caminho hardcoded `/Users/hnai/Downloads/...`; otimização só-MPS (Apple Silicon) | Caminho por argumento/env/relativo; detecção CUDA>MPS>CPU |

## Correções sugeridas (não aplicadas — exigem decisão)

| # | Repositório | Sugestão |
|---|-------------|----------|
| 1 | rag-finetuning | Criar arquivos ausentes citados no README (`re_embed_wikipedia.py`, `test_end_to_end.py`, `fine_tuned_wiki_features.py`, `fine_tuned_embedding_odfv.py`) |
| 2 | rag-and-fine-tuning-demo | Fixar versões em `requirements.txt`; tornar caminhos em `rag/rag_system.py` e `prepare_data.py` relativos |
| 3 | enterprise-llm-finetuning | Implementar DPO/RLHF (v2.0) e servidor de inferência vLLM |
| 4 | post_training_llms | Adicionar PEFT/LoRA/QLoRA |
| 5 | AIHealthResearch / DiabeticsresearchJEV | Inspecionar pipelines de treino concretos |
