import json
import sqlite3
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parents[1]
metadata = json.loads((OUT / 'vectors.json').read_text(encoding='utf-8'))
with sqlite3.connect(OUT / 'corpus.sqlite3') as db:
    rows = db.execute('SELECT id,sha256 FROM chunks ORDER BY id').fetchall()
with np.load(OUT / 'vectors.npz', allow_pickle=False) as data:
    ids, hashes, vectors = data['ids'], data['hashes'], data['vectors']
    valid = (len(ids) == len(rows) == metadata['count'] and vectors.shape == (len(rows), metadata['dimensions'])
             and all(int(ids[i]) == row[0] and hashes[i] == row[1] for i, row in enumerate(rows))
             and bool(np.isfinite(vectors).all()) and bool(np.allclose(np.linalg.norm(vectors, axis=1), 1, atol=.001)))
report = {'status': 'PASS' if valid else 'FAIL', 'count': len(rows), 'dimensions': metadata['dimensions'],
          'revision': metadata['revision'], 'scope': 'IDs, source hashes, finite normalized vectors and dimensions; not retrieval quality'}
(OUT / 'vector-verification.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report))
raise SystemExit(not valid)
