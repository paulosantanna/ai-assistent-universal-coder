# dark-videos — mapa estático de skills

Updated: 2026-10-13

Entry point: ../README.md

Tipo: Git próprio. Arquivos no inventário delimitado: 581; entradas excluídas: 66.

[Voltar ao índice](../README.md) · [Matriz completa](../matriz.csv)

## Dez dimensões

| Dimensão | Estado | Observação | Evidência |
| --- | --- | --- | --- |
| Tecnologias e versões | declarado | Declarações extraídas dos manifests, incluindo faixas e extras. Não são versões instaladas nem prova de compatibilidade. Lockfiles permanecem nas fontes para análise posterior. | [02_repositorios/dark-videos/backend/pyproject.toml:10](../../../02_repositorios/dark-videos/backend/pyproject.toml); [02_repositorios/dark-videos/backend/pyproject.toml:11](../../../02_repositorios/dark-videos/backend/pyproject.toml); [02_repositorios/dark-videos/backend/pyproject.toml:12](../../../02_repositorios/dark-videos/backend/pyproject.toml); demais fontes em mapa.json/declarações abaixo |
| Arquitetura | documentado | Backend Python/FastAPI, workers Celery e frontend Next.js/React; inicialização desktop própria. | [02_repositorios/dark-videos/README.md:16](../../../02_repositorios/dark-videos/README.md) |
| Propósito | declarado | Aplicação de vídeos curtos com mineração, composição, agenda e publicação social. | [02_repositorios/dark-videos/README.md:1](../../../02_repositorios/dark-videos/README.md) |
| Fluxo | observado | Tarefa publishing.dispatch_due chama run_dispatch para processamento das publicações vencidas. | [02_repositorios/dark-videos/backend/app/modules/publishing/tasks.py:17](../../../02_repositorios/dark-videos/backend/app/modules/publishing/tasks.py) |
| Dados | observado | Base SQLAlchemy usa UUIDs/JSONB; modelos próprios dos módulos mining, creative, learning e publishing. | [02_repositorios/dark-videos/backend/app/db/base.py:11](../../../02_repositorios/dark-videos/backend/app/db/base.py) |
| Configuração/deploy | documentado | Execução desktop Windows documenta PostgreSQL portátil e Redis; ambiente atual não sondado. | [02_repositorios/dark-videos/README.md:57](../../../02_repositorios/dark-videos/README.md) |
| Operação/observabilidade | observado | FastAPI registra roteador de observabilidade; saúde/telemetria não exercitadas neste mapa. | [02_repositorios/dark-videos/backend/app/main.py:58](../../../02_repositorios/dark-videos/backend/app/main.py) |
| Interfaces/dependências | observado | Cliente LAYA declara endpoint externo de decisões; vínculo com a pasta laya não comprovado. | [02_repositorios/dark-videos/backend/app/modules/learning/laya_jev_client.py:41](../../../02_repositorios/dark-videos/backend/app/modules/learning/laya_jev_client.py) |
| Vulnerabilidades | não verificado | Nenhuma consulta atual a advisories/scanner foi executada; não equivale a ausência de CVEs. | Sem verificação nesta missão |
| Obsolescência | não verificado | Datas de suporte/EOL não consultadas. Versões declaradas não comprovam suporte atual. | Sem verificação nesta missão |

## Declarações dos manifests

Faixas e extras são preservados; versões instaladas/resolvidas não foram verificadas.

| Declaração | Valor | Fonte |
| --- | --- | --- |
| name | dark-videos-backend | [02_repositorios/dark-videos/backend/pyproject.toml:2](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| version | 0.1.0 | [02_repositorios/dark-videos/backend/pyproject.toml:3](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| requires-python | >=3.12 | [02_repositorios/dark-videos/backend/pyproject.toml:5](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | alembic>=1.20.0 | [02_repositorios/dark-videos/backend/pyproject.toml:7](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | argon2-cffi>=25.1.0 | [02_repositorios/dark-videos/backend/pyproject.toml:8](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | celery[redis]>=5.6.3 | [02_repositorios/dark-videos/backend/pyproject.toml:9](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | cryptography>=50.0.2 | [02_repositorios/dark-videos/backend/pyproject.toml:10](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | email-validator>=2.3.0 | [02_repositorios/dark-videos/backend/pyproject.toml:11](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | fastapi>=0.142.2 | [02_repositorios/dark-videos/backend/pyproject.toml:12](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | httpx>=0.28.1 | [02_repositorios/dark-videos/backend/pyproject.toml:13](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | langdetect==1.0.9 | [02_repositorios/dark-videos/backend/pyproject.toml:14](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | pgvector>=0.5.0 | [02_repositorios/dark-videos/backend/pyproject.toml:15](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | playwright>=1.55 | [02_repositorios/dark-videos/backend/pyproject.toml:16](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | pillow>=11 | [02_repositorios/dark-videos/backend/pyproject.toml:17](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | psycopg[binary]>=3.3.6 | [02_repositorios/dark-videos/backend/pyproject.toml:18](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | pydantic>=2.13.5 | [02_repositorios/dark-videos/backend/pyproject.toml:19](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | pydantic-settings>=2.15.0 | [02_repositorios/dark-videos/backend/pyproject.toml:20](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | redis>=6.4.0 | [02_repositorios/dark-videos/backend/pyproject.toml:21](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | sqlalchemy>=2.1.3 | [02_repositorios/dark-videos/backend/pyproject.toml:22](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | uvicorn[standard]>=0.54.0 | [02_repositorios/dark-videos/backend/pyproject.toml:23](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | yt-dlp>=2025.10.14 | [02_repositorios/dark-videos/backend/pyproject.toml:24](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | opentelemetry-api>=1.45.1 | [02_repositorios/dark-videos/backend/pyproject.toml:25](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | opentelemetry-sdk>=1.45.1 | [02_repositorios/dark-videos/backend/pyproject.toml:26](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | opentelemetry-exporter-otlp-proto-http>=1.45.1 | [02_repositorios/dark-videos/backend/pyproject.toml:27](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| dependency | opentelemetry-instrumentation-fastapi>=0.66b1 | [02_repositorios/dark-videos/backend/pyproject.toml:28](../../../02_repositorios/dark-videos/backend/pyproject.toml) |
| name | dark-videos-frontend | [02_repositorios/dark-videos/frontend/package.json:2](../../../02_repositorios/dark-videos/frontend/package.json) |
| version | 0.1.0 | [02_repositorios/dark-videos/frontend/package.json:3](../../../02_repositorios/dark-videos/frontend/package.json) |
| node | >=22 | [02_repositorios/dark-videos/frontend/package.json:37](../../../02_repositorios/dark-videos/frontend/package.json) |
| next | 16.4.0 | [02_repositorios/dark-videos/frontend/package.json:15](../../../02_repositorios/dark-videos/frontend/package.json) |
| react | 19.3.0 | [02_repositorios/dark-videos/frontend/package.json:16](../../../02_repositorios/dark-videos/frontend/package.json) |
| react-dom | 19.3.0 | [02_repositorios/dark-videos/frontend/package.json:16](../../../02_repositorios/dark-videos/frontend/package.json) |
| @tailwindcss/turbopack | ^4 | [02_repositorios/dark-videos/frontend/package.json:20](../../../02_repositorios/dark-videos/frontend/package.json) |
| @testing-library/dom | ^10.4.2 | [02_repositorios/dark-videos/frontend/package.json:21](../../../02_repositorios/dark-videos/frontend/package.json) |
| @testing-library/jest-dom | ^7.0.1 | [02_repositorios/dark-videos/frontend/package.json:22](../../../02_repositorios/dark-videos/frontend/package.json) |
| @testing-library/react | ^16.3.3 | [02_repositorios/dark-videos/frontend/package.json:23](../../../02_repositorios/dark-videos/frontend/package.json) |
| @testing-library/user-event | ^14.6.7 | [02_repositorios/dark-videos/frontend/package.json:24](../../../02_repositorios/dark-videos/frontend/package.json) |
| @types/node | ^22.20.5 | [02_repositorios/dark-videos/frontend/package.json:25](../../../02_repositorios/dark-videos/frontend/package.json) |
| @types/react | ^19 | [02_repositorios/dark-videos/frontend/package.json:26](../../../02_repositorios/dark-videos/frontend/package.json) |
| @types/react-dom | ^19 | [02_repositorios/dark-videos/frontend/package.json:26](../../../02_repositorios/dark-videos/frontend/package.json) |
| @vitejs/plugin-react | ^6.1.2 | [02_repositorios/dark-videos/frontend/package.json:28](../../../02_repositorios/dark-videos/frontend/package.json) |
| eslint | ^9 | [02_repositorios/dark-videos/frontend/package.json:29](../../../02_repositorios/dark-videos/frontend/package.json) |
| eslint-config-next | 16.4.0 | [02_repositorios/dark-videos/frontend/package.json:15](../../../02_repositorios/dark-videos/frontend/package.json) |
| jsdom | ^29.1.1 | [02_repositorios/dark-videos/frontend/package.json:31](../../../02_repositorios/dark-videos/frontend/package.json) |
| tailwindcss | ^4 | [02_repositorios/dark-videos/frontend/package.json:20](../../../02_repositorios/dark-videos/frontend/package.json) |
| typescript | ^5 | [02_repositorios/dark-videos/frontend/package.json:33](../../../02_repositorios/dark-videos/frontend/package.json) |
| vitest | ^5.0.3 | [02_repositorios/dark-videos/frontend/package.json:34](../../../02_repositorios/dark-videos/frontend/package.json) |

## Skills diretamente relacionadas

| Skill | Aplicação | Fonte |
| --- | --- | --- |
| [ai-architecture-expert](../../../00_skills/(architecture)/ai-architecture-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos/README.md:1](../../../02_repositorios/dark-videos/README.md) |
| [ai-engineering-expert](../../../00_skills/(development)/ai-engineering-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos/README.md:1](../../../02_repositorios/dark-videos/README.md) |
| [ai-evals-expert](../../../00_skills/(quality)/ai-evals-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos/README.md:1](../../../02_repositorios/dark-videos/README.md) |
| [anti-hallucination-evaluator](../../../00_skills/(quality)/anti-hallucination-evaluator/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos/README.md:1](../../../02_repositorios/dark-videos/README.md) |
| [ci-quality-gate-engineer](../../../00_skills/(development)/ci-quality-gate-engineer/SKILL.md) | Necessidade observada: ci. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos/.github/workflows/ci.yml:1](../../../02_repositorios/dark-videos/.github/workflows/ci.yml); [02_repositorios/dark-videos/.github/workflows/portable-exe.yml:1](../../../02_repositorios/dark-videos/.github/workflows/portable-exe.yml) |
| [core-web-vitals](../../../00_skills/(performance)/core-web-vitals/SKILL.md) | Necessidade observada: react. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos/README.md:16](../../../02_repositorios/dark-videos/README.md) |
| [dark-videos-pipeline-expert](../../../00_skills/(development)/dark-videos-pipeline-expert/SKILL.md) | Especialização adequada ao contrato/estrutura observados; ativar apenas na tarefa correspondente. | [02_repositorios/dark-videos/backend/app/modules/learning/laya_jev_client.py:41](../../../02_repositorios/dark-videos/backend/app/modules/learning/laya_jev_client.py); [02_repositorios/dark-videos/backend/app/modules/publishing/tasks.py:17](../../../02_repositorios/dark-videos/backend/app/modules/publishing/tasks.py) |
| [database-architecture-planner](../../../00_skills/(architecture)/database-architecture-planner/SKILL.md) | Necessidade observada: database. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos/backend/app/db/base.py:11](../../../02_repositorios/dark-videos/backend/app/db/base.py) |
| [deployment-pipeline-expert](../../../00_skills/(cloud)/deployment-pipeline-expert/SKILL.md) | Necessidade observada: ci. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos/.github/workflows/ci.yml:1](../../../02_repositorios/dark-videos/.github/workflows/ci.yml); [02_repositorios/dark-videos/.github/workflows/portable-exe.yml:1](../../../02_repositorios/dark-videos/.github/workflows/portable-exe.yml) |
| [devops-pipeline-engineering](../../../00_skills/(cloud)/devops-pipeline-engineering/SKILL.md) | Necessidade observada: ci. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos/.github/workflows/ci.yml:1](../../../02_repositorios/dark-videos/.github/workflows/ci.yml); [02_repositorios/dark-videos/.github/workflows/portable-exe.yml:1](../../../02_repositorios/dark-videos/.github/workflows/portable-exe.yml) |
| [fine-tuning-expert](../../../00_skills/(development)/fine-tuning-expert/SKILL.md) | Necessidade observada: training. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos/README.md:1](../../../02_repositorios/dark-videos/README.md) |
| [llm-model-selection-expert](../../../00_skills/(development)/llm-model-selection-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos/README.md:1](../../../02_repositorios/dark-videos/README.md) |
| [lora-qlora-dora-expert](../../../00_skills/(development)/lora-qlora-dora-expert/SKILL.md) | Necessidade observada: training. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos/README.md:1](../../../02_repositorios/dark-videos/README.md) |
| [python-bug-solver-skill](../../../00_skills/(development)/python-bug-solver-skill/SKILL.md) | Necessidade observada: python. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos/backend/app/modules/publishing/tasks.py:17](../../../02_repositorios/dark-videos/backend/app/modules/publishing/tasks.py) |
| [python-expert](../../../00_skills/(development)/python-expert/SKILL.md) | Necessidade observada: python. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos/backend/app/modules/publishing/tasks.py:17](../../../02_repositorios/dark-videos/backend/app/modules/publishing/tasks.py) |
| [react-expert](../../../00_skills/(development)/react-expert/SKILL.md) | Necessidade observada: react. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos/README.md:16](../../../02_repositorios/dark-videos/README.md) |
| [social-media-operator](../../../00_skills/(tooling)/social-media-operator/SKILL.md) | Necessidade observada: social. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos/README.md:1](../../../02_repositorios/dark-videos/README.md) |
| [web-quality-audit](../../../00_skills/(quality)/web-quality-audit/SKILL.md) | Necessidade observada: react. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos/README.md:16](../../../02_repositorios/dark-videos/README.md) |
| [typesafe-ai](../../../00_skills/(development)/typesafe-ai/SKILL.md) | Especialização adequada ao contrato/estrutura observados; ativar apenas na tarefa correspondente. | [02_repositorios/dark-videos/backend/app/modules/learning/jev/client.py:28](../../../02_repositorios/dark-videos/backend/app/modules/learning/jev/client.py) |
| [web-accessibility](../../../00_skills/(quality)/web-accessibility/SKILL.md) | Necessidade observada: react. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos/README.md:16](../../../02_repositorios/dark-videos/README.md) |
| [chrome-devtools](../../../00_skills/(tooling)/chrome-devtools/SKILL.md) | Necessidade observada: browser. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos/README.md:16](../../../02_repositorios/dark-videos/README.md) |
| [gh-fix-ci](../../../00_skills/(tooling)/gh-fix-ci/SKILL.md) | Necessidade observada: ci. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos/.github/workflows/ci.yml:1](../../../02_repositorios/dark-videos/.github/workflows/ci.yml); [02_repositorios/dark-videos/.github/workflows/portable-exe.yml:1](../../../02_repositorios/dark-videos/.github/workflows/portable-exe.yml) |
| [playwright-skill](../../../00_skills/(web-automation)/playwright-skill/SKILL.md) | Necessidade observada: browser. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos/README.md:16](../../../02_repositorios/dark-videos/README.md) |
| [react-best-practices](../../../00_skills/(quality)/react-best-practices/SKILL.md) | Necessidade observada: react. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos/README.md:16](../../../02_repositorios/dark-videos/README.md) |
| [react-composition-patterns](../../../00_skills/(architecture)/react-composition-patterns/SKILL.md) | Necessidade observada: react. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos/README.md:16](../../../02_repositorios/dark-videos/README.md) |

## Uso condicionado

- **ai-continuous-training-maintainer**: Contrato fixa E:/GitHub/aidiabetic-research/src/, diferente deste alvo. Confirmar escopo e pipeline antes de reutilizar.
- **atualizar-dependencias**: Somente em missão de atualização com baseline e compatibilidade.
- **compatibility-analyzer**: Ao verificar troca de linguagem/runtime/dependência.
- **dependency-updater**: Somente em atualização autorizada, preservando lockfiles.
- **github-operations**: Ao operar GitHub com alvo, credenciais e autorização próprios.
- **jev-call-expert**: Cliente TypeSafe/Jev existe; confirmar despacho para funções permitidas antes de aplicar o contrato de function calling.
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

207 arquivos candidatos por nome/caminho; não corresponde a quantidade de testes executados. 2 workflows encontrados. Suites não executadas.

- [02_repositorios/dark-videos/.github/workflows/ci.yml:1](../../../02_repositorios/dark-videos/.github/workflows/ci.yml)
- [02_repositorios/dark-videos/.github/workflows/portable-exe.yml:1](../../../02_repositorios/dark-videos/.github/workflows/portable-exe.yml)

## Lacunas

- README contém status histórico; prevalecem código/manifests e continuidade local.
- Autenticação/contas e publicação real não verificadas.
- Nome LAYA não identifica o projeto local laya.
