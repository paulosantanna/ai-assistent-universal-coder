from __future__ import annotations

import argparse

from .planner import production_checklist, project_plan, scaffold_manifest, scaffold_package, stack_matrix


def build_mcp():
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP("AEOS Universal Project MCP")

    @mcp.tool(name="project.plan")
    def tool_project_plan(
        objective: str,
        architecture: str = "unspecified",
        languages: list[str] | None = None,
        databases: list[str] | None = None,
        deployment_target: str = "cloud",
    ) -> dict:
        return project_plan(objective, architecture, languages, databases, deployment_target)

    @mcp.tool(name="project.stack_matrix")
    def tool_stack_matrix(languages: list[str] | None = None, databases: list[str] | None = None) -> dict:
        return stack_matrix(languages, databases)

    @mcp.tool(name="project.production_checklist")
    def tool_production_checklist(architecture: str, deployment_target: str = "cloud") -> dict:
        return production_checklist(architecture, deployment_target)

    @mcp.tool(name="project.scaffold_manifest")
    def tool_scaffold_manifest(project_name: str, architecture: str, languages: list[str] | None = None) -> dict:
        return scaffold_manifest(project_name, architecture, languages)

    @mcp.tool(name="project.scaffold_package")
    def tool_scaffold_package(
        project_name: str,
        objective: str,
        architecture: str,
        languages: list[str] | None = None,
        databases: list[str] | None = None,
        deployment_target: str = "cloud",
    ) -> dict:
        return scaffold_package(project_name, objective, architecture, languages, databases, deployment_target)

    return mcp


def main() -> None:
    parser = argparse.ArgumentParser(description="AEOS universal project MCP")
    parser.parse_args()
    build_mcp().run(transport="stdio")


if __name__ == "__main__":
    main()
