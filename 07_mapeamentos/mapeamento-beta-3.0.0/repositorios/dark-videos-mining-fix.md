# dark-videos-mining-fix — beta 3.0.0

Updated: 2026-10-27
Entry point: [índice](../README.md) · [mapa estruturado](../mapa.json)

Arquivos com hash: 449; fingerprint: `27c07a49cee7d2cc61e84fa368273ad2c71a31a1e6825730035d28bc367d9852`.
Git próprio: False; HEAD: `não aplicável`; branch: `não aplicável`.
Estado local: pacote sem Git próprio; detalhes em inventory.json.

## Atualizações e reconciliação

Continua pacote sem Git próprio; README histórico de aplicação não prova sincronização com dark-videos atual.

## Dimensões e evidências

### Propósito

**declarado** — Pacote de correção de mineração pt-BR, deduplicação e inspeção do vídeo original para dark-videos.

[dark-videos-mining-fix/README.md:1](../../../02_repositorios/dark-videos-mining-fix/README.md)

### Arquitetura

**observado** — Pacote com cópia backend, alterações frontend e ferramenta de aplicação; não tem Git próprio.

[dark-videos-mining-fix/package.py:60](../../../02_repositorios/dark-videos-mining-fix/package.py)

### Fluxo

**documentado** — Política documentada admite título OU descrição pt-BR e exige inspeção do original antes da moldura.

[dark-videos-mining-fix/README.md:9](../../../02_repositorios/dark-videos-mining-fix/README.md)

### Dados

**observado** — Herda a base SQLAlchemy/JSONB do backend; não é outro serviço de dados independente.

[dark-videos-mining-fix/backend/app/db/base.py:11](../../../02_repositorios/dark-videos-mining-fix/backend/app/db/base.py)

### Interfaces

**observado** — Metadados são avaliados por política específica; adaptadores não garantem acesso funcional aos provedores.

[dark-videos-mining-fix/backend/app/modules/mining/metadata_policy.py:53](../../../02_repositorios/dark-videos-mining-fix/backend/app/modules/mining/metadata_policy.py)

### Configuração/deploy

**documentado** — README aponta aplicação externa em D:/Git/dark-videos; estado histórico não prova os arquivos do espelho atual.

[dark-videos-mining-fix/README.md:3](../../../02_repositorios/dark-videos-mining-fix/README.md)

### Operação

**observado** — Harness run_checks define verificações; os resultados existentes são históricos e não foram reexecutados.

[dark-videos-mining-fix/run_checks.py:25](../../../02_repositorios/dark-videos-mining-fix/run_checks.py)

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

[dark-videos-mining-fix/backend/pyproject.toml:10](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml)
[dark-videos-mining-fix/backend/pyproject.toml:11](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml)
[dark-videos-mining-fix/backend/pyproject.toml:12](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml)
[dark-videos-mining-fix/backend/pyproject.toml:13](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml)
[dark-videos-mining-fix/backend/pyproject.toml:14](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml)
[dark-videos-mining-fix/backend/pyproject.toml:15](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml)
[dark-videos-mining-fix/backend/pyproject.toml:16](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml)
[dark-videos-mining-fix/backend/pyproject.toml:17](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml)

### Vulnerabilidades

**não verificado** — Sem consulta de CVE/EOL nesta missão.


### Obsolescência

**não verificado** — Sem consulta de CVE/EOL nesta missão.


## Declarações de versão

| Manifest / declaração | Valor | Evidência |
|---|---|---|
| name | dark-videos-backend | [dark-videos-mining-fix/backend/pyproject.toml:2](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| version | 0.1.0 | [dark-videos-mining-fix/backend/pyproject.toml:3](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| requires-python | >=3.12 | [dark-videos-mining-fix/backend/pyproject.toml:5](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | alembic>=1.20.0 | [dark-videos-mining-fix/backend/pyproject.toml:7](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | argon2-cffi>=25.1.0 | [dark-videos-mining-fix/backend/pyproject.toml:8](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | celery[redis]>=5.6.3 | [dark-videos-mining-fix/backend/pyproject.toml:9](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | cryptography>=50.0.2 | [dark-videos-mining-fix/backend/pyproject.toml:10](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | email-validator>=2.3.0 | [dark-videos-mining-fix/backend/pyproject.toml:11](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | fastapi>=0.142.2 | [dark-videos-mining-fix/backend/pyproject.toml:12](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | httpx>=0.28.1 | [dark-videos-mining-fix/backend/pyproject.toml:13](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | langdetect==1.0.9 | [dark-videos-mining-fix/backend/pyproject.toml:14](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | pgvector>=0.5.0 | [dark-videos-mining-fix/backend/pyproject.toml:15](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | playwright>=1.55 | [dark-videos-mining-fix/backend/pyproject.toml:16](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | pillow>=11 | [dark-videos-mining-fix/backend/pyproject.toml:17](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | psycopg[binary]>=3.3.6 | [dark-videos-mining-fix/backend/pyproject.toml:18](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | pydantic>=2.13.5 | [dark-videos-mining-fix/backend/pyproject.toml:19](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | pydantic-settings>=2.15.0 | [dark-videos-mining-fix/backend/pyproject.toml:20](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | redis>=6.4.0 | [dark-videos-mining-fix/backend/pyproject.toml:21](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | sqlalchemy>=2.1.3 | [dark-videos-mining-fix/backend/pyproject.toml:22](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | uvicorn[standard]>=0.54.0 | [dark-videos-mining-fix/backend/pyproject.toml:23](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | yt-dlp>=2025.10.14 | [dark-videos-mining-fix/backend/pyproject.toml:24](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | opentelemetry-api>=1.45.1 | [dark-videos-mining-fix/backend/pyproject.toml:25](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | opentelemetry-sdk>=1.45.1 | [dark-videos-mining-fix/backend/pyproject.toml:26](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | opentelemetry-exporter-otlp-proto-http>=1.45.1 | [dark-videos-mining-fix/backend/pyproject.toml:27](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |
| dependency | opentelemetry-instrumentation-fastapi>=0.66b1 | [dark-videos-mining-fix/backend/pyproject.toml:28](../../../02_repositorios/dark-videos-mining-fix/backend/pyproject.toml) |

## Qualidade e limites

Workflows: 0; arquivos candidatos a testes: 177. Não executados.

- Amostra semântica seletiva; hash e busca textual não equivalem a auditoria integral.
- Nenhum runtime, treino, publicação ou sincronização remota executado.
- Fontes modificadas/não rastreadas fazem parte deste snapshot local.
