# ibunny — mapa estático de skills

Updated: 2026-10-13

Entry point: ../README.md

Tipo: Git próprio. Arquivos no inventário delimitado: 205; entradas excluídas: 4.

[Voltar ao índice](../README.md) · [Matriz completa](../matriz.csv)

## Dez dimensões

| Dimensão | Estado | Observação | Evidência |
| --- | --- | --- | --- |
| Tecnologias e versões | declarado | Declarações extraídas dos manifests, incluindo faixas e extras. Não são versões instaladas nem prova de compatibilidade. Lockfiles permanecem nas fontes para análise posterior. | [02_repositorios/ibunny/apps/client/pubspec.yaml:12](../../../02_repositorios/ibunny/apps/client/pubspec.yaml); [02_repositorios/ibunny/apps/client/pubspec.yaml:13](../../../02_repositorios/ibunny/apps/client/pubspec.yaml); [02_repositorios/ibunny/apps/client/pubspec.yaml:14](../../../02_repositorios/ibunny/apps/client/pubspec.yaml); demais fontes em mapa.json/declarações abaixo |
| Arquitetura | observado | Cliente Flutter/Dart e API Go modular com runner separado; Flame só está mencionado na documentação. | [02_repositorios/ibunny/apps/client/pubspec.yaml:8](../../../02_repositorios/ibunny/apps/client/pubspec.yaml) |
| Propósito | declarado | Jogo educacional 2D com missões de programação, XP e créditos bônus. | [02_repositorios/ibunny/README.md:3](../../../02_repositorios/ibunny/README.md) |
| Fluxo | observado | Servidor Go oferece POST /v1/missions/next; runner de avaliação retorna passed=false com marcador de stub. | [02_repositorios/ibunny/services/api/internal/adapters/http/server.go:38](../../../02_repositorios/ibunny/services/api/internal/adapters/http/server.go) |
| Dados | observado | Demonstração usa ledger em memória; Store PostgreSQL permanece stub até conectar Compose/Postgres. | [02_repositorios/ibunny/services/api/internal/adapters/postgres/store.go:3](../../../02_repositorios/ibunny/services/api/internal/adapters/postgres/store.go) |
| Configuração/deploy | documentado | Compose e esqueleto Kubernetes estão presentes; README distingue funcionalidades fora desta fatia. | [02_repositorios/ibunny/README.md:73](../../../02_repositorios/ibunny/README.md) |
| Operação/observabilidade | observado | Runner oferece /healthz, mas saúde do processo não comprova execução de código educacional. | [02_repositorios/ibunny/services/runner/cmd/runner/main.go:22](../../../02_repositorios/ibunny/services/runner/cmd/runner/main.go) |
| Interfaces/dependências | documentado | API HTTP serve missões; XP e saldo são autoridade do servidor conforme contrato local. | [02_repositorios/ibunny/AGENTS.md:62](../../../02_repositorios/ibunny/AGENTS.md) |
| Vulnerabilidades | não verificado | Nenhuma consulta atual a advisories/scanner foi executada; não equivale a ausência de CVEs. | Sem verificação nesta missão |
| Obsolescência | não verificado | Datas de suporte/EOL não consultadas. Versões declaradas não comprovam suporte atual. | Sem verificação nesta missão |

## Declarações dos manifests

Faixas e extras são preservados; versões instaladas/resolvidas não foram verificadas.

| Declaração | Valor | Fonte |
| --- | --- | --- |
| declaration | version: 1.0.0-alpha.8+108 | [02_repositorios/ibunny/apps/client/pubspec.yaml:4](../../../02_repositorios/ibunny/apps/client/pubspec.yaml) |
| declaration | sdk: ">=3.12.0 <4.0.0" | [02_repositorios/ibunny/apps/client/pubspec.yaml:7](../../../02_repositorios/ibunny/apps/client/pubspec.yaml) |
| declaration | flutter: ">=3.44.0" | [02_repositorios/ibunny/apps/client/pubspec.yaml:8](../../../02_repositorios/ibunny/apps/client/pubspec.yaml) |
| declaration | flutter: | [02_repositorios/ibunny/apps/client/pubspec.yaml:8](../../../02_repositorios/ibunny/apps/client/pubspec.yaml) |
| declaration | sdk: flutter | [02_repositorios/ibunny/apps/client/pubspec.yaml:12](../../../02_repositorios/ibunny/apps/client/pubspec.yaml) |
| declaration | audioplayers: ^6.8.1 | [02_repositorios/ibunny/apps/client/pubspec.yaml:13](../../../02_repositorios/ibunny/apps/client/pubspec.yaml) |
| declaration | http: ^1.6.0 | [02_repositorios/ibunny/apps/client/pubspec.yaml:14](../../../02_repositorios/ibunny/apps/client/pubspec.yaml) |
| declaration | speech_to_text: ^7.5.0 | [02_repositorios/ibunny/apps/client/pubspec.yaml:16](../../../02_repositorios/ibunny/apps/client/pubspec.yaml) |
| declaration | sdk: flutter | [02_repositorios/ibunny/apps/client/pubspec.yaml:12](../../../02_repositorios/ibunny/apps/client/pubspec.yaml) |
| declaration | flutter: | [02_repositorios/ibunny/apps/client/pubspec.yaml:8](../../../02_repositorios/ibunny/apps/client/pubspec.yaml) |
| declaration | module github.com/paulosantanna/ibunny/services/api | [02_repositorios/ibunny/services/api/go.mod:1](../../../02_repositorios/ibunny/services/api/go.mod) |
| declaration | go 1.22 | [02_repositorios/ibunny/services/api/go.mod:3](../../../02_repositorios/ibunny/services/api/go.mod) |
| declaration | module github.com/paulosantanna/ibunny/services/runner | [02_repositorios/ibunny/services/runner/go.mod:1](../../../02_repositorios/ibunny/services/runner/go.mod) |
| declaration | go 1.22 | [02_repositorios/ibunny/services/runner/go.mod:3](../../../02_repositorios/ibunny/services/runner/go.mod) |

## Skills diretamente relacionadas

| Skill | Aplicação | Fonte |
| --- | --- | --- |
| [ci-quality-gate-engineer](../../../00_skills/(development)/ci-quality-gate-engineer/SKILL.md) | Necessidade observada: ci. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/ibunny/.github/workflows/cd-skeleton.yml:1](../../../02_repositorios/ibunny/.github/workflows/cd-skeleton.yml); [02_repositorios/ibunny/.github/workflows/ci.yml:1](../../../02_repositorios/ibunny/.github/workflows/ci.yml) |
| [database-architecture-planner](../../../00_skills/(architecture)/database-architecture-planner/SKILL.md) | Especialização adequada ao contrato/estrutura observados; ativar apenas na tarefa correspondente. | [02_repositorios/ibunny/AGENTS.md:62](../../../02_repositorios/ibunny/AGENTS.md); [02_repositorios/ibunny/services/api/internal/adapters/http/server.go:38](../../../02_repositorios/ibunny/services/api/internal/adapters/http/server.go) |
| [deployment-pipeline-expert](../../../00_skills/(cloud)/deployment-pipeline-expert/SKILL.md) | Necessidade observada: ci. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/ibunny/.github/workflows/cd-skeleton.yml:1](../../../02_repositorios/ibunny/.github/workflows/cd-skeleton.yml); [02_repositorios/ibunny/.github/workflows/ci.yml:1](../../../02_repositorios/ibunny/.github/workflows/ci.yml) |
| [devops-pipeline-engineering](../../../00_skills/(cloud)/devops-pipeline-engineering/SKILL.md) | Necessidade observada: ci. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/ibunny/.github/workflows/cd-skeleton.yml:1](../../../02_repositorios/ibunny/.github/workflows/cd-skeleton.yml); [02_repositorios/ibunny/.github/workflows/ci.yml:1](../../../02_repositorios/ibunny/.github/workflows/ci.yml) |
| [domain-analysis](../../../00_skills/(architecture)/domain-analysis/SKILL.md) | Especialização adequada ao contrato/estrutura observados; ativar apenas na tarefa correspondente. | [02_repositorios/ibunny/AGENTS.md:62](../../../02_repositorios/ibunny/AGENTS.md); [02_repositorios/ibunny/services/api/internal/adapters/http/server.go:38](../../../02_repositorios/ibunny/services/api/internal/adapters/http/server.go) |
| [gh-fix-ci](../../../00_skills/(tooling)/gh-fix-ci/SKILL.md) | Necessidade observada: ci. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/ibunny/.github/workflows/cd-skeleton.yml:1](../../../02_repositorios/ibunny/.github/workflows/cd-skeleton.yml); [02_repositorios/ibunny/.github/workflows/ci.yml:1](../../../02_repositorios/ibunny/.github/workflows/ci.yml) |
| [modular-design-principles](../../../00_skills/(architecture)/modular-design-principles/SKILL.md) | Especialização adequada ao contrato/estrutura observados; ativar apenas na tarefa correspondente. | [02_repositorios/ibunny/AGENTS.md:62](../../../02_repositorios/ibunny/AGENTS.md); [02_repositorios/ibunny/services/api/internal/adapters/http/server.go:38](../../../02_repositorios/ibunny/services/api/internal/adapters/http/server.go) |
| [tactical-ddd](../../../00_skills/(architecture)/tactical-ddd/SKILL.md) | Especialização adequada ao contrato/estrutura observados; ativar apenas na tarefa correspondente. | [02_repositorios/ibunny/AGENTS.md:62](../../../02_repositorios/ibunny/AGENTS.md); [02_repositorios/ibunny/services/api/internal/adapters/http/server.go:38](../../../02_repositorios/ibunny/services/api/internal/adapters/http/server.go) |

## Uso condicionado

- **atualizar-dependencias**: Somente em missão de atualização com baseline e compatibilidade.
- **compatibility-analyzer**: Ao verificar troca de linguagem/runtime/dependência.
- **dependency-updater**: Somente em atualização autorizada, preservando lockfiles.
- **github-operations**: Ao operar GitHub com alvo, credenciais e autorização próprios.
- **kotlin-expert**: Wrapper Android contém Kotlin; não cobre o cliente Dart.
- **kubernetes-code-context-mapper**: Manifests/esqueleto Kubernetes presentes; acesso a cluster não verificado.
- **local-secret-vault**: Só se a tarefa depender de credenciais autorizadas; não abrir para mapear.
- **observability-root-cause-integrator**: Requer incidente/sintomas e telemetria atual.
- **pr-reviewer**: Requer PR/diff concreto.
- **pr-reviewer-advanced**: Requer PR/diff concreto e evidências de revisão.
- **release-readiness-judge**: Requer release concreta e checks determinísticos.
- **girl-voice-composer-simulation-expert**: Skill local de voz foi encontrada; gravação/TTS requer engine e escopo próprios.
- **frontend-design**: Princípios visuais reaproveitáveis; não cobre APIs Flutter.
- **gh-address-comments**: Requer comentários de PR e alvo concreto.
- **cve-advisory-sync**: Só ao solicitar consulta atual de advisories oficiais.
- **cve-remediation**: Requer CVE/GHSA concreto, versão afetada e correção autorizada.
- **eol-advisory-sync**: Requer consulta atual de suporte oficial para os produtos declarados.
- **revisar-seguranca-pr**: Requer diff de PR e escopo de segurança.
- **vuln-obsol-recon**: Inventário estático é ponto de partida; auditoria de CVE/EOL não foi executada.
- **runtime-troubleshooting**: Requer runtime/logs atuais; o mapa é estático.

## Testes/CI

6 arquivos candidatos por nome/caminho; não corresponde a quantidade de testes executados. 2 workflows encontrados. Suites não executadas.

- [02_repositorios/ibunny/.github/workflows/cd-skeleton.yml:1](../../../02_repositorios/ibunny/.github/workflows/cd-skeleton.yml)
- [02_repositorios/ibunny/.github/workflows/ci.yml:1](../../../02_repositorios/ibunny/.github/workflows/ci.yml)

## Lacunas

- Não há skills canônicas específicas de Go ou Flutter/Dart.
- Flame não aparece nas dependências do pubspec.yaml.
- Runner e persistência PostgreSQL ainda são stubs.
