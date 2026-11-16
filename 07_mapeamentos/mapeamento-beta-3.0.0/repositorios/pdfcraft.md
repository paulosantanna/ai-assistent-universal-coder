# pdfcraft — beta 3.0.0

Updated: 2026-10-27
Entry point: [índice](../README.md) · [mapa estruturado](../mapa.json)

Arquivos com hash: 543; fingerprint: `54801aca3dbe4346eb6575cd6d628d6e8a3c664b4e5f505f6bb08d2ca64561a3`.
Git próprio: True; HEAD: `7437bde378f43856eada40af25b983812e615e8a`; branch: `main`.
Estado local: limpo; detalhes em inventory.json.

## Atualizações e reconciliação

Workspace Rust/CLI/MCP opt-in mantido; regras de clean-room/licença devem acompanhar reutilização.

## Dimensões e evidências

### Propósito

**declarado** — Workbench PDF nativo, com leitura, organização, combinação, separação e segurança de PDFs.

[pdfcraft/README.md:14](../../../02_repositorios/pdfcraft/README.md)

### Arquitetura

**observado** — Workspace Rust com crates de engine/UI e aplicativos desktop, CLI e web; automação compartilha tabela de tools.

[pdfcraft/crates/automation/src/lib.rs:6](../../../02_repositorios/pdfcraft/crates/automation/src/lib.rs)

### Fluxo

**observado** — CLI roteia subcomandos e MCP opcional; Automation::call resolve tool pelo nome e retorna Result.

[pdfcraft/crates/automation/src/lib.rs:168](../../../02_repositorios/pdfcraft/crates/automation/src/lib.rs)

### Dados

**observado** — Engine mantém documento, formulários e trust store de assinaturas; documentos externos são entradas não confiáveis.

[pdfcraft/crates/engine/src/lib.rs:331](../../../02_repositorios/pdfcraft/crates/engine/src/lib.rs)

### Interfaces

**observado** — Automação headless e MCP reaproveitam contrato JSON; a11y de PDF é funcionalidade de documento.

[pdfcraft/crates/automation/README.md:3](../../../02_repositorios/pdfcraft/crates/automation/README.md)

### Configuração/deploy

**observado** — MCP é opt-in e depende da feature Cargo mcp; ausente na build produz erro explícito.

[pdfcraft/apps/pdfcraft-cli/src/main.rs:103](../../../02_repositorios/pdfcraft/apps/pdfcraft-cli/src/main.rs)

### Operação

**observado** — Aplicativo registra logs/panics; contrato proíbe panics em caminhos de entradas externas.

[pdfcraft/apps/pdfcraft/src/main.rs:163](../../../02_repositorios/pdfcraft/apps/pdfcraft/src/main.rs)

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

[pdfcraft/Cargo.toml:11](../../../02_repositorios/pdfcraft/Cargo.toml)
[pdfcraft/Cargo.toml:8](../../../02_repositorios/pdfcraft/Cargo.toml)
[pdfcraft/Cargo.toml:9](../../../02_repositorios/pdfcraft/Cargo.toml)
[pdfcraft/apps/pdfcraft-cli/Cargo.toml:2](../../../02_repositorios/pdfcraft/apps/pdfcraft-cli/Cargo.toml)
[pdfcraft/apps/pdfcraft-web/Cargo.toml:2](../../../02_repositorios/pdfcraft/apps/pdfcraft-web/Cargo.toml)
[pdfcraft/apps/pdfcraft/Cargo.toml:2](../../../02_repositorios/pdfcraft/apps/pdfcraft/Cargo.toml)
[pdfcraft/crates/a11y/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/a11y/Cargo.toml)
[pdfcraft/crates/annot/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/annot/Cargo.toml)

### Vulnerabilidades

**não verificado** — Sem consulta de CVE/EOL nesta missão.


### Obsolescência

**não verificado** — Sem consulta de CVE/EOL nesta missão.


## Declarações de versão

| Manifest / declaração | Valor | Evidência |
|---|---|---|
| version | 0.7.1 | [pdfcraft/Cargo.toml:8](../../../02_repositorios/pdfcraft/Cargo.toml) |
| edition | 2024 | [pdfcraft/Cargo.toml:9](../../../02_repositorios/pdfcraft/Cargo.toml) |
| rust-version | 1.95 | [pdfcraft/Cargo.toml:11](../../../02_repositorios/pdfcraft/Cargo.toml) |
| name | pdfcraft | [pdfcraft/apps/pdfcraft/Cargo.toml:2](../../../02_repositorios/pdfcraft/apps/pdfcraft/Cargo.toml) |
| name | pdfcraft-cli | [pdfcraft/apps/pdfcraft-cli/Cargo.toml:2](../../../02_repositorios/pdfcraft/apps/pdfcraft-cli/Cargo.toml) |
| name | pdfcraft-web | [pdfcraft/apps/pdfcraft-web/Cargo.toml:2](../../../02_repositorios/pdfcraft/apps/pdfcraft-web/Cargo.toml) |
| name | pdfcraft-a11y | [pdfcraft/crates/a11y/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/a11y/Cargo.toml) |
| name | pdfcraft-annot | [pdfcraft/crates/annot/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/annot/Cargo.toml) |
| name | pdfcraft-audit | [pdfcraft/crates/audit/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/audit/Cargo.toml) |
| name | pdfcraft-automation | [pdfcraft/crates/automation/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/automation/Cargo.toml) |
| name | pdfcraft-compare | [pdfcraft/crates/compare/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/compare/Cargo.toml) |
| name | pdfcraft-content | [pdfcraft/crates/content/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/content/Cargo.toml) |
| name | pdfcraft-cos | [pdfcraft/crates/cos/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/cos/Cargo.toml) |
| name | pdfcraft-create | [pdfcraft/crates/create/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/create/Cargo.toml) |
| name | pdfcraft-crypt | [pdfcraft/crates/crypt/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/crypt/Cargo.toml) |
| name | pdfcraft-edit | [pdfcraft/crates/edit/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/edit/Cargo.toml) |
| name | pdfcraft-engine | [pdfcraft/crates/engine/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/engine/Cargo.toml) |
| name | pdfcraft-export | [pdfcraft/crates/export/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/export/Cargo.toml) |
| name | pdfcraft-filters | [pdfcraft/crates/filters/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/filters/Cargo.toml) |
| name | pdfcraft-filters-fuzz | [pdfcraft/crates/filters/fuzz/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/filters/fuzz/Cargo.toml) |
| version | 0.0.0 | [pdfcraft/crates/filters/fuzz/Cargo.toml:3](../../../02_repositorios/pdfcraft/crates/filters/fuzz/Cargo.toml) |
| edition | 2024 | [pdfcraft/crates/filters/fuzz/Cargo.toml:5](../../../02_repositorios/pdfcraft/crates/filters/fuzz/Cargo.toml) |
| name | pdfcraft-fonts | [pdfcraft/crates/fonts/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/fonts/Cargo.toml) |
| name | pdfcraft-forms | [pdfcraft/crates/forms/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/forms/Cargo.toml) |
| name | pdfcraft-geom | [pdfcraft/crates/geom/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/geom/Cargo.toml) |
| name | pdfcraft-js | [pdfcraft/crates/js/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/js/Cargo.toml) |
| name | pdfcraft-measure | [pdfcraft/crates/measure/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/measure/Cargo.toml) |
| name | pdfcraft-model | [pdfcraft/crates/model/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/model/Cargo.toml) |
| name | pdfcraft-ocr | [pdfcraft/crates/ocr/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/ocr/Cargo.toml) |
| name | pdfcraft-optimize | [pdfcraft/crates/optimize/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/optimize/Cargo.toml) |
| name | pdfcraft-organize | [pdfcraft/crates/organize/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/organize/Cargo.toml) |
| name | pdfcraft-platform | [pdfcraft/crates/platform/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/platform/Cargo.toml) |
| name | pdfcraft-preflight | [pdfcraft/crates/preflight/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/preflight/Cargo.toml) |
| name | pdfcraft-print | [pdfcraft/crates/print/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/print/Cargo.toml) |
| name | pdfcraft-redact | [pdfcraft/crates/redact/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/redact/Cargo.toml) |
| name | pdfcraft-render | [pdfcraft/crates/render/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/render/Cargo.toml) |
| name | pdfcraft-sign | [pdfcraft/crates/sign/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/sign/Cargo.toml) |
| name | pdfcraft-ui-egui | [pdfcraft/crates/ui-egui/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/ui-egui/Cargo.toml) |
| rust-version | 1.95 | [pdfcraft/crates/ui-egui/Cargo.toml:7](../../../02_repositorios/pdfcraft/crates/ui-egui/Cargo.toml) |
| name | pdfcraft-xfa | [pdfcraft/crates/xfa/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/xfa/Cargo.toml) |
| name | pdfcraft-xfdf | [pdfcraft/crates/xfdf/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/xfdf/Cargo.toml) |
| name | xtask | [pdfcraft/xtask/Cargo.toml:2](../../../02_repositorios/pdfcraft/xtask/Cargo.toml) |
| version | 0.1.0 | [pdfcraft/xtask/Cargo.toml:3](../../../02_repositorios/pdfcraft/xtask/Cargo.toml) |
| edition | 2024 | [pdfcraft/xtask/Cargo.toml:4](../../../02_repositorios/pdfcraft/xtask/Cargo.toml) |

## Qualidade e limites

Workflows: 5; arquivos candidatos a testes: 103. Não executados.

- Amostra semântica seletiva; hash e busca textual não equivalem a auditoria integral.
- Nenhum runtime, treino, publicação ou sincronização remota executado.
- Fontes modificadas/não rastreadas fazem parte deste snapshot local.
