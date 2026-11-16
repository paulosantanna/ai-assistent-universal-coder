# rag-finetuning — beta 3.0.0

Updated: 2026-10-27
Entry point: [índice](../README.md) · [mapa estruturado](../mapa.json)

Arquivos com hash: 19; fingerprint: `3fe963f884a4cb4f0383038ce92ad3392b69c6733c6948e750866ba2c668caae`.
Git próprio: True; HEAD: `d33d2f5e7fb43b1d80144d34042a12d213449024`; branch: `main`.
Estado local: há alterações/não rastreados; detalhes em inventory.json.

## Atualizações e reconciliação

Imports fine_tuned ausentes removidos do __init__ local; preserva imports absolutos que dependem do contexto Feast. Integração fim a fim e arquivos ainda citados precisam de validação.

## Dimensões e evidências

### Propósito

**código presente** — Treino de embeddings para recuperação usando SentenceTransformer e Kubeflow.

[rag-finetuning/kubeflow_embedding_training.py:16](../../../02_repositorios/rag-finetuning/kubeflow_embedding_training.py)

### Arquitetura

**código presente** — Função de treinamento, definições Feast e serviços de recuperação descritos separadamente.

[rag-finetuning/feature_repo/__init__.py:4](../../../02_repositorios/rag-finetuning/feature_repo/__init__.py)

### Fluxo

**código presente** — Configura execução distribuída quando WORLD_SIZE existe e instancia SentenceTransformer.

[rag-finetuning/kubeflow_embedding_training.py:116](../../../02_repositorios/rag-finetuning/kubeflow_embedding_training.py)

### Dados

**código presente** — Dataset próprio lê Feast ou fallback Parquet; dados não inspecionados.

[rag-finetuning/kubeflow_embedding_training.py:155](../../../02_repositorios/rag-finetuning/kubeflow_embedding_training.py)

### Interfaces

**código presente** — Imports de feature views existentes substituem os módulos fine_tuned ausentes do relato antigo.

[rag-finetuning/feature_repo/__init__.py:5](../../../02_repositorios/rag-finetuning/feature_repo/__init__.py)

### Configuração/deploy

**declarado** — Docker Compose está presente; serviços não iniciados.

[rag-finetuning/docker-compose.yml:3](../../../02_repositorios/rag-finetuning/docker-compose.yml)

### Operação

**código presente** — Treinamento inicializa SummaryWriter no rank zero.

[rag-finetuning/kubeflow_embedding_training.py:138](../../../02_repositorios/rag-finetuning/kubeflow_embedding_training.py)

### Fine-tuning

**código presente** — Treino de embeddings SentenceTransformer, não de LLM causal.

[rag-finetuning/kubeflow_embedding_training.py:116](../../../02_repositorios/rag-finetuning/kubeflow_embedding_training.py)

### RAG

**declarado** — Feature store Feast e Milvus declarados para recuperação.

[rag-finetuning/feature_repo/feature_store.yaml:6](../../../02_repositorios/rag-finetuning/feature_repo/feature_store.yaml)

### Pós-treino

**não demonstrado na amostra** — Sem conclusão positiva nesta revisão estática; não equivale a ausência universal.


### Inferência

**não demonstrado na amostra** — Sem conclusão positiva nesta revisão estática; não equivale a ausência universal.


### Tecnologias/versões

**declarado** — Ver declarações extraídas e manifests; versões instaladas e compatibilidade não verificadas.

[rag-finetuning/pyproject.toml:10](../../../02_repositorios/rag-finetuning/pyproject.toml)
[rag-finetuning/pyproject.toml:11](../../../02_repositorios/rag-finetuning/pyproject.toml)
[rag-finetuning/pyproject.toml:12](../../../02_repositorios/rag-finetuning/pyproject.toml)
[rag-finetuning/pyproject.toml:13](../../../02_repositorios/rag-finetuning/pyproject.toml)
[rag-finetuning/pyproject.toml:14](../../../02_repositorios/rag-finetuning/pyproject.toml)
[rag-finetuning/pyproject.toml:15](../../../02_repositorios/rag-finetuning/pyproject.toml)
[rag-finetuning/pyproject.toml:16](../../../02_repositorios/rag-finetuning/pyproject.toml)
[rag-finetuning/pyproject.toml:2](../../../02_repositorios/rag-finetuning/pyproject.toml)

### Vulnerabilidades

**não verificado** — Sem consulta de CVE/EOL nesta missão.


### Obsolescência

**não verificado** — Sem consulta de CVE/EOL nesta missão.


## Declarações de versão

| Manifest / declaração | Valor | Evidência |
|---|---|---|
| name | rag-finetuning | [rag-finetuning/pyproject.toml:2](../../../02_repositorios/rag-finetuning/pyproject.toml) |
| version | 0.1.0 | [rag-finetuning/pyproject.toml:3](../../../02_repositorios/rag-finetuning/pyproject.toml) |
| requires-python | >=3.11 | [rag-finetuning/pyproject.toml:6](../../../02_repositorios/rag-finetuning/pyproject.toml) |
| dependency | bigtree>=0.29.2 | [rag-finetuning/pyproject.toml:8](../../../02_repositorios/rag-finetuning/pyproject.toml) |
| dependency | datasets==3.6.0 | [rag-finetuning/pyproject.toml:9](../../../02_repositorios/rag-finetuning/pyproject.toml) |
| dependency | feast[milvus]>=0.51.0 | [rag-finetuning/pyproject.toml:10](../../../02_repositorios/rag-finetuning/pyproject.toml) |
| dependency | ipython>=9.5.0 | [rag-finetuning/pyproject.toml:11](../../../02_repositorios/rag-finetuning/pyproject.toml) |
| dependency | kubeflow==0.1.0 | [rag-finetuning/pyproject.toml:12](../../../02_repositorios/rag-finetuning/pyproject.toml) |
| dependency | kubeflow-sdk>=0.1.9 | [rag-finetuning/pyproject.toml:13](../../../02_repositorios/rag-finetuning/pyproject.toml) |
| dependency | marshmallow==3.10.0 | [rag-finetuning/pyproject.toml:14](../../../02_repositorios/rag-finetuning/pyproject.toml) |
| dependency | sentence-transformers>=5.1.0 | [rag-finetuning/pyproject.toml:15](../../../02_repositorios/rag-finetuning/pyproject.toml) |
| dependency | torch>=2.8.0 | [rag-finetuning/pyproject.toml:16](../../../02_repositorios/rag-finetuning/pyproject.toml) |
| dependency | kubeflow==0.2.0 | [rag-finetuning/requirements.txt:2](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | kubeflow-trainer-api>=2.0.0 | [rag-finetuning/requirements.txt:3](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | kubeflow-katib-api>=0.19.0 | [rag-finetuning/requirements.txt:4](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | torch>=2.8.0 | [rag-finetuning/requirements.txt:7](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | sentence-transformers>=3.0.0 | [rag-finetuning/requirements.txt:8](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | accelerate>=0.26.0 | [rag-finetuning/requirements.txt:9](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | safetensors>=0.4.3 | [rag-finetuning/requirements.txt:10](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | pandas>=2.0.0 | [rag-finetuning/requirements.txt:13](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | numpy>=1.24.0 | [rag-finetuning/requirements.txt:14](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | pyarrow>=15.0.0 | [rag-finetuning/requirements.txt:15](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | datasets>=3.0.0 | [rag-finetuning/requirements.txt:16](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | scikit-learn>=1.0.0 | [rag-finetuning/requirements.txt:17](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | transformers>=4.41.0,<5.0.0 | [rag-finetuning/requirements.txt:20](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | tokenizers>=0.22.0,<=0.23.0 | [rag-finetuning/requirements.txt:21](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | huggingface-hub>=0.20.0 | [rag-finetuning/requirements.txt:22](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | tensorboard>=2.14.0 | [rag-finetuning/requirements.txt:25](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | tqdm>=4.65.0 | [rag-finetuning/requirements.txt:26](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | psutil>=5.9.0 | [rag-finetuning/requirements.txt:27](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | kubernetes>=27.2.0 | [rag-finetuning/requirements.txt:30](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | pydantic>=2.10.0 | [rag-finetuning/requirements.txt:31](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | pyyaml>=5.1 | [rag-finetuning/requirements.txt:32](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | requests>=2.32.2 | [rag-finetuning/requirements.txt:33](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | fsspec>=0.8.5 | [rag-finetuning/requirements.txt:36](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | filelock>=3.0.0 | [rag-finetuning/requirements.txt:37](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | typing-extensions>=4.10.0 | [rag-finetuning/requirements.txt:38](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | pillow>=8.0.0 | [rag-finetuning/requirements.txt:39](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | packaging>=20.0 | [rag-finetuning/requirements.txt:40](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | scipy>=1.9.0,<1.17.0 | [rag-finetuning/requirements.txt:47](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | sympy>=1.13.3,<1.15.0 | [rag-finetuning/requirements.txt:48](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | networkx>=2.5.1,<4.0.0 | [rag-finetuning/requirements.txt:49](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | jinja2>=3.0.0,<4.0.0 | [rag-finetuning/requirements.txt:50](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | markdown>=2.6.8,<4.0.0 | [rag-finetuning/requirements.txt:51](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | protobuf>=3.19.6,!=4.24.0,<7.0.0 | [rag-finetuning/requirements.txt:52](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | werkzeug>=1.0.1,<4.0.0 | [rag-finetuning/requirements.txt:53](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | grpcio>=1.48.2,<2.0.0 | [rag-finetuning/requirements.txt:54](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | absl-py>=0.4,<3.0.0 | [rag-finetuning/requirements.txt:55](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | google-auth>=1.0.1,<3.0.0 | [rag-finetuning/requirements.txt:58](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | requests-oauthlib>=1.0.0,<3.0.0 | [rag-finetuning/requirements.txt:59](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | websocket-client>=0.32.0,!=0.40.0,!=0.41.*,!=0.42.*,<2.0.0 | [rag-finetuning/requirements.txt:60](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | urllib3>=1.24.2,<2.4.0 | [rag-finetuning/requirements.txt:61](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | multiprocess>=0.70.0,<0.70.19 | [rag-finetuning/requirements.txt:64](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | dill>=0.3.0,<0.4.1 | [rag-finetuning/requirements.txt:65](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | httpx>=0.24.0,<1.0.0 | [rag-finetuning/requirements.txt:68](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | anyio>=3.0.0,<5.0.0 | [rag-finetuning/requirements.txt:69](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | certifi>=2020.0.0 | [rag-finetuning/requirements.txt:70](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | httpcore>=0.15.0,<2.0.0 | [rag-finetuning/requirements.txt:71](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | idna>=2.10,<4.0.0 | [rag-finetuning/requirements.txt:72](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | h11>=0.16.0,<1.0.0 | [rag-finetuning/requirements.txt:73](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | six>=1.9.0,<2.0.0 | [rag-finetuning/requirements.txt:76](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | python-dateutil>=2.8.2,<3.0.0 | [rag-finetuning/requirements.txt:77](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | pytz>=2020.1 | [rag-finetuning/requirements.txt:78](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | tzdata>=2022.7 | [rag-finetuning/requirements.txt:79](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | click>=8.0.0,<9.0.0 | [rag-finetuning/requirements.txt:80](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | shellingham>=1.5.0,<2.0.0 | [rag-finetuning/requirements.txt:81](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | joblib>=1.2.0,<2.0.0 | [rag-finetuning/requirements.txt:82](../../../02_repositorios/rag-finetuning/requirements.txt) |
| dependency | threadpoolctl>=3.1.0,<4.0.0 | [rag-finetuning/requirements.txt:83](../../../02_repositorios/rag-finetuning/requirements.txt) |

## Qualidade e limites

Workflows: 0; arquivos candidatos a testes: 0. Não executados.

- Amostra semântica seletiva; hash e busca textual não equivalem a auditoria integral.
- Nenhum runtime, treino, publicação ou sincronização remota executado.
- Fontes modificadas/não rastreadas fazem parte deste snapshot local.
