# Produção do MP3 - Mistérios da Ciência e do Espaço

## Visão Geral
Documentário de 90 minutos em PT-BR, 9 capítulos, 87 cenas, ~9.938 palavras
Taxa de narração alvo: ~110-125 palavras/minuto (natural para documentário PT-BR)

---

## Pipeline de Produção (Documentary Factory)

### 1. Narração (ptbr-documentary-voice-expert)
**Entrada:** `13_narration_ssml.xml` (SSML com marcação prosódica)
**Motor TTS recomendado:** 
- **Azure Speech Service** (pt-BR-AntonioNeural / pt-BR-FranciscaNeural)
- **AWS Polly** (pt-BR-Thiago / pt-BR-Camila)
- **Google Cloud TTS** (pt-BR-Neural2-A / pt-BR-Neural2-B)
- **Piper TTS** (local, modelo pt_BR)

**Parâmetros de voz:**
- Voz: Masculina, documental, profunda (AntonioNeural recomendado)
- Taxa: 0% (normal) ou -5% (ligeiramente mais lento para documentário)
- Pitch: 0% (natural)
- Volume: medium

**Saída:** `narration_raw.wav` (48kHz, 16-bit, mono) + `narration_timestamps.json` (alinhamento palavra-por-palavra)

### 2. Trilha Musical (documentary-music-curator)
**Critérios:**
- Licença CC-BY, CC0, ou royalty-free com atribuição clara
- Caráter "calmo" (BPM 60-80, harmonia consonante, sem percussão marcante)
- Duração: ~90 min (loop ou faixas contínuas)
- Formato: WAV 48kHz/24-bit

**Fontes recomendadas:**
- Free Music Archive (FMA)
- Incompetech (Kevin MacLeod)
- Musopen
- YouTube Audio Library
- Archive.org

**Curadoria por capítulo:**
- Cap 1-2 (Cosmologia): Ambient space, drones suaves
- Cap 3 (Astrobiologia): Orgânico, textural
- Cap 4 (Buracos Negros): Profundo, grave, misterioso
- Cap 5 (Quântica): Minimalista, repetitivo
- Cap 6 (Origem da Vida): Orgânico, evolutivo
- Cap 7 (Multiverso): Expansivo, etéreo
- Cap 8 (Consciência): Introspectivo, piano/sintetizador suave
- Cap 9 (Futuro): Resolutivo, amplo

**Saída:** `music_stems/` (faixas separadas por capítulo) + `music_license_ledger.json`

### 3. Mixagem de Áudio (documentary-audio-engineer)
**Entradas:**
- `narration_raw.wav`
- `music_master.wav` (mix das faixas musicais)

**Processamento:**
1. **Narração:**
   - EQ: High-pass 80Hz, presença 2-4kHz, air 10-12kHz
   - Compressão: Ratio 3:1, attack 10ms, release 100ms, threshold -18dB
   - Loudnorm: -16 LUFS integrado, -1.5 dBTP true peak
   - De-esser: 5-8kHz, threshold -30dB

2. **Música:**
   - EQ: Low-pass 8kHz (dar espaço à narração), high-pass 40Hz
   - Compressão leve: Ratio 2:1
   - Loudnorm: -24 LUFS (8dB abaixo da narração)

3. **Ducking (Sidechain):**
   - Sidechain da narração → compressor na música
   - Threshold: -20dB, Ratio: 4:1, Attack: 5ms, Release: 200ms
   - Gain reduction: 6-12dB durante fala

4. **Mix Final:**
   - Loudnorm master: -16 LUFS integrado, -1.5 dBTP
   - Verificação de silêncio: `ffmpeg -v info -i mix.wav -vn -af silencedetect=noise=-45dB:d=2.0 -f null -`
   - Zero silêncio > 3s (exceto transições intencionais)

**Saída:** `documentario_final.wav` (48kHz/24-bit) + `render.json` (medições)

### 4. MP3 Final (Spotify)
**Codificação:**
```bash
ffmpeg -i documentario_final.wav \
  -c:a libmp3lame -b:a 320k \
  -joint_stereo 1 \
  -id3v2_version 3 \
  -write_id3v1 1 \
  -metadata title="Mistérios da Ciência e do Espaço" \
  -metadata artist="CodENavi Documentary Factory" \
  -metadata album="Documentários Científicos" \
  -metadata date="2026" \
  -metadata genre="Documentary" \
  -metadata comment="Documentário de 90 min sobre ciência e espaço" \
  -metadata track="1" \
  documentario_misterios_ciencia_espaco.mp3
```

**Loudness normalizado para Spotify:** -14 LUFS (Spotify normaliza para -14 LUFS)
- Se master em -16 LUFS: ganho +2dB no encode
- Ou usar `loudnorm=I=-14:TP=-1.5:LRA=11` no ffmpeg

---

## Arquivos do Projeto

```
documentario-misterios-ciencia-espaco/
├── 01_fact-ledger.json           # Ledger de fatos com 73 fontes
├── 02_chapter-outline.json       # Outline dos 9 capítulos
├── 03_scenes_chapter1.json       # Cenas cap 1 (CMB)
├── 04_scenes_chapter2.json       # Cenas cap 2 (Matéria/Energia Escura)
├── 05_scenes_chapter3.json       # Cenas cap 3 (Fermi/Vida)
├── 06_scenes_chapter4.json       # Cenas cap 4 (Buracos Negros)
├── 07_scenes_chapter5.json       # Cenas cap 5 (Realidade Quântica)
├── 08_scenes_chapter6.json       # Cenas cap 6 (Origem da Vida)
├── 09_scenes_chapter7.json       # Cenas cap 7 (Multiverso)
├── 10_scenes_chapter8.json       # Cenas cap 8 (Consciência)
├── 11_scenes_chapter9.json       # Cenas cap 9 (Futuro)
├── 12_master_script.json         # Script mestre
├── 13_narration_ssml.xml         # SSML para TTS
├── full_narration.txt            # Texto completo (legível)
├── narration_segments/           # (a criar) WAVs por cena
│   ├── cap1_cena1.wav
│   ├── cap1_cena2.wav
│   └── ...
├── music_stems/                  # (a criar) Música por capítulo
│   ├── cap1_music.wav
│   └── ...
├── narration_raw.wav             # (output TTS) Narração completa
├── music_master.wav              # (output music) Música mixada
├── documentario_final.wav        # (output mix) Mix final
├── documentario_misterios_ciencia_espaco.mp3  # (final) MP3 320kbps
├── render.json                   # Medições de loudness/silêncio
├── music_license_ledger.json     # Licenças das músicas
└── production_log.md             # Log de produção
```

---

## Comandos de Produção (Referência)

### TTS com Azure Speech CLI (exemplo)
```bash
# Instalar
pip install azure-cognitiveservices-speech

# Gerar narração completa
python generate_narration.py \
  --ssml 13_narration_ssml.xml \
  --voice pt-BR-AntonioNeural \
  --output narration_raw.wav \
  --timestamps narration_timestamps.json
```

### TTS com Piper (local, gratuito)
```bash
# Baixar modelo pt_BR
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx.json

# Converter SSML para texto simples (remover tags)
python ssml_to_text.py 13_narration_ssml.xml > narration_text.txt

# Gerar áudio por capítulos (para controlar pausas)
piper --model pt_BR-faber-medium.onnx \
  --output_dir narration_segments/ \
  --input_file narration_text.txt
```

### Mixagem com FFmpeg (script automatizado)
```bash
#!/bin/bash
# mix_audio.sh

# 1. Processar narração
ffmpeg -i narration_raw.wav -af "
  highpass=f=80,
  lowpass=f=12000,
  equalizer=f=3000:width_type=h:width=500:g=3,
  equalizer=f=10000:width_type=h:width=1000:g=2,
  compand=attacks=0.01:decays=0.1:points=-90/-90|-30/-18|0/-3:soft-knee=6,
  loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json
" -ar 48000 narration_processed.wav

# 2. Processar música
ffmpeg -i music_master.wav -af "
  highpass=f=40,
  lowpass=f=8000,
  compand=attacks=0.05:decays=0.2:points=-90/-90|-30/-24|0/-6,
  loudnorm=I=-24:TP=-2:LRA=15
" -ar 48000 music_processed.wav

# 3. Ducking (sidechain narration -> music)
ffmpeg -i narration_processed.wav -i music_processed.wav -filter_complex "
  [1:a][0:a]sidechaincompress=threshold=0.01:ratio=4:attack=5:release=200:makeup=1[music_ducked];
  [0:a][music_ducked]amix=inputs=2:duration=first:dropout_transition=0[mixed];
  [mixed]loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json
" -ar 48000 documentario_final.wav

# 4. Verificar silêncio
ffmpeg -v info -i documentario_final.wav -vn -af silencedetect=noise=-45dB:d=2.0 -f null - 2>&1 | grep silence

# 5. Gerar MP3 para Spotify
ffmpeg -i documentario_final.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11" \
  -c:a libmp3lame -b:a 320k -joint_stereo 1 \
  -metadata title="Mistérios da Ciência e do Espaço" \
  -metadata artist="CodENavi Documentary Factory" \
  documentario_misterios_ciencia_espaco.mp3
```

### QA Final (Checklist)
- [ ] Duração total: 88-92 minutos
- [ ] Loudness integrado: -16 LUFS (±0.5) / -14 LUFS para Spotify
- [ ] True peak: ≤ -1.5 dBFS
- [ ] LRA: 7-15 LU
- [ ] Zero silêncio > 3s (exceto transições de capítulo ~2s)
- [ ] Música audível durante toda narração (LRA do mix > LRA da narração sola)
- [ ] Narração inteligível em todo momento (sem abafamento)
- [ ] Transições suaves entre capítulos (fade 1-2s)
- [ ] Metadados ID3 completos no MP3
- [ ] Licenças musicais documentadas em `music_license_ledger.json`

---

## Entrega para Spotify

### Via Spotify for Podcasters (RSS)
1. Hospedar MP3 em CDN (AWS S3, Cloudflare R2, etc.)
2. Criar feed RSS com:
   - Título: "Mistérios da Ciência e do Espaço"
   - Descrição: "Documentário de 90 minutos explorando os maiores mistérios da cosmologia, física quântica, origem da vida e consciência."
   - Imagem: 3000x3000px (capa)
   - Categoria: Science / Documentary
   - Explicit: false

### Via Distribuidor (Anchor, DistroKid, etc.)
- Upload do MP3 + metadados
- Selecionar "Podcast" > "Science"
- Aguardar aprovação (24-48h)

---

## Métricas de Qualidade (Gates)

| Métrica | Alvo | Tolerância | Ferramenta |
|---------|------|------------|------------|
| Duração | 5400s | ±120s | ffprobe |
| Loudness (integrado) | -16 LUFS | ±0.5 LU | ffmpeg loudnorm |
| True Peak | -1.5 dBFS | ±0.2 dB | ffmpeg loudnorm |
| LRA | 11 LU | ±3 LU | ffmpeg loudnorm |
| Silêncio > 3s | 0 eventos | 0 | ffmpeg silencedetect |
| THD+N | < 0.1% | - | Adobe Audition / RX |
| Narração/Música ratio | 8-12 dB | ±2 dB | Medição manual |

---

## Próximos Passos

1. **Selecionar motor TTS** (Azure/AWS/Google/Piper) e gerar `narration_raw.wav`
2. **Curar trilha musical** (8-10 faixas, ~10-12 min cada, licenças verificadas)
3. **Executar mixagem** (script `mix_audio.sh` ou DAW: Reaper, Audacity, Adobe Audition)
4. **QA completo** (checklist acima)
5. **Gerar MP3 final** (320kbps, -14 LUFS para Spotify)
6. **Publicar no Spotify** via Spotify for Podcasters ou distribuidor

---

*Gerado pelo Documentary Factory Pipeline - CodENavi Agent*
*Data: 2026-10-31*