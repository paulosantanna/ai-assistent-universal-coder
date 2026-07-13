import json
from .bundle_models import BundleManifest

def save_manifest(manifest: BundleManifest, out_path: str) -> None:
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest.model_dump(), f, indent=2)

def load_manifest(in_path: str) -> BundleManifest:
    with open(in_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return BundleManifest(**data)
