# Protocolo de evidência — como o juiz obtém prova real

Updated: 2026-10-31. Módulo de [`documentary-adversarial-judge`](../SKILL.md).

Este módulo existe para impedir duas fraudes: julgar por impressão e julgar por herança de contexto.
Toda nota precisa de um artefato de evidência nomeado. Sem artefato, a nota é `INCONCLUSAO`.

## Regra de contexto virgem

O juiz recebe somente:

- o arquivo de vídeo final (mixado);
- `project.json` (roteiro e estrutura) e `subtitles.srt`;
- `license-ledger.json` (música) e `sourcing-ledger.json` (assets);
- relatórios de medição do mix (`render.json` ou equivalente);
- `sources.json` (ledger de fatos).

O juiz **não** recebe: resumo do produtor, justificativa de escolha, changelog, opinião de quem
escreveu, nem a conversa que produziu o roteiro. Se receber, o julgamento é inválido.

## Evidência obrigatória por dimensão

| Dimensão | Evidência mínima |
| --- | --- |
| `musica` | loudness/LRA do mix medidos; faixa(s) do ledger com licença; trecho amostrado de música isolada quando possível; verificação de ducking sob a voz |
| `voz` | amostras de áudio de cenas **distantes** entre si (início, meio, fim); pronúncia PT-BR; ausência de artefato; consistência de timbre |
| `fluencia` | medição de silêncio com `-v info`; duração de fala por cena; `subtitles.srt` confrontado com o roteiro; ausência de trecho mudo |
| `enredo` | `project.json` completo lido como especialista do domínio; cada `claim` conferida contra `sources.json`; repetição e fragmento por contagem |
| `visual_tematico` | quadros amostrados ao longo de TODO o vídeo e dentro de cada capítulo; conferência tema×quadro; detecção de marca d'água/logo/texto falso |
| `direitos` | ledger completo; licença por item; atribuições exigidas presentes nos créditos |

## Comandos de extração

Silêncio — **com `-v info`**. `-v error` suprime os eventos e produz falso "0 silêncios":

```powershell
ffmpeg -v info -i preview.mp4 -vn -af silencedetect=noise=-45dB:d=2.0 -f null -
```

Loudness integrado, true peak e LRA:

```powershell
ffmpeg -v info -i preview.mp4 -vn -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json -f null -
```

Espectrograma (prova visual da trilha presente e do ducking):

```powershell
ffmpeg -i preview.mp4 -lavfi showspectrumpic=s=1280x720:legend=1 espectro.png
```

Amostragem de quadros ao longo de todo o filme — início, meio, fim e por capítulo:

```powershell
ffmpeg -ss <t> -i preview.mp4 -frames:v 1 quadro_<t>.png
```

Extrair a voz isolada quando o mix permitir, ou pelo menos trechos de áudio por cena, para
inspeção de pronúncia e de consistência.

## Declaração de método

O veredito declara explicitamente: quantos quadros foram amostrados, em quais instantes, quantas
amostras de áudio foram ouvidas, e quais comandos produziram cada medição. É proibido escrever
"assisti ao vídeo" ou "ouvi integralmente" quando o método foi amostragem.

## Limite conhecido

Nenhum juiz automático substitui a percepção artística humana de 90 minutos contínuos. O juiz
adversarial reduz risco e aponta causa raiz; a aprovação artística final é do operador. Declarar
esse limite é parte do veredito, não uma ressalva opcional.
