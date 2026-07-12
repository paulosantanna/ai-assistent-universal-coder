from __future__ import annotations
from collections import Counter
from pathlib import Path

CODE_SUFFIXES={".py",".java",".kt",".scala",".go",".rs",".cs",".cpp",".c",".js",".ts",".sql",".sh",".ps1"}
MANIFESTS={"pyproject.toml","requirements.txt","poetry.lock","uv.lock","pom.xml","build.gradle","build.gradle.kts","package.json","package-lock.json","Cargo.toml","go.mod","Dockerfile"}
TERMS={"train","trainer","training","finetun","lora","qlora","dora","rag","retrieval","embedding","bm25","rerank","simulation","evaluation"}

def _ignored(path: Path) -> bool:
    return any(x in path.parts for x in {".git",".venv","venv","node_modules","__pycache__",".pytest_cache"})

def scan_repository(repository: str) -> dict:
    root=Path(repository).resolve()
    if not root.is_dir(): raise FileNotFoundError(root)
    files=[p for p in root.rglob("*") if p.is_file() and not _ignored(p)]
    return {
        "root":str(root),
        "file_count":len(files),
        "code_files":[str(p.relative_to(root)) for p in files if p.suffix.lower() in CODE_SUFFIXES],
        "languages_by_suffix":dict(Counter(p.suffix.lower() for p in files if p.suffix)),
        "manifests":[str(p.relative_to(root)) for p in files if p.name in MANIFESTS],
        "tests":[str(p.relative_to(root)) for p in files if "test" in p.name.lower() or "tests" in p.parts],
        "documentation":[str(p.relative_to(root)) for p in files if p.suffix.lower()==".md"],
        "pipeline_candidates":[str(p.relative_to(root)) for p in files if any(t in p.name.lower() for t in TERMS)],
        "top_level":sorted(p.name for p in root.iterdir()),
    }

def architecture_inventory(repository: str) -> dict:
    root=Path(repository).resolve()
    scan=scan_repository(repository)
    markers={
      "api":["api","controller","route","fastapi","spring"],
      "ingestion":["ingest","scrap","crawler","source","pubmed"],
      "knowledge":["knowledge","rag","vector","embedding","bm25"],
      "training":["train","lora","qlora","trainer","finetun"],
      "simulation":["simulation","simulator","causal","molecular"],
      "evaluation":["eval","metric","benchmark","judge"],
      "governance":["governance","audit","risk","policy"],
      "observability":["otel","prometheus","grafana","logging","trace"],
    }
    areas={k:[] for k in markers}
    for p in root.rglob("*"):
        if not p.is_file() or _ignored(p): continue
        rel=str(p.relative_to(root)).lower()
        for k,terms in markers.items():
            if any(t in rel for t in terms): areas[k].append(str(p.relative_to(root)))
    return {"scan":scan,"areas":areas}
