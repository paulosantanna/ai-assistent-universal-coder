"""LCP Resolver — loads and merges LCPs by priority from the registry."""

from pathlib import Path
from typing import Any


PRIORITY_ORDER = [
    "security-governance",   # 1st — can never be overridden
    "global-rules",          # 2nd
    "project-specific",       # 3rd
    "stack-specific",        # 4th
    "output-specific",       # 5th
]

SECURITY_LCP_ID = "security-governance"
GLOBAL_LCP_ID = "global-rules"


class LCPResolver:
    def __init__(self, workspace_root: Path, registry_path: Path):
        self.workspace_root = workspace_root.resolve()
        self.registry_path = registry_path
        self._lcp_cache: dict[str, dict] = {}

    def load_registry(self) -> list[dict]:
        import yaml
        if not self.registry_path.exists():
            raise FileNotFoundError(f"LCP registry not found: {self.registry_path}")
        data = yaml.safe_load(self.registry_path.read_text(encoding="utf-8"))
        return data.get("lcps", [])

    def load_lcp(self, lcp_entry: dict) -> dict:
        rel_path = lcp_entry["path"]
        lcp_path = (self.workspace_root / rel_path).resolve()
        if not lcp_path.exists():
            raise FileNotFoundError(f"LCP file not found: {lcp_path}")
        import yaml
        return yaml.safe_load(lcp_path.read_text(encoding="utf-8"))

    def resolve_for(self, playbook_id: str, stack_ids: list[str] | None = None) -> dict:
        import yaml
        registry = self.load_registry()
        resolved: dict[str, dict] = {}

        # Sort by priority descending
        sorted_lcps = sorted(registry, key=lambda x: x.get("priority", 0), reverse=True)

        for entry in sorted_lcps:
            lcp_id = entry["id"]
            lcp_data = self.load_lcp(entry)
            self._lcp_cache[lcp_id] = lcp_data

            if lcp_id == SECURITY_LCP_ID:
                resolved[lcp_id] = lcp_data
                continue

            if lcp_id == GLOBAL_LCP_ID:
                resolved[lcp_id] = lcp_data
                continue

            if lcp_id in resolved:
                continue

            resolved[lcp_id] = lcp_data

        merged = self._merge(resolved)
        self._validate_security(merged, resolved)
        return merged

    def _merge(self, resolved: dict[str, dict]) -> dict:
        merged_rules: list[str] = []
        merged_forbidden: list[str] = []
        merged_evidence: list[str] = []
        all_templates: dict = {}

        priority_order = [SECURITY_LCP_ID, GLOBAL_LCP_ID]
        for lid in priority_order:
            lcp = resolved.get(lid, {})
            merged_rules.extend(lcp.get("rules", []))
            merged_forbidden.extend(lcp.get("forbidden", []))
            merged_evidence.extend(lcp.get("required_evidence", []))

        for lid in sorted(resolved.keys()):
            if lid in priority_order:
                continue
            lcp = resolved[lid]
            merged_rules.extend(lcp.get("rules", []))
            merged_forbidden.extend(lcp.get("forbidden", []))
            merged_evidence.extend(lcp.get("required_evidence", []))
            templates = lcp.get("documentation_templates", {})
            if templates:
                all_templates.update(templates)

        merged_rules = list(dict.fromkeys(merged_rules))
        merged_forbidden = list(dict.fromkeys(merged_forbidden))
        merged_evidence = list(dict.fromkeys(merged_evidence))

        return {
            "resolved_lcps": list(resolved.keys()),
            "rules": merged_rules,
            "forbidden": merged_forbidden,
            "required_evidence": merged_evidence,
            "documentation_templates": all_templates,
        }

    def _validate_security(self, merged: dict, resolved: dict):
        sec = resolved.get(SECURITY_LCP_ID, {})
        sec_rules = set(sec.get("rules", []))
        sec_forbidden = set(sec.get("forbidden", []))

        if not sec_rules.issubset(set(merged.get("rules", []))):
            missing = sec_rules - set(merged.get("rules", []))
            raise ValueError(
                f"Security LCP rules were overridden! Missing: {missing}. "
                f"Security-governance LCP can never be overridden."
            )
        if not sec_forbidden.issubset(set(merged.get("forbidden", []))):
            missing = sec_forbidden - set(merged.get("forbidden", []))
            raise ValueError(
                f"Security LCP forbidden actions were overridden! Missing: {missing}. "
                f"Security-governance LCP can never be overridden."
            )

    def get_raw_lcp(self, lcp_id: str) -> dict | None:
        return self._lcp_cache.get(lcp_id)