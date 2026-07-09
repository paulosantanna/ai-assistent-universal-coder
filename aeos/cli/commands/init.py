from pathlib import Path


def cmd_init(args) -> int:
    workspace = getattr(args, "target", Path.cwd())
    root = Path(workspace).resolve()
    dirs = [
        root / ".aeos" / "evidence",
        root / ".aeos" / "reports",
        root / ".aeos" / "packages",
        root / ".aeos" / "config",
        root / ".aeos" / "registries",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    config_file = root / ".aeos" / "config" / "aeos.yaml"
    if not config_file.exists():
        config_file.write_text("# AEOS Configuration\nworkspace: .\n")
    print(f"AEOS workspace initialized at {root}")
    return 0
