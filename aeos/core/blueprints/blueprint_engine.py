from pathlib import Path

class BlueprintEngine:
    def __init__(self, target_root: str):
        self.target_root = Path(target_root)

    def generate_to_sandbox(self, execution_id: str, blueprint: dict):
        out = self.target_root / ".aeos" / "sandbox" / execution_id / "blueprints" / blueprint["id"]
        out.mkdir(parents=True, exist_ok=True)
        generated = []
        for file_path in blueprint.get("generated_files", []):
            dest = out / file_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(f"# Generated placeholder for {file_path}\n", encoding="utf-8")
            generated.append(str(dest))
        return generated
