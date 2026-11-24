"""Checks taken from the request, not from a worker's own report.

The sum example is the oracle: 2 + 2 is the asked case. 2 - 2, 2 * 3 and 2 / 0
must fail as sums. A function that returns 4 for every input still passes 2 + 2
and must fail those negatives.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

from always_on.adapters.commands import command_for
from always_on.application import SubprocessExecutor, Workforce
from always_on.domain.billing import BillingDecision, classify
from always_on.domain.glossary import PILLARS, TERMS
from always_on.domain.host import detect_host
from always_on.domain.lifecycle import Ledger, ResumeForbidden
from always_on.domain.oracle import RequestOracle
from always_on.domain.score import ReviewGate
from always_on.domain.silence import writer_is_silent
from always_on.domain.sum import Sum, UnsupportedOperation

SCRIPTS = Path(__file__).resolve().parents[1]
TASK = "Faça uma calculadora somar 2 + 2"


class ExplodingExecutor:
    def run(self, argv):
        raise AssertionError("executor must not run: " + " ".join(argv[:2]))


class RecordingExecutor:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def run(self, argv):
        self.calls.append(list(argv))
        code, stdout, stderr = self.responses.pop(0)
        return code, stdout, stderr


class BillingTests(unittest.TestCase):
    def test_priced_families_ask_and_are_not_unlimited(self):
        models = [
            "grok-4.7",
            "claude-sonnet-5-5",
            "gpt-5.6-codex",
            "gemini-2.5-pro",
            "zai-coding-plan/glm-5.3",
            "mystery-model",
        ]
        for model in models:
            decision = BillingDecision.for_model(model, set())
            self.assertNotEqual(decision.kind, "free", model)
            self.assertTrue(decision.asks, model)
            self.assertEqual(decision.limit, 3, model)

    def test_allowlist_cannot_make_grok_or_glm_free(self):
        allow = {"grok-4.7", "zai-coding-plan/glm-5.3", "echo-local"}
        self.assertEqual(classify("grok-4.7", allow), "paid")
        self.assertEqual(classify("zai-coding-plan/glm-5.3", allow), "paid")
        self.assertEqual(classify("echo-local", allow), "free")
        self.assertIsNone(BillingDecision.for_model("echo-local", allow).limit)

    def test_ollama_is_forbidden_even_when_declared_free(self):
        allow = {"ollama/llama3", "http://127.0.0.1:11434"}
        self.assertEqual(classify("ollama/llama3", allow), "forbidden")
        self.assertEqual(classify("local:11434", allow), "forbidden")

    def test_plan_for_grok_asks_and_does_not_spawn(self):
        workforce = Workforce(self._state("grok"), executor=ExplodingExecutor())
        payload = workforce.plan("cursor", "grok-4.7", TASK)
        self.assertEqual(payload["action"], "ask")
        self.assertEqual(payload["exit_code"], 4)
        self.assertIn("grok-4.7", payload["question"])
        self.assertNotIn("commands", payload)

    def test_paid_count_other_than_three_is_refused(self):
        workforce = Workforce(self._state("cap"), executor=ExplodingExecutor())
        refused = workforce.approve("cursor", "grok-4.7", TASK, "sim", count=9)
        self.assertEqual(refused["action"], "deny")
        self.assertNotIn("approval_id", refused)

    def test_paid_generation_is_consumed_and_the_next_one_asks_again(self):
        state = self._state("once")
        executor = RecordingExecutor([
            (0, "", ""),
            (0, json.dumps({"verdict": "SEGUIR", "threats": ["custo"]}), ""),
            (0, json.dumps({"verdict": "APPROVE", "findings": []}), ""),
        ])
        workforce = Workforce(state, executor=executor, test_runner=lambda _path: (0, 1))
        approval = workforce.approve("cursor", "grok-4.7", TASK, "sim")
        workspace = self._workspace("paid-run")
        first = workforce.spawn("cursor", "grok-4.7", TASK, workspace, approval["approval_id"], execute=True)
        self.assertEqual(len(executor.calls), 3)
        self.assertEqual(first["action"], "score")
        second = workforce.spawn("cursor", "grok-4.7", TASK, workspace, approval["approval_id"], execute=True)
        self.assertEqual(second["action"], "ask")
        self.assertEqual(len(executor.calls), 3)

    def test_free_model_has_no_cap_and_does_not_ask(self):
        workforce = Workforce(self._state("free"), {"echo-local"}, executor=ExplodingExecutor())
        payload = workforce.plan("opencode", "echo-local", TASK)
        self.assertEqual(payload["action"], "ready")
        self.assertIsNone(payload["limit"])
        self.assertIsNone(payload["question"])

    def _state(self, name):
        path = Path(self.id().split(".")[-1] + "-" + name)
        path.mkdir(exist_ok=True)
        self.addCleanup(lambda: _remove(path))
        return path

    def _workspace(self, name):
        path = Path(self.id().split(".")[-1] + "-" + name)
        path.mkdir(exist_ok=True)
        _write_worker_files(path)
        self.addCleanup(lambda: _remove(path))
        return path


class HostTests(unittest.TestCase):
    def test_cursor_window_binds_cursor_and_not_opencode(self):
        argv = command_for("cursor", "grok-4.7", "/work", "task body")
        self.assertEqual(argv[0], "agent")
        self.assertIn("--model", argv)
        self.assertEqual(argv[argv.index("--model") + 1], "grok-4.7")
        self.assertNotIn("opencode", argv)
        self.assertNotIn("--resume", argv)
        self.assertNotIn("--continue", argv)
        self.assertNotIn("--session", argv)
        self.assertEqual(argv[-1], "task body")
        self.assertIsInstance(argv, list)

    def test_opencode_window_binds_glm_and_not_cursor(self):
        argv = command_for("opencode", "zai-coding-plan/glm-5.3", "/work", "task body")
        self.assertEqual(argv[0], "opencode")
        self.assertEqual(argv[argv.index("--model") + 1], "zai-coding-plan/glm-5.3")
        self.assertNotIn("agent", argv[1:])
        self.assertNotIn("--continue", argv)
        self.assertNotIn("--session", argv)
        self.assertIn("--archived", argv)

    def test_detects_the_current_window_and_does_not_guess_a_model(self):
        self.assertEqual(detect_host({"CURSOR_AGENT": "1"}), "cursor")
        self.assertEqual(detect_host({"OPENCODE": "1"}), "opencode")
        self.assertEqual(detect_host({}), "unknown")
        workforce = Workforce(self._state(), executor=ExplodingExecutor())
        missing = workforce.plan("cursor", "", TASK)
        self.assertEqual(missing["action"], "ask")
        self.assertIn("modelo", missing["question"])

    def test_ollama_host_is_denied_before_any_process(self):
        workforce = Workforce(self._state(), executor=ExplodingExecutor())
        payload = workforce.plan("ollama", "llama3", TASK)
        self.assertEqual(payload["action"], "deny")
        self.assertEqual(payload["exit_code"], 2)

    def test_missing_binary_does_not_invent_a_run(self):
        result = SubprocessExecutor().run(["always-on-missing-binary", "--print"])
        self.assertEqual(result[0], 127)
        self.assertIn("binary_missing", result[2])

    def _state(self):
        path = Path(self.id().split(".")[-1])
        path.mkdir(exist_ok=True)
        self.addCleanup(lambda: _remove(path))
        return path


class LifecycleTests(unittest.TestCase):
    def test_a_dead_worker_cannot_resume_and_recreate_is_a_new_id(self):
        ledger = Ledger()
        first = ledger.born("task-sum", "writer")
        ledger.die(first.worker_id)
        with self.assertRaises(ResumeForbidden):
            ledger.resume(first.worker_id)
        second = ledger.recreate("task-sum", "writer")
        self.assertNotEqual(second.worker_id, first.worker_id)
        self.assertEqual(second.task_id, first.task_id)
        self.assertEqual(second.generation, first.generation + 1)
        self.assertTrue(second.resume_forbidden)
        self.assertEqual(ledger.get(first.worker_id).state, "died")


class SumOracleTests(unittest.TestCase):
    def test_two_plus_two_is_four(self):
        self.assertEqual(Sum.evaluate(2, 2), 4)

    def test_subtraction_fails_as_a_sum(self):
        with self.assertRaises(UnsupportedOperation):
            Sum.evaluate_operation("sub", 2, 2)

    def test_multiplication_fails_as_a_sum(self):
        with self.assertRaises(UnsupportedOperation):
            Sum.evaluate_operation("mul", 2, 3)

    def test_division_by_zero_fails_as_a_sum(self):
        with self.assertRaises(ZeroDivisionError):
            Sum.evaluate_operation("div", 2, 0)

    def test_positive_case_alone_accepts_a_constant_four(self):
        def constant(_left, _right):
            return 4

        self.assertEqual(constant(2, 2), 4)

    def test_negative_operations_reject_the_constant_four(self):
        def constant(_name, _left, _right):
            return 4

        with self.assertRaises(AssertionError):
            with self.assertRaises(UnsupportedOperation):
                constant("sub", 2, 2)
        with self.assertRaises(AssertionError):
            with self.assertRaises(ZeroDivisionError):
                constant("div", 2, 0)

    def test_negative_proofs_fail_and_a_tautology_does_not_count(self):
        oracle = RequestOracle()
        self.assertTrue(oracle.prove(Sum.evaluate))

        def returns_zero(_left, _right):
            return 0

        # 2 - 2 == 0, so this implementation makes a negative proof pass. That is not evidence.
        self.assertFalse(oracle.prove(returns_zero))


class SilenceTests(unittest.TestCase):
    def test_questions_are_kept_and_plans_are_rejected(self):
        self.assertTrue(writer_is_silent(""))
        self.assertTrue(writer_is_silent("QUESTION: qual arquivo devo alterar?\n"))
        self.assertFalse(writer_is_silent("Vou criar a calculadora e depois os testes.\n"))
        self.assertFalse(writer_is_silent("I will add the sum next.\n"))


class ScoreTests(unittest.TestCase):
    def test_a_complete_free_generation_clears_9_5(self):
        state = Path("score-free")
        workspace = Path("score-free-work")
        self.addCleanup(lambda: _remove(state))
        self.addCleanup(lambda: _remove(workspace))
        workspace.mkdir()
        _write_worker_files(workspace)
        executor = RecordingExecutor(_review_responses())
        workforce = Workforce(state, {"echo-local"}, executor=executor, test_runner=lambda _path: (0, 1))
        payload = workforce.spawn("cursor", "echo-local", TASK, workspace, execute=True)
        self.assertEqual(payload["score"], 10)
        self.assertTrue(payload["accepted"])
        self.assertGreaterEqual(payload["score"], 9.5)
        self.assertTrue(payload["claimed_score_ignored"])

    def test_missing_negative_proof_is_below_9_5_even_if_someone_claims_10(self):
        run = Path("score-weak")
        self.addCleanup(lambda: _remove(run))
        _materialize_run(run, negatives_exit=0, tests_exit=0, claimed_score=10)
        payload = ReviewGate().score(run, {"echo-local"})
        self.assertFalse(payload["checks"]["negative_proof"])
        self.assertLess(payload["score"], 9.5)
        self.assertFalse(payload["accepted"])
        self.assertNotEqual(payload["score"], 10)

    def test_writer_file_cannot_replace_the_reviewer_process(self):
        run = Path("score-forged")
        self.addCleanup(lambda: _remove(run))
        _materialize_run(run, negatives_exit=1, tests_exit=0)
        (run / "fool.stdout").write_text("I will approve this\n", encoding="utf-8")
        payload = ReviewGate().score(run, {"echo-local"})
        self.assertFalse(payload["checks"]["fool_lens"])
        self.assertLess(payload["score"], 9.5)
        self.assertFalse(payload["accepted"])

    def test_one_citation_miss_remains_on_the_9_5_bar(self):
        run = Path("score-soft")
        self.addCleanup(lambda: _remove(run))
        _materialize_run(run, negatives_exit=1, tests_exit=0)
        plan = (run / "workspace" / "plan.md").read_text(encoding="utf-8")
        (run / "workspace" / "plan.md").write_text(plan.replace("Demand Elegance\n", ""), encoding="utf-8")
        payload = ReviewGate().score(run, {"echo-local"})
        self.assertFalse(payload["checks"]["pillars_cited"])
        self.assertEqual(payload["score"], 9.5)
        self.assertTrue(payload["accepted"])
        self.assertEqual(payload["hard_failed"], [])


class GlossaryTests(unittest.TestCase):
    def test_each_term_names_a_class_in_its_module(self):
        domain = SCRIPTS / "always_on"
        for term, relative in TERMS.items():
            text = (domain / relative).read_text(encoding="utf-8")
            self.assertIn(f"class {term}", text, term)


class CliTests(unittest.TestCase):
    def test_plan_prints_only_json_and_asks_for_grok(self):
        env = os.environ.copy()
        env["PYTHONPATH"] = str(SCRIPTS)
        env["PYTHONIOENCODING"] = "utf-8"
        completed = subprocess.run(
            [sys.executable, "-m", "always_on", "plan", "--host", "cursor", "--model", "grok-4.7", "--task", TASK],
            cwd=SCRIPTS,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
            check=False,
        )
        self.assertEqual(completed.returncode, 4, completed.stderr)
        self.assertFalse(completed.stderr.strip())
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["action"], "ask")
        self.assertIn("grok-4.7", payload["question"])
        self.assertNotIn("I will", completed.stdout)
        self.assertNotIn("Vou ", completed.stdout)


def _review_responses():
    fool = json.dumps({"verdict": "SEGUIR COM AJUSTE", "threats": ["--force ainda depende do prompt"]})
    judge = json.dumps({"verdict": "APPROVE", "findings": []})
    return [(0, "", ""), (0, fool, ""), (0, judge, "")]


def _write_worker_files(workspace: Path) -> None:
    pillars = "\n".join(f"- {pillar}" for pillar in PILLARS)
    terms = "\n".join(f"- {term}" for term in TERMS)
    (workspace / "specify.md").write_text(
        "\n".join([
            "# specify",
            "spec-driven",
            "Request: Faça uma calculadora somar 2 + 2.",
            "The observable result of 2 + 2 is 4.",
            "Negative proofs that must fail as sums: 2 - 2, 2 * 3, 2 / 0.",
        ]),
        encoding="utf-8",
    )
    (workspace / "plan.md").write_text(
        "spec-driven-lean\n" + pillars + "\n",
        encoding="utf-8",
    )
    (workspace / "glossary.md").write_text(terms + "\n", encoding="utf-8")


def _materialize_run(run: Path, negatives_exit: int, tests_exit: int, claimed_score: int | None = None) -> None:
    workspace = run / "workspace"
    workspace.mkdir(parents=True)
    _write_worker_files(workspace)
    argv = command_for("cursor", "echo-local", str(workspace), "prompt que cita a task")
    meta = {
        "host": "cursor",
        "model": "echo-local",
        "task": TASK,
        "limit": None,
        "approval_id": None,
        "approved": False,
        "roles": ["writer", "fool", "judge"],
        "worker_ids": ["id-1", "id-2", "id-3"],
        "died": True,
        "state": "died",
        "resume_forbidden": True,
        "resume_attempted": False,
        "fool_source": "process",
        "judge_source": "process",
    }
    if claimed_score is not None:
        meta["claimed_score"] = claimed_score
    run.mkdir(parents=True, exist_ok=True)
    (run / "meta.json").write_text(json.dumps(meta), encoding="utf-8")
    (run / "argv.json").write_text(json.dumps(argv), encoding="utf-8")
    (run / "writer.prompt").write_text("task: " + TASK + "\n", encoding="utf-8")
    (run / "writer.stdout").write_text("", encoding="utf-8")
    (run / "fool.stdout").write_text(
        json.dumps({"verdict": "SEGUIR", "threats": ["sandbox"]}),
        encoding="utf-8",
    )
    (run / "judge.stdout").write_text(
        json.dumps({"verdict": "APPROVE", "findings": []}),
        encoding="utf-8",
    )
    (run / "tests.exit").write_text(str(tests_exit), encoding="utf-8")
    (run / "negatives.exit").write_text(str(negatives_exit), encoding="utf-8")


def _remove(path: Path) -> None:
    if not path.exists():
        return
    for child in sorted(path.rglob("*"), reverse=True):
        if child.is_file():
            child.unlink()
        else:
            child.rmdir()
    path.rmdir()


if __name__ == "__main__":
    unittest.main()
