# Nota de mapeamento — enterprise-llm-finetuning

**Caminho:** `02_repositorios/enterprise-llm-finetuning`  
**Updated:** 2026-10-20  
**Tipo:** Aplicação de fine-tuning corporativo de LLM (arquitetura Clean/Hexagonal)  
**Status no Beta 2.0:** NOVO (não estava no Beta 1.x)

## Propósito
Pipeline de fine-tuning de LLMs com foco enterprise: ingestão de datasets, pré-processamento com chat templates, carregamento de modelo base com quantização 4-bit, aplicação de adapters LoRA/QLoRA, treinamento via TRL/HF Trainer, avaliação determinística com delta metrics (base vs fine-tuned), quality gates e registro de artefatos (safetensors, merge de LoRA).

## Stack
- Python 3.13 (`.python-version`)
- Hugging Face Transformers 5.14.1, PEFT 0.19.1, TRL 1.8.0, PyTorch 2.13.0, Datasets 5.0.0, Tokenizers 0.22.2
- accelerate, bitsandbytes, datasets, peft, prometheus-client, structlog, wandb, transformers, trl
- YAML (configuração), pydantic v2 (schemas)
- vLLM (serving, planejado em ADR, não implementado em código)

## Fine-tuning LLM
**SIM.** Técnicas implementadas:
- **SFT** (Supervised Fine-Tuning) via `TRL SFTTrainer` e `transformers.Trainer`
- **LoRA / QLoRA** via `peft.LoraConfig`, `get_peft_model`, `prepare_model_for_kbit_training`, gradient checkpointing
- Quantização 4-bit (bitsandbytes NF4, double quant, bfloat16 compute)
- FSDP e DeepSpeed (stage 2/3) para treino distribuído

Arquivos-chave:
- `src/application/usecases/train_pipeline.py` — orquestração end-to-end
- `src/application/usecases/train_model_usecase.py` — uso case atômico de treino
- `src/infrastructure/trainer/trl_trainer.py` — adapter TRL SFTTrainer
- `src/infrastructure/trainer/huggingface_trainer.py` — adapter transformers.Trainer
- `src/infrastructure/llm_model_loader/transformers_llm_model_loader.py` — carregamento 4-bit + LoRA
- `src/domain/schemas/config_schema.py` — schemas Pydantic v2 (PEFTConfig r=16/alpha=32, QuantizationConfig 4-bit NF4, TrainingArgs)
- `src/finetuning_config.yaml` — config de exemplo (Gemma-3-1B, QLoRA r=16, lr 2e-4, max_steps 100)
- `src/infrastructure/monitoring/prometheus_callback.py`, `prometheus_exporter.py`, `wandb_tracker.py` — observabilidade de treino

## RAG
Não identificado. Não há retrieval, embeddings, vector store, chunking ou retrieval chain.

## Pós-treino / alinhamento
Parcial. Não há implementação de DPO, PPO ou RLHF. O PRD (docs/phase_1_understand/01_prd_and_problem_statement.md) lista RLHF/PPO como **non-goal para v1.0**, alvo para v2.0. Existe avaliação comparativa base vs fine-tuned (`EvaluateModelUseCase` com `model.disable_adapter()` + delta metrics ΔEM, ΔF1, ΔROUGE-L).

## Inferência / serving
A inferência existe apenas dentro do `DeterministicEvaluator` (modo avaliação/batch, `model.generate()`). Não há servidor de inferência implementado (sem FastAPI, sem vLLM engine no código-fonte). O serving via vLLM está apenas nos ADRs/documentação (`docs/phase_5_decisions/0005-asynchronous-vllm-engine-for-production-serving.md`).

## Artefatos de treino
- `src/finetuning_config.yaml` — config de experimento completo
- Checkpoints esperados em `./gemma_finetuned_final` (conforme config registry: safetensors, save_merged_model true)
- Testes unitários em `tests/unit/` (test_train_model_usecase.py, test_trainer_factory.py, test_config_schema.py, etc.)

## Evidência-chave
- `pyproject.toml` (dependências de produção)
- `src/domain/schemas/config_schema.py` (PEFTConfig, QuantizationConfig, TrainingArgs)
- `src/application/usecases/train_pipeline.py`
- `src/infrastructure/monitoring/prometheus_exporter.py`

## Lacunas / limites
- Não há DPO, PPO ou RLHF implementado (v2.0 planejado).
- Não há servidor de inferência/serving implementado (apenas avaliação em batch).
- Não há RAG.
- CVE/EOL, runtime/MCP instalado, testes aprovados e implantação real não verificados.

## Correções aplicadas
Nenhuma (pipeline estruturado e funcional no escopo que se propõe).

## Correções sugeridas
Implementar DPO/RLHF (v2.0) e servidor de inferência vLLM — são nova funcionalidade, não correção de bug.