"""Local OpenAI-compatible inference endpoint. Only loopback, no telemetry or paid APIs."""
import gc
import json
import os
import threading
import time
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request

os.environ.setdefault('HF_HUB_DISABLE_TELEMETRY', '1')
os.environ.setdefault('DO_NOT_TRACK', '1')

app = FastAPI(title='Local GraphRAG models')
mutex = threading.RLock()
state = {'generator': None, 'tokenizer': None, 'embedder': None, 'paused': False}
MODEL = os.getenv('RGL_MODEL', 'Qwen/Qwen3-4B-Instruct-2507')
EMBEDDING = os.getenv('RGL_EMBEDDING', 'intfloat/multilingual-e5-base')


@app.middleware('http')
async def local_clients_only(request, call_next):
    from urllib.parse import urlparse

    from fastapi.responses import JSONResponse
    host = urlparse('http://' + request.headers.get('host', '')).hostname
    if request.headers.get('origin') or host not in {'127.0.0.1', 'localhost', '::1', 'testserver'}:
        return JSONResponse({'detail': 'Local service clients only'}, status_code=403)
    return await call_next(request)


def generator():
    if state['paused']:
        raise HTTPException(503, 'Inference paused while GPU training owns the device')
    if state['generator'] is None:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
        if not torch.cuda.is_available():
            raise HTTPException(503, 'CUDA is unavailable; run the runtime preflight')
        state['tokenizer'] = AutoTokenizer.from_pretrained(MODEL, trust_remote_code=False)
        state['generator'] = AutoModelForCausalLM.from_pretrained(MODEL, device_map='auto',
            quantization_config=BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type='nf4',
                                                  bnb_4bit_compute_dtype=torch.bfloat16),
            trust_remote_code=False)
        adapter = os.getenv('RGL_LLM_ADAPTER')
        if adapter:
            from peft import PeftModel
            artifact = Path(adapter).resolve()
            if not artifact.is_relative_to((Path(__file__).parent / '.state/experiments').resolve()):
                raise HTTPException(400, 'Adapter must be a local experiment artifact')
            state['generator'] = PeftModel.from_pretrained(state['generator'], artifact)
        state['generator'].eval()
    return state['generator'], state['tokenizer']


@app.get('/v1/models')
def models():
    return {'object': 'list', 'data': [{'id': MODEL, 'object': 'model'}, {'id': EMBEDDING, 'object': 'model'}],
            'weights_loaded': state['generator'] is not None, 'paused': state['paused']}


@app.post('/unload')
def unload():
    with mutex:
        state['paused'] = True
        state['generator'] = state['tokenizer'] = None
        gc.collect()
        import torch
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        return {'unloaded': True, 'paused': True}


@app.post('/resume')
def resume():
    with mutex:
        state['paused'] = False
        return {'paused': False}


@app.post('/v1/chat/completions')
async def completion(request: Request):
    import asyncio
    body = await request.json()
    if body.get('model') != MODEL or body.get('stream'):
        raise HTTPException(400, 'Only the configured local model and non-streaming completions are supported')

    def run():
        with mutex:
            import torch
            model, tokenizer = generator()
            messages = body.get('messages', [])
            if not isinstance(messages, list) or len(messages) > 50:
                raise HTTPException(400, 'Invalid messages')
            normalized = []
            for message in messages:
                if message.get('role') not in {'system', 'user', 'assistant'}:
                    raise HTTPException(400, 'Unsupported message role')
                content = message.get('content', '')
                if isinstance(content, list):
                    content = '\n'.join(part.get('text', '') for part in content if part.get('type') == 'text')
                normalized.append({'role': message['role'], 'content': str(content)})
            schema = body.get('response_format', {}).get('json_schema', {}).get('schema')
            if schema:
                normalized.insert(0, {'role': 'system', 'content': 'Return ONLY valid JSON satisfying this schema: ' + json.dumps(schema)})
            prompt = tokenizer.apply_chat_template(normalized, tokenize=False, add_generation_prompt=True)
            inputs = tokenizer(prompt, return_tensors='pt')
            if inputs.input_ids.shape[1] > 8192:
                raise HTTPException(400, 'Input exceeds the local 8192-token inference budget')
            inputs = inputs.to(model.device)
            maximum = min(4096, max(1, int(body.get('max_tokens', 1200))))
            with torch.inference_mode():
                result = model.generate(**inputs, max_new_tokens=maximum, do_sample=False)
            text = tokenizer.decode(result[0, inputs.input_ids.shape[1]:], skip_special_tokens=True)
            if schema:
                import jsonschema
                normalized = text.strip()
                if normalized.startswith('```json') and normalized.endswith('```'):
                    normalized = normalized[7:-3].strip()
                elif normalized.startswith('```') and normalized.endswith('```'):
                    normalized = normalized[3:-3].strip()
                try:
                    jsonschema.validate(json.loads(normalized), schema)
                    text = normalized
                except (ValueError, jsonschema.ValidationError) as exc:
                    failure = {'error_type': type(exc).__name__, 'output_characters': len(text),
                               'token_limit_reached': result.shape[1] - inputs.input_ids.shape[1] >= maximum,
                               'validator': getattr(exc, 'validator', None)}
                    (Path(__file__).parent / '.state/last-schema-error.json').write_text(json.dumps(failure), encoding='utf-8')
                    raise HTTPException(422, 'Local generation did not satisfy the requested JSON schema; see sanitized last-schema-error.json') from None
            return {'id': 'chatcmpl-' + uuid.uuid4().hex, 'object': 'chat.completion', 'created': int(time.time()),
                    'model': MODEL, 'choices': [{'index': 0, 'message': {'role': 'assistant', 'content': text},
                                               'finish_reason': 'stop'}],
                    'usage': {'prompt_tokens': inputs.input_ids.shape[1], 'completion_tokens': result.shape[1]-inputs.input_ids.shape[1],
                              'total_tokens': result.shape[1]}}
    return await asyncio.to_thread(run)


@app.post('/v1/embeddings')
async def embeddings(request: Request):
    import asyncio
    body = await request.json()
    if body.get('model') != EMBEDDING:
        raise HTTPException(400, 'Unknown embedding model')
    texts = body.get('input')
    if isinstance(texts, str):
        texts = [texts]
    if not isinstance(texts, list) or len(texts) > 128 or any(not isinstance(t, str) for t in texts):
        raise HTTPException(400, 'Embedding input must contain at most128 text strings')

    def run():
        with mutex:
            if state['embedder'] is None:
                from sentence_transformers import SentenceTransformer
                state['embedder'] = SentenceTransformer(EMBEDDING, device='cpu', trust_remote_code=False)
            # Graphiti supplies query/fact text through one endpoint; both have explicit E5 prefixes.
            prefixed = [t if t.startswith(('query: ', 'passage: ')) else 'query: ' + t for t in texts]
            vectors = state['embedder'].encode(prefixed, normalize_embeddings=True)
            return {'object': 'list', 'model': EMBEDDING, 'data': [
                {'object': 'embedding', 'index': i, 'embedding': v.tolist()} for i, v in enumerate(vectors)],
                'usage': {'prompt_tokens': 0, 'total_tokens': 0}}
    return await asyncio.to_thread(run)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8008, log_level='warning')
