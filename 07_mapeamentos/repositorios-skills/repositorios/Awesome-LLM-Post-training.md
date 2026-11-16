# Awesome-LLM-Post-training — mapa estático de skills

Updated: 2026-11-16

Entry point: ../README.md

Tipo: Git próprio. Arquivos no inventário delimitado: 11; entradas excluídas: 2.

[Voltar ao índice](../README.md) · [Matriz completa](../matriz.csv)

## Dez dimensões

| Dimensão | Estado | Observação | Evidência |
| --- | --- | --- | --- |
| Tecnologias e versões | declarado | Declarações extraídas dos manifests, incluindo faixas e extras. Não são versões instaladas nem prova de compatibilidade. Lockfiles permanecem nas fontes para análise posterior. | Sem verificação nesta missão |
| Arquitetura | documentado | Organização por taxonomia e links externos; não é implementação local dos trabalhos listados. | [02_repositorios/Awesome-LLM-Post-training/README.md:11](../../../02_repositorios/Awesome-LLM-Post-training/README.md) |
| Propósito | declarado | Curadoria bibliográfica de pós-treino, raciocínio e avaliação de LLMs. | [02_repositorios/Awesome-LLM-Post-training/README.md:11](../../../02_repositorios/Awesome-LLM-Post-training/README.md) |
| Fluxo | documentado | Entrada pelo README e seções; papers citados exigem inspeção própria. | [02_repositorios/Awesome-LLM-Post-training/README.md:1](../../../02_repositorios/Awesome-LLM-Post-training/README.md) |
| Dados | documentado | Conteúdo é lista de referências; não há corpus de treino local. | [02_repositorios/Awesome-LLM-Post-training/README.md:11](../../../02_repositorios/Awesome-LLM-Post-training/README.md) |
| Configuração/deploy | documentado | Repositório de links e documentação; sem pipeline de deploy inferido. | [02_repositorios/Awesome-LLM-Post-training/README.md:4](../../../02_repositorios/Awesome-LLM-Post-training/README.md) |
| Operação/observabilidade | documentado | Manutenção declarada no README; disponibilidade de links externos não verificada. | [02_repositorios/Awesome-LLM-Post-training/README.md:4](../../../02_repositorios/Awesome-LLM-Post-training/README.md) |
| Interfaces/dependências | documentado | Interface é Markdown e URLs; não há API local nesta amostra. | [02_repositorios/Awesome-LLM-Post-training/README.md:11](../../../02_repositorios/Awesome-LLM-Post-training/README.md) |
| Vulnerabilidades | não verificado | Nenhuma consulta atual a advisories/scanner foi executada; não equivale a ausência de CVEs. | Sem verificação nesta missão |
| Obsolescência | não verificado | Datas de suporte/EOL não consultadas. Versões declaradas não comprovam suporte atual. | Sem verificação nesta missão |

## Declarações dos manifests

Faixas e extras são preservados; versões instaladas/resolvidas não foram verificadas.

| Declaração | Valor | Fonte |
| --- | --- | --- |

## Skills diretamente relacionadas

| Skill | Aplicação | Fonte |
| --- | --- | --- |
| [ai-architecture-expert](../../../00_skills/(architecture)/ai-architecture-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/Awesome-LLM-Post-training/README.md:11](../../../02_repositorios/Awesome-LLM-Post-training/README.md) |
| [ai-engineering-expert](../../../00_skills/(development)/ai-engineering-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/Awesome-LLM-Post-training/README.md:11](../../../02_repositorios/Awesome-LLM-Post-training/README.md) |
| [ai-evals-expert](../../../00_skills/(quality)/ai-evals-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/Awesome-LLM-Post-training/README.md:11](../../../02_repositorios/Awesome-LLM-Post-training/README.md) |
| [anti-hallucination-evaluator](../../../00_skills/(quality)/anti-hallucination-evaluator/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/Awesome-LLM-Post-training/README.md:11](../../../02_repositorios/Awesome-LLM-Post-training/README.md) |
| [fine-tuning-expert](../../../00_skills/(development)/fine-tuning-expert/SKILL.md) | Necessidade observada: training. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/Awesome-LLM-Post-training/README.md:11](../../../02_repositorios/Awesome-LLM-Post-training/README.md) |
| [llm-model-selection-expert](../../../00_skills/(development)/llm-model-selection-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/Awesome-LLM-Post-training/README.md:11](../../../02_repositorios/Awesome-LLM-Post-training/README.md) |
| [lora-qlora-dora-expert](../../../00_skills/(development)/lora-qlora-dora-expert/SKILL.md) | Necessidade observada: training. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/Awesome-LLM-Post-training/README.md:11](../../../02_repositorios/Awesome-LLM-Post-training/README.md) |

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

- Nenhum trainer local inferido dos links.
- CVE/EOL dos projetos citados não verificados.
