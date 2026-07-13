from __future__ import annotations

import argparse

from .generator import architecture_package, documentation_package, documentation_plan, mermaid_template, validate_mermaid


def build_mcp():
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP("AEOS Complete Documentation MCP")

    @mcp.tool(name="docs.plan")
    def docs_plan(scope: str, audience: str = "engineering", depth: str = "complete") -> dict:
        return documentation_plan(scope, audience, depth)

    @mcp.tool(name="docs.mermaid_template")
    def docs_mermaid_template(diagram_type: str, title: str = "System") -> dict:
        return mermaid_template(diagram_type, title)

    @mcp.tool(name="docs.validate_mermaid")
    def docs_validate_mermaid(source: str) -> dict:
        return validate_mermaid(source)

    @mcp.tool(name="docs.package")
    def docs_package(scope: str, audience: str = "engineering", include_diagrams: bool = True) -> dict:
        return documentation_package(scope, audience, include_diagrams)

    @mcp.tool(name="docs.architecture_package")
    def docs_architecture_package(scope: str, audience: str = "engineering", maturity_target: str = "cloud-ready") -> dict:
        return architecture_package(scope, audience, maturity_target)

    return mcp


def main() -> None:
    parser = argparse.ArgumentParser(description="AEOS complete documentation MCP")
    parser.parse_args()
    build_mcp().run(transport="stdio")


if __name__ == "__main__":
    main()
