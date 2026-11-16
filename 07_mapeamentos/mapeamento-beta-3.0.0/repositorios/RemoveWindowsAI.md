# RemoveWindowsAI — beta 3.0.0

Updated: 2026-10-27
Entry point: [índice](../README.md) · [mapa estruturado](../mapa.json)

Arquivos com hash: 10; fingerprint: `83267aaa8c8a882ad3250275696e53faeb91b6bc327dfda34a3ba18109f1696f`.
Git próprio: True; HEAD: `fd90ea37fb6102fa198d1592c59564ceba796494`; branch: `main`.
Estado local: limpo; detalhes em inventory.json.

## Atualizações e reconciliação

Scripts e documentação do Windows permanecem leitura estática; nenhum efeito no SO ou binário foi exercitado.

## Dimensões e evidências

### Propósito

**declarado** — Utilitário para desativar/remover recursos de IA do Windows e ajustar políticas/pacotes.

[RemoveWindowsAI/README.md:1](../../../02_repositorios/RemoveWindowsAI/README.md)

### Arquitetura

**documentado** — Dois scripts PowerShell e payloads Windows; documentação descreve execução via TrustedInstaller.

[RemoveWindowsAI/Documentation.md:23](../../../02_repositorios/RemoveWindowsAI/Documentation.md)

### Fluxo

**observado** — Script verifica versão PowerShell e oferece opções de alteração do sistema; cleanup usa execução elevada.

[RemoveWindowsAI/RemoveWindowsAi.ps1:51](../../../02_repositorios/RemoveWindowsAI/RemoveWindowsAi.ps1)

### Dados

**documentado** — Registro Windows, pacotes Appx e backups são o estado manipulado; não é corpus de IA.

[RemoveWindowsAI/Documentation.md:51](../../../02_repositorios/RemoveWindowsAI/Documentation.md)

### Interfaces

**observado** — Usa privilégios de backup/restore e processo TrustedInstaller; alterações têm impacto elevado no SO.

[RemoveWindowsAI/RemoveAI-UpdateCleanup.ps1:65](../../../02_repositorios/RemoveWindowsAI/RemoveAI-UpdateCleanup.ps1)

### Configuração/deploy

**observado** — Script exige Windows PowerShell 5.1; pacote de aplicação e binários acompanham o diretório.

[RemoveWindowsAI/RemoveWindowsAi.ps1:51](../../../02_repositorios/RemoveWindowsAI/RemoveWindowsAi.ps1)

### Operação

**observado** — Cleanup escreve status de falhas de parada do TrustedInstaller; não executado.

[RemoveWindowsAI/RemoveAI-UpdateCleanup.ps1:147](../../../02_repositorios/RemoveWindowsAI/RemoveAI-UpdateCleanup.ps1)

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


### Vulnerabilidades

**não verificado** — Sem consulta de CVE/EOL nesta missão.


### Obsolescência

**não verificado** — Sem consulta de CVE/EOL nesta missão.


## Declarações de versão

| Manifest / declaração | Valor | Evidência |
|---|---|---|

## Qualidade e limites

Workflows: 0; arquivos candidatos a testes: 0. Não executados.

- Amostra semântica seletiva; hash e busca textual não equivalem a auditoria integral.
- Nenhum runtime, treino, publicação ou sincronização remota executado.
- Fontes modificadas/não rastreadas fazem parte deste snapshot local.
