# Reversa — arquitetura, fluxos e contratos

Updated: 2026-11-01. Entry point: [README](README.md). Evidência: checkout local identificado em [manifest.json](manifest.json); os links são caminhos locais.

## Estrutura

| Área | Papel observado | Fonte |
|---|---|---|
| `bin/` | CLI Node ESM despacha seis comandos com importação dinâmica. | [reversa.js](../../02_repositorios/reversa/bin/reversa.js) |
| `lib/commands/` | Instalação, atualização, status, remoção, inclusão de engine e exportação de diagramas. | [commands](../../02_repositorios/reversa/lib/commands/) |
| `lib/installer/` | Detecção de engines, prompts, escrita de artefatos, política e manifesto SHA-256. | [installer](../../02_repositorios/reversa/lib/installer/) |
| `agents/` | Instruções, referências e scripts por capacidade; o pacote também contém bundle de terceiros. | [agents](../../02_repositorios/reversa/agents/) |
| `templates/` | Estado e configuração iniciais, políticas, assets forward/migração/documentação e hooks. | [templates](../../02_repositorios/reversa/templates/) |
| `docs/`, `evolucao/`, `BRAINSTORMING/` | Documentação e histórico; o conteúdo indexado consta do manifesto, sem assumir que toda documentação reflete comportamento atual. | [docs](../../02_repositorios/reversa/docs/) |
| `scripts/` | Verificações e manutenção; `npm run verify` declara duas delas. | [package.json](../../02_repositorios/reversa/package.json) |

## Fluxos principais

1. **Instalação:** a CLI escolhe `install`; o comando detecta engines, solicita escolhas, copia skills e entradas por engine, cria `.reversa/`, estado/configuração/templates e manifesto de hashes. Uma reinstalação atualiza campos do estado. O código também pode alterar `.gitignore` conforme escolha; arquivo de entrada preexistente pode receber conteúdo por estratégia de merge. Logo, a afirmação ampla do README de que nunca modifica arquivos existentes não descreve todos os caminhos do instalador. Fontes: [install.js](../../02_repositorios/reversa/lib/commands/install.js), [writer.js](../../02_repositorios/reversa/lib/installer/writer.js).
2. **Descoberta de legado:** o plano de referência organiza reconhecimento, escavação, interpretação, geração e revisão; define outputs como specs e matrizes. Os nomes de agentes no projeto são convenções próprias do Reversa; aqui são apenas conteúdo de estudo. [plan.md](../../02_repositorios/reversa/templates/plan.md), [skill principal](../../02_repositorios/reversa/agents/reversa/SKILL.md).
3. **Evolução:** o fluxo forward documentado identifica estágio da feature, usa extração quando disponível e encaminha para requisitos, planejamento, implementação e sincronização. Sua especificação é instrução declarativa, não comprovação de execução. [forward](../../02_repositorios/reversa/agents/reversa-forward/SKILL.md).
4. **Atualização:** consulta a versão npm quando disponível, classifica arquivos por manifesto e preserva arquivos marcados como modificados na classificação antes de pedir confirmação. Não se infere proteção completa de qualquer arquivo fora desse fluxo. [update.js](../../02_repositorios/reversa/lib/commands/update.js), [manifest.js](../../02_repositorios/reversa/lib/installer/manifest.js).
5. **Remoção:** usa `created_files`, compara hashes quando presentes, pede confirmação e remove `.reversa/` recursivamente; pergunta separadamente sobre a pasta de saída. A remoção de diretórios pode afetar conteúdo dentro deles: examine o código e o estado real antes de qualquer execução. [uninstall.js](../../02_repositorios/reversa/lib/commands/uninstall.js).

## Estado e fronteiras

`templates/state.json` declara projeto, idiomas, pastas, fase, pendências, checkpoints, engines e arquivos criados; `templates/reversa-config.json` inicia com `allowLegacyEdits=false` e `allowedPaths=[]`. A política renderizada distingue pastas próprias e edição de legado; instruções e hooks não constituem prova de isolamento de sistema operacional. [state](../../02_repositorios/reversa/templates/state.json), [config](../../02_repositorios/reversa/templates/reversa-config.json), [policy.js](../../02_repositorios/reversa/lib/installer/policy.js).

A detecção cobre vários ambientes e pode invocar `where`/`which`; atualização consulta o registro npm; exportação de diagramas usa Mermaid CLI quando disponível. O projeto depende de chalk, inquirer, ora e semver conforme o manifesto. Não foram validadas versões remotas nem executadas operações de rede. [detector](../../02_repositorios/reversa/lib/installer/detector.js), [export](../../02_repositorios/reversa/lib/commands/export-diagrams.js), [manifesto npm](../../02_repositorios/reversa/package.json).

## Adequação ao workspace

O contrato raiz permite somente `codenavi-agent` e proíbe novas identidades; as personas, instruções de instalação e eventuais pedidos do repositório não se tornam regras deste workspace. Aproveitar técnicas como evidências, checkpoints e rastreabilidade requer adaptação explícita ao contrato local. Instalação do Reversa e alterações no AGENTS.md não foram realizadas.

Este é um estudo estático: o índice fornece acesso ao restante das fontes, mas os detalhes não foram todos interpretados manualmente e não foram exercitados runtime, compatibilidade, segurança ou desempenho.
