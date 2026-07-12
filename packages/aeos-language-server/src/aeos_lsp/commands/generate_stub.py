from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_STUB_TEMPLATES: dict[str, str] = {
    "agent": """# {name}
# Auto-generated agent stub

agent:
  name: {name}
  stable_id: agent:{uri}#{name}
  description: ""
  visibility: public
  layers:
    - name: default
      skills: []
""",
    "skill": """# {name}
# Auto-generated skill stub

skill:
  name: {name}
  stable_id: skill:{uri}#{name}
  description: ""
  visibility: public
  tools: []
  inputs: []
  outputs: []
""",
    "playbook": """# {name}
# Auto-generated playbook stub

playbook:
  name: {name}
  stable_id: playbook:{uri}#{name}
  description: ""
  visibility: public
  steps: []
  variables: []
""",
    "tool": """# {name}
# Auto-generated tool stub

tool:
  name: {name}
  stable_id: tool:{uri}#{name}
  description: ""
  command: ""
  mutating: false
  inputs: []
  outputs: []
""",
    "policy": """# {name}
# Auto-generated policy stub

policy:
  name: {name}
  stable_id: policy:{uri}#{name}
  description: ""
  rules: []
""",
    "permission": """# {name}
# Auto-generated permission stub

permission:
  name: {name}
  stable_id: permission:{uri}#{name}
  description: ""
  scopes: []
  capabilities: []
""",
    "registry": """# {name}
# Auto-generated registry stub

{name}:
  items: []
""",
    "model_profile": """# {name}
# Auto-generated model profile stub

model_profile:
  name: {name}
  stable_id: model:{uri}#{name}
  provider: ""
  model: ""
  token_budget: 4096
  temperature: 0.7
""",
}


def _sanitize_name(name: str) -> str:
    sanitized = re.sub(r"[^a-zA-Z0-9_-]", "_", name)
    sanitized = re.sub(r"^[^a-zA-Z_]+", "", sanitized)
    return sanitized or "unnamed"


def generate_stub(server: Any, args: dict[str, Any]) -> dict[str, Any]:
    entity_type = args.get("entity_type", "").lower()
    name = args.get("name", "")
    uri = args.get("uri", "")

    if not entity_type:
        return {"error": "Missing 'entity_type' argument"}
    if not name:
        return {"error": "Missing 'name' argument"}

    logger.info("Generating stub for %s '%s'", entity_type, name)

    try:
        if entity_type not in _STUB_TEMPLATES:
            valid_types = ", ".join(_STUB_TEMPLATES.keys())
            return {
                "error": f"Unknown entity type '{entity_type}'. Valid types: {valid_types}",
            }

        if not uri:
            workspace = getattr(server, "workspace_manager", None)
            if workspace is not None:
                aeos_root = getattr(workspace, "aeos_root", None)
                if aeos_root is not None:
                    uri = str(Path(aeos_root) / f"{_sanitize_name(name)}.{entity_type}.md")

        safe_name = _sanitize_name(name)
        template = _STUB_TEMPLATES[entity_type]
        content = template.format(name=safe_name, uri=uri or "local")

        suggested_path = None
        if uri:
            suggested_path = uri
        else:
            cwd = Path.cwd()
            suggested_path = str(cwd / "aeos" / "stubs" / f"{safe_name}.{entity_type}.md")

        return {
            "entity_type": entity_type,
            "name": name,
            "sanitized_name": safe_name,
            "content": content,
            "suggested_path": suggested_path,
            "line_count": len(content.strip().split("\n")),
            "char_count": len(content),
        }
    except Exception as exc:
        logger.exception("Failed to generate stub for %s '%s'", entity_type, name)
        return {"error": str(exc)}
