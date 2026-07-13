from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from aeos.core.execution.execution_models import ResolvedSkill
from aeos.core.registries.registry_models import SkillEntry
from aeos.core.skill_engine.skill_contract_validator import SkillContractValidator
from aeos.core.skill_engine.skill_loader import SkillLoader


class SkillResolver:
    """Resolve a registry skill into an executable contract."""

    def __init__(self, aeos_root: str = "."):
        self.aeos_root = Path(aeos_root).resolve()
        self.loader = SkillLoader(str(self.aeos_root))
        self.validator = SkillContractValidator(str(self.aeos_root))

    def resolve(self, skill_id: str) -> Optional[ResolvedSkill]:
        registry = self.loader.resolver.load()
        raw_entry = registry.get(skill_id)
        if not raw_entry:
            return None

        contract = self.loader.load_skill_contract(skill_id)
        if contract is None:
            return None

        validation = self.validator.validate(skill_id)
        path = raw_entry.get("path", "")
        entry = self._entry_from_raw(raw_entry)
        return ResolvedSkill(
            skill_id=skill_id,
            entry=entry,
            contract=contract,
            path=str((self.aeos_root / path).resolve()) if path else "",
            validation=validation,
        )

    def _entry_from_raw(self, entry: dict[str, Any]) -> SkillEntry:
        capabilities = entry.get("capabilities", [])
        return SkillEntry(
            id=entry.get("id", ""),
            owner_agent=entry.get("owner_agent"),
            risk_level=entry.get("risk_level"),
            capabilities=capabilities if isinstance(capabilities, list) else [],
            path=entry.get("path"),
            version=entry.get("version"),
            production_ready=entry.get("production_ready"),
        )
