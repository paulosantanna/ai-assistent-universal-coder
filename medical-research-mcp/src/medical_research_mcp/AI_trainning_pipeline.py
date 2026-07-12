STAGES=[
 {"id":"source_acquisition","inputs":["source_policy"],"outputs":["raw_evidence"],"gates":["license","provenance"]},
 {"id":"curation","inputs":["raw_evidence"],"outputs":["curated_dataset"],"gates":["deduplication","quality"]},
 {"id":"split","inputs":["curated_dataset"],"outputs":["train","validation","test"],"gates":["entity_leakage","temporal_leakage"]},
 {"id":"retrieval_index","inputs":["curated_dataset"],"outputs":["bm25_index","vector_index"],"gates":["recall","provenance"]},
 {"id":"fine_tuning","inputs":["train","base_model"],"outputs":["adapter"],"gates":["reproducibility","holdout_protection"]},
 {"id":"evaluation","inputs":["adapter","test"],"outputs":["evaluation_report"],"gates":["subgroups","calibration","safety"]},
 {"id":"simulation","inputs":["validated_model","mechanistic_assumptions"],"outputs":["hypotheses"],"gates":["sensitivity","falsifiability"]},
 {"id":"promotion","inputs":["evaluation_report","judge_report"],"outputs":["versioned_candidate"],"gates":["human_approval","rollback"]},
]
def pipeline_blueprint() -> list[dict]: return STAGES
def audit_pipeline_artifacts(artifacts: list[str]) -> dict:
    present=set(artifacts); findings=[]
    for s in STAGES:
        mi=sorted(set(s["inputs"])-present); mo=sorted(set(s["outputs"])-present)
        if mi or mo: findings.append({"stage":s["id"],"missing_inputs":mi,"missing_outputs":mo,"gates":s["gates"]})
    return {"complete":not findings,"findings":findings}
