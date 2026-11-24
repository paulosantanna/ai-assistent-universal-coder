"""Twenty checks. Nineteen is 9.5. A self-reported score is not read."""

from __future__ import annotations

import json
from pathlib import Path

from always_on.domain.billing import PAID_GENERATION_LIMIT, classify, is_ollama
from always_on.domain.glossary import PILLARS, TERMS
from always_on.domain.host import ADAPTERS
from always_on.domain.oracle import REQUIRED_NEGATIVES
from always_on.domain.silence import writer_is_silent

PASS_AT = 19
# A single miss among the citation checks can still score 9.5.
# Any miss here is a failure and the reported score cannot stay on the bar.
HARD_CHECKS = (
    "not_ollama",
    "billing_gate",
    "negative_proof",
    "tests_green",
    "silence",
    "fool_lens",
    "judge_lens",
    "died",
    "no_resume",
    "reviewers_from_process",
)
ROLES = ("writer", "fool", "judge")
RESUME_FLAGS = ("--resume", "--continue", "--session")
CHECK_IDS = (
    "host_bound",
    "model_bound",
    "not_ollama",
    "billing_gate",
    "generation_shape",
    "spec_driven",
    "spec_lean",
    "request_oracle",
    "negative_proof",
    "ddd_glossary",
    "pillars_cited",
    "silence",
    "tests_green",
    "fool_lens",
    "judge_lens",
    "died",
    "no_resume",
    "fresh_ids",
    "reviewers_from_process",
    "qualified_task",
)


def _load(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def _json_object(text: str) -> dict:
    text = (text or "").strip()
    if not text:
        return {}
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _flag(argv: list, name: str) -> str:
    if name not in argv:
        return ""
    index = argv.index(name)
    if index + 1 >= len(argv):
        return ""
    return str(argv[index + 1])


class ReviewGate:
    def score(self, run_dir: Path, allowlist: set[str] | None = None) -> dict:
        allowlist = allowlist or set()
        meta = _json_object(_load(run_dir / "meta.json"))
        argv_value = json.loads(_load(run_dir / "argv.json") or "[]")
        argv = [str(item) for item in argv_value] if isinstance(argv_value, list) else []
        # The last element is the prompt. It is allowed to mention Ollama as a prohibition.
        scanned = argv[:-1]
        scanned_text = " ".join(scanned)
        workspace = run_dir / "workspace"
        specify = _load(workspace / "specify.md")
        plan = _load(workspace / "plan.md")
        glossary = _load(workspace / "glossary.md")
        writer = _load(run_dir / "writer.stdout")
        fool = _json_object(_load(run_dir / "fool.stdout"))
        judge = _json_object(_load(run_dir / "judge.stdout"))
        model = str(meta.get("model") or "")
        host = str(meta.get("host") or "")
        billing = classify(model, allowlist)
        ids = list(meta.get("worker_ids") or [])
        roles = list(meta.get("roles") or [])
        checks = {
            "host_bound": host in ADAPTERS and _binary_matches(host, argv),
            "model_bound": bool(model) and _flag(argv, "--model") == model,
            "not_ollama": not any(is_ollama(part) for part in (model, host, scanned_text)),
            "billing_gate": _billing_ok(meta, billing),
            "generation_shape": roles == list(ROLES) and len(ids) == PAID_GENERATION_LIMIT,
            "spec_driven": "spec-driven" in specify.lower() and "specify" in specify.lower(),
            "spec_lean": "spec-driven-lean" in plan.lower(),
            "request_oracle": "2 + 2" in specify and "4" in specify,
            "negative_proof": _negatives(run_dir, specify),
            "ddd_glossary": all(term in glossary for term in TERMS),
            "pillars_cited": all(pillar in plan for pillar in PILLARS),
            "silence": writer_is_silent(writer),
            "tests_green": _load(run_dir / "tests.exit").strip() == "0",
            "fool_lens": fool.get("verdict") in {"SEGUIR", "SEGUIR COM AJUSTE"} and bool(fool.get("threats")),
            "judge_lens": judge.get("verdict") == "APPROVE" and not judge.get("findings"),
            "died": meta.get("died") is True and meta.get("state") == "died",
            "no_resume": meta.get("resume_forbidden") is True
            and meta.get("resume_attempted") is False
            and not any(flag in scanned for flag in RESUME_FLAGS),
            "fresh_ids": len(ids) == len(set(ids)) == PAID_GENERATION_LIMIT,
            "reviewers_from_process": meta.get("fool_source") == "process" and meta.get("judge_source") == "process",
            "qualified_task": bool(meta.get("task")) and str(meta["task"]) in _load(run_dir / "writer.prompt"),
        }
        missing = [name for name in CHECK_IDS if name not in checks]
        if missing:
            raise RuntimeError("score map drifted: " + ",".join(missing))
        passed = sum(1 for name in CHECK_IDS if checks[name])
        hard_failed = [name for name in HARD_CHECKS if not checks[name]]
        score = passed / 2
        accepted = passed >= PASS_AT and not hard_failed
        if hard_failed and score >= PASS_AT / 2:
            score = 9.0
        return {
            "passed_checks": passed,
            "score": score,
            "accepted": accepted,
            "hard_failed": hard_failed,
            "checks": {name: bool(checks[name]) for name in CHECK_IDS},
            "claimed_score_ignored": True,
        }


def _binary_matches(host: str, argv: list[str]) -> bool:
    if not argv:
        return False
    binary = Path(argv[0]).name
    if host == "cursor":
        return binary in {"agent", "cursor-agent"}
    if host == "opencode":
        return binary == "opencode"
    return False


def _billing_ok(meta: dict, billing: str) -> bool:
    if billing == "free":
        return meta.get("limit") is None and not meta.get("approval_id")
    if billing in {"paid", "unknown"}:
        return (
            meta.get("approved") is True
            and meta.get("approval_count") == PAID_GENERATION_LIMIT
            and meta.get("limit") == PAID_GENERATION_LIMIT
        )
    return False


def _negatives(run_dir: Path, specify: str) -> bool:
    exit_code = _load(run_dir / "negatives.exit").strip()
    if exit_code in {"", "0"}:
        return False
    return all(expr in specify for expr in REQUIRED_NEGATIVES)
