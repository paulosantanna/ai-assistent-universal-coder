# rag-and-fine-tuning-demo — mapa estático de skills

Updated: 2026-11-16

Entry point: ../README.md

Tipo: Git próprio. Arquivos no inventário delimitado: 16; entradas excluídas: 1.

[Voltar ao índice](../README.md) · [Matriz completa](../matriz.csv)

## Dez dimensões

| Dimensão | Estado | Observação | Evidência |
| --- | --- | --- | --- |
| Tecnologias e versões | declarado | Declarações extraídas dos manifests, incluindo faixas e extras. Não são versões instaladas nem prova de compatibilidade. Lockfiles permanecem nas fontes para análise posterior. | [02_repositorios/rag-and-fine-tuning-demo/requirements.txt:1](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt); [02_repositorios/rag-and-fine-tuning-demo/requirements.txt:10](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt); [02_repositorios/rag-and-fine-tuning-demo/requirements.txt:11](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt); demais fontes em mapa.json/declarações abaixo |
| Arquitetura | documentado | Workspace de tutorial com múltiplos caminhos de integração de dados. | [02_repositorios/rag-and-fine-tuning-demo/README.md:19](../../../02_repositorios/rag-and-fine-tuning-demo/README.md) |
| Propósito | declarado | Demo educacional comparando RAG, fine-tuning e abordagem híbrida. | [02_repositorios/rag-and-fine-tuning-demo/README.md:5](../../../02_repositorios/rag-and-fine-tuning-demo/README.md) |
| Fluxo | documentado | RAG dá acesso open-book; fine-tuning internaliza conhecimento de domínio. | [02_repositorios/rag-and-fine-tuning-demo/README.md:17](../../../02_repositorios/rag-and-fine-tuning-demo/README.md) |
| Dados | documentado | Perfil de domínio específico no README; licença e direitos do corpus não verificados. | [02_repositorios/rag-and-fine-tuning-demo/README.md:9](../../../02_repositorios/rag-and-fine-tuning-demo/README.md) |
| Configuração/deploy | documentado | Entrada chama use_cuda=False no padrão observado historicamente; CUDA opcional. | [02_repositorios/rag-and-fine-tuning-demo/README.md:13](../../../02_repositorios/rag-and-fine-tuning-demo/README.md) |
| Operação/observabilidade | documentado | Demonstração local; sem observabilidade de produção. | [02_repositorios/rag-and-fine-tuning-demo/README.md:2](../../../02_repositorios/rag-and-fine-tuning-demo/README.md) |
| Interfaces/dependências | documentado | Scripts Python de tutorial; endpoints não são serviço gerenciado. | [02_repositorios/rag-and-fine-tuning-demo/README.md:5](../../../02_repositorios/rag-and-fine-tuning-demo/README.md) |
| Vulnerabilidades | não verificado | Nenhuma consulta atual a advisories/scanner foi executada; não equivale a ausência de CVEs. | Sem verificação nesta missão |
| Obsolescência | não verificado | Datas de suporte/EOL não consultadas. Versões declaradas não comprovam suporte atual. | Sem verificação nesta missão |

## Declarações dos manifests

Faixas e extras são preservados; versões instaladas/resolvidas não foram verificadas.

| Declaração | Valor | Fonte |
| --- | --- | --- |
| declaration | langchain | [02_repositorios/rag-and-fine-tuning-demo/requirements.txt:1](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| declaration | langchain-ollama | [02_repositorios/rag-and-fine-tuning-demo/requirements.txt:2](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| declaration | langchain-huggingface | [02_repositorios/rag-and-fine-tuning-demo/requirements.txt:3](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| declaration | langchain-community | [02_repositorios/rag-and-fine-tuning-demo/requirements.txt:4](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| declaration | langchain-text-splitters | [02_repositorios/rag-and-fine-tuning-demo/requirements.txt:5](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| declaration | faiss-cpu | [02_repositorios/rag-and-fine-tuning-demo/requirements.txt:6](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| declaration | transformers | [02_repositorios/rag-and-fine-tuning-demo/requirements.txt:7](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| declaration | peft | [02_repositorios/rag-and-fine-tuning-demo/requirements.txt:8](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| declaration | accelerate | [02_repositorios/rag-and-fine-tuning-demo/requirements.txt:9](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| declaration | datasets | [02_repositorios/rag-and-fine-tuning-demo/requirements.txt:10](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| declaration | trl | [02_repositorios/rag-and-fine-tuning-demo/requirements.txt:11](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| declaration | sentence-transformers | [02_repositorios/rag-and-fine-tuning-demo/requirements.txt:12](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| declaration | torch | [02_repositorios/rag-and-fine-tuning-demo/requirements.txt:13](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| declaration | torchvision | [02_repositorios/rag-and-fine-tuning-demo/requirements.txt:14](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| declaration | torchaudio | [02_repositorios/rag-and-fine-tuning-demo/requirements.txt:15](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| declaration | pandas | [02_repositorios/rag-and-fine-tuning-demo/requirements.txt:16](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| declaration | tqdm | [02_repositorios/rag-and-fine-tuning-demo/requirements.txt:17](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| declaration | gradio | [02_repositorios/rag-and-fine-tuning-demo/requirements.txt:18](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |

## Skills diretamente relacionadas

| Skill | Aplicação | Fonte |
| --- | --- | --- |
| [ai-architecture-expert](../../../00_skills/(architecture)/ai-architecture-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/rag-and-fine-tuning-demo/README.md:5](../../../02_repositorios/rag-and-fine-tuning-demo/README.md) |
| [ai-engineering-expert](../../../00_skills/(development)/ai-engineering-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/rag-and-fine-tuning-demo/README.md:5](../../../02_repositorios/rag-and-fine-tuning-demo/README.md) |
| [ai-evals-expert](../../../00_skills/(quality)/ai-evals-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/rag-and-fine-tuning-demo/README.md:5](../../../02_repositorios/rag-and-fine-tuning-demo/README.md) |
| [anti-hallucination-evaluator](../../../00_skills/(quality)/anti-hallucination-evaluator/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/rag-and-fine-tuning-demo/README.md:5](../../../02_repositorios/rag-and-fine-tuning-demo/README.md) |
| [bm25-expert](../../../00_skills/(development)/bm25-expert/SKILL.md) | Necessidade observada: rag. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/rag-and-fine-tuning-demo/README.md:5](../../../02_repositorios/rag-and-fine-tuning-demo/README.md) |
| [fine-tuning-expert](../../../00_skills/(development)/fine-tuning-expert/SKILL.md) | Necessidade observada: training. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/rag-and-fine-tuning-demo/README.md:5](../../../02_repositorios/rag-and-fine-tuning-demo/README.md) |
| [llm-model-selection-expert](../../../00_skills/(development)/llm-model-selection-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/rag-and-fine-tuning-demo/README.md:5](../../../02_repositorios/rag-and-fine-tuning-demo/README.md) |
| [lora-qlora-dora-expert](../../../00_skills/(development)/lora-qlora-dora-expert/SKILL.md) | Necessidade observada: training. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/rag-and-fine-tuning-demo/README.md:5](../../../02_repositorios/rag-and-fine-tuning-demo/README.md) |
| [python-bug-solver-skill](../../../00_skills/(development)/python-bug-solver-skill/SKILL.md) | Necessidade observada: python. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/rag-and-fine-tuning-demo/README.md:17](../../../02_repositorios/rag-and-fine-tuning-demo/README.md) |
| [python-expert](../../../00_skills/(development)/python-expert/SKILL.md) | Necessidade observada: python. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/rag-and-fine-tuning-demo/README.md:17](../../../02_repositorios/rag-and-fine-tuning-demo/README.md) |
| [python-rag-audit](../../../00_skills/(development)/python-rag-audit/SKILL.md) | Necessidade observada: rag. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/rag-and-fine-tuning-demo/README.md:5](../../../02_repositorios/rag-and-fine-tuning-demo/README.md) |
| [rag-expert](../../../00_skills/(development)/rag-expert/SKILL.md) | Necessidade observada: rag. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/rag-and-fine-tuning-demo/README.md:5](../../../02_repositorios/rag-and-fine-tuning-demo/README.md) |

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

- Wrapper híbrido é conceitual; integração fim a fim não validada.
- Correções de caminho são locais ao clone.
