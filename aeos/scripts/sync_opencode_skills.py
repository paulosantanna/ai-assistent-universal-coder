#!/usr/bin/env python3
"""Sincroniza e converte todas as skills do AEOS (.skill.md) para os locais de descobrimento do Antigravity CLI e OpenCode:
Exporta tanto com o nome limpo (<skill_name>) quanto com o prefixo (aeos-<skill_name>) em:
1. Workspace Antigravity CLI: .agents/skills/<name>/SKILL.md
2. Global Antigravity CLI: ~/.gemini/antigravity-cli/skills/<name>/SKILL.md
3. Workspace OpenCode: skills/<name>/SKILL.md
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
AEOS_SKILLS_CORE = ROOT_DIR / "aeos" / "skills" / "core"
AEOS_SKILLS_ENT = ROOT_DIR / "aeos" / "skills" / "enterprise"

TARGET_AGENTS_SKILLS_DIR = ROOT_DIR / ".agents" / "skills"
TARGET_SKILLS_DIR = ROOT_DIR / "skills"
GLOBAL_CLI_SKILLS_DIR = Path.home() / ".gemini" / "antigravity-cli" / "skills"


def parse_mission(content: str) -> str:
    """Extrai a missão/descrição do arquivo de skill."""
    match = re.search(r"## Mission\s*\n\n(.*?)(?=\n\n##|\Z)", content, re.DOTALL)
    if match:
        lines = [l.strip() for l in match.group(1).splitlines() if l.strip()]
        if lines:
            return lines[0]
    return "AEOS System Skill"


def write_skill_variant(name_key: str, content: str, description: str) -> None:
    frontmatter = f"""---
name: {name_key}
description: {description}
---

{content}
"""

    # 1. Workspace Antigravity CLI (.agents/skills/<name>/SKILL.md)
    w_agents_folder = TARGET_AGENTS_SKILLS_DIR / name_key
    w_agents_folder.mkdir(parents=True, exist_ok=True)
    (w_agents_folder / "SKILL.md").write_text(frontmatter, encoding="utf-8")

    # 2. Workspace OpenCode (skills/<name>/SKILL.md)
    w_skills_folder = TARGET_SKILLS_DIR / name_key
    w_skills_folder.mkdir(parents=True, exist_ok=True)
    (w_skills_folder / "SKILL.md").write_text(frontmatter, encoding="utf-8")

    # 3. Global Antigravity CLI (~/.gemini/antigravity-cli/skills/<name>/SKILL.md)
    try:
        g_folder = GLOBAL_CLI_SKILLS_DIR / name_key
        g_folder.mkdir(parents=True, exist_ok=True)
        (g_folder / "SKILL.md").write_text(frontmatter, encoding="utf-8")
    except Exception:
        pass


def convert_skill_file(skill_file: Path) -> None:
    skill_name = skill_file.stem.replace(".skill", "")
    content = skill_file.read_text(encoding="utf-8")
    description = parse_mission(content)

    # Escreve a versão com o nome limpo e a versão com prefixo aeos-
    write_skill_variant(skill_name, content, description)
    write_skill_variant(f"aeos-{skill_name}", content, description)

    print(f"[OK] Skill exportada (versão limpa & prefixada): {skill_name}")


def main() -> None:
    print("Iniciando sincronização completa de Skills do AEOS em todos os endpoints de descoberta...")
    count = 0

    if AEOS_SKILLS_CORE.exists():
        for f in AEOS_SKILLS_CORE.glob("*.skill.md"):
            convert_skill_file(f)
            count += 1

    if AEOS_SKILLS_ENT.exists():
        for f in AEOS_SKILLS_ENT.glob("*.skill.md"):
            convert_skill_file(f)
            count += 1

    print(f"\nTotal de {count} skills do AEOS sincronizadas com sucesso (variantes limpas e prefixadas)!")


if __name__ == "__main__":
    main()
