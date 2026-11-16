@echo off
REM ============================================================================
REM PRODUÇÃO MP3 SPOTIFY - Mistérios da Ciência e do Espaço (Windows)
REM ============================================================================

set PROJECT_DIR=%~dp0
cd /d "%PROJECT_DIR%"

echo ============================================================================
echo 🎬 PRODUÇÃO MP3 - Mistérios da Ciência e do Espaço (90 min)
echo ============================================================================

REM ---------------------------------------------------------------------------
REM 1. VERIFICAR DEPENDÊNCIAS
REM ---------------------------------------------------------------------------
echo.
echo 🔍 Verificando dependências...

where ffmpeg >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ ffmpeg NÃO ENCONTRADO
    echo.
    echo Instale ffmpeg:
    echo   1. Baixe em: https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z
    echo   2. Extraia e adicione a pasta 'bin' ao PATH do Windows
    echo   3. Reinicie o terminal
    pause
    exit /b 1
) else (
    echo ✓ ffmpeg encontrado
)

where ffprobe >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ ffprobe NÃO ENCONTRADO (vem com ffmpeg)
    pause
    exit /b 1
) else (
    echo ✓ ffprobe encontrado
)

where piper >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ piper NÃO ENCONTRADO
    echo.
    echo Instale Piper TTS:
    echo   pip install piper-tts
    echo.
    echo Ou baixe binário em: https://github.com/rhasspy/piper/releases
    pause
    exit /b 1
) else (
    echo ✓ piper encontrado
)

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ python NÃO ENCONTRADO
    pause
    exit /b 1
) else (
    echo ✓ python encontrado
)

REM ---------------------------------------------------------------------------
REM 2. BAIXAR MODELO PIPER pm_alex (voz masculina PT-BR)
REM ---------------------------------------------------------------------------
echo.
echo 📥 Verificando modelo Piper pm_alex...

set MODEL_DIR=%USERPROFILE%\.local\share\piper\voices
if not exist "%MODEL_DIR%" mkdir "%MODEL_DIR%"

set MODEL_PATH=%MODEL_DIR%\pm_alex.onnx
set MODEL_JSON=%MODEL_DIR%\pm_alex.onnx.json

if not exist "%MODEL_PATH%" (
    echo Baixando modelo pt_BR-faber-medium (voz masculina PT-BR, fallback para pm_alex)...
    cd /d "%MODEL_DIR%"
    
    curl -L -o pm_alex.onnx "https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx"
    if errorlevel 1 (
        echo ❌ Falha ao baixar modelo .onnx
        pause
        exit /b 1
    )
    
    curl -L -o pm_alex.onnx.json "https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx.json"
    if errorlevel 1 (
        echo ❌ Falha ao baixar modelo .json
        pause
        exit /b 1
    )
    
    cd /d "%PROJECT_DIR%"
) else (
    echo ✓ Modelo já existe: %MODEL_PATH%
)

REM ---------------------------------------------------------------------------
REM 3. VERIFICAR ARQUIVOS DO PROJETO
REM ---------------------------------------------------------------------------
echo.
echo 📁 Verificando arquivos do projeto...

for %%f in (13_narration_ssml.xml 01_fact-ledger.json 12_master_script.json) do (
    if exist "%%f" (
        echo ✓ %%f
    ) else (
        echo ❌ %%f (FALTANDO)
        pause
        exit /b 1
    )
)

REM ---------------------------------------------------------------------------
REM 4. MÚSICA DE FUNDO
REM ---------------------------------------------------------------------------
echo.
echo 🎵 Verificando música de fundo...

set MUSIC_FILE=
for %%f in (music_*.wav music_*.mp3 bg_*.wav bg_*.mp3) do (
    if exist "%%f" if "%MUSIC_FILE%"=="" set MUSIC_FILE=%%f
)

if "%MUSIC_FILE%"=="" (
    echo ⚠ Nenhum arquivo de música encontrado.
    echo Será gerada música sintética (drone suave).
    echo.
    echo Para usar sua própria música (recomendado):
    echo   1. Coloque arquivo MP3/WAV nesta pasta
    echo   2. Renomeie para 'music_background.mp3' ou 'bg_music.wav'
    echo   3. Reexecute este script
    echo.
    echo Fontes livres (CC-BY/CC0):
    echo   - https://freemusicarchive.org/
    echo   - https://incompetech.filmmusic.io/
    echo   - https://www.youtube.com/audiolibrary/music
    set MUSIC_ARG=
) else (
    echo ✓ Encontrado: %MUSIC_FILE%
    set MUSIC_ARG=--music "%MUSIC_FILE%"
)

REM ---------------------------------------------------------------------------
REM 5. EXECUTAR PRODUÇÃO
REM ---------------------------------------------------------------------------
echo.
echo ============================================================================
echo 🚀 INICIANDO PRODUÇÃO DO MP3
echo ============================================================================
echo.
echo Configuração:
echo   Modelo voz: %MODEL_PATH%
echo   Música: %MUSIC_FILE%
echo   Saída: output\Misterios_Ciencia_Espaco_Spotify.mp3
echo.

python produce_mp3_spotify.py --project-dir "%PROJECT_DIR%" --voice "%MODEL_PATH%" %MUSIC_ARG% 2>&1 | tee production.log

REM ---------------------------------------------------------------------------
REM 6. VERIFICAÇÃO FINAL
REM ---------------------------------------------------------------------------
set OUTPUT_MP3=output\Misterios_Ciencia_Espaco_Spotify.mp3

if exist "%OUTPUT_MP3%" (
    echo.
    echo ============================================================================
    echo ✅ PRODUÇÃO CONCLUÍDA COM SUCESSO!
    echo ============================================================================
    echo.
    echo 📁 Arquivo final: %OUTPUT_MP3%
    echo.
    echo 📊 Especificações técnicas:
    for /f "tokens=*" %%a in ('ffprobe -v error -show_entries format^=duration -of default^=noprint_wrappers^=1:nokey^=1 "%OUTPUT_MP3%"') do (
        set DUR=%%a
    )
    for /f "tokens=*" %%a in ('ffprobe -v error -show_entries format^=bit_rate -of default^=noprint_wrappers^=1:nokey^=1 "%OUTPUT_MP3%"') do (
        set BR=%%a
    )
    echo   Duração: %DUR% segundos
    echo   Bitrate: %BR% bps
    echo   Formato: MP3 (libmp3lame), 48kHz, Stereo
    echo   Loudness: -14 LUFS (Spotify standard)
    echo   True Peak: -1.5 dBFS
    echo.
    echo 📋 Próximos passos para publicar no Spotify:
    echo   1. Acesse https://podcasters.spotify.com/
    echo   2. Faça login ou crie conta
    echo   3. Clique em 'Criar podcast' > 'Carregar arquivo'
    echo   4. Selecione: %OUTPUT_MP3%
    echo   5. Preencha metadados (já embutidos no ID3):
    echo      - Título: Mistérios da Ciência e do Espaço
    echo      - Artista: CodENavi Documentary Factory
    echo      - Categoria: Science / Documentary
    echo      - Explícito: Não
    echo   6. Publique!
    echo.
) else (
    echo.
    echo ============================================================================
    echo ❌ FALHA NA PRODUÇÃO
    echo ============================================================================
    echo Verifique o log acima para erros.
    echo Log salvo em: production.log
)

pause