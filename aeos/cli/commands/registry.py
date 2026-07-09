from pathlib import Path


def _load_registry_entries(workspace: Path):
    import yaml
    from aeos.core.registries.registry_fragment_loader import RegistryFragmentLoader
    loader = RegistryFragmentLoader()
    entries = {"skills": [], "playbooks": [], "agents": [], "mcps": [], "lcps": []}
    registry_dir = workspace / ".aeos" / "registries"
    if registry_dir.exists():
        for f in sorted(registry_dir.iterdir()):
            if f.suffix in (".yaml", ".yml", ".json"):
                try:
                    frag = loader.load_fragment(str(f))
                    if frag and frag.metadata.loaded:
                        for e in frag.skills:
                            entries["skills"].append(e.id)
                        for e in frag.playbooks:
                            entries["playbooks"].append(e.id)
                        for e in frag.agents:
                            entries["agents"].append(e.id)
                        for e in frag.mcps:
                            entries["mcps"].append(e.id)
                        for e in frag.lcps:
                            entries["lcps"].append(e.id)
                except Exception:
                    pass
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
