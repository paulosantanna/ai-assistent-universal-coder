from __future__ import annotations

from typing import Any

from aeos.core.registries.registry_models import (
    ConflictRecord,
    ConsolidatedRegistry,
    FragmentCategory,
    LoadedFragment,
    RegistryType,
)


class RegistryConflictDetector:
    def __init__(self):
        self.conflicts: list[ConflictRecord] = []
        self.deduplications: list[dict[str, Any]] = []

    def detect(self, fragments: list[LoadedFragment]) -> list[ConflictRecord]:
        self.conflicts = []
        self.deduplications = []

        groups: dict[str, list[tuple[LoadedFragment, Any]]] = {}

        for frag in fragments:
            if not frag.metadata.loaded:
                continue
            for agent in frag.agents:
                key = f"agents:{agent.id}"
                groups.setdefault(key, []).append((frag, agent))
            for skill in frag.skills:
                key = f"skills:{skill.id}"
                groups.setdefault(key, []).append((frag, skill))
            for playbook in frag.playbooks:
                key = f"playbooks:{playbook.id}"
                groups.setdefault(key, []).append((frag, playbook))

        for key, entries in groups.items():
            if len(entries) < 2:
                continue

            reg_type_str = key.split(":")[0]
            entry_id = key.split(":", 1)[1]
            reg_type = RegistryType(reg_type_str)

            entries_with_path = [
                (frag, entry) for frag, entry in entries
                if hasattr(entry, "path") and entry.path
            ]

            path_set: set[str] = set()
            for frag, entry in entries_with_path:
                path_set.add(entry.path)

            if len(path_set) <= 1:
                self.deduplications.append({
                    "entry_id": entry_id,
                    "registry_type": reg_type_str,
                    "path": next(iter(path_set)) if path_set else None,
                    "source_fragments": [frag.metadata.path for frag, _ in entries],
                    "count": len(entries),
                })
            else:
                seen_pairs: set[tuple[str, str]] = set()
                for i in range(len(entries_with_path)):
                    for j in range(i + 1, len(entries_with_path)):
                        frag_a, entry_a = entries_with_path[i]
                        frag_b, entry_b = entries_with_path[j]
                        if entry_a.path != entry_b.path:
                            pair = tuple(sorted([frag_a.metadata.path, frag_b.metadata.path]))
                            if pair not in seen_pairs:
                                seen_pairs.add(pair)
                                self.conflicts.append(
                                    ConflictRecord(
                                        entry_id=entry_id,
                                        registry_type=reg_type,
                                        source_a_path=frag_a.metadata.path,
                                        source_b_path=frag_b.metadata.path,
                                        existing_path=entry_a.path,
                                        conflicting_path=entry_b.path,
                                        description=f"Duplicate id '{entry_id}' with different paths across fragments",
                                    )
                                )

        return self.conflicts

    def get_conflict_count(self) -> int:
        return len(self.conflicts)

    def get_deduplication_count(self) -> int:
        return len(self.deduplications)
