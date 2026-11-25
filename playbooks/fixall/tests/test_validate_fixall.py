import importlib.util
import unittest
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(
    "validate_fixall",
    Path(__file__).resolve().parents[1] / "validate_fixall.py",
)
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)
validate_playbook = _MODULE.validate_playbook
validate_run = _MODULE.validate_run

PLAYBOOK = Path("playbooks/fixall/PLAYBOOK.md").read_text(encoding="utf-8")


def attempt(fool, judge, evidence=("playbooks/fixall/PLAYBOOK.md",)):
    return {"fool": fool, "judge": judge, "evidence": list(evidence)}


class PlaybookTests(unittest.TestCase):
    def test_playbook_contract(self):
        self.assertEqual(validate_playbook(PLAYBOOK), [])

    def test_low_score_is_rejected(self):
        record = {"push": "no", "push_performed": False, "invented": False, "pentest": "not_called",
                  "stages": [{"id": "spec-driven", "attempts": [attempt(8, 10)]}]}
        errors = validate_run(record, Path("."))
        self.assertTrue(any("abaixo de 9" in item for item in errors))

    def test_third_failure_asks_instead_of_passing(self):
        record = {"push": "ask", "push_performed": False, "invented": False, "pentest": "not_called",
                  "stages": [{"id": "qa-expert", "attempts": [attempt(8, 8), attempt(8, 9), attempt(9, 8)]}]}
        errors = validate_run(record, Path("."))
        self.assertTrue(any("perguntar" in item for item in errors))

    def test_pass_requires_real_evidence_and_respects_no_push(self):
        record = {"push": "no", "push_performed": False, "invented": False, "pentest": "not_called",
                  "stages": [{"id": "spec-driven-lean", "attempts": [attempt(9, 9)]}]}
        self.assertEqual(validate_run(record, Path(".")), [])

    def test_missing_evidence_file_fails(self):
        record = {"push": "yes", "push_performed": False, "invented": False, "pentest": "not_called",
                  "stages": [{"id": "the-judge", "attempts": [attempt(9, 10, ("nao/existe.md",))]}]}
        errors = validate_run(record, Path("."))
        self.assertTrue(any("evidencia ausente" in item for item in errors))

    def test_push_after_refusal_fails(self):
        record = {"push": "no", "push_performed": True, "invented": False, "pentest": "not_called",
                  "stages": [{"id": "the-fool", "attempts": [attempt(9, 9)]}]}
        errors = validate_run(record, Path("."))
        self.assertTrue(any("recusou" in item for item in errors))

    def test_optional_pentest_is_not_required(self):
        record = {"push": "ask", "push_performed": False, "invented": False, "pentest": "not_called",
                  "stages": [{"id": "qa-expert", "attempts": [attempt(9, 9)]}]}
        self.assertEqual(validate_run(record, Path(".")), [])

    def test_payload_field_is_rejected(self):
        bad = attempt(9, 9)
        bad["payload"] = "no"
        record = {"push": "no", "push_performed": False, "invented": False, "pentest": "called",
                  "stages": [{"id": "pentests-expert", "attempts": [bad]}]}
        errors = validate_run(record, Path("."))
        self.assertTrue(any("payload" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
