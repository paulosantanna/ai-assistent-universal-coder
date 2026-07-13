from complete_docs_mcp.generator import architecture_package, documentation_package, documentation_plan, mermaid_template, validate_mermaid


def test_documentation_plan_requires_mermaid_diagrams():
    plan = documentation_plan("AEOS")
    assert plan["status"] == "PASS"
    assert "architecture" in plan["required_diagrams"]
    assert "cloud-readiness" in plan["required_diagrams"]
    assert plan["sections"]


def test_mermaid_template_returns_valid_flowchart():
    result = mermaid_template("architecture", "AEOS")
    assert result["status"] == "PASS"
    assert result["mermaid"].startswith("flowchart TD")


def test_validate_mermaid_flags_sensitive_terms():
    result = validate_mermaid("flowchart TD\n  A[api_key] --> B[Service]")
    assert result["status"] == "REVIEW"
    assert result["issues"]


def test_documentation_package_includes_output_files_and_diagrams():
    package = documentation_package("AEOS")
    assert package["status"] == "PASS"
    assert package["diagrams"]
    assert "docs/ARCHITECTURE.md" in package["output_files"]
    assert "docs/CLOUD_READINESS.md" in package["output_files"]
    assert package["artifacts"]
    assert package["adr_candidates"]


def test_architecture_package_includes_cloud_review_order_and_content():
    package = architecture_package("AEOS")
    assert package["status"] == "PASS"
    assert package["maturity_target"] == "cloud-ready"
    assert "docs/SKILLS_MCPS_LSPS.md" in package["review_order"]
    assert any(artifact["path"] == "docs/adr/0001-documentation-architecture-package.md" for artifact in package["artifacts"])
    assert any(item["dimension"] == "observability" for item in package["cloud_readiness"])


def test_new_diagram_templates_validate():
    for diagram_type in ("skill-mcp-lsp", "cloud-readiness"):
        template = mermaid_template(diagram_type, "AEOS")
        assert template["status"] == "PASS"
        assert validate_mermaid(template["mermaid"])["status"] == "PASS"
