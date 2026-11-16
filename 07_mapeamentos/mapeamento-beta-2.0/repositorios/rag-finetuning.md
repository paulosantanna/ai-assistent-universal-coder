# Nota de mapeamento — rag-finetuning

**Caminho:** `02_repositorios/rag-finetuning`  
**Updated:** 2026-10-20  
**Tipo:** Pipeline de fine-tuning de **embeddings** para RAG (Kubeflow distribuído + Feast + Milvus)  
**Status no Beta 2.0:** NOVO (não estava no Beta 1.x)  
**Licença:** Apache 2.0

## Propósito
Pipeline production-ready e integrado para fine-tuning de **modelos de embeddings** (não LLM causal) para RAG, usando Kubeflow Trainer para treinamento distribuído (PyTorch) em clusters KIND, Feast Feature Store para gerenciamento de dados e serving em tempo real, On Demand Feature Views (ODFV) para inferência em tempo real, embeddings de 384 dimensões, amostragem dinâmica de hard negatives e TensorBoard local.

**Importante:** este repositório faz fine-tuning de embeddings (SentenceTransformer + ContrastiveLoss), **não** fine-tuning de LLM causal com LoRA/QLoRA/PEFT/SFT/DPO. Não há RLHF, DPO, PPO ou alignment de LLM.

## Stack
- Python >=3.11 (`pyproject.toml`, `Dockerfile` python:3.11-slim)
- UV (gerenciador de pacotes, `uv.lock`)
- Docker, Kubernetes/KIND, Kubeflow Trainer v2.1.0
- Feast (feature store), Milvus (online store opcional, vector search)
- sentence-transformers, torch, transformers, tokenizers, datasets, accelerate, safetensors
- tensorboard, kubernetes, pydantic, pyyaml, requests

## Fine-tuning LLM
Não é fine-tuning de LLM causal. É **fine-tuning de embeddings**:
- `prepare_training_data.py` — `TrainingDataPreparer`: gera pares positivo/negativo/hard negative usando `SentenceTransformer` + `cos_sim`, exporta parquet compatível com Feast
- `kubeflow_embedding_training.py` — `hybrid_embedding_training`: treino distribuído PyTorch DDP + Kubeflow Trainer, `ContrastiveLoss`, hard negatives dinâmicos, avaliação por similaridade cosseno, salvamento do modelo
- Loss: `ContrastiveLoss(model=model)`; otimizador Adam (lr 2e-6); distribuição `torch.distributed` backend `gloo` + `DistributedSampler`

## RAG
**SIM.** Infraestrutura RAG com embeddings:
- `feature_repo/wiki_features.py` — FeatureView `wiki_passages` (texto + embeddings 384-d, vector_index=True, COSINE, online=True com Milvus)
- `feature_repo/training_data_features.py` — FeatureViews `embedding_training_pairs` (offline) e `query_embeddings` (online, 384-d, COSINE)
- `feature_repo/chunk_parquet_data.py` — chunking de texto para parquet (max_chars=380, compatível com limite varchar do Milvus)
- `feature_store.yaml` — online store Milvus (127.0.0.1:19530, 384-d, IVF_FLAT, COSINE), offline store file
- Modelo de embedding: `sentence-transformers/all-MiniLM-L6-v2` (384 dims); alternativas citadas: `all-mpnet-base-v2`, `paraphrase-multilingual-MiniLM-L12-v2`

## Pós-treino / alinhamento
Não identificado. Não há RLHF, DPO, PPO, alignment, reward modeling. O "pós-treino" aqui se limita a re-embedding do corpus com o modelo de embeddings fine-tuned (arquivo `re_embed_wikipedia.py` citado no README, mas **não existente**).

## Inferência / serving
Apenas inferência de **embeddings** (SentenceTransformer `.encode()`), não inferência de LLM generativo:
- Feast ODFV para serving em tempo real de query embeddings (conceitual; arquivo `fine_tuned_embedding_odfv.py` citado no README, mas **não existente**)
- `kubeflow_embedding_training.py` carrega modelo fine-tuned e salva (`model.save()` → config.json, pytorch_model.bin, tokenizer.json)
- `Dockerfile` pré-baixa `all-MiniLM-L6-v2` no build

## Artefatos de treino
- `feature_repo/data/train-00000-of-00157_sample.parquet` e `..._with_timestamp_chunked.parquet` (dados de amostra Wikipedia)
- Outputs esperados em `training_outputs/` (não existem; gerados em runtime)
- Modelo salvo em `cached_model/` (não existe; gerado em runtime)

## Evidência-chave
- `prepare_training_data.py` (linhas 25, 45, 71, 109, 188, 237, 261, 301)
- `kubeflow_embedding_training.py` (linhas 16, 155, 190, 247, 294, 383, 665, 871)
- `deploy_kubeflow_training.py` (linhas 323, 276, 228, 85, 393, 441, 487)
- `feature_repo/wiki_features.py`, `training_data_features.py`, `chunk_parquet_data.py`
- `feature_store.yaml`, `training-storage.yaml`
- `Dockerfile`, `docker-compose.yml`, `setup-kind-kubeflow.sh`
- `pyproject.toml`, `requirements.txt`, `uv.lock`

## Lacunas / limites
- **Bugs críticos corrigidos nesta missão:** `feature_repo/__init__.py` importava módulos `fine_tuned_wiki_features` e `fine_tuned_embedding_odfv` que **não existem** → `ModuleNotFoundError` ao importar o pacote ou rodar `feast apply`. Removidas essas imports e as entradas em `__all__`.
- README cita arquivos que **não existem**: `re_embed_wikipedia.py`, `test_end_to_end.py`, `feature_repo/fine_tuned_wiki_features.py`, `feature_repo/fine_tuned_embedding_odfv.py`, `registry.db`, `embedding_training_data.parquet`, `query_embeddings.parquet`, `wiki_fine_tuned_embeddings.parquet`, pastas `training_outputs/`, `cached_model/`, `.venv/`.
- `feature_repo/__init__.py` ainda importava esses módulos inexistentes (corrigido).
- Caminho hardcoded no fallback de parquet em `kubeflow_embedding_training.py` (`/Users/farceo/dev/...`).
- Divergências de versão entre `pyproject.toml` e `requirements.txt` (kubeflow 0.1.0 vs 0.2.0; sentence-transformers >=5.1.0 vs >=3.0.0; datasets ==3.6.0 vs >=3.0.0).
- Não há testes automatizados.
- Não há `.gitignore` identificado.

## Correções aplicadas
- `feature_repo/__init__.py`: removidas imports de `fine_tuned_wiki_features` e `fine_tuned_embedding_odfv` (módulos inexistentes) e entradas correspondentes em `__all__` (esta missão).

## Correções sugeridas
- Criar os arquivos ausentes citados no README (`re_embed_wikipedia.py`, `test_end_to_end.py`, `fine_tuned_wiki_features.py`, `fine_tuned_embedding_odfv.py`) — nova funcionalidade.
- Corrigir caminho hardcoded em `kubeflow_embedding_training.py`.
- Alinhar versões entre `pyproject.toml` e `requirements.txt`.
- Adicionar `.gitignore` e testes automatizados.