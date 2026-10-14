# Verificação da instalação

Updated: 2026-10-13
Entry point: [catálogo](INDEX.md), [resultado reproduzível](validation.report.json).

Resultado atual: PASS, zero erros e zero avisos.

## Atualização das 77 novas imagens

302 pacotes canônicos, 305 entradas nativas e 827 SKILL.md com máximo de 99 linhas físicas. 2.872 links operativos resolvidos; 92 pacotes/777 recursos TLC preservados. As 77 imagens IMG_2700–IMG_2776 possuem ID/hash/OCR e revisão visual contabilizados em images.2026-10-13.manifest.json; o validador também confere esse lote e os recursos importados do Impeccable.
30 verificações reais de CLI/FFmpeg/Chromium passaram, além da sintaxe de 107 arquivos JavaScript. Build de call.json é determinístico; omissões, identidade não confirmada, HTML seguro, player offline/File API e busca por timestamp foram exercitados com fixture sintética. O gate rejeitou ID de foto duplicado e voltou a PASS após restauração byte-idêntica do manifesto.
Evidência e limites: [resultado final](photo-update-verification.json), [mudanças](PHOTO-UPDATE.md), [estrutura e material ausente](PHOTO-STRUCTURE.md). Não houve execução real de reconhecimento Whisper/qualidade Resemblyzer, instalação de motores/modelos/fontes ou conexão corporativa. Lentes sequenciais não equivalem a agentes independentes.

## Instalação anterior — referência histórica de 2026-10-12

Os números abaixo descrevem a migração original, preservada pela nova atualização.

| Contrato | Observação |
| --- | --- |
| Catálogo canônico | 301 skills em `00_skills/(categoria)/nome/`. |
| TLC completo | 92 pacotes e 777 arquivos de origem com SHA-256 preservado. |
| Fonte | `tech-leads-club/agent-skills`, commit `6df68d52028b9261058231e0f4998048c0352f45`. |
| Imagens | 770 IDs do Drive, 389 hashes únicos; IMG_2112–IMG_2500 em sequência. |
| Limite | 824 entradas SKILL.md inspecionadas; máximo físico de 99 linhas. |
| Módulos | 2.742 links locais operativos resolvidos; snapshots TLC preservados como fontes. |
| Descoberta | 301 IDs canônicas + três aliases em `.agents/skills/`; uma entrada existente de `.codex/skills/` atualizada. |
| Governança | Dono canônico `codenavi-agent`; 74 contratos AGENT.md antigos movidos para referências de lentes internas. |
| Recursos existentes | Todos os 1.467 recursos de 215 pacotes originais localizados; 195 recursos não Markdown com bytes preservados e dois com apenas adaptação de caminhos. |

Comando: `python "00_skills/(creation)/skill-factory/scripts/validate-workspace.py" --json-out 00_skills/validation.report.json`.

O validador do skill-architect também foi executado em todos os 301 pacotes. O limite desta missão é mais estrito que o limite original do TLC: conta o arquivo inteiro, não apenas o corpo.

A auditoria de preservação comparou os backups com os destinos, incluindo notas e contratos movidos para referências. Não encontrou recursos ausentes. As duas alterações não Markdown foram o mapa JSON de integração e o texto de retomada do tests-expert; a comparação confirmou que somente caminhos migrados e suas aspas de shell mudaram. O resumo está em `migration.manifest.json:resource_preservation`.

## Helpers e oracle

As CLIs `architecture-decision-record/scripts/adr_lint.mjs` e `architecture-decision-log/scripts/adl_index.mjs` foram executadas contra o mesmo fixture antes e depois da migração. Os scripts têm os mesmos bytes, ambas as versões saíram com código zero e produziram a mesma saída. O índice também exerce a importação relativa do parser de ADR após a mudança de pasta.

O tests-expert registrou PASS nas três verificações CLI congeladas a partir do pedido do usuário: limite/módulos, catálogo completo e inventário/ordem das imagens. Hash do charter: `372b714e0db6eec3f4cd39b0d20aea2f408858ec6c0a65ec831909a53e0c9cfd`. Saídas brutas e estado ficam no diretório ignorado `.tools/tlc-migration/`; este documento não contém fotos, OCR nem credenciais.

## Limites do resultado

- A análise de todas as imagens usou OCR e revisão estrutural/temática em sequência; amostras receberam inspeção visual adicional. Não houve comparação visual automatizada de cada linha fotografada.
- Fontes/logos binários não fornecidos pelas referências não foram inventados; report-design registra os tokens observados e exige os ativos oficiais quando necessários.
- A instalação das instruções não comprova disponibilidade de MCPs, provedores, autenticação ou infraestrutura. Esses requisitos devem ser verificados ao invocar a skill.
- As exclusões externas de `aeos/`, `runtime/`, `scripts/`, `templates/` e `references/` foram preservadas. O catálogo novo não restaura o runtime removido nem altera permissões externas.
