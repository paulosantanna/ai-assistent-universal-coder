from universal_project_mcp.planner import production_checklist, project_plan, scaffold_manifest, scaffold_package, stack_matrix


def test_project_plan_blocks_missing_stack_decisions():
    plan = project_plan("Build an app")
    assert plan["status"] == "BLOCKED"
    assert plan["blocking_conditions"]


def test_project_plan_passes_with_stack_and_database():
    plan = project_plan("Build API", "hexagonal", ["Python"], ["PostgreSQL"])
    assert plan["status"] == "PASS"
    assert "zero-to-production-project" in plan["required_playbooks"]


def test_stack_matrix_includes_language_and_database_decisions():
    matrix = stack_matrix(["Java"], ["PostgreSQL"])
    assert matrix["languages"][0]["language"] == "Java"
    assert "migration tool" in matrix["databases"][0]["required_decisions"]


def test_production_checklist_contains_token_budget_stop_condition():
    checklist = production_checklist("event-driven")
    assert any("token budget" in item for item in checklist["stop_conditions"])


def test_scaffold_manifest_is_sandbox_only():
    manifest = scaffold_manifest("demo", "clean", ["TypeScript"])
    assert manifest["write_policy"] == "sandbox_only_until_approval"


def test_scaffold_package_generates_python_postgres_files():
    package = scaffold_package("Demo API", "Build API", "hexagonal", ["Python"], ["PostgreSQL"])
    paths = {artifact["path"] for artifact in package["artifacts"]}

    assert package["status"] == "PASS"
    assert "pyproject.toml" in paths
    assert "src/app/main.py" in paths
    assert "db/migrations/001_initial_postgresql.sql" in paths
    assert "docs/ROLLBACK.md" in paths


def test_scaffold_package_generates_java_and_typescript_without_duplicate_paths():
    package = scaffold_package("Polyglot", "Build services", "modular", ["Java", "TypeScript"], ["MongoDB"])
    paths = [artifact["path"] for artifact in package["artifacts"]]

    assert "pom.xml" in paths
    assert "package.json" in paths
    assert "tsconfig.json" in paths
    assert len(paths) == len(set(paths))


def test_scaffold_package_blocks_missing_required_decisions():
    package = scaffold_package("", "", "unspecified", [], [])
    assert package["status"] == "BLOCKED"
    assert package["blocking_conditions"]
