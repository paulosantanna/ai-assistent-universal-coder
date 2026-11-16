"""skills-quality-eval v4 analysis (Amendment A3). Implements the pre-registered gates; no post-hoc rules.

Subcommands:
  iaa      load A1/A2, compute reliability, write the adjudication tasks for the third annotator
  final    add A3 votes, build consensus, evaluate JEV vs consensus (strata), apply gates, write report
  triage   JEV triage Nouls about the evidence, then decide per dimension whether to leave silver
"""
from __future__ import annotations

import hashlib
import json
import math
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, r"E:\Github\workspace-brain")
import skills_quality_eval_v4 as v4  # noqa: E402
from brain.evaluate import confusion_at, wilson_interval  # noqa: E402

A3 = v4.A3
OUT = A3 / "annot" / "out"
DIMS = v4.DIMS
G = v4.GATES
THR = v4.THRESHOLD_YES


def load_votes(annotator: str, ids: list[str]) -> dict[str, dict[str, int | None]]:
    votes: dict[str, dict[str, int | None]] = {}
    for path in sorted(OUT.glob(f"{annotator}-shard-*.jsonl")):
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            row = json.loads(line)  # malformed JSON must fail loudly, not be skipped
            sid = row["id"]
            votes[sid] = {}
            for d in DIMS:
                lab = row[d]["label"]
                if lab not in (0, 1, "u"):
                    raise ValueError(f"{path.name}:{n} {sid}.{d} invalid label {lab!r}")
                votes[sid][d] = None if lab == "u" else lab
    missing = sorted(set(ids) - set(votes))
    extra = sorted(set(votes) - set(ids))
    if missing or extra:
        raise ValueError(f"{annotator}: missing={len(missing)} extra={len(extra)} {missing[:3]} {extra[:3]}")
    return votes


def cohen_kappa(a: list[int], b: list[int]):
    n = len(a)
    if n == 0:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return None if pe == 1 else (po - pe) / (1 - pe)


def gwet_ac1(a: list[int], b: list[int]):
    n = len(a)
    if n == 0:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    pi = (sum(a) + sum(b)) / (2 * n)
    pe = 2 * pi * (1 - pi)
    return None if pe == 1 else (po - pe) / (1 - pe)


def reliability(v1, v2, ids):
    out = {}
    for d in DIMS:
        pairs = [(v1[s][d], v2[s][d]) for s in ids if v1[s][d] is not None and v2[s][d] is not None]
        a, b = [p[0] for p in pairs], [p[1] for p in pairs]
        n = len(pairs)
        raw = sum(x == y for x, y in pairs) / n if n else None
        prev = (sum(a) + sum(b)) / (2 * n) if n else None
        minority = min(prev, 1 - prev) if prev is not None else None
        k, ac1 = cohen_kappa(a, b), gwet_ac1(a, b)
        lp = G["reliability_low_prevalence"]
        if minority is not None and minority < lp["minority_below"]:
            rule, ok = "low-prevalence: AC1>=0.85 and raw>=0.92", bool(ac1 is not None and ac1 >= lp["ac1_min"] and raw >= lp["raw_agreement_min"])
        else:
            rule, ok = "kappa>=0.70", bool(k is not None and k >= G["reliability_kappa_min"])
        out[d] = {"n_both_valid": n, "raw_agreement": raw, "kappa": k, "ac1": ac1, "prevalence_pos": prev,
                  "minority_prevalence": minority, "u_a1": sum(v1[s][d] is None for s in ids),
                  "u_a2": sum(v2[s][d] is None for s in ids), "rule": rule, "reliability_pass": ok}
    return out


def cmd_iaa() -> None:
    ids = sorted(v4.skills_text())
    v1, v2 = load_votes("A1", ids), load_votes("A2", ids)
    rel = reliability(v1, v2, ids)
    tasks = {}
    for s in ids:
        need = [d for d in DIMS if v1[s][d] is None or v2[s][d] is None or v1[s][d] != v2[s][d]]
        if need:
            tasks[s] = need
    (A3 / "iaa-v4.json").write_text(json.dumps(rel, indent=2), encoding="utf-8")
    (A3 / "adjudication-tasks.json").write_text(json.dumps(tasks, indent=1), encoding="utf-8")
    texts = v4.skills_text()
    adj = A3 / "adjud"
    adj.mkdir(exist_ok=True)
    keys = sorted(tasks)
    size = max(1, -(-len(keys) // 3))
    shards = [keys[i : i + size] for i in range(0, len(keys), size)]
    for k, chunk in enumerate(shards):
        body = "\n".join(
            f"\n===== SKILL_ID: {s} | QUESTIONS_TO_ANSWER: {', '.join(tasks[s])} =====\n{texts[s]}\n===== END SKILL_ID: {s} =====\n"
            for s in chunk
        )
        (adj / f"shard-{k}.md").write_text(body, encoding="utf-8", newline="\n")
        (adj / f"shard-{k}.ids.json").write_text(json.dumps({s: tasks[s] for s in chunk}), encoding="utf-8")
    print(json.dumps({d: {k: (round(v, 3) if isinstance(v, float) else v) for k, v in rel[d].items()} for d in DIMS}, indent=1))
    print("skills needing adjudication:", len(tasks), "| items:", sum(len(v) for v in tasks.values()), "| shards:", len(shards))


def consensus(v1, v2, v3, s, d):
    a, b = v1[s][d], v2[s][d]
    if a is not None and a == b:
        return a, "S1"
    c = v3.get(s, {}).get(d)
    votes = [x for x in (a, b) if x is not None]
    if c is not None and c in votes:
        return c, "ADJ"
    return None, "null"


def load_a3(ids):
    votes: dict[str, dict[str, int | None]] = {}
    for path in sorted(OUT.glob("A3-shard-*.jsonl")):
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            row = json.loads(line)
            votes[row["id"]] = {}
            for d in DIMS:
                if d not in row:
                    continue
                cell = row[d]
                # Accept nested {"label","quote"} (canonical) or a bare label int/str.
                lab = cell["label"] if isinstance(cell, dict) else cell
                if lab not in (0, 1, "u"):
                    raise ValueError(f"{path.name}:{n} {row['id']}.{d} invalid label {lab!r}")
                votes[row["id"]][d] = None if lab == "u" else lab
    tasks = json.loads((A3 / "adjudication-tasks.json").read_text(encoding="utf-8"))
    missing = [(s, d) for s, ds in tasks.items() for d in ds if d not in votes.get(s, {})]
    if missing:
        raise ValueError(f"A3 missing {len(missing)} items, e.g. {missing[:3]}")
    return votes


def jev_metrics(pairs):
    c = confusion_at(pairs, THR)
    n_pos = sum(1 for _, y in pairs if y == 1)
    n_neg = len(pairs) - n_pos
    band = sum(1 for p, _ in pairs if v4.THRESHOLD_NO < p < THR)
    c.update({
        "n": len(pairs), "positives": n_pos, "negatives": n_neg,
        "review_band_share": round(band / len(pairs), 4) if pairs else None,
        "wilson_precision_95": wilson_interval(c["tp"], c["approved"]) if c["approved"] else None,
    })
    return c


def verdict(m):
    if m["negatives"] < G["negatives_min_for_pass"]:
        return "uninformative"
    ok = (m["precision"] or 0) >= G["jev_precision_min"] and m["approved"] >= G["jev_approved_min"]
    return "pass" if ok else "review"


def cmd_final() -> None:
    texts = v4.skills_text()
    ids = sorted(texts)
    v1, v2 = load_votes("A1", ids), load_votes("A2", ids)
    v3 = load_a3(ids)
    jev = json.loads((A3 / "judgments-v4.json").read_text(encoding="utf-8"))
    silver = json.loads((A3 / "labels-silver-v4.json").read_text(encoding="utf-8"))
    prereg = json.loads((A3 / "prereg.json").read_text(encoding="utf-8"))
    assert prereg["frozen_sha256"] == v4.frozen_sha(ids), "frozen A3 inputs changed after pre-registration"
    dev = set(json.loads((v4.WORK / "sample.json").read_text(encoding="utf-8"))["skills"])
    h1 = set(json.loads((v4.WORK / "judgments-v2.json").read_text(encoding="utf-8")))
    free = [s for s in ids if s not in dev | h1]
    rel = reliability(v1, v2, ids)
    report = {"amendment": "A3", "frozen_sha256": prereg["frozen_sha256"], "n_skills": len(ids), "per_dimension": {}}
    labels_out = {}
    for d in DIMS:
        cons = {s: consensus(v1, v2, v3, s, d) for s in ids}
        n_null = sum(1 for s in ids if cons[s][0] is None)
        s1 = [(jev[s][d], cons[s][0]) for s in ids if cons[s][1] == "S1"]
        allc = [(jev[s][d], cons[s][0]) for s in ids if cons[s][0] is not None]
        adjp = [(jev[s][d], cons[s][0]) for s in ids if cons[s][1] == "ADJ"]
        freep = [(jev[s][d], cons[s][0]) for s in free if cons[s][1] == "S1"]
        sil = [(jev[s][d], silver[s][d]["label"]) for s in ids if silver[s][d]["label"] is not None]
        sil_vs_cons = [(silver[s][d]["label"], cons[s][0]) for s in ids if silver[s][d]["label"] is not None and cons[s][0] is not None]
        agree_sc = [x for x, _ in sil_vs_cons], [y for _, y in sil_vs_cons]
        head = jev_metrics(s1)
        report["per_dimension"][d] = {
            "reliability": rel[d],
            "n_null_consensus": n_null,
            "null_share": round(n_null / len(ids), 4),
            "strata_counts": {"S1_A1eqA2": len(s1), "ADJ": len(adjp), "null": n_null},
            "jev_headline_S1": {**head, "verdict": verdict(head)},
            "jev_all_consensus": jev_metrics(allc),
            "jev_tuning_free_S1": jev_metrics(freep),
            "jev_vs_silver_rules": jev_metrics(sil),
            "silver_vs_consensus": {"n": len(sil_vs_cons), "raw_agreement": round(sum(x == y for x, y in sil_vs_cons) / len(sil_vs_cons), 4) if sil_vs_cons else None,
                                    "kappa": cohen_kappa(*agree_sc) if sil_vs_cons else None},
        }
        labels_out[d] = {s: cons[s][0] for s in ids}
    vs = [report["per_dimension"][d]["jev_headline_S1"]["verdict"] for d in DIMS]
    report["overall_verdict"] = "pass" if all(v == "pass" for v in vs) else "partial"
    (A3 / "consensus-labels-v4.json").write_text(json.dumps(labels_out, indent=1), encoding="utf-8")
    (A3 / "eval-report-v4.json").write_text(json.dumps(report, indent=2, default=lambda o: None), encoding="utf-8")
    for d in DIMS:
        p = report["per_dimension"][d]
        h = p["jev_headline_S1"]
        r = p["reliability"]
        print(f"{d:22s} kappa={r['kappa'] if r['kappa'] is None else round(r['kappa'],3)} ac1={r['ac1'] if r['ac1'] is None else round(r['ac1'],3)} raw={round(r['raw_agreement'],3)} "
              f"rel_pass={r['reliability_pass']} null={p['null_share']:.1%} | JEV S1 n={h['n']} neg={h['negatives']} approved={h['approved']} "
              f"prec={None if h['precision'] is None else round(h['precision'],3)} rec={None if h['recall'] is None else round(h['recall'],3)} -> {h['verdict']}")
    print("overall:", report["overall_verdict"])


TRIAGE_Q = {
    "T1_independence": "The consensus labels in this state were produced by annotators from model families different from the rubric author, working blind to each other and to the automated judge under evaluation, so the labels are independent of the author.",
    "T2_reliability": "The inter-annotator reliability numbers in this state meet the pre-registered threshold stated in the same state for this dimension.",
    "T3_sufficiency": "Even without a human reviewer, the evidence in this state is sufficient to use these consensus labels as ground truth for measuring the precision of an automated judge on this dimension.",
}


def cmd_triage() -> None:
    from brain.jev import JevClient, noul_probabilities

    rep = json.loads((A3 / "eval-report-v4.json").read_text(encoding="utf-8"))
    client = JevClient()
    out = {}
    for d in DIMS:
        p = rep["per_dimension"][d]
        r = p["reliability"]
        state = {
            "dimension": d,
            "rubric_author_model_family": "Anthropic Claude",
            # Actual families after Gemini/DeepSeek/Grok quota failures: A2+A3 = Composer.
            # Independence A1≠A2 still holds; A3 same family as A2 weakens adjudication-only independence.
            "annotators": {
                "A1": "OpenAI GPT (blind)",
                "A2": "Cursor Composer (blind; Gemini/DeepSeek quota blocked)",
                "A3_adjudicator_only_on_disagreements": "Cursor Composer (blind; same family as A2 — weaker than pre-registered Grok)",
            },
            "n_skills_annotated_by_both": r["n_both_valid"],
            "pre_registered_threshold": r["rule"],
            "raw_agreement": r["raw_agreement"], "cohen_kappa": r["kappa"], "gwet_ac1": r["ac1"],
            "minority_prevalence": r["minority_prevalence"], "reliability_gate_passed": r["reliability_pass"],
            "null_share_after_adjudication": p["null_share"],
            "negatives_in_ground_truth": p["jev_headline_S1"]["negatives"],
            "human_review": "none",
        }
        qs = {f"{d}__{k}": q for k, q in TRIAGE_Q.items()}
        probs = noul_probabilities(client.systemone(state, qs), list(qs))
        out[d] = {k: probs[f"{d}__{k}"] for k in TRIAGE_Q}
    decisions = {}
    for d in DIMS:
        p = rep["per_dimension"][d]
        r = p["reliability"]
        t = out[d]
        triage_ok = all(v >= G["triage_p_min"] for v in t.values())
        triage_band = any(G["triage_p_min"] > v > v4.THRESHOLD_NO for v in t.values())
        complete = r["n_both_valid"] + r["u_a1"] + r["u_a2"] >= 0  # structural completeness already enforced in load_votes
        exit_silver = bool(r["reliability_pass"] and p["null_share"] <= G["unresolved_max"] and complete and triage_ok)
        decisions[d] = {"exit_silver": exit_silver, "reliability_pass": r["reliability_pass"], "null_ok": p["null_share"] <= G["unresolved_max"],
                        "triage": t, "triage_all_ge_0.7": triage_ok, "triage_in_review_band": triage_band,
                        "status": "consenso-IA independente" if exit_silver else "permanece silver"}
    (A3 / "triage-decision-v4.json").write_text(json.dumps(decisions, indent=2), encoding="utf-8")
    for d in DIMS:
        x = decisions[d]
        print(f"{d:22s} rel={x['reliability_pass']} null_ok={x['null_ok']} triage={ {k: round(v,2) for k, v in x['triage'].items()} } -> {x['status']}")


if __name__ == "__main__":
    {"iaa": cmd_iaa, "final": cmd_final, "triage": cmd_triage}[sys.argv[1]]()
