# ibunny — beta 3.0.0

Updated: 2026-10-27
Entry point: [índice](../README.md) · [mapa estruturado](../mapa.json)

Arquivos com hash: 101; fingerprint: `8e61e23c46947e4cf3812d4fc3e8be8a83f26928551542f3f36ec79104652da0`.
Git próprio: True; HEAD: `0e1c4ae893d39a6be6eb199e02e69c2aee4d6fa2`; branch: `develop`.
Estado local: limpo; detalhes em inventory.json.

## Atualizações e reconciliação

Branch develop registrada; arquitetura Flutter/Go mantida. Nenhum pipeline LLM demonstrado na amostra.

## Dimensões e evidências

### Propósito

**declarado** — Jogo educacional 2D com missões de programação, XP e créditos bônus.

[ibunny/README.md:3](../../../02_repositorios/ibunny/README.md)

### Arquitetura

**observado** — Cliente Flutter/Dart e API Go modular com runner separado; Flame só está mencionado na documentação.

[ibunny/apps/client/pubspec.yaml:8](../../../02_repositorios/ibunny/apps/client/pubspec.yaml)

### Fluxo

**observado** — Servidor Go oferece POST /v1/missions/next; runner de avaliação retorna passed=false com marcador de stub.

[ibunny/services/api/internal/adapters/http/server.go:38](../../../02_repositorios/ibunny/services/api/internal/adapters/http/server.go)

### Dados

**observado** — Demonstração usa ledger em memória; Store PostgreSQL permanece stub até conectar Compose/Postgres.

[ibunny/services/api/internal/adapters/postgres/store.go:3](../../../02_repositorios/ibunny/services/api/internal/adapters/postgres/store.go)

### Interfaces

**documentado** — API HTTP serve missões; XP e saldo são autoridade do servidor conforme contrato local.

[ibunny/AGENTS.md:62](../../../02_repositorios/ibunny/AGENTS.md)

### Configuração/deploy

**documentado** — Compose e esqueleto Kubernetes estão presentes; README distingue funcionalidades fora desta fatia.

[ibunny/README.md:73](../../../02_repositorios/ibunny/README.md)

### Operação

**observado** — Runner oferece /healthz, mas saúde do processo não comprova execução de código educacional.

[ibunny/services/runner/cmd/runner/main.go:22](../../../02_repositorios/ibunny/services/runner/cmd/runner/main.go)

### Fine-tuning

**não demonstrado na amostra** — Sem conclusão positiva nesta revisão estática; não equivale a ausência universal.


### RAG

**não demonstrado na amostra** — Sem conclusão positiva nesta revisão estática; não equivale a ausência universal.


### Pós-treino

**não demonstrado na amostra** — Sem conclusão positiva nesta revisão estática; não equivale a ausência universal.


### Inferência

**não demonstrado na amostra** — Sem conclusão positiva nesta revisão estática; não equivale a ausência universal.


### Tecnologias/versões

**declarado** — Ver declarações extraídas e manifests; versões instaladas e compatibilidade não verificadas.

[ibunny/apps/client/pubspec.yaml:12](../../../02_repositorios/ibunny/apps/client/pubspec.yaml)
[ibunny/apps/client/pubspec.yaml:4](../../../02_repositorios/ibunny/apps/client/pubspec.yaml)
[ibunny/apps/client/pubspec.yaml:7](../../../02_repositorios/ibunny/apps/client/pubspec.yaml)
[ibunny/apps/client/pubspec.yaml:8](../../../02_repositorios/ibunny/apps/client/pubspec.yaml)
[ibunny/services/api/go.mod:1](../../../02_repositorios/ibunny/services/api/go.mod)
[ibunny/services/api/go.mod:3](../../../02_repositorios/ibunny/services/api/go.mod)
[ibunny/services/runner/go.mod:1](../../../02_repositorios/ibunny/services/runner/go.mod)
[ibunny/services/runner/go.mod:3](../../../02_repositorios/ibunny/services/runner/go.mod)

### Vulnerabilidades

**não verificado** — Sem consulta de CVE/EOL nesta missão.


### Obsolescência

**não verificado** — Sem consulta de CVE/EOL nesta missão.


## Declarações de versão

| Manifest / declaração | Valor | Evidência |
|---|---|---|
| runtime | version: 1.0.0-alpha.8+108 | [ibunny/apps/client/pubspec.yaml:4](../../../02_repositorios/ibunny/apps/client/pubspec.yaml) |
| runtime | sdk: ">=3.12.0 <4.0.0" | [ibunny/apps/client/pubspec.yaml:7](../../../02_repositorios/ibunny/apps/client/pubspec.yaml) |
| runtime | flutter: ">=3.44.0" | [ibunny/apps/client/pubspec.yaml:8](../../../02_repositorios/ibunny/apps/client/pubspec.yaml) |
| runtime | flutter: | [ibunny/apps/client/pubspec.yaml:8](../../../02_repositorios/ibunny/apps/client/pubspec.yaml) |
| runtime | sdk: flutter | [ibunny/apps/client/pubspec.yaml:12](../../../02_repositorios/ibunny/apps/client/pubspec.yaml) |
| runtime | sdk: flutter | [ibunny/apps/client/pubspec.yaml:12](../../../02_repositorios/ibunny/apps/client/pubspec.yaml) |
| runtime | flutter: | [ibunny/apps/client/pubspec.yaml:8](../../../02_repositorios/ibunny/apps/client/pubspec.yaml) |
| runtime | module github.com/paulosantanna/ibunny/services/api | [ibunny/services/api/go.mod:1](../../../02_repositorios/ibunny/services/api/go.mod) |
| runtime | go 1.22 | [ibunny/services/api/go.mod:3](../../../02_repositorios/ibunny/services/api/go.mod) |
| runtime | module github.com/paulosantanna/ibunny/services/runner | [ibunny/services/runner/go.mod:1](../../../02_repositorios/ibunny/services/runner/go.mod) |
| runtime | go 1.22 | [ibunny/services/runner/go.mod:3](../../../02_repositorios/ibunny/services/runner/go.mod) |

## Qualidade e limites

Workflows: 2; arquivos candidatos a testes: 5. Não executados.

- Amostra semântica seletiva; hash e busca textual não equivalem a auditoria integral.
- Nenhum runtime, treino, publicação ou sincronização remota executado.
- Fontes modificadas/não rastreadas fazem parte deste snapshot local.
