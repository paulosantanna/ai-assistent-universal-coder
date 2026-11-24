"""One generation: plan, optional approval, three processes, score, death."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from uuid import uuid4

from always_on.domain.billing import PAID_GENERATION_LIMIT, BillingDecision, accepts_answer, is_ollama
from always_on.domain.glossary import PILLARS, TERMS
from always_on.domain.host import ADAPTERS, HostSession, detect_host, require_model
from always_on.domain.lifecycle import Ledger
from always_on.adapters.commands import command_for
from always_on.domain.score import ROLES, ReviewGate

ROLES_LIST = list(ROLES)


class SubprocessExecutor:
    def run(self, argv: list[str]) -> tuple[int, str, str]:
        binary = shutil.which(argv[0])
        if binary is None:
            return 127, "", "binary_missing:" + argv[0]
        completed = subprocess.run(
            [binary, *argv[1:]],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=False,
            check=False,
        )
        return completed.returncode, completed.stdout, completed.stderr


class Workforce:
    def __init__(self, state_dir: Path, allowlist: set[str] | None = None, executor=None, test_runner=None):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.allowlist = set(allowlist or [])
        self.executor = executor if executor is not None else SubprocessExecutor()
        self.test_runner = test_runner
        self.ledger = Ledger()

    def plan(self, host: str | None, model: str | None, task: str, env: dict | None = None) -> dict:
        resolved_host = (host or detect_host(env or {})).strip().lower()
        resolved_model = require_model(model)
        if is_ollama(resolved_host) or is_ollama(resolved_model or ""):
            return _result("deny", "Ollama está fora deste módulo.", 2)
        if resolved_host not in ADAPTERS:
            return _result(
                "ask",
                "Qual é a janela desta sessão: cursor ou opencode? Não vou adivinhar o host.",
                4,
                host=resolved_host,
            )
        if not resolved_model:
            return _result(
                "ask",
                "Qual é o modelo desta janela? Não vou adivinhar.",
                4,
                host=resolved_host,
            )
        decision = BillingDecision.for_model(resolved_model, self.allowlist)
        session = HostSession(resolved_host, resolved_model)
        if decision.kind == "forbidden":
            return _result("deny", "Ollama está fora deste módulo.", 2, host=session.host, model=session.model)
        if decision.asks:
            return _result(
                "ask",
                _question(session.host, session.model),
                4,
                host=session.host,
                model=session.model,
                billing=decision.kind,
                limit=decision.limit,
            )
        return _result(
            "ready",
            None,
            0,
            host=session.host,
            model=session.model,
            billing="free",
            limit=None,
            task=task,
        )

    def approve(self, host: str, model: str, task: str, answer: str, count: int = PAID_GENERATION_LIMIT) -> dict:
        decision = BillingDecision.for_model(model, self.allowlist)
        if decision.kind == "free":
            return _result("deny", "Modelo gratuito não pede autorização.", 2, host=host, model=model)
        if decision.kind == "forbidden" or is_ollama(host):
            return _result("deny", "Ollama está fora deste módulo.", 2)
        if not accepts_answer(answer):
            return _result("ask", _question(host, model), 4, host=host, model=model, billing=decision.kind)
        if count != PAID_GENERATION_LIMIT:
            return _result(
                "deny",
                f"Uma geração paga tem exatamente {PAID_GENERATION_LIMIT} processos.",
                2,
                host=host,
                model=model,
            )
        approval_id = str(uuid4())
        record = {
            "id": approval_id,
            "host": host,
            "model": model,
            "task": task,
            "count": count,
            "answer": answer.strip().lower(),
            "consumed": False,
        }
        path = self.state_dir / "approvals" / f"{approval_id}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(record, ensure_ascii=False), encoding="utf-8")
        return _result("approved", None, 0, host=host, model=model, billing=decision.kind, approval_id=approval_id, limit=count)

    def spawn(self, host: str, model: str, task: str, workspace: Path, approval_id: str | None = None, execute: bool = False) -> dict:
        planned = self.plan(host, model, task)
        if planned["action"] == "deny":
            return planned
        if planned["action"] == "ask" and not approval_id:
            return planned
        if planned["billing"] == "free":
            approval_id = None
        record = None
        if planned["billing"] != "free":
            record = self._load_approval(approval_id)
            if record is None or record.get("consumed") or record.get("host") != host or record.get("model") != model or record.get("task") != task:
                return _result("ask", _question(host, model), 4, host=host, model=model, billing=planned["billing"])
        task_id = str(uuid4())
        workers = [self.ledger.born(task_id, role, 1) for role in ROLES_LIST]
        prompts = {role: _prompt(role, host, model, task) for role in ROLES_LIST}
        commands = {
            role: command_for(host, model, str(workspace), prompts[role])
            for role in ROLES_LIST
        }
        if not execute:
            for worker in workers:
                self.ledger.die(worker.worker_id)
            return _result(
                "dry-run",
                None,
                0,
                host=host,
                model=model,
                billing=planned["billing"],
                limit=planned["limit"],
                commands={role: commands[role] for role in ROLES_LIST},
                worker_ids=[worker.worker_id for worker in workers],
            )
        outputs = {}
        for role in ROLES_LIST:
            code, stdout, stderr = self.executor.run(commands[role])
            outputs[role] = {"code": code, "stdout": stdout, "stderr": stderr}
            if code == 127:
                for worker in workers:
                    if self.ledger.get(worker.worker_id).state != "died":
                        self.ledger.die(worker.worker_id)
                return _result(
                    "deny",
                    "O binário do host não está instalado: " + commands[role][0],
                    3,
                    host=host,
                    model=model,
                    billing=planned["billing"],
                )
        for worker in workers:
            self.ledger.die(worker.worker_id)
        if record is not None:
            record["consumed"] = True
            self._save_approval(record)
        tests_exit, negatives_exit = (1, 1)
        if self.test_runner is not None:
            tests_exit, negatives_exit = self.test_runner(workspace)
        run_dir = self._write_run(
            workspace=workspace,
            host=host,
            model=model,
            task=task,
            billing=planned["billing"],
            limit=planned["limit"],
            approval_id=approval_id,
            workers=workers,
            prompts=prompts,
            commands=commands,
            outputs=outputs,
            tests_exit=tests_exit,
            negatives_exit=negatives_exit,
        )
        scored = ReviewGate().score(run_dir, self.allowlist)
        scored.update({
            "action": "score",
            "exit_code": 0 if scored["accepted"] else 1,
            "run_dir": str(run_dir),
            "recreate": not scored["accepted"],
            "host": host,
            "model": model,
            "billing": planned["billing"],
            "question": None,
        })
        if not scored["accepted"] and planned["billing"] != "free":
            scored["question"] = _question(host, model)
            scored["action"] = "ask"
            scored["exit_code"] = 4
        return scored

    def recreate(self, task_id: str, role: str):
        return self.ledger.recreate(task_id, role)

    def _load_approval(self, approval_id: str | None) -> dict | None:
        if not approval_id:
            return None
        path = self.state_dir / "approvals" / f"{approval_id}.json"
        if not path.is_file():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def _save_approval(self, record: dict) -> None:
        path = self.state_dir / "approvals" / f"{record['id']}.json"
        path.write_text(json.dumps(record, ensure_ascii=False), encoding="utf-8")

    def _write_run(self, workspace, host, model, task, billing, limit, approval_id, workers, prompts, commands, outputs, tests_exit, negatives_exit) -> Path:
        run_dir = self.state_dir / "runs" / workers[0].worker_id
        mirror = run_dir / "workspace"
        mirror.mkdir(parents=True)
        for name in ("specify.md", "plan.md", "glossary.md"):
            source = Path(workspace) / name
            if source.is_file():
                (mirror / name).write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        meta = {
            "host": host,
            "model": model,
            "task": task,
            "billing": billing,
            "limit": limit,
            "approval_id": approval_id,
            "approved": approval_id is not None and billing != "free",
            "approval_count": PAID_GENERATION_LIMIT if billing != "free" else None,
            "roles": ROLES_LIST,
            "worker_ids": [worker.worker_id for worker in workers],
            "died": True,
            "state": "died",
            "resume_forbidden": True,
            "resume_attempted": False,
            "fool_source": "process",
            "judge_source": "process",
            "generation": 1,
        }
        (run_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
        (run_dir / "argv.json").write_text(json.dumps(commands["writer"], ensure_ascii=False), encoding="utf-8")
        (run_dir / "writer.prompt").write_text(prompts["writer"], encoding="utf-8")
        (run_dir / "writer.stdout").write_text(outputs["writer"]["stdout"], encoding="utf-8")
        (run_dir / "fool.stdout").write_text(outputs["fool"]["stdout"], encoding="utf-8")
        (run_dir / "judge.stdout").write_text(outputs["judge"]["stdout"], encoding="utf-8")
        (run_dir / "tests.exit").write_text(str(tests_exit), encoding="utf-8")
        (run_dir / "negatives.exit").write_text(str(negatives_exit), encoding="utf-8")
        return run_dir


def _question(host: str, model: str) -> str:
    return (
        f"O modelo {model} no host {host} não é gratuito neste módulo. "
        f"Uma geração paga cria {PAID_GENERATION_LIMIT} processos (código, the-fool, the-judge), "
        "eles morrem ao terminar, e outra geração precisa de nova autorização. Criar esta geração?"
    )


def _prompt(role: str, host: str, model: str, task: str) -> str:
    pillars = ", ".join(PILLARS)
    terms = ", ".join(TERMS)
    if role == "writer":
        return (
            f"codenavi-agent worker. host={host} model={model}\n"
            f"task: {task}\n"
            "Write files only. Stdout may contain QUESTION: lines and nothing else.\n"
            "Start with specify.md for spec-driven and plan.md for spec-driven-lean.\n"
            f"Cite the pillars: {pillars}.\n"
            f"Use the glossary terms: {terms}.\n"
            "Tests assert the request, including 2 + 2 = 4, and the negative proofs 2 - 2, 2 * 3 and 2 / 0 must fail.\n"
        )
    if role == "fool":
        return (
            "codenavi-agent applying the the-fool lens. Do not edit code. "
            "Stdout is one JSON object with verdict and threats. "
            f"task: {task}\n"
        )
    return (
        "codenavi-agent applying the the-judge lens. Do not edit code. "
        "Stdout is one JSON object with verdict and findings. "
        f"task: {task}\n"
    )


def _result(action: str, question: str | None, exit_code: int, **extra) -> dict:
    payload = {
        "action": action,
        "question": question,
        "exit_code": exit_code,
        "claimed_score_ignored": True,
    }
    payload.update(extra)
    return payload
