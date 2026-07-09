import hashlib
import json

def stable_hash(obj) -> str:
    raw = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

class EvidenceCacheKeyBuilder:
    def build(self, *, aeos_version, config_hash, policy_hash, permission_hash,
              playbook_id, playbook_version, skill_versions, lcp_versions,
              target_path, file_hashes, command_inputs) -> str:
        return stable_hash({
            "aeos_version": aeos_version,
            "config_hash": config_hash,
            "policy_hash": policy_hash,
            "permission_hash": permission_hash,
            "playbook_id": playbook_id,
            "playbook_version": playbook_version,
            "skill_versions": skill_versions,
            "lcp_versions": lcp_versions,
            "target_path": target_path,
            "file_hashes": file_hashes,
            "command_inputs": command_inputs,
        })
