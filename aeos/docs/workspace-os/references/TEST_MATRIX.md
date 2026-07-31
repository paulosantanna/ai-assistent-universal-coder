# Matriz de verificação do Workspace OS

Execução: `workspace-os-token-control-20260724`

Ambiente: Windows, Python 3.14.5, SQLite da biblioteca-padrão.

Estado da ADR no momento da execução: `PROPOSED`; aceite depende do JUDGE final.

## Resultados do diff final

| Categoria | Aplicabilidade | Resultado | Evidência |
|---|---|---|---|
| Import, compilação e startup | REQUIRED | PASS | `compileall`; CLI `version`, `plan`, `status` com exit 0 |
| Packaging e instalação | NOT_APPLICABLE | N/A | nenhum manifest, entrypoint ou dependência foi alterado |
| Formatação, lint, tipos e estática do slice | REQUIRED | PASS | Ruff e Bandit com exit 0; mypy isolado com `--follow-imports=skip` passou em 19 arquivos; compileall com exit 0 |
| Grafo global de imports no mypy | REQUIRED | FAIL | 57 erros legados fora do slice em 18 arquivos; resultado preservado e impede readiness global |
| Arquitetura | REQUIRED | PASS | namespace strangler isolado; ADR-0001; sem imports de runtimes legados |
| Unitário, componente e contrato | REQUIRED | PASS | suíte focada: 139 testes |
| API e end-to-end local | REQUIRED | PASS | parser CLI → kernel → SQLite → status/replay |
| Regressão Python AEOS | REQUIRED | PASS | `608 passed in 90.92s` |
| Positivo, negativo, limite e erro | REQUIRED | PASS | transições, DAG, budgets, JSON, IDs, overflow e falha fechada |
| Adversarial | REQUIRED | PASS | claim autoatestada, famílias de segredos, texto/proveniência sensíveis, tamper, exclusão e rehash recusados |
| Property-based e diferencial | REQUIRED | PASS | ordem do DAG e conservação do ledger; replay versus materialização |
| Concorrência, race e CAS | REQUIRED | PASS | última reserva e transição concorrente; apenas um commit vence; status usa um único snapshot SQLite |
| Segurança de input e persistência | REQUIRED | PASS | Bandit; confinement; IDs; limite 1 MiB; detector central recusa chaves, texto e proveniência sensíveis |
| Dependência e supply chain | NOT_APPLICABLE | N/A | nenhuma dependência nova ou atualizada |
| Performance, volume e recursos | REQUIRED | PASS | DAG de 500 tarefas; sem vazamentos com `ResourceWarning` como erro |
| Stress, spike, endurance e soak | NOT_APPLICABLE | N/A | slice não é serviço contínuo nem executa providers |
| Retry, timeout, backpressure e failover | NOT_APPLICABLE | N/A | nenhuma integração remota ou fila neste slice |
| Crash, rollback, reopen e recovery | REQUIRED | PASS | rollback transacional, `synchronous=FULL`, WAL e reopen testados |
| Schema, integridade, replay e compatibilidade | REQUIRED | PASS | schema, quick-check, hash-chain/head, replay e CLI antiga preservada |
| Migração forward/backward | NOT_APPLICABLE | N/A | banco novo; sem migração ou dual-write de estado legado |
| Windows/Python 3.14 | REQUIRED | PASS | testes, regressão e smokes comprovados no ambiente registrado |
| Linux e macOS | REQUIRED | NOT_RUN | ambientes indisponíveis nesta execução; compatibilidade permanece não verificada |
| Browser, dispositivo, visual e acessibilidade | NOT_APPLICABLE | N/A | saída CLI JSON sem UI |
| Usabilidade/manual exploratório | REQUIRED | PASS | `plan` e `status` executados manualmente com saída idêntica persistida |
| Logs, auditoria, health e redaction | REQUIRED | PASS | eventos atômicos, hash-chain, head/count, replay e secret-key gate |
| Provider, MCP, rede e E2E de modelo | NOT_APPLICABLE | N/A | explicitamente fora do trust boundary do slice |

Cobertura do novo kernel: `91%` (`846` statements, `76` não cobertos).
Cobertura é indicador, não substitui os testes comportamentais.

## Verificador global do repositório

`verify.py --suite full` continua `FAIL`, preservado sem reclassificação. O core
novo passou, mas o baseline global mantém bloqueadores fora deste slice:

- `src/src` e artefatos/pycache detectados pelo structural guard;
- benchmark legado `scanner_pruned` acima do budget;
- hashes obsoletos do `skills/skill-factory/MANIFEST.json`;
- packages MCP e LSP ausentes no ambiente;
- runtime Node não localizado pelo subprocesso do verificador.

Isso impede declarar o AEOS integral production-ready, mas não altera o resultado
determinístico da regressão do namespace novo.

## Evidência reproduzível

Logs, exit codes, versões e hashes SHA-256 estão em:

`.aeos/evidence/workspace-os-token-control-20260724/`

O diretório contém também todas as tentativas anteriores, inclusive falhas de
taxonomia de teste, health-check Hypothesis e o `verify.py full` bloqueado.
