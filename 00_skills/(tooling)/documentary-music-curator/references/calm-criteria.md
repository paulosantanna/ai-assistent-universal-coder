# Critério de calma, licenças aceitas e medição

Updated: 2026-10-31. Módulo de [`documentary-music-curator`](../SKILL.md).

## Calma é mensurável

"Calma" não é impressão subjetiva; cada critério abaixo tem verificação:

| Critério | Aceitar | Rejeitar |
| --- | --- | --- |
| Andamento | contido, referência ≤ ~90 BPM | acelerado, dançante, marcha rápida |
| Percussão | ausente ou não marcada | bateria em destaque, beat de quatro no chão |
| Vocal | ausente, ou sem palavra inteligível | vocal cantado em primeiro plano |
| Dinâmica | estável; sem pico súbito | subidas de volume, drops, clímax explosivo |
| Caráter | ambiental, drone tonal, neoclássico lento, piano/strings lentos, pad sustentado | EDM, rock, dubstep, trailer de ação |
| Espectro | sustentado, sem transiente agressivo | agressivo em agudos, "brilho" de trailer |

Medir com ferramenta: duração, loudness integrado e LRA via `ffmpeg`. Registrar o número medido em
`why_calm`. Estimativa de memória não vale como evidência.

## Licenças aceitas

| Acervo | Licença típica | Cuidado |
| --- | --- | --- |
| Free Music Archive | CC0 / CC BY / CC BY-SA | conferir a tag **da faixa** |
| Pixabay Music | Pixabay Content License | permite comercial; ler a página da faixa |
| ccMixter | CC (varia por obra) | mistura CC BY-NC — rejeitar NC |
| Wikimedia Commons | CC0 / CC BY / PD | conferir a página do arquivo |
| Internet Archive | PD / CC0 / CC | coleções misturam licenças |
| Openverse | agrega CC | sempre resolve para a origem |
| Site oficial do artista | declarada pelo autor | exige página de licença real |

## Rejeição por procedência

Canal de YouTube, perfil de rede social ou site de "músicas grátis" que se autodenomina sem
copyright **sem licença explícita e verificável na descrição ou na obra do artista** é rejeitado.
A maioria rotula errado; o custo do erro é claim de Content ID sobre o vídeo do operador.

## Campos obrigatórios por faixa aceita

`license_name`, `license_url`, `evidence_url` (conferidos, reais), `commercial_use`,
`derivatives_allowed`, `attribution_required` e `attribution_text` quando exigido. Faixa com
atribuição exigida e sem texto de atribuição **não entra** — o crédito é condição da licença.

## Cobertura

A trilha tem de cobrir a duração do vídeo. Faixa mais curta exige ponto de loop declarado. Sem
acervo suficiente, reportar a lacuna: a trilha procedural validada (`music_gen.py`) é o fallback
declarado — nunca um equivalente silencioso, e nunca a mesma coisa que uma faixa licenciada.
