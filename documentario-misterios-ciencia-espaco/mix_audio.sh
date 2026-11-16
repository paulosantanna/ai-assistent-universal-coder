#!/usr/bin/env bash
# mix_audio.sh - Mixagem automatizada de narração + música para documentário
# Requer: ffmpeg, ffprobe

set -euo pipefail

# Configurações
NARRATION_FILE="${1:-narration_full.wav}"
MUSIC_FILE="${2:-music_master.wav}"
OUTPUT_FILE="${3:-documentario_final.wav}"
OUTPUT_MP3="${4:-documentario_misterios_ciencia_espaco.mp3}"

# Verificar arquivos de entrada
for f in "$NARRATION_FILE" "$MUSIC_FILE"; do
    if [[ ! -f "$f" ]]; then
        echo "ERRO: Arquivo não encontrado: $f"
        exit 1
    fi
done

echo "=== Mixagem de Áudio - Documentário ==="
echo "Narração: $NARRATION_FILE"
echo "Música:   $MUSIC_FILE"
echo "Saída:    $OUTPUT_FILE"
echo "MP3:      $OUTPUT_MP3"
echo

# 1. Analisar arquivos de entrada
echo "1. Analisando arquivos de entrada..."
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$NARRATION_FILE" | xargs -I {} echo "  Duração narração: {}s"
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$MUSIC_FILE" | xargs -I {} echo "  Duração música:   {}s"

# 2. Processar narração: EQ, compressão, loudnorm
echo
echo "2. Processando narração..."
ffmpeg -y -i "$NARRATION_FILE" -af "
    highpass=f=80,
    lowpass=f=12000,
    equalizer=f=3000:width_type=h:width=500:g=3,
    equalizer=f=10000:width_type=h:width=1000:g=2,
    compand=attacks=0.01:decays=0.1:points=-90/-90|-30/-18|0/-3:soft-knee=6,
    loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json
" -ar 48000 -sample_fmt s16 narration_proc.wav

# 3. Processar música: EQ, compressão leve, loudnorm mais baixo
echo "3. Processando música..."
ffmpeg -y -i "$MUSIC_FILE" -af "
    highpass=f=40,
    lowpass=f=8000,
    compand=attacks=0.05:decays=0.2:points=-90/-90|-30/-24|0/-6,
    loudnorm=I=-24:TP=-2:LRA=15:print_format=json
" -ar 48000 -sample_fmt s16 music_proc.wav

# 4. Ducking: música cede para narração (sidechain)
echo "4. Aplicando ducking (sidechain)..."
ffmpeg -y -i narration_proc.wav -i music_proc.wav -filter_complex "
    [1:a][0:a]sidechaincompress=threshold=0.01:ratio=4:attack=5:release=200:makeup=1[music_ducked];
    [0:a][music_ducked]amix=inputs=2:duration=first:dropout_transition=0[mixed];
    [mixed]loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json
" -ar 48000 -sample_fmt s16 "$OUTPUT_FILE"

# 5. Verificar silêncio
echo "5. Verificando silêncio (QA)..."
SILENCE_LOG=$(ffmpeg -v info -i "$OUTPUT_FILE" -vn -af silencedetect=noise=-45dB:d=2.0 -f null - 2>&1 | grep -E 'silence_(start|end|duration)')
if [[ -n "$SILENCE_LOG" ]]; then
    echo "  ATENÇÃO: Silêncios detectados:"
    echo "$SILENCE_LOG" | sed 's/^/    /'
    SILENCE_COUNT=$(echo "$SILENCE_LOG" | grep -c 'silence_duration' || true)
    if [[ $SILENCE_COUNT -gt 0 ]]; then
        echo "  Total de silêncios >2s: $SILENCE_COUNT"
    fi
else
    echo "  OK: Nenhum silêncio >2s detectado"
fi

# 6. Medir loudness final
echo "6. Medindo loudness final..."
LOUDNESS_JSON=$(ffmpeg -y -i "$OUTPUT_FILE" -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | tail -20)
echo "$LOUDNESS_JSON" | grep -E 'input_i|input_tp|input_lra|input_thresh|target_offset' | sed 's/^/  /'

# 7. Gerar MP3 para Spotify (-14 LUFS normalizado)
echo "7. Gerando MP3 320kbps para Spotify..."
ffmpeg -y -i "$OUTPUT_FILE" -af "loudnorm=I=-14:TP=-1.5:LRA=11" \
    -c:a libmp3lame -b:a 320k -joint_stereo 1 \
    -id3v2_version 3 -write_id3v1 1 \
    -metadata title="Mistérios da Ciência e do Espaço" \
    -metadata artist="CodENavi Documentary Factory" \
    -metadata album="Documentários Científicos" \
    -metadata date="2026" \
    -metadata genre="Documentary" \
    -metadata comment="Documentário de 90 min sobre os mistérios da ciência e do espaço" \
    -metadata track="1" \
    "$OUTPUT_MP3"

# 8. Verificar MP3
echo "8. Verificando MP3 final..."
ffprobe -v error -show_entries format=duration,bit_rate -of default=noprint_wrappers=1:nokey=1 "$OUTPUT_MP3" | xargs -I {} echo "  {}"

echo
echo "=== Mixagem Concluída ==="
echo "WAV final: $OUTPUT_FILE"
echo "MP3 final: $OUTPUT_MP3"
echo
echo "Próximos passos:"
echo "  1. Ouvir arquivo final para QA subjetivo"
echo "  2. Verificar metadados ID3: ffprobe $OUTPUT_MP3 -show_entries format_tags"
echo "  3. Publicar no Spotify via Spotify for Podcasters ou distribuidor"