# FreePDFReader — beta 3.0.0

Updated: 2026-10-27
Entry point: [índice](../README.md) · [mapa estruturado](../mapa.json)

Arquivos com hash: 56; fingerprint: `59d1bd161554a75d5ba08de82bb37fd640dd01b8fd70625f4a9cf090c0985cc9`.
Git próprio: True; HEAD: `{'error': 'git_exit_128'}`; branch: `master`.
Estado local: há alterações/não rastreados; detalhes em inventory.json.

## Atualizações e reconciliação

Diretório tem .git, mas HEAD não resolvido e arquivos não rastreados. Não atribuir commit ou versão de release a esse estado.

## Dimensões e evidências

### Propósito

**declarado** — Leitor PDF nativo multiplataforma com resumo, perguntas e tradução por IA local.

[FreePDFReader/README.md:3](../../../02_repositorios/FreePDFReader/README.md)

### Arquitetura

**observado** — Workspace Cargo separa core, UI, AI e xtask; eframe/egui, PDFium e ONNX são dependências declaradas.

[FreePDFReader/Cargo.toml:6](../../../02_repositorios/FreePDFReader/Cargo.toml)

### Fluxo

**observado** — CLI/GUI inicializa a aplicação; Document::open conecta à biblioteca PDFium e abre arquivo.

[FreePDFReader/crates/freepdfreader-core/src/document.rs:48](../../../02_repositorios/FreePDFReader/crates/freepdfreader-core/src/document.rs)

### Dados

**observado** — Documento expõe metadados, páginas e índice de busca local.

[FreePDFReader/crates/freepdfreader-core/src/document.rs:138](../../../02_repositorios/FreePDFReader/crates/freepdfreader-core/src/document.rs)

### Interfaces

**observado** — Engine de IA usa modelos ONNX locais de resumo, QA e tradução.

[FreePDFReader/crates/freepdfreader-ai/src/engine.rs:84](../../../02_repositorios/FreePDFReader/crates/freepdfreader-ai/src/engine.rs)

### Configuração/deploy

**documentado** — Pacote portátil requer pdfium.dll e onnxruntime.dll segundo documentação.

[FreePDFReader/PORTABLE.md:45](../../../02_repositorios/FreePDFReader/PORTABLE.md)

### Operação

**observado** — Entrypoint oferece informações de versão; inferência e renderização não foram executadas.

[FreePDFReader/src/main.rs:267](../../../02_repositorios/FreePDFReader/src/main.rs)

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

[FreePDFReader/Cargo.toml:4](../../../02_repositorios/FreePDFReader/Cargo.toml)
[FreePDFReader/crates/freepdfreader-ai/Cargo.toml:2](../../../02_repositorios/FreePDFReader/crates/freepdfreader-ai/Cargo.toml)
[FreePDFReader/crates/freepdfreader-core/Cargo.toml:2](../../../02_repositorios/FreePDFReader/crates/freepdfreader-core/Cargo.toml)
[FreePDFReader/crates/freepdfreader-ui/Cargo.toml:2](../../../02_repositorios/FreePDFReader/crates/freepdfreader-ui/Cargo.toml)
[FreePDFReader/crates/xtask/Cargo.toml:2](../../../02_repositorios/FreePDFReader/crates/xtask/Cargo.toml)

### Vulnerabilidades

**não verificado** — Sem consulta de CVE/EOL nesta missão.


### Obsolescência

**não verificado** — Sem consulta de CVE/EOL nesta missão.


## Declarações de versão

| Manifest / declaração | Valor | Evidência |
|---|---|---|
| name | freepdfreader | [FreePDFReader/Cargo.toml:4](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| name | freepdfreader-ai | [FreePDFReader/crates/freepdfreader-ai/Cargo.toml:2](../../../02_repositorios/FreePDFReader/crates/freepdfreader-ai/Cargo.toml) |
| name | freepdfreader-core | [FreePDFReader/crates/freepdfreader-core/Cargo.toml:2](../../../02_repositorios/FreePDFReader/crates/freepdfreader-core/Cargo.toml) |
| name | freepdfreader-ui | [FreePDFReader/crates/freepdfreader-ui/Cargo.toml:2](../../../02_repositorios/FreePDFReader/crates/freepdfreader-ui/Cargo.toml) |
| name | xtask | [FreePDFReader/crates/xtask/Cargo.toml:2](../../../02_repositorios/FreePDFReader/crates/xtask/Cargo.toml) |

## Qualidade e limites

Workflows: 2; arquivos candidatos a testes: 4. Não executados.

- Amostra semântica seletiva; hash e busca textual não equivalem a auditoria integral.
- Nenhum runtime, treino, publicação ou sincronização remota executado.
- Fontes modificadas/não rastreadas fazem parte deste snapshot local.
