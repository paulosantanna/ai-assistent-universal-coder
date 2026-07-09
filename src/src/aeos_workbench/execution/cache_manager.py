"""Evidence Cache Manager — cache_key, storage, invalidation, security-aware caching."""

import hashlib
import json
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


SHA256_EMPTY = hashlib.sha256(b"").hexdigest()
MAX_CACHE_AGE_SECONDS = 7 * 24 * 3600
MAX_CACHE_SIZE_BYTES = 500 * 1024 * 1024
SECURITY_PLAYBOOK_RISK_LEVELS = {"high", "critical"}


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _hash_dir(directory: Path, max_files: int = 200) -> str:
    if not directory.is_dir():
        return SHA256_EMPTY
    hashes = []
    for i, f in enumerate(sorted(directory.rglob("*"))):
        if i >= max_files:
            break
        if f.is_file():
            try:
                hashes.append(f.name + ":" + _sha256_file(f))
            except Exception:
                hashes.append(f.name + ":ERROR")
    return _sha256_text("\n".join(hashes))


def _config_hash(workspace_root: Path) -> str:
    config_path = workspace_root / "aeos" / "config" / "aeos.config.yaml"
    if config_path.exists():
        return _sha256_file(config_path)
    return SHA256_EMPTY


class CacheManager:
    def __init__(self, workspace_root: Path, cache_dir: Optional[Path] = None):
        self.workspace_root = workspace_root.resolve()
        self.cache_dir = (cache_dir or (self.workspace_root / ".aeos" / "cache")).resolve()
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._manifest_path = self.cache_dir / "cache-manifest.json"
        self._manifest: dict = self._load_manifest()
        self._hit_count = 0

    def _load_manifest(self) -> dict:
        if self._manifest_path.exists():
            try:
                return json.loads(self._manifest_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"version": "1.0.0", "entries": {}, "created_at": datetime.now(timezone.utc).isoformat()}

    def _save_manifest(self):
        self._manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
        self._manifest_path.write_text(
            json.dumps(self._manifest, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    def build_cache_key(
        self,
        playbook_id: str,
        playbook_version: str,
        skill_versions: dict[str, str],
        target_path: Path,
    ) -> str:
        raw = (
            _config_hash(self.workspace_root)
            + playbook_id
            + playbook_version
            + json.dumps(skill_versions, sort_keys=True)
            + _hash_dir(target_path, max_files=200)
            + str(target_path.resolve())
        )
        return _sha256_text(raw)

    def get(self, cache_key: str, playbook_id: str) -> Optional[dict]:
        playbook_entry = self._manifest.get("entries", {}).get(playbook_id, {})
        if not playbook_entry:
            return None

        entry = playbook_entry.get(cache_key)
        if not entry:
            return None

        if entry.get("security_revalidation_required", False):
            return None

        created_at = entry.get("created_at", "")
        try:
            age = time.time() - datetime.fromisoformat(created_at).timestamp()
            if age > MAX_CACHE_AGE_SECONDS:
                return None
        except Exception:
            return None

        cache_path = Path(entry.get("cache_path", ""))
        if not cache_path.exists():
            return None

        self._hit_count += 1
        return {
            "artifacts": entry.get("artifact_entries", []),
            "generated_at": created_at,
            "cache_key": cache_key,
        }

    def set(
        self,
        cache_key: str,
        playbook_id: str,
        source_files: list[Path],
        generated_artifacts: list[dict],
        playbook_risk_level: str = "low",
    ) -> dict:
        security_flag = playbook_risk_level in SECURITY_PLAYBOOK_RISK_LEVELS

        prefix = cache_key[:16]
        cache_entry_dir = self.cache_dir / playbook_id / prefix
        cache_entry_dir.mkdir(parents=True, exist_ok=True)

        artifact_entries = []
        total_size = 0
        for art in generated_artifacts:
            src = Path(art["path"])
            if not src.exists():
                continue
            dst = cache_entry_dir / src.name
            dst.write_bytes(src.read_bytes())
            artifact_entries.append({
                "name": dst.name,
                "type": art.get("type", "unknown"),
                "size": src.stat().st_size,
                "cached_path": str(dst),
            })
            total_size += src.stat().st_size

        if playbook_id not in self._manifest["entries"]:
            self._manifest["entries"][playbook_id] = {}
        self._manifest["entries"][playbook_id][cache_key] = {
            "cache_path": str(cache_entry_dir),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "artifact_count": len(artifact_entries),
            "total_size_bytes": total_size,
            "security_revalidation_required": security_flag,
            "source_file_count": len(source_files),
            "artifact_entries": artifact_entries,
        }

        self._evict_if_full()
        self._save_manifest()

        return {
            "cache_key": cache_key,
            "path": str(cache_entry_dir),
            "artifact_count": len(artifact_entries),
        }

    def _evict_if_full(self):
        total = 0
        for pb_id, pb_entry in self._manifest.get("entries", {}).items():
            for ck, entry in pb_entry.items():
                total += entry.get("total_size_bytes", 0)
        if total <= MAX_CACHE_SIZE_BYTES:
            return

        all_entries = []
        for pb_id, pb_entry in self._manifest["entries"].items():
            for ck, entry in pb_entry.items():
                all_entries.append((pb_id, ck, entry.get("created_at", ""), entry.get("total_size_bytes", 0)))

        all_entries.sort(key=lambda x: x[2])
        freed = 0
        for pb_id, ck, ts, size in all_entries:
            entry = self._manifest["entries"][pb_id].pop(ck, {})
            cp = Path(entry.get("cache_path", ""))
            if cp.exists():
                shutil.rmtree(cp, ignore_errors=True)
            freed += size
            if total - freed < MAX_CACHE_SIZE_BYTES:
                break

    def clear(self, playbook_id: Optional[str] = None):
        if playbook_id:
            entry = self._manifest.get("entries", {}).pop(playbook_id, {})
            for ck, cache_entry in entry.items():
                cp = Path(cache_entry.get("cache_path", ""))
                if cp.exists():
                    shutil.rmtree(cp, ignore_errors=True)
            self._save_manifest()
            return
        for pb_id in list(self._manifest.get("entries", {}).keys()):
            entry = self._manifest["entries"].pop(pb_id, {})
            for ck, cache_entry in entry.items():
                cp = Path(cache_entry.get("cache_path", ""))
                if cp.exists():
                    shutil.rmtree(cp, ignore_errors=True)
        self._save_manifest()

    def status(self) -> dict:
        total_entries = 0
        total_size = 0
        for pb_id, pb_entry in self._manifest.get("entries", {}).items():
            for ck, entry in pb_entry.items():
                total_entries += 1
                total_size += entry.get("total_size_bytes", 0)
        return {
            "cache_dir": str(self.cache_dir),
            "total_playbooks": len(self._manifest.get("entries", {})),
            "total_entries": total_entries,
            "total_size_bytes": total_size,
            "max_size_bytes": MAX_CACHE_SIZE_BYTES,
            "max_age_days": 7,
        }

    @property
    def hit(self) -> bool:
        return self._hit_count > 0

    @property
    def hit_count(self) -> int:
        return self._hit_count