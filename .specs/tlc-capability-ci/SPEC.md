# Esteira de qualidade de capacidades

Updated: 2026-10-14
Entry point: .github/workflows/, quality/

## Objetivo e escopo

Substituir a esteira dependente de runtime removido por gates reais do checkout atual: catálogo/contratos TLC, modularidade/distribuição, MCP e LSP, segurança estrutural e testes dos validadores. Acompanhar diariamente a fonte oficial tech-leads-club/agent-skills, detectar mudanças do padrão e novas skills, produzir propostas rastreáveis. Preservar AGENTS.md e a identidade codenavi-agent.

## Decisões

- Reusar o validador local de skill-factory e skill-architect, acrescentando cobertura de novas capacidades e inventário declarado.
- O limite local de100 linhas físicas permanece mais estrito que o guia TLC de500. Fonte atual e hashes fixados; monitor consulta origem oficial, nunca executa código recém-baixado sem revisão.
- Diferenciar conformidade estática, descoberta, teste do protocolo e disponibilidade de execução externa. Sem inferir um servidor LSP instalado a partir de instruções; ausência atual declarada, novo servidor sem contrato deve falhar.
- Qualidade empresarial é medida por contratos, limites, manutenção, distribuição, segurança e verificação reproduzíveis; isso não prova a eficácia de toda skill em produção.
- Usuário escolheu incorporação automática após validação. Monitor diário prepara apenas capacidades novas e metadados de acompanhamento; validação ocorre em runner sem permissão de escrita, publicação em job separado por push normal na master. Mudança de regra upstream desconhecida bloqueia publicação até adaptação comprovada. Não instalar dependências/modelos nem substituir adaptações existentes silenciosamente.

## Gates de aceitação

- [x] Baseline estabelecido; CI real a3f11175 falha em setup-node/cache, e checkout Git exportado apresenta441 erros de hash contra PASS Windows. Normalização textual/proveniência corrigida, binários intactos.
- [x] Workflows push/PR/manual implementados; gates locais e checkout exportado aprovados; evidência JSON/Markdown/artifacts por commit.
- [x] MCPs inventariados com estados reais:1adaptador self-test offline,3quarentenas explícitas. Contrato/protocolo ativo testado com servidor controlado; não alegar conformidade dos legados.
- [x] LSPs:0instalados; contratos ativos e handshakes controlados aprovados, linguagem inválida/configuração sem registro rejeitadas.
- [x] Monitor consulta fonte oficial atual, importa novas e atualiza auto-imports intactos; observou mudança real de tlc-prd para7f93bf3b e validou10 arquivos antes de aplicar. No-op e falha de candidato não alteram checkout. Regra desconhecida bloqueia lote.
- [x]41 testes adversariais/protocolo e publicação em remoto Git isolado; catálogo305/832 entradas/2874links/sintaxe83Python/142JS passam no checkout exato Git.
- [x] CI inicial ad7a0d0a e manutenção manual terminais success (runs38650490307/38650523248), sem contornar proteção ou enfraquecer gates. Correção final de3 modos executáveis exige nova evidência latestSHA.

## Riscos e compensação

Novos padrões podem exigir revisão humana de regras; upstream é conteúdo externo não confiável. Testes não usam credenciais ou projetos vizinhos. Falha de rede bloqueia o monitor. Mudanças publicadas podem ser revertidas em novo commit, sem reescrever histórico. Não configurar proteção da branch silenciosamente.
