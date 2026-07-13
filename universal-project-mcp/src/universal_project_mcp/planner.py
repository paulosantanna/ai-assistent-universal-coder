from __future__ import annotations

import re
from typing import Any


PRODUCTION_ARTIFACTS = [
    "README.md",
    "docs/ARCHITECTURE.md",
    "docs/ADR/",
    "docs/RUNBOOK.md",
    "docs/SECURITY.md",
    "docs/OBSERVABILITY.md",
    "docs/DEPLOYMENT.md",
    "docs/ROLLBACK.md",
    "docker-compose.yml or platform equivalent",
    "Dockerfile or buildpack config",
    ".github/workflows/ci.yml or CI equivalent",
    "test strategy and quality gates",
    "environment variable contract",
    "database migration plan",
]


def normalize_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    return [str(value)]


def project_plan(
    objective: str,
    architecture: str = "unspecified",
    languages: list[str] | None = None,
    databases: list[str] | None = None,
    deployment_target: str = "cloud",
) -> dict[str, Any]:
    languages = normalize_list(languages)
    databases = normalize_list(databases)
    blockers = []
    if not objective.strip():
        blockers.append("objective is required")
    if architecture == "unspecified":
        blockers.append("architecture must be confirmed or selected by chromatic-decision")
    if not languages:
        blockers.append("at least one language/runtime must be selected or discovered")
    if not databases:
        blockers.append("database choice must be selected, discovered or explicitly not required")

    return {
        "status": "BLOCKED" if blockers else "PASS",
        "objective": objective,
        "architecture": architecture,
        "languages": languages,
        "databases": databases,
        "deployment_target": deployment_target,
        "phases": [
            "requirements_contract",
            "architecture_decision",
            "stack_and_database_selection",
            "scaffold_generation",
            "domain_model_and_api_contract",
            "implementation",
            "tests_and_quality_gates",
            "security_and_supply_chain",
            "observability_and_operations",
            "packaging_and_deployment",
            "production_readiness_judge",
        ],
        "required_playbooks": [
            "chromatic-decision",
            "zero-to-production-project",
            "documentation-generation",
            "security-secrets-audit",
            "test-recovery",
            "package-full-review",
        ],
        "required_artifacts": PRODUCTION_ARTIFACTS,
        "blocking_conditions": blockers,
    }


def stack_matrix(languages: list[str] | None = None, databases: list[str] | None = None) -> dict[str, Any]:
    languages = normalize_list(languages)
    databases = normalize_list(databases)
    rows = []
    for language in languages or ["runtime-to-be-selected"]:
        rows.append(
            {
                "language": language,
                "required_decisions": [
                    "runtime version",
                    "package manager",
                    "test framework",
                    "linter/formatter",
                    "build artifact",
                    "LSP/profile validation",
                ],
            }
        )
    return {
        "status": "PASS",
        "languages": rows,
        "databases": [
            {
                "database": database,
                "required_decisions": [
                    "driver/ORM",
                    "migration tool",
                    "connection pooling",
                    "backup/restore",
                    "local dev service",
                    "production secret boundary",
                ],
            }
            for database in (databases or ["database-to-be-selected"])
        ],
    }


def production_checklist(architecture: str, deployment_target: str = "cloud") -> dict[str, Any]:
    return {
        "status": "PASS",
        "architecture": architecture,
        "deployment_target": deployment_target,
        "gates": [
            "requirements accepted",
            "ADR accepted",
            "scaffold generated in sandbox",
            "tests pass",
            "security scan pass or reviewed",
            "secrets externalized",
            "observability configured",
            "database migrations reversible",
            "rollback documented",
            "CI/CD pipeline generated",
            "production readiness Judge PASS",
        ],
        "stop_conditions": [
            "missing runtime version",
            "missing database migration plan",
            "missing tests",
            "missing rollback",
            "secret in repository output",
            "token budget exceeded without user-approved scope reduction",
        ],
    }


def scaffold_manifest(project_name: str, architecture: str, languages: list[str] | None = None) -> dict[str, Any]:
    languages = normalize_list(languages)
    base_dirs = ["docs", "src", "tests", "scripts", "deploy", "ops"]
    return {
        "status": "PASS" if project_name.strip() else "BLOCKED",
        "project_name": project_name,
        "architecture": architecture,
        "directories": base_dirs,
        "files": PRODUCTION_ARTIFACTS,
        "language_overlays": [
            {
                "language": language,
                "expected": ["runtime config", "dependency manifest", "test config", "linter config"],
            }
            for language in (languages or ["runtime-to-be-selected"])
        ],
        "write_policy": "sandbox_only_until_approval",
        "blocking_conditions": [] if project_name.strip() else ["project_name is required"],
    }


def scaffold_package(
    project_name: str,
    objective: str,
    architecture: str,
    languages: list[str] | None = None,
    databases: list[str] | None = None,
    deployment_target: str = "cloud",
) -> dict[str, Any]:
    languages = normalize_list(languages)
    databases = normalize_list(databases)
    manifest = scaffold_manifest(project_name, architecture, languages)
    plan = project_plan(objective, architecture, languages, databases, deployment_target)
    project_slug = safe_name(project_name)
    artifacts = base_artifacts(project_slug, objective, architecture, languages, databases, deployment_target)

    for language in languages:
        artifacts.extend(language_artifacts(language, project_slug))
    for database in databases:
        artifacts.extend(database_artifacts(database))

    return {
        "status": "BLOCKED" if manifest["blocking_conditions"] or plan["blocking_conditions"] else "PASS",
        "project_name": project_name,
        "project_slug": project_slug,
        "write_policy": "sandbox_only_until_approval",
        "manifest": manifest,
        "plan": plan,
        "artifacts": dedupe_artifacts(artifacts),
        "blocking_conditions": manifest["blocking_conditions"] + plan["blocking_conditions"],
    }


def safe_name(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip().lower()).strip("-._")
    return cleaned or "aeos-project"


def dedupe_artifacts(artifacts: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: dict[str, dict[str, str]] = {}
    for artifact in artifacts:
        seen[artifact["path"]] = artifact
    return list(seen.values())


def base_artifacts(
    project_slug: str,
    objective: str,
    architecture: str,
    languages: list[str],
    databases: list[str],
    deployment_target: str,
) -> list[dict[str, str]]:
    language_text = ", ".join(languages) if languages else "to be selected"
    database_text = ", ".join(databases) if databases else "not selected"
    return [
        {
            "path": "README.md",
            "content": "\n".join(
                [
                    f"# {project_slug}",
                    "",
                    f"Objective: {objective}",
                    "",
                    "## Stack",
                    "",
                    f"- Architecture: {architecture}",
                    f"- Languages: {language_text}",
                    f"- Databases: {database_text}",
                    f"- Deployment target: {deployment_target}",
                    "",
                    "## Governance",
                    "",
                    "- Generated sandbox-first by AEOS.",
                    "- Apply to the active repository only after review and approval.",
                    "- Keep secrets outside source control.",
                    "- Run tests, security, observability and rollback gates before production.",
                ]
            ),
        },
        {"path": "docs/ARCHITECTURE.md", "content": architecture_doc(architecture, languages, databases)},
        {"path": "docs/ADR/0001-initial-architecture.md", "content": adr_doc(architecture, languages, databases)},
        {"path": "docs/RUNBOOK.md", "content": runbook_doc(project_slug)},
        {"path": "docs/SECURITY.md", "content": security_doc()},
        {"path": "docs/OBSERVABILITY.md", "content": observability_doc()},
        {"path": "docs/DEPLOYMENT.md", "content": deployment_doc(deployment_target)},
        {"path": "docs/ROLLBACK.md", "content": rollback_doc()},
        {"path": ".env.example", "content": env_example(databases)},
        {"path": ".gitignore", "content": ".env\n.env.*\n__pycache__/\nnode_modules/\ntarget/\ndist/\nbuild/\n.aeos/sandbox/\n"},
        {"path": ".github/workflows/ci.yml", "content": ci_doc(languages)},
        {"path": "docker-compose.yml", "content": compose_doc(databases)},
        {"path": "tests/README.md", "content": "# Tests\n\nAdd unit, integration, contract and deployment smoke tests here.\n"},
        {"path": "ops/production-readiness.md", "content": production_readiness_doc()},
    ]


def language_artifacts(language: str, project_slug: str) -> list[dict[str, str]]:
    key = language.lower()
    if "python" in key:
        return [
            {"path": "pyproject.toml", "content": python_pyproject(project_slug)},
            {"path": "src/app/main.py", "content": 'def health() -> dict[str, str]:\n    return {"status": "ok"}\n'},
            {"path": "tests/test_health.py", "content": "from app.main import health\n\n\ndef test_health():\n    assert health()[\"status\"] == \"ok\"\n"},
            {"path": "Dockerfile", "content": python_dockerfile()},
        ]
    if "java" in key:
        return [
            {"path": "pom.xml", "content": java_pom(project_slug)},
            {"path": "src/main/java/app/App.java", "content": "package app;\n\npublic final class App {\n    public String health() {\n        return \"ok\";\n    }\n}\n"},
            {"path": "src/test/java/app/AppTest.java", "content": "package app;\n\nimport org.junit.jupiter.api.Test;\nimport static org.junit.jupiter.api.Assertions.assertEquals;\n\nclass AppTest {\n    @Test\n    void health() {\n        assertEquals(\"ok\", new App().health());\n    }\n}\n"},
            {"path": "Dockerfile", "content": java_dockerfile()},
        ]
    if "angular" in key:
        return [
            {"path": "package.json", "content": node_package(project_slug, angular=True, typescript=True)},
            {"path": "angular.json", "content": '{\n  "version": 1,\n  "projects": {}\n}\n'},
            {"path": "src/main.ts", "content": "console.log('AEOS Angular scaffold placeholder');\n"},
            {"path": "Dockerfile", "content": node_dockerfile()},
        ]
    if "typescript" in key or "node" in key:
        return [
            {"path": "package.json", "content": node_package(project_slug, typescript=True)},
            {"path": "tsconfig.json", "content": tsconfig()},
            {"path": "src/index.ts", "content": "export function health(): string {\n  return 'ok';\n}\n"},
            {"path": "tests/health.test.ts", "content": "import { health } from '../src/index';\n\ntest('health', () => {\n  expect(health()).toBe('ok');\n});\n"},
            {"path": "Dockerfile", "content": node_dockerfile()},
        ]
    if "javascript" in key:
        return [
            {"path": "package.json", "content": node_package(project_slug)},
            {"path": "src/index.js", "content": "export function health() {\n  return 'ok';\n}\n"},
            {"path": "tests/health.test.js", "content": "import { health } from '../src/index.js';\n\ntest('health', () => {\n  expect(health()).toBe('ok');\n});\n"},
            {"path": "Dockerfile", "content": node_dockerfile()},
        ]
    return [
        {"path": f"src/{safe_name(language)}/README.md", "content": f"# {language}\n\nAdd runtime-specific source files here.\n"},
        {"path": f"tests/{safe_name(language)}/README.md", "content": f"# {language} Tests\n\nAdd runtime-specific tests here.\n"},
    ]


def database_artifacts(database: str) -> list[dict[str, str]]:
    key = database.lower()
    name = safe_name(database)
    if "none" in key or "no database" in key:
        return [{"path": "docs/DATABASE.md", "content": "# Database\n\nNo persistent database is required by the current project contract.\n"}]
    return [
        {"path": "docs/DATABASE.md", "content": database_doc(database)},
        {"path": f"db/migrations/001_initial_{name}.sql", "content": "-- Initial migration placeholder. Replace with reviewed schema changes.\n"},
        {"path": "db/README.md", "content": "# Database\n\nKeep migrations reversible when possible and document backup/restore procedures.\n"},
    ]


def architecture_doc(architecture: str, languages: list[str], databases: list[str]) -> str:
    return "\n".join(
        [
            "# Architecture",
            "",
            f"Selected architecture: {architecture}",
            "",
            "```mermaid",
            "flowchart TD",
            "  Client[Client] --> App[Application]",
            "  App --> Domain[Domain Layer]",
            "  Domain --> Data[Data Access]",
            "  Data --> Store[(Database)]",
            "```",
            "",
            f"Languages: {', '.join(languages) if languages else 'to be selected'}",
            f"Databases: {', '.join(databases) if databases else 'to be selected'}",
            "",
            "All concrete boundaries must be confirmed with implementation evidence before production.",
        ]
    )


def adr_doc(architecture: str, languages: list[str], databases: list[str]) -> str:
    return "\n".join(
        [
            "# ADR 0001: Initial Architecture",
            "",
            "## Status",
            "",
            "Proposed",
            "",
            "## Decision",
            "",
            f"Use `{architecture}` with `{', '.join(languages)}` and `{', '.join(databases)}` as the initial project direction.",
            "",
            "## Consequences",
            "",
            "- Validate this decision with tests, security review and production readiness gates.",
            "- Update this ADR when runtime, database or deployment decisions change.",
        ]
    )


def runbook_doc(project_slug: str) -> str:
    return f"# Runbook\n\nService: `{project_slug}`\n\n## Health Check\n\nRun the project-specific test command and verify the health endpoint or health function.\n"


def security_doc() -> str:
    return "# Security\n\n- Store secrets outside source control.\n- Run dependency and secret scans in CI.\n- Document auth, authorization and data boundaries before production.\n"


def observability_doc() -> str:
    return "# Observability\n\n- Define logs, metrics and traces before production.\n- Include request IDs or correlation IDs where applicable.\n- Add alerts for availability, latency and error rate.\n"


def deployment_doc(deployment_target: str) -> str:
    return f"# Deployment\n\nTarget: `{deployment_target}`\n\nUse sandbox-generated manifests until deployment approval is granted.\n"


def rollback_doc() -> str:
    return "# Rollback\n\n- Define rollback command or redeploy strategy.\n- Verify database migration rollback or forward-fix strategy.\n- Keep release artifacts immutable.\n"


def env_example(databases: list[str]) -> str:
    lines = ["APP_ENV=local", "LOG_LEVEL=info"]
    if databases and not any("none" in db.lower() for db in databases):
        lines.append("DATABASE_URL=replace-with-local-development-url")
    return "\n".join(lines) + "\n"


def ci_doc(languages: list[str]) -> str:
    return "\n".join(
        [
            "name: ci",
            "on:",
            "  pull_request:",
            "  push:",
            "    branches: [main]",
            "jobs:",
            "  validate:",
            "    runs-on: ubuntu-latest",
            "    steps:",
            "      - uses: actions/checkout@v4",
            "      - name: Review generated stack",
            f"        run: echo \"Validate languages: {', '.join(languages) if languages else 'to-be-selected'}\"",
        ]
    ) + "\n"


def compose_doc(databases: list[str]) -> str:
    services = ["services:", "  app:", "    build: .", "    env_file: .env.example"]
    for database in databases:
        key = database.lower()
        if "postgres" in key:
            services.extend(["  postgres:", "    image: postgres:16", "    environment:", "      POSTGRES_PASSWORD: local-dev-only"])
        elif "mysql" in key or "mariadb" in key:
            services.extend(["  mysql:", "    image: mysql:8", "    environment:", "      MYSQL_ROOT_PASSWORD: local-dev-only"])
        elif "mongo" in key:
            services.extend(["  mongo:", "    image: mongo:7"])
        elif "redis" in key:
            services.extend(["  redis:", "    image: redis:7"])
    return "\n".join(services) + "\n"


def production_readiness_doc() -> str:
    return "# Production Readiness\n\n- [ ] Requirements accepted\n- [ ] Tests passing\n- [ ] Security scan reviewed\n- [ ] Observability configured\n- [ ] Rollback tested\n- [ ] Token budget respected\n"


def database_doc(database: str) -> str:
    return f"# Database\n\nSelected database: `{database}`\n\nDocument schema ownership, migrations, backup, restore, connection pooling and production secret boundaries.\n"


def python_pyproject(project_slug: str) -> str:
    return f"[project]\nname = \"{project_slug}\"\nversion = \"0.1.0\"\nrequires-python = \">=3.11\"\ndependencies = []\n\n[tool.pytest.ini_options]\npythonpath = [\"src\"]\n"


def python_dockerfile() -> str:
    return "FROM python:3.12-slim\nWORKDIR /app\nCOPY . .\nCMD [\"python\", \"-m\", \"app.main\"]\n"


def java_pom(project_slug: str) -> str:
    return f"""<project xmlns=\"http://maven.apache.org/POM/4.0.0\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd\">
  <modelVersion>4.0.0</modelVersion>
  <groupId>app</groupId>
  <artifactId>{project_slug}</artifactId>
  <version>0.1.0</version>
  <properties>
    <maven.compiler.release>21</maven.compiler.release>
  </properties>
</project>
"""


def java_dockerfile() -> str:
    return "FROM eclipse-temurin:21-jre\nWORKDIR /app\nCOPY target/*.jar app.jar\nCMD [\"java\", \"-jar\", \"app.jar\"]\n"


def node_package(project_slug: str, angular: bool = False, typescript: bool = False) -> str:
    scripts = '"test": "echo \\"Add tests\\"", "build": "echo \\"Add build\\""'
    package_type = '"type": "module",'
    deps = '"dependencies": {},'
    dev_deps = '"devDependencies": {}'
    return f'{{\n  "name": "{project_slug}",\n  {package_type}\n  "version": "0.1.0",\n  "scripts": {{{scripts}}},\n  {deps}\n  {dev_deps}\n}}\n'


def tsconfig() -> str:
    return '{\n  "compilerOptions": {\n    "target": "ES2022",\n    "module": "ES2022",\n    "strict": true,\n    "outDir": "dist"\n  },\n  "include": ["src", "tests"]\n}\n'


def node_dockerfile() -> str:
    return "FROM node:22-slim\nWORKDIR /app\nCOPY package*.json ./\nRUN npm install\nCOPY . .\nCMD [\"npm\", \"test\"]\n"
