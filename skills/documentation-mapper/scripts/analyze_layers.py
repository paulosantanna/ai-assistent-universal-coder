#!/usr/bin/env python3
"""Analyze all 10 architectural layers of a project repository.

Usage:
    python analyze_layers.py <repo_path> <output_dir>
"""

import json
import os
import sys
import yaml
from datetime import datetime
from pathlib import Path


def main():
    repo_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("./output")

    if not repo_path.exists():
        print(f"ERROR: Repository path '{repo_path}' does not exist.")
        sys.exit(1)

    print(f"Analyzing repository: {repo_path.resolve()}")

    analysis = {
        "metadata": {
            "analyzed_at": datetime.utcnow().isoformat(),
            "repository": str(repo_path.resolve()),
            "analysis_version": "1.0.0"
        },
        "layers": {}
    }

    # Layer 1: Infrastructure
    analysis["layers"]["infrastructure"] = analyze_infrastructure(repo_path)

    # Layer 2: Data & Persistence
    analysis["layers"]["data_persistence"] = analyze_data_persistence(repo_path)

    # Layer 3: Backend & API
    analysis["layers"]["backend_api"] = analyze_backend_api(repo_path)

    # Layer 4: Frontend & Presentation
    analysis["layers"]["frontend"] = analyze_frontend(repo_path)

    # Layer 5: Business Logic & Domain
    analysis["layers"]["business_logic"] = analyze_business_logic(repo_path)

    # Layer 6: Integrations
    analysis["layers"]["integrations"] = analyze_integrations(repo_path)

    # Layer 7: Security
    analysis["layers"]["security"] = analyze_security(repo_path)

    # Layer 8: DevOps
    analysis["layers"]["devops"] = analyze_devops(repo_path)

    # Layer 9: Observability
    analysis["layers"]["observability"] = analyze_observability(repo_path)

    # Layer 10: Governance & Documentation
    analysis["layers"]["governance"] = analyze_governance(repo_path)

    # Save analysis
    data_dir = output_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    analysis_file = data_dir / "analise_camadas.yaml"

    with open(analysis_file, "w", encoding="utf-8") as f:
        yaml.dump(analysis, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    print(f"Analysis saved to: {analysis_file}")
    return analysis


def find_files(repo: Path, patterns: list[str]) -> list[Path]:
    """Find files matching glob patterns, up to reasonable depth."""
    files = []
    for pattern in patterns:
        matched = list(repo.rglob(pattern))
        # Limit depth to avoid scanning node_modules, .git, etc.
        matched = [m for m in matched
                   if not any(part.startswith('.') or part == 'node_modules'
                              or part == '__pycache__' or part == 'venv'
                              for part in m.relative_to(repo).parts)]
        files.extend(matched)
    return files


def analyze_infrastructure(repo: Path) -> dict:
    evidence = []
    findings = {}

    # Docker
    docker_files = find_files(repo, ["Dockerfile", "docker-compose*", "*.yml", "*.yaml"])
    docker_compose = [f for f in docker_files if "docker-compose" in f.name]
    docker_files_list = [f for f in docker_files if f.name == "Dockerfile"]

    if docker_files_list:
        findings["docker"] = {
            "status": "FOUND",
            "files": [str(f.relative_to(repo)) for f in docker_files_list[:5]],
            "count": len(docker_files_list)
        }
        for f in docker_files_list[:3]:
            evidence.append({"file": str(f.relative_to(repo)), "content_preview": read_preview(f)})
    else:
        findings["docker"] = {"status": "NOT_FOUND", "files": []}

    if docker_compose:
        findings["docker_compose"] = {
            "status": "FOUND",
            "files": [str(f.relative_to(repo)) for f in docker_compose[:3]]
        }
        for f in docker_compose[:2]:
            evidence.append({"file": str(f.relative_to(repo)), "content_preview": read_preview(f)})
    else:
        findings["docker_compose"] = {"status": "NOT_FOUND"}

    # Kubernetes
    k8s_files = find_files(repo, ["*.k8s.yaml", "k8s/**/*", "kubernetes/**/*", "*.deployment.yaml", "*.service.yaml"])
    if k8s_files:
        findings["kubernetes"] = {
            "status": "FOUND",
            "files": [str(f.relative_to(repo)) for f in k8s_files[:5]],
            "count": len(k8s_files)
        }
        evidence.append({"file": str(k8s_files[0].relative_to(repo)), "content_preview": read_preview(k8s_files[0])})
    else:
        findings["kubernetes"] = {"status": "NOT_FOUND"}

    # Terraform / Cloud
    tf_files = find_files(repo, ["*.tf", "*.tfvars", "*.tfstate*", "provider.tf"])
    if tf_files:
        findings["terraform"] = {
            "status": "FOUND",
            "files": [str(f.relative_to(repo)) for f in tf_files[:5]],
            "count": len(tf_files)
        }
        evidence.append({"file": str(tf_files[0].relative_to(repo)), "content_preview": read_preview(tf_files[0])})
    else:
        findings["terraform"] = {"status": "NOT_FOUND"}

    # Environment configs
    env_files = find_files(repo, [".env*", ".env.example", "*.env.sample"])
    if env_files:
        findings["environment"] = {
            "status": "FOUND",
            "files": [str(f.relative_to(repo)) for f in env_files[:5]]
        }
        evidence.append({"file": str(env_files[0].relative_to(repo)), "content_preview": "[REDACTED - contains secrets]"})
    else:
        findings["environment"] = {"status": "NOT_FOUND"}

    # Nginx / reverse proxy
    nginx_files = find_files(repo, ["nginx*", "nginx/**/*", "*.nginx.conf", "Caddyfile", "haproxy*"])
    if nginx_files:
        findings["reverse_proxy"] = {
            "status": "FOUND",
            "files": [str(f.relative_to(repo)) for f in nginx_files[:3]]
        }
    else:
        findings["reverse_proxy"] = {"status": "NOT_FOUND"}

    return {
        "summary": f"Infrastructure analysis complete. {sum(1 for v in findings.values() if v['status'] == 'FOUND')} categories found.",
        "findings": findings,
        "evidence_count": len(evidence),
        "evidence": evidence[:10]
    }


def analyze_data_persistence(repo: Path) -> dict:
    evidence = []
    findings = {}

    # MongoDB models/schemas
    mongo_files = find_files(repo, ["**/*.mongoose*", "**/*mongo*", "**/*schema*", "**/*model*"])
    mongo_schemas = [f for f in mongo_files if any(kw in f.name.lower() for kw in ["mongo", "mongoose", "schema"])]

    if mongo_schemas:
        findings["mongodb"] = {
            "status": "FOUND",
            "files": [str(f.relative_to(repo)) for f in mongo_schemas[:10]],
            "count": len(mongo_schemas)
        }
        for f in mongo_schemas[:3]:
            evidence.append({"file": str(f.relative_to(repo)), "content_preview": read_preview(f)})
    else:
        findings["mongodb"] = {"status": "NOT_FOUND"}

    # ChromaDB
    chroma_files = find_files(repo, ["**/*chroma*", "**/*vector*", "**/*embedding*", "**/*qdrant*", "**/*pinecone*"])
    if chroma_files:
        findings["chromadb"] = {
            "status": "FOUND",
            "files": [str(f.relative_to(repo)) for f in chroma_files[:5]],
            "count": len(chroma_files)
        }
        evidence.append({"file": str(chroma_files[0].relative_to(repo)), "content_preview": read_preview(chroma_files[0])})
    else:
        findings["chromadb"] = {"status": "NOT_FOUND"}

    # SQL
    sql_files = find_files(repo, ["**/*.sql", "**/*prisma*", "**/*migration*", "**/schema.prisma",
                                   "**/*.typeorm*", "**/*.sequelize*", "**/alembic*", "**/*.db", "**/*.sqlite"])
    if sql_files:
        findings["sql"] = {
            "status": "FOUND",
            "files": [str(f.relative_to(repo)) for f in sql_files[:10]],
            "count": len(sql_files)
        }
        for f in sql_files[:3]:
            evidence.append({"file": str(f.relative_to(repo)), "content_preview": read_preview(f)})
    else:
        findings["sql"] = {"status": "NOT_FOUND"}

    # Redis / Cache
    redis_files = find_files(repo, ["**/*redis*", "**/*cache*"])
    if redis_files:
        findings["redis"] = {
            "status": "FOUND",
            "files": [str(f.relative_to(repo)) for f in redis_files[:3]]
        }
    else:
        findings["redis"] = {"status": "NOT_FOUND"}

    return {
        "summary": f"Data persistence analysis complete. {sum(1 for v in findings.values() if v['status'] == 'FOUND')} database types found.",
        "findings": findings,
        "evidence": evidence[:10]
    }


def analyze_backend_api(repo: Path) -> dict:
    evidence = []
    findings = {}

    # Language detection
    extensions = set()
    for ext in ["*.ts", "*.js", "*.py", "*.java", "*.go", "*.rs", "*.rb", "*.php", "*.cs"]:
        if list(repo.rglob(ext)):
            extensions.add(ext.replace("*.", ""))
    findings["languages"] = list(extensions) if extensions else ["NOT_DETECTED"]

    # Route/controller files
    route_patterns = find_files(repo, [
        "**/*route*", "**/*controller*", "**/*handler*", "**/*endpoint*",
        "**/*resolver*", "**/*graphql*", "**/api/**", "**/routes/**", "**/controllers/**"
    ])
    if route_patterns:
        findings["routes_controllers"] = {
            "status": "FOUND",
            "files": [str(f.relative_to(repo)) for f in route_patterns[:15]],
            "count": len(route_patterns)
        }
        for f in route_patterns[:5]:
            evidence.append({"file": str(f.relative_to(repo)), "content_preview": read_preview(f)})
    else:
        findings["routes_controllers"] = {"status": "NOT_FOUND"}

    # Framework detection
    pkg_files = find_files(repo, ["package.json", "requirements.txt", "go.mod", "Cargo.toml", "Gemfile", "composer.json", "pom.xml", "*.csproj"])
    findings["package_files"] = [str(f.relative_to(repo)) for f in pkg_files[:5]]

    # Middleware
    middleware_files = find_files(repo, ["**/*middleware*", "**/*middleware*"])
    if middleware_files:
        findings["middleware"] = {
            "status": "FOUND",
            "files": [str(f.relative_to(repo)) for f in middleware_files[:5]]
        }
    else:
        findings["middleware"] = {"status": "NOT_FOUND"}

    return {
        "summary": f"Backend analysis complete. Languages: {', '.join(findings['languages'])}. {findings.get('routes_controllers', {}).get('count', 0)} route/controller files.",
        "findings": findings,
        "evidence": evidence[:10]
    }


def analyze_frontend(repo: Path) -> dict:
    evidence = []
    findings = {}

    # Framework detection
    pkg = find_files(repo, ["package.json"])
    frontend_frameworks = []
    if pkg:
        try:
            with open(pkg[0], "r", encoding="utf-8") as f:
                data = json.load(f)
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            for framework in ["react", "vue", "angular", "svelte", "next", "nuxt", "gatsby", "remix", "solid"]:
                if framework in deps or any(k.startswith(f"@{framework}") for k in deps):
                    frontend_frameworks.append(framework)
        except Exception:
            pass
    findings["frameworks"] = frontend_frameworks if frontend_frameworks else ["NOT_DETECTED"]

    # Page/component files
    component_extensions = ["*.tsx", "*.jsx", "*.vue", "*.svelte", "*.astro", "*.page.tsx", "*.page.jsx"]
    component_files = find_files(repo, component_extensions)
    if component_files:
        findings["components"] = {
            "status": "FOUND",
            "files": [str(f.relative_to(repo)) for f in component_files[:15]],
            "count": len(component_files)
        }
        evidence.append({"file": str(component_files[0].relative_to(repo)), "content_preview": read_preview(component_files[0])})
    else:
        findings["components"] = {"status": "NOT_FOUND"}

    # State management
    state_files = find_files(repo, ["**/*store*", "**/*redux*", "**/*context*",
                                      "**/*zustand*", "**/*recoil*", "**/*pinia*", "**/*vuex*"])
    if state_files:
        findings["state_management"] = {
            "status": "FOUND",
            "files": [str(f.relative_to(repo)) for f in state_files[:5]]
        }
    else:
        findings["state_management"] = {"status": "NOT_FOUND"}

    # Styling
    css_files = find_files(repo, ["**/*.css", "**/*.scss", "**/*.less", "**/*.styled*", "**/tailwind*", "**/*.module.css"])
    if css_files:
        findings["styling"] = {
            "status": "FOUND",
            "files": [str(f.relative_to(repo)) for f in css_files[:5]],
            "count": len(css_files)
        }

    return {
        "summary": f"Frontend analysis complete. Frameworks: {', '.join(findings['frameworks'])}. {findings.get('components', {}).get('count', 0)} components.",
        "findings": findings,
        "evidence": evidence[:10]
    }


def analyze_business_logic(repo: Path) -> dict:
    evidence = []
    findings = {}

    service_files = find_files(repo, [
        "**/*service*", "**/*domain*", "**/*usecase*", "**/*use-case*",
        "**/*business*", "**/*workflow*", "**/*feature*"
    ])

    if service_files:
        findings["services"] = {
            "status": "FOUND",
            "files": [str(f.relative_to(repo)) for f in service_files[:15]],
            "count": len(service_files)
        }
        for f in service_files[:3]:
            evidence.append({"file": str(f.relative_to(repo)), "content_preview": read_preview(f)})
    else:
        findings["services"] = {"status": "NOT_FOUND"}

    # Test files for business logic
    test_files = find_files(repo, ["**/*test*", "**/*spec*", "**/__tests__/**", "**/tests/**"])
    if test_files:
        findings["tests"] = {
            "status": "FOUND",
            "count": len(test_files),
            "files": [str(f.relative_to(repo)) for f in test_files[:10]]
        }

    return {
        "summary": f"Business logic analysis complete. {findings.get('services', {}).get('count', 0)} service files. {findings.get('tests', {}).get('count', 0)} test files.",
        "findings": findings,
        "evidence": evidence[:10]
    }


def analyze_integrations(repo: Path) -> dict:
    evidence = []
    findings = {}

    integration_keywords = ["*webhook*", "*integrat*", "*external*", "*third*party*",
                             "*payment*", "*gateway*", "*stripe*", "*paypal*", "*email*",
                             "*sendgrid*", "*slack*", "*discord*", "*telegram*", "*whatsapp*",
                             "*mcp*", "*queue*", "*rabbit*", "*kafka*", "*redis*", "*pubsub*",
                             "*s3*", "*storage*", "*cdn*"]

    integration_files = find_files(repo, integration_keywords)
    if integration_files:
        findings["integrations"] = {
            "status": "FOUND",
            "files": [str(f.relative_to(repo)) for f in integration_files[:15]],
            "count": len(integration_files)
        }
        evidence.append({"file": str(integration_files[0].relative_to(repo)), "content_preview": read_preview(integration_files[0])})
    else:
        findings["integrations"] = {"status": "NOT_FOUND"}

    return {
        "summary": f"Integration analysis complete. {findings.get('integrations', {}).get('count', 0)} integration files.",
        "findings": findings,
        "evidence": evidence[:10]
    }


def analyze_security(repo: Path) -> dict:
    evidence = []
    findings = {}

    # Auth files
    auth_files = find_files(repo, [
        "**/*auth*", "**/*login*", "**/*jwt*", "**/*oauth*",
        "**/*sso*", "**/*password*", "**/*permission*", "**/*rbac*",
        "**/*guard*", "**/*session*"
    ])
    if auth_files:
        findings["authentication"] = {
            "status": "FOUND",
            "files": [str(f.relative_to(repo)) for f in auth_files[:10]],
            "count": len(auth_files)
        }
        evidence.append({"file": str(auth_files[0].relative_to(repo)), "content_preview": read_preview(auth_files[0])})
    else:
        findings["authentication"] = {"status": "NOT_FOUND"}

    # Encryption / secrets
    encrypt_files = find_files(repo, ["**/*encrypt*", "**/*crypto*", "**/*hash*", "**/*secret*", "**/*vault*"])
    if encrypt_files:
        findings["encryption"] = {
            "status": "FOUND",
            "files": [str(f.relative_to(repo)) for f in encrypt_files[:5]]
        }
    else:
        findings["encryption"] = {"status": "NOT_FOUND"}

    # CSP / CORS / security headers
    security_config = find_files(repo, ["**/*csp*", "**/*cors*", "**/*helmet*", "**/*security*"])
    if security_config:
        findings["security_headers"] = {
            "status": "FOUND",
            "files": [str(f.relative_to(repo)) for f in security_config[:5]]
        }

    return {
        "summary": f"Security analysis complete. {findings.get('authentication', {}).get('count', 0)} auth files.",
        "findings": findings,
        "evidence": evidence[:10]
    }


def analyze_devops(repo: Path) -> dict:
    evidence = []
    findings = {}

    ci_files = find_files(repo, [".github/**/*", ".gitlab-ci*", "Jenkinsfile*",
                                  ".circleci/**/*", "azure-pipelines*", ".drone*",
                                  "bitbucket-pipelines*", "Makefile", "docker-compose*"])
    if ci_files:
        findings["ci_cd"] = {
            "status": "FOUND",
            "files": [str(f.relative_to(repo)) for f in ci_files[:10]],
            "count": len(ci_files)
        }
        for f in ci_files[:2]:
            evidence.append({"file": str(f.relative_to(repo)), "content_preview": read_preview(f)})
    else:
        findings["ci_cd"] = {"status": "NOT_FOUND"}

    # Scripts
    script_files = find_files(repo, ["scripts/**/*", "bin/**/*", "*.sh", "*.bat", "*.ps1"])
    if script_files:
        findings["scripts"] = {
            "status": "FOUND",
            "files": [str(f.relative_to(repo)) for f in script_files[:10]],
            "count": len(script_files)
        }

    return {
        "summary": f"DevOps analysis complete. {findings.get('ci_cd', {}).get('count', 0)} CI/CD files.",
        "findings": findings,
        "evidence": evidence[:10]
    }


def analyze_observability(repo: Path) -> dict:
    evidence = []
    findings = {}

    obs_files = find_files(repo, [
        "**/*log*", "**/*monitor*", "**/*metric*", "**/*alert*",
        "**/*grafana*", "**/*prometheus*", "**/*datadog*",
        "**/*newrelic*", "**/*sentry*", "**/*opentelemetry*",
        "**/*health*", "**/*readyz*", "**/*livez*", "**/*trace*", "**/*span*"
    ])
    if obs_files:
        findings["observability"] = {
            "status": "FOUND",
            "files": [str(f.relative_to(repo)) for f in obs_files[:10]],
            "count": len(obs_files)
        }
    else:
        findings["observability"] = {"status": "NOT_FOUND"}

    return {
        "summary": f"Observability analysis complete. {findings.get('observability', {}).get('count', 0)} observability files.",
        "findings": findings,
        "evidence": evidence[:10]
    }


def analyze_governance(repo: Path) -> dict:
    evidence = []
    findings = {}

    doc_files = find_files(repo, [
        "README*", "CONTRIBUTING*", "LICENSE*", "CODE_OF_CONDUCT*",
        "CHANGELOG*", "docs/**/*", "*.md", "ADRs/**/*", "adr/**/*",
        "wiki/**/*"
    ])
    if doc_files:
        findings["documentation"] = {
            "status": "FOUND",
            "files": [str(f.relative_to(repo)) for f in doc_files[:15]],
            "count": len(doc_files)
        }
        for f in doc_files[:3]:
            evidence.append({"file": str(f.relative_to(repo)), "content_preview": read_preview(f)})
    else:
        findings["documentation"] = {"status": "NOT_FOUND"}

    return {
        "summary": f"Governance analysis complete. {findings.get('documentation', {}).get('count', 0)} documentation files.",
        "findings": findings,
        "evidence": evidence[:10]
    }


def read_preview(filepath: Path, max_chars: int = 500) -> str:
    """Read a preview of a file."""
    try:
        raw = filepath.read_bytes()
        # Detect binary content: if null bytes or non-UTF-8 decode issues at high ratio
        if b'\x00' in raw:
            return "[ERROR: Binary file - cannot preview]"
        content = raw.decode("utf-8", errors="replace")
        if len(content) > max_chars:
            return content[:max_chars] + "...[TRUNCATED]"
        return content
    except Exception:
        return "[ERROR: Could not read file]"


if __name__ == "__main__":
    main()
