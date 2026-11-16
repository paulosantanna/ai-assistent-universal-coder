# reversa

Updated: 2026-11-01
Entry point: [diretório](../../../02_repositorios/reversa/).

- Arquivos inventariados: 520; exclusões: 32; erros: 0.
- Git HEAD: `0d4e01d9f28926ae1379cfc68f4588ce8e1026b0`; estado: limpo. Fingerprint: `63ba8a567404e53b2d7f94073bed95e212382edf03f795b066edaab2e28fbec2`.
- Diretórios por quantidade de arquivos: agents (319), docs (128), templates (34), lib (16), evolucao (9), scripts (4), .github (3), BRAINSTORMING (2), bin (1)
- Manifests e lockfiles: `package-lock.json`, `package.json`
- Candidatos a teste: 0; workflows: 3. Presença não prova execução.
- Sinais textuais por quantidade de arquivos: serving: 7

## Arquitetura e fluxo

O README descreve uma ferramenta para transformar software legado em especificações. O package.json declara versão 1.3.6, Node >=18.20.2 e CLI `bin/reversa.js`. A CLI despacha para módulos em `lib/commands`: install, update, status, uninstall, add-engine e export-diagrams. O README descreve instalação de instruções e criação de estruturas no projeto analisado; isso deve ser reconciliado com a regra de agente único deste workspace antes de qualquer uso.

Dependências declaradas: chalk, inquirer, ora e semver. O script verify declara verificações Python e Node; sua presença não comprova aprovação. Não foram executados instalador, testes nem código do projeto.

[README](../../../02_repositorios/reversa/README.md) · [manifest](../../../02_repositorios/reversa/package.json) · [CLI](../../../02_repositorios/reversa/bin/reversa.js).

Detalhes de arquivos, hashes, exclusões, indicadores e erros: [inventory.json](../inventory.json).
