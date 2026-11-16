"""SQLite is the durable ledger; graph events describe committed changes only."""
import hashlib
import json
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


class Store:
    def __init__(self, root: Path):
        self.root = root
        root.mkdir(parents=True, exist_ok=True)
        self.path = root / 'ledger.sqlite3'
        with self.connection() as db:
            db.executescript('''
            CREATE TABLE IF NOT EXISTS sources(id TEXT PRIMARY KEY, metadata TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS documents(id TEXT PRIMARY KEY, source_id TEXT NOT NULL,
                hash TEXT NOT NULL, text TEXT NOT NULL, active INTEGER NOT NULL DEFAULT 1,
                status TEXT NOT NULL, episodes TEXT NOT NULL DEFAULT '[]', created REAL NOT NULL);
            CREATE TABLE IF NOT EXISTS chunks(id TEXT PRIMARY KEY, document_id TEXT NOT NULL,
                ordinal INTEGER NOT NULL, text TEXT NOT NULL, active INTEGER NOT NULL DEFAULT 0);
            CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(id UNINDEXED,text);
            CREATE TABLE IF NOT EXISTS graph_items(kind TEXT NOT NULL,id TEXT NOT NULL,payload TEXT NOT NULL,
                PRIMARY KEY(kind,id));
            CREATE TABLE IF NOT EXISTS origins(kind TEXT NOT NULL,item_id TEXT NOT NULL,document_id TEXT NOT NULL,
                PRIMARY KEY(kind,item_id,document_id));
            CREATE TABLE IF NOT EXISTS events(seq INTEGER PRIMARY KEY AUTOINCREMENT,kind TEXT NOT NULL,
                payload TEXT NOT NULL,created REAL NOT NULL);
            CREATE TABLE IF NOT EXISTS jobs(id TEXT PRIMARY KEY,operation TEXT NOT NULL,status TEXT NOT NULL,
                progress REAL NOT NULL DEFAULT 0,result TEXT,error TEXT,cancel INTEGER NOT NULL DEFAULT 0,
                created REAL NOT NULL,updated REAL NOT NULL);
            CREATE TABLE IF NOT EXISTS experiments(id TEXT PRIMARY KEY,payload TEXT NOT NULL);
            ''')
            if 'inputs' not in {r['name'] for r in db.execute('PRAGMA table_info(jobs)')}:
                db.execute("ALTER TABLE jobs ADD COLUMN inputs TEXT NOT NULL DEFAULT '{}'")

    @contextmanager
    def connection(self):
        db = sqlite3.connect(self.path, timeout=30)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA journal_mode=WAL')
        try:
            yield db
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def emit(db, kind, payload):
        now = time.time()
        return db.execute('INSERT INTO events(kind,payload,created) VALUES(?,?,?)',
                          (kind, json.dumps({**payload, 'committed_at': now}), now)).lastrowid

    def event(self, kind, payload):
        with self.connection() as db:
            return self.emit(db, kind, payload)

    def events(self, after=0, limit=200):
        with self.connection() as db:
            return [dict(seq=r['seq'], kind=r['kind'], payload=json.loads(r['payload']))
                    for r in db.execute('SELECT * FROM events WHERE seq>? ORDER BY seq LIMIT ?', (after, limit))]

    def source(self, source_id):
        with self.connection() as db:
            row = db.execute('SELECT metadata FROM sources WHERE id=?', (source_id,)).fetchone()
            if row is None:
                raise ValueError('Unknown source_id; call sources_list first')
            return json.loads(row[0])

    def save_source(self, metadata):
        with self.connection() as db:
            db.execute('INSERT INTO sources VALUES(?,?) ON CONFLICT(id) DO UPDATE SET metadata=excluded.metadata',
                       (metadata['id'], json.dumps(metadata)))

    def sources(self):
        with self.connection() as db:
            return [json.loads(r[0]) for r in db.execute('SELECT metadata FROM sources ORDER BY id')]

    def document(self, doc_id):
        with self.connection() as db:
            r = db.execute('SELECT * FROM documents WHERE id=?', (doc_id,)).fetchone()
            if r is None:
                raise ValueError('Unknown document_id')
            result = dict(r)
            result['episodes'] = json.loads(result['episodes'])
            return result

    def prepare_document(self, source_id, text):
        sha = digest(text)
        doc_id = digest(source_id + ':' + sha)
        with self.connection() as db:
            db.execute('INSERT OR IGNORE INTO documents VALUES(?,?,?,?,1,?, ?,?)',
                       (doc_id, source_id, sha, text, 'pending', '[]', time.time()))
        return self.document(doc_id)

    def save_chunk(self, doc_id, ordinal, text):
        chunk_id = digest(f'{doc_id}:{ordinal}')
        with self.connection() as db:
            db.execute('INSERT OR IGNORE INTO chunks VALUES(?,?,?,?,0)', (chunk_id, doc_id, ordinal, text))
        return chunk_id

    def commit_graph(self, doc_id, episode_id, nodes, edges):
        with self.connection() as db:
            for kind, items in [('node', nodes), ('edge', edges)]:
                for item in items:
                    db.execute('INSERT INTO graph_items VALUES(?,?,?) ON CONFLICT(kind,id) '
                               'DO UPDATE SET payload=excluded.payload', (kind, item['id'], json.dumps(item)))
                    db.execute('INSERT OR IGNORE INTO origins VALUES(?,?,?)', (kind, item['id'], doc_id))
            episodes = json.loads(db.execute('SELECT episodes FROM documents WHERE id=?', (doc_id,)).fetchone()[0])
            if episode_id not in episodes:
                episodes.append(episode_id)
            db.execute('UPDATE documents SET episodes=? WHERE id=?', (json.dumps(episodes), doc_id))
            self.emit(db, 'graph.changed', {'document_id': doc_id, 'episode_id': episode_id})

    def activate_document(self, doc_id):
        with self.connection() as db:
            db.execute("UPDATE documents SET status='indexed',active=1 WHERE id=?", (doc_id,))
            db.execute('UPDATE chunks SET active=1 WHERE document_id=?', (doc_id,))
            for row in db.execute('SELECT id,text FROM chunks WHERE document_id=?', (doc_id,)).fetchall():
                db.execute('DELETE FROM chunks_fts WHERE id=?', (row['id'],))
                db.execute('INSERT INTO chunks_fts VALUES(?,?)', (row['id'], row['text']))
            self.emit(db, 'document.indexed', {'document_id': doc_id})

    def deactivate_document(self, doc_id):
        with self.connection() as db:
            db.execute("UPDATE documents SET active=0,status='removed' WHERE id=?", (doc_id,))
            db.execute('UPDATE chunks SET active=0 WHERE document_id=?', (doc_id,))
            db.execute('DELETE FROM chunks_fts WHERE id IN(SELECT id FROM chunks WHERE document_id=?)', (doc_id,))
            db.execute('DELETE FROM origins WHERE document_id=?', (doc_id,))
            db.execute('DELETE FROM graph_items WHERE NOT EXISTS '
                       '(SELECT 1 FROM origins o WHERE o.kind=graph_items.kind AND o.item_id=graph_items.id)')
            self.emit(db, 'graph.changed', {'removed_document_id': doc_id})

    def lexical(self, query, limit):
        import re
        tokens = re.findall(r'\w+', query, re.UNICODE)
        if not tokens:
            return []
        match = ' OR '.join('"' + x.replace('"', '""') + '"' for x in tokens[:30])
        with self.connection() as db:
            rows = db.execute('SELECT c.*,d.source_id,bm25(chunks_fts) AS rank FROM chunks_fts '
                              'JOIN chunks c ON c.id=chunks_fts.id JOIN documents d ON d.id=c.document_id '
                              'WHERE chunks_fts MATCH ? AND c.active=1 AND d.active=1 ORDER BY rank LIMIT ?',
                              (match, limit)).fetchall()
            return [dict(r) for r in rows]

    def snapshot(self, limit=500):
        with self.connection() as db:
            # SQLite does not start a read transaction for SELECT automatically.
            # Nodes, edges and cursor must belong to one snapshot or SSE can miss a commit.
            db.execute('BEGIN')
            nodes = [json.loads(r[0]) for r in db.execute("SELECT payload FROM graph_items WHERE kind='node' ORDER BY id LIMIT ?", (limit,))]
            ids = {n['id'] for n in nodes}
            edges = [json.loads(r[0]) for r in db.execute("SELECT payload FROM graph_items WHERE kind='edge' ORDER BY id")]
            edges = [e for e in edges if e['source'] in ids and e['target'] in ids]
            sources = {}
            for row in db.execute('SELECT o.item_id,d.source_id FROM origins o JOIN documents d ON d.id=o.document_id WHERE d.active=1'):
                sources.setdefault(row['item_id'], set()).add(row['source_id'])
            for item in nodes + edges:
                item['source_ids'] = sorted(sources.get(item['id'], []))
            seq = db.execute('SELECT coalesce(max(seq),0) FROM events').fetchone()[0]
            total = db.execute("SELECT count(*) FROM graph_items WHERE kind='node'").fetchone()[0]
            return {'nodes': nodes, 'edges': edges, 'cursor': seq, 'truncated': total > limit, 'total_nodes': total}

    def save_job(self, job_id, operation, inputs=None):
        now = time.time()
        with self.connection() as db:
            db.execute("INSERT INTO jobs(id,operation,status,created,updated,inputs) VALUES(?,?,'queued',?,?,?)", (job_id, operation, now, now, json.dumps(inputs or {})))
            self.emit(db, 'job.changed', {'job_id': job_id, 'status': 'queued'})

    def update_job(self, job_id, status, result=None, error=None, progress=None):
        with self.connection() as db:
            db.execute('UPDATE jobs SET status=?,result=?,error=?,progress=coalesce(?,progress),updated=? WHERE id=?',
                       (status, json.dumps(result) if result is not None else None, error, progress, time.time(), job_id))
            self.emit(db, 'job.changed', {'job_id': job_id, 'status': status, 'progress': progress, 'error': error})

    def job(self, job_id):
        with self.connection() as db:
            row = db.execute('SELECT * FROM jobs WHERE id=?', (job_id,)).fetchone()
            if row is None:
                raise ValueError('Unknown job_id')
            value = dict(row)
            value['result'] = json.loads(value['result']) if value['result'] else None
            value['inputs'] = json.loads(value['inputs'])
            return value

    def recover_jobs(self):
        with self.connection() as db:
            db.execute("UPDATE jobs SET status='interrupted',error='Process restarted; inspect partial artifacts before retry',updated=? WHERE status IN('queued','running')", (time.time(),))

