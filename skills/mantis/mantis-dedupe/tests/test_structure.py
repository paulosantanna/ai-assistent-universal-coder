from pathlib import Path

def test_required_files():
    root=Path(__file__).resolve().parents[1]
    assert (root/'SKILL.md').exists()
    assert (root/'README.md').exists()
    assert (root/'AGENT.md').exists()
    assert (root/'knowledge'/'NEGATIVE_KNOWLEDGE.md').exists()
    assert (root/'evaluation'/'HONEST_EVALUATOR.md').exists()
