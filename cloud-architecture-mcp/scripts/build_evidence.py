"""Build the tracked claims evidence used by the cloud architecture MCPs.

Inputs (research workspace, not tracked):
  --claims  path to the claims source module (claims.py: CLAIMS list)
  --triage  path to the JEV triage JSON of the final run (jev-triage.json)
Output (tracked): evidence/claims.json

Labels: JEV probability is recorded as triage (>=0.7 supported, <=0.3 not supported, else uncertain).
The two borderline claims were checked by hand; the reason is stored next to the label.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib

MANUAL = {
    "aws-opensearch-serverless-4ocu-ga": {
        "final": "supported_historical",
        "reason": "JEV p=0.62 (uncertain). Manual check: the 2023 GA blog states 4 OCUs and the no-activity instantiation verbatim. "
                  "The claim is historical and must not be read as current OpenSearch Serverless behavior.",
    },
    "az-signing-basic-price": {
        "final": "supported_manual",
        "reason": "JEV p=0.68 (uncertain). Manual check: the Azure product page states 'Basic Plan: $9.99/month for up to 5,000 "
                  "signatures'. The Azure Retail Prices convention is USD, so the $ sign is USD.",
    },
}

FIELDS = ("id", "provider", "topic", "control", "expected_true", "claim", "source_url", "source_kind", "excerpt")


def load_claims(path: pathlib.Path) -> list[dict]:
    spec = importlib.util.spec_from_file_location("claims_source", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.CLAIMS


def jev_label(p: float | None) -> str:
    if p is None:
        return "error"
    if p >= 0.7:
        return "supported"
    if p <= 0.3:
        return "not_supported"
    return "uncertain"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claims", required=True, type=pathlib.Path)
    parser.add_argument("--triage", required=True, type=pathlib.Path)
    parser.add_argument("--out", required=True, type=pathlib.Path)
    args = parser.parse_args()

    claims = load_claims(args.claims)
    triage_doc = json.loads(args.triage.read_text(encoding="utf-8"))
    triage = {row["id"]: row for row in triage_doc["rows"]}

    rows = []
    for claim in claims:
        result = triage[claim["id"]]
        final = jev_label(result["p_supported"])
        manual = MANUAL.get(claim["id"])
        if manual:
            final = manual["final"]
        row = {field: claim[field] for field in FIELDS}
        row.update({
            "jev_p_supported": result["p_supported"],
            "jev_label": result["label"],
            "final_label": final,
            "manual_note": manual["reason"] if manual else None,
        })
        rows.append(row)

    payload = {
        "description": "Claims verified against source excerpts; JEV Noul is triage, manual notes override only the listed borderline cases.",
        "jev_question_run": triage_doc["summary"]["retrieved_at"],
        "jev_thresholds": triage_doc["summary"]["thresholds"],
        "claims": rows,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {len(rows)} claims to {args.out}")


if __name__ == "__main__":
    main()
