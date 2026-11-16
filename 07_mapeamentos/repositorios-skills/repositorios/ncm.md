# ncm — mapa estático de skills

Updated: 2026-11-16

Entry point: ../README.md

Tipo: Git próprio. Arquivos no inventário delimitado: 28; entradas excluídas: 3.

[Voltar ao índice](../README.md) · [Matriz completa](../matriz.csv)

## Dez dimensões

| Dimensão | Estado | Observação | Evidência |
| --- | --- | --- | --- |
| Tecnologias e versões | declarado | Declarações extraídas dos manifests, incluindo faixas e extras. Não são versões instaladas nem prova de compatibilidade. Lockfiles permanecem nas fontes para análise posterior. | [02_repositorios/ncm/requirements.txt:1](../../../02_repositorios/ncm/requirements.txt); [02_repositorios/ncm/requirements.txt:2](../../../02_repositorios/ncm/requirements.txt); [02_repositorios/ncm/requirements.txt:3](../../../02_repositorios/ncm/requirements.txt); demais fontes em mapa.json/declarações abaixo |
| Arquitetura | código presente | Tokenizer VQ-VAE e gerador NextConceptTransformer são módulos distintos. | [02_repositorios/ncm/models/next_concept.py:65](../../../02_repositorios/ncm/models/next_concept.py) |
| Propósito | documentado | Geração coarse-to-fine por conceitos multiescala (Next-Concept Modeling). | [02_repositorios/ncm/README.md:1](../../../02_repositorios/ncm/README.md) |
| Fluxo | código presente | Entrypoint evaluate coordena geração e medição por config. | [02_repositorios/ncm/evaluate.py:10](../../../02_repositorios/ncm/evaluate.py) |
| Dados | código presente | Quantização residual multiescala em models/quant.py. | [02_repositorios/ncm/models/quant.py:228](../../../02_repositorios/ncm/models/quant.py) |
| Configuração/deploy | documentado | Avaliação usa checkpoints e configs YAML; treino completo não demonstrado. | [02_repositorios/ncm/evaluate.py:12](../../../02_repositorios/ncm/evaluate.py) |
| Operação/observabilidade | documentado | CLI de avaliação por shard GPU; operação não exercitada neste mapa. | [02_repositorios/ncm/evaluate.py:15](../../../02_repositorios/ncm/evaluate.py) |
| Interfaces/dependências | documentado | API é scripts Python e configs; sem servidor HTTP inferido nesta amostra. | [02_repositorios/ncm/evaluate.py:11](../../../02_repositorios/ncm/evaluate.py) |
| Vulnerabilidades | não verificado | Nenhuma consulta atual a advisories/scanner foi executada; não equivale a ausência de CVEs. | Sem verificação nesta missão |
| Obsolescência | não verificado | Datas de suporte/EOL não consultadas. Versões declaradas não comprovam suporte atual. | Sem verificação nesta missão |

## Declarações dos manifests

Faixas e extras são preservados; versões instaladas/resolvidas não foram verificadas.

| Declaração | Valor | Fonte |
| --- | --- | --- |
| declaration | torch | [02_repositorios/ncm/requirements.txt:1](../../../02_repositorios/ncm/requirements.txt) |
| declaration | numpy | [02_repositorios/ncm/requirements.txt:2](../../../02_repositorios/ncm/requirements.txt) |
| declaration | omegaconf | [02_repositorios/ncm/requirements.txt:3](../../../02_repositorios/ncm/requirements.txt) |
| declaration | hydra-core | [02_repositorios/ncm/requirements.txt:4](../../../02_repositorios/ncm/requirements.txt) |
| declaration | transformers>=4.51 | [02_repositorios/ncm/requirements.txt:5](../../../02_repositorios/ncm/requirements.txt) |
| declaration | huggingface_hub[cli] | [02_repositorios/ncm/requirements.txt:6](../../../02_repositorios/ncm/requirements.txt) |
| declaration | regex | [02_repositorios/ncm/requirements.txt:7](../../../02_repositorios/ncm/requirements.txt) |
| declaration | rouge_score | [02_repositorios/ncm/requirements.txt:8](../../../02_repositorios/ncm/requirements.txt) |
| declaration | sacrebleu | [02_repositorios/ncm/requirements.txt:9](../../../02_repositorios/ncm/requirements.txt) |

## Skills diretamente relacionadas

| Skill | Aplicação | Fonte |
| --- | --- | --- |
| [ai-architecture-expert](../../../00_skills/(architecture)/ai-architecture-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/ncm/README.md:1](../../../02_repositorios/ncm/README.md) |
| [ai-engineering-expert](../../../00_skills/(development)/ai-engineering-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/ncm/README.md:1](../../../02_repositorios/ncm/README.md) |
| [ai-evals-expert](../../../00_skills/(quality)/ai-evals-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/ncm/README.md:1](../../../02_repositorios/ncm/README.md) |
| [anti-hallucination-evaluator](../../../00_skills/(quality)/anti-hallucination-evaluator/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/ncm/README.md:1](../../../02_repositorios/ncm/README.md) |
| [fine-tuning-expert](../../../00_skills/(development)/fine-tuning-expert/SKILL.md) | Necessidade observada: training. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/ncm/README.md:1](../../../02_repositorios/ncm/README.md) |
| [llm-model-selection-expert](../../../00_skills/(development)/llm-model-selection-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/ncm/README.md:1](../../../02_repositorios/ncm/README.md) |
| [lora-qlora-dora-expert](../../../00_skills/(development)/lora-qlora-dora-expert/SKILL.md) | Necessidade observada: training. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/ncm/README.md:1](../../../02_repositorios/ncm/README.md) |
| [python-bug-solver-skill](../../../00_skills/(development)/python-bug-solver-skill/SKILL.md) | Necessidade observada: python. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/ncm/evaluate.py:10](../../../02_repositorios/ncm/evaluate.py) |
| [python-expert](../../../00_skills/(development)/python-expert/SKILL.md) | Necessidade observada: python. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/ncm/evaluate.py:10](../../../02_repositorios/ncm/evaluate.py) |

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

- Treino completo não demonstrado localmente.
- Paradigma NCM não é LLM autoregressivo clássico.
