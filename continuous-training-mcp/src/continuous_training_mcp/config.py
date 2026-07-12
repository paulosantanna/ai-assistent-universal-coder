from __future__ import annotations

import os
from pathlib import Path

import yaml
from pydantic import ValidationError

from .models import ContinuousTrainingConfig

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config" / "continuous-training.yaml"


def load_config(path: str | None = None) -> ContinuousTrainingConfig:
    config_path = Path(path) if path else DEFAULT_CONFIG_PATH
    if not config_path.exists():
        return ContinuousTrainingConfig()
    try:
        with open(config_path, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return ContinuousTrainingConfig(**data.get("continuous_training", {}))
    except (ValidationError, yaml.YAMLError, OSError):
        return ContinuousTrainingConfig()


def merge_env_overrides(config: ContinuousTrainingConfig) -> ContinuousTrainingConfig:
    overrides = {}
    if "CT_MAX_SOURCES" in os.environ:
        overrides["max_sources_per_search"] = int(os.environ["CT_MAX_SOURCES"])
    if "CT_TIMEOUT" in os.environ:
        overrides["request_timeout"] = int(os.environ["CT_TIMEOUT"])
    if "CT_CONCURRENCY" in os.environ:
        overrides["max_concurrent_requests"] = int(os.environ["CT_CONCURRENCY"])
    if "CT_CACHE_TTL" in os.environ:
        overrides["cache_ttl_seconds"] = int(os.environ["CT_CACHE_TTL"])
    if "CT_ENABLE_TS" in os.environ:
        overrides["enable_ts_scraper"] = os.environ["CT_ENABLE_TS"].lower() in ("1", "true", "yes")
    return config.model_copy(update=overrides) if overrides else config
