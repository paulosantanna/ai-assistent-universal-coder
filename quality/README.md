# Esteira TLC de capacidades

Updated: 2026-10-14
Entry point: [workflow de qualidade](../.github/workflows/aeos-enterprise-ci.template.yml), [manutenção diária](../.github/workflows/tlc-upstream-maintenance.yml).

Este pacote herda `AGENTS.md`, CodENavi Full Workspace v2 e o ciclo BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF. Não cria outra identidade nem restaura o runtime removido.

```powershell
python -m pip install --require-hashes -r quality/requirements.txt
python -m unittest discover -s quality/tests -v
python quality/validate.py --runtime
python quality/upstream.py
```

O parser YAML6.0.3 usa hashes oficiais do PyPI, sem dependências transitivas. O comando de unittest testa os gates com entradas válidas e mutações inválidas. validate grava `.aeos/quality/report.json` e `summary.md`: catálogo, hashes, modularidade, distribuição, revisões de skills novas/alteradas, código Python/JavaScript e contratos de servidores. upstream consulta o TLC oficial e registra o commit observado e novidades; erro de rede ou padrão desconhecido é falha, nunca “atualizado”. Nenhum comando imprime valores de credenciais.

## Regras e cobertura

- Guia e validadores oficiais TLC observados no commit fixado em `tlc-upstream.json`; a implementação Python do skill-architect foi comparada com a fonte atual. O limite local de100 linhas físicas é mais estrito que as500 linhas sugeridas pelo TLC.
- Entradas canônicas seguem `00_skills/(categoria)/slug/SKILL.md`; descrição com resultado, gatilhos e exclusões, licença/autor/versão/dono, procedimento e erros. Links operativos são conferidos recursivamente. Snapshots TLC mantêm origem e recursos completos.
- Catálogo, categorias, aliases, `.agents/skills` e `skills.registry.yaml` devem concordar. Uma skill publicada fora do catálogo, descoberta ausente ou categoria incorreta falha.
- `skills-baseline.json` é o baseline estrutural dos pacotes anteriores. Mudança no conteúdo completo de um pacote ou uma skill nova exige `reviews/<id>.json` com hash,3 gatilhos concretos e3 limites. Avaliação estática de wording não é acurácia de roteamento nem avaliação funcional em produção.
- Hash de texto usa UTF-8 com LF; binários são exatos. `acquired_sha256` preserva hashes históricos de cópias CRLF. `.gitattributes` torna futuros checkouts consistentes.
- Varredura bloqueia arquivos de credenciais e padrões conhecidos de tokens/chaves. Não é uma auditoria de segurança completa nem substitui avaliação de prompt injection por provedor especializado.

## MCPs e LSPs

`capabilities.json` declara a superfície local real. Servidor ativo deve declarar entrada, comando em array, protocolo, dono, política de segredos e schemas; nova implementação/configuração sem registro falha. O probe roda sem credenciais herdadas e só negocia protocolo, lista tools, faz ping ou encerra a sessão LSP. Não executa ações remotas.

MCP ativo usa JSON-RPC em stdio com mensagens JSON por linha, negociação2025-11-25, `serverInfo`, capability `tools`, nomes únicos e esquemas de entrada com estrutura válida. O gate checa o subconjunto declarado de JSON Schema; não afirma validar vocabulários arbitrários. LSP usa framing Content-Length, initialize/initialized/shutdown/exit e declaração de linguagens/extensões.

O inventário inicial possui um adaptador KingHost com self-test offline aprovado e três pacotes em quarentena: protocolo antigo/ambiente incompleto ou dependências/source ausentes. Eles são reportados como ADAPTER/QUARANTINED, **não como MCP conformes**. Alterar seus bytes invalida o baseline e exige resolver seu contrato. Não há servidor LSP local instalado; extensões do editor não são prova de disponibilidade. Adições só podem entrar como ativas, com contrato e probe válidos.

Fontes: [MCP tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools), [LSP3.17](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/).

## Atualização automática autorizada

Todos os dias às09:23UTC (06:23São Paulo), ou por workflow_dispatch:

1. Um job somente leitura consulta `tech-leads-club/agent-skills/main`; obtém um commit imutável e confere hashes dos controles TLC. Não executa código baixado.
2. Novas skills sem colisão são preparadas em checkout temporário, com hashes de conteúdo conferidos contra o registry oficial, atribuição, recursos intactos, entrada local curta, descoberta/catálogo/registro e avaliação estática. Não instala dependências, modelos ou imagens Docker.
3. O candidato passa por todos os gates. Qualquer falha impede alterações/publicação; a preparação é transacional e idempotente.
4. Um artefato de diff/manifesto segue para job separado com escrita. O publicador permite metadados, pacotes novos e atualizações de pacotes previamente incorporados pelo próprio bot, com hash local ainda intacto. Não aceita trocar validadores, workflows, policy ou adaptações curadas. Confere base SHA, hash exato do patch e hashes dos pacotes mantidos, aplica e faz push normal na master; proteção da branch permanece soberana.

Mudança de padrão não reconhecida bloqueia o lote até adaptação validada dos gates. Adaptações de skills já existentes são preservadas; diferenças upstream são relatadas para revisão específica. “Mais recente” significa a última consulta bem-sucedida, não uma garantia de monitoramento instantâneo. Agendamento GitHub pode sofrer atraso. Pushes feitos com GITHUB_TOKEN não disparam outro workflow por push; o candidato já passou pelos gates no job anterior.

Saídas: relatórios por commit em artifacts, diff e manifesto da atualização. Riscos: indisponibilidade do GitHub, regra upstream nova, colisão e proteção podem bloquear a atualização. Compensação de alteração publicada: novo commit de revert autorizado, sem force-push.

Use `python quality/upstream.py --apply` apenas em checkout revisado; o fluxo automatizado usa workspace isolado. Para validar sem rede, `--source PATH` aceita uma cópia oficial já inspecionada e fixa seu HEAD.

## Qualidade empresarial

Os gates comprovam estrutura, integridade e contratos. A nota de eficácia em tarefas empresariais depende de execução real com fixtures, avaliação de resultados e evidência por domínio. Não há score inventado para as305 skills. Toda revisão registra esse limite; os requisitos de performance, utilidade e segurança em produção continuam sob suas skills de domínio.
