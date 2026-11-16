# AIHealthResearch — beta 3.0.0

Updated: 2026-10-27
Entry point: [índice](../README.md) · [mapa estruturado](../mapa.json)

Arquivos com hash: 97; fingerprint: `d71672a66f61a57664fc074dcce4c7485ef8bfe574da0fa47937164bb54e65e2`.
Git próprio: True; HEAD: `5878719f17d5272e3aab48e8b2e0b2a7c5ef360c`; branch: `main`.
Estado local: limpo; detalhes em inventory.json.

## Atualizações e reconciliação

Correção de precisão do beta 2: há implementação LoRA/DoRA, não apenas intenção PEFT. Promoção continua separada do treino.

## Dimensões e evidências

### Propósito

**declarado** — Plataforma de pesquisa em diabetes com RAG baseado em evidências, revisão determinística e treino candidato para AWS.

[AIHealthResearch/README.md:3](../../../02_repositorios/AIHealthResearch/README.md)

### Arquitetura

**documentado** — Camadas domain/application/infrastructure/interfaces; documentação separa AWS alvo de laboratório local.

[AIHealthResearch/docs/ARCHITECTURE.md:29](../../../02_repositorios/AIHealthResearch/docs/ARCHITECTURE.md)

### Fluxo

**código presente** — Pesquisa revalida versão das evidências; treino candidato valida snapshot e limita método a LoRA/DoRA.

[AIHealthResearch/src/aihealthresearch/infrastructure/trainer.py:21](../../../02_repositorios/AIHealthResearch/src/aihealthresearch/infrastructure/trainer.py)

### Dados

**observado** — SQLAlchemy mantém knowledge_versions; dados de conhecimento são versionados e auditados.

[AIHealthResearch/src/aihealthresearch/infrastructure/database.py:25](../../../02_repositorios/AIHealthResearch/src/aihealthresearch/infrastructure/database.py)

### Interfaces

**observado** — FastAPI e CLI air; despacho de chamadas usa Choice/Noul, funções permitidas e limiares de confiança.

[AIHealthResearch/src/aihealthresearch/application/dispatch.py:30](../../../02_repositorios/AIHealthResearch/src/aihealthresearch/application/dispatch.py)

### Configuração/deploy

**observado** — Gerador CloudFormation declara VPC e serviços AWS; presença do gerador não comprova implantação.

[AIHealthResearch/infra/render_stack.py:37](../../../02_repositorios/AIHealthResearch/infra/render_stack.py)

### Operação

**observado** — Treino possui callback de telemetria; disponibilidade e métricas reais não verificadas.

[AIHealthResearch/src/aihealthresearch/infrastructure/trainer.py:73](../../../02_repositorios/AIHealthResearch/src/aihealthresearch/infrastructure/trainer.py)

### Fine-tuning

**código presente** — LoRA/DoRA causal LM implementados; artefato candidato permanece promoted=false e validação científica pendente.

[AIHealthResearch/src/aihealthresearch/infrastructure/trainer.py:132](../../../02_repositorios/AIHealthResearch/src/aihealthresearch/infrastructure/trainer.py)

### RAG

**código presente** — Recuperação BM25/vetorial com evidências versionadas.

[AIHealthResearch/src/aihealthresearch/infrastructure/search.py:9](../../../02_repositorios/AIHealthResearch/src/aihealthresearch/infrastructure/search.py)

### Pós-treino

**não demonstrado na amostra** — Sem conclusão positiva nesta revisão estática; não equivale a ausência universal.


### Inferência

**não demonstrado na amostra** — Sem conclusão positiva nesta revisão estática; não equivale a ausência universal.


### Tecnologias/versões

**declarado** — Ver declarações extraídas e manifests; versões instaladas e compatibilidade não verificadas.

[AIHealthResearch/pyproject.toml:10](../../../02_repositorios/AIHealthResearch/pyproject.toml)
[AIHealthResearch/pyproject.toml:11](../../../02_repositorios/AIHealthResearch/pyproject.toml)
[AIHealthResearch/pyproject.toml:12](../../../02_repositorios/AIHealthResearch/pyproject.toml)
[AIHealthResearch/pyproject.toml:5](../../../02_repositorios/AIHealthResearch/pyproject.toml)
[AIHealthResearch/pyproject.toml:6](../../../02_repositorios/AIHealthResearch/pyproject.toml)
[AIHealthResearch/pyproject.toml:7](../../../02_repositorios/AIHealthResearch/pyproject.toml)
[AIHealthResearch/pyproject.toml:8](../../../02_repositorios/AIHealthResearch/pyproject.toml)
[AIHealthResearch/requirements.txt:1](../../../02_repositorios/AIHealthResearch/requirements.txt)

### Vulnerabilidades

**não verificado** — Sem consulta de CVE/EOL nesta missão.


### Obsolescência

**não verificado** — Sem consulta de CVE/EOL nesta missão.


## Declarações de versão

| Manifest / declaração | Valor | Evidência |
|---|---|---|
| name | aihealthresearch | [AIHealthResearch/pyproject.toml:5](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| version | 0.2.0 | [AIHealthResearch/pyproject.toml:6](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| requires-python | >=3.12,<3.13 | [AIHealthResearch/pyproject.toml:7](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| dependency | fastapi==0.141.1 | [AIHealthResearch/pyproject.toml:8](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| dependency | uvicorn==0.52.4 | [AIHealthResearch/pyproject.toml:8](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| dependency | SQLAlchemy==2.0.52 | [AIHealthResearch/pyproject.toml:8](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| dependency | psycopg[binary]==3.3.5 | [AIHealthResearch/pyproject.toml:8](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| dependency | httpx==0.28.1 | [AIHealthResearch/pyproject.toml:8](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| dependency | PyJWT[crypto]==2.14.0 | [AIHealthResearch/pyproject.toml:8](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| dependency | boto3==1.43.93 | [AIHealthResearch/pyproject.toml:8](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| dependency | opensearch-py==3.2.0 | [AIHealthResearch/pyproject.toml:8](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| dependency | defusedxml==0.7.1 | [AIHealthResearch/pyproject.toml:8](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| extra:dev | pytest==9.1.1 | [AIHealthResearch/pyproject.toml:10](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| extra:dev | ruff==0.16.7 | [AIHealthResearch/pyproject.toml:10](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| extra:dev | bandit==1.9.4 | [AIHealthResearch/pyproject.toml:10](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| extra:dev | pip-audit==2.10.1 | [AIHealthResearch/pyproject.toml:10](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| extra:dev | cfn-lint==1.56.3 | [AIHealthResearch/pyproject.toml:10](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| extra:ml | torch==2.14.0 | [AIHealthResearch/pyproject.toml:11](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| extra:ml | transformers==5.17.0 | [AIHealthResearch/pyproject.toml:11](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| extra:ml | peft==0.20.0 | [AIHealthResearch/pyproject.toml:11](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| extra:ml | accelerate==1.15.0 | [AIHealthResearch/pyproject.toml:11](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| extra:vector | sentence-transformers>=5.1,<6 | [AIHealthResearch/pyproject.toml:12](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| extra:vector | chromadb>=1,<2 | [AIHealthResearch/pyproject.toml:12](../../../02_repositorios/AIHealthResearch/pyproject.toml) |
| dependency | fastapi>=0.116.0 | [AIHealthResearch/requirements.txt:1](../../../02_repositorios/AIHealthResearch/requirements.txt) |
| dependency | strawberry-graphql>=0.275.0 | [AIHealthResearch/requirements.txt:2](../../../02_repositorios/AIHealthResearch/requirements.txt) |
| dependency | uvicorn>=0.35.0 | [AIHealthResearch/requirements.txt:3](../../../02_repositorios/AIHealthResearch/requirements.txt) |
| dependency | pydantic>=2.11.0 | [AIHealthResearch/requirements.txt:4](../../../02_repositorios/AIHealthResearch/requirements.txt) |
| dependency | boto3>=1.40.0 | [AIHealthResearch/requirements.txt:5](../../../02_repositorios/AIHealthResearch/requirements.txt) |
| dependency | chromadb>=1.0.0 | [AIHealthResearch/requirements.txt:6](../../../02_repositorios/AIHealthResearch/requirements.txt) |
| dependency | rank-bm25>=0.2.2 | [AIHealthResearch/requirements.txt:7](../../../02_repositorios/AIHealthResearch/requirements.txt) |
| dependency | numpy>=2.0.0 | [AIHealthResearch/requirements.txt:8](../../../02_repositorios/AIHealthResearch/requirements.txt) |
| dependency | python-dotenv>=1.1.0 | [AIHealthResearch/requirements.txt:9](../../../02_repositorios/AIHealthResearch/requirements.txt) |

## Qualidade e limites

Workflows: 2; arquivos candidatos a testes: 16. Não executados.

- Amostra semântica seletiva; hash e busca textual não equivalem a auditoria integral.
- Nenhum runtime, treino, publicação ou sincronização remota executado.
- Fontes modificadas/não rastreadas fazem parte deste snapshot local.
