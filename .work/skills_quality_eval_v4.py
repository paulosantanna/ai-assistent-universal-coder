"""skills-quality-eval v4 (rubric Amendment A3): ALL 324 skills, full SKILL.md text, independent consensus labels.

Subcommands: prereg | silver | shards | jev
Run from the workspace root. The JEV key is read in memory by workspace-brain's client and never printed.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import random
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, r"E:\Github\workspace-brain")
import skills_quality_eval_v2 as v2  # noqa: E402  (silver rules: KEY_RE, SENT_RE, label())

ROOT = v2.ROOT
WORK = v2.WORK
A3 = WORK / "a3"
THRESHOLD_YES, THRESHOLD_NO = 0.7, 0.3
N_SHARDS = 6
SHARD_SEED = 20261119
DIMS = ("gov_codenavi", "provenance_pointer", "secrets_runtime_only", "fail_closed")

# Frozen question texts. Annotators receive the SAME construct definition as JEV (one condition each).
QUESTIONS = {
    "gov_codenavi": v2.QUESTIONS["gov_codenavi"],
    "provenance_pointer": v2.QUESTIONS["provenance_pointer"],
    # Amendment A2 wording (was too narrow in v2).
    "secrets_runtime_only": (
        "This skill text contains at least one explicit rule that protects secrets or credentials: "
        "keeping them in runtime providers, redacting or masking them, or never persisting them. "
        "Answer no if secrets are not mentioned or are mentioned without any protective rule."
    ),
    "fail_closed": v2.QUESTIONS["fail_closed"],
}

GATES = {
    "reliability_kappa_min": 0.70,
    "reliability_low_prevalence": {"minority_below": 0.10, "ac1_min": 0.85, "raw_agreement_min": 0.92},
    "unresolved_max": 0.05,
    "jev_precision_min": 0.85,
    "jev_approved_min": 20,
    "negatives_min_for_pass": 10,
    "triage_p_min": 0.70,
}


def skills_text() -> dict[str, str]:
    catalog = json.loads((ROOT / "00_skills/catalog.json").read_text(encoding="utf-8"))
    return {
        s["id"]: (ROOT / s["path"].replace("/", "\\")).read_text(encoding="utf-8", errors="replace")
        for s in catalog["skills"]
    }


def frozen_sha(ids: list[str]) -> str:
    blob = json.dumps(
        {"questions": QUESTIONS, "gates": GATES, "dims": DIMS, "yes": THRESHOLD_YES, "no": THRESHOLD_NO,
         "shards": N_SHARDS, "shard_seed": SHARD_SEED, "ids": ids, "silver_rules": v2.rules_sha()},
        sort_keys=True,
    )
    return hashlib.sha256(blob.encode()).hexdigest()


def cmd_prereg() -> None:
    texts = skills_text()
    ids = sorted(texts)
    dev = set(json.loads((WORK / "sample.json").read_text(encoding="utf-8"))["skills"])
    h1 = set(json.loads((WORK / "judgments-v2.json").read_text(encoding="utf-8")))
    A3.mkdir(parents=True, exist_ok=True)
    out = {
        "amendment": "A3",
        "declared_before_any_a3_run": True,
        "frozen_sha256": frozen_sha(ids),
        "n_skills": len(ids),
        "text": "full SKILL.md",
        "max_chars": max(len(t) for t in texts.values()),
        "truncated_in_prior_runs_at_3000": sum(1 for t in texts.values() if len(t) > 3000),
        "dev_set_n": len(dev),
        "holdout1_n": len(h1),
        "tuning_free_subset_n": len([s for s in ids if s not in dev | h1]),
        "gates": GATES,
        "questions": QUESTIONS,
    }
    (A3 / "prereg.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: out[k] for k in out if k not in {"questions", "gates"}}, indent=2))


def cmd_silver() -> None:
    texts = skills_text()
    labels = {
        sid: {d: dict(zip(("label", "quote"), v2.label(d, texts[sid]))) for d in DIMS} for sid in sorted(texts)
    }
    (A3 / "labels-silver-v4.json").write_text(json.dumps(labels, ensure_ascii=False, indent=1), encoding="utf-8")
    for d in DIMS:
        vals = [labels[s][d]["label"] for s in labels]
        print(d, "pos", vals.count(1), "neg", vals.count(0), "null", vals.count(None))


def cmd_shards() -> None:
    texts = skills_text()
    ids = sorted(texts)
    random.Random(SHARD_SEED).shuffle(ids)  # avoid category-blocked shards
    d = A3 / "annot"
    d.mkdir(parents=True, exist_ok=True)
    size = -(-len(ids) // N_SHARDS)
    for k in range(N_SHARDS):
        chunk = ids[k * size : (k + 1) * size]
        # Blind input: id + full text only. No rule labels, no JEV output, no registry fields.
        # Markdown (not one-line JSON) so annotators can page through it with a line-based reader.
        body = "\n".join(f"\n===== SKILL_ID: {s} =====\n{texts[s]}\n===== END SKILL_ID: {s} =====\n" for s in chunk)
        (d / f"shard-{k}.md").write_text(body, encoding="utf-8", newline="\n")
        (d / f"shard-{k}.ids.json").write_text(json.dumps(chunk), encoding="utf-8")
    print("shards:", N_SHARDS, "size~", size, "total", len(ids))


def cmd_jev() -> None:
    from brain.jev import JevClient, noul_probabilities

    texts = skills_text()
    path = A3 / "judgments-v4.json"
    done = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    client = JevClient()
    t0 = time.time()
    for n, sid in enumerate(sorted(texts), 1):
        if sid in done:
            continue
        qs = {f"{sid}__{d}": q for d, q in QUESTIONS.items()}
        probs = noul_probabilities(client.systemone({"skill_id": sid, "text": texts[sid]}, qs), list(qs))
        done[sid] = {d: probs[f"{sid}__{d}"] for d in DIMS}
        if n % 10 == 0:
            path.write_text(json.dumps(done, indent=1), encoding="utf-8")
            print(f"{n}/{len(texts)} elapsed={time.time() - t0:.0f}s", flush=True)
    path.write_text(json.dumps(done, indent=1), encoding="utf-8")
    print("jev done:", len(done), "skills; model=jev-latest; request sha of last:", client.last_request_sha256[:12])


if __name__ == "__main__":
    {"prereg": cmd_prereg, "silver": cmd_silver, "shards": cmd_shards, "jev": cmd_jev}[sys.argv[1]]()
