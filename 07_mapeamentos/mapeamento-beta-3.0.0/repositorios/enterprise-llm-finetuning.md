# enterprise-llm-finetuning — beta 3.0.0

Updated: 2026-10-27
Entry point: [índice](../README.md) · [mapa estruturado](../mapa.json)

Arquivos com hash: 101; fingerprint: `370375aba76bee95058bd666ab9e2512a1e57189f0b767d7734d29c8545c57b7`.
Git próprio: True; HEAD: `c0fac5a162a14890d6555f5775cfa3f85ff763d1`; branch: `main`.
Estado local: há alterações/não rastreados; detalhes em inventory.json.

## Atualizações e reconciliação

DPO/PPO/retrieval FAISS estão na árvore local modificada. query devolve contexto, sem geração LLM; adaptador PPO exige reward_model e o pipeline padrão não o fornece. Presença de código não comprova execução fim a fim.

## Dimensões e evidências

### Propósito

**código presente** — Pipeline de fine-tuning com casos de uso e adaptadores configuráveis.

[enterprise-llm-finetuning/src/application/usecases/train_pipeline.py:31](../../../02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py)

### Arquitetura

**código presente** — Casos de uso dependem de interfaces de domínio; factories selecionam trainers.

[enterprise-llm-finetuning/src/infrastructure/factories/trainer_factory.py:15](../../../02_repositorios/enterprise-llm-finetuning/src/infrastructure/factories/trainer_factory.py)

### Fluxo

**código presente** — Configuração → dados → modelo/adaptador → treino opcional → avaliação opcional → resultado.

[enterprise-llm-finetuning/src/application/usecases/train_pipeline.py:59](../../../02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py)

### Dados

**código presente** — Schemas Pydantic incluem treinamento, DPO, PPO e RAG.

[enterprise-llm-finetuning/src/domain/schemas/config_schema.py:102](../../../02_repositorios/enterprise-llm-finetuning/src/domain/schemas/config_schema.py)

### Interfaces

**código presente** — CLI inclui opções de execução RAG.

[enterprise-llm-finetuning/src/presentation/cli.py:73](../../../02_repositorios/enterprise-llm-finetuning/src/presentation/cli.py)

### Configuração/deploy

**declarado** — Manifest Python declara dependências; instalação e compatibilidade não verificadas.

[enterprise-llm-finetuning/pyproject.toml:19](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml)

### Operação

**código presente** — Pipeline mede duração e publica métricas de avaliação no caminho W&B quando ativo.

[enterprise-llm-finetuning/src/application/usecases/train_pipeline.py:147](../../../02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py)

### Fine-tuning

**código presente** — SFT/LoRA/quantização têm adaptadores locais; treino não executado.

[enterprise-llm-finetuning/src/infrastructure/llm_model_loader/transformers_llm_model_loader.py:87](../../../02_repositorios/enterprise-llm-finetuning/src/infrastructure/llm_model_loader/transformers_llm_model_loader.py)

### RAG

**código presente** — FAISS IndexFlatIP, embeddings normalizados e chunking. query retorna contexto concatenado em answer; não gera resposta com LLM.

[enterprise-llm-finetuning/src/infrastructure/rag/faiss_rag_pipeline.py:244](../../../02_repositorios/enterprise-llm-finetuning/src/infrastructure/rag/faiss_rag_pipeline.py)

### Pós-treino

**código presente** — Adaptadores DPO e PPO presentes na árvore local modificada; funcionamento fim a fim não comprovado.

[enterprise-llm-finetuning/src/infrastructure/trainer/ppo_trainer.py:20](../../../02_repositorios/enterprise-llm-finetuning/src/infrastructure/trainer/ppo_trainer.py)

### Inferência

**código presente** — Pipeline padrão passa ppo_config mas não reward_model ao caso de uso; comparar a exigência do adaptador PPO antes de executar.

[enterprise-llm-finetuning/src/application/usecases/train_pipeline.py:347](../../../02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py)

### Tecnologias/versões

**declarado** — Ver declarações extraídas e manifests; versões instaladas e compatibilidade não verificadas.

[enterprise-llm-finetuning/pyproject.toml:20](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml)
[enterprise-llm-finetuning/pyproject.toml:21](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml)
[enterprise-llm-finetuning/pyproject.toml:24](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml)
[enterprise-llm-finetuning/pyproject.toml:26](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml)
[enterprise-llm-finetuning/pyproject.toml:27](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml)
[enterprise-llm-finetuning/pyproject.toml:28](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml)
[enterprise-llm-finetuning/pyproject.toml:29](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml)
[enterprise-llm-finetuning/pyproject.toml:30](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml)

### Vulnerabilidades

**não verificado** — Sem consulta de CVE/EOL nesta missão.


### Obsolescência

**não verificado** — Sem consulta de CVE/EOL nesta missão.


## Declarações de versão

| Manifest / declaração | Valor | Evidência |
|---|---|---|
| name | finetuning-basics | [enterprise-llm-finetuning/pyproject.toml:20](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| version | 0.1.0 | [enterprise-llm-finetuning/pyproject.toml:21](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| requires-python | >=3.13 | [enterprise-llm-finetuning/pyproject.toml:24](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| dependency | accelerate>=1.14.0 | [enterprise-llm-finetuning/pyproject.toml:26](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| dependency | bitsandbytes>=0.49.2 | [enterprise-llm-finetuning/pyproject.toml:27](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| dependency | datasets>=5.0.0 | [enterprise-llm-finetuning/pyproject.toml:28](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| dependency | dotenv>=0.9.9 | [enterprise-llm-finetuning/pyproject.toml:29](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| dependency | faiss-cpu>=1.11.0 | [enterprise-llm-finetuning/pyproject.toml:30](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| dependency | peft>=0.19.1 | [enterprise-llm-finetuning/pyproject.toml:31](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| dependency | prometheus-client>=0.20.0 | [enterprise-llm-finetuning/pyproject.toml:32](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| dependency | sentence-transformers>=5.1.0 | [enterprise-llm-finetuning/pyproject.toml:33](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| dependency | structlog>=24.0.0 | [enterprise-llm-finetuning/pyproject.toml:34](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| dependency | torch>=2.13.0 | [enterprise-llm-finetuning/pyproject.toml:35](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| dependency | transformers>=5.14.1 | [enterprise-llm-finetuning/pyproject.toml:36](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| dependency | trl>=1.8.0 | [enterprise-llm-finetuning/pyproject.toml:37](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| dependency | wandb>=0.20.0 | [enterprise-llm-finetuning/pyproject.toml:38](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |

## Qualidade e limites

Workflows: 0; arquivos candidatos a testes: 13. Não executados.

- Amostra semântica seletiva; hash e busca textual não equivalem a auditoria integral.
- Nenhum runtime, treino, publicação ou sincronização remota executado.
- Fontes modificadas/não rastreadas fazem parte deste snapshot local.
