"""Explicit providers. No network calls or model loading during protocol negotiation."""
import ipaddress
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import httpx


def validate_model_url(settings):
    parsed = urlparse(settings.model_url)
    if parsed.username or parsed.password or parsed.scheme not in {'http', 'https'}:
        raise ValueError('Model endpoint must use HTTP(S) without embedded credentials')
    try:
        local = ipaddress.ip_address(parsed.hostname or '').is_loopback
    except ValueError:
        local = parsed.hostname == 'localhost'
    if not local and not settings.allow_external:
        raise ValueError('External model endpoint requires RGL_ALLOW_EXTERNAL=1')
    if not local and parsed.scheme != 'https':
        raise ValueError('External model endpoints require HTTPS')


class ModelClient:
    def __init__(self, settings):
        self.settings = settings

    async def complete(self, messages, schema=None, max_tokens=1200):
        validate_model_url(self.settings)
        body = {'model': self.settings.model, 'messages': messages, 'temperature': 0,
                'max_tokens': max_tokens}
        if schema is not None:
            body['response_format'] = {'type': 'json_schema', 'json_schema': {'name': 'response', 'schema': schema}}
        async with httpx.AsyncClient(timeout=300) as client:
            for attempt in range(3):
                response = await client.post(self.settings.model_url.rstrip('/') + '/chat/completions',
                                             json=body, headers={'Authorization': 'Bearer ' + (self.settings.api_key or 'local')})
                if response.status_code == 422 and schema is not None and attempt < 2:
                    body['messages'] = [*messages, {'role': 'user', 'content': 'Return complete JSON only, matching the schema. Keep each answer under two sentences.'}]
                    continue
                response.raise_for_status()
                return response.json()['choices'][0]['message']['content']

    async def health(self):
        validate_model_url(self.settings)
        async with httpx.AsyncClient(timeout=3) as client:
            response = await client.get(self.settings.model_url.rstrip('/') + '/models',
                                        headers={'Authorization': 'Bearer ' + (self.settings.api_key or 'local')})
            response.raise_for_status()
            return response.json()


class Graph:
    def __init__(self, settings):
        self.settings = settings
        self.client = None

    async def get(self):
        if self.client is None:
            if not self.settings.neo4j_password:
                raise ValueError('Configure RGL_NEO4J_PASSWORD through the runtime environment before graph operations')
            validate_model_url(self.settings)
            from graphiti_core import Graphiti
            from graphiti_core.cross_encoder.openai_reranker_client import OpenAIRerankerClient
            from graphiti_core.embedder.openai import OpenAIEmbedder, OpenAIEmbedderConfig
            from graphiti_core.llm_client.config import LLMConfig
            from graphiti_core.llm_client.openai_generic_client import OpenAIGenericClient
            cfg = LLMConfig(api_key=self.settings.api_key or 'local', model=self.settings.model,
                            small_model=self.settings.model, base_url=self.settings.model_url)
            llm = OpenAIGenericClient(config=cfg)
            self.client = Graphiti(self.settings.neo4j_url, self.settings.neo4j_user,
                                  self.settings.neo4j_password, llm_client=llm,
                                  embedder=OpenAIEmbedder(config=OpenAIEmbedderConfig(
                                      api_key=self.settings.api_key or 'local', embedding_model=self.settings.embedding,
                                      embedding_dim=768, base_url=self.settings.model_url)),
                                  cross_encoder=OpenAIRerankerClient(client=llm, config=cfg))
            await self.client.build_indices_and_constraints()
        return self.client

    async def add(self, chunk_id, text, source):
        from graphiti_core.errors import NodeNotFoundError
        from graphiti_core.nodes import EpisodeType, EpisodicNode
        graph = await self.get()
        episode_id = chunk_id[:8] + '-' + chunk_id[8:12] + '-' + chunk_id[12:16] + '-' + chunk_id[16:20] + '-' + chunk_id[20:32]
        now = datetime.now(timezone.utc)
        try:
            await EpisodicNode.get_by_uuid(graph.driver, episode_id)
        except NodeNotFoundError:
            # Graphiti0.30 treats an explicit UUID as an existing episode.
            # Persist a deterministic source episode before asking it to extract relations.
            episode = EpisodicNode(uuid=episode_id, name=chunk_id, group_id='rgl-domain', labels=[],
                                   source=EpisodeType.text, content=text, source_description=source['url'],
                                   created_at=now, valid_at=now)
            await episode.save(graph.driver)
        result = await graph.add_episode(name=chunk_id, episode_body=text,
                                         source_description=source['url'], source=EpisodeType.text,
                                         reference_time=now, group_id='rgl-domain', uuid=episode_id)
        nodes = [{'id': n.uuid, 'label': n.name, 'summary': n.summary, 'type': 'entity'} for n in result.nodes]
        edges = [{'id': e.uuid, 'source': e.source_node_uuid, 'target': e.target_node_uuid, 'label': e.name,
                  'fact': e.fact, 'valid_at': e.valid_at.isoformat() if e.valid_at else None,
                  'invalid_at': e.invalid_at.isoformat() if e.invalid_at else None} for e in result.edges]
        return result.episode.uuid, nodes, edges

    async def search(self, query, limit):
        graph = await self.get()
        edges = await graph.search(query, group_ids=['rgl-domain'], num_results=limit)
        return [{'id': e.uuid, 'text': e.fact, 'episodes': e.episodes, 'type': 'fact'} for e in edges]

    async def remove(self, episode_ids):
        graph = await self.get()
        for episode_id in episode_ids:
            await graph.remove_episode(episode_id)

    async def close(self):
        if self.client is not None:
            await self.client.close()


class Laya:
    def __init__(self, settings):
        self.settings = settings
        self.model = None

    def decide(self, state, questions):
        # Permit only typed schemas, and leave action authorization to deterministic code.
        for question in questions.values():
            if not isinstance(question, dict) or question.get('type') not in {'choice', 'score', 'noul'}:
                raise ValueError('Laya questions must use choice, score or noul')
            criteria = question.get('criteria', {})
            if question['type'] == 'choice' and (not isinstance(criteria, dict) or not 2 <= len(criteria) <= 20):
                raise ValueError('Each choice must have 2-20 bounded criteria')
        if self.model is None:
            try:
                import laya
            except ImportError as exc:
                raise ValueError('Install the locked training extra for Laya inference') from exc
            self.model = laya.load(self.settings.laya_checkpoint, device='cpu')
        value = self.model.predict(state, questions)
        checkpoint = Path(self.settings.laya_checkpoint)
        report = checkpoint.parent / 'result.json'
        calibrated = False
        if checkpoint.is_dir() and report.is_file():
            metadata = json.loads(report.read_text(encoding='utf-8'))
            quality = metadata.get('candidate', {})
            calibrated = metadata.get('flow') == 'laya' and all(
                quality.get(name, {}).get('count', 0) >= 50 and quality.get(name, {}).get('ece', 1) <= .1
                for name in ('strategy', 'relevance'))
        return {**value, 'checkpoint': self.settings.laya_checkpoint,
                'calibration_verified': calibrated,
                'authorization': 'typed decisions never authorize execution'}
