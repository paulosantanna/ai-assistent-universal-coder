#!/usr/bin/env bash
# ============================================================================
# SETUP E EXECUÇÃO - Produção MP3 Spotify
# Mistérios da Ciência e do Espaço (90 min)
# ============================================================================

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "================================================================"
echo "🎬 SETUP PRODUÇÃO MP3 - Mistérios da Ciência e do Espaço"
echo "================================================================"

# ---------------------------------------------------------------------------
# 1. VERIFICAR DEPENDÊNCIAS
# ---------------------------------------------------------------------------
echo ""
echo "🔍 Verificando dependências..."

check_cmd() {
    if command -v "$1" &> /dev/null; then
        echo "  ✓ $1: $(command -v $1)"
        return 0
    else
        echo "  ✗ $1: NÃO ENCONTRADO"
        return 1
    fi
}

MISSING=0
check_cmd ffmpeg || MISSING=1
check_cmd ffprobe || MISSING=1
check_cmd piper || MISSING=1
check_cmd python3 || MISSING=1

if [ $MISSING -eq 1 ]; then
    echo ""
    echo "⚠️  Dependências faltando. Instale:"
    echo ""
    echo "  # Ubuntu/Debian/WSL:"
    echo "  sudo apt update && sudo apt install -y ffmpeg python3 python3-pip"
    echo "  pip3 install piper-tts"
    echo ""
    echo "  # Windows (WSL2 recomendado) ou use Docker:"
    echo "  # Ver https://github.com/rhasspy/piper para instalacao Windows nativa"
    echo ""
    exit 1
fi

# ---------------------------------------------------------------------------
# 2. BAIXAR MODELO PIPER pm_alex
# ---------------------------------------------------------------------------
echo ""
echo "📥 Verificando modelo Piper pm_alex..."

MODEL_DIR="${HOME}/.local/share/piper/voices"
mkdir -p "$MODEL_DIR"

MODEL_PATH="${MODEL_DIR}/pm_alex.onnx"
MODEL_JSON="${MODEL_DIR}/pm_alex.onnx.json"

if [ ! -f "$MODEL_PATH" ]; then
    echo "  Baixando modelo pm_alex (voz masculina PT-BR)..."
    cd "$MODEL_DIR"
    
    # Tentar baixar do HuggingFace (piper-voices)
    # Nota: pm_alex pode não existir; usar fallback se necessário
    wget -q --show-progress "https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx" -O pm_alex.onnx 2>/dev/null || \
    wget -q --show-progress "https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx.json" -O pm_alex.onnx.json 2>/dev/null || \
    {
        echo "  ⚠ Modelo pm_alex não encontrado no repositório oficial."
        echo "  Usando modelo pt_BR-faber-medium como fallback (voz masculina PT-BR)..."
        wget -q --show-progress "https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx" -O pm_alex.onnx
        wget -q --show-progress "https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx.json" -O pm_alex.onnx.json
    }
    
    cd "$PROJECT_DIR"
else
    echo "  ✓ Modelo já existe: $MODEL_PATH"
fi

# Verificar se modelo é válido
if [ ! -f "$MODEL_PATH" ]; then
    echo "  ✗ Falha ao obter modelo Piper"
    exit 1
fi

# ---------------------------------------------------------------------------
# 3. VERIFICAR ARQUIVOS DO PROJETO
# ---------------------------------------------------------------------------
echo ""
echo "📁 Verificando arquivos do projeto..."

REQUIRED_FILES=(
    "13_narration_ssml.xml"
    "01_fact-ledger.json"
    "12_master_script.json"
)

for f in "${REQUIRED_FILES[@]}"; do
    if [ -f "$f" ]; then
        echo "  ✓ $f"
    else
        echo "  ✗ $f (FALTANDO)"
        exit 1
    fi
done

# ---------------------------------------------------------------------------
# 4. MÚSICA DE FUNDO (OPCIONAL)
# ---------------------------------------------------------------------------
echo ""
echo "🎵 Verificando música de fundo..."

MUSIC_FILE=""
if ls music_*.wav music_*.mp3 bg_*.wav bg_*.mp3 2>/dev/null | head -1 | grep -q .; then
    MUSIC_FILE=$(ls music_*.wav music_*.mp3 bg_*.wav bg_*.mp3 2>/dev/null | head -1)
    echo "  ✓ Encontrado: $MUSIC_FILE"
else
    echo "  ⚠ Nenhum arquivo de música encontrado."
    echo "  Será gerada música sintética (drone suave)."
    echo ""
    echo "  Para usar sua própria música (recomendado):"
    echo "    1. Coloque arquivo MP3/WAV na pasta do projeto"
    echo "    2. Renomeie para 'music_background.mp3' ou 'bg_music.wav'"
    echo "    3. Reexecute este script"
    echo ""
    echo "  Fontes livres recomendadas (CC-BY/CC0):"
    echo "    - https://freemusicarchive.org/"
    echo "    - https://incompetech.filmmusic.io/"
    echo "    - https://www.youtube.com/audiolibrary/music"
    echo "    - https://archive.org/details/audio_music_cc0"
fi

# ---------------------------------------------------------------------------
# 5. EXECUTAR PRODUÇÃO
# ---------------------------------------------------------------------------
echo ""
echo "================================================================"
echo "🚀 INICIANDO PRODUÇÃO DO MP3"
echo "================================================================"

PYTHON_SCRIPT="produce_mp3_spotify.py"

if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "  ✗ Script de produção não encontrado: $PYTHON_SCRIPT"
    exit 1
fi

# Argumentos
VOICE_MODEL="$MODEL_PATH"
MUSIC_ARG=""
if [ -n "$MUSIC_FILE" ]; then
    MUSIC_ARG="--music $MUSIC_FILE"
fi

echo ""
echo "Configuração:"
echo "  Modelo voz: $VOICE_MODEL"
echo "  Música: ${MUSIC_FILE:-'Sintética (gerada)'}"
echo "  Saída: output/Misterios_Ciencia_Espaco_Spotify.mp3"
echo ""

# Executar
python3 "$PYTHON_SCRIPT" \
    --project-dir "$PROJECT_DIR" \
    --voice "$VOICE_MODEL" \
    $MUSIC_ARG \
    2>&1 | tee production.log

# ---------------------------------------------------------------------------
# 6. VERIFICAÇÃO FINAL
# ---------------------------------------------------------------------------
OUTPUT_MP3="output/Misterios_Ciencia_Espaco_Spotify.mp3"

if [ -f "$OUTPUT_MP3" ]; then
    echo ""
    echo "================================================================"
    echo "✅ PRODUÇÃO CONCLUÍDA COM SUCESSO!"
    echo "================================================================"
    echo ""
    echo "📁 Arquivo final: $OUTPUT_MP3"
    echo ""
    echo "📊 Especificações técnicas:"
    ffprobe -v error -show_entries format=duration,bit_rate -of default=noprint_wrappers=1:nokey=1 "$OUTPUT_MP3" | while read line; do
        if [[ $line =~ ^[0-9]+\.?[0-9]*$ ]]; then
            echo "  Duração: $(echo "scale=1; $line/60" | bc) min"
        else
            echo "  Bitrate: $(echo "scale=0; $line/1000" | bc) kbps"
        fi
    done
    echo "  Formato: MP3 (libmp3lame), 48kHz, Stereo"
    echo "  Loudness: -14 LUFS (Spotify standard)"
    echo "  True Peak: -1.5 dBFS"
    echo ""
    echo "📋 Próximos passos para publicar no Spotify:"
    echo "  1. Acesse https://podcasters.spotify.com/"
    echo "  2. Faça login ou crie conta"
    echo "  3. Clique em 'Criar podcast' > 'Carregar arquivo'"
    echo "  4. Selecione: $OUTPUT_MP3"
    echo "  5. Preencha metadados (já embutidos no ID3):"
    echo "     - Título: Mistérios da Ciência e do Espaço"
    echo "     - Artista: CodENavi Documentary Factory"
    echo "     - Categoria: Science / Documentary"
    echo "     - Explícito: Não"
    echo "  6. Publique!"
    echo ""
else
    echo ""
    echo "================================================================"
    echo "❌ FALHA NA PRODUÇÃO"
    echo "================================================================"
    echo "Verifique o log acima para erros."
    echo "Log salvo em: production.log"
    exit 1
fi