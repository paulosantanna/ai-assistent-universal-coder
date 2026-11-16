# Engenharia-Reversa — beta 3.0.0

Updated: 2026-10-27
Entry point: [índice](../README.md) · [mapa estruturado](../mapa.json)

Arquivos com hash: 6237; fingerprint: `fbfda656a9bd70536f7da3d17ec5bf470619eb2ec9c39b7f00cdb86537c0af8f`.
Git próprio: True; HEAD: `f89b03e738fe94f2bea6927c84e05871293707ea`; branch: `main`.
Estado local: há alterações/não rastreados; detalhes em inventory.json.

## Atualizações e reconciliação

Manifest atual rea-agents 6.8.0; composição MCP em eagerRuntime/transporte. Documentação local não rastreada separada do estado commitado.

## Dimensões e evidências

### Propósito

**declarado** — REA fornece CLI e servidor MCP para investigar binários, aplicações e comportamento runtime.

[Engenharia-Reversa/package.json:5](../../../02_repositorios/Engenharia-Reversa/package.json)

### Arquitetura

**documentado** — CLI e MCP compartilham workflows; protocolos de engine ficam fora de domain/application.

[Engenharia-Reversa/AGENTS.md:17](../../../02_repositorios/Engenharia-Reversa/AGENTS.md)

### Fluxo

**código presente** — Runtime MCP foi separado em composição e transporte; eagerRuntime é fonte atual.

[Engenharia-Reversa/src/main/eagerRuntime.ts:12](../../../02_repositorios/Engenharia-Reversa/src/main/eagerRuntime.ts)

### Dados

**documentado** — Semântica de Evidence e sessões tem proveniência e distingue observações/inferências; não é um banco corporativo inferido.

[Engenharia-Reversa/AGENTS.md:5](../../../02_repositorios/Engenharia-Reversa/AGENTS.md)

### Interfaces

**observado** — Bridge Java integra API Ghidra; transporte MCP presente no código não implica instalação nesta sessão.

[Engenharia-Reversa/bridge/ghidra/ReaGhidraBridge.java:118](../../../02_repositorios/Engenharia-Reversa/bridge/ghidra/ReaGhidraBridge.java)

### Configuração/deploy

**documentado** — Pacote npm rea-agents publica CLI e ponte Java; engines são BYO conforme contrato local.

[Engenharia-Reversa/AGENTS.md:11](../../../02_repositorios/Engenharia-Reversa/AGENTS.md)

### Operação

**observado** — CLI documenta comando doctor e contratos de diagnóstico; não exercitados.

[Engenharia-Reversa/src/cli.ts:98](../../../02_repositorios/Engenharia-Reversa/src/cli.ts)

### Fine-tuning

**não demonstrado na amostra** — Sem conclusão positiva nesta revisão estática; não equivale a ausência universal.


### RAG

**não demonstrado na amostra** — Sem conclusão positiva nesta revisão estática; não equivale a ausência universal.


### Pós-treino

**não demonstrado na amostra** — Sem conclusão positiva nesta revisão estática; não equivale a ausência universal.


### Inferência

**não demonstrado na amostra** — Sem conclusão positiva nesta revisão estática; não equivale a ausência universal.


### Tecnologias/versões

**declarado** — Ver declarações extraídas e manifests; versões instaladas e compatibilidade não verificadas.

[Engenharia-Reversa/package.json:2](../../../02_repositorios/Engenharia-Reversa/package.json)
[Engenharia-Reversa/package.json:339](../../../02_repositorios/Engenharia-Reversa/package.json)
[Engenharia-Reversa/package.json:341](../../../02_repositorios/Engenharia-Reversa/package.json)
[Engenharia-Reversa/package.json:342](../../../02_repositorios/Engenharia-Reversa/package.json)
[Engenharia-Reversa/package.json:343](../../../02_repositorios/Engenharia-Reversa/package.json)
[Engenharia-Reversa/package.json:344](../../../02_repositorios/Engenharia-Reversa/package.json)
[Engenharia-Reversa/package.json:345](../../../02_repositorios/Engenharia-Reversa/package.json)
[Engenharia-Reversa/package.json:346](../../../02_repositorios/Engenharia-Reversa/package.json)

### Vulnerabilidades

**não verificado** — Sem consulta de CVE/EOL nesta missão.


### Obsolescência

**não verificado** — Sem consulta de CVE/EOL nesta missão.


## Declarações de versão

| Manifest / declaração | Valor | Evidência |
|---|---|---|
| name | rea-agents | [Engenharia-Reversa/package.json:2](../../../02_repositorios/Engenharia-Reversa/package.json) |
| version | 6.8.0 | [Engenharia-Reversa/package.json:4](../../../02_repositorios/Engenharia-Reversa/package.json) |
| packageManager | npm@11.16.0 | [Engenharia-Reversa/package.json:48](../../../02_repositorios/Engenharia-Reversa/package.json) |
| engines:node | ^22.23.4 &#124;&#124; ^24.22.1 &#124;&#124; >=26.12.1 | [Engenharia-Reversa/package.json:46](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:@babel/parser | 8.0.4 | [Engenharia-Reversa/package.json:339](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:@babel/types | 8.0.4 | [Engenharia-Reversa/package.json:339](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:@bufbuild/protobuf | 2.16.0 | [Engenharia-Reversa/package.json:341](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:@clack/prompts | 1.7.0 | [Engenharia-Reversa/package.json:342](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:@electron/asar | 4.2.0 | [Engenharia-Reversa/package.json:343](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:@jridgewell/trace-mapping | 0.3.31 | [Engenharia-Reversa/package.json:344](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:@lydell/node-pty | 1.1.0 | [Engenharia-Reversa/package.json:345](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:@modelcontextprotocol/client | 2.3.1 | [Engenharia-Reversa/package.json:346](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:@modelcontextprotocol/server | 2.3.1 | [Engenharia-Reversa/package.json:346](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:@msgpack/msgpack | 3.1.3 | [Engenharia-Reversa/package.json:348](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:@xmldom/xmldom | 0.9.12 | [Engenharia-Reversa/package.json:349](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:@xterm/addon-serialize | 0.14.0 | [Engenharia-Reversa/package.json:350](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:@xterm/headless | 6.0.0 | [Engenharia-Reversa/package.json:351](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:@zip.js/zip.js | 2.15.0 | [Engenharia-Reversa/package.json:352](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:ajv | 8.20.0 | [Engenharia-Reversa/package.json:353](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:ajv-formats | 3.0.1 | [Engenharia-Reversa/package.json:354](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:canonicalize | 3.0.0 | [Engenharia-Reversa/package.json:355](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:cborg | 6.1.3 | [Engenharia-Reversa/package.json:356](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:cross-spawn | 7.0.6 | [Engenharia-Reversa/package.json:357](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:diff | 9.0.0 | [Engenharia-Reversa/package.json:358](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:evmole | 0.9.3 | [Engenharia-Reversa/package.json:359](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:har-schema | 2.0.0 | [Engenharia-Reversa/package.json:360](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:ignore | 7.0.6 | [Engenharia-Reversa/package.json:357](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:incur | 0.6.1 | [Engenharia-Reversa/package.json:362](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:isomorphic-git | 1.38.7 | [Engenharia-Reversa/package.json:363](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:jsonc-parser | 3.3.1 | [Engenharia-Reversa/package.json:364](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:lossless-json | 4.3.1 | [Engenharia-Reversa/package.json:365](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:openpgp | 6.3.2 | [Engenharia-Reversa/package.json:366](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:parse5 | 8.0.1 | [Engenharia-Reversa/package.json:367](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:pino | 10.4.0 | [Engenharia-Reversa/package.json:368](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:playwright-core | 1.64.1 | [Engenharia-Reversa/package.json:369](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:plist | 5.0.0 | [Engenharia-Reversa/package.json:370](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:saxes | 6.0.0 | [Engenharia-Reversa/package.json:351](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:semver | 7.8.5 | [Engenharia-Reversa/package.json:372](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:smol-toml | 1.9.0 | [Engenharia-Reversa/package.json:373](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:stream-chain | 4.2.6 | [Engenharia-Reversa/package.json:374](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:stream-json | 3.7.0 | [Engenharia-Reversa/package.json:375](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:tokenx | 1.3.0 | [Engenharia-Reversa/package.json:376](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:write-file-atomic | 7.0.0 | [Engenharia-Reversa/package.json:377](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:ws | 8.21.0 | [Engenharia-Reversa/package.json:378](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:yaml | 2.9.0 | [Engenharia-Reversa/package.json:379](../../../02_repositorios/Engenharia-Reversa/package.json) |
| dependencies:zod | 4.6.6 | [Engenharia-Reversa/package.json:380](../../../02_repositorios/Engenharia-Reversa/package.json) |
| devDependencies:@fast-check/vitest | 0.5.0 | [Engenharia-Reversa/package.json:391](../../../02_repositorios/Engenharia-Reversa/package.json) |
| devDependencies:@stryker-mutator/core | 10.0.0 | [Engenharia-Reversa/package.json:392](../../../02_repositorios/Engenharia-Reversa/package.json) |
| devDependencies:@stryker-mutator/typescript-checker | 10.0.0 | [Engenharia-Reversa/package.json:392](../../../02_repositorios/Engenharia-Reversa/package.json) |
| devDependencies:@stryker-mutator/vitest-runner | 10.0.0 | [Engenharia-Reversa/package.json:392](../../../02_repositorios/Engenharia-Reversa/package.json) |
| devDependencies:@types/cross-spawn | 6.0.6 | [Engenharia-Reversa/package.json:395](../../../02_repositorios/Engenharia-Reversa/package.json) |
| devDependencies:@types/node | 26.6.4 | [Engenharia-Reversa/package.json:396](../../../02_repositorios/Engenharia-Reversa/package.json) |
| devDependencies:@types/semver | 7.7.1 | [Engenharia-Reversa/package.json:397](../../../02_repositorios/Engenharia-Reversa/package.json) |
| devDependencies:@types/write-file-atomic | 4.0.3 | [Engenharia-Reversa/package.json:398](../../../02_repositorios/Engenharia-Reversa/package.json) |
| devDependencies:@types/ws | 8.18.1 | [Engenharia-Reversa/package.json:399](../../../02_repositorios/Engenharia-Reversa/package.json) |
| devDependencies:@vitest/coverage-v8 | 5.0.3 | [Engenharia-Reversa/package.json:400](../../../02_repositorios/Engenharia-Reversa/package.json) |
| devDependencies:husky | 9.1.7 | [Engenharia-Reversa/package.json:401](../../../02_repositorios/Engenharia-Reversa/package.json) |
| devDependencies:jscpd | 5.0.12 | [Engenharia-Reversa/package.json:402](../../../02_repositorios/Engenharia-Reversa/package.json) |
| devDependencies:knip | 6.39.0 | [Engenharia-Reversa/package.json:403](../../../02_repositorios/Engenharia-Reversa/package.json) |
| devDependencies:lint-staged | 16.4.0 | [Engenharia-Reversa/package.json:404](../../../02_repositorios/Engenharia-Reversa/package.json) |
| devDependencies:oxfmt | 0.72.0 | [Engenharia-Reversa/package.json:405](../../../02_repositorios/Engenharia-Reversa/package.json) |
| devDependencies:oxlint | 1.87.0 | [Engenharia-Reversa/package.json:406](../../../02_repositorios/Engenharia-Reversa/package.json) |
| devDependencies:oxlint-tsgolint | 7.0.2005 | [Engenharia-Reversa/package.json:407](../../../02_repositorios/Engenharia-Reversa/package.json) |
| devDependencies:release-please | 17.3.0 | [Engenharia-Reversa/package.json:408](../../../02_repositorios/Engenharia-Reversa/package.json) |
| devDependencies:rolldown | 1.2.12 | [Engenharia-Reversa/package.json:409](../../../02_repositorios/Engenharia-Reversa/package.json) |
| devDependencies:tsrs | 0.18.0-ts7.1.0-dev.20260929 | [Engenharia-Reversa/package.json:410](../../../02_repositorios/Engenharia-Reversa/package.json) |
| devDependencies:tsx | 4.23.15 | [Engenharia-Reversa/package.json:411](../../../02_repositorios/Engenharia-Reversa/package.json) |
| devDependencies:turbo | 2.11.7 | [Engenharia-Reversa/package.json:412](../../../02_repositorios/Engenharia-Reversa/package.json) |
| devDependencies:typescript | 7.0.2 | [Engenharia-Reversa/package.json:407](../../../02_repositorios/Engenharia-Reversa/package.json) |
| devDependencies:typescript-termux | npm:typescript@5.9.3 | [Engenharia-Reversa/package.json:414](../../../02_repositorios/Engenharia-Reversa/package.json) |
| devDependencies:typescript6 | npm:typescript@6.0.3 | [Engenharia-Reversa/package.json:415](../../../02_repositorios/Engenharia-Reversa/package.json) |
| devDependencies:vitepress | 1.6.4 | [Engenharia-Reversa/package.json:416](../../../02_repositorios/Engenharia-Reversa/package.json) |
| devDependencies:vitest | 5.0.3 | [Engenharia-Reversa/package.json:400](../../../02_repositorios/Engenharia-Reversa/package.json) |
| name | rea-verify-skills-cli | [Engenharia-Reversa/scripts/verify-tools/skills/package.json:2](../../../02_repositorios/Engenharia-Reversa/scripts/verify-tools/skills/package.json) |
| dependencies:skills | 1.7.2 | [Engenharia-Reversa/scripts/verify-tools/skills/package.json:6](../../../02_repositorios/Engenharia-Reversa/scripts/verify-tools/skills/package.json) |
| name | rea-readiness-electron | [Engenharia-Reversa/tests/conformance/readiness/electron/package.json:2](../../../02_repositorios/Engenharia-Reversa/tests/conformance/readiness/electron/package.json) |
| version | 1.0.0 | [Engenharia-Reversa/tests/conformance/readiness/electron/package.json:3](../../../02_repositorios/Engenharia-Reversa/tests/conformance/readiness/electron/package.json) |
| name | rea-readiness-javascript-cli | [Engenharia-Reversa/tests/conformance/readiness/javascript-cli/package.json:2](../../../02_repositorios/Engenharia-Reversa/tests/conformance/readiness/javascript-cli/package.json) |
| version | 1.0.0 | [Engenharia-Reversa/tests/conformance/readiness/javascript-cli/package.json:3](../../../02_repositorios/Engenharia-Reversa/tests/conformance/readiness/javascript-cli/package.json) |
| dependency | CairoSVG==2.9.1 | [Engenharia-Reversa/website/requirements.txt:2](../../../02_repositorios/Engenharia-Reversa/website/requirements.txt) |
| dependency | polib==1.2.0 | [Engenharia-Reversa/website/requirements.txt:4](../../../02_repositorios/Engenharia-Reversa/website/requirements.txt) |
| name | rea-notes-example | [Engenharia-Reversa/website/public/examples/notes-electron/package.json:2](../../../02_repositorios/Engenharia-Reversa/website/public/examples/notes-electron/package.json) |
| version | 1.0.0 | [Engenharia-Reversa/website/public/examples/notes-electron/package.json:3](../../../02_repositorios/Engenharia-Reversa/website/public/examples/notes-electron/package.json) |

## Qualidade e limites

Workflows: 34; arquivos candidatos a testes: 3012. Não executados.

- Amostra semântica seletiva; hash e busca textual não equivalem a auditoria integral.
- Nenhum runtime, treino, publicação ou sincronização remota executado.
- Fontes modificadas/não rastreadas fazem parte deste snapshot local.
