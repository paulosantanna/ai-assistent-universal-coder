"""Read the separate, provenance-checked local Reversa lexical corpus."""
import hashlib
import importlib.util
import json
import sqlite3
from functools import lru_cache

from .config import ROOT

CORPUS = ROOT.parent / '07_mapeamentos' / 'reversa-2026-11-01' / 'scripts' / 'corpus.py'


@lru_cache(maxsize=1)
def embedding_model():
    import torch
    from sentence_transformers import SentenceTransformer
    torch.set_num_threads(4)
    hub = ROOT / '.state' / 'models' / 'hub' / 'models--intfloat--multilingual-e5-base'
    revision = (hub / 'refs' / 'main').read_text(encoding='utf-8').strip()
    return SentenceTransformer(str(hub / 'snapshots' / revision), device='cpu',
                               trust_remote_code=False, local_files_only=True), revision


def retrieve(query, limit, strategy='lexical'):
    if not CORPUS.is_file():
        raise ValueError('Reversa corpus script is unavailable; build the local source index first')
    spec = importlib.util.spec_from_file_location('reversa_local_corpus', CORPUS)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not module.DB.is_file():
        raise ValueError('Reversa index is unavailable; build the local source index first')
    matches = module.search(query, min(20, limit * 2))
    if strategy == 'hybrid':
        import numpy as np
        vector_path = module.OUT / 'vectors.npz'
        metadata_path = module.OUT / 'vectors.json'
        if not vector_path.is_file() or not metadata_path.is_file():
            raise ValueError('Reversa vector index is unavailable; run vectors.py first')
        model, revision = embedding_model()
        metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
        if metadata.get('revision') != revision:
            raise ValueError('Reversa embedding revision changed; rebuild the vector index')
        vector = model.encode(['query: ' + query], normalize_embeddings=True, convert_to_numpy=True)[0]
        with np.load(vector_path, allow_pickle=False) as data:
            ids, hashes = data['ids'], data['hashes']
            scores = data['vectors'] @ vector
        with sqlite3.connect(module.DB) as db:
            rows = {row[0]: row[1:] for row in db.execute('SELECT id,path,start_line,end_line,sha256,body FROM chunks')}
        semantic = []
        for index in np.argsort(-scores):
            row = rows.get(int(ids[index]))
            if not row or row[3] != hashes[index]:
                continue
            path, start, end, digest, body = row
            source = module.REPO / path
            if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest() != digest:
                continue
            semantic.append({'path': path, 'start_line': start, 'end_line': end, 'sha256': digest, 'text': body})
            if len(semantic) >= limit * 2:
                break
        ranked = {}
        for candidates in (matches, semantic):
            for rank, item in enumerate(candidates, 1):
                key = (item['path'], item['start_line'], item['sha256'])
                record = ranked.setdefault(key, {'item': item, 'score': 0})
                record['score'] += 1 / (60 + rank)
        matches = [x['item'] for x in sorted(ranked.values(), key=lambda x: -x['score'])]
    matches = matches[:limit]
    evidence = [{'id': f"{m['sha256']}:{m['start_line']}", 'source_id': 'reversa-local',
                 'url': '02_repositorios/reversa/' + m['path'], **m} for m in matches]
    return {'evidence': evidence, 'strategy': strategy, 'scope': 'local Reversa sources; not GraphRAG'}
