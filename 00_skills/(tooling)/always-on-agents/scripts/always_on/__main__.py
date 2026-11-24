"""JSON-only entry point. Stdout is one object. The question is the only user-facing text."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from always_on.application import Workforce
from always_on.domain.score import ReviewGate

PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def load_allowlist(path: Path | None = None) -> set[str]:
    source = path or (PACKAGE_ROOT / "free-models.json")
    data = json.loads(source.read_text(encoding="utf-8"))
    return set(data.get("models") or [])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="always_on", description="Same-model code workers")
    parser.add_argument("--state", default=".always-on")
    parser.add_argument("--allowlist", default="")
    sub = parser.add_subparsers(dest="command", required=True)

    plan = sub.add_parser("plan")
    _common(plan)

    approve = sub.add_parser("approve")
    _common(approve)
    approve.add_argument("--answer", required=True)

    spawn = sub.add_parser("spawn")
    _common(spawn)
    spawn.add_argument("--workspace", required=True)
    spawn.add_argument("--approval", default="")
    spawn.add_argument("--execute", action="store_true")

    score = sub.add_parser("score")
    score.add_argument("--run", required=True)
    return parser


def _common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--host", default="")
    parser.add_argument("--model", default="")
    parser.add_argument("--task", default="")


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = build_parser().parse_args(argv)
    allowlist = load_allowlist(Path(args.allowlist) if args.allowlist else None)
    if args.command == "score":
        payload = ReviewGate().score(Path(args.run), allowlist)
        payload["action"] = "score"
        payload["exit_code"] = 0 if payload["accepted"] else 1
        payload["question"] = None
        _emit(payload)
        return payload["exit_code"]
    workforce = Workforce(Path(args.state), allowlist)
    if args.command == "plan":
        payload = workforce.plan(args.host, args.model, args.task)
    elif args.command == "approve":
        payload = workforce.approve(args.host, args.model, args.task, args.answer)
    else:
        payload = workforce.spawn(
            args.host,
            args.model,
            args.task,
            Path(args.workspace),
            approval_id=args.approval or None,
            execute=args.execute,
        )
    _emit(payload)
    return int(payload["exit_code"])


def _emit(payload: dict) -> None:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
