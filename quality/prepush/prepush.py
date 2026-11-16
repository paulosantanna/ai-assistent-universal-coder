"""Pre-push gate. Exit 0 passes, 1 fails a check, 2 is blocked because a source could not be refreshed."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from engine import HERE, run, write_report


def install_hook(repo: Path) -> Path:
    git = repo / ".git"
    if git.is_file():
        line = next(item for item in git.read_text(encoding="utf-8").splitlines() if item.startswith("gitdir:"))
        git = Path(line.split(":", 1)[1].strip())
        if not git.is_absolute():
            git = (repo / git).resolve()
    destination = git / "hooks" / "pre-push"
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = (HERE / "hooks" / "pre-push").read_bytes().replace(b"\r\n", b"\n")
    destination.write_bytes(payload)
    destination.chmod(0o755)
    return destination


def render(report: dict) -> str:
    lines = [f"prepush: {report['status'].upper()}"]
    shown = 0
    for backend in report["backends"]:
        count = len(backend["findings"])
        lines.append(f"{backend['id']}: {backend['status']} ({count})")
        for item in backend["findings"]:
            if shown >= 40:
                lines.append("... demais achados em .aeos/prepush/report.json")
                return "\n".join(lines)
            lines.append(f"  {item['code']} {item['message']}")
            shown += 1
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Valida CVE, bibliotecas, linguagem, executaveis, SAST e seguranca antes do push.")
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--install-hook", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    repo = args.repo.resolve()
    if args.install_hook:
        destination = install_hook(repo)
        print(f"hook instalado em {destination}")
        if len(argv if argv is not None else sys.argv[1:]) == 1:
            return 0
    report = run(repo)
    try:
        write_report(report, repo)
    except OSError as exc:
        print(f"prepush: relatorio nao gravado: {exc}", file=sys.stderr)
    print(json.dumps(report, ensure_ascii=False, indent=2) if args.json else render(report))
    if report["status"] == "pass":
        return 0
    if report["status"] == "blocked":
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
