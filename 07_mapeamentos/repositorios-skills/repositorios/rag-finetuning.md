# rag-finetuning — mapa estático de skills

Updated: 2026-11-16

Entry point: ../README.md

Tipo: Git próprio. Arquivos no inventário delimitado: 22; entradas excluídas: 2.

[Voltar ao índice](../README.md) · [Matriz completa](../matriz.csv)

## Dez dimensões

| Dimensão | Estado | Observação | Evidência |
| --- | --- | --- | --- |
| Tecnologias e versões | declarado | Declarações extraídas dos manifests, incluindo faixas e extras. Não são versões instaladas nem prova de compatibilidade. Lockfiles permanecem nas fontes para análise posterior. | [02_repositorios/rag-finetuning/pyproject.toml:10](../../../02_repositorios/rag-finetuning/pyproject.toml); [02_repositorios/rag-finetuning/pyproject.toml:11](../../../02_repositorios/rag-finetuning/pyproject.toml); [02_repositorios/rag-finetuning/pyproject.toml:12](../../../02_repositorios/rag-finetuning/pyproject.toml); demais fontes em mapa.json/declarações abaixo |
| Arquitetura | documentado | Feast feature store e Kubeflow Trainer para treino distribuído documentados. | [02_repositorios/rag-finetuning/README.md:8](../../../02_repositorios/rag-finetuning/README.md) |
| Propósito | declarado | Pipeline de fine-tuning de embeddings RAG com Kubeflow e Feast. | [02_repositorios/rag-finetuning/README.md:1](../../../02_repositorios/rag-finetuning/README.md) |
| Fluxo | documentado | ODFV e negative sampling dinâmico no treino de embeddings 384-d. | [02_repositorios/rag-finetuning/README.md:11](../../../02_repositorios/rag-finetuning/README.md) |
| Dados | documentado | Feast gerencia features; consistência de dimensão declarada. | [02_repositorios/rag-finetuning/README.md:9](../../../02_repositorios/rag-finetuning/README.md) |
| Configuração/deploy | documentado | KIND clusters e TensorBoard local citados; cluster real não verificado. | [02_repositorios/rag-finetuning/README.md:8](../../../02_repositorios/rag-finetuning/README.md) |
| Operação/observabilidade | documentado | Validação end-to-end documentada; não executada neste mapa. | [02_repositorios/rag-finetuning/README.md:14](../../../02_repositorios/rag-finetuning/README.md) |
| Interfaces/dependências | documentado | Integração Feast/Kubeflow; imports fine_tuned podem depender do contexto Feast. | [02_repositorios/rag-finetuning/README.md:10](../../../02_repositorios/rag-finetuning/README.md) |
| Vulnerabilidades | não verificado | Nenhuma consulta atual a advisories/scanner foi executada; não equivale a ausência de CVEs. | Sem verificação nesta missão |
| Obsolescência | não verificado | Datas de suporte/EOL não consultadas. Versões declaradas não comprovam suporte atual. | Sem verificação nesta missão |

## Declarações dos manifests

Faixas e extras são preservados; versões instaladas/resolvidas não foram verificadas.

| Declaração | Valor | Fonte |
| --- | --- | --- |
| name | rag-finetuning | [02_repositorios/rag-finetuning/pyproject.toml:2](../../../02_repositorios/rag-finetuning/pyproject.toml) |
| version | 0.1.0 | [02_repositorios/rag-finetuning/pyproject.toml:3](../../../02_repositorios/rag-finetuning/pyproject.toml) |
| requires-python | >=3.11 | [02_repositorios/rag-finetuning/pyproject.toml:6](../../../02_repositorios/rag-finetuning/pyproject.toml) |
| dependency | bigtree>=0.29.2 | [02_repositorios/rag-finetuning/pyproject.toml:8](../../../02_repositorios/rag-finetuning/pyproject.toml) |
| dependency | datasets==3.6.0 | [02_repositorios/rag-finetuning/pyproject.toml:9](../../../02_repositorios/rag-finetuning/pyproject.toml) |
| dependency | feast[milvus]>=0.51.0 | [02_repositorios/rag-finetuning/pyproject.toml:10](../../../02_repositorios/rag-finetuning/pyproject.toml) |
| dependency | ipython>=9.5.0 | [02_repositorios/rag-finetuning/pyproject.toml:11](../../../02_repositorios/rag-finetuning/pyproject.toml) |
| dependency | kubeflow==0.1.0 | [02_repositorios/rag-finetuning/pyproject.toml:12](../../../02_repositorios/rag-finetuning/pyproject.toml) |
| dependency | kubeflow-sdk>=0.1.9 | [02_repositorios/rag-finetuning/pyproject.toml:13](../../../02_repositorios/rag-finetuning/pyproject.toml) |
| dependency | marshmallow==3.10.0 | [02_repositorios/rag-finetuning/pyproject.toml:14](../../../02_repositorios/rag-finetuning/pyproject.toml) |
| dependency | sentence-transformers>=5.1.0 | [02_repositorios/rag-finetuning/pyproject.toml:15](../../../02_repositorios/rag-finetuning/pyproject.toml) |
| dependency | torch>=2.8.0 | [02_repositorios/rag-finetuning/pyproject.toml:16](../../../02_repositorios/rag-finetuning/pyproject.toml) |
| declaration | kubeflow==0.2.0 | [02_repositorios/rag-finetuning/requirements.txt:2](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | kubeflow-trainer-api>=2.0.0 | [02_repositorios/rag-finetuning/requirements.txt:3](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | kubeflow-katib-api>=0.19.0 | [02_repositorios/rag-finetuning/requirements.txt:4](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | torch>=2.8.0 | [02_repositorios/rag-finetuning/requirements.txt:7](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | sentence-transformers>=3.0.0 | [02_repositorios/rag-finetuning/requirements.txt:8](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | accelerate>=0.26.0 | [02_repositorios/rag-finetuning/requirements.txt:9](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | safetensors>=0.4.3 | [02_repositorios/rag-finetuning/requirements.txt:10](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | pandas>=2.0.0 | [02_repositorios/rag-finetuning/requirements.txt:13](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | numpy>=1.24.0 | [02_repositorios/rag-finetuning/requirements.txt:14](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | pyarrow>=15.0.0 | [02_repositorios/rag-finetuning/requirements.txt:15](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | datasets>=3.0.0 | [02_repositorios/rag-finetuning/requirements.txt:16](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | scikit-learn>=1.0.0 | [02_repositorios/rag-finetuning/requirements.txt:17](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | transformers>=4.41.0,<5.0.0 | [02_repositorios/rag-finetuning/requirements.txt:20](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | tokenizers>=0.22.0,<=0.23.0 | [02_repositorios/rag-finetuning/requirements.txt:21](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | huggingface-hub>=0.20.0 | [02_repositorios/rag-finetuning/requirements.txt:22](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | tensorboard>=2.14.0 | [02_repositorios/rag-finetuning/requirements.txt:25](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | tqdm>=4.65.0 | [02_repositorios/rag-finetuning/requirements.txt:26](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | psutil>=5.9.0 | [02_repositorios/rag-finetuning/requirements.txt:27](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | kubernetes>=27.2.0 | [02_repositorios/rag-finetuning/requirements.txt:30](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | pydantic>=2.10.0 | [02_repositorios/rag-finetuning/requirements.txt:31](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | pyyaml>=5.1 | [02_repositorios/rag-finetuning/requirements.txt:32](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | requests>=2.32.2 | [02_repositorios/rag-finetuning/requirements.txt:33](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | fsspec>=0.8.5 | [02_repositorios/rag-finetuning/requirements.txt:36](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | filelock>=3.0.0 | [02_repositorios/rag-finetuning/requirements.txt:37](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | typing-extensions>=4.10.0 | [02_repositorios/rag-finetuning/requirements.txt:38](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | pillow>=8.0.0 | [02_repositorios/rag-finetuning/requirements.txt:39](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | packaging>=20.0 | [02_repositorios/rag-finetuning/requirements.txt:40](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | scipy>=1.9.0,<1.17.0 | [02_repositorios/rag-finetuning/requirements.txt:47](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | sympy>=1.13.3,<1.15.0 | [02_repositorios/rag-finetuning/requirements.txt:48](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | networkx>=2.5.1,<4.0.0 | [02_repositorios/rag-finetuning/requirements.txt:49](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | jinja2>=3.0.0,<4.0.0 | [02_repositorios/rag-finetuning/requirements.txt:50](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | markdown>=2.6.8,<4.0.0 | [02_repositorios/rag-finetuning/requirements.txt:51](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | protobuf>=3.19.6,!=4.24.0,<7.0.0 | [02_repositorios/rag-finetuning/requirements.txt:52](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | werkzeug>=1.0.1,<4.0.0 | [02_repositorios/rag-finetuning/requirements.txt:53](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | grpcio>=1.48.2,<2.0.0 | [02_repositorios/rag-finetuning/requirements.txt:54](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | absl-py>=0.4,<3.0.0 | [02_repositorios/rag-finetuning/requirements.txt:55](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | google-auth>=1.0.1,<3.0.0 | [02_repositorios/rag-finetuning/requirements.txt:58](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | requests-oauthlib>=1.0.0,<3.0.0 | [02_repositorios/rag-finetuning/requirements.txt:59](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | websocket-client>=0.32.0,!=0.40.0,!=0.41.*,!=0.42.*,<2.0.0 | [02_repositorios/rag-finetuning/requirements.txt:60](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | urllib3>=1.24.2,<2.4.0 | [02_repositorios/rag-finetuning/requirements.txt:61](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | multiprocess>=0.70.0,<0.70.19 | [02_repositorios/rag-finetuning/requirements.txt:64](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | dill>=0.3.0,<0.4.1 | [02_repositorios/rag-finetuning/requirements.txt:65](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | httpx>=0.24.0,<1.0.0 | [02_repositorios/rag-finetuning/requirements.txt:68](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | anyio>=3.0.0,<5.0.0 | [02_repositorios/rag-finetuning/requirements.txt:69](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | certifi>=2020.0.0 | [02_repositorios/rag-finetuning/requirements.txt:70](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | httpcore>=0.15.0,<2.0.0 | [02_repositorios/rag-finetuning/requirements.txt:71](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | idna>=2.10,<4.0.0 | [02_repositorios/rag-finetuning/requirements.txt:72](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | h11>=0.16.0,<1.0.0 | [02_repositorios/rag-finetuning/requirements.txt:73](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | six>=1.9.0,<2.0.0 | [02_repositorios/rag-finetuning/requirements.txt:76](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | python-dateutil>=2.8.2,<3.0.0 | [02_repositorios/rag-finetuning/requirements.txt:77](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | pytz>=2020.1 | [02_repositorios/rag-finetuning/requirements.txt:78](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | tzdata>=2022.7 | [02_repositorios/rag-finetuning/requirements.txt:79](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | click>=8.0.0,<9.0.0 | [02_repositorios/rag-finetuning/requirements.txt:80](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | shellingham>=1.5.0,<2.0.0 | [02_repositorios/rag-finetuning/requirements.txt:81](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | joblib>=1.2.0,<2.0.0 | [02_repositorios/rag-finetuning/requirements.txt:82](../../../02_repositorios/rag-finetuning/requirements.txt) |
| declaration | threadpoolctl>=3.1.0,<4.0.0 | [02_repositorios/rag-finetuning/requirements.txt:83](../../../02_repositorios/rag-finetuning/requirements.txt) |

## Skills diretamente relacionadas

| Skill | Aplicação | Fonte |
| --- | --- | --- |
| [ai-architecture-expert](../../../00_skills/(architecture)/ai-architecture-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/rag-finetuning/README.md:1](../../../02_repositorios/rag-finetuning/README.md) |
| [ai-engineering-expert](../../../00_skills/(development)/ai-engineering-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/rag-finetuning/README.md:1](../../../02_repositorios/rag-finetuning/README.md) |
| [ai-evals-expert](../../../00_skills/(quality)/ai-evals-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/rag-finetuning/README.md:1](../../../02_repositorios/rag-finetuning/README.md) |
| [anti-hallucination-evaluator](../../../00_skills/(quality)/anti-hallucination-evaluator/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/rag-finetuning/README.md:1](../../../02_repositorios/rag-finetuning/README.md) |
| [bm25-expert](../../../00_skills/(development)/bm25-expert/SKILL.md) | Necessidade observada: rag. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/rag-finetuning/README.md:10](../../../02_repositorios/rag-finetuning/README.md) |
| [fine-tuning-expert](../../../00_skills/(development)/fine-tuning-expert/SKILL.md) | Necessidade observada: training. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/rag-finetuning/README.md:1](../../../02_repositorios/rag-finetuning/README.md) |
| [llm-model-selection-expert](../../../00_skills/(development)/llm-model-selection-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/rag-finetuning/README.md:1](../../../02_repositorios/rag-finetuning/README.md) |
| [lora-qlora-dora-expert](../../../00_skills/(development)/lora-qlora-dora-expert/SKILL.md) | Necessidade observada: training. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/rag-finetuning/README.md:1](../../../02_repositorios/rag-finetuning/README.md) |
| [python-bug-solver-skill](../../../00_skills/(development)/python-bug-solver-skill/SKILL.md) | Necessidade observada: python. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/rag-finetuning/README.md:11](../../../02_repositorios/rag-finetuning/README.md) |
| [python-expert](../../../00_skills/(development)/python-expert/SKILL.md) | Necessidade observada: python. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/rag-finetuning/README.md:11](../../../02_repositorios/rag-finetuning/README.md) |
| [python-rag-audit](../../../00_skills/(development)/python-rag-audit/SKILL.md) | Necessidade observada: rag. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/rag-finetuning/README.md:10](../../../02_repositorios/rag-finetuning/README.md) |
| [rag-expert](../../../00_skills/(development)/rag-expert/SKILL.md) | Necessidade observada: rag. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/rag-finetuning/README.md:10](../../../02_repositorios/rag-finetuning/README.md) |

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

0 arquivos candidatos por nome/caminho; não corresponde a quantidade de testes executados. 0 workflows encontrados. Suites não executadas.


## Lacunas

- Imports ausentes removidos localmente no __init__; Feast context obrigatório.
- Integração fim a fim precisa validação runtime.
