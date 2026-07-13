from __future__ import annotations

from aeos.core.chromatic import ChromaticOrchestrator


def test_chromatic_orchestrator_selects_cloud_architecture_colors():
    colors = ChromaticOrchestrator().select_colors(
        "Evolve AEOS architecture for cloud readiness with security and rollout risks",
        decision_type="cloud-readiness",
    )

    assert "WHITE" in colors
    assert "BLUE" in colors
    assert "RED" in colors
    assert "BLACK" in colors
    assert len(colors) <= 5


def test_chromatic_run_blocks_high_impact_without_evidence():
    run = ChromaticOrchestrator().create_run(
        objective="Decide AEOS cloud deployment architecture",
        decision_type="cloud-readiness",
    )

    assert run.blocking_conditions
    assert "evidence_refs" in " ".join(run.blocking_conditions)


def test_chromatic_run_contains_handoffs_and_decision_matrix():
    run = ChromaticOrchestrator().create_run(
        objective="Compare two AEOS migration strategies",
        decision_type="migration",
        evidence_refs=["registry-validation.jsonl"],
    )

    assert not run.blocking_conditions
    assert run.handoffs
    assert run.decision_matrix
    assert all("color" in handoff for handoff in run.handoffs)
