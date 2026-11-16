# Estudo: RAG + Fine-tuning com NVIDIA Nemotron 3.5 Super na Cloud (sem hardware local)

**Data:** 30/10/2026  
**Fonte primária:** docs.nvidia.com (Nemotron + NIM), research.nvidia.com, huggingface.co/nvidia, developer.nvidia.com, blogs.nvidia.com  
**Modelo alvo:** NVIDIA-Nemotron-3.5-Super-VL-120B-A12B (120B total / 12B ativos, MoE híbrido Mamba-Transformer, visão-linguagem, MTP)

---

## 1. Resumo executivo

Você quer:
1. **Treinar/fine-tunar um LLM opensource (Nemotron 3.5 Super) sem usar seu hardware local** — ou seja, usar GPU alugada na nuvem.
2. **Armazenar os dados/modelo treinados localmente** durante o desenvolvimento.
3. **Subir o LLM e o banco vetorial para a nuvem** e continuar RAG + fine-tuning via API (NVIDIA NIM / OpenAI-compatible).

Esta é uma estratégia **híbrida desenvolv → nuvem**: desenvolvimento/training em GPU cloud alugada, checkpoint salvo localmente, depois deploy como NIM self-hosted ou na nuvem com API estável.

---

## 2. O que é o Nemotron 3.5 Super

| Item | Detalhe |
|------|---------|
| Nome | Nemotron-3.5-Super-VL-120B-A12B |
| Tipo | Open weights, visão-linguagem (VLM), híbrido Mamba-Transformer + MoE |
| Parâmetros | 120B total / 12B ativos |
| Contexto | até 1M tokens (long-context recovery) |
| Multi-Token Prediction (MTP) | nativo, 2 camadas compartilhadas |
| Licença | OpenMDW-1.1 (pesos abertos, datasets abertos, receitas abertas) |
| Checkpoints | BF16 (base e pós-treinado), NVFP4 (quantizado) |
| Hugging Face | `nvidia/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-BF16`, `...-NVFP4` |
| Engines de inferência | vLLM, SGLang, TensorRT-LLM, NIM |
| Hardware suportado | Blackwell (GB200/GB300), Hopper (H100/H200), Ampere (A100), DGX Spark/Station, RTX |

> **Importante:** os dados de SFT e RL usados no modelo publicado da NVIDIA não são todos open-source (alguns estão "pending open-source release"). Você deve usar **seus próprios dados** para fine-tuning.

---

## 3. Estratégia híbrida: treinar sem hardware local, armazenar localmente, subir para nuvem

### 3.1. Treinar sem hardware local (cloud GPU)

Como você **não quer usar seu hardware local**, alugue GPU na nuvem apenas para o tempo de treino:

| Opção | Descrição |
|-------|-----------|
| **NVIDIA DGX Cloud** | Executor oficial das receitas Nemotron (Slurm, run:ai, Lepton). Ideal para SFT/RL de larga escala. |
| **CSP Partners (AWS/Azure/GCP/OCI)** | Instâncias com GPU NVIDIA (H100, B200, etc.) rodando NIM container. |
| **Brev GPU instance** | Instâncias GPU sob demanda compatíveis com NIM. |
| **VPS/cloud genérica com GPU** | Qualquer instância Linux + NVIDIA GPU + Docker. |

**Fluxo:**
1. Alugue instância GPU na nuvem (ex: 1× ou 4× H100/B200).
2. Baixe o checkpoint base Nemotron 3.5 Super do Hugging Face.
3. Rode fine-tuning (SFT/LoRA/RL) com seus dados na instância alugada.
4. Salve os pesos treinados (`.safetensors`, `model.safetensors.index.json`, config, tokenizer) num volume persistente.
5. **Baixe esse volume para seu disco local** → agora você tem o modelo treinado armazenado localmente, sem ter usado seu hardware para treinar.

### 3.2. Armazenar localmente os dados treinados

Estrutura recomendada local:

```
modelos-treinados/
  nemotron-3-5-super-meu-dominio/
    model.safetensors.index.json
    model-00001-of-0000X.safetensors  (shards)
    config.json
    tokenizer.json / tokenizer.model
    generation_config.json
    runtime_config.json  (se for servir com NIM)
    README.md  (dados de treino, data cut, métricas)
```

Não coloque credenciais (NGC_API_KEY, AWS keys) nos arquivos locais.

### 3.3. Subir o LLM e o banco para a nuvem (RAG + fine-tuning contínuo)

Depois de ter o checkpoint treinado localmente:

1. **Suba o modelo para um bucket/cloud storage** (S3, GCS, OCI Object Storage, ou NGC) ou diretamente para a instância GPU na nuvem.
2. **Sirva com NVIDIA NIM** (container) naquela instância cloud:
   - Cria um model store a partir do profile NIM.
   - Substitui os pesos pelos seus (fine-tuned checkpoint).
   - Roda o container com `NIM_MODEL_PATH=/model-store`.
3. **API disponível:** endpoint OpenAI-compatible (`/v1/chat/completions`, `/v1/embeddings`) na nuvem.
4. **Banco vetorial:** suba o índice vetorial (LanceDB, Chroma, Qdrant, Milvus, etc.) para a nuvem também, ou use NeMo Retriever + Retriever NIM.

Assim você continua RAG + fine-tuning **direto na nuvem via API**, sem tocar no hardware local.

---

## 4. Fine-tuning do Nemotron 3.5 Super (receitas NVIDIA)

As receitas oficiais usam **NeMo + Megatron-Bridge** e rodam em cluster GPU (Slurm / DGX Cloud / local-docker).

### 4.1. Instalação das receitas

```bash
git clone https://github.com/NVIDIA-NeMo/Nemotron
cd Nemotron
uv sync
```

### 4.2. Pipeline de treinamento (Super 3.5)

| Stage | Nome | Propósito | Comando (resumido) |
|-------|------|-----------|-------------------|
| 0 | Pretraining (opcional) | Visão-linguagem (image-caption) | `uv run nemotron super35 pretrain --run CLUSTER` |
| 1 | SFT (estágio 1) | Supervised fine-tuning amplo (visão, raciocínio, chat, longo contexto, segurança, agente) | `uv run nemotron super35 data import sft /dados/estagio1` → `uv run nemotron super35 sft --run CLUSTER` |
| 1b | SFT (estágio 2) | Re-peso do blend | `uv run nemotron super35 data import sft /dados/estagio2 --name ...` → `uv run nemotron super35 sft --run CLUSTER` |
| 2 | RL (RLVR/RLHF/MOPD) | Reinforcement learning (raciocínio, agente, alinhamento) | `uv run nemotron super35 rl --run CLUSTER` |
| 3 | Eval | Avaliação | `uv run nemotron super35 eval` |
| — | Quantization | PTQ + QAD → NVFP4 | receita de quantização |

**Dados:** formato **Energon** (dataset da NVIDIA). Você importa seus próprios dados SFT/RL.

### 4.3. Fine-tuning leve (LoRA) — alternativa mais acessível

Para domínios específicos sem treinar todos os pesos:

- **LoRA Text2SQL** (receita Nemotron 3 Super): https://github.com/NVIDIA-NeMo/nemotron/tree/main/usage-cookbook/Nemotron-3-Super/lora-text2sql
- **NeMo AutoModel** + LoRA
- **Unsloth**: fine-tuning eficiente (memória reduzida) — https://unsloth.ai/docs/models/nemotron-3
- **ms-swift** (ModelScope): fine-tuning do Nemotron 3.5 Super VL — https://modelscope.ai/collections/nv-community/Nemotron-35-Super-VL

### 4.4. Estimativa de custo/compute

Use a **Nemotron Post-training Calculator**: https://docs.nvidia.com/nemotron/nightly/train-models/sizing-calculator.html  
Estima GPU count, tempo de treino e custo de compute para SFT, LoRA ou GRPO.

> Full-weight SFT do Super 3.5 exige cluster multi-GPU (H100/B200). LoRA pode rodar em menos GPUs.

---

## 5. RAG com Nemotron (NeMo Retriever + NIM)

### 5.1. Componentes do RAG NVIDIA

| Componente | Função | Modelo / NIM |
|------------|--------|--------------|
| **Embedding** | Converte texto/chunks em vetores | Nemotron-3-Embed-1B-BF16 (dim 2048, seq 512) |
| **Reranking** | Reordena trechos recuperados por relevância | Nemotron Reranker (cross-encoder) |
| **LLM (geração)** | Responde com contexto recuperado | Nemotron 3.5 Super (via NIM API) |
| **Extração** | OCR, tabelas, gráficos, infográficos | NeMo Retriever Extraction / Image OCR NIM |
| **Banco vetorial** | Armazena vetores | LanceDB (local), Qdrant/Milvus/Pinecone (nuvem) |

### 5.2. Pipeline RAG (6 estágios da receita Embed)

1. **SDG (Synthetic Data Generation):** LLM gera pares pergunta-resposta a partir de seus documentos (usa NVIDIA API por padrão, `NVIDIA_API_BASE_URL` configurável).
2. **Data Prep:** converte, mina hard negatives, unrolla dados.
3. **Finetune:** fine-tune do modelo de embedding (Nemotron 3 Embed) nos seus dados de domínio.
4. **Eval:** compara base vs fine-tuned (nDCG, Recall, Precision@k, MAP@k).
5. **Export:** checkpoint consolidado.
6. **Deploy:** serve com **Retriever NIM** ou **vLLM** (`NIM_MODEL_PATH=/model`).

### 5.3. Exemplo RAG com LangChain + NeMo Retriever Embedding NIM

```python
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Embedding via NIM (self-hosted ou build.nvidia.com)
embedding_model = NVIDIAEmbeddings(
    model="nvidia/nemotron-3-embed-1b",
    base_url="http://localhost:8000/v1",  # ou https://integrate.api.nvidia.com/v1
)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
document_chunks = text_splitter.split_documents(documentos)

page_contents = [doc.page_content for doc in document_chunks]
vectors = embedding_model.embed_documents(page_contents)  # armazene no banco vetorial
```

### 5.4. NeMo Retriever Library (ingestão local, sem container)

```python
pip install nemo-retriever
# pipeline: files -> extract -> embed -> vdb_upload (LanceDB local ou S3)
```

Pode rodar localmente (Linux + CUDA) ou chamar NIM remoto via `embed_invoke_url`.

---

## 6. Servir o modelo fine-tunado na nuvem com NVIDIA NIM

O NIM permite servir **seu próprio checkpoint fine-tunado** mantendo a engine (vLLM/SGLang/TRT-LLM) e a API OpenAI-compatible.

### 6.1. Workflow "Deploy a Fine-Tuned Checkpoint"

```bash
# 1. Escolha o profile para sua GPU e precisão (use BF16 profile para fine-tune BF16)
export MODEL_STORE=/caminho/para/model-store

# 2. Cria o model store a partir do profile NIM
docker run --rm --gpus=all \
  -e NGC_API_KEY=$NGC_API_KEY \
  -v "$LOCAL_NIM_CACHE:/opt/nim/.cache" \
  -v "$MODEL_STORE:/model-store" \
  ${NIM_LLM_IMAGE} create-model-store --model nemotron-3.5-super-vl-120b-a12b

# 3. Substitua os pesos pelos seus (fine-tuned checkpoint)
#    Copie *.safetensors, model.safetensors.index.json, config, tokenizer
#    Mantenha runtime_config.json

# 4. Rode o NIM contra o store
docker run --gpus=all \
  -e NIM_MODEL_PATH=/model-store \
  -v "$MODEL_STORE:/model-store" \
  -p 8000:8000 \
  ${NIM_LLM_IMAGE}
```

### 6.2. Variáveis importantes

| Variável | Função |
|----------|--------|
| `NIM_MODEL_PATH` | Caminho para o model store local ou remoto (`ngc://`, `hf://`, `s3://`, `gs://`) |
| `NGC_API_KEY` | Credencial NVIDIA para baixar containers/profiles |
| `NIM_TENSOR_PARALLEL_SIZE` / `NIM_PIPELINE_PARALLEL_SIZE` | Paralelismo de inferência |
| `NIM_SPECDEC_ENABLE` | Desativar speculative decoding se o fine-tune não atualizou MTP |
| `LOCAL_NIM_CACHE` | Cache local de modelos NIM |

### 6.3. API disponível (OpenAI-compatible)

Após subir o NIM na nuvem, você tem endpoint:

```
POST https://<seu-endpoint-cloud>/v1/chat/completions
Authorization: Bearer <NGC_API_KEY ou token do endpoint>
Content-Type: application/json

{
  "model": "nemotron-3.5-super-vl",
  "messages": [...],
  "temperature": 0.7,
  "max_tokens": 8192
}
```

Também:
- `/v1/embeddings` (para RAG)
- Endpoints de health: `/health`, `/v1/models`

### 6.4. Hospedagem do NIM na nuvem

- **build.nvidia.com:** API hospedada da NVIDIA (free tier para prototipagem, depois rate limits). Modelo: `nvidia/nemotron-3.5-super-vl-120b-a12b`.
- **Self-hosted NIM:** container rodando em sua instância cloud (AWS/Azure/GCP/OCI, DGX Cloud, Brev). API idêntica, sem mudança de código.
- **Docker Agent / OpenCode:** podem usar o NIM como provider com `base_url` customizado.

---

## 7. Arquitetura recomendada (seu caso)

Fase 1 — Desenvolvimento / Treino (sem hardware local):

```
[Seu PC local]  <-- baixa/checkpoint salvo <--  [Instância GPU alugada na nuvem]
                                                    |
                                                    | fine-tuning Nemotron 3.5 Super
                                                    | (NeMo + Megatron-Bridge / LoRA / Unsloth)
                                                    | dados: seus documentos (Energon)
                                                    |
                                            [Banco vetorial local: LanceDB/Chroma]
                                                    |
                                            [Embedding Nemotron 3 Embed fine-tunado]
```

Fase 2 — Produção na nuvem (RAG + fine-tuning contínuo via API):

```
[Seu app / usuário]  -->  API NIM (OpenAI-compatible) na nuvem
                              |
                      [Nemotron 3.5 Super fine-tunado]  [Retriever NIM / Embedding NIM]
                              |                           |
                      [Banco vetorial na nuvem]  <-- dados atualizados
```

**Fluxo contínuo:**
1. Usuário faz pergunta → API NIM do Nemotron 3.5 Super (fine-tunado).
2. Sistema recupera contexto do banco vetorial na nuvem (Retriever NIM + Embedding fine-tunado).
3. LLM responde com RAG.
4. Periodicamente, novos dados → novo fine-tuning (LoRA ou full SFT) na nuvem → novo checkpoint → substitui pesos no NIM (`NIM_MODEL_PATH`).

---

## 8. Ferramentas e receitas oficiais (links)

| Finalidade | Link |
|------------|------|
| Nemotron 3.5 Super Training Recipe | https://docs.nvidia.com/nemotron/latest/nemotron/super35/README.html |
| Deploy Fine-Tuned Checkpoint (NIM) | https://docs.nvidia.com/nim/large-language-models/latest/get-started/advanced/get-started-nemotron-3.5-super-vl.html |
| Nemotron Post-training Calculator | https://docs.nvidia.com/nemotron/nightly/train-models/sizing-calculator.html |
| NeMo Retriever Embedding NIM | https://docs.nvidia.com/nim/nemo-retriever/text-embedding/latest/overview.html |
| NeMo Retriever Library | https://pypi.org/project/nemo-retriever/ |
| NVIDIA RAG Blueprint | https://github.com/NVIDIA-AI-Blueprints/rag/ |
| Hugging Face Nemotron | https://huggingface.co/nvidia (NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-BF16 / -NVFP4) |
| build.nvidia.com (API NIM hospedada) | https://build.nvidia.com/nvidia/nemotron-3.5-super-vl-120b-a12b |
| Nemotron GitHub (cookbooks) | https://github.com/NVIDIA-NeMo/Nemotron |
| Unsloth Nemotron | https://unsloth.ai/docs/models/nemotron-3 |
| ms-swift Nemotron 3.5 Super VL | https://modelscope.ai/collections/nv-community/Nemotron-35-Super-VL |

---

## 9. Checklist de execução

- [ ] Criar conta NVIDIA Developer e gerar `NGC_API_KEY`
- [ ] Alugar instância GPU na nuvem (DGX Cloud, AWS/Azure/GCP com H100/B200, ou Brev)
- [ ] Baixar checkpoint base Nemotron 3.5 Super BF16 do Hugging Face
- [ ] Preparar dados de treino no formato Energon (para SFT) ou JSONL (para LoRA/Unsloth)
- [ ] Rodar fine-tuning (SFT ou LoRA) na instância alugada
- [ ] Salvar pesos treinados (`.safetensors`, config, tokenizer) e baixar para armazenamento local
- [ ] Criar/fine-tunar modelo de embedding Nemotron 3 Embed para seu domínio (RAG)
- [ ] Indexar documentos no banco vetorial local (LanceDB/Chroma)
- [ ] Subir modelo + banco vetorial para a nuvem
- [ ] Subir container NIM com `NIM_MODEL_PATH` apontando para seu checkpoint fine-tunado
- [ ] Validar API `/v1/chat/completions` e `/v1/embeddings`
- [ ] Integrar aplicação ao endpoint NIM na nuvem (RAG + LLM)
- [ ] Definir ciclo de re-treino contínuo na nuvem (novos dados → novo checkpoint → deploy NIM)

---

## 10. Riscos e observações

1. **Fine-tuning full-weight do Super 3.5 é pesado:** exige cluster multi-GPU (H100/B200). Se o orçamento for limitado, use **LoRA** ou treine apenas o **embedding** para RAG.
2. **Dados de SFT/RL oficiais não são todos abertos:** use seus próprios dados; os resultados diferirão dos benchmarks publicados.
3. **NVFP4:** se for servir com NIM NVFP4, quantize o fine-tuned checkpoint para NVFP4 antes.
4. **MTP/speculative decoding:** se o fine-tune não manter as camadas MTP, desative `NIM_SPECDEC_ENABLE=false`.
5. **Credenciais:** nunca salve `NGC_API_KEY`, AWS keys ou cookies em arquivos do repositório. Use variáveis de ambiente ou secret manager da nuvem.
6. **Licença:** OpenMDW-1.1 permite uso comercial e customização, mas leia os termos do container NIM e dos pesos separadamente.

---

## 11. Mapeamento 3.0 do workspace (resumo)

O workspace `E:\Github\ai-assistent-universal-coder` é **um único repositório Git** contendo:

- **ECOSISTEMA DE SKILLS:** `00_skills/` (316 skills), `skills/` (209 skills mirror), `.agents/skills/` (319 skills)
- **MCPs:** `kinghost-control-mcp`, `kinghost-commerce-mcp`, `continuous-training-mcp`, `rag-graph-laya-mcp`, `dark-videos-pipeline-mcp`
- **PROJETOS:** `science-studio/`, `quality/`, `.tools/tlc-ci-upstream/` (sub-repo com `.git` próprio — Tech Leads Club Agent Skills)
- **MAPEAMENTOS:** `07_mapeamentos/` com `mapeamento-beta-3.0.0/` (17 diretórios, 9.152 arquivos hashados)
- **REPOS CLONADOS:** `02_repositorios/` (inclui `rag-and-fine-tuning-demo`, `enterprise-llm-finetuning`, `post_training_llms`, etc. — somente leitura)
- **NOTEBOOK:** `.notebook/` com HANDOFF, MEMORY, PROGRESS, LEARNING + notas de domínio
- **GOVERNANÇA:** `AGENTS.md` (canônico, byte-identical), `docs/`, `.specs/`, `.github/workflows/`

Este estudo pode ser integrado ao seu fluxo existente, especialmente às pastas `02_repositorios/` (já tem demos de RAG/fine-tuning) e `07_mapeamentos/` (para catalogar o novo fluxo Nemotron).
