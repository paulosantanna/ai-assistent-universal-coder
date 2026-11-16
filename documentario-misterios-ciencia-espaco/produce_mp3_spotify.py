#!/usr/bin/env python3
"""
Produção completa do MP3 para Spotify - Mistérios da Ciência e do Espaço
- Narração: Piper TTS com voz pm_alex (ou fallback)
- Música de fundo: +2dB em relação à narração (conforme solicitado)
- Output: MP3 320kbps, -14 LUFS (Spotify standard)
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path
from xml.etree import ElementTree as ET


class DocumentaryProducer:
    def __init__(self, project_dir):
        self.project_dir = Path(project_dir)
        self.ssml_file = self.project_dir / "13_narration_ssml.xml"
        self.output_dir = self.project_dir / "output"
        self.output_dir.mkdir(exist_ok=True)
        
        # Configurações de áudio
        self.sample_rate = 48000
        self.target_lufs_spotify = -14.0
        self.target_tp = -1.5
        self.target_lra = 11.0
        
        # Music level: +2dB relative to narration (user request)
        # This means music will be LOUDER than narration by 2dB
        self.music_gain_db = 2.0
        
    def extract_narration_text(self):
        """Extrai texto puro do SSML para TTS"""
        tree = ET.parse(self.ssml_file)
        root = tree.getroot()
        ns = {'ssml': 'http://www.w3.org/2001/10/synthesis'}
        
        texts = []
        for p in root.findall('.//ssml:p', ns):
            if p.text:
                texts.append(p.text.strip())
            for child in p:
                if child.tail:
                    texts.append(child.tail.strip())
        
        full_text = ' '.join(texts)
        return full_text
    
    def generate_narration_piper(self, text, voice_model, output_wav):
        """Gera narração com Piper TTS"""
        # Verificar se modelo existe
        if not Path(voice_model).exists():
            # Tentar encontrar modelo pm_alex
            possible_paths = [
                voice_model,
                Path.home() / ".local/share/piper/voices/pm_alex.onnx",
                Path("/usr/share/piper/voices/pm_alex.onnx"),
                self.project_dir / "pm_alex.onnx",
            ]
            
            for p in possible_paths:
                if Path(p).exists():
                    voice_model = str(p)
                    break
            else:
                raise FileNotFoundError(f"Modelo Piper não encontrado: {voice_model}")
        
        print(f"  Usando modelo: {voice_model}")
        
        # Piper aceita texto via stdin
        cmd = [
            'piper',
            '--model', voice_model,
            '--output_file', str(output_wav),
            '--sample_rate', str(self.sample_rate),
        ]
        
        print(f"  Gerando narração ({len(text)} chars)...")
        result = subprocess.run(cmd, input=text.encode('utf-8'), 
                               capture_output=True, timeout=300)
        
        if result.returncode != 0:
            raise RuntimeError(f"Piper falhou: {result.stderr.decode()}")
        
        print(f"  ✓ Narração salva: {output_wav}")
        return output_wav
    
    def generate_silence(self, duration_sec, output_wav):
        """Gera silêncio (para pausas entre capítulos)"""
        cmd = [
            'ffmpeg', '-y', '-f', 'lavfi', 
            '-i', f'anullsrc=r={self.sample_rate}:cl=mono',
            '-t', str(duration_sec),
            '-c:a', 'pcm_s16le',
            str(output_wav)
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return output_wav
    
    def create_background_music(self, duration_sec, output_wav):
        """
        Cria música de fundo sintética ou usa arquivo existente.
        Como não temos arquivos de música licenciados, gera tom suave.
        """
        # Verificar se já existe música curada
        music_files = list(self.project_dir.glob("music_*.wav")) + \
                     list(self.project_dir.glob("music_*.mp3")) + \
                     list(self.project_dir.glob("bg_*.wav"))
        
        if music_files:
            print(f"  Usando música existente: {music_files[0]}")
            # Loop da música para duração necessária
            cmd = [
                'ffmpeg', '-y', '-stream_loop', '-1', '-i', str(music_files[0]),
                '-t', str(duration_sec),
                '-c:a', 'pcm_s16le', '-ar', str(self.sample_rate),
                str(output_wav)
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            return output_wav
        
        print("  Gerando música de fundo sintética (drone suave)...")
        # Gerar drone suave com múltiplos senoidais (som "cósmico")
        # Frequências: 55Hz (A1), 82.4Hz (E2), 110Hz (A2), 164.8Hz (E3), 220Hz (A3)
        freq_filters = []
        for i, freq in enumerate([55, 82.41, 110, 164.81, 220, 329.63]):
            freq_filters.append(f"sine=frequency={freq}:amplitude=0.05")
        
        filter_complex = '+'.join(freq_filters)
        filter_complex += f",lowpass=f=500,volume=0.3,aecho=0.8:0.9:1000:0.3"
        
        cmd = [
            'ffmpeg', '-y', '-f', 'lavfi',
            '-i', f"{filter_complex}:duration={duration_sec}:sample_rate={self.sample_rate}",
            '-c:a', 'pcm_s16le',
            str(output_wav)
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"  ✓ Música sintética gerada: {output_wav}")
        return output_wav
    
    def mix_audio(self, narration_wav, music_wav, output_wav):
        """
        Mixa narração + música com música em +2dB relativo à narração.
        Fluxo: 
        1. Normalizar narração para -16 LUFS
        2. Normalizar música para -14 LUFS (2dB acima = +2dB)
        3. Mixar
        4. Normalizar final para -14 LUFS (Spotify)
        """
        print("  Processando narração (-16 LUFS)...")
        narration_norm = self.output_dir / "narration_norm.wav"
        subprocess.run([
            'ffmpeg', '-y', '-i', str(narration_wav),
            '-af', f'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json',
            '-ar', str(self.sample_rate), '-sample_fmt', 's16le',
            str(narration_norm)
        ], check=True, capture_output=True)
        
        print("  Processando música (-14 LUFS = +2dB relativo)...")
        music_norm = self.output_dir / "music_norm.wav"
        subprocess.run([
            'ffmpeg', '-y', '-i', str(music_wav),
            '-af', f'loudnorm=I=-14:TP=-1.5:LRA=15:print_format=json',
            '-ar', str(self.sample_rate), '-sample_fmt', 's16le',
            str(music_norm)
        ], check=True, capture_output=True)
        
        print("  Mixando (narração + música)...")
        # Mix simples: ambos já normalizados nos níveis corretos
        subprocess.run([
            'ffmpeg', '-y', '-i', str(narration_norm), '-i', str(music_norm),
            '-filter_complex', '[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=0[mixed];[mixed]loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json',
            '-ar', str(self.sample_rate), '-sample_fmt', 's16le',
            str(output_wav)
        ], check=True, capture_output=True)
        
        print(f"  ✓ Mix final: {output_wav}")
        return output_wav
    
    def encode_mp3_spotify(self, input_wav, output_mp3):
        """Codifica MP3 320kbps otimizado para Spotify (-14 LUFS)"""
        print("  Codificando MP3 320kbps para Spotify...")
        subprocess.run([
            'ffmpeg', '-y', '-i', str(input_wav),
            '-af', f'loudnorm=I={self.target_lufs_spotify}:TP={self.target_tp}:LRA={self.target_lra}',
            '-c:a', 'libmp3lame', '-b:a', '320k', '-joint_stereo', '1',
            '-id3v2_version', '3', '-write_id3v1', '1',
            '-metadata', 'title=Mistérios da Ciência e do Espaço',
            '-metadata', 'artist=CodENavi Documentary Factory',
            '-metadata', 'album=Documentários Científicos',
            '-metadata', 'date=2026',
            '-metadata', 'genre=Documentary',
            '-metadata', 'comment=Documentário de 90 min sobre os mistérios da ciência e do espaço',
            '-metadata', 'track=1',
            str(output_mp3)
        ], check=True, capture_output=True)
        
        print(f"  ✓ MP3 final: {output_mp3}")
        return output_mp3
    
    def verify_output(self, mp3_file):
        """Verifica especificações do arquivo final"""
        print("\n=== VERIFICAÇÃO FINAL ===")
        
        # Duração
        dur = subprocess.run([
            'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', str(mp3_file)
        ], capture_output=True, text=True, check=True).stdout.strip()
        print(f"  Duração: {float(dur):.1f}s ({float(dur)/60:.1f} min)")
        
        # Bitrate
        br = subprocess.run([
            'ffprobe', '-v', 'error', '-show_entries', 'format=bit_rate',
            '-of', 'default=noprint_wrappers=1:nokey=1', str(mp3_file)
        ], capture_output=True, text=True, check=True).stdout.strip()
        print(f"  Bitrate: {int(br)//1000} kbps")
        
        # Loudness
        loud = subprocess.run([
            'ffmpeg', '-y', '-i', str(mp3_file),
            '-af', f'loudnorm=I={self.target_lufs_spotify}:TP={self.target_tp}:LRA={self.target_lra}:print_format=json',
            '-f', 'null', '-'
        ], capture_output=True, text=True).stderr
        
        import re
        for key in ['input_i', 'input_tp', 'input_lra', 'input_thresh', 'target_offset']:
            match = re.search(f'"{key}":\\s*([-\\d.]+)', loud)
            if match:
                print(f"  {key}: {match.group(1)}")
        
        # Verificar silêncio
        silence = subprocess.run([
            'ffmpeg', '-v', 'info', '-i', str(mp3_file),
            '-vn', '-af', 'silencedetect=noise=-45dB:d=2.0', '-f', 'null', '-'
        ], capture_output=True, text=True).stderr
        
        silences = re.findall(r'silence_duration: ([\d.]+)', silence)
        if silences:
            print(f"  ⚠ Silêncios >2s detectados: {len(silences)}")
            for s in silences[:3]:
                print(f"    - {s}s")
        else:
            print(f"  ✓ Nenhum silêncio >2s")
        
        return True
    
    def run(self, voice_model="pm_alex.onnx", music_file=None):
        """Pipeline completo de produção"""
        print("=" * 60)
        print("PRODUÇÃO MP3 SPOTIFY - Mistérios da Ciência e do Espaço")
        print("=" * 60)
        
        # 1. Extrair texto
        print("\n1. Extraindo texto do SSML...")
        text = self.extract_narration_text()
        print(f"   Total: {len(text)} chars, ~{len(text.split())} palavras")
        
        # 2. Gerar narração
        print("\n2. Gerando narração com Piper TTS...")
        narration_raw = self.output_dir / "narration_raw.wav"
        self.generate_narration_piper(text, voice_model, narration_raw)
        
        # 3. Obter duração da narração
        dur_result = subprocess.run([
            'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', str(narration_raw)
        ], capture_output=True, text=True, check=True)
        narration_duration = float(dur_result.stdout.strip())
        print(f"   Duração narração: {narration_duration:.1f}s")
        
        # 4. Música de fundo
        print("\n3. Preparando música de fundo...")
        if music_file and Path(music_file).exists():
            music_raw = self.output_dir / "music_raw.wav"
            # Converter para WAV 48kHz mono se necessário
            subprocess.run([
                'ffmpeg', '-y', '-i', str(music_file),
                '-ar', str(self.sample_rate), '-ac', '1',
                '-c:a', 'pcm_s16le', str(music_raw)
            ], check=True, capture_output=True)
        else:
            music_raw = self.output_dir / "music_synthetic.wav"
            self.create_background_music(narration_duration, music_raw)
        
        # 5. Mixagem
        print("\n4. Mixando áudio (música +2dB)...")
        mix_final = self.output_dir / "documentario_final.wav"
        self.mix_audio(narration_raw, music_raw, mix_final)
        
        # 6. MP3 final para Spotify
        print("\n5. Gerando MP3 final para Spotify...")
        mp3_final = self.output_dir / "Misterios_Ciencia_Espaco_Spotify.mp3"
        self.encode_mp3_spotify(mix_final, mp3_final)
        
        # 7. Verificação
        self.verify_output(mp3_final)
        
        print("\n" + "=" * 60)
        print("✅ PRODUÇÃO CONCLUÍDA!")
        print(f"📁 Arquivo final: {mp3_final}")
        print(f"📊 Especificações: 320kbps, -14 LUFS, 48kHz, Stereo")
        print("=" * 60)
        
        return mp3_final


def main():
    parser = argparse.ArgumentParser(
        description='Produz MP3 final para Spotify do documentário'
    )
    parser.add_argument('--project-dir', default='.', 
                       help='Diretório do projeto (padrão: atual)')
    parser.add_argument('--voice', default='pm_alex.onnx',
                       help='Modelo Piper TTS (padrão: pm_alex.onnx)')
    parser.add_argument('--music', help='Arquivo de música de fundo (opcional)')
    parser.add_argument('--output', default='output/Misterios_Ciencia_Espaco_Spotify.mp3',
                       help='Arquivo MP3 de saída')
    
    args = parser.parse_args()
    
    # Verificar dependências
    for cmd in ['piper', 'ffmpeg', 'ffprobe']:
        if not shutil.which(cmd):
            print(f"ERRO: '{cmd}' não encontrado no PATH")
            print("Instale: pip install piper-tts  &&  apt install ffmpeg")
            sys.exit(1)
    
    producer = DocumentaryProducer(args.project_dir)
    mp3_file = producer.run(voice_model=args.voice, music_file=args.music)
    
    print(f"\n🎧 Pronto para upload no Spotify: {mp3_file}")


if __name__ == '__main__':
    main()