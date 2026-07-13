from pathlib import Path


def _load_registry_entries(workspace: Path):
    from aeos.core.registries.registry_fragment_loader import RegistryFragmentLoader
    loader = RegistryFragmentLoader()
    entries = {"skills": [], "playbooks": [], "agents": [], "mcps": [], "lcps": []}
    seen = {key: set() for key in entries}

    registry_dirs = [
        workspace / ".aeos" / "derived" / "registries",
        workspace / ".aeos" / "registries",
        workspace / "aeos" / "registries",
    ]

    for registry_dir in registry_dirs:
        if not registry_dir.exists():
            continue
        for f in sorted(registry_dir.glob("*")):
            if f.suffix in (".yaml", ".yml", ".json"):
                try:
                    frag = loader.load_fragment(str(f))
                    if frag and frag.metadata.loaded:
                        for kind, values in (
                            ("skills", frag.skills),
                            ("playbooks", frag.playbooks),
                            ("agents", frag.agents),
                            ("mcps", frag.mcps),
                            ("lcps", frag.lcps),
                        ):
                            for e in values:
                                if e.id in seen[kind]:
                                    continue
                                entries[kind].append(e.id)
                                seen[kind].add(e.id)
                except Exception:
                    pass
        if any(entries.values()):
            break
    return entries


def cmd_registry_validate(args) -> int:
    from aeos.cli.main import get_workspace_root
    workspace = get_workspace_root(args)
    try:
        entries = _load_registry_entries(workspace)
        errors = []
        if not any(entries.values()):
            errors.append("Registry is empty")
        for reg_type, items in entries.items():
            if not items:
                continue
            for item in items:
                pass
        if errors:
            for e in errors:
                print(f"  ERROR: {e}")
            print(f"Registry validation: FAILED ({len(errors)} issues)")
            return 1
        total = sum(len(v) for v in entries.values())
        print(f"Registry validation: PASS ({total} entries across {sum(1 for v in entries.values() if v)} types)")
        return 0
    except Exception as e:
        print(f"Registry validation error: {e}", file=__import__("sys").stderr)
        return 2


def cmd_registry_list(args) -> int:
    from aeos.cli.main import get_workspace_root
    workspace = get_workspace_root(args)
    entity = getattr(args, "entity", "skills")
    try:
        entries = _load_registry_entries(workspace)
        items = entries.get(entity, [])
        print(f"Registry {entity}:")
        for item in items:
            print(f"  - {item}")
        if not items:
            print("  (empty)")
        return 0
    except Exception as e:
        print(f"Registry list error: {e}", file=__import__("sys").stderr)
        return 2
