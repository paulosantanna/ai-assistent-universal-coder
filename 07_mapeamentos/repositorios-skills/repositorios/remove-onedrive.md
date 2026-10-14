# remove-onedrive — mapa estático de skills

Updated: 2026-10-13

Entry point: ../README.md

Tipo: Git próprio. Arquivos no inventário delimitado: 4; entradas excluídas: 2.

[Voltar ao índice](../README.md) · [Matriz completa](../matriz.csv)

## Dez dimensões

| Dimensão | Estado | Observação | Evidência |
| --- | --- | --- | --- |
| Tecnologias e versões | declarado | Declarações extraídas dos manifests, incluindo faixas e extras. Não são versões instaladas nem prova de compatibilidade. Lockfiles permanecem nas fontes para análise posterior. | Sem verificação nesta missão |
| Arquitetura | observado | Script PowerShell monolítico com funções de log, elevação, backup e restauração; não é servidor. | [02_repositorios/remove-onedrive/Remove-OneDrive.ps1:129](../../../02_repositorios/remove-onedrive/Remove-OneDrive.ps1) |
| Propósito | declarado | Utilitário para remover OneDrive e restaurar controle local de pastas no Windows. | [02_repositorios/remove-onedrive/README.md:1](../../../02_repositorios/remove-onedrive/README.md) |
| Fluxo | observado | Localiza pastas e oferece backup antes da remoção; nenhuma operação de remoção foi executada. | [02_repositorios/remove-onedrive/Remove-OneDrive.ps1:179](../../../02_repositorios/remove-onedrive/Remove-OneDrive.ps1) |
| Dados | observado | Arquivos/pastas do perfil e backups são dados operacionais; risco de dados deve ser avaliado antes de executar. | [02_repositorios/remove-onedrive/Remove-OneDrive.ps1:159](../../../02_repositorios/remove-onedrive/Remove-OneDrive.ps1) |
| Configuração/deploy | documentado | Execução Windows com elevação programática documentada no script. | [02_repositorios/remove-onedrive/Remove-OneDrive.ps1:69](../../../02_repositorios/remove-onedrive/Remove-OneDrive.ps1) |
| Operação/observabilidade | observado | Write-Log usa arquivo e há ErrorActionPreference=Continue; continuar após erro exige revisão específica. | [02_repositorios/remove-onedrive/Remove-OneDrive.ps1:75](../../../02_repositorios/remove-onedrive/Remove-OneDrive.ps1) |
| Interfaces/dependências | documentado | Interage com sistema operacional e OneDrive; não foi identificado contrato HTTP/DB no escopo lido. | [02_repositorios/remove-onedrive/Remove-OneDrive.ps1:7](../../../02_repositorios/remove-onedrive/Remove-OneDrive.ps1) |
| Vulnerabilidades | não verificado | Nenhuma consulta atual a advisories/scanner foi executada; não equivale a ausência de CVEs. | Sem verificação nesta missão |
| Obsolescência | não verificado | Datas de suporte/EOL não consultadas. Versões declaradas não comprovam suporte atual. | Sem verificação nesta missão |

## Declarações dos manifests

Faixas e extras são preservados; versões instaladas/resolvidas não foram verificadas.

| Declaração | Valor | Fonte |
| --- | --- | --- |

## Skills diretamente relacionadas

| Skill | Aplicação | Fonte |
| --- | --- | --- |
| [diff-reviewer](../../../00_skills/(quality)/diff-reviewer/SKILL.md) | Necessidade observada: destructive-windows. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/remove-onedrive/Remove-OneDrive.ps1:179](../../../02_repositorios/remove-onedrive/Remove-OneDrive.ps1) |
| [patch-planner](../../../00_skills/(development)/patch-planner/SKILL.md) | Necessidade observada: destructive-windows. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/remove-onedrive/Remove-OneDrive.ps1:179](../../../02_repositorios/remove-onedrive/Remove-OneDrive.ps1) |
| [risk-classifier](../../../00_skills/(security)/risk-classifier/SKILL.md) | Necessidade observada: destructive-windows. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/remove-onedrive/Remove-OneDrive.ps1:179](../../../02_repositorios/remove-onedrive/Remove-OneDrive.ps1) |
| [rollback-planner](../../../00_skills/(cloud)/rollback-planner/SKILL.md) | Necessidade observada: destructive-windows. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/remove-onedrive/Remove-OneDrive.ps1:179](../../../02_repositorios/remove-onedrive/Remove-OneDrive.ps1) |
| [security-audit](../../../00_skills/(security)/security-audit/SKILL.md) | Necessidade observada: destructive-windows. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/remove-onedrive/Remove-OneDrive.ps1:179](../../../02_repositorios/remove-onedrive/Remove-OneDrive.ps1) |

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
- Sem testes automatizados ou CI identificados no inventário; docs/verification.md é relato histórico.
- Backup incompleto e arquivos somente em nuvem exigem análise antes de uso.
