import os
from dataclasses import dataclass
from pathlib import Path

os.environ.setdefault('GRAPHITI_TELEMETRY_ENABLED', 'false')

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Settings:
    state: Path
    model_url: str = 'http://127.0.0.1:8008/v1'
    model: str = 'Qwen/Qwen3-4B-Instruct-2507'
    embedding: str = 'intfloat/multilingual-e5-base'
    neo4j_url: str = 'bolt://127.0.0.1:7687'
    neo4j_user: str = 'neo4j'
    neo4j_password: str = ''
    api_key: str = ''
    allow_external: bool = False
    laya_checkpoint: str = 'convaiinnovations/laya-multilingual'

    @classmethod
    def load(cls):
        return cls(
            state=Path(os.getenv('RGL_STATE', str(ROOT / '.state'))).resolve(),
            model_url=os.getenv('RGL_MODEL_URL', 'http://127.0.0.1:8008/v1'),
            model=os.getenv('RGL_MODEL', 'Qwen/Qwen3-4B-Instruct-2507'),
            embedding=os.getenv('RGL_EMBEDDING', 'intfloat/multilingual-e5-base'),
            neo4j_url=os.getenv('RGL_NEO4J_URL', 'bolt://127.0.0.1:7687'),
            neo4j_user=os.getenv('RGL_NEO4J_USER', 'neo4j'),
            neo4j_password=os.getenv('RGL_NEO4J_PASSWORD', ''),
            api_key=os.getenv('RGL_MODEL_API_KEY', ''),
            allow_external=os.getenv('RGL_ALLOW_EXTERNAL', '0') == '1',
            laya_checkpoint=os.getenv('RGL_LAYA_CHECKPOINT', 'convaiinnovations/laya-multilingual'),
        )
