"""Build a local E5 index using only already-cached model weights."""
import json
import os
import sqlite3
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
ROOT = OUT.parents[1]
os.environ['HF_HOME'] = str(ROOT / 'rag-graph-laya-mcp' / '.state' / 'models')
os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['HF_HUB_DISABLE_TELEMETRY'] = '1'

import numpy as np
import torch
from sentence_transformers import SentenceTransformer

torch.set_num_threads(4)
with sqlite3.connect(OUT / 'corpus.sqlite3') as db:
    rows = db.execute('SELECT id, sha256, body FROM chunks ORDER BY id').fetchall()
if not rows:
    raise SystemExit('Índice lexical vazio')
model = SentenceTransformer('intfloat/multilingual-e5-base', device='cpu', trust_remote_code=False, local_files_only=True)
blocks = []
for start in range(0, len(rows), 32):
    batch = ['passage: ' + row[2] for row in rows[start:start+32]]
    blocks.append(model.encode(batch, batch_size=8, normalize_embeddings=True, convert_to_numpy=True, show_progress_bar=False))
    print(f'{min(start+32, len(rows))}/{len(rows)}', flush=True)
vectors = np.concatenate(blocks).astype('float32')
tmp = OUT / 'vectors.tmp.npz'
np.savez_compressed(tmp, vectors=vectors, ids=np.asarray([r[0] for r in rows]), hashes=np.asarray([r[1] for r in rows]))
tmp.replace(OUT / 'vectors.npz')
revision = (ROOT / 'rag-graph-laya-mcp/.state/models/hub/models--intfloat--multilingual-e5-base/refs/main').read_text(encoding='utf-8').strip()
(OUT / 'vectors.json').write_text(json.dumps({'model': 'intfloat/multilingual-e5-base', 'revision': revision, 'count': len(rows), 'dimensions': int(vectors.shape[1]), 'caveat': 'E5 truncates passages at its model token limit; compare with full cited source.'}, indent=2) + '\n', encoding='utf-8')
print('Índice vetorial concluído', flush=True)
