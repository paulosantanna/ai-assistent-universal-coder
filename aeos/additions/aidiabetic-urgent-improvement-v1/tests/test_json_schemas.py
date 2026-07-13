from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def test_json_files_parse():
    for path in ROOT.rglob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))
