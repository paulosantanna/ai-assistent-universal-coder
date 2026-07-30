from pathlib import Path


def test_solve_problems_structure_and_contract():
    root = Path(__file__).resolve().parents[1]
    text = (root / "SKILL.md").read_text(encoding="utf-8")

    assert "slug: solve-problems" in text
    assert "architecture_level: 3" in text
    assert "Do not add comments" in text or "do not add comments" in text
    assert "unused imports" in text
    assert "orphan variables" in text
    assert "preserve architecture" in text or "preserves architecture" in text

    for rel in [
        "AGENT.md",
        "schemas/output.schema.json",
        "references/LANGUAGE_ROUTING.md",
        "evaluation/HONEST_EVALUATOR.md",
        "templates/execution-bundle/Memory/memory.md",
        "templates/execution-bundle/Handoff/handoff.md",
        "templates/execution-bundle/progress/progress.md",
        "templates/execution-bundle/Learning/learning.md",
        "templates/execution-bundle/evidencias/linha-do-tempo-worktree-git.md",
        "templates/execution-bundle/evidencias/testes.md",
        "templates/execution-bundle/evidencias/logs-pods.md",
        "templates/execution-bundle/evidencias/telemetria-observabilidade.md",
        "templates/execution-bundle/analise/plano-diagnostico-detalhado.md",
        "templates/execution-bundle/analise/proposta-correcao.md",
    ]:
        assert (root / rel).exists(), rel


def test_no_placeholder_terms_in_release_contract():
    root = Path(__file__).resolve().parents[1]
    combined = "\n".join(p.read_text(encoding="utf-8") for p in root.rglob("*.md"))
    for term in ["TODO", "TBD", "FIXME", "god mode", "never fail"]:
        assert term not in combined
