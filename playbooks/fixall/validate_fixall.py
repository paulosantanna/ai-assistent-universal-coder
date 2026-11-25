#!/usr/bin/env python3
"""Aprova ou reprova o playbook fixall e um run.json. Nao atribui nota."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLAYBOOK = Path(__file__).resolve().parent / "PLAYBOOK.md"
REQUIRED = (
    "spec-driven",
    "spec-driven-lean",
    "the-fool",
    "the-judge",
    "qa-expert",
    "pentests-expert",
    "07_mapeamentos",
    "codenavi-agent",
    "quality/prepush/prepush.py",
    "sast",
    "9/10",
)


def validate_playbook(text):
    errors = []
    for token in REQUIRED:
        if token not in text:
            errors.append(f"playbook sem {token}")
    if "se o pedido já disse que não sobe" not in text.lower() and "nao sobe" not in text.lower():
        errors.append("playbook sem a regra de nao subir quando o usuario recusou")
    if "pergunte" not in text.lower():
        errors.append("playbook sem a pergunta quando o envio nao foi dito")
    if "não invent" not in text.lower() and "nao invent" not in text.lower():
        errors.append("playbook sem a proibicao de inventar")
    if "opcional" not in text.lower() and "somente se o pedido chamar" not in text.lower():
        errors.append("pentests-expert precisa ser opcional")
    return errors


def validate_run(record, evidence_root):
    errors = []
    if record.get("invented") is True:
        errors.append("run marca invented")
    push = record.get("push")
    if push not in {"no", "ask", "yes"}:
        errors.append("push deve ser no, ask ou yes")
    performed = record.get("push_performed")
    if push in {"no", "ask"} and performed is True and record.get("answer") != "yes":
        errors.append("envio ao GitHub sem resposta yes")
    if push == "no" and performed is True:
        errors.append("usuario recusou o envio e o run subiu")
    stages = record.get("stages")
    if not isinstance(stages, list) or not stages:
        return errors + ["run sem etapas"]
    for stage in stages:
        attempts = stage.get("attempts") or []
        if not attempts:
            errors.append(f"{stage.get('id')} sem attempts")
            continue
        below = [item for item in attempts if _score(item, "fool") < 9 or _score(item, "judge") < 9]
        accepted = [item for item in attempts if _score(item, "fool") >= 9 and _score(item, "judge") >= 9]
        if stage.get("required", True) and not accepted:
            if len(attempts) >= 3:
                errors.append(f"{stage.get('id')} estourou 3 tentativas abaixo de 9 e precisa perguntar")
            else:
                errors.append(f"{stage.get('id')} abaixo de 9/10")
        if len(below) >= 3 and not accepted:
            errors.append(f"{stage.get('id')} nao pode ser done")
        for item in accepted:
            evidence = item.get("evidence") or []
            if not evidence:
                errors.append(f"{stage.get('id')} aceito sem evidencia")
            for ref in evidence:
                path = evidence_root / ref
                if not path.is_file():
                    errors.append(f"evidencia ausente: {ref}")
            if item.get("payload") or item.get("command") or item.get("reproduction"):
                errors.append(f"{stage.get('id')} guardou payload, comando ou reproducao")
    pentest = record.get("pentest")
    if pentest == "called" and "pentests-expert" not in {stage.get("id") for stage in stages}:
        errors.append("pentest chamado sem etapa pentests-expert")
    if pentest == "not_called" and any(stage.get("id") == "pentests-expert" and stage.get("required") for stage in stages):
        errors.append("pentest nao pedido nao pode ser etapa obrigatoria")
    return errors


def _score(item, key):
    value = item.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return -1
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--playbook", type=Path, default=PLAYBOOK)
    parser.add_argument("--run", type=Path)
    parser.add_argument("--evidence-root", type=Path, default=ROOT)
    args = parser.parse_args()
    errors = validate_playbook(args.playbook.read_text(encoding="utf-8"))
    if args.run:
        errors.extend(validate_run(json.loads(args.run.read_text(encoding="utf-8")), args.evidence_root))
    status = "PASS" if not errors else "FAIL"
    json.dump({"status": status, "errors": errors}, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
