# pdfcraft — mapa estático de skills

Updated: 2026-10-13

Entry point: ../README.md

Tipo: Git próprio. Arquivos no inventário delimitado: 603; entradas excluídas: 6.

[Voltar ao índice](../README.md) · [Matriz completa](../matriz.csv)

## Dez dimensões

| Dimensão | Estado | Observação | Evidência |
| --- | --- | --- | --- |
| Tecnologias e versões | declarado | Declarações extraídas dos manifests, incluindo faixas e extras. Não são versões instaladas nem prova de compatibilidade. Lockfiles permanecem nas fontes para análise posterior. | [02_repositorios/pdfcraft/Cargo.toml:11](../../../02_repositorios/pdfcraft/Cargo.toml); [02_repositorios/pdfcraft/Cargo.toml:16](../../../02_repositorios/pdfcraft/Cargo.toml); [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml); demais fontes em mapa.json/declarações abaixo |
| Arquitetura | observado | Workspace Rust com crates de engine/UI e aplicativos desktop, CLI e web; automação compartilha tabela de tools. | [02_repositorios/pdfcraft/crates/automation/src/lib.rs:6](../../../02_repositorios/pdfcraft/crates/automation/src/lib.rs) |
| Propósito | declarado | Workbench PDF nativo, com leitura, organização, combinação, separação e segurança de PDFs. | [02_repositorios/pdfcraft/README.md:14](../../../02_repositorios/pdfcraft/README.md) |
| Fluxo | observado | CLI roteia subcomandos e MCP opcional; Automation::call resolve tool pelo nome e retorna Result. | [02_repositorios/pdfcraft/crates/automation/src/lib.rs:168](../../../02_repositorios/pdfcraft/crates/automation/src/lib.rs) |
| Dados | observado | Engine mantém documento, formulários e trust store de assinaturas; documentos externos são entradas não confiáveis. | [02_repositorios/pdfcraft/crates/engine/src/lib.rs:331](../../../02_repositorios/pdfcraft/crates/engine/src/lib.rs) |
| Configuração/deploy | observado | MCP é opt-in e depende da feature Cargo mcp; ausente na build produz erro explícito. | [02_repositorios/pdfcraft/apps/pdfcraft-cli/src/main.rs:103](../../../02_repositorios/pdfcraft/apps/pdfcraft-cli/src/main.rs) |
| Operação/observabilidade | observado | Aplicativo registra logs/panics; contrato proíbe panics em caminhos de entradas externas. | [02_repositorios/pdfcraft/apps/pdfcraft/src/main.rs:163](../../../02_repositorios/pdfcraft/apps/pdfcraft/src/main.rs) |
| Interfaces/dependências | observado | Automação headless e MCP reaproveitam contrato JSON; a11y de PDF é funcionalidade de documento. | [02_repositorios/pdfcraft/crates/automation/README.md:3](../../../02_repositorios/pdfcraft/crates/automation/README.md) |
| Vulnerabilidades | não verificado | Nenhuma consulta atual a advisories/scanner foi executada; não equivale a ausência de CVEs. | Sem verificação nesta missão |
| Obsolescência | não verificado | Datas de suporte/EOL não consultadas. Versões declaradas não comprovam suporte atual. | Sem verificação nesta missão |

## Declarações dos manifests

Faixas e extras são preservados; versões instaladas/resolvidas não foram verificadas.

| Declaração | Valor | Fonte |
| --- | --- | --- |
| version | 0.7.1 | [02_repositorios/pdfcraft/Cargo.toml:8](../../../02_repositorios/pdfcraft/Cargo.toml) |
| edition | 2024 | [02_repositorios/pdfcraft/Cargo.toml:9](../../../02_repositorios/pdfcraft/Cargo.toml) |
| rust-version | 1.95 | [02_repositorios/pdfcraft/Cargo.toml:11](../../../02_repositorios/pdfcraft/Cargo.toml) |
| craft-ui | 0.1.0 | [02_repositorios/pdfcraft/Cargo.toml:16](../../../02_repositorios/pdfcraft/Cargo.toml) |
| craft-print | 0.1.0 | [02_repositorios/pdfcraft/Cargo.toml:16](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-geom | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-filters | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-cos | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-crypt | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-organize | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-measure | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-annot | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-audit | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-fonts | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-model | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-content | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-redact | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-print | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-xfdf | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-sign | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-optimize | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-a11y | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-ocr | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-js | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-compare | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-preflight | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-export | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-edit | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-create | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-forms | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-xfa | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-render | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-engine | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-platform | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-ui-egui | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| pdfcraft-automation | 0.7.0 | [02_repositorios/pdfcraft/Cargo.toml:20](../../../02_repositorios/pdfcraft/Cargo.toml) |
| hayro | 0.7.1 | [02_repositorios/pdfcraft/Cargo.toml:8](../../../02_repositorios/pdfcraft/Cargo.toml) |
| hayro-syntax | 0.7.2 | [02_repositorios/pdfcraft/Cargo.toml:54](../../../02_repositorios/pdfcraft/Cargo.toml) |
| lopdf | 0.45 | [02_repositorios/pdfcraft/Cargo.toml:55](../../../02_repositorios/pdfcraft/Cargo.toml) |
| flate2 | 1.1 | [02_repositorios/pdfcraft/Cargo.toml:56](../../../02_repositorios/pdfcraft/Cargo.toml) |
| weezl | 0.2 | [02_repositorios/pdfcraft/Cargo.toml:57](../../../02_repositorios/pdfcraft/Cargo.toml) |
| thiserror | 2 | [02_repositorios/pdfcraft/Cargo.toml:9](../../../02_repositorios/pdfcraft/Cargo.toml) |
| serde | 1 | [02_repositorios/pdfcraft/Cargo.toml:8](../../../02_repositorios/pdfcraft/Cargo.toml) |
| serde_json | 1 | [02_repositorios/pdfcraft/Cargo.toml:8](../../../02_repositorios/pdfcraft/Cargo.toml) |
| log | 0.4 | [02_repositorios/pdfcraft/Cargo.toml:55](../../../02_repositorios/pdfcraft/Cargo.toml) |
| kurbo | 0.13 | [02_repositorios/pdfcraft/Cargo.toml:64](../../../02_repositorios/pdfcraft/Cargo.toml) |
| proptest | 1 | [02_repositorios/pdfcraft/Cargo.toml:8](../../../02_repositorios/pdfcraft/Cargo.toml) |
| egui | 0.36 | [02_repositorios/pdfcraft/Cargo.toml:70](../../../02_repositorios/pdfcraft/Cargo.toml) |
| egui_extras | 0.36 | [02_repositorios/pdfcraft/Cargo.toml:70](../../../02_repositorios/pdfcraft/Cargo.toml) |
| eframe | 0.36 | [02_repositorios/pdfcraft/Cargo.toml:70](../../../02_repositorios/pdfcraft/Cargo.toml) |
| egui_kittest | 0.36 | [02_repositorios/pdfcraft/Cargo.toml:70](../../../02_repositorios/pdfcraft/Cargo.toml) |
| rfd | 0.17 | [02_repositorios/pdfcraft/Cargo.toml:74](../../../02_repositorios/pdfcraft/Cargo.toml) |
| name | pdfcraft | [02_repositorios/pdfcraft/apps/pdfcraft/Cargo.toml:2](../../../02_repositorios/pdfcraft/apps/pdfcraft/Cargo.toml) |
| ureq | 3.4 | [02_repositorios/pdfcraft/apps/pdfcraft/Cargo.toml:14](../../../02_repositorios/pdfcraft/apps/pdfcraft/Cargo.toml) |
| rustls-native-certs | 0.8 | [02_repositorios/pdfcraft/apps/pdfcraft/Cargo.toml:15](../../../02_repositorios/pdfcraft/apps/pdfcraft/Cargo.toml) |
| name | pdfcraft-cli | [02_repositorios/pdfcraft/apps/pdfcraft-cli/Cargo.toml:2](../../../02_repositorios/pdfcraft/apps/pdfcraft-cli/Cargo.toml) |
| base64 | 0.22 | [02_repositorios/pdfcraft/apps/pdfcraft-cli/Cargo.toml:22](../../../02_repositorios/pdfcraft/apps/pdfcraft-cli/Cargo.toml) |
| name | pdfcraft-web | [02_repositorios/pdfcraft/apps/pdfcraft-web/Cargo.toml:2](../../../02_repositorios/pdfcraft/apps/pdfcraft-web/Cargo.toml) |
| name | pdfcraft-a11y | [02_repositorios/pdfcraft/crates/a11y/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/a11y/Cargo.toml) |
| name | pdfcraft-annot | [02_repositorios/pdfcraft/crates/annot/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/annot/Cargo.toml) |
| name | pdfcraft-audit | [02_repositorios/pdfcraft/crates/audit/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/audit/Cargo.toml) |
| name | pdfcraft-automation | [02_repositorios/pdfcraft/crates/automation/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/automation/Cargo.toml) |
| sha2 | 0.11 | [02_repositorios/pdfcraft/crates/automation/Cargo.toml:18](../../../02_repositorios/pdfcraft/crates/automation/Cargo.toml) |
| tempfile | 3.27 | [02_repositorios/pdfcraft/crates/automation/Cargo.toml:19](../../../02_repositorios/pdfcraft/crates/automation/Cargo.toml) |
| png | 0.18 | [02_repositorios/pdfcraft/crates/automation/Cargo.toml:20](../../../02_repositorios/pdfcraft/crates/automation/Cargo.toml) |
| base64 | 0.22 | [02_repositorios/pdfcraft/crates/automation/Cargo.toml:21](../../../02_repositorios/pdfcraft/crates/automation/Cargo.toml) |
| name | pdfcraft-compare | [02_repositorios/pdfcraft/crates/compare/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/compare/Cargo.toml) |
| name | pdfcraft-content | [02_repositorios/pdfcraft/crates/content/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/content/Cargo.toml) |
| name | pdfcraft-cos | [02_repositorios/pdfcraft/crates/cos/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/cos/Cargo.toml) |
| name | pdfcraft-create | [02_repositorios/pdfcraft/crates/create/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/create/Cargo.toml) |
| png | 0.18 | [02_repositorios/pdfcraft/crates/create/Cargo.toml:15](../../../02_repositorios/pdfcraft/crates/create/Cargo.toml) |
| tiff | 0.11 | [02_repositorios/pdfcraft/crates/create/Cargo.toml:16](../../../02_repositorios/pdfcraft/crates/create/Cargo.toml) |
| image | 0.25 | [02_repositorios/pdfcraft/crates/create/Cargo.toml:17](../../../02_repositorios/pdfcraft/crates/create/Cargo.toml) |
| zune-jpeg | 0.5 | [02_repositorios/pdfcraft/crates/create/Cargo.toml:19](../../../02_repositorios/pdfcraft/crates/create/Cargo.toml) |
| encoding_rs | 0.8 | [02_repositorios/pdfcraft/crates/create/Cargo.toml:22](../../../02_repositorios/pdfcraft/crates/create/Cargo.toml) |
| name | pdfcraft-crypt | [02_repositorios/pdfcraft/crates/crypt/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/crypt/Cargo.toml) |
| aes | 0.9 | [02_repositorios/pdfcraft/crates/crypt/Cargo.toml:14](../../../02_repositorios/pdfcraft/crates/crypt/Cargo.toml) |
| md-5 | 0.11 | [02_repositorios/pdfcraft/crates/crypt/Cargo.toml:15](../../../02_repositorios/pdfcraft/crates/crypt/Cargo.toml) |
| sha2 | 0.11 | [02_repositorios/pdfcraft/crates/crypt/Cargo.toml:15](../../../02_repositorios/pdfcraft/crates/crypt/Cargo.toml) |
| stringprep | 0.1 | [02_repositorios/pdfcraft/crates/crypt/Cargo.toml:15](../../../02_repositorios/pdfcraft/crates/crypt/Cargo.toml) |
| name | pdfcraft-edit | [02_repositorios/pdfcraft/crates/edit/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/edit/Cargo.toml) |
| unicode-bidi | 0.3 | [02_repositorios/pdfcraft/crates/edit/Cargo.toml:21](../../../02_repositorios/pdfcraft/crates/edit/Cargo.toml) |
| name | pdfcraft-engine | [02_repositorios/pdfcraft/crates/engine/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/engine/Cargo.toml) |
| image | 0.25 | [02_repositorios/pdfcraft/crates/engine/Cargo.toml:13](../../../02_repositorios/pdfcraft/crates/engine/Cargo.toml) |
| png | 0.18 | [02_repositorios/pdfcraft/crates/engine/Cargo.toml:38](../../../02_repositorios/pdfcraft/crates/engine/Cargo.toml) |
| url | 2.5 | [02_repositorios/pdfcraft/crates/engine/Cargo.toml:41](../../../02_repositorios/pdfcraft/crates/engine/Cargo.toml) |
| idna | 1.1 | [02_repositorios/pdfcraft/crates/engine/Cargo.toml:42](../../../02_repositorios/pdfcraft/crates/engine/Cargo.toml) |
| icu_properties | 2.3 | [02_repositorios/pdfcraft/crates/engine/Cargo.toml:43](../../../02_repositorios/pdfcraft/crates/engine/Cargo.toml) |
| name | pdfcraft-export | [02_repositorios/pdfcraft/crates/export/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/export/Cargo.toml) |
| name | pdfcraft-filters | [02_repositorios/pdfcraft/crates/filters/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/filters/Cargo.toml) |
| name | pdfcraft-filters-fuzz | [02_repositorios/pdfcraft/crates/filters/fuzz/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/filters/fuzz/Cargo.toml) |
| version | 0.0.0 | [02_repositorios/pdfcraft/crates/filters/fuzz/Cargo.toml:3](../../../02_repositorios/pdfcraft/crates/filters/fuzz/Cargo.toml) |
| edition | 2024 | [02_repositorios/pdfcraft/crates/filters/fuzz/Cargo.toml:5](../../../02_repositorios/pdfcraft/crates/filters/fuzz/Cargo.toml) |
| libfuzzer-sys | 0.4 | [02_repositorios/pdfcraft/crates/filters/fuzz/Cargo.toml:16](../../../02_repositorios/pdfcraft/crates/filters/fuzz/Cargo.toml) |
| name | pdfcraft-fonts | [02_repositorios/pdfcraft/crates/fonts/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/fonts/Cargo.toml) |
| skrifa | 0.44 | [02_repositorios/pdfcraft/crates/fonts/Cargo.toml:14](../../../02_repositorios/pdfcraft/crates/fonts/Cargo.toml) |
| harfrust | 0.12 | [02_repositorios/pdfcraft/crates/fonts/Cargo.toml:16](../../../02_repositorios/pdfcraft/crates/fonts/Cargo.toml) |
| unicode-bidi | 0.3 | [02_repositorios/pdfcraft/crates/fonts/Cargo.toml:17](../../../02_repositorios/pdfcraft/crates/fonts/Cargo.toml) |
| name | pdfcraft-forms | [02_repositorios/pdfcraft/crates/forms/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/forms/Cargo.toml) |
| name | pdfcraft-geom | [02_repositorios/pdfcraft/crates/geom/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/geom/Cargo.toml) |
| name | pdfcraft-js | [02_repositorios/pdfcraft/crates/js/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/js/Cargo.toml) |
| boa_engine | 0.22.0 | [02_repositorios/pdfcraft/crates/js/Cargo.toml:14](../../../02_repositorios/pdfcraft/crates/js/Cargo.toml) |
| name | pdfcraft-measure | [02_repositorios/pdfcraft/crates/measure/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/measure/Cargo.toml) |
| name | pdfcraft-model | [02_repositorios/pdfcraft/crates/model/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/model/Cargo.toml) |
| name | pdfcraft-ocr | [02_repositorios/pdfcraft/crates/ocr/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/ocr/Cargo.toml) |
| ocrs | 0.13.1 | [02_repositorios/pdfcraft/crates/ocr/Cargo.toml:15](../../../02_repositorios/pdfcraft/crates/ocr/Cargo.toml) |
| rten | 0.26.0 | [02_repositorios/pdfcraft/crates/ocr/Cargo.toml:16](../../../02_repositorios/pdfcraft/crates/ocr/Cargo.toml) |
| name | pdfcraft-optimize | [02_repositorios/pdfcraft/crates/optimize/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/optimize/Cargo.toml) |
| image | 0.25 | [02_repositorios/pdfcraft/crates/optimize/Cargo.toml:20](../../../02_repositorios/pdfcraft/crates/optimize/Cargo.toml) |
| name | pdfcraft-organize | [02_repositorios/pdfcraft/crates/organize/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/organize/Cargo.toml) |
| name | pdfcraft-platform | [02_repositorios/pdfcraft/crates/platform/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/platform/Cargo.toml) |
| name | pdfcraft-preflight | [02_repositorios/pdfcraft/crates/preflight/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/preflight/Cargo.toml) |
| name | pdfcraft-print | [02_repositorios/pdfcraft/crates/print/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/print/Cargo.toml) |
| name | pdfcraft-redact | [02_repositorios/pdfcraft/crates/redact/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/redact/Cargo.toml) |
| name | pdfcraft-render | [02_repositorios/pdfcraft/crates/render/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/render/Cargo.toml) |
| bytemuck | 1 | [02_repositorios/pdfcraft/crates/render/Cargo.toml:23](../../../02_repositorios/pdfcraft/crates/render/Cargo.toml) |
| name | pdfcraft-sign | [02_repositorios/pdfcraft/crates/sign/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/sign/Cargo.toml) |
| base64 | 0.22 | [02_repositorios/pdfcraft/crates/sign/Cargo.toml:18](../../../02_repositorios/pdfcraft/crates/sign/Cargo.toml) |
| sha1 | 0.11 | [02_repositorios/pdfcraft/crates/sign/Cargo.toml:19](../../../02_repositorios/pdfcraft/crates/sign/Cargo.toml) |
| sha2 | 0.11 | [02_repositorios/pdfcraft/crates/sign/Cargo.toml:19](../../../02_repositorios/pdfcraft/crates/sign/Cargo.toml) |
| p256 | 0.14 | [02_repositorios/pdfcraft/crates/sign/Cargo.toml:21](../../../02_repositorios/pdfcraft/crates/sign/Cargo.toml) |
| p384 | 0.14 | [02_repositorios/pdfcraft/crates/sign/Cargo.toml:21](../../../02_repositorios/pdfcraft/crates/sign/Cargo.toml) |
| p521 | 0.14 | [02_repositorios/pdfcraft/crates/sign/Cargo.toml:21](../../../02_repositorios/pdfcraft/crates/sign/Cargo.toml) |
| bp256 | 0.14 | [02_repositorios/pdfcraft/crates/sign/Cargo.toml:21](../../../02_repositorios/pdfcraft/crates/sign/Cargo.toml) |
| bp384 | 0.14 | [02_repositorios/pdfcraft/crates/sign/Cargo.toml:21](../../../02_repositorios/pdfcraft/crates/sign/Cargo.toml) |
| ecdsa | 0.17 | [02_repositorios/pdfcraft/crates/sign/Cargo.toml:27](../../../02_repositorios/pdfcraft/crates/sign/Cargo.toml) |
| crypto-bigint | 0.7 | [02_repositorios/pdfcraft/crates/sign/Cargo.toml:29](../../../02_repositorios/pdfcraft/crates/sign/Cargo.toml) |
| rsa | =0.10.0-rc.18 | [02_repositorios/pdfcraft/crates/sign/Cargo.toml:30](../../../02_repositorios/pdfcraft/crates/sign/Cargo.toml) |
| pbkdf2 | 0.13 | [02_repositorios/pdfcraft/crates/sign/Cargo.toml:31](../../../02_repositorios/pdfcraft/crates/sign/Cargo.toml) |
| hmac | 0.13 | [02_repositorios/pdfcraft/crates/sign/Cargo.toml:31](../../../02_repositorios/pdfcraft/crates/sign/Cargo.toml) |
| aes | 0.9 | [02_repositorios/pdfcraft/crates/sign/Cargo.toml:33](../../../02_repositorios/pdfcraft/crates/sign/Cargo.toml) |
| cbc | 0.2 | [02_repositorios/pdfcraft/crates/sign/Cargo.toml:18](../../../02_repositorios/pdfcraft/crates/sign/Cargo.toml) |
| des | 0.9 | [02_repositorios/pdfcraft/crates/sign/Cargo.toml:33](../../../02_repositorios/pdfcraft/crates/sign/Cargo.toml) |
| rc2 | 0.9 | [02_repositorios/pdfcraft/crates/sign/Cargo.toml:33](../../../02_repositorios/pdfcraft/crates/sign/Cargo.toml) |
| sha3 | 0.12.0 | [02_repositorios/pdfcraft/crates/sign/Cargo.toml:37](../../../02_repositorios/pdfcraft/crates/sign/Cargo.toml) |
| ripemd | 0.2.0 | [02_repositorios/pdfcraft/crates/sign/Cargo.toml:38](../../../02_repositorios/pdfcraft/crates/sign/Cargo.toml) |
| ed25519-dalek | 3.0.0 | [02_repositorios/pdfcraft/crates/sign/Cargo.toml:39](../../../02_repositorios/pdfcraft/crates/sign/Cargo.toml) |
| name | pdfcraft-ui-egui | [02_repositorios/pdfcraft/crates/ui-egui/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/ui-egui/Cargo.toml) |
| rust-version | 1.95 | [02_repositorios/pdfcraft/crates/ui-egui/Cargo.toml:7](../../../02_repositorios/pdfcraft/crates/ui-egui/Cargo.toml) |
| bytemuck | 1 | [02_repositorios/pdfcraft/crates/ui-egui/Cargo.toml:7](../../../02_repositorios/pdfcraft/crates/ui-egui/Cargo.toml) |
| png | 0.18 | [02_repositorios/pdfcraft/crates/ui-egui/Cargo.toml:30](../../../02_repositorios/pdfcraft/crates/ui-egui/Cargo.toml) |
| base64 | 0.22 | [02_repositorios/pdfcraft/crates/ui-egui/Cargo.toml:31](../../../02_repositorios/pdfcraft/crates/ui-egui/Cargo.toml) |
| unicode-bidi | 0.3 | [02_repositorios/pdfcraft/crates/ui-egui/Cargo.toml:33](../../../02_repositorios/pdfcraft/crates/ui-egui/Cargo.toml) |
| name | pdfcraft-xfa | [02_repositorios/pdfcraft/crates/xfa/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/xfa/Cargo.toml) |
| roxmltree | 0.20 | [02_repositorios/pdfcraft/crates/xfa/Cargo.toml:16](../../../02_repositorios/pdfcraft/crates/xfa/Cargo.toml) |
| base64 | 0.22 | [02_repositorios/pdfcraft/crates/xfa/Cargo.toml:17](../../../02_repositorios/pdfcraft/crates/xfa/Cargo.toml) |
| png | 0.18 | [02_repositorios/pdfcraft/crates/xfa/Cargo.toml:18](../../../02_repositorios/pdfcraft/crates/xfa/Cargo.toml) |
| sha2 | 0.11 | [02_repositorios/pdfcraft/crates/xfa/Cargo.toml:19](../../../02_repositorios/pdfcraft/crates/xfa/Cargo.toml) |
| image | 0.25 | [02_repositorios/pdfcraft/crates/xfa/Cargo.toml:20](../../../02_repositorios/pdfcraft/crates/xfa/Cargo.toml) |
| name | pdfcraft-xfdf | [02_repositorios/pdfcraft/crates/xfdf/Cargo.toml:2](../../../02_repositorios/pdfcraft/crates/xfdf/Cargo.toml) |
| roxmltree | 0.20 | [02_repositorios/pdfcraft/crates/xfdf/Cargo.toml:16](../../../02_repositorios/pdfcraft/crates/xfdf/Cargo.toml) |
| name | xtask | [02_repositorios/pdfcraft/xtask/Cargo.toml:2](../../../02_repositorios/pdfcraft/xtask/Cargo.toml) |
| version | 0.1.0 | [02_repositorios/pdfcraft/xtask/Cargo.toml:3](../../../02_repositorios/pdfcraft/xtask/Cargo.toml) |
| edition | 2024 | [02_repositorios/pdfcraft/xtask/Cargo.toml:4](../../../02_repositorios/pdfcraft/xtask/Cargo.toml) |
| anyhow | 1 | [02_repositorios/pdfcraft/xtask/Cargo.toml:3](../../../02_repositorios/pdfcraft/xtask/Cargo.toml) |
| lopdf | 0.45 | [02_repositorios/pdfcraft/xtask/Cargo.toml:10](../../../02_repositorios/pdfcraft/xtask/Cargo.toml) |
| png | 0.18 | [02_repositorios/pdfcraft/xtask/Cargo.toml:11](../../../02_repositorios/pdfcraft/xtask/Cargo.toml) |
| serde_json | 1 | [02_repositorios/pdfcraft/xtask/Cargo.toml:3](../../../02_repositorios/pdfcraft/xtask/Cargo.toml) |
| serde | 1 | [02_repositorios/pdfcraft/xtask/Cargo.toml:3](../../../02_repositorios/pdfcraft/xtask/Cargo.toml) |
| sha2 | 0.11 | [02_repositorios/pdfcraft/xtask/Cargo.toml:14](../../../02_repositorios/pdfcraft/xtask/Cargo.toml) |
| toml | 1 | [02_repositorios/pdfcraft/xtask/Cargo.toml:3](../../../02_repositorios/pdfcraft/xtask/Cargo.toml) |

## Skills diretamente relacionadas

| Skill | Aplicação | Fonte |
| --- | --- | --- |
| [ci-quality-gate-engineer](../../../00_skills/(development)/ci-quality-gate-engineer/SKILL.md) | Necessidade observada: ci. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/pdfcraft/.github/workflows/ci.yml:1](../../../02_repositorios/pdfcraft/.github/workflows/ci.yml); [02_repositorios/pdfcraft/.github/workflows/freebsd.yml:1](../../../02_repositorios/pdfcraft/.github/workflows/freebsd.yml); [02_repositorios/pdfcraft/.github/workflows/packaging-lint.yml:1](../../../02_repositorios/pdfcraft/.github/workflows/packaging-lint.yml); [02_repositorios/pdfcraft/.github/workflows/release.yml:1](../../../02_repositorios/pdfcraft/.github/workflows/release.yml); [02_repositorios/pdfcraft/.github/workflows/windows-arm64.yml:1](../../../02_repositorios/pdfcraft/.github/workflows/windows-arm64.yml) |
| [deployment-pipeline-expert](../../../00_skills/(cloud)/deployment-pipeline-expert/SKILL.md) | Necessidade observada: ci. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/pdfcraft/.github/workflows/ci.yml:1](../../../02_repositorios/pdfcraft/.github/workflows/ci.yml); [02_repositorios/pdfcraft/.github/workflows/freebsd.yml:1](../../../02_repositorios/pdfcraft/.github/workflows/freebsd.yml); [02_repositorios/pdfcraft/.github/workflows/packaging-lint.yml:1](../../../02_repositorios/pdfcraft/.github/workflows/packaging-lint.yml); [02_repositorios/pdfcraft/.github/workflows/release.yml:1](../../../02_repositorios/pdfcraft/.github/workflows/release.yml); [02_repositorios/pdfcraft/.github/workflows/windows-arm64.yml:1](../../../02_repositorios/pdfcraft/.github/workflows/windows-arm64.yml) |
| [devops-pipeline-engineering](../../../00_skills/(cloud)/devops-pipeline-engineering/SKILL.md) | Necessidade observada: ci. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/pdfcraft/.github/workflows/ci.yml:1](../../../02_repositorios/pdfcraft/.github/workflows/ci.yml); [02_repositorios/pdfcraft/.github/workflows/freebsd.yml:1](../../../02_repositorios/pdfcraft/.github/workflows/freebsd.yml); [02_repositorios/pdfcraft/.github/workflows/packaging-lint.yml:1](../../../02_repositorios/pdfcraft/.github/workflows/packaging-lint.yml); [02_repositorios/pdfcraft/.github/workflows/release.yml:1](../../../02_repositorios/pdfcraft/.github/workflows/release.yml); [02_repositorios/pdfcraft/.github/workflows/windows-arm64.yml:1](../../../02_repositorios/pdfcraft/.github/workflows/windows-arm64.yml) |
| [evidence-integrity-engineer](../../../00_skills/(development)/evidence-integrity-engineer/SKILL.md) | Especialização adequada ao contrato/estrutura observados; ativar apenas na tarefa correspondente. | [02_repositorios/pdfcraft/crates/automation/README.md:3](../../../02_repositorios/pdfcraft/crates/automation/README.md); [02_repositorios/pdfcraft/crates/automation/src/lib.rs:168](../../../02_repositorios/pdfcraft/crates/automation/src/lib.rs) |
| [fixture-corpus-validator](../../../00_skills/(quality)/fixture-corpus-validator/SKILL.md) | Especialização adequada ao contrato/estrutura observados; ativar apenas na tarefa correspondente. | [02_repositorios/pdfcraft/crates/automation/README.md:3](../../../02_repositorios/pdfcraft/crates/automation/README.md); [02_repositorios/pdfcraft/crates/automation/src/lib.rs:168](../../../02_repositorios/pdfcraft/crates/automation/src/lib.rs) |
| [mcp-discovery](../../../00_skills/(tooling)/mcp-discovery/SKILL.md) | Necessidade observada: mcp. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/pdfcraft/crates/automation/README.md:3](../../../02_repositorios/pdfcraft/crates/automation/README.md) |
| [mcp-health-check](../../../00_skills/(tooling)/mcp-health-check/SKILL.md) | Necessidade observada: mcp. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/pdfcraft/crates/automation/README.md:3](../../../02_repositorios/pdfcraft/crates/automation/README.md) |
| [mcp-poisoning-evaluator](../../../00_skills/(security)/mcp-poisoning-evaluator/SKILL.md) | Necessidade observada: mcp. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/pdfcraft/crates/automation/README.md:3](../../../02_repositorios/pdfcraft/crates/automation/README.md) |
| [mcp-risk-controller](../../../00_skills/(tooling)/mcp-risk-controller/SKILL.md) | Necessidade observada: mcp. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/pdfcraft/crates/automation/README.md:3](../../../02_repositorios/pdfcraft/crates/automation/README.md) |
| [rust-expert](../../../00_skills/(development)/rust-expert/SKILL.md) | Necessidade observada: rust. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/pdfcraft/crates/automation/src/lib.rs:6](../../../02_repositorios/pdfcraft/crates/automation/src/lib.rs) |
| [supply-chain-auditor](../../../00_skills/(security)/supply-chain-auditor/SKILL.md) | Especialização adequada ao contrato/estrutura observados; ativar apenas na tarefa correspondente. | [02_repositorios/pdfcraft/crates/automation/README.md:3](../../../02_repositorios/pdfcraft/crates/automation/README.md); [02_repositorios/pdfcraft/crates/automation/src/lib.rs:168](../../../02_repositorios/pdfcraft/crates/automation/src/lib.rs) |
| [gh-fix-ci](../../../00_skills/(tooling)/gh-fix-ci/SKILL.md) | Necessidade observada: ci. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/pdfcraft/.github/workflows/ci.yml:1](../../../02_repositorios/pdfcraft/.github/workflows/ci.yml); [02_repositorios/pdfcraft/.github/workflows/freebsd.yml:1](../../../02_repositorios/pdfcraft/.github/workflows/freebsd.yml); [02_repositorios/pdfcraft/.github/workflows/packaging-lint.yml:1](../../../02_repositorios/pdfcraft/.github/workflows/packaging-lint.yml); [02_repositorios/pdfcraft/.github/workflows/release.yml:1](../../../02_repositorios/pdfcraft/.github/workflows/release.yml); [02_repositorios/pdfcraft/.github/workflows/windows-arm64.yml:1](../../../02_repositorios/pdfcraft/.github/workflows/windows-arm64.yml) |

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

125 arquivos candidatos por nome/caminho; não corresponde a quantidade de testes executados. 5 workflows encontrados. Suites não executadas.

- [02_repositorios/pdfcraft/.github/workflows/ci.yml:1](../../../02_repositorios/pdfcraft/.github/workflows/ci.yml)
- [02_repositorios/pdfcraft/.github/workflows/freebsd.yml:1](../../../02_repositorios/pdfcraft/.github/workflows/freebsd.yml)
- [02_repositorios/pdfcraft/.github/workflows/packaging-lint.yml:1](../../../02_repositorios/pdfcraft/.github/workflows/packaging-lint.yml)
- [02_repositorios/pdfcraft/.github/workflows/release.yml:1](../../../02_repositorios/pdfcraft/.github/workflows/release.yml)
- [02_repositorios/pdfcraft/.github/workflows/windows-arm64.yml:1](../../../02_repositorios/pdfcraft/.github/workflows/windows-arm64.yml)

## Lacunas

- Respeitar clean-room, allowlist de licenças e regras de atribuição antes de qualquer asset.
- Skills WCAG de web não validam automaticamente acessibilidade de PDF.
- MCP não deve ser habilitado automaticamente pelo mapeamento.
