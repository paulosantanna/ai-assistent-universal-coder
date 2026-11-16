"""Optional local adapters. No model weights or third-party Python packages are bundled."""
from __future__ import annotations

import argparse
import copy
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

import context_gate
from studio import probe, read, run, validate, write


def request(base, route, payload=None):
    parts = urllib.parse.urlsplit(base)
    if parts.scheme != 'http' or parts.hostname not in ('127.0.0.1', 'localhost', '::1'):
        raise ValueError('local_provider_url_required')
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(base.rstrip('/') + route, data=data,
                                 headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=600) as response:
        return json.load(response)


def research(project, source_file):
    # Sources are inspected by the session, or supplied as a reviewed local corpus.
    sources = read(source_file)
    if not isinstance(sources, list) or not sources:
        raise ValueError('reviewed_source_corpus_required')
    if any(not all(s.get(k) for k in ('id', 'url', 'accessed', 'excerpt')) for s in sources):
        raise ValueError('source_id_url_accessed_excerpt_required')
    project['sources'] = sources


def script(project, base, model):
    # Bounded chapters avoid a single 90-minute model completion/context overflow.
    scenes = []
    remaining = project['duration']
    chapter = 0
    while remaining > 0:
        seconds = min(120, remaining)
        instructions = {
            'task': 'Escreva cenas para documentário científico em PT-BR; retorne JSON com scenes.',
            'topic': project['topic'], 'chapter': chapter, 'total_seconds': project['duration'],
            'chapter_seconds': seconds, 'sources': project['sources'],
            'previous_summary': [s['narration'] for s in scenes[-2:]],
            'rules': 'Use somente fatos nos excerpts. Não invente fontes nem certeza. Cada cena 10 segundos, '
                     'narração 18 a 24 palavras, visual descreve precisamente o que é narrado, '
                     'claims lista IDs das fontes. Arte HQ detalhada cartoon cinematográfica sem balões. '
                     'Não repetir cenas para preencher duração. Estruture começo, explicação e conclusão '
                     'considerando chapter e total_seconds. Sem áudio ou imagens ainda.',
            'scene_schema': {'duration': 10, 'narration': 'texto', 'visual': 'descrição',
                             'claims': ['source-id'], 'transition': 'cut',
                             'layers': [{'path': 'placeholder.png', 'kind': 'image'}]},
        }
        response = request(base, '/api/chat', {'model': model, 'stream': False, 'format': 'json',
                                              'messages': [{'role': 'user', 'content': json.dumps(instructions, ensure_ascii=False)}]})
        batch = json.loads(response['message']['content'])
        if not isinstance(batch, dict) or 'scenes' not in batch:
            raise ValueError('model_missing_scenes_key: revise prompt or model')
        batch = batch['scenes']
        if not isinstance(batch, list):
            raise ValueError('model_scenes_not_list: revise prompt or model')
        defaults = {'duration': 10, 'narration': '', 'visual': '', 'claims': [],
                    'transition': 'cut', 'layers': [{'path': 'placeholder.png', 'kind': 'image'}]}
        for scene in batch:
            if not isinstance(scene, dict):
                raise ValueError('model_scene_not_object: revise prompt or model')
            for key, value in defaults.items():
                scene.setdefault(key, value)
            if isinstance(scene.get('duration'), str):
                scene['duration'] = int(float(scene['duration']))
        if abs(sum(s['duration'] for s in batch) - seconds) > 0.1:
            raise ValueError('model_chapter_duration_mismatch: revise prompt or scenes')
        for scene in batch:
            scene['chapter'] = chapter
        scenes.extend(batch)
        chapter += 1
        remaining -= seconds
    project['scenes'] = scenes


def comfy_image(base, workflow, prompt, seed):
    graph = copy.deepcopy(workflow)
    found = False
    for node in graph.values():
        for key, value in node.get('inputs', {}).items():
            if value == '__PROMPT__':
                node['inputs'][key] = prompt
                found = True
            elif value == '__SEED__':
                node['inputs'][key] = seed
    if not found:
        raise ValueError('comfy_api_workflow_requires___PROMPT___binding')
    result = request(base, '/prompt', {'prompt': graph})
    if result.get('node_errors') or not result.get('prompt_id'):
        raise ValueError('comfy_workflow_rejected')
    prompt_id = result['prompt_id']
    deadline = time.monotonic() + 1800
    while time.monotonic() < deadline:
        history = request(base, '/history/' + prompt_id).get(prompt_id)
        if history:
            if history.get('status', {}).get('status_str') == 'error':
                raise ValueError('comfy_generation_failed')
            images = [im for output in history.get('outputs', {}).values() for im in output.get('images', [])]
            if not images:
                raise ValueError('comfy_missing_saveimage_output')
            image = images[-1]
            query = urllib.parse.urlencode({k: image[k] for k in ('filename', 'subfolder', 'type') if k in image})
            with urllib.request.urlopen(base.rstrip('/') + '/view?' + query, timeout=120) as response:
                return response.read()
        time.sleep(2)
    raise ValueError('comfy_timeout: inspect queue before retry; job may still be running')


def assets(project, root, base, workflow_file, foreground_file):
    workflow = read(workflow_file)
    foreground = read(foreground_file) if foreground_file else None
    folder = root / 'assets'
    folder.mkdir(exist_ok=True)
    for i, scene in enumerate(project['scenes']):
        path = folder / f'{i:04}-background.png'
        # O prompt exato é a prova do vínculo roteiro→imagem (trava de contexto visual).
        background_prompt = (scene['visual'] + ', detailed cinematic comic art, '
                             'no text, no speech balloons, composition with generous safe margins')
        generated = not path.exists()
        if generated:
            data = comfy_image(base, workflow, background_prompt, 1000 + i)
            path.write_bytes(data)
        context_gate.record_generation(root, path.relative_to(root).as_posix(), i,
                                       'background', background_prompt, 1000 + i,
                                       generated=generated)
        scene['layers'] = [{'path': path.relative_to(root).as_posix(), 'kind': 'image',
                            'scale': 1.08, 'zoom_end': 1.04, 'x0': -20, 'x1': -35, 'y0': -20, 'y1': -30}]
        scene['layer_separation'] = 'pending: provide transparent foreground/effects layers before final review'
        if foreground:
            subject = folder / f'{i:04}-foreground.png'
            subject_prompt = (scene['visual'] + ', isolated main subject, '
                              'transparent background, no text, detailed comic art, same visual style')
            subject_generated = not subject.exists()
            if subject_generated:
                subject.write_bytes(comfy_image(base, foreground, subject_prompt, 1000 + i))
            context_gate.record_generation(root, subject.relative_to(root).as_posix(), i,
                                           'foreground', subject_prompt, 1000 + i,
                                           generated=subject_generated)
            alpha = run(['ffmpeg', '-v', 'error', '-i', str(subject), '-vf',
                         'alphaextract,scale=32:32', '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'])
            if not alpha or min(alpha) == 255 or max(alpha) == 0:
                raise ValueError('foreground_requires_real_transparency: configure segmentation/matting workflow')
            scene['layers'].append({'path': subject.relative_to(root).as_posix(), 'kind': 'image',
                                    'scale': 1, 'zoom_end': 1.02, 'x0': 0, 'x1': 15, 'y0': 0, 'y1': -10})
            scene['layer_separation'] = 'generated: requires visual continuity review'


def voice(project, root, executable, model):
    folder = root / 'audio'
    folder.mkdir(exist_ok=True)
    for i, scene in enumerate(project['scenes']):
        raw, target = folder / f'{i:04}-raw.wav', folder / f'{i:04}.wav'
        run([executable, '-m', str(model), '-f', str(raw), '--', scene['narration']])
        actual = float(probe(raw)['format']['duration'])
        tempo = actual / scene['duration']
        if not 0.85 <= tempo <= 1.2:
            raise ValueError(f'voice_timing_out_of_range_scene_{i}: rewrite narration; ratio={tempo:.2f}')
        run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-af',
             f'atempo={tempo},loudnorm=I=-16:TP=-1.5:LRA=11,apad',
             '-t', str(scene['duration']), '-ar', '48000', str(target)])
        scene['audio'] = target.relative_to(root).as_posix()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=('research', 'script', 'assets', 'voice'))
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--sources', type=Path)
    parser.add_argument('--url')
    parser.add_argument('--model')
    parser.add_argument('--workflow', type=Path)
    parser.add_argument('--foreground-workflow', type=Path)
    parser.add_argument('--piper', default='piper')
    args = parser.parse_args()
    file = args.project.resolve()
    project = read(file)
    if args.stage == 'research':
        research(project, args.sources)
    elif args.stage == 'script':
        script(project, args.url, args.model)
        validate(project, file.parent, media=False)
    elif args.stage == 'assets':
        assets(project, file.parent, args.url, args.workflow, args.foreground_workflow)
    else:
        voice(project, file.parent, args.piper, args.model)
    write(file, project)


if __name__ == '__main__':
    main()
