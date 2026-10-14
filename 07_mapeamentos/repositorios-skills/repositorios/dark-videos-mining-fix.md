# dark-videos-mining-fix — mapa estático de skills

Updated: 2026-10-13

Entry point: ../README.md

Tipo: pacote sem Git próprio. Arquivos no inventário delimitado: 519; entradas excluídas: 55.

[Voltar ao índice](../README.md) · [Matriz completa](../matriz.csv)

## Dez dimensões

| Dimensão | Estado | Observação | Evidência |
| --- | --- | --- | --- |
| Tecnologias e versões | declarado | Declarações extraídas dos manifests, incluindo faixas e extras. Não são versões instaladas nem prova de compatibilidade. Lockfiles permanecem nas fontes para análise posterior. | [02_repositorios/dark-videos-mining-fix/backend/pyproject.toml:10](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml); [02_repositorios/dark-videos-mining-fix/backend/pyproject.toml:11](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml); [02_repositorios/dark-videos-mining-fix/backend/pyproject.toml:12](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml); demais fontes em mapa.json/declarações abaixo |
| Arquitetura | observado | Pacote com cópia backend, alterações frontend e ferramenta de aplicação; não tem Git próprio. | [02_repositorios/dark-videos-mining-fix/package.py:60](../../../02_repositorios/dark-videos-mining-fix/package.py) |
| Propósito | declarado | Pacote de correção de mineração pt-BR, deduplicação e inspeção do vídeo original para dark-videos. | [02_repositorios/dark-videos-mining-fix/README.md:1](../../../02_repositorios/dark-videos-mining-fix/README.md) |
| Fluxo | documentado | Política documentada admite título OU descrição pt-BR e exige inspeção do original antes da moldura. | [02_repositorios/dark-videos-mining-fix/README.md:9](../../../02_repositorios/dark-videos-mining-fix/README.md) |
| Dados | observado | Herda a base SQLAlchemy/JSONB do backend; não é outro serviço de dados independente. | [02_repositorios/dark-videos-mining-fix/backend/app/db/base.py:11](../../../02_repositorios/dark-videos-mining-fix/backend/app/db/base.py) |
| Configuração/deploy | documentado | README aponta aplicação externa em D:/Git/dark-videos; estado histórico não prova os arquivos do espelho atual. | [02_repositorios/dark-videos-mining-fix/README.md:3](../../../02_repositorios/dark-videos-mining-fix/README.md) |
| Operação/observabilidade | observado | Harness run_checks define verificações; os resultados existentes são históricos e não foram reexecutados. | [02_repositorios/dark-videos-mining-fix/run_checks.py:25](../../../02_repositorios/dark-videos-mining-fix/run_checks.py) |
| Interfaces/dependências | observado | Metadados são avaliados por política específica; adaptadores não garantem acesso funcional aos provedores. | [02_repositorios/dark-videos-mining-fix/backend/app/modules/mining/metadata_policy.py:53](../../../02_repositorios/dark-videos-mining-fix/backend/app/modules/mining/metadata_policy.py) |
| Vulnerabilidades | não verificado | Nenhuma consulta atual a advisories/scanner foi executada; não equivale a ausência de CVEs. | Sem verificação nesta missão |
| Obsolescência | não verificado | Datas de suporte/EOL não consultadas. Versões declaradas não comprovam suporte atual. | Sem verificação nesta missão |

## Declarações dos manifests

Faixas e extras são preservados; versões instaladas/resolvidas não foram verificadas.

| Declaração | Valor | Fonte |
| --- | --- | --- |
| name | dark-videos-backend | [02_repositorios/dark-videos-mining-fix/backend/pyproject.toml:2](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| version | 0.1.0 | [02_repositorios/dark-videos-mining-fix/backend/pyproject.toml:3](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| requires-python | >=3.12 | [02_repositorios/dark-videos-mining-fix/backend/pyproject.toml:5](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | alembic>=1.20.0 | [02_repositorios/dark-videos-mining-fix/backend/pyproject.toml:7](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | argon2-cffi>=25.1.0 | [02_repositorios/dark-videos-mining-fix/backend/pyproject.toml:8](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | celery[redis]>=5.6.3 | [02_repositorios/dark-videos-mining-fix/backend/pyproject.toml:9](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | cryptography>=50.0.2 | [02_repositorios/dark-videos-mining-fix/backend/pyproject.toml:10](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | email-validator>=2.3.0 | [02_repositorios/dark-videos-mining-fix/backend/pyproject.toml:11](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | fastapi>=0.142.2 | [02_repositorios/dark-videos-mining-fix/backend/pyproject.toml:12](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | httpx>=0.28.1 | [02_repositorios/dark-videos-mining-fix/backend/pyproject.toml:13](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | langdetect==1.0.9 | [02_repositorios/dark-videos-mining-fix/backend/pyproject.toml:14](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | pgvector>=0.5.0 | [02_repositorios/dark-videos-mining-fix/backend/pyproject.toml:15](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | playwright>=1.55 | [02_repositorios/dark-videos-mining-fix/backend/pyproject.toml:16](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | pillow>=11 | [02_repositorios/dark-videos-mining-fix/backend/pyproject.toml:17](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | psycopg[binary]>=3.3.6 | [02_repositorios/dark-videos-mining-fix/backend/pyproject.toml:18](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | pydantic>=2.13.5 | [02_repositorios/dark-videos-mining-fix/backend/pyproject.toml:19](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | pydantic-settings>=2.15.0 | [02_repositorios/dark-videos-mining-fix/backend/pyproject.toml:20](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | redis>=6.4.0 | [02_repositorios/dark-videos-mining-fix/backend/pyproject.toml:21](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | sqlalchemy>=2.1.3 | [02_repositorios/dark-videos-mining-fix/backend/pyproject.toml:22](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | uvicorn[standard]>=0.54.0 | [02_repositorios/dark-videos-mining-fix/backend/pyproject.toml:23](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | yt-dlp>=2025.10.14 | [02_repositorios/dark-videos-mining-fix/backend/pyproject.toml:24](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | opentelemetry-api>=1.45.1 | [02_repositorios/dark-videos-mining-fix/backend/pyproject.toml:25](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | opentelemetry-sdk>=1.45.1 | [02_repositorios/dark-videos-mining-fix/backend/pyproject.toml:26](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | opentelemetry-exporter-otlp-proto-http>=1.45.1 | [02_repositorios/dark-videos-mining-fix/backend/pyproject.toml:27](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | opentelemetry-instrumentation-fastapi>=0.66b1 | [02_repositorios/dark-videos-mining-fix/backend/pyproject.toml:28](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |

## Skills diretamente relacionadas

| Skill | Aplicação | Fonte |
| --- | --- | --- |
| [ai-architecture-expert](../../../00_skills/(architecture)/ai-architecture-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos-mining-fix/README.md:1](../../../02_repositorios/dark-videos-mining-fix/README.md) |
| [ai-engineering-expert](../../../00_skills/(development)/ai-engineering-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos-mining-fix/README.md:1](../../../02_repositorios/dark-videos-mining-fix/README.md) |
| [ai-evals-expert](../../../00_skills/(quality)/ai-evals-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos-mining-fix/README.md:1](../../../02_repositorios/dark-videos-mining-fix/README.md) |
| [anti-hallucination-evaluator](../../../00_skills/(quality)/anti-hallucination-evaluator/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos-mining-fix/README.md:1](../../../02_repositorios/dark-videos-mining-fix/README.md) |
| [change-trace-auditor](../../../00_skills/(quality)/change-trace-auditor/SKILL.md) | Especialização adequada ao contrato/estrutura observados; ativar apenas na tarefa correspondente. | [02_repositorios/dark-videos-mining-fix/backend/app/modules/mining/metadata_policy.py:53](../../../02_repositorios/dark-videos-mining-fix/backend/app/modules/mining/metadata_policy.py); [02_repositorios/dark-videos-mining-fix/README.md:9](../../../02_repositorios/dark-videos-mining-fix/README.md) |
| [dark-videos-pipeline-expert](../../../00_skills/(development)/dark-videos-pipeline-expert/SKILL.md) | Especialização adequada ao contrato/estrutura observados; ativar apenas na tarefa correspondente. | [02_repositorios/dark-videos-mining-fix/backend/app/modules/mining/metadata_policy.py:53](../../../02_repositorios/dark-videos-mining-fix/backend/app/modules/mining/metadata_policy.py); [02_repositorios/dark-videos-mining-fix/README.md:9](../../../02_repositorios/dark-videos-mining-fix/README.md) |
| [database-architecture-planner](../../../00_skills/(architecture)/database-architecture-planner/SKILL.md) | Necessidade observada: database. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos-mining-fix/backend/app/db/base.py:11](../../../02_repositorios/dark-videos-mining-fix/backend/app/db/base.py) |
| [diff-reviewer](../../../00_skills/(quality)/diff-reviewer/SKILL.md) | Especialização adequada ao contrato/estrutura observados; ativar apenas na tarefa correspondente. | [02_repositorios/dark-videos-mining-fix/backend/app/modules/mining/metadata_policy.py:53](../../../02_repositorios/dark-videos-mining-fix/backend/app/modules/mining/metadata_policy.py); [02_repositorios/dark-videos-mining-fix/README.md:9](../../../02_repositorios/dark-videos-mining-fix/README.md) |
| [llm-model-selection-expert](../../../00_skills/(development)/llm-model-selection-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos-mining-fix/README.md:1](../../../02_repositorios/dark-videos-mining-fix/README.md) |
| [python-bug-solver-skill](../../../00_skills/(development)/python-bug-solver-skill/SKILL.md) | Necessidade observada: python. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos-mining-fix/README.md:9](../../../02_repositorios/dark-videos-mining-fix/README.md) |
| [python-expert](../../../00_skills/(development)/python-expert/SKILL.md) | Necessidade observada: python. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos-mining-fix/README.md:9](../../../02_repositorios/dark-videos-mining-fix/README.md) |
| [react-expert](../../../00_skills/(development)/react-expert/SKILL.md) | Especialização adequada ao contrato/estrutura observados; ativar apenas na tarefa correspondente. | [02_repositorios/dark-videos-mining-fix/backend/app/modules/mining/metadata_policy.py:53](../../../02_repositorios/dark-videos-mining-fix/backend/app/modules/mining/metadata_policy.py); [02_repositorios/dark-videos-mining-fix/README.md:9](../../../02_repositorios/dark-videos-mining-fix/README.md) |
| [rollback-planner](../../../00_skills/(cloud)/rollback-planner/SKILL.md) | Especialização adequada ao contrato/estrutura observados; ativar apenas na tarefa correspondente. | [02_repositorios/dark-videos-mining-fix/backend/app/modules/mining/metadata_policy.py:53](../../../02_repositorios/dark-videos-mining-fix/backend/app/modules/mining/metadata_policy.py); [02_repositorios/dark-videos-mining-fix/README.md:9](../../../02_repositorios/dark-videos-mining-fix/README.md) |
| [social-media-operator](../../../00_skills/(tooling)/social-media-operator/SKILL.md) | Necessidade observada: social. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/dark-videos-mining-fix/README.md:1](../../../02_repositorios/dark-videos-mining-fix/README.md) |

## Uso condicionado

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

169 arquivos candidatos por nome/caminho; não corresponde a quantidade de testes executados. 0 workflows encontrados. Suites não executadas.


## Lacunas

- Pacote de trabalho, não repositório Git independente.
- Não reaplicar automaticamente: README já declara aplicação externa.
- Sem workflow CI próprio no inventário.
