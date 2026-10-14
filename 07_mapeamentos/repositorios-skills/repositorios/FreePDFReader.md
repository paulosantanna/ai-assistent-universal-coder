# FreePDFReader — mapa estático de skills

Updated: 2026-10-13

Entry point: ../README.md

Tipo: Git próprio. Arquivos no inventário delimitado: 67; entradas excluídas: 3.

[Voltar ao índice](../README.md) · [Matriz completa](../matriz.csv)

## Dez dimensões

| Dimensão | Estado | Observação | Evidência |
| --- | --- | --- | --- |
| Tecnologias e versões | declarado | Declarações extraídas dos manifests, incluindo faixas e extras. Não são versões instaladas nem prova de compatibilidade. Lockfiles permanecem nas fontes para análise posterior. | [02_repositorios/FreePDFReader/Cargo.toml:11](../../../02_repositorios/FreePDFReader/Cargo.toml); [02_repositorios/FreePDFReader/Cargo.toml:12](../../../02_repositorios/FreePDFReader/Cargo.toml); [02_repositorios/FreePDFReader/Cargo.toml:21](../../../02_repositorios/FreePDFReader/Cargo.toml); demais fontes em mapa.json/declarações abaixo |
| Arquitetura | observado | Workspace Cargo separa core, UI, AI e xtask; eframe/egui, PDFium e ONNX são dependências declaradas. | [02_repositorios/FreePDFReader/Cargo.toml:6](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| Propósito | declarado | Leitor PDF nativo multiplataforma com resumo, perguntas e tradução por IA local. | [02_repositorios/FreePDFReader/README.md:3](../../../02_repositorios/FreePDFReader/README.md) |
| Fluxo | observado | CLI/GUI inicializa a aplicação; Document::open conecta à biblioteca PDFium e abre arquivo. | [02_repositorios/FreePDFReader/crates/freepdfreader-core/src/document.rs:48](../../../02_repositorios/FreePDFReader/crates/freepdfreader-core/src/document.rs) |
| Dados | observado | Documento expõe metadados, páginas e índice de busca local. | [02_repositorios/FreePDFReader/crates/freepdfreader-core/src/document.rs:138](../../../02_repositorios/FreePDFReader/crates/freepdfreader-core/src/document.rs) |
| Configuração/deploy | documentado | Pacote portátil requer pdfium.dll e onnxruntime.dll segundo documentação. | [02_repositorios/FreePDFReader/PORTABLE.md:45](../../../02_repositorios/FreePDFReader/PORTABLE.md) |
| Operação/observabilidade | observado | Entrypoint oferece informações de versão; inferência e renderização não foram executadas. | [02_repositorios/FreePDFReader/src/main.rs:267](../../../02_repositorios/FreePDFReader/src/main.rs) |
| Interfaces/dependências | observado | Engine de IA usa modelos ONNX locais de resumo, QA e tradução. | [02_repositorios/FreePDFReader/crates/freepdfreader-ai/src/engine.rs:84](../../../02_repositorios/FreePDFReader/crates/freepdfreader-ai/src/engine.rs) |
| Vulnerabilidades | não verificado | Nenhuma consulta atual a advisories/scanner foi executada; não equivale a ausência de CVEs. | Sem verificação nesta missão |
| Obsolescência | não verificado | Datas de suporte/EOL não consultadas. Versões declaradas não comprovam suporte atual. | Sem verificação nesta missão |

## Declarações dos manifests

Faixas e extras são preservados; versões instaladas/resolvidas não foram verificadas.

| Declaração | Valor | Fonte |
| --- | --- | --- |
| version | 0.1.0 | [02_repositorios/FreePDFReader/Cargo.toml:11](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| edition | 2024 | [02_repositorios/FreePDFReader/Cargo.toml:12](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| pdfium-render | 0.9 | [02_repositorios/FreePDFReader/Cargo.toml:21](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| tokio | 1.40 | [02_repositorios/FreePDFReader/Cargo.toml:22](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| serde | 1.0 | [02_repositorios/FreePDFReader/Cargo.toml:11](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| serde_json | 1.0 | [02_repositorios/FreePDFReader/Cargo.toml:11](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| thiserror | 1.0 | [02_repositorios/FreePDFReader/Cargo.toml:11](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| anyhow | 1.0 | [02_repositorios/FreePDFReader/Cargo.toml:11](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| tracing | 0.1 | [02_repositorios/FreePDFReader/Cargo.toml:11](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| tracing-subscriber | 0.3 | [02_repositorios/FreePDFReader/Cargo.toml:28](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| dirs | 5.0 | [02_repositorios/FreePDFReader/Cargo.toml:29](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| once_cell | 1.19 | [02_repositorios/FreePDFReader/Cargo.toml:30](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| parking_lot | 0.12 | [02_repositorios/FreePDFReader/Cargo.toml:31](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| blake3 | 1.5 | [02_repositorios/FreePDFReader/Cargo.toml:32](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| num_cpus | 1.16 | [02_repositorios/FreePDFReader/Cargo.toml:33](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| chrono | 0.4 | [02_repositorios/FreePDFReader/Cargo.toml:34](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| ort | 2.0.0-rc.13 | [02_repositorios/FreePDFReader/Cargo.toml:37](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| tokenizers | 0.19 | [02_repositorios/FreePDFReader/Cargo.toml:38](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| ndarray | 0.16 | [02_repositorios/FreePDFReader/Cargo.toml:39](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| egui | 0.30 | [02_repositorios/FreePDFReader/Cargo.toml:42](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| eframe | 0.30 | [02_repositorios/FreePDFReader/Cargo.toml:42](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| egui_extras | 0.30 | [02_repositorios/FreePDFReader/Cargo.toml:42](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| arboard | 3.6 | [02_repositorios/FreePDFReader/Cargo.toml:45](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| rfd | 0.13 | [02_repositorios/FreePDFReader/Cargo.toml:46](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| image | 0.24 | [02_repositorios/FreePDFReader/Cargo.toml:47](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| clap | 4.5 | [02_repositorios/FreePDFReader/Cargo.toml:50](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| criterion | 0.5 | [02_repositorios/FreePDFReader/Cargo.toml:53](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| tempfile | 3.8 | [02_repositorios/FreePDFReader/Cargo.toml:54](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| predicates | 3.0 | [02_repositorios/FreePDFReader/Cargo.toml:55](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| cargo-bundle | 0.6 | [02_repositorios/FreePDFReader/Cargo.toml:58](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| which | 5.0 | [02_repositorios/FreePDFReader/Cargo.toml:29](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| walkdir | 2.4 | [02_repositorios/FreePDFReader/Cargo.toml:60](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| zip | 0.6 | [02_repositorios/FreePDFReader/Cargo.toml:58](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| reqwest | 0.12 | [02_repositorios/FreePDFReader/Cargo.toml:31](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| indicatif | 0.17 | [02_repositorios/FreePDFReader/Cargo.toml:63](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| semver | 1.0 | [02_repositorios/FreePDFReader/Cargo.toml:11](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| toml | 0.8 | [02_repositorios/FreePDFReader/Cargo.toml:65](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| toml_edit | 0.22 | [02_repositorios/FreePDFReader/Cargo.toml:66](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| sha2 | 0.10 | [02_repositorios/FreePDFReader/Cargo.toml:67](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| flume | 0.11 | [02_repositorios/FreePDFReader/Cargo.toml:68](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| otel | 0.25 | [02_repositorios/FreePDFReader/Cargo.toml:71](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| otel-sdk | 0.25 | [02_repositorios/FreePDFReader/Cargo.toml:71](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| tracing-opentelemetry | 0.5 | [02_repositorios/FreePDFReader/Cargo.toml:53](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| name | freepdfreader-ai | [02_repositorios/FreePDFReader/crates/freepdfreader-ai/Cargo.toml:2](../../../02_repositorios/FreePDFReader/crates/freepdfreader-ai/Cargo.toml) |
| sha2 | 0.10 | [02_repositorios/FreePDFReader/crates/freepdfreader-ai/Cargo.toml:27](../../../02_repositorios/FreePDFReader/crates/freepdfreader-ai/Cargo.toml) |
| lru | 0.10 | [02_repositorios/FreePDFReader/crates/freepdfreader-ai/Cargo.toml:27](../../../02_repositorios/FreePDFReader/crates/freepdfreader-ai/Cargo.toml) |
| indicatif | 0.17 | [02_repositorios/FreePDFReader/crates/freepdfreader-ai/Cargo.toml:29](../../../02_repositorios/FreePDFReader/crates/freepdfreader-ai/Cargo.toml) |
| async-trait | 0.1 | [02_repositorios/FreePDFReader/crates/freepdfreader-ai/Cargo.toml:27](../../../02_repositorios/FreePDFReader/crates/freepdfreader-ai/Cargo.toml) |
| futures | 0.3 | [02_repositorios/FreePDFReader/crates/freepdfreader-ai/Cargo.toml:31](../../../02_repositorios/FreePDFReader/crates/freepdfreader-ai/Cargo.toml) |
| tokio-util | 0.7 | [02_repositorios/FreePDFReader/crates/freepdfreader-ai/Cargo.toml:32](../../../02_repositorios/FreePDFReader/crates/freepdfreader-ai/Cargo.toml) |
| byteorder | 1.5 | [02_repositorios/FreePDFReader/crates/freepdfreader-ai/Cargo.toml:33](../../../02_repositorios/FreePDFReader/crates/freepdfreader-ai/Cargo.toml) |
| half | 2.4 | [02_repositorios/FreePDFReader/crates/freepdfreader-ai/Cargo.toml:34](../../../02_repositorios/FreePDFReader/crates/freepdfreader-ai/Cargo.toml) |
| name | freepdfreader-core | [02_repositorios/FreePDFReader/crates/freepdfreader-core/Cargo.toml:2](../../../02_repositorios/FreePDFReader/crates/freepdfreader-core/Cargo.toml) |
| name | freepdfreader-ui | [02_repositorios/FreePDFReader/crates/freepdfreader-ui/Cargo.toml:2](../../../02_repositorios/FreePDFReader/crates/freepdfreader-ui/Cargo.toml) |
| rfd | 0.13 | [02_repositorios/FreePDFReader/crates/freepdfreader-ui/Cargo.toml:27](../../../02_repositorios/FreePDFReader/crates/freepdfreader-ui/Cargo.toml) |
| name | xtask | [02_repositorios/FreePDFReader/crates/xtask/Cargo.toml:2](../../../02_repositorios/FreePDFReader/crates/xtask/Cargo.toml) |
| reqwest | 0.12 | [02_repositorios/FreePDFReader/crates/xtask/Cargo.toml:22](../../../02_repositorios/FreePDFReader/crates/xtask/Cargo.toml) |
| clap | 4.5 | [02_repositorios/FreePDFReader/crates/xtask/Cargo.toml:23](../../../02_repositorios/FreePDFReader/crates/xtask/Cargo.toml) |
| indicatif | 0.17 | [02_repositorios/FreePDFReader/crates/xtask/Cargo.toml:24](../../../02_repositorios/FreePDFReader/crates/xtask/Cargo.toml) |
| semver | 1.0 | [02_repositorios/FreePDFReader/crates/xtask/Cargo.toml:26](../../../02_repositorios/FreePDFReader/crates/xtask/Cargo.toml) |
| toml | 0.8 | [02_repositorios/FreePDFReader/crates/xtask/Cargo.toml:27](../../../02_repositorios/FreePDFReader/crates/xtask/Cargo.toml) |
| toml_edit | 0.22 | [02_repositorios/FreePDFReader/crates/xtask/Cargo.toml:28](../../../02_repositorios/FreePDFReader/crates/xtask/Cargo.toml) |
| sha2 | 0.10 | [02_repositorios/FreePDFReader/crates/xtask/Cargo.toml:29](../../../02_repositorios/FreePDFReader/crates/xtask/Cargo.toml) |
| flume | 0.11 | [02_repositorios/FreePDFReader/crates/xtask/Cargo.toml:30](../../../02_repositorios/FreePDFReader/crates/xtask/Cargo.toml) |

## Skills diretamente relacionadas

| Skill | Aplicação | Fonte |
| --- | --- | --- |
| [ai-architecture-expert](../../../00_skills/(architecture)/ai-architecture-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/FreePDFReader/README.md:3](../../../02_repositorios/FreePDFReader/README.md) |
| [ai-engineering-expert](../../../00_skills/(development)/ai-engineering-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/FreePDFReader/README.md:3](../../../02_repositorios/FreePDFReader/README.md) |
| [ai-evals-expert](../../../00_skills/(quality)/ai-evals-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/FreePDFReader/README.md:3](../../../02_repositorios/FreePDFReader/README.md) |
| [anti-hallucination-evaluator](../../../00_skills/(quality)/anti-hallucination-evaluator/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/FreePDFReader/README.md:3](../../../02_repositorios/FreePDFReader/README.md) |
| [ci-quality-gate-engineer](../../../00_skills/(development)/ci-quality-gate-engineer/SKILL.md) | Necessidade observada: ci. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/FreePDFReader/.github/workflows/ci.yml:1](../../../02_repositorios/FreePDFReader/.github/workflows/ci.yml); [02_repositorios/FreePDFReader/.github/workflows/release.yml:1](../../../02_repositorios/FreePDFReader/.github/workflows/release.yml) |
| [deployment-pipeline-expert](../../../00_skills/(cloud)/deployment-pipeline-expert/SKILL.md) | Necessidade observada: ci. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/FreePDFReader/.github/workflows/ci.yml:1](../../../02_repositorios/FreePDFReader/.github/workflows/ci.yml); [02_repositorios/FreePDFReader/.github/workflows/release.yml:1](../../../02_repositorios/FreePDFReader/.github/workflows/release.yml) |
| [devops-pipeline-engineering](../../../00_skills/(cloud)/devops-pipeline-engineering/SKILL.md) | Necessidade observada: ci. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/FreePDFReader/.github/workflows/ci.yml:1](../../../02_repositorios/FreePDFReader/.github/workflows/ci.yml); [02_repositorios/FreePDFReader/.github/workflows/release.yml:1](../../../02_repositorios/FreePDFReader/.github/workflows/release.yml) |
| [llm-model-selection-expert](../../../00_skills/(development)/llm-model-selection-expert/SKILL.md) | Necessidade observada: ai. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/FreePDFReader/README.md:3](../../../02_repositorios/FreePDFReader/README.md) |
| [rust-expert](../../../00_skills/(development)/rust-expert/SKILL.md) | Necessidade observada: rust. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/FreePDFReader/Cargo.toml:6](../../../02_repositorios/FreePDFReader/Cargo.toml) |
| [gh-fix-ci](../../../00_skills/(tooling)/gh-fix-ci/SKILL.md) | Necessidade observada: ci. Usar na tarefa correspondente, respeitando o contrato da skill. | [02_repositorios/FreePDFReader/.github/workflows/ci.yml:1](../../../02_repositorios/FreePDFReader/.github/workflows/ci.yml); [02_repositorios/FreePDFReader/.github/workflows/release.yml:1](../../../02_repositorios/FreePDFReader/.github/workflows/release.yml) |

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

4 arquivos candidatos por nome/caminho; não corresponde a quantidade de testes executados. 2 workflows encontrados. Suites não executadas.

- [02_repositorios/FreePDFReader/.github/workflows/ci.yml:1](../../../02_repositorios/FreePDFReader/.github/workflows/ci.yml)
- [02_repositorios/FreePDFReader/.github/workflows/release.yml:1](../../../02_repositorios/FreePDFReader/.github/workflows/release.yml)

## Lacunas

- README diz Rust 1.80+ mas Cargo declara edição 2024; compatibilidade não validada.
- Modelos, DLLs e funcionamento de inferência não verificados.
- RAG e fine-tuning não inferidos apenas por haver QA local.
