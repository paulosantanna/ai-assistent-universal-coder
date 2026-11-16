# Nota de mapeamento — rag-and-fine-tuning-demo

**Caminho:** `02_repositorios/rag-and-fine-tuning-demo`  
**Updated:** 2026-10-20  
**Tipo:** Demo comparativo: Direct LLM vs RAG vs Fine-Tuned (Gemma LoRA) vs Hybrid  
**Status no Beta 2.0:** NOVO (não estava no Beta 1.x)  
**Contato:** hereandnowai.com, info@hereandnowai.com

## Propósito
Demonstração completa e comparativa de três abordagens para especializar um LLM em domínio específico:
1. **RAG (Retrieval-Augmented Generation):** acesso "open-book" a documentos específicos.
2. **Fine-Tuning:** retreinamento de pesos para internalizar conhecimento de domínio.
3. **Hybrid AI Systems:** combinação de RAG + Fine-Tuning.

O domínio de exemplo é o perfil profissional de Ruthran Raghavan, Chief AI Scientist da HERE AND NOW AI.

## Stack
- Python (versão não declarada explicitamente)
- langchain, langchain-ollama, langchain-huggingface, langchain-community, langchain-text-splitters
- faiss-cpu (vector store)
- transformers, peft, accelerate, datasets, trl, sentence-transformers, torch
- gradio (interface web)
- pandas, tqdm
- Ollama local (modelo `gpt-oss:20b`)
- Modelo de embeddings: `sentence-transformers/all-MiniLM-L6-v2` (384 dims)
- Modelo base fine-tunado: `google/gemma-3-270m`

## Fine-tuning LLM
**SIM.** Fine-tuning de Gemma-3-270m com LoRA + SFT:
- `fine_tuning/train_gemma.py` — `LoraConfig` (r=16, alpha=32, target_modules q/o/k/v_proj, gate/up/down_proj, task_type="CAUSAL_LM"), `SFTConfig` (batch 4, grad_accum 2, lr 1e-4, max_steps 100, bf16, gradient_checkpointing, max_length 512), `SFTTrainer` da TRL
- `fine_tuning/prepare_data.py` — geração sintética de 9 exemplos Q&A (Instruction-Context-Response)
- `fine_tuning/training_data.json` — 9 exemplos estáticos

**Correção aplicada (esta missão):**
- Removido caminho hardcoded `/Users/hnai/Downloads/...` (L15). O caminho do dataset agora se resolve por: argumento da função `train_gemma()` > variável de ambiente `GEMMA_TRAINING_DATA` > caminho relativo `fine_tuning/training_data.json`.
- A função agora aceita parâmetros opcionais `dataset_path` e `use_cuda`.
- Seleção de dtype/device: CUDA (bf16, device_map="auto") > MPS (bf16, device_map="auto") > CPU (float32, device_map=None). Anteriormente estava otimizado apenas para Apple Silicon MPS.

## RAG
**SIM.** Pipeline RAG completo:
- `rag/rag_system.py` — `setup_rag()`: TextLoader → CharacterTextSplitter (chunk_size=1000, overlap=200) → HuggingFaceEmbeddings (all-MiniLM-L6-v2) → FAISS.from_documents → OllamaLLM (gpt-oss:20b) → create_retrieval_chain / create_stuff_documents_chain
- `chatbot_app.py` — `_get_rag_chain()` / `_query_rag()` com lazy loading

## Pós-treino / alinhamento
Não identificado. Não há DPO, PPO, RLHF, reward modeling ou alinhamento de preferências. Apenas SFT (fine-tuning supervisionado com LoRA).

## Inferência / serving
Quatro modalidades no `chatbot_app.py` (Gradio):
1. Direct LLM (gpt-oss:20b via Ollama, sem contexto)
2. RAG (gpt-oss:20b + chunks recuperados do FAISS)
3. Fine-Tuned (Gemma-3-270m com adapter LoRA via `AutoPeftModelForCausalLM` + `model.generate()`)
4. Hybrid (FT + RAG)
- Porta 7861 (conforme walkthrough)
- Mediçao de latência de resposta

## Artefatos de treino
- `fine_tuning/training_data.json` (9 exemplos)
- Saída esperada: `./gemma_finetuned` e `./gemma_finetuned_final` (pastas de output, não existem no repositório; geradas ao rodar o treino)

## Evidência-chave
- `fine_tuning/train_gemma.py` (corrigido nesta missão)
- `fine_tuning/prepare_data.py`
- `rag/rag_system.py`
- `chatbot_app.py`
- `DEMO_WALKTHROUGH.md` (710 linhas, guia educacional)
- `evaluation/comparison_report.md` (métricas comparativas)
- `requirements.txt` (18 dependências, sem versões fixas)

## Lacunas / limites
- `requirements.txt` sem versões fixas → reproduzibilidade comprometida.
- Vários caminhos hardcoded em `rag/rag_system.py` (L14) e `fine_tuning/prepare_data.py` (L84-85) para ambiente original do autor (`/Users/hnai/...`).
- `train_gemma.py` usava `torch.backends.mps.is_available()` (apenas Apple Silicon) — corrigido para CUDA/MPS/CPU.
- Não há QLoRA, DPO, PPO, RLHF, reranking, query expansion, hybrid search.
- Não há CI/CD, testes unitários, Dockerfile.
- Pastas `gemma_finetuned/` e `gemma_finetuned_final/` estão no `.gitignore` (não existem no repo).

## Correções aplicadas
- `fine_tuning/train_gemma.py`: caminho de dataset parametrizado + detecção CUDA/MPS/CPU (esta missão).

## Correções sugeridas
- Fixar versões em `requirements.txt`.
- Tornar caminhos em `rag/rag_system.py` e `prepare_data.py` relativos/configuráveis.
- Adicionar testes unitários.