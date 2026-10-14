# AIHealthResearch — mapa estático de skills

Updated: 2026-10-13

Entry point: ../README.md

Tipo: Git próprio. Arquivos no inventário delimitado: 107; entradas excluídas: 2.

[Voltar ao índice](../README.md) · [Matriz completa](../matriz.csv)

## Dez dimensões

| Dimensão | Estado | Observação | Evidência |
| --- | --- | --- | --- |
| Tecnologias e versões | declarado | Declarações extraídas dos manifests, incluindo faixas e extras. Não são versões instaladas nem prova de compatibilidade. Lockfiles permanecem nas fontes para análise posterior. | [02_repositorios/AIHealthResearch/pyproject.toml:10](../../../02_repositorios/AIHealthResearch/pyproject.toml); [02_repositorios/AIHealthResearch/pyproject.toml:11](../../../02_repositorios/AIHealthResearch/pyproject.toml); [02_repositorios/AIHealthResearch/pyproject.toml:12](../../../02_repositorios/AIHealthResearch/pyproject.toml); demais fontes em mapa.json/declarações abaixo |
| Arquitetura | documentado | Camadas domain/application/infrastructure/interfaces; documentação separa AWS alvo de laboratório local. | [02_repositorios/AIHealthResearch/docs/ARCHITECTURE.md:29](../../../02_repositorios/AIHealthResearch/docs/ARCHITECTURE.md) |
| Propósito | declarado | Plataforma de pesquisa em diabetes com RAG baseado em evidências, revisão determinística e treino candidato para AWS. | [02_repositorios/AIHealthResearch/README.md:3](../../../02_repositorios/AIHealthResearch/README.md) |
| Fluxo | observado | Research recebe pergunta, recupera evidências e revalida versões/uso antes da resposta; rejeições fazem parte do contrato. | [02_repositorios/AIHealthResearch/src/aihealthresearch/application/research.py:106](../../../02_repositorios/AIHealthResearch/src/aihealthresearch/application/research.py) |
| Dados | observado | SQLAlchemy mantém knowledge_versions; dados de conhecimento são versionados e auditados. | [02_repositorios/AIHealthResearch/src/aihealthresearch/infrastructure/database.py:25](../../../02_repositorios/AIHealthResearch/src/aihealthresearch/infrastructure/database.py) |
| Configuração/deploy | observado | Gerador CloudFormation declara VPC e serviços AWS; presença do gerador não comprova implantação. | [02_repositorios/AIHealthResearch/infra/render_stack.py:37](../../../02_repositorios/AIHealthResearch/infra/render_stack.py) |
| Operação/observabilidade | observado | Treino possui callback de telemetria; disponibilidade e métricas reais não verificadas. | [02_repositorios/AIHealthResearch/src/aihealthresearch/infrastructure/trainer.py:73](../../../02_repositorios/AIHealthResearch/src/aihealthresearch/infrastructure/trainer.py) |
| Interfaces/dependências | observado | FastAPI e CLI air; despacho de chamadas usa Choice/Noul, funções permitidas e limiares de confiança. | [02_repositorios/AIHealthResearch/src/aihealthresearch/application/dispatch.py:30](../../../02_repositorios/AIHealthResearch/src/aihealthresearch/application/dispatch.py) |
| Vulnerabilidades | não verificado | Nenhuma consulta atual a advisories/scanner foi executada; não equivale a ausência de CVEs. | Sem verificação nesta missão |
| Obsolescência | não verificado | Datas de suporte/EOL não consultadas. Versões declaradas não comprovam suporte atual. | Sem verificação nesta missão |

## Declarações dos manifests

Faixas e extras são preservados; versões instaladas/resolvidas não foram verificadas.

| Declaração | Valor | Fonte |
| --- | --- | --- |
| name | aihealthresearch | [02_repositorios/AIHealthResearch/pyproject.toml:5](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| version | 0.2.0 | [02_repositorios/AIHealthResearch/pyproject.toml:6](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| requires-python | >=3.12,<3.13 | [02_repositorios/AIHealthResearch/pyproject.toml:7](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| dependency | fastapi==0.141.1 | [02_repositorios/AIHealthResearch/pyproject.toml:8](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| dependency | uvicorn==0.52.4 | [02_repositorios/AIHealthResearch/pyproject.toml:8](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| dependency | SQLAlchemy==2.0.52 | [02_repositorios/AIHealthResearch/pyproject.toml:8](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| dependency | psycopg[binary]==3.3.5 | [02_repositorios/AIHealthResearch/pyproject.toml:8](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| dependency | httpx==0.28.1 | [02_repositorios/AIHealthResearch/pyproject.toml:8](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| dependency | PyJWT[crypto]==2.14.0 | [02_repositorios/AIHealthResearch/pyproject.toml:8](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| dependency | boto3==1.43.93 | [02_repositorios/AIHealthResearch/pyproject.toml:8](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| dependency | opensearch-py==3.2.0 | [02_repositorios/AIHealthResearch/pyproject.toml:8](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| dependency | defusedxml==0.7.1 | [02_repositorios/AIHealthResearch/pyproject.toml:8](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| extra:dev | pytest==9.1.1 | [02_repositorios/AIHealthResearch/pyproject.toml:10](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| extra:dev | ruff==0.16.7 | [02_repositorios/AIHealthResearch/pyproject.toml:10](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| extra:dev | bandit==1.9.4 | [02_repositorios/AIHealthResearch/pyproject.toml:10](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| extra:dev | pip-audit==2.10.1 | [02_repositorios/AIHealthResearch/pyproject.toml:10](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| extra:dev | cfn-lint==1.56.3 | [02_repositorios/AIHealthResearch/pyproject.toml:10](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| extra:ml | torch==2.14.0 | [02_repositorios/AIHealthResearch/pyproject.toml:11](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| extra:ml | transformers==5.17.0 | [02_repositorios/AIHealthResearch/pyproject.toml:11](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| extra:ml | peft==0.20.0 | [02_repositorios/AIHealthResearch/pyproject.toml:11](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| extra:ml | accelerate==1.15.0 | [02_repositorios/AIHealthResearch/pyproject.toml:11](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| extra:vector | sentence-transformers>=5.1,<6 | [02_repositorios/AIHealthResearch/pyproject.toml:12](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| extra:vector | chromadb>=1,<2 | [02_repositorios/AIHealthResearch/pyproject.toml:12](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| declaration | fastapi>=0.116.0 | [02_repositorios/AIHealthResearch/requirements.txt:1](../../../02_repositorios/AIHealthResearch/requirements.txt) |
| declaration | strawberry-graphql>=0.275.0 | [02_repositorios/AIHealthResearch/requirements.txt:2](../../../02_repositorios/AIHealthResearch/requirements.txt) |
| declaration | uvicorn>=0.35.0 | [02_repositorios/AIHealthResearch/requirements.txt:3](../../../02_repositorios/AIHealthResearch/requirements.txt) |
| declaration | pydantic>=2.11.0 | [02_repositorios/AIHealthResearch/requirements.txt:4](../../../02_repositorios/AIHealthResearch/requirements.txt) |
| declaration | boto3>=1.40.0 | [02_repositorios/AIHealthResearch/requirements.txt:5](../../../02_repositorios/AIHealthResearch/requirements.txt) |
| declaration | chromadb>=1.0.0 | [02_repositorios/AIHealthResearch/requirements.txt:6](../../../02_repositorios/AIHealthResearch/requirements.txt) |
| declaration | rank-bm25>=0.2.2 | [02_repositorios/AIHealthResearch/requirements.txt:7](../../../02_repositorios/AIHealthResearch/requirements.txt) |
| declaration | numpy>=2.0.0 | [02_repositorios/AIHealthResearch/requirements.txt:8](../../../02_repositorios/AIHealthResearch/requirements.txt) |
| declaration | python-dotenv>=1.1.0 | [02_repositorios/AIHealthResearch/requirements.txt:9](../../../02_repositorios/AIHealthResearch/requirements.txt) |

## Skills diretamente relacionadas

| Skill | Aplicação | Fonte |
| --- | --- | --- |
| [ai-architecture-expert](../../../00_skills/(architecture)/ai-architecture-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/AIHealthResearch/README.md:3](../../../02_repositorios/AIHealthResearch/README.md) |
| [ai-engineering-expert](../../../00_skills/(development)/ai-engineering-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/AIHealthResearch/README.md:3](../../../02_repositorios/AIHealthResearch/README.md) |
| [ai-evals-expert](../../../00_skills/(quality)/ai-evals-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/AIHealthResearch/README.md:3](../../../02_repositorios/AIHealthResearch/README.md) |
| [anti-hallucination-evaluator](../../../00_skills/(quality)/anti-hallucination-evaluator/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/AIHealthResearch/README.md:3](../../../02_repositorios/AIHealthResearch/README.md) |
| [bm25-expert](../../../00_skills/(development)/bm25-expert/SKILL.md) | Necessidade observada: rag. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/AIHealthResearch/src/aihealthresearch/application/dispatch.py:30](../../../02_repositorios/AIHealthResearch/src/aihealthresearch/application/dispatch.py) |
| [ci-quality-gate-engineer](../../../00_skills/(development)/ci-quality-gate-engineer/SKILL.md) | Necessidade observada: ci. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/AIHealthResearch/.github/workflows/ci.yml:1](../../../02_repositorios/AIHealthResearch/.github/workflows/ci.yml); [02_repositorios/AIHealthResearch/.github/workflows/scientific-extraction-governance.yml:1](../../../02_repositorios/AIHealthResearch/.github/workflows/scientific-extraction-governance.yml) |
| [database-architecture-planner](../../../00_skills/(architecture)/database-architecture-planner/SKILL.md) | Necessidade observada: database. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/AIHealthResearch/src/aihealthresearch/infrastructure/database.py:25](../../../02_repositorios/AIHealthResearch/src/aihealthresearch/infrastructure/database.py) |
| [deployment-pipeline-expert](../../../00_skills/(cloud)/deployment-pipeline-expert/SKILL.md) | Necessidade observada: ci. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/AIHealthResearch/.github/workflows/ci.yml:1](../../../02_repositorios/AIHealthResearch/.github/workflows/ci.yml); [02_repositorios/AIHealthResearch/.github/workflows/scientific-extraction-governance.yml:1](../../../02_repositorios/AIHealthResearch/.github/workflows/scientific-extraction-governance.yml) |
| [devops-pipeline-engineering](../../../00_skills/(cloud)/devops-pipeline-engineering/SKILL.md) | Necessidade observada: ci. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/AIHealthResearch/.github/workflows/ci.yml:1](../../../02_repositorios/AIHealthResearch/.github/workflows/ci.yml); [02_repositorios/AIHealthResearch/.github/workflows/scientific-extraction-governance.yml:1](../../../02_repositorios/AIHealthResearch/.github/workflows/scientific-extraction-governance.yml) |
| [fine-tuning-expert](../../../00_skills/(development)/fine-tuning-expert/SKILL.md) | Necessidade observada: training. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/AIHealthResearch/README.md:3](../../../02_repositorios/AIHealthResearch/README.md) |
| [jev-call-expert](../../../00_skills/(development)/jev-call-expert/SKILL.md) | Necessidade observada: typed-dispatch. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/AIHealthResearch/src/aihealthresearch/application/dispatch.py:30](../../../02_repositorios/AIHealthResearch/src/aihealthresearch/application/dispatch.py) |
| [llm-calibration-temperature-expert](../../../00_skills/(development)/llm-calibration-temperature-expert/SKILL.md) | Necessidade observada: typed-dispatch. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/AIHealthResearch/src/aihealthresearch/application/dispatch.py:30](../../../02_repositorios/AIHealthResearch/src/aihealthresearch/application/dispatch.py) |
| [llm-model-selection-expert](../../../00_skills/(development)/llm-model-selection-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/AIHealthResearch/README.md:3](../../../02_repositorios/AIHealthResearch/README.md) |
| [lora-qlora-dora-expert](../../../00_skills/(development)/lora-qlora-dora-expert/SKILL.md) | Necessidade observada: training. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/AIHealthResearch/README.md:3](../../../02_repositorios/AIHealthResearch/README.md) |
| [production-deployment-planner](../../../00_skills/(cloud)/production-deployment-planner/SKILL.md) | Necessidade observada: aws. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/AIHealthResearch/infra/render_stack.py:37](../../../02_repositorios/AIHealthResearch/infra/render_stack.py) |
| [python-bug-solver-skill](../../../00_skills/(development)/python-bug-solver-skill/SKILL.md) | Necessidade observada: python. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/AIHealthResearch/src/aihealthresearch/application/research.py:106](../../../02_repositorios/AIHealthResearch/src/aihealthresearch/application/research.py) |
| [python-expert](../../../00_skills/(development)/python-expert/SKILL.md) | Necessidade observada: python. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/AIHealthResearch/src/aihealthresearch/application/research.py:106](../../../02_repositorios/AIHealthResearch/src/aihealthresearch/application/research.py) |
| [python-rag-audit](../../../00_skills/(development)/python-rag-audit/SKILL.md) | Necessidade observada: rag. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/AIHealthResearch/src/aihealthresearch/application/dispatch.py:30](../../../02_repositorios/AIHealthResearch/src/aihealthresearch/application/dispatch.py) |
| [rag-expert](../../../00_skills/(development)/rag-expert/SKILL.md) | Necessidade observada: rag. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/AIHealthResearch/src/aihealthresearch/application/dispatch.py:30](../../../02_repositorios/AIHealthResearch/src/aihealthresearch/application/dispatch.py) |
| [typesafe-ai](../../../00_skills/(development)/typesafe-ai/SKILL.md) | Necessidade observada: typed-dispatch. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/AIHealthResearch/src/aihealthresearch/application/dispatch.py:30](../../../02_repositorios/AIHealthResearch/src/aihealthresearch/application/dispatch.py) |
| [aws-advisor](../../../00_skills/(cloud)/aws-advisor/SKILL.md) | Necessidade observada: aws. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/AIHealthResearch/infra/render_stack.py:37](../../../02_repositorios/AIHealthResearch/infra/render_stack.py) |
| [gh-fix-ci](../../../00_skills/(tooling)/gh-fix-ci/SKILL.md) | Necessidade observada: ci. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/AIHealthResearch/.github/workflows/ci.yml:1](../../../02_repositorios/AIHealthResearch/.github/workflows/ci.yml); [02_repositorios/AIHealthResearch/.github/workflows/scientific-extraction-governance.yml:1](../../../02_repositorios/AIHealthResearch/.github/workflows/scientific-extraction-governance.yml) |

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

18 arquivos candidatos por nome/caminho; não corresponde a quantidade de testes executados. 2 workflows encontrados. Suites não executadas.

- [02_repositorios/AIHealthResearch/.github/workflows/ci.yml:1](../../../02_repositorios/AIHealthResearch/.github/workflows/ci.yml)
- [02_repositorios/AIHealthResearch/.github/workflows/scientific-extraction-governance.yml:1](../../../02_repositorios/AIHealthResearch/.github/workflows/scientific-extraction-governance.yml)

## Lacunas

- Aprovação científica e implantação não verificadas.
- Instruções existentes de treino contínuo citam outro caminho; confirmar alvo antes de reutilizar.
