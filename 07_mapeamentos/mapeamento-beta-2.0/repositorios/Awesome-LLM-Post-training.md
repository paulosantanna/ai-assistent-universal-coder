# Nota de mapeamento — Awesome-LLM-Post-training

**Caminho:** `02_repositorios/Awesome-LLM-Post-training`  
**Updated:** 2026-10-20  
**Tipo:** Lista bibliográfica / "awesome list" (não é software executável de treino)  
**Status no Beta 2.0:** NOVO (não estava no Beta 1.x)

## Propósito
Coleção curada de papers, implementações, benchmarks e recursos sobre **Pós-treino de LLMs**. Vinculado ao survey paper "LLM Post-Training: A Deep Dive into Reasoning Large Language Models" (arXiv:2502.21321, aceito no IEEE TPAMI).

## Stack
Não há stack própria. Não há `pyproject.toml`, `requirements.txt`, `setup.py`, `package.json`, `Cargo.toml`. Apenas:
- `README.md` (362 linhas) — documentação principal
- `scripts/future_research_data.py` (101 linhas) — coleta de dados via API Semantic Scholar
- `scripts/deep_collection_sementic.py` (144 linhas) — coleta profunda de papers
- `assets/Keywords.csv` (70 keywords), `assets/2000+papers.json`, `assets/papers_temp_DEEP.json`
- `Images/` (logos, PDFs de apoio)

## Fine-tuning LLM
Conteúdo **bibliográfico apenas** (links para repositórios externos no README, L257-L277):
- **TRL (huggingface/trl):** SFT, PPO, GRPO, DPO (baseada em 🤗 Transformers)
- **LLaMA-Factory (hiyouga):** pre-training, multimodal fine-tuning, reward modeling, PPO, DPO, ORPO, **LoRA, QLoRA**, inferência via vLLM
- **veRL (volcengine):** PPO, GRPO, SFT, RLHF (escala até 70B)
- **trlX (CarperAI):** PPO, ILQL
- **RL4LMs (allenai):** RL modular para fine-tuning a preferências humanas
- **InstructLLaMA:** SFT e RLHF para LLaMA2
- **Okapi:** instruction tuning com RLHF, 26 idiomas, BLOOM e LLaMa

**Não há código de fine-tuning local.** Termos PEFT/LoRA/QLoRA/SFT/DPO aparecem apenas como descrição de repositórios externos.

## RAG
Conteúdo bibliográfico apenas:
- **RAG-Gym** (README L223): "Optimizing Reasoning and Search Agents with Process Supervision" (arXiv:2502.13957)

## Pós-treino / alinhamento
Conteúdo bibliográfico extenso:
- Survey principal: arXiv:2502.21321
- RLHF surveys, alignment techniques, reward learning / PRM (Math-Shepherd, Step-DPO, ReST-MCTS)
- Modelos citados: LLaMA2/3, DeepSeek-R1, Kimi k1.5, Qwen, Mistral, GPT-4/o1/o3, Gemini 2.0, BLOOM

## Inferência / serving
Não há código local. Menção indireta: LLaMA-Factory com "fast inference via API, Gradio UI, and CLI with vLLM workers".

## Artefatos de treino
Nenhum local. Apenas dois scripts Python de coleta de dados (não treinam modelos).

## Evidência-chave
- `README.md` — seções Papers, LLMs-in-RL, Reward Learning, Policy Optimization, RL & LLM Fine-Tuning Repositories (L257-L277)
- `scripts/future_research_data.py`, `scripts/deep_collection_sementic.py`

## Lacunas / limites
- Não é repositório de treinamento; não contém implementação própria de fine-tuning (PEFT/LoRA/QLoRA/SFT/DPO), RAG, inferência de LLM ou tokenização.
- Todo conteúdo técnico está em links externos.
- Não há declaração de dependências nem versão de Python.
- Discrepância de licença: badge diz MIT, texto da licença é CC BY-NC-SA 4.0.

## Correções aplicadas
Nenhuma (não há código de pipeline para corrigir).

## Correções sugeridas
Nenhuma aplicável (é lista bibliográfica; úteis como referência de estudo, não como base de execução).