# Nota de mapeamento — post_training_llms

**Caminho:** `02_repositorios/post_training_llms`  
**Updated:** 2026-10-20  
**Tipo:** Kit educacional de pós-treino de LLM (baseado no curso DeepLearning.AI "Post-training LLMs")  
**Status no Beta 2.0:** NOVO (não estava no Beta 1.x)  
**Licença:** MIT (autor: Yan Cotta)

## Propósito
Implementação e recurso educacional para três técnicas modernas de pós-treino que aumentam capacidades e alinhamento de LLMs: **SFT** (instrução-following), **DPO** (alinhamento por preferências diretas) e **GRPO** (RL online com sinais de recompensa).

## Stack
- Python >=3.8 (setup.py; classifiers 3.8, 3.9, 3.10, 3.11)
- torch>=2.0.0, numpy>=1.24.0, transformers>=4.40.0, datasets>=2.0.0, trl>=0.8.0
- pandas, scikit-learn, pyyaml, tqdm, jinja2, markupsafe, rouge-score, evaluate
- accelerate (opcional, distributed training); jupyter, matplotlib, seaborn (opcional, notebooks)
- black, flake8, pytest (dev tools)

## Fine-tuning LLM
**SIM.** Técnicas implementadas (todas full-parameter, sem PEFT/LoRA/QLoRA):
- **SFT** — `src/training/sft_trainer.py` (`SFTTrainingPipeline` com `SFTTrainer`/`SFTConfig` da TRL)
- **DPO** — `src/training/dpo_trainer.py` (`DPOTrainingPipeline` com `DPOTrainer`/`DPOConfig`, parâmetro `beta`, pares chosen/rejected)
- **GRPO / RL online** — `src/training/rl_trainer.py` (`RLTrainingPipeline` com `GRPOTrainer`/`GRPOConfig`, reward function matemática `\boxed{}`, `num_generations`)

Arquivos-chave:
- `src/utils/model_utils.py` — `load_model_and_tokenizer`, `generate_responses` (inferência), `save_model_and_tokenizer`, `get_model_info`
- `src/utils/data_utils.py` — `prepare_sft_dataset`, `prepare_dpo_dataset`, `prepare_rl_dataset`, `create_identity_dataset`
- `src/utils/config.py` — sistema unificado de config (dataclasses: SFTConfig/DPOConfig/RLConfig + YAML)
- `src/evaluation/metrics.py` — métricas (accuracy, preference, identity consistency, toxicity, perplexity)
- `src/evaluation/benchmark.py` — `ModelBenchmark` (Q&A, matemática, identidade, segurança, perplexidade)
- `examples/run_sft.py`, `run_dpo.py`, `run_rl.py`, `run_benchmark.py` — scripts CLI
- `configs/sft_config.yaml`, `dpo_config.yaml`, `rl_config.yaml` — configs YAML
- `notebooks/01_supervised_fine_tuning.ipynb`, `02_direct_preference_optimization.ipynb`, `03_online_reinforcement_learning.ipynb` — tutoriais

## RAG
Não identificado. Nenhum componente de retrieval, embeddings, vector DB ou chunking.

## Pós-treino / alinhamento
**SIM.** Todo o repositório é focado em pós-treino:
- SFT (alignamento supervisionado)
- DPO (alignamento por preferência direta, alternativa ao RLHF sem reward model dedicado)
- GRPO (RL online com reward function)
- Não há menção explícita a RLHF com reward model separado.
- Não há PEFT/LoRA/QLoRA (busca negativa por esses termos).

## Inferência / serving
- `generate_responses()` em `src/utils/model_utils.py` (aplica `chat_template`, `model.generate()`, decodificação)
- `test_model_with_questions()` para teste de inferência
- `ModelBenchmark` para avaliação de inferência (latência, tamanho de resposta)
- Não há servidor de inferência dedicado (apenas inferência em batch/scripts de exemplo).

## Artefatos de treino
- `configs/*.yaml` (configs de treino)
- Checkpoints esperados em `models/` (criada em runtime, ignorada pelo .gitignore)
- Datasets: `banghua/DL-SFT-Dataset` (SFT), `mrfakename/identity` (DPO), `openai/gsm8k` (RL/math)
- Modelos: `HuggingFaceTB/SmolLM2-135M` / `135M-Instruct` / `1.7B`, `Qwen2.5-0.5B`, `Qwen2.5-1.5B`

## Evidência-chave
- `src/training/sft_trainer.py`, `dpo_trainer.py`, `rl_trainer.py`
- `src/utils/config.py` (sistema unificado de configuração)
- `src/evaluation/benchmark.py`
- `requirements.txt`, `setup.py`

## Lacunas / limites
- Não há PEFT/LoRA/QLoRA (fine-tuning full-parameter apenas; não é eficiente em parâmetros).
- Não há RAG.
- Não há reward model separado (DPO e GRPO são alternativas sem reward model dedicado).
- `python_requires>=3.8` pode ser restritivo para algumas dependências recentes.

## Correções aplicadas
Nenhuma (pipeline funcional para o escopo educacional).

## Correções sugeridas
Adicionar PEFT/LoRA/QLoRA (nova funcionalidade).