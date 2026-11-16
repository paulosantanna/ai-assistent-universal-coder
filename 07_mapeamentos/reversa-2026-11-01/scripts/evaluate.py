import hashlib
import json
import sqlite3
from pathlib import Path
from corpus import DB, OUT, REPO, search

# Diagnostic examples, authored from source; not a representative held-out benchmark.
cases = [
    ('files-manifest sha256 hashFile', 'lib/installer/manifest.js'),
    ('getWritableFolders allowLegacyEdits', 'lib/installer/policy.js'),
    ('detectEngines ENGINES skillsDir', 'lib/installer/detector.js'),
    ('createReversaDir Writer installSkill', 'lib/installer/writer.js'),
    ('fetchLatestVersion registry.npmjs.org', 'lib/commands/update.js'),
    ('MMDC_TIMEOUT_MS runMmdc', 'lib/commands/export-diagrams.js'),
    ('created_files modifiedFiles removeOutput', 'lib/commands/uninstall.js'),
    ('MIGRATION_AGENT_IDS DISCOVERY_CORE', 'lib/installer/prompts.js'),
]
results = []
for query, expected in cases:
    found = search(query, 10)
    rank = next((i for i, r in enumerate(found, 1) if r['path'] == expected), None)
    results.append({'query': query, 'expected_path': expected, 'rank': rank})
manifest = json.loads((OUT / 'manifest.json').read_text(encoding='utf-8'))
errors = []
with sqlite3.connect(DB) as db:
    integrity = db.execute('PRAGMA integrity_check').fetchone()[0]
    rows = db.execute('SELECT path,start_line,end_line,sha256,body FROM chunks').fetchall()
if integrity != 'ok': errors.append('sqlite integrity_check')
for path, start, end, digest, body in rows:
    raw = (REPO / path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != digest or '\n'.join(raw.decode('utf-8-sig').splitlines()[start-1:end]) != body:
        errors.append(f'origem divergente: {path}:{start}')
if len(rows) != manifest['chunks']: errors.append('contagem de chunks')
if any(r['rank'] is None for r in results): errors.append('consulta diagnóstica sem fonte esperada no top 10')
report = {'status': 'PASS' if not errors else 'FAIL', 'sqlite_integrity': integrity, 'chunks_checked': len(rows), 'diagnostic_recall_at_10': sum(r['rank'] is not None for r in results)/len(results), 'cases': results, 'errors': errors, 'limits': 'Consultas diagnósticas por caminho, pequenas e não independentes; não medem resposta gerada, pertinência geral ou faithfulness.'}
(OUT / 'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(bool(errors))
