from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from aeos.core.playbook_engine.playbook_dag import PlaybookDAG
from aeos.core.playbook_engine.playbook_models import PlaybookContract, PlaybookStep


class TestPlaybookDAG:
    def test_dag_no_cycles_for_linear_steps(self):
        contract = PlaybookContract(
            id="test-playbook",
            objective="Test DAG",
            required_agents=[],
            required_skills=[],
            required_lcps=[],
            allowed_mcps=[],
            steps=[
                PlaybookStep(id="step-1", depends_on=[]),
                PlaybookStep(id="step-2", depends_on=["step-1"]),
                PlaybookStep(id="step-3", depends_on=["step-2"]),
            ],
            blocking_conditions=[],
            outputs=[],
            final_report_sections=[],
        )
        dag = PlaybookDAG(contract)
        cycles = dag.detect_cycles()
        assert len(cycles) == 0

    def test_dag_detects_cycle(self):
        contract = PlaybookContract(
            id="test-cycle",
            objective="Test cycle detection",
            required_agents=[],
            required_skills=[],
            required_lcps=[],
            allowed_mcps=[],
            steps=[
                PlaybookStep(id="step-1", depends_on=["step-3"]),
                PlaybookStep(id="step-2", depends_on=["step-1"]),
                PlaybookStep(id="step-3", depends_on=["step-2"]),
            ],
            blocking_conditions=[],
            outputs=[],
            final_report_sections=[],
        )
        dag = PlaybookDAG(contract)
        cycles = dag.detect_cycles()
        assert len(cycles) > 0

    def test_dag_topological_sort(self):
        contract = PlaybookContract(
            id="test-sort",
            objective="Test topological sort",
            required_agents=[],
            required_skills=[],
            required_lcps=[],
            allowed_mcps=[],
            steps=[
                PlaybookStep(id="a", depends_on=[]),
                PlaybookStep(id="b", depends_on=["a"]),
                PlaybookStep(id="c", depends_on=["a"]),
                PlaybookStep(id="d", depends_on=["b", "c"]),
            ],
            blocking_conditions=[],
            outputs=[],
            final_report_sections=[],
        )
        dag = PlaybookDAG(contract)
        order = dag.topological_sort()
        order_ids = [s.id for s in order]
        assert order_ids.index("a") < order_ids.index("b")
        assert order_ids.index("a") < order_ids.index("c")
        assert order_ids.index("b") < order_ids.index("d")
        assert order_ids.index("c") < order_ids.index("d")

    def test_dag_ready_steps(self):
        contract = PlaybookContract(
            id="test-ready",
            objective="Test ready steps",
            required_agents=[],
            required_skills=[],
            required_lcps=[],
            allowed_mcps=[],
            steps=[
                PlaybookStep(id="a", depends_on=[]),
                PlaybookStep(id="b", depends_on=["a"]),
                PlaybookStep(id="c", depends_on=["a"]),
            ],
            blocking_conditions=[],
            outputs=[],
            final_report_sections=[],
        )
        dag = PlaybookDAG(contract)
        ready = dag.ready_steps(set())
        assert len(ready) == 1
        assert ready[0].id == "a"

        ready = dag.ready_steps({"a"})
        assert len(ready) == 2
        assert {s.id for s in ready} == {"b", "c"}

    def test_dag_unresolved_dependencies(self):
        contract = PlaybookContract(
            id="test-unresolved",
            objective="Test unresolved deps",
            required_agents=[],
            required_skills=[],
            required_lcps=[],
            allowed_mcps=[],
            steps=[
                PlaybookStep(id="step-1", skill="skill-a", depends_on=[]),
                PlaybookStep(id="step-2", skill="skill-b", depends_on=["step-1"]),
            ],
            blocking_conditions=[],
            outputs=[],
            final_report_sections=[],
        )
        dag = PlaybookDAG(contract)
        unresolved = dag.detect_unresolved_dependencies(["skill-a"])
        assert len(unresolved) == 1
        assert "skill-b" in unresolved[0]
