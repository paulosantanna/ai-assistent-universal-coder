# DiabeticsresearchJEV — mapa estático de skills

Updated: 2026-10-13

Entry point: ../README.md

Tipo: Git próprio. Arquivos no inventário delimitado: 130; entradas excluídas: 12.

[Voltar ao índice](../README.md) · [Matriz completa](../matriz.csv)

## Dez dimensões

| Dimensão | Estado | Observação | Evidência |
| --- | --- | --- | --- |
| Tecnologias e versões | declarado | Declarações extraídas dos manifests, incluindo faixas e extras. Não são versões instaladas nem prova de compatibilidade. Lockfiles permanecem nas fontes para análise posterior. | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:10](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml); [02_repositorios/DiabeticsresearchJEV/pyproject.toml:21](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml); [02_repositorios/DiabeticsresearchJEV/pyproject.toml:22](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml); demais fontes em mapa.json/declarações abaixo |
| Arquitetura | observado | Camadas application/domain/infrastructure/interfaces; API REST e GraphQL usam serviços compartilhados. | [02_repositorios/DiabeticsresearchJEV/src/diabeticsresearchjev/interfaces/api.py:12](../../../02_repositorios/DiabeticsresearchJEV/src/diabeticsresearchjev/interfaces/api.py) |
| Propósito | declarado | Pesquisa biomédica em diabetes com coleta multilíngue, GraphRAG e treino contínuo QLoRA. | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:8](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| Fluxo | observado | run_full_cycle coleta, extrai grafo, indexa, treina, executa descoberta e avalia. | [02_repositorios/DiabeticsresearchJEV/src/diabeticsresearchjev/application/pipeline/full_cycle.py:31](../../../02_repositorios/DiabeticsresearchJEV/src/diabeticsresearchjev/application/pipeline/full_cycle.py) |
| Dados | documentado | MongoDB nativo e Chroma embutido são documentados; Compose descreve espelhos de serviços de dados. | [02_repositorios/DiabeticsresearchJEV/docker-compose.yml:8](../../../02_repositorios/DiabeticsresearchJEV/docker-compose.yml) |
| Configuração/deploy | documentado | Compose declara serviços locais; comentários de equivalência AWS são intenção, não prova de implantação AWS. | [02_repositorios/DiabeticsresearchJEV/docker-compose.yml:2](../../../02_repositorios/DiabeticsresearchJEV/docker-compose.yml) |
| Operação/observabilidade | observado | API oferece endpoint de saúde e página de métricas; operação real não medida. | [02_repositorios/DiabeticsresearchJEV/src/diabeticsresearchjev/interfaces/api.py:88](../../../02_repositorios/DiabeticsresearchJEV/src/diabeticsresearchjev/interfaces/api.py) |
| Interfaces/dependências | observado | HybridRetriever combina Chroma, BM25 e expansão opcional por grafo; GraphQL fica em /graphql. | [02_repositorios/DiabeticsresearchJEV/src/diabeticsresearchjev/application/rag/retriever.py:1](../../../02_repositorios/DiabeticsresearchJEV/src/diabeticsresearchjev/application/rag/retriever.py) |
| Vulnerabilidades | não verificado | Nenhuma consulta atual a advisories/scanner foi executada; não equivale a ausência de CVEs. | Sem verificação nesta missão |
| Obsolescência | não verificado | Datas de suporte/EOL não consultadas. Versões declaradas não comprovam suporte atual. | Sem verificação nesta missão |

## Declarações dos manifests

Faixas e extras são preservados; versões instaladas/resolvidas não foram verificadas.

| Declaração | Valor | Fonte |
| --- | --- | --- |
| name | diabeticsresearchjev | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:6](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| version | 0.2.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:7](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| requires-python | >=3.11 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:10](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | pydantic>=2.7.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:21](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | pydantic-settings>=2.3.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:22](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | fastapi>=0.111.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:23](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | uvicorn>=0.30.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:24](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | websockets>=12.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:25](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | httpx>=0.27.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:26](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | rich>=13.7.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:27](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | typer>=0.12.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:28](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | pymongo>=4.8.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:29](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | chromadb>=1.0.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:30](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | strawberry-graphql[fastapi]>=0.240.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:31](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | numpy>=1.26.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:32](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | networkx>=3.3 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:33](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | redis>=5.0.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:34](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | neo4j>=5.20.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:35](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | boto3>=1.34.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:36](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | pypdf>=4.2.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:37](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | fonttools>=4.40.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:38](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | beautifulsoup4>=4.12.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:39](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| dependency | lxml>=5.2.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:40](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:rag | sentence-transformers>=3.0.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:45](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:rag | rank-bm25>=0.2.2 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:46](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:rag | lingua-language-detector>=2.0.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:47](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:rag | gliner>=0.2.10 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:48](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:train | torch>=2.7.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:51](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:train | transformers>=4.51.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:52](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:train | peft>=0.15.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:53](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:train | trl>=0.19.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:54](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:train | accelerate>=1.0.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:55](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:train | bitsandbytes>=0.50.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:56](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:train | datasets>=3.0.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:57](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:train | mlflow-skinny>=2.14.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:58](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:pdf-plus | pymupdf>=1.24.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:62](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:viz | matplotlib>=3.8.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:65](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:unsloth | unsloth | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:67](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:dev | pytest>=8.2.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:71](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:dev | pytest-asyncio>=0.23.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:72](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:dev | ruff>=0.4.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:73](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:dev | mypy>=1.10.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:74](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:dev | mongomock>=4.1.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:75](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| extra:dev | respx>=0.21.0 | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:76](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |

## Skills diretamente relacionadas

| Skill | Aplicação | Fonte |
| --- | --- | --- |
| [ai-architecture-expert](../../../00_skills/(architecture)/ai-architecture-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:8](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| [ai-engineering-expert](../../../00_skills/(development)/ai-engineering-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:8](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| [ai-evals-expert](../../../00_skills/(quality)/ai-evals-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:8](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| [anti-hallucination-evaluator](../../../00_skills/(quality)/anti-hallucination-evaluator/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:8](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| [bm25-expert](../../../00_skills/(development)/bm25-expert/SKILL.md) | Necessidade observada: rag. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/DiabeticsresearchJEV/src/diabeticsresearchjev/application/rag/retriever.py:1](../../../02_repositorios/DiabeticsresearchJEV/src/diabeticsresearchjev/application/rag/retriever.py) |
| [ci-quality-gate-engineer](../../../00_skills/(development)/ci-quality-gate-engineer/SKILL.md) | Necessidade observada: ci. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/DiabeticsresearchJEV/.github/workflows/ci.yml:1](../../../02_repositorios/DiabeticsresearchJEV/.github/workflows/ci.yml); [02_repositorios/DiabeticsresearchJEV/.github/workflows/merge-main.yml:1](../../../02_repositorios/DiabeticsresearchJEV/.github/workflows/merge-main.yml) |
| [database-architecture-planner](../../../00_skills/(architecture)/database-architecture-planner/SKILL.md) | Necessidade observada: database. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/DiabeticsresearchJEV/docker-compose.yml:8](../../../02_repositorios/DiabeticsresearchJEV/docker-compose.yml) |
| [deployment-pipeline-expert](../../../00_skills/(cloud)/deployment-pipeline-expert/SKILL.md) | Necessidade observada: ci. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/DiabeticsresearchJEV/.github/workflows/ci.yml:1](../../../02_repositorios/DiabeticsresearchJEV/.github/workflows/ci.yml); [02_repositorios/DiabeticsresearchJEV/.github/workflows/merge-main.yml:1](../../../02_repositorios/DiabeticsresearchJEV/.github/workflows/merge-main.yml) |
| [devops-pipeline-engineering](../../../00_skills/(cloud)/devops-pipeline-engineering/SKILL.md) | Necessidade observada: ci. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/DiabeticsresearchJEV/.github/workflows/ci.yml:1](../../../02_repositorios/DiabeticsresearchJEV/.github/workflows/ci.yml); [02_repositorios/DiabeticsresearchJEV/.github/workflows/merge-main.yml:1](../../../02_repositorios/DiabeticsresearchJEV/.github/workflows/merge-main.yml) |
| [fine-tuning-expert](../../../00_skills/(development)/fine-tuning-expert/SKILL.md) | Necessidade observada: training. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:8](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| [llm-model-selection-expert](../../../00_skills/(development)/llm-model-selection-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:8](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| [lora-qlora-dora-expert](../../../00_skills/(development)/lora-qlora-dora-expert/SKILL.md) | Necessidade observada: training. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/DiabeticsresearchJEV/pyproject.toml:8](../../../02_repositorios/DiabeticsresearchJEV/pyproject.toml) |
| [python-bug-solver-skill](../../../00_skills/(development)/python-bug-solver-skill/SKILL.md) | Necessidade observada: python. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/DiabeticsresearchJEV/src/diabeticsresearchjev/application/pipeline/full_cycle.py:31](../../../02_repositorios/DiabeticsresearchJEV/src/diabeticsresearchjev/application/pipeline/full_cycle.py) |
| [python-expert](../../../00_skills/(development)/python-expert/SKILL.md) | Necessidade observada: python. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/DiabeticsresearchJEV/src/diabeticsresearchjev/application/pipeline/full_cycle.py:31](../../../02_repositorios/DiabeticsresearchJEV/src/diabeticsresearchjev/application/pipeline/full_cycle.py) |
| [python-rag-audit](../../../00_skills/(development)/python-rag-audit/SKILL.md) | Necessidade observada: rag. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/DiabeticsresearchJEV/src/diabeticsresearchjev/application/rag/retriever.py:1](../../../02_repositorios/DiabeticsresearchJEV/src/diabeticsresearchjev/application/rag/retriever.py) |
| [rag-expert](../../../00_skills/(development)/rag-expert/SKILL.md) | Necessidade observada: rag. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/DiabeticsresearchJEV/src/diabeticsresearchjev/application/rag/retriever.py:1](../../../02_repositorios/DiabeticsresearchJEV/src/diabeticsresearchjev/application/rag/retriever.py) |
| [gh-fix-ci](../../../00_skills/(tooling)/gh-fix-ci/SKILL.md) | Necessidade observada: ci. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/DiabeticsresearchJEV/.github/workflows/ci.yml:1](../../../02_repositorios/DiabeticsresearchJEV/.github/workflows/ci.yml); [02_repositorios/DiabeticsresearchJEV/.github/workflows/merge-main.yml:1](../../../02_repositorios/DiabeticsresearchJEV/.github/workflows/merge-main.yml) |

## Uso condicionado

- **ai-continuous-training-maintainer**: Contrato fixa E:/GitHub/aidiabetic-research/src/, diferente deste alvo. Confirmar escopo e pipeline antes de reutilizar.
- **atualizar-dependencias**: Somente em missão de atualização com baseline e compatibilidade.
- **compatibility-analyzer**: Ao verificar troca de linguagem/runtime/dependência.
- **dependency-updater**: Somente em atualização autorizada, preservando lockfiles.
- **github-operations**: Ao operar GitHub com alvo, credenciais e autorização próprios.
- **local-secret-vault**: Só se a tarefa depender de credenciais autorizadas; não abrir para mapear.
- **observability-root-cause-integrator**: Requer incidente/sintomas e telemetria atual.
- **pr-reviewer**: Requer PR/diff concreto.
- **pr-reviewer-advanced**: Requer PR/diff concreto e evidências de revisão.
- **release-readiness-judge**: Requer release concreta e checks determinísticos.
- **gh-address-comments**: Requer comentários de PR e alvo concreto.
- **cve-advisory-sync**: Só ao solicitar consulta atual de advisories oficiais.
- **cve-remediation**: Requer CVE/GHSA concreto, versão afetada e correção autorizada.
- **eol-advisory-sync**: Requer consulta atual de suporte oficial para os produtos declarados.
- **revisar-seguranca-pr**: Requer diff de PR e escopo de segurança.
- **vuln-obsol-recon**: Inventário estático é ponto de partida; auditoria de CVE/EOL não foi executada.
- **runtime-troubleshooting**: Requer runtime/logs atuais; o mapa é estático.

## Testes/CI

11 arquivos candidatos por nome/caminho; não corresponde a quantidade de testes executados. 2 workflows encontrados. Suites não executadas.

- [02_repositorios/DiabeticsresearchJEV/.github/workflows/ci.yml:1](../../../02_repositorios/DiabeticsresearchJEV/.github/workflows/ci.yml)
- [02_repositorios/DiabeticsresearchJEV/.github/workflows/merge-main.yml:1](../../../02_repositorios/DiabeticsresearchJEV/.github/workflows/merge-main.yml)

## Lacunas

- JEV aqui significa Judge/Evaluation/Verification; isso não comprova TypeSafe function calling.
- Perfil smoke não comprova treino QLoRA real.
- Alvo fixo de ai-continuous-training-maintainer não coincide com este diretório.
