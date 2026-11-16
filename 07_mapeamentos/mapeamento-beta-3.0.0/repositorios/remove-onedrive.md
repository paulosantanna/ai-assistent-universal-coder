# remove-onedrive — beta 3.0.0

Updated: 2026-10-27
Entry point: [índice](../README.md) · [mapa estruturado](../mapa.json)

Arquivos com hash: 3; fingerprint: `29e0bb104b5dc3b2f8e30cb7343cb17cbe66ff6d3f7b7e79f400fb9cfb8bb4c5`.
Git próprio: True; HEAD: `4066b4a29281ebecde06cc2c9bc1c9418195217d`; branch: `main`.
Estado local: limpo; detalhes em inventory.json.

## Atualizações e reconciliação

Utilitário de remoção de alto impacto permanece apenas lido; não confundir presença de IA no nome de outros projetos com pipeline LLM.

## Dimensões e evidências

### Propósito

**declarado** — Utilitário para remover OneDrive e restaurar controle local de pastas no Windows.

[remove-onedrive/README.md:1](../../../02_repositorios/remove-onedrive/README.md)

### Arquitetura

**observado** — Script PowerShell monolítico com funções de log, elevação, backup e restauração; não é servidor.

[remove-onedrive/Remove-OneDrive.ps1:129](../../../02_repositorios/remove-onedrive/Remove-OneDrive.ps1)

### Fluxo

**observado** — Localiza pastas e oferece backup antes da remoção; nenhuma operação de remoção foi executada.

[remove-onedrive/Remove-OneDrive.ps1:179](../../../02_repositorios/remove-onedrive/Remove-OneDrive.ps1)

### Dados

**observado** — Arquivos/pastas do perfil e backups são dados operacionais; risco de dados deve ser avaliado antes de executar.

[remove-onedrive/Remove-OneDrive.ps1:159](../../../02_repositorios/remove-onedrive/Remove-OneDrive.ps1)

### Interfaces

**documentado** — Interage com sistema operacional e OneDrive; não foi identificado contrato HTTP/DB no escopo lido.

[remove-onedrive/Remove-OneDrive.ps1:7](../../../02_repositorios/remove-onedrive/Remove-OneDrive.ps1)

### Configuração/deploy

**documentado** — Execução Windows com elevação programática documentada no script.

[remove-onedrive/Remove-OneDrive.ps1:69](../../../02_repositorios/remove-onedrive/Remove-OneDrive.ps1)

### Operação

**observado** — Write-Log usa arquivo e há ErrorActionPreference=Continue; continuar após erro exige revisão específica.

[remove-onedrive/Remove-OneDrive.ps1:75](../../../02_repositorios/remove-onedrive/Remove-OneDrive.ps1)

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
