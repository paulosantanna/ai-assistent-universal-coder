PYTHON_RULES={
 "language":["Python >=3.11","typing","Pydantic at boundaries"],
 "quality":["ruff","mypy","pytest","small pure functions"],
 "security":["no eval/exec","no shell=True","safe YAML","secret manager"],
 "dependencies":["locks","SBOM","OSV/NVD/KEV/EPSS/vendor advisories"],
 "operations":["structured logs","timeouts","bounded retries","idempotency"],
}
def python_quality_gate(capabilities: list[str]) -> dict:
    required={"typing","pytest","ruff","mypy","locked_dependencies","timeouts"}
    missing=sorted(required-set(capabilities))
    return {"passed":not missing,"missing":missing}
