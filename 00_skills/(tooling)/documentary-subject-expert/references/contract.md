# Contrato do enredo e anti-padrões herdados

Updated: 2026-10-31. Módulo de [`documentary-subject-expert`](../SKILL.md).

## Ledger de fatos

Formato: `{id, title, url, publisher, accessed, excerpt}`. `id` kebab-case ASCII curto e único.
`excerpt` são 1–3 frases factuais densas que sustentam uma afirmação do roteiro — não resumo de
artigo, não opinião. `accessed` é data ISO.

Confiança preferencial: instituto de metrologia (NIST/CODATA), colaborações científicas (CERN,
PDG), agências espaciais (NASA/ESA), premiações oficiais (Nobel), física e química revisadas e
artigos históricos primários. Enciclopédia serve como ponteiro para a fonte primária, não como
autoridade final.

Fonte não confirmada é **descartada**. Inventar URL, DOI, autor ou trecho é a falha mais grave
possível neste papel — um único fato inventado contamina o documentário inteiro.

## Orçamento de palavras

Narração PT-BR documental rende ~110–145 palavras por minuto. Referência operacional:

| Duração da cena | Palavras de narração |
| --- | --- |
| 15 s | 27–34 |
| 30 s | 54–68 |
| 45 s | 81–102 |
| **60 s** | **108–136** |

Cena de 60 s narrada com ~13 palavras deixa ~54 s de silêncio e mata o vídeo. O TTS local ajusta a
taxa para caber na cena, mas não cria conteúdo ausente: a faixa acima é obrigatória.

## Estrutura da cena

Campos: `narration`, `visual`, `duration`, `claims` (lista de `id` do ledger), `transition`
(`cut`/`fade`), `sd_prompt` (diretiva de arte). Uma cena = **um** fenômeno. O `visual` descreve o
fenômeno mencionado naquele intervalo; "ilustração de ciência" não é diretiva válida.

## Anti-padrões herdados (falhas reais já ocorridas)

- **Cena subnarrada** — 13 palavras para 60 s. Silêncio massivo. Já aconteceu; não repetir.
- **Repetição de palavra** — mesma palavra mais de duas vezes na cena, ou frase repetida entre
  cenas. Sinal de geração em lote sem revisão.
- **Fragmento curto** — sentença de 1–2 tokens, resíduo de edição automática.
- **Certeza falsa** — hipótese em aberto apresentada como resultado estabelecido.
- **Visual genérico** — placa de circuito estilizada, cientista posando, "tecnologia" abstrata no
  lugar do fenômeno. Também já trouxe conteúdo fora do tema para dentro do vídeo.
- **Numeral ou rótulo falso gerado por IA** dentro de uma imagem — motivo para rejeitar o asset,
  tratado no papel 3.
- **Capítulo sem fechamento** — assunto que abre e não resolve; o espectador sente como corte.
- **Perda de fio no lote** — gerar capítulos sem outline global produz colcha de retalhos. Congelar
  o arco antes de escrever cena.
