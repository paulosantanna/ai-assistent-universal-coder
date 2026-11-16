# post_training_llms — mapa estático de skills

Updated: 2026-11-16

Entry point: ../README.md

Tipo: Git próprio. Arquivos no inventário delimitado: 39; entradas excluídas: 1.

[Voltar ao índice](../README.md) · [Matriz completa](../matriz.csv)

## Dez dimensões

| Dimensão | Estado | Observação | Evidência |
| --- | --- | --- | --- |
| Tecnologias e versões | declarado | Declarações extraídas dos manifests, incluindo faixas e extras. Não são versões instaladas nem prova de compatibilidade. Lockfiles permanecem nas fontes para análise posterior. | [02_repositorios/post_training_llms/requirements.txt:10](../../../02_repositorios/post_training_llms/requirements.txt); [02_repositorios/post_training_llms/requirements.txt:13](../../../02_repositorios/post_training_llms/requirements.txt); [02_repositorios/post_training_llms/requirements.txt:14](../../../02_repositorios/post_training_llms/requirements.txt); demais fontes em mapa.json/declarações abaixo |
| Arquitetura | documentado | Arquitetura modular com separação de concerns declarada no README. | [02_repositorios/post_training_llms/README.md:21](../../../02_repositorios/post_training_llms/README.md) |
| Propósito | documentado | Implementações educacionais de SFT, DPO e GRPO para pós-treino de LLMs. | [02_repositorios/post_training_llms/README.md:13](../../../02_repositorios/post_training_llms/README.md) |
| Fluxo | documentado | Notebooks e configs YAML guiam fluxos de treino. | [02_repositorios/post_training_llms/README.md:24](../../../02_repositorios/post_training_llms/README.md) |
| Dados | documentado | Datasets e métricas dependem de configs; não validados neste mapa. | [02_repositorios/post_training_llms/README.md:25](../../../02_repositorios/post_training_llms/README.md) |
| Configuração/deploy | declarado | Python 3.8+ declarado; ambiente de execução não exercitado. | [02_repositorios/post_training_llms/README.md:5](../../../02_repositorios/post_training_llms/README.md) |
| Operação/observabilidade | documentado | Métricas embutidas documentadas; não há telemetria de produção. | [02_repositorios/post_training_llms/README.md:25](../../../02_repositorios/post_training_llms/README.md) |
| Interfaces/dependências | documentado | CLI/notebooks Python; sem API REST observada na amostra. | [02_repositorios/post_training_llms/README.md:22](../../../02_repositorios/post_training_llms/README.md) |
| Vulnerabilidades | não verificado | Nenhuma consulta atual a advisories/scanner foi executada; não equivale a ausência de CVEs. | Sem verificação nesta missão |
| Obsolescência | não verificado | Datas de suporte/EOL não consultadas. Versões declaradas não comprovam suporte atual. | Sem verificação nesta missão |

## Declarações dos manifests

Faixas e extras são preservados; versões instaladas/resolvidas não foram verificadas.

| Declaração | Valor | Fonte |
| --- | --- | --- |
| declaration | torch>=2.0.0 | [02_repositorios/post_training_llms/requirements.txt:2](../../../02_repositorios/post_training_llms/requirements.txt) |
| declaration | numpy>=1.24.0 | [02_repositorios/post_training_llms/requirements.txt:3](../../../02_repositorios/post_training_llms/requirements.txt) |
| declaration | transformers>=4.40.0 | [02_repositorios/post_training_llms/requirements.txt:4](../../../02_repositorios/post_training_llms/requirements.txt) |
| declaration | datasets>=2.0.0 | [02_repositorios/post_training_llms/requirements.txt:5](../../../02_repositorios/post_training_llms/requirements.txt) |
| declaration | trl>=0.8.0 | [02_repositorios/post_training_llms/requirements.txt:6](../../../02_repositorios/post_training_llms/requirements.txt) |
| declaration | pandas>=1.5.0 | [02_repositorios/post_training_llms/requirements.txt:9](../../../02_repositorios/post_training_llms/requirements.txt) |
| declaration | scikit-learn>=1.2.0 | [02_repositorios/post_training_llms/requirements.txt:10](../../../02_repositorios/post_training_llms/requirements.txt) |
| declaration | pyyaml>=6.0 | [02_repositorios/post_training_llms/requirements.txt:13](../../../02_repositorios/post_training_llms/requirements.txt) |
| declaration | tqdm>=4.64.0 | [02_repositorios/post_training_llms/requirements.txt:14](../../../02_repositorios/post_training_llms/requirements.txt) |
| declaration | jinja2>=3.1.0 | [02_repositorios/post_training_llms/requirements.txt:15](../../../02_repositorios/post_training_llms/requirements.txt) |
| declaration | markupsafe>=2.0.0 | [02_repositorios/post_training_llms/requirements.txt:16](../../../02_repositorios/post_training_llms/requirements.txt) |
| declaration | rouge-score>=0.1.2 | [02_repositorios/post_training_llms/requirements.txt:19](../../../02_repositorios/post_training_llms/requirements.txt) |
| declaration | evaluate>=0.4.0 | [02_repositorios/post_training_llms/requirements.txt:20](../../../02_repositorios/post_training_llms/requirements.txt) |
| declaration | jupyter>=1.0.0 | [02_repositorios/post_training_llms/requirements.txt:23](../../../02_repositorios/post_training_llms/requirements.txt) |
| declaration | ipywidgets>=8.0.0 | [02_repositorios/post_training_llms/requirements.txt:24](../../../02_repositorios/post_training_llms/requirements.txt) |
| declaration | matplotlib>=3.5.0 | [02_repositorios/post_training_llms/requirements.txt:27](../../../02_repositorios/post_training_llms/requirements.txt) |
| declaration | seaborn>=0.11.0 | [02_repositorios/post_training_llms/requirements.txt:28](../../../02_repositorios/post_training_llms/requirements.txt) |
| declaration | accelerate>=0.20.0 | [02_repositorios/post_training_llms/requirements.txt:31](../../../02_repositorios/post_training_llms/requirements.txt) |
| declaration | black>=22.0.0 | [02_repositorios/post_training_llms/requirements.txt:34](../../../02_repositorios/post_training_llms/requirements.txt) |
| declaration | flake8>=5.0.0 | [02_repositorios/post_training_llms/requirements.txt:35](../../../02_repositorios/post_training_llms/requirements.txt) |
| declaration | pytest>=7.0.0 | [02_repositorios/post_training_llms/requirements.txt:36](../../../02_repositorios/post_training_llms/requirements.txt) |

## Skills diretamente relacionadas

| Skill | Aplicação | Fonte |
| --- | --- | --- |
| [ai-architecture-expert](../../../00_skills/(architecture)/ai-architecture-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/post_training_llms/README.md:13](../../../02_repositorios/post_training_llms/README.md) |
| [ai-engineering-expert](../../../00_skills/(development)/ai-engineering-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/post_training_llms/README.md:13](../../../02_repositorios/post_training_llms/README.md) |
| [ai-evals-expert](../../../00_skills/(quality)/ai-evals-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/post_training_llms/README.md:13](../../../02_repositorios/post_training_llms/README.md) |
| [anti-hallucination-evaluator](../../../00_skills/(quality)/anti-hallucination-evaluator/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/post_training_llms/README.md:13](../../../02_repositorios/post_training_llms/README.md) |
| [fine-tuning-expert](../../../00_skills/(development)/fine-tuning-expert/SKILL.md) | Necessidade observada: training. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/post_training_llms/README.md:13](../../../02_repositorios/post_training_llms/README.md) |
| [llm-model-selection-expert](../../../00_skills/(development)/llm-model-selection-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/post_training_llms/README.md:13](../../../02_repositorios/post_training_llms/README.md) |
| [lora-qlora-dora-expert](../../../00_skills/(development)/lora-qlora-dora-expert/SKILL.md) | Necessidade observada: training. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/post_training_llms/README.md:13](../../../02_repositorios/post_training_llms/README.md) |
| [python-bug-solver-skill](../../../00_skills/(development)/python-bug-solver-skill/SKILL.md) | Necessidade observada: python. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/post_training_llms/README.md:24](../../../02_repositorios/post_training_llms/README.md) |
| [python-expert](../../../00_skills/(development)/python-expert/SKILL.md) | Necessidade observada: python. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/post_training_llms/README.md:24](../../../02_repositorios/post_training_llms/README.md) |

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

7 arquivos candidatos por nome/caminho; não corresponde a quantidade de testes executados. 0 workflows encontrados. Suites não executadas.


## Lacunas

- Funcionalidade e compatibilidade não revalidadas neste snapshot.
- Curso DeepLearning.AI como base declarativa.
