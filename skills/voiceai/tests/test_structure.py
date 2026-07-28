from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]


def test_required_files():
    for rel in [
        "SKILL.md",
        "README.md",
        "AGENT.md",
        "knowledge/NEGATIVE_KNOWLEDGE.md",
        "knowledge/POSITIVE_KNOWLEDGE.md",
        "schemas/output.schema.json",
        "templates/OUTPUT.template.md",
        "evaluation/HONEST_EVALUATOR.md",
    ]:
        assert (ROOT / rel).exists(), rel


def test_skill_contract_covers_voiceai_requirements():
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8").lower()
    for term in [
        "consent",
        "literal transcript",
        "mixed-language",
        "video",
        "drive",
        "language tags",
        "joke",
        "out-of-scope",
        "actionable intent",
        "aeos handoff",
        "skills, mcps, lsps, playbooks, guardrails",
    ]:
        assert term in text


def test_output_schema_requires_voice_pipeline_outputs():
    schema = json.loads((ROOT / "schemas" / "output.schema.json").read_text(encoding="utf-8"))
    required = set(schema["required"])
    for field in [
        "media_sources",
        "literal_transcript",
        "segments",
        "actionable_intent",
        "out_of_scope_ledger",
        "handoff",
    ]:
        assert field in required


def test_segment_classifications_include_jokes_and_scope_boundaries():
    schema = json.loads((ROOT / "schemas" / "output.schema.json").read_text(encoding="utf-8"))
    classifications = set(
        schema["properties"]["segments"]["items"]["properties"]["classification"]["enum"]
    )
    assert {"joke", "out_of_scope", "actionable", "correction", "unclear"} <= classifications


def test_media_sources_include_video_and_drive_modes():
    schema = json.loads((ROOT / "schemas" / "output.schema.json").read_text(encoding="utf-8"))
    source_types = set(
        schema["properties"]["media_sources"]["items"]["properties"]["source_type"]["enum"]
    )
    assert {"live_audio", "video_file", "local_drive_path", "mounted_drive_path", "cloud_drive_connector"} <= source_types
