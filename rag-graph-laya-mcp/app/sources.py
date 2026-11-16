import asyncio
import io
import json
from datetime import datetime, timezone
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

from .config import ROOT
from .store import digest

ALLOWED_HOSTS = {'github.com', 'api.github.com', 'raw.githubusercontent.com', 'arxiv.org', 'export.arxiv.org'}


def seed_catalog(store):
    for source in json.loads((ROOT / 'knowledge/sources.json').read_text(encoding='utf-8'))['sources']:
        try:
            store.source(source['id'])
        except ValueError:
            store.save_source({**source, 'status': 'discovered', 'content_hash': None, 'revision': None,
                               'consulted_at': None, 'analysis': None})


def validate_url(url):
    p = urlparse(url)
    if p.scheme != 'https' or p.hostname not in ALLOWED_HOSTS or p.username or p.password or p.port not in (None, 443):
        raise ValueError('Source URL is outside the primary-source allowlist')


async def fetch(client, url):
    for _ in range(5):
        validate_url(url)
        async with client.stream('GET', url) as response:
            if response.is_redirect:
                url = str(response.url.join(response.headers['location']))
                continue
            response.raise_for_status()
            data = bytearray()
            async for part in response.aiter_bytes():
                data.extend(part)
                if len(data) > 20_000_000:
                    raise ValueError('Source exceeds the 20MB acquisition limit')
            return bytes(data), response.headers.get('content-type', ''), str(response.url)
    raise ValueError('Source redirect limit exceeded')


def parse(data, content_type):
    if 'pdf' in content_type or data.startswith(b'%PDF'):
        from pypdf import PdfReader
        return '\n'.join(page.extract_text() or '' for page in PdfReader(io.BytesIO(data)).pages)
    text = data.decode('utf-8', errors='replace')
    if 'html' in content_type:
        soup = BeautifulSoup(text, 'html.parser')
        for item in soup(['script', 'style', 'nav', 'footer', 'header']):
            item.decompose()
        text = (soup.find('main') or soup).get_text('\n', strip=True)
    return text


async def acquire(store, source_ids, check_cancel, progress):
    source_ids = list(dict.fromkeys(source_ids))
    semaphore = asyncio.Semaphore(3)
    results = []
    async with httpx.AsyncClient(timeout=60, follow_redirects=False,
                                 headers={'User-Agent': 'CodENavi-RGL/0.1 primary-source research'}) as client:
        async def one(source_id):
            async with semaphore:
                check_cancel()
                source = store.source(source_id)
                url = source['url']
                if source.get('repo'):
                    raw, _, _ = await fetch(client, f"https://api.github.com/repos/{source['repo']}/commits/HEAD")
                    source['revision'] = json.loads(raw)['sha']
                    url = f"https://raw.githubusercontent.com/{source['repo']}/{source['revision']}/{source['file']}"
                data, content_type, final_url = await fetch(client, url)
                text = parse(data, content_type)
                if len(text.strip()) < 80:
                    raise ValueError('Source has insufficient extractable text')
                check_cancel()
                document = store.prepare_document(source_id, text)
                source.update(status='acquired', content_hash=digest(text), fetched_url=final_url,
                              consulted_at=datetime.now(timezone.utc).isoformat(), document_id=document['id'],
                              analysis=None)
                store.save_source(source)
                results.append({'source_id': source_id, 'document_id': document['id'], 'characters': len(text)})
                progress(len(results) / len(source_ids))
        outcomes = await asyncio.gather(*(one(s) for s in source_ids), return_exceptions=True)
        failures = [source_ids[i] for i, value in enumerate(outcomes) if isinstance(value, Exception)]
        if failures:
            raise ValueError('Acquisition failed for: ' + ', '.join(failures) + '; successful sources remain acquired')
    return {'acquired': results}
