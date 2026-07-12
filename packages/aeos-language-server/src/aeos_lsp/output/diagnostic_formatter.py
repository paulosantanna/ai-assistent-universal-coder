from __future__ import annotations

import json
import logging
from typing import Any

from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range

logger = logging.getLogger(__name__)


class DiagnosticFormatter:
    SEVERITY_LABELS: dict[DiagnosticSeverity, str] = {
        DiagnosticSeverity.Error: "error",
        DiagnosticSeverity.Warning: "warning",
        DiagnosticSeverity.Information: "info",
        DiagnosticSeverity.Hint: "hint",
    }

    def __init__(self, profile: str = "editor") -> None:
        self._profile = profile

    @property
    def profile(self) -> str:
        return self._profile

    @profile.setter
    def profile(self, value: str) -> None:
        if value in ("editor", "agent", "json", "sarif"):
            self._profile = value
        else:
            logger.warning("Unknown diagnostic profile: %s, using 'editor'", value)
            self._profile = "editor"

    def format(self, diagnostics: list[Diagnostic], uri: str = "") -> str:
        if self._profile == "json":
            return self.format_json(diagnostics, uri)
        elif self._profile == "sarif":
            return self.format_sarif(diagnostics, uri)
        elif self._profile == "agent":
            return self.format_agent(diagnostics, uri)
        else:
            return self.format_editor(diagnostics, uri)

    def format_editor(self, diagnostics: list[Diagnostic], uri: str = "") -> str:
        if not diagnostics:
            return ""

        lines: list[str] = []
        for d in diagnostics:
            sev = self.SEVERITY_LABELS.get(d.severity or DiagnosticSeverity.Hint, "unknown")
            location = self._format_location(d.range)
            code = d.code or "?"
            msg = d.message.split("\n")[0] if d.message else ""
            lines.append(f"  {location} {sev} [{code}] {msg}")

        summary = self._format_summary(diagnostics)
        header = f"Diagnostics for {uri}" if uri else "Diagnostics"
        result = f"{header} ({summary})\n" + "\n".join(lines)
        return result

    def format_agent(self, diagnostics: list[Diagnostic], uri: str = "") -> str:
        if not diagnostics:
            return ""

        parts: list[str] = []
        errors = [d for d in diagnostics if d.severity == DiagnosticSeverity.Error]
        warnings = [d for d in diagnostics if d.severity == DiagnosticSeverity.Warning]
        infos = [d for d in diagnostics if d.severity in (DiagnosticSeverity.Information, DiagnosticSeverity.Hint)]

        if errors:
            parts.append(f"## errors ({len(errors)})")
            for d in errors[:20]:
                parts.append(f"- [{d.code}] {d.message[:200]}")
            if len(errors) > 20:
                parts.append(f"- ... and {len(errors) - 20} more")

        if warnings:
            parts.append(f"## warnings ({len(warnings)})")
            for d in warnings[:20]:
                parts.append(f"- [{d.code}] {d.message[:200]}")
            if len(warnings) > 20:
                parts.append(f"- ... and {len(warnings) - 20} more")

        if infos:
            parts.append(f"## info ({len(infos)})")
            for d in infos[:10]:
                parts.append(f"- [{d.code}] {d.message[:200]}")

        if not parts:
            return "No diagnostics"

        return "\n".join(parts)

    def format_json(self, diagnostics: list[Diagnostic], uri: str = "") -> str:
        data: list[dict[str, Any]] = []
        for d in diagnostics:
            entry = {
                "uri": uri,
                "range": {
                    "start": {"line": d.range.start.line, "character": d.range.start.character},
                    "end": {"line": d.range.end.line, "character": d.range.end.character},
                },
                "severity": self.SEVERITY_LABELS.get(d.severity or DiagnosticSeverity.Hint, "unknown"),
                "code": d.code,
                "source": d.source,
                "message": d.message,
            }
            if d.code_description:
                entry["code_description"] = d.code_description
            if d.tags:
                entry["tags"] = [str(t) for t in d.tags]
            if d.related_information:
                entry["related_information"] = [
                    {
                        "location": {
                            "uri": ri.location.uri,
                            "range": {
                                "start": {"line": ri.location.range.start.line, "character": ri.location.range.start.character},
                                "end": {"line": ri.location.range.end.line, "character": ri.location.range.end.character},
                            },
                        },
                        "message": ri.message,
                    }
                    for ri in d.related_information
                ]
            data.append(entry)

        return json.dumps(data, indent=2, ensure_ascii=False)

    def format_sarif(self, diagnostics: list[Diagnostic], uri: str = "") -> str:
        sarif_runs: list[dict[str, Any]] = [{
            "tool": {
                "driver": {
                    "name": "AEOS Language Server",
                    "version": "1.0.0",
                    "informationUri": "https://aeos.ai",
                }
            },
            "results": [],
        }]

        for d in diagnostics:
            level = "none"
            if d.severity == DiagnosticSeverity.Error:
                level = "error"
            elif d.severity == DiagnosticSeverity.Warning:
                level = "warning"
            elif d.severity in (DiagnosticSeverity.Information, DiagnosticSeverity.Hint):
                level = "note"

            result = {
                "ruleId": str(d.code or "unknown"),
                "level": level,
                "message": {
                    "text": d.message,
                },
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {
                                "uri": uri,
                            },
                            "region": {
                                "startLine": d.range.start.line + 1,
                                "startColumn": d.range.start.character + 1,
                                "endLine": d.range.end.line + 1,
                                "endColumn": d.range.end.character + 1,
                            },
                        }
                    }
                ],
            }

            if d.source:
                result["message"]["text"] = f"[{d.source}] {d.message}"

            sarif_runs[0]["results"].append(result)

        sarif_doc = {
            "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
            "version": "2.1.0",
            "runs": sarif_runs,
        }

        return json.dumps(sarif_doc, indent=2, ensure_ascii=False)

    def format_single(self, diagnostic: Diagnostic, uri: str = "") -> str:
        return self.format([diagnostic], uri)

    def summary(self, diagnostics: list[Diagnostic]) -> str:
        return self._format_summary(diagnostics)

    def _format_location(self, range_: Range) -> str:
        return f"L{range_.start.line + 1}:{range_.start.character + 1}"

    def _format_summary(self, diagnostics: list[Diagnostic]) -> str:
        if not diagnostics:
            return "0 diagnostics"

        errors = sum(1 for d in diagnostics if d.severity == DiagnosticSeverity.Error)
        warnings = sum(1 for d in diagnostics if d.severity == DiagnosticSeverity.Warning)
        infos = sum(1 for d in diagnostics if d.severity in (DiagnosticSeverity.Information, DiagnosticSeverity.Hint))

        parts: list[str] = []
        if errors:
            parts.append(f"{errors} error{'s' if errors != 1 else ''}")
        if warnings:
            parts.append(f"{warnings} warning{'s' if warnings != 1 else ''}")
        if infos:
            parts.append(f"{infos} info")
        if not parts:
            parts.append("0 issues")

        return ", ".join(parts) if parts else "0 diagnostics"

    def __repr__(self) -> str:
        return f"DiagnosticFormatter(profile={self._profile})"
