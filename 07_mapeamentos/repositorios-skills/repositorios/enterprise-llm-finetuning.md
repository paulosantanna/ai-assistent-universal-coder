# enterprise-llm-finetuning — mapa estático de skills

Updated: 2026-11-16

Entry point: ../README.md

Tipo: Git próprio. Arquivos no inventário delimitado: 104; entradas excluídas: 12.

[Voltar ao índice](../README.md) · [Matriz completa](../matriz.csv)

## Dez dimensões

| Dimensão | Estado | Observação | Evidência |
| --- | --- | --- | --- |
| Tecnologias e versões | declarado | Declarações extraídas dos manifests, incluindo faixas e extras. Não são versões instaladas nem prova de compatibilidade. Lockfiles permanecem nas fontes para análise posterior. | [02_repositorios/enterprise-llm-finetuning/pyproject.toml:20](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml); [02_repositorios/enterprise-llm-finetuning/pyproject.toml:21](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml); [02_repositorios/enterprise-llm-finetuning/pyproject.toml:24](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml); demais fontes em mapa.json/declarações abaixo |
| Arquitetura | código presente | Casos de uso dependem de interfaces de domínio; factories selecionam trainers. | [02_repositorios/enterprise-llm-finetuning/src/infrastructure/factories/trainer_factory.py:15](../../../02_repositorios/enterprise-llm-finetuning/src/infrastructure/factories/trainer_factory.py) |
| Propósito | código presente | Pipeline de fine-tuning empresarial com casos de uso e adaptadores configuráveis. | [02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py:31](../../../02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py) |
| Fluxo | código presente | run() orquestra carga, preprocessamento, treino e avaliação opcional. | [02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py:59](../../../02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py) |
| Dados | código presente | Dataset loaders e preprocessadores são encadeados no pipeline. | [02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py:13](../../../02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py) |
| Configuração/deploy | declarado | pyproject declara dependências incluindo faiss-cpu; presença não comprova implantação. | [02_repositorios/enterprise-llm-finetuning/pyproject.toml:30](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| Operação/observabilidade | código presente | Logging de contexto no pipeline; telemetria de produção não verificada. | [02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py:26](../../../02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py) |
| Interfaces/dependências | código presente | FaissRAGPipeline e rag_pipeline_usecase expõem recuperação indexada. | [02_repositorios/enterprise-llm-finetuning/src/infrastructure/__init__.py:19](../../../02_repositorios/enterprise-llm-finetuning/src/infrastructure/__init__.py) |
| Vulnerabilidades | não verificado | Nenhuma consulta atual a advisories/scanner foi executada; não equivale a ausência de CVEs. | Sem verificação nesta missão |
| Obsolescência | não verificado | Datas de suporte/EOL não consultadas. Versões declaradas não comprovam suporte atual. | Sem verificação nesta missão |

## Declarações dos manifests

Faixas e extras são preservados; versões instaladas/resolvidas não foram verificadas.

| Declaração | Valor | Fonte |
| --- | --- | --- |
| name | finetuning-basics | [02_repositorios/enterprise-llm-finetuning/pyproject.toml:20](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| version | 0.1.0 | [02_repositorios/enterprise-llm-finetuning/pyproject.toml:21](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| requires-python | >=3.13 | [02_repositorios/enterprise-llm-finetuning/pyproject.toml:24](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| dependency | accelerate>=1.14.0 | [02_repositorios/enterprise-llm-finetuning/pyproject.toml:26](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| dependency | bitsandbytes>=0.49.2 | [02_repositorios/enterprise-llm-finetuning/pyproject.toml:27](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| dependency | datasets>=5.0.0 | [02_repositorios/enterprise-llm-finetuning/pyproject.toml:28](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| dependency | dotenv>=0.9.9 | [02_repositorios/enterprise-llm-finetuning/pyproject.toml:29](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| dependency | faiss-cpu>=1.11.0 | [02_repositorios/enterprise-llm-finetuning/pyproject.toml:30](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| dependency | peft>=0.19.1 | [02_repositorios/enterprise-llm-finetuning/pyproject.toml:31](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| dependency | prometheus-client>=0.20.0 | [02_repositorios/enterprise-llm-finetuning/pyproject.toml:32](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| dependency | sentence-transformers>=5.1.0 | [02_repositorios/enterprise-llm-finetuning/pyproject.toml:33](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| dependency | structlog>=24.0.0 | [02_repositorios/enterprise-llm-finetuning/pyproject.toml:34](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| dependency | torch>=2.13.0 | [02_repositorios/enterprise-llm-finetuning/pyproject.toml:35](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| dependency | transformers>=5.14.1 | [02_repositorios/enterprise-llm-finetuning/pyproject.toml:36](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| dependency | trl>=1.8.0 | [02_repositorios/enterprise-llm-finetuning/pyproject.toml:37](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |
| dependency | wandb>=0.20.0 | [02_repositorios/enterprise-llm-finetuning/pyproject.toml:38](../../../02_repositorios/enterprise-llm-finetuning/pyproject.toml) |

## Skills diretamente relacionadas

| Skill | Aplicação | Fonte |
| --- | --- | --- |
| [ai-architecture-expert](../../../00_skills/(architecture)/ai-architecture-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py:31](../../../02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py) |
| [ai-engineering-expert](../../../00_skills/(development)/ai-engineering-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py:31](../../../02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py) |
| [ai-evals-expert](../../../00_skills/(quality)/ai-evals-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py:31](../../../02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py) |
| [anti-hallucination-evaluator](../../../00_skills/(quality)/anti-hallucination-evaluator/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py:31](../../../02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py) |
| [bm25-expert](../../../00_skills/(development)/bm25-expert/SKILL.md) | Necessidade observada: rag. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/enterprise-llm-finetuning/src/infrastructure/__init__.py:19](../../../02_repositorios/enterprise-llm-finetuning/src/infrastructure/__init__.py) |
| [fine-tuning-expert](../../../00_skills/(development)/fine-tuning-expert/SKILL.md) | Necessidade observada: training. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py:31](../../../02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py) |
| [llm-model-selection-expert](../../../00_skills/(development)/llm-model-selection-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py:31](../../../02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py) |
| [lora-qlora-dora-expert](../../../00_skills/(development)/lora-qlora-dora-expert/SKILL.md) | Necessidade observada: training. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py:31](../../../02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py) |
| [python-bug-solver-skill](../../../00_skills/(development)/python-bug-solver-skill/SKILL.md) | Necessidade observada: python. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py:59](../../../02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py) |
| [python-expert](../../../00_skills/(development)/python-expert/SKILL.md) | Necessidade observada: python. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py:59](../../../02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py) |
| [python-rag-audit](../../../00_skills/(development)/python-rag-audit/SKILL.md) | Necessidade observada: rag. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/enterprise-llm-finetuning/src/infrastructure/__init__.py:19](../../../02_repositorios/enterprise-llm-finetuning/src/infrastructure/__init__.py) |
| [rag-expert](../../../00_skills/(development)/rag-expert/SKILL.md) | Necessidade observada: rag. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/enterprise-llm-finetuning/src/infrastructure/__init__.py:19](../../../02_repositorios/enterprise-llm-finetuning/src/infrastructure/__init__.py) |

## Uso condicionado

- **ai-continuous-training-maintainer**: Contrato fixa E:/GitHub/aidiabetic-research/src/, diferente deste alvo. Confirmar escopo e pipeline antes de reutilizar.
- **atualizar-dependencias**: Somente em missão de atualização com baseline e compatibilidade.
- **compatibility-analyzer**: Ao verificar troca de linguagem/runtime/dependência.
- **cve-advisory-sync**: Só ao solicitar consulta atual de advisories oficiais.
- **cve-remediation**: Requer CVE/GHSA concreto, versão afetada e correção autorizada.
- **dependency-updater**: Somente em atualização autorizada, preservando lockfiles.
- **eol-advisory-sync**: Requer consulta atual de suporte oficial para os produtos declarados.
- **gh-address-comments**: Requer comentários de PR e alvo concreto.
- **github-operations**: Ao operar GitHub com alvo, credenciais e autorização próprios.
- **local-secret-vault**: Só se a tarefa depender de credenciais autorizadas; não abrir para mapear.
- **observability-root-cause-integrator**: Requer incidente/sintomas e telemetria atual.
- **pr-reviewer**: Requer PR/diff concreto.
- **pr-reviewer-advanced**: Requer PR/diff concreto e evidências de revisão.
- **release-readiness-judge**: Requer release concreta e checks determinísticos.
- **revisar-seguranca-pr**: Requer diff de PR e escopo de segurança.
- **runtime-troubleshooting**: Requer runtime/logs atuais; o mapa é estático.
- **vuln-obsol-recon**: Inventário estático é ponto de partida; auditoria de CVE/EOL não foi executada.

## Testes/CI

13 arquivos candidatos por nome/caminho; não corresponde a quantidade de testes executados. 0 workflows encontrados. Suites não executadas.


## Lacunas

- DPO/PPO na árvore local modificada; execução fim a fim não demonstrada.
- query devolve contexto sem geração LLM no caminho padrão observado.
