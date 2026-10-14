"""Build deterministic offline meeting outputs from a single validated call.json."""
import argparse
import html
import json
import math
from pathlib import Path
import sys

def stamp(seconds, comma=False):
    ms = round(float(seconds) * 1000)
    return f'{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02}{"," if comma else "."}{ms % 1000:03}'

def validate(call):
    duration = float(call['media']['duration'])
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError('Media duration must be finite and positive')
    previous = 0
    for segment in call['segments']:
        start, end = float(segment['start']), float(segment['end'])
        if not (math.isfinite(start) and math.isfinite(end)) or start < previous or end <= start or end > duration + .1:
            raise ValueError('Invalid/unordered segment timestamps')
        if segment['speaker'] not in call['speakers'] or not isinstance(segment['text'], str):
            raise ValueError('Unknown speaker or nontext segment')
        if not isinstance(segment.get('offtopic', False), bool):
            raise ValueError('offtopic must be boolean')
        previous = start
    previous = -1
    for topic in call.get('topics', []):
        start = float(topic['start'])
        if not math.isfinite(start) or start < 0 or start <= previous or start >= duration or not isinstance(topic['title'], str):
            raise ValueError('Topics must have text titles and increasing timestamps within media')
        previous = start
    for speaker in call['speakers'].values():
        if not isinstance(speaker.get('confirmed', False), bool):
            raise ValueError('Speaker confirmed must be boolean')
    if not call['segments']:
        raise ValueError('No segments')
    return duration

def build(call, out_dir):
    duration = validate(call)
    out_dir.mkdir(parents=True, exist_ok=True)
    segments = [s for s in call['segments'] if not s.get('offtopic', False)]
    speakers = call['speakers']
    def speaker_name(key):
        record = speakers[key]
        return record.get('name', key) if record.get('confirmed', False) else key
    meeting = call.get('meeting', {})
    topics = call.get('topics', [])
    transcript = '\n\n'.join(f'[{stamp(s["start"])}] {speaker_name(s["speaker"])}: {s["text"]}' for s in segments)
    subtitles = '\n\n'.join(f'{i}\n{stamp(s["start"], True)} --> {stamp(s["end"], True)}\n{speaker_name(s["speaker"])}: {s["text"]}' for i, s in enumerate(segments, 1))
    vtt = 'WEBVTT\n\n' + '\n\n'.join(f'{stamp(s["start"])} --> {stamp(s["end"])}\n{speaker_name(s["speaker"])}: {s["text"].replace("-->", "→")}' for s in segments) + '\n'
    chapters = 'WEBVTT\n\n' + '\n\n'.join(f'{stamp(t["start"])} --> {stamp(topics[i + 1]["start"] if i + 1 < len(topics) else duration)}\n{t["title"].replace("-->", "→")}' for i, t in enumerate(topics)) + '\n'
    minutes = meeting.get('ata_md', '')
    if meeting.get('acoes'):
        minutes += '\n\n## Ações\n\n' + '\n'.join('- ' + str(a.get('tarefa', '')) + ' — ' + str(a.get('responsavel', 'não informado')) + ' — ' + str(a.get('prazo', 'não informado')) for a in meeting['acoes'])
    summary = meeting.get('resumo_md', '')
    if meeting.get('glossario'):
        summary += '\n\n## Glossário\n\n' + '\n'.join('- ' + str(g.get('sigla', '')) + ': ' + str(g.get('expansao', '')) + ' — ' + str(g.get('nota', '')) for g in meeting['glossario'])
    filename = html.escape(str(call['media'].get('filename', 'gravação local')))
    topic_html = ''.join(f'<li><button type="button" data-time="{float(t["start"])}">{html.escape(t["title"])}</button></li>' for t in topics)
    segment_html = ''.join(f'<p><button type="button" data-time="{float(s["start"])}">{stamp(s["start"])}</button> <strong>{html.escape(speaker_name(s["speaker"]))}</strong>: {html.escape(s["text"])}</p>' for s in segments)
    document = f'''<!doctype html>
<html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ata e transcrição</title>
<style>body{{font:16px/1.5 system-ui;max-width:1100px;margin:auto;padding:24px;color:#222}}video{{width:100%;max-height:60vh}}button,input{{font:inherit}}button{{padding:8px;margin:4px;cursor:pointer}}:focus-visible{{outline:3px solid #075ac5}}pre{{white-space:pre-wrap;overflow-wrap:anywhere}}</style>
<h1>Ata e transcrição</h1><p>Gravação: {filename}. Trechos omitidos da documentação: {len(call['segments']) - len(segments)}. A seleção do arquivo mantém o vídeo original, inclusive esses trechos.</p>
<label>Selecionar vídeo local <input id="media" type="file" accept="video/*,.mkv"></label><p id="status" role="status">Selecione a gravação para ativar a navegação.</p><video id="player" controls preload="metadata"></video>
<nav aria-label="Tópicos"><h2>Tópicos</h2><ol>{topic_html}</ol></nav><section><h2>Resumo e glossário</h2><pre>{html.escape(summary)}</pre></section><section><h2>Ata e ações</h2><pre>{html.escape(minutes)}</pre></section><section><h2>Transcrição</h2>{segment_html}</section>
<script>
const player=document.getElementById('player'), status=document.getElementById('status');let mediaURL;
document.getElementById('media').addEventListener('change',event=>{{const file=event.target.files[0];if(!file)return;if(mediaURL)URL.revokeObjectURL(mediaURL);mediaURL=URL.createObjectURL(file);player.src=mediaURL;status.textContent='Vídeo selecionado: '+file.name;}});
player.addEventListener('error',()=>{{status.textContent='O navegador não decodifica este arquivo. Selecione uma cópia em formato compatível; os documentos continuam disponíveis.';}});
document.querySelectorAll('[data-time]').forEach(button=>button.addEventListener('click',()=>{{if(!player.src){{status.textContent='Selecione o vídeo local primeiro.';return;}}player.currentTime=Number(button.dataset.time);player.play().catch(()=>{{status.textContent='Use o controle Reproduzir do vídeo.';}});}}));
window.addEventListener('pagehide',()=>{{if(mediaURL)URL.revokeObjectURL(mediaURL);}});
</script></html>'''
    outputs = {'index.html': document, 'ata.md': minutes, 'resumo.md': summary, 'transcricao.md': transcript, 'legendas.srt': subtitles, 'legendas.vtt': vtt, 'capitulos.vtt': chapters}
    for name, content in outputs.items():
        (out_dir / name).write_text(content.rstrip() + '\n', encoding='utf-8')
    return outputs

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--call', type=Path, required=True)
    parser.add_argument('--out-dir', type=Path, required=True)
    args = parser.parse_args()
    try:
        call = json.loads(args.call.read_text(encoding='utf-8'))
        build(call, args.out_dir)
        print('Built seven offline outputs from call.json')
        return 0
    except (ValueError, OSError, KeyError, TypeError) as error:
        print('Build blocked: ' + str(error), file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
