#!/usr/bin/env python3
"""
Gerador de Narração para Documentário - Mistérios da Ciência e do Espaço
Suporta: Piper TTS (local), Azure Speech, AWS Polly, Google Cloud TTS
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree as ET


def ssml_to_text(ssml_file):
    """Extrai texto puro do SSML para TTS que não suporta SSML"""
    tree = ET.parse(ssml_file)
    root = tree.getroot()
    
    # Namespace SSML
    ns = {'ssml': 'http://www.w3.org/2001/10/synthesis'}
    
    texts = []
    for p in root.findall('.//ssml:p', ns):
        if p.text:
            texts.append(p.text.strip())
        for child in p:
            if child.tail:
                texts.append(child.tail.strip())
    
    return ' '.join(texts)


def split_by_chapters(text, ssml_file):
    """Divide texto por capítulos usando marcadores do SSML"""
    tree = ET.parse(ssml_file)
    root = tree.getroot()
    ns = {'ssml': 'http://www.w3.org/2001/10/synthesis'}
    
    chapters = {}
    current_chapter = None
    current_text = []
    
    for elem in root.iter():
        if elem.tag.endswith('mark') and 'name' in elem.attrib:
            name = elem.attrib['name']
            if name.startswith('cap') and '_cena1' in name:
                if current_chapter and current_text:
                    chapters[current_chapter] = ' '.join(current_text)
                current_chapter = name.replace('_cena1', '')
                current_text = []
        elif elem.tag.endswith('p') and elem.text:
            current_text.append(elem.text.strip())
        elif elem.tail and elem.tail.strip():
            current_text.append(elem.tail.strip())
    
    if current_chapter and current_text:
        chapters[current_chapter] = ' '.join(current_text)
    
    return chapters


def generate_with_piper(text, output_file, model_path, speaker_id=0):
    """Gera áudio com Piper TTS (local)"""
    cmd = [
        'piper',
        '--model', model_path,
        '--output_file', output_file,
        '--speaker', str(speaker_id),
    ]
    
    # Piper aceita stdin para texto
    proc = subprocess.run(cmd, input=text.encode('utf-8'), capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(f"Piper failed: {proc.stderr.decode()}")
    return True


def generate_with_azure(text, output_file, voice, subscription_key, region):
    """Gera áudio com Azure Speech Service"""
    try:
        import azure.cognitiveservices.speech as speechsdk
    except ImportError:
        raise RuntimeError("azure-cognitiveservices-speech não instalado. Use: pip install azure-cognitiveservices-speech")
    
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    speech_config.speech_synthesis_voice_name = voice
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff48Khz16BitMonoPcm)
    
    # SSML para controle fino
    ssml = f"""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="pt-BR">
    <voice name="{voice}">
        <prosody rate="0%" pitch="0%" volume="medium">
            {text}
        </prosody>
    </voice>
    </speak>"""
    
    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    
    result = synthesizer.speak_ssml_async(ssml).get()
    
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Áudio gerado: {output_file}")
        return True
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = result.cancellation_details
        raise RuntimeError(f"TTS cancelado: {cancellation.reason} - {cancellation.error_details}")
    
    return False


def generate_with_aws(text, output_file, voice, region):
    """Gera áudio com AWS Polly"""
    try:
        import boto3
    except ImportError:
        raise RuntimeError("boto3 não instalado. Use: pip install boto3")
    
    polly = boto3.client('polly', region_name=region)
    
    response = polly.synthesize_speech(
        Text=text,
        TextType='ssml' if '<speak>' in text else 'text',
        VoiceId=voice,
        OutputFormat='pcm',
        SampleRate='48000'
    )
    
    if 'AudioStream' in response:
        with open(output_file, 'wb') as f:
            f.write(response['AudioStream'].read())
        # Converter raw PCM para WAV
        convert_pcm_to_wav(output_file, output_file.replace('.wav', '_raw.pcm'))
        os.rename(output_file.replace('.wav', '_raw.pcm'), output_file)
        return True
    raise RuntimeError("Erro na síntese AWS Polly")


def generate_with_google(text, output_file, voice_name, credentials_path):
    """Gera áudio com Google Cloud TTS"""
    try:
        from google.cloud import texttospeech
    except ImportError:
        raise RuntimeError("google-cloud-texttospeech não instalado. Use: pip install google-cloud-texttospeech")
    
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
    client = texttospeech.TextToSpeechClient()
    
    synthesis_input = texttospeech.SynthesisInput(ssml=text if '<speak>' in text else None, text=text if '<speak>' not in text else None)
    voice = texttospeech.VoiceSelectionParams(language_code='pt-BR', name=voice_name)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000
    )
    
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    
    with open(output_file, 'wb') as f:
        f.write(response.audio_content)
    return True


def convert_pcm_to_wav(wav_file, pcm_file, sample_rate=48000, channels=1, sample_width=2):
    """Converte raw PCM para WAV"""
    import wave
    with open(pcm_file, 'rb') as pcm_f:
        pcm_data = pcm_f.read()
    with wave.open(wav_file, 'wb') as wav_f:
        wav_f.setnchannels(channels)
        wav_f.setsampwidth(sample_width)
        wav_f.setframerate(sample_rate)
        wav_f.writeframes(pcm_data)


def main():
    parser = argparse.ArgumentParser(description='Gerar narração para documentário')
    parser.add_argument('--ssml', default='13_narration_ssml.xml', help='Arquivo SSML de entrada')
    parser.add_argument('--output-dir', default='narration_segments', help='Diretório de saída')
    parser.add_argument('--engine', choices=['piper', 'azure', 'aws', 'google'], default='piper', help='Motor TTS')
    parser.add_argument('--voice', default='pt-BR-AntonioNeural', help='Voz (Azure: pt-BR-AntonioNeural, AWS: Thiago, Google: pt-BR-Neural2-A)')
    parser.add_argument('--piper-model', default='pt_BR-faber-medium.onnx', help='Caminho do modelo Piper')
    parser.add_argument('--azure-key', help='Azure Speech subscription key')
    parser.add_argument('--azure-region', default='eastus', help='Azure region')
    parser.add_argument('--aws-region', default='us-east-1', help='AWS region')
    parser.add_argument('--google-creds', help='Google Cloud credentials JSON path')
    parser.add_argument('--single-file', action='store_true', help='Gerar arquivo único em vez de segmentos por capítulo')
    parser.add_argument('--chapter', help='Gerar apenas capítulo específico (ex: cap1)')
    
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Carregar SSML
    if not os.path.exists(args.ssml):
        print(f"ERRO: Arquivo SSML não encontrado: {args.ssml}")
        sys.exit(1)
    
    # Dividir por capítulos
    chapters = split_by_chapters('', args.ssml)
    
    if not chapters:
        print("AVISO: Não foi possível dividir por capítulos. Usando texto completo.")
        full_text = ssml_to_text(args.ssml)
        chapters = {'full': full_text}
    
    # Filtrar capítulo se especificado
    if args.chapter:
        if args.chapter in chapters:
            chapters = {args.chapter: chapters[args.chapter]}
        else:
            print(f"Capítulo {args.chapter} não encontrado. Disponíveis: {list(chapters.keys())}")
            sys.exit(1)
    
    print(f"Capítulos a processar: {list(chapters.keys())}")
    
    # Gerar áudio para cada capítulo
    for chap_name, text in chapters.items():
        output_file = os.path.join(args.output_dir, f'{chap_name}.wav')
        print(f"\nProcessando {chap_name}... ({len(text)} chars, ~{len(text.split())} palavras)")
        
        try:
            if args.engine == 'piper':
                if not os.path.exists(args.piper_model):
                    print(f"ERRO: Modelo Piper não encontrado: {args.piper_model}")
                    print("Baixe em: https://huggingface.co/rhasspy/piper-voices/tree/main/pt/pt_BR/faber/medium")
                    sys.exit(1)
                generate_with_piper(text, output_file, args.piper_model)
            elif args.engine == 'azure':
                if not args.azure_key:
                    print("ERRO: --azure-key obrigatório para Azure TTS")
                    sys.exit(1)
                generate_with_azure(text, output_file, args.voice, args.azure_key, args.azure_region)
            elif args.engine == 'aws':
                generate_with_aws(text, output_file, args.voice, args.aws_region)
            elif args.engine == 'google':
                if not args.google_creds:
                    print("ERRO: --google-creds obrigatório para Google TTS")
                    sys.exit(1)
                generate_with_google(text, output_file, args.voice, args.google_creds)
            
            print(f"  ✓ Salvo: {output_file}")
        except Exception as e:
            print(f"  ✗ ERRO em {chap_name}: {e}")
    
    # Se single-file, concatenar
    if args.single_file and len(chapters) > 1:
        print("\nConcatenando arquivos...")
        concat_list = os.path.join(args.output_dir, 'concat_list.txt')
        with open(concat_list, 'w') as f:
            for chap_name in chapters.keys():
                f.write(f"file '{chap_name}.wav'\n")
        
        output_full = os.path.join(args.output_dir, 'narration_full.wav')
        subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', concat_list, '-c', 'copy', output_full], check=True)
        print(f"Arquivo completo: {output_full}")
    
    print("\n✓ Geração concluída!")


if __name__ == '__main__':
    main()