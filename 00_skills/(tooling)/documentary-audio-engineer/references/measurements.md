# Medições, alvos e armadilhas de comando

Updated: 2026-10-31. Módulo de [`documentary-audio-engineer`](../SKILL.md).

## Alvos

| Métrica | Alvo | Como medir |
| --- | --- | --- |
| Voz (integrado) | **-16 LUFS** | `loudnorm` com `print_format=json` |
| True peak | **-1.5 dBFS** | idem, campo `input_tp` |
| LRA do mix | saudável, música audível | idem, campo `input_lra` |
| Silêncio | **zero acima de 2–3 s** | `silencedetect` com `-v info` |
| Fala por cena | 108–136 palavras / 60 s | contagem no roteiro + duração medida do WAV |

## Armadilha que já aprovou um vídeo mudo

`ffmpeg -v error` **suprime as mensagens do `silencedetect`**. O relatório sai "0 silêncios" e o
vídeo é aprovado com 90% de mudez. Este erro já aconteceu de verdade neste workspace.

Correto:

```powershell
ffmpeg -v info -i preview.mp4 -vn -af silencedetect=noise=-45dB:d=2.0 -f null -
```

Errado (produz falso negativo):

```powershell
ffmpeg -v error -i preview.mp4 -vn -af silencedetect=noise=-45dB:d=2.0 -f null -
```

O threshold `-45dB` detecta mudez real abaixo de qualquer trilha audível. Com trilha calma sempre
presente, nenhuma pausa cai abaixo dele — se cair, o áudio morreu.

## Loudness e true peak

```powershell
ffmpeg -v info -i preview.mp4 -vn -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json -f null -
```

Ler `input_i`, `input_tp`, `input_lra` do JSON. Medição sem números lidos é achismo.

## Ducking por sidechain

A trilha cede sob a voz sem ser desligada:

```powershell
ffmpeg -i voz.wav -i musica.wav -filter_complex "[1:a][0:a]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=600[ducked];[0:a][ducked]amix=inputs=2:duration=first:dropout_transition=0[mix]" -map "[mix]" mix.wav
```

A música continua audível nas pausas e recua durante a fala. Música que abaixa demais deixa de ser
trilha e vira zunido — se o resultado soar "mudo com ruído", o problema é de curadoria musical
(papel 1), não de volume.

## Fala por cena

Cena de 60 s com 13 palavras produz ~54 s de silêncio — falha real já ocorrida. Medir a duração do
WAV da cena contra a duração declarada da cena e conferir a contagem de palavras do roteiro. Cena
subnarrada volta para o roteiro; não se compensa com pausa, música alta ou alongamento artificial.

## Entrega

Mixar com `science-studio/audio_mix.py --in-place --record render.json` para que o arquivo revisado
e o arquivo exportado sejam os mesmos bytes. Registrar todas as medições em relatório JSON com o
comando usado ao lado de cada número.
