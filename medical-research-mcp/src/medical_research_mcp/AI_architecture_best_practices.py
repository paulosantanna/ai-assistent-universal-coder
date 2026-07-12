BEST_PRACTICES={
 "boundaries":["Separate ingestion, knowledge, training, evaluation, simulation and serving."],
 "reproducibility":["Version data, code, configs, prompts and artifacts."],
 "resilience":["Idempotent ingestion, checkpoints, bounded retries and rollback."],
 "observability":["Trace source-to-answer provenance without leaking medical data."],
 "evolution":["Modular-monolith-first; evidence-backed extraction only."]
}
def evaluate_architecture_practices(capabilities: list[str]) -> dict:
    required={"versioned_data","artifact_hashing","dependency_lock","tests","provenance","observability","rollback","adr"}
    missing=sorted(required-set(capabilities))
    return {"passed":not missing,"missing":missing,"required":sorted(required)}
