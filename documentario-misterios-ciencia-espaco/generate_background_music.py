#!/usr/bin/env python3
"""
Gerador de música de fundo para documentário
Cria tracks ambientais por capítulo (9 tracks, ~10 min cada)
Licença: CC0 (domínio público - gerado algoritmicamente)
"""

import subprocess
import os
import sys
from pathlib import Path


CHAPTER_CONFIGS = [
    {
        "name": "cap1_cosmologia",
        "duration_sec": 600,
        "base_freq": 55,      # A1 - grave, cósmico
        "intervals": [1, 1.5, 2, 2.5, 3, 4],  # oitava, quinta, oitava, nona, décima, décima terceira
        "lfo_rate": 0.05,     # modulação muito lenta
        "filter_freq": 200,   # lowpass suave
        "reverb": 0.4,
        "description": "CMB, Big Bang - grave, expansivo"
    },
    {
        "name": "cap2_escuro",
        "duration_sec": 600,
        "base_freq": 41.2,    # E1 - muito grave
        "intervals": [1, 1.33, 2, 2.67, 3],   # menores, mais misterioso
        "lfo_rate": 0.03,
        "filter_freq": 150,
        "reverb": 0.5,
        "description": "Matéria/Energia Escura - misterioso, invisível"
    },
    {
        "name": "cap3_vida",
        "duration_sec": 600,
        "base_freq": 65.4,    # C2
        "intervals": [1, 1.25, 1.5, 2, 2.5, 3],  # maior, orgânico
        "lfo_rate": 0.08,
        "filter_freq": 400,
        "reverb": 0.3,
        "description": "Fermi, Astrobiologia - orgânico, esperançoso"
    },
    {
        "name": "cap4_buracos_negros",
        "duration_sec": 600,
        "base_freq": 32.7,    # C1 - extremamente grave
        "intervals": [1, 1.5, 2, 3],  # power chords, pesado
        "lfo_rate": 0.02,
        "filter_freq": 100,
        "reverb": 0.6,
        "description": "Buracos Negros - pesado, gravitacional"
    },
    {
        "name": "cap5_quantica",
        "duration_sec": 600,
        "base_freq": 82.4,    # E2
        "intervals": [1, 1.25, 1.5, 1.75, 2, 2.5, 3],  # complexo, quântico
        "lfo_rate": 0.15,     # mais rápido, "quântico"
        "filter_freq": 800,
        "reverb": 0.2,
        "description": "Realidade Quântica - complexo, vibrante"
    },
    {
        "name": "cap6_origem_vida",
        "duration_sec": 600,
        "base_freq": 73.4,    # D2
        "intervals": [1, 1.125, 1.25, 1.5, 2, 2.25, 3],  # evolutivo
        "lfo_rate": 0.06,
        "filter_freq": 500,
        "reverb": 0.35,
        "description": "Origem da Vida - evolutivo, emergente"
    },
    {
        "name": "cap7_multiverso",
        "duration_sec": 600,
        "base_freq": 49,      # G1
        "intervals": [1, 1.5, 2, 2.5, 3, 4, 5],  # expansivo, infinito
        "lfo_rate": 0.04,
        "filter_freq": 300,
        "reverb": 0.5,
        "description": "Multiverso - expansivo, infinito"
    },
    {
        "name": "cap8_consciencia",
        "duration_sec": 600,
        "base_freq": 110,     # A2
        "intervals": [1, 1.25, 1.5, 1.75, 2, 2.5],  # introspectivo
        "lfo_rate": 0.07,
        "filter_freq": 600,
        "reverb": 0.3,
        "description": "Consciência - introspectivo, interno"
    },
    {
        "name": "cap9_futuro",
        "duration_sec": 600,
        "base_freq": 55,      # A1 - volta ao início
        "intervals": [1, 1.5, 2, 2.5, 3, 3.5, 4],  # resolutivo
        "lfo_rate": 0.03,
        "filter_freq": 250,
        "reverb": 0.4,
        "description": "Futuro do Cosmos - resolutivo, cíclico"
    },
]


def generate_chapter_music(config, output_dir):
    """Gera música para um capítulo usando ffmpeg/lavfi"""
    
    name = config["name"]
    duration = config["duration_sec"]
    base = config["base_freq"]
    intervals = config["intervals"]
    lfo = config["lfo_rate"]
    filt = config["filter_freq"]
    rev = config["reverb"]
    
    output_file = Path(output_dir) / f"music_{name}.wav"
    
    # Construir senoidais
    sines = []
    for i, interval in enumerate(intervals):
        freq = base * interval
        amp = 0.04 / (i + 1)  # harmônicos mais baixos mais altos
        sines.append(f"sine=frequency={freq:.2f}:amplitude={amp:.4f}")
    
    sine_chain = '+'.join(sines)
    
    # Filter chain: soma → lowpass → LFO tremolo → reverb → gain
    filter_complex = (
        f"{sine_chain},"
        f"lowpass=f={filt}:width_type=h:width=100,"
        f"tremolo=f={lfo}:d=0.3,"
        f"aecho=0.8:0.9:{int(1000*rev)}:0.3,"
        f"highpass=f=30,"
        f"volume=0.25"
    )
    
    cmd = [
        'ffmpeg', '-y', '-f', 'lavfi',
        '-i', f"{filter_complex}:duration={duration}:sample_rate=48000",
        '-c:a', 'pcm_s16le',
        '-ar', '48000',
        str(output_file)
    ]
    
    print(f"  Gerando {name} ({duration/60:.0f}min) - {config['description']}...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    
    if result.returncode != 0:
        print(f"    ❌ Erro: {result.stderr[:200]}")
        return False
    
    # Verificar arquivo
    size = output_file.stat().st_size
    print(f"    ✓ {output_file.name} ({size/1024/1024:.1f} MB)")
    return True


def create_master_mix(output_dir):
    """Concatena todas as músicas em um master contínuo"""
    print("\n🎵 Criando master contínuo (music_master.wav)...")
    
    # Lista de arquivos em ordem
    files = []
    for config in CHAPTER_CONFIGS:
        f = Path(output_dir) / f"music_{config['name']}.wav"
        if f.exists():
            files.append(f)
    
    if not files:
        print("  ❌ Nenhum arquivo de música encontrado")
        return False
    
    # Criar lista para concat
    concat_list = Path(output_dir) / "concat_list.txt"
    with open(concat_list, 'w') as f:
        for file in files:
            f.write(f"file '{file.absolute()}'\n")
    
    master_file = Path(output_dir) / "music_master.wav"
    cmd = [
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
        '-i', str(concat_list),
        '-c:a', 'copy',
        str(master_file)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        size = master_file.stat().st_size
        print(f"  ✓ Master criado: {master_file.name} ({size/1024/1024:.1f} MB)")
        return True
    else:
        print(f"  ❌ Erro no master: {result.stderr}")
        return False


def main():
    project_dir = Path(__file__).parent
    output_dir = project_dir / "music_stems"
    output_dir.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("🎵 GERADOR DE MÚSICA DE FUNDO - Documentário 90min")
    print("=" * 60)
    print(f"📁 Pasta de saída: {output_dir}")
    print(f"📋 Capítulos: {len(CHAPTER_CONFIGS)}")
    print(f"⏱️  Duração total: {sum(c['duration_sec'] for c in CHAPTER_CONFIGS)/60:.0f} min")
    print()
    
    # Verificar ffmpeg
    if not shutil.which('ffmpeg'):
        print("❌ ffmpeg não encontrado. Instale: apt install ffmpeg / brew install ffmpeg")
        sys.exit(1)
    
    import shutil
    
    # Gerar cada capítulo
    success = 0
    for config in CHAPTER_CONFIGS:
        if generate_chapter_music(config, output_dir):
            success += 1
    
    print(f"\n✅ {success}/{len(CHAPTER_CONFIGS)} tracks gerados")
    
    # Criar master
    if success > 0:
        create_master_mix(output_dir)
    
    print("\n📋 Licença: CC0 (Domínio Público - gerado algoritmicamente)")
    print("📄 Use livremente no documentário.")
    print(f"\n🎧 Arquivos em: {output_dir}")
    print("   - music_cap1_cosmologia.wav ... music_cap9_futuro.wav")
    print("   - music_master.wav (contínuo, 90 min)")


if __name__ == '__main__':
    main()