# Playbook — Fábrica de Documentários (documentary-factory)

Updated: 2026-10-31. Entry point: [`studio.py`](studio.py). Super-skill: [`documentary-factory`](../00_skills/(tooling)/documentary-factory/SKILL.md). Owner: codenavi-agent. Herda `AGENTS.md` e CodENavi Full Workspace v2. Papéis especializados são skills, nunca identidades adicionais.

Objetivo: tema → evidência → enredo → assets → voz → render → mix → gates → juiz adversarial → entrega local. Sem publicação automática. Falha de motor, licença ou fonte bloqueia a etapa dependente e preserva o trabalho válido das etapas anteriores.

Este playbook é o sucessor operacional de [`PLAYBOOK.md`](PLAYBOOK.md). O contrato de projeto (`project.json`), a CLI (`studio.py`) e o compositor são os mesmos; o que muda é a **fábrica de papéis**, o **juiz adversarial com limiar** e o **loop de reinício**.

## Os seis papéis obrigatórios

Cada papel é um contrato de trabalho executado como unidade de sessão com contexto próprio. O papel 6 é instanciado com contexto **virgem**.

| # | Papel | Skill | Entrega | Gate de saída |
|---|---|---|---|---|
| 1 | Aquisição de áudio sem copyright | `documentary-music-curator` | `license-ledger.json` + faixas | licença por URL real; sem canal autodeclarado |
| 2 | Engenharia de áudio (calma) | `documentary-audio-engineer` | mix tratado + medições | -16 LUFS / -1.5 dBTP; 0 silêncio > 2 s |
| 3 | Audiovisual sem marca d'água | `documentary-visual-curator` | `sourcing-ledger.json` + assets | inspeção visual real; licença por arquivo |
| 4 | Vídeo para internet | `documentary-social-video-expert` | `social/plan.json` + `metadata.md` | capítulos somam a duração; limites citados |
| 5 | Especialista do assunto | `documentary-subject-expert` | `sources.json` + arco + cenas | claim ↔ fonte; palavras/cena na faixa |
| 6 | Juiz adversarial (The-Fool) | `documentary-adversarial-judge` | veredito com 6 notas + evidência | todas as dimensões ≥ 9,5 |

## Perfis

| Perfil | Duração | Canvas | Destino editorial |
| --- | --- | --- | --- |
| short | 60 s | 1080×1920 / 30 fps | TikTok, Shorts, Reels |
| youtube | 600 s | 1920×1080 / 30 fps | YouTube |
| documentary | 3600 s | 1920×1080 / 30 fps | Documentário |
| full-documentary | 5400 s | 1920×1080 / 30 fps | Documentário longo |

Padrão editorial do operador: **90 min em 1920×1080 paisagem**, com música calma sempre presente.

## Regras invioláveis do operador

1. NUNCA imagem/GIF/vídeo de jogos, filmes ou séries.
2. SEMPRE música de fundo calma; nunca abafar o narrador.
3. SEM trechos mudos; a narração preenche a cena.
4. Imagens sempre no tema, na orientação correta; NUNCA espelhar/rotacionar/reposicionar asset para disfarçar reuso.
5. Toda validação (vídeo, imagem, áudio) passa por papel com EVIDÊNCIA real.
6. Todo vídeo é salvo em `D:\Git\dark-videos`.
7. **PROIBIDO qualquer frame visual fora do contexto do roteiro** — travado pelo GATE 3 (`context_gate.py`), falha fechada, sem bypass (2026-11-08).

## Modo canal dark (sem rosto, sem voz própria, 100% IA)

O pipeline já é nativo de canal dark; nenhum material do criador entra no vídeo:

- **Roteiro 100% IA**: `providers.py script` (LLM local via Ollama) — sem rascunho humano.
- **Narração 100% IA**: `voice_kokoro.py` (Kokoro PT-BR local) ou `voice_google.py`; a voz do criador nunca é usada e não há clonagem de terceiros.
- **Sem rosto exigido**: `speech_balloons: false` é obrigatório no contrato e visuais são gerados por IA (`providers.py assets`) ou curados com licença (`build_layers.py`); nada do operador aparece.
- **Trava de contexto visual**: toda camada de toda cena precisa provar vínculo com o roteiro — ver próxima seção.

## Execução

1. **BRIEFING/RECON**: ler `.notebook/` e este playbook; rodar `python science-studio/studio.py doctor`. Confirmar TTS local, geração de imagem e FFmpeg; nunca prometer motor não verificado.
2. **PLAN**: congelar domínio, arco de capítulos e orçamento de palavras. Para 60 s: 108–136 palavras. Gerar em lotes exige outline global prévio.
3. **Evidência (papel 5)**: `sources.json` com `id/title/url/publisher/accessed/excerpt`. Fonte não verificada é descartada, nunca preenchida.
4. **Enredo (papel 5)**: cenas com `narration`, `visual`, `duration`, `claims`, `transition`, `sd_prompt`. Cena = um fenômeno.
5. **Assets (papel 3)**: buscar em acervo com licença explícita, inspecionar o arquivo baixado, rejeitar marca d'água/logo/texto falso/gameplay, registrar licença. Arte local gerada cobre lacuna declarada.
6. **Trilha (papel 1)**: licença verificável por faixa; medir caráter calmo e duração; capturar atribuição exigida; fallback declarado é a trilha procedural de [`music_gen.py`](music_gen.py), nunca equivalente silencioso.
7. **Voz**: `voice_kokoro.py` (local, grátis). PT-BR, masculina documental profunda quando pedido, com normalização de pronúncia.
8. **Render**: `studio.py render` sobre o `project.json` validado.
9. **Mix (papel 2)**: `audio_mix.py --in-place --record render.json`; alvos medidos e arquivo revisado idêntico ao exportado.
10. **Gates determinísticos**: `studio.py gates` — 1 narração (The-Fool), 2 direitos de asset (com marca d'água), **3 trava de contexto visual**, 4 música selecionada de fato, 5 score técnico.
11. **Juiz adversarial (papel 6)**: contexto virgem, evidência real, seis notas. Ver abaixo.
12. **Publicação**: planejada pelo papel 4, executada só sob pedido explícito e com os gates do publicador existente.

## O juiz adversarial e o limiar

O papel 6 recebe o artefato e a evidência, **sem** o contexto narrativo do produtor, e é ele mesmo especialista no assunto pedido. Ele pontua 0–10 em `musica`, `voz`, `fluencia`, `enredo`, `visual_tematico` e `direitos`.

- **Limiar**: cada dimensão e o conjunto (média) precisam atingir **≥ 9,5/10**.
- **Evidência**: transcrição completa, quadros amostrados ao longo de TODO o vídeo, medições de loudness/LRA/silêncio, espectrograma, coerência tema×visual. O método de amostragem é declarado — ninguém afirma ter assistido 90 minutos quando amostrou.
- **Aprovação artística final**: humana, do operador. O juiz não substitui a palavra final.
- **Reprovação**: `REPROVADO` descarta os papéis de produção, exige causa raiz priorizada e reinicia a produção na etapa que a causa exige. Roteiro reprovado não se conserta na mixagem.
- **Limite**: máximo 3 tentativas. Na terceira, escalar ao operador em vez de girar indefinidamente.

## Trava de contexto visual (GATE 3) — `context_gate.py`

REGRA ABSOLUTA: se a cena fala de música, o frame mostra música daquele estilo; se fala de um átomo, o frame mostra átomos. Nada fora do contexto do roteiro — falha fechada, sem flag de bypass.

Como o vínculo é provado (determinístico):

1. **Ledger de proveniência** `assets/prompts.json`: `providers.py assets` registra, para cada imagem gerada por IA, `arquivo → {scene, kind, prompt exato, seed, generated}`. O gate compara os tokens do prompt com os tokens do roteiro da cena (tópico + narração + visual + sd_prompt). Asset reutilizado sem prova de geração (`generated: false`) bloqueia — apague o arquivo e regenere.
2. **Assets curados** (`build_layers.py`): a seleção usa `context_gate.select_scene_assets` — o nome do arquivo precisa citar o contexto (token comum após normalização de acentos/plural e famílias de domínio). **Cena sem nenhum asset em contexto bloqueia a execução (exit 2)**; o comportamento antigo (atribuir silenciosamente o primeiro asset em ordem alfabética) foi eliminado.
3. **Famílias de domínio** (`DOMAIN_FAMILIES`) são dados declarados (átomo↔atom, música↔music, …) e só se estendem por edição explícita; família ausente deixa o gate mais estrito, nunca mais frouxo.
4. **Evidência por execução**: `context_report.json` grava o veredito por cena/camada; o gate escreve o relatório mesmo quando bloqueia.

Contratos verificados: `test_context_gate.py` (17 testes, stdlib puro) + fumaça de encadeamento (asset sem proveniência → `GATE 3 FAIL: FORA DO CONTEXTO`; com ledger `proven` → segue ao GATE 4).

## Marca d'água — limite de política

Aquisição ocorre em acervos que já entregam o asset sem marca d'água (CC0, domínio público, CC BY). **Detecção e rejeição** de asset marcado são obrigatórias. **Remoção** de marca d'água de conteúdo de terceiros é proibida por política — burla copyright e termos de uso. Remoção só é admitida para asset próprio ou licenciado, com registro de licença e autorização explícita do operador. A ferramenta `assetguard` implementa detecção/rejeição e a remoção com registro.

## Comandos

```powershell
python science-studio/studio.py doctor
python science-studio/studio.py init --topic "O Elétron: descoberta e curiosidades" --profile full-documentary --output .work/electron-factory-90min
python science-studio/studio.py validate .work/electron-factory-90min/project.json
python science-studio/studio.py render   .work/electron-factory-90min/project.json
python science-studio/audio_mix.py --input .work/electron-factory-90min/preview.mp4 --in-place --record .work/electron-factory-90min/render.json
python science-studio/studio.py gates    .work/electron-factory-90min/project.json
python science-studio/studio.py review   .work/electron-factory-90min/project.json --reviewer "operador" --checks science visual voice subtitles rights
python science-studio/studio.py export   .work/electron-factory-90min/project.json
```

`init` cria um contrato vazio real, não um roteiro fictício. A duração total do projeto tem de fechar com a soma das cenas. `review` só é registrado após confirmação explícita do operador.

## Evidência e recuperação

`project.json` é a fonte de verdade; `stages.json` registra checkpoints; `render/` cacheia cena; `render.json` amarra hashes de conteúdo/vídeo/SRT; `approval.json` amarra a entrega revisada. Nunca editar aprovação para contornar saída obsoleta. Medição de silêncio usa `-v info` (`-v error` suprime os eventos do `silencedetect` e produz falso "0 silêncios"). Em mudança de fonte ou asset, validar e renderizar de novo. Arquivo revisado e exportado têm de ser os mesmos bytes.
