# RemoveWindowsAI — mapa estático de skills

Updated: 2026-10-13

Entry point: ../README.md

Tipo: Git próprio. Arquivos no inventário delimitado: 131; entradas excluídas: 1.

[Voltar ao índice](../README.md) · [Matriz completa](../matriz.csv)

## Dez dimensões

| Dimensão | Estado | Observação | Evidência |
| --- | --- | --- | --- |
| Tecnologias e versões | declarado | Declarações extraídas dos manifests, incluindo faixas e extras. Não são versões instaladas nem prova de compatibilidade. Lockfiles permanecem nas fontes para análise posterior. | Sem verificação nesta missão |
| Arquitetura | documentado | Dois scripts PowerShell e payloads Windows; documentação descreve execução via TrustedInstaller. | [02_repositorios/RemoveWindowsAI/Documentation.md:23](../../../02_repositorios/RemoveWindowsAI/Documentation.md) |
| Propósito | declarado | Utilitário para desativar/remover recursos de IA do Windows e ajustar políticas/pacotes. | [02_repositorios/RemoveWindowsAI/README.md:1](../../../02_repositorios/RemoveWindowsAI/README.md) |
| Fluxo | observado | Script verifica versão PowerShell e oferece opções de alteração do sistema; cleanup usa execução elevada. | [02_repositorios/RemoveWindowsAI/RemoveWindowsAi.ps1:51](../../../02_repositorios/RemoveWindowsAI/RemoveWindowsAi.ps1) |
| Dados | documentado | Registro Windows, pacotes Appx e backups são o estado manipulado; não é corpus de IA. | [02_repositorios/RemoveWindowsAI/Documentation.md:51](../../../02_repositorios/RemoveWindowsAI/Documentation.md) |
| Configuração/deploy | observado | Script exige Windows PowerShell 5.1; pacote de aplicação e binários acompanham o diretório. | [02_repositorios/RemoveWindowsAI/RemoveWindowsAi.ps1:51](../../../02_repositorios/RemoveWindowsAI/RemoveWindowsAi.ps1) |
| Operação/observabilidade | observado | Cleanup escreve status de falhas de parada do TrustedInstaller; não executado. | [02_repositorios/RemoveWindowsAI/RemoveAI-UpdateCleanup.ps1:147](../../../02_repositorios/RemoveWindowsAI/RemoveAI-UpdateCleanup.ps1) |
| Interfaces/dependências | observado | Usa privilégios de backup/restore e processo TrustedInstaller; alterações têm impacto elevado no SO. | [02_repositorios/RemoveWindowsAI/RemoveAI-UpdateCleanup.ps1:65](../../../02_repositorios/RemoveWindowsAI/RemoveAI-UpdateCleanup.ps1) |
| Vulnerabilidades | não verificado | Nenhuma consulta atual a advisories/scanner foi executada; não equivale a ausência de CVEs. | Sem verificação nesta missão |
| Obsolescência | não verificado | Datas de suporte/EOL não consultadas. Versões declaradas não comprovam suporte atual. | Sem verificação nesta missão |

## Declarações dos manifests

Faixas e extras são preservados; versões instaladas/resolvidas não foram verificadas.

| Declaração | Valor | Fonte |
| --- | --- | --- |

## Skills diretamente relacionadas

| Skill | Aplicação | Fonte |
| --- | --- | --- |
| [diff-reviewer](../../../00_skills/(quality)/diff-reviewer/SKILL.md) | Necessidade observada: destructive-windows. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/RemoveWindowsAI/RemoveWindowsAi.ps1:51](../../../02_repositorios/RemoveWindowsAI/RemoveWindowsAi.ps1) |
| [patch-planner](../../../00_skills/(development)/patch-planner/SKILL.md) | Necessidade observada: destructive-windows. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/RemoveWindowsAI/RemoveWindowsAi.ps1:51](../../../02_repositorios/RemoveWindowsAI/RemoveWindowsAi.ps1) |
| [risk-classifier](../../../00_skills/(security)/risk-classifier/SKILL.md) | Necessidade observada: destructive-windows. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/RemoveWindowsAI/RemoveWindowsAi.ps1:51](../../../02_repositorios/RemoveWindowsAI/RemoveWindowsAi.ps1) |
| [rollback-planner](../../../00_skills/(cloud)/rollback-planner/SKILL.md) | Necessidade observada: destructive-windows. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/RemoveWindowsAI/RemoveWindowsAi.ps1:51](../../../02_repositorios/RemoveWindowsAI/RemoveWindowsAi.ps1) |
| [security-audit](../../../00_skills/(security)/security-audit/SKILL.md) | Necessidade observada: destructive-windows. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/RemoveWindowsAI/RemoveWindowsAi.ps1:51](../../../02_repositorios/RemoveWindowsAI/RemoveWindowsAi.ps1) |

## Uso condicionado

- **atualizar-dependencias**: Somente em missão de atualização com baseline e compatibilidade.
- **compatibility-analyzer**: Ao verificar troca de linguagem/runtime/dependência.
- **dependency-updater**: Somente em atualização autorizada, preservando lockfiles.
- **github-operations**: Ao operar GitHub com alvo, credenciais e autorização próprios.
- **local-secret-vault**: Só se a tarefa depender de credenciais autorizadas; não abrir para mapear.
- **observability-root-cause-integrator**: Requer incidente/sintomas e telemetria atual.
- **pr-reviewer**: Requer PR/diff concreto.
- **pr-reviewer-advanced**: Requer PR/diff concreto e evidências de revisão.
- **release-readiness-judge**: Requer release concreta e checks determinísticos.
- **gh-address-comments**: Requer comentários de PR e alvo concreto.
- **cve-advisory-sync**: Só ao solicitar consulta atual de advisories oficiais.
- **cve-remediation**: Requer CVE/GHSA concreto, versão afetada e correção autorizada.
- **eol-advisory-sync**: Requer consulta atual de suporte oficial para os produtos declarados.
- **revisar-seguranca-pr**: Requer diff de PR e escopo de segurança.
- **vuln-obsol-recon**: Inventário estático é ponto de partida; auditoria de CVE/EOL não foi executada.
- **runtime-troubleshooting**: Requer runtime/logs atuais; o mapa é estático.

## Testes/CI

0 arquivos candidatos por nome/caminho; não corresponde a quantidade de testes executados. 0 workflows encontrados. Suites não executadas.


## Lacunas

- Não há especialista PowerShell/Windows no catálogo.
- Sem testes/CI executáveis identificados no inventário; binários não foram inspecionados.
- Estado de suporte do Windows e efeito das alterações não verificados.
