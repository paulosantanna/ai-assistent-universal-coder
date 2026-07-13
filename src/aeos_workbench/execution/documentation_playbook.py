"""Documentation Generation Playbook — generates docs in sandbox based on detected files."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from aeos_workbench.scanner.scanner import ProjectScanner
from aeos_workbench.stack_detector.detector import StackDetector

import re

SECRET_PATTERNS = [
    (r'(?i)password\s*[=:]\s*[\'"][^\'"]+[\'"]', "password-assignment"),
    (r'(?i)secret\s*[=:]\s*[\'"][^\'"]+[\'"]', "secret-assignment"),
    (r'(?i)api[_-]?key\s*[=:]\s*[\'"][^\'"]+[\'"]', "api-key"),
    (r'(?i)token\s*[=:]\s*[\'"][^\'"]+[\'"]', "token-assignment"),
    (r'AKIA[0-9A-Z]{16}', "aws-access-key"),
    (r'sk-[a-zA-Z0-9]{20,}', "openai-secret-key"),
    (r'-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----', "private-key"),
    (r'-----BEGIN CERTIFICATE-----', "certificate"),
]


def _has_secrets(content: str) -> list[str]:
    found = []
    for pattern, label in SECRET_PATTERNS:
        if re.search(pattern, content):
            found.append(label)
    return found


def _markdown_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


class DocumentationPlaybook:
    def __init__(self, sandbox_writer, rollback_manager, step_engine, execution_id: str):
        self.sandbox_writer = sandbox_writer
        self.rollback_manager = rollback_manager
        self.step_engine = step_engine
        self.execution_id = execution_id
        self.generated_artifacts: list[dict] = []
        self.risks: list[str] = []
        self.assumptions: list[str] = []
        self.secrets_found: list[str] = []
        self.files_analyzed: list[str] = []

    def execute(self, target_path: Path) -> dict:
        step_id = self.step_engine.register_step({
            "step_id": "documentation-scan",
            "skill": "documentation",
            "status": "running",
            "inputs": {"target_path": str(target_path)},
            "outputs": {},
            "evidence": [],
            "permission_decisions": [],
            "risks": [],
            "errors": [],
        })

        scan_result = self._scan_project(target_path)
        self.files_analyzed = [f["path"] for f in scan_result.get("files", [])[:50]]
        languages = scan_result.get("languages", {})
        stacks = self._detect_stacks(scan_result)

        self.step_engine.update_step(step_id, {
            "status": "completed",
            "outputs": {
                "total_files": scan_result.get("total_files", 0),
                "languages": list(languages.keys()),
                "stacks": [s.get("name", "?") for s in stacks],
            },
            "evidence": [
                {"type": "scan", "files_found": len(self.files_analyzed)}
            ],
        })
        self.step_engine.save_all()

        self.generate_readme(target_path, scan_result, stacks)
        self.generate_architecture(target_path, scan_result, stacks)
        self.generate_runbook(target_path, scan_result, stacks)
        self.generate_dependency_overview(scan_result, stacks)
        self.generate_risk_summary(scan_result, stacks)

        return {
            "generated_artifacts": self.generated_artifacts,
            "risks": self.risks,
            "assumptions": self.assumptions,
            "secrets_found": self.secrets_found,
            "files_analyzed": self.files_analyzed,
        }

    def _scan_project(self, target_path: Path) -> dict:
        scanner = ProjectScanner(target_path)
        return scanner.scan()

    def _detect_stacks(self, scan_result: dict) -> list[dict]:
        detector = StackDetector(scan_result)
        return detector.detect()

    def _write_artifact(self, name: str, content: str, artifact_type: str = "documentation"):
        secrets = _has_secrets(content)
        if secrets:
            self.secrets_found.append(f"Potential secret pattern in {name}: {secrets}")
            content = f"""[SECURITY BLOCKED] Potential secret pattern detected: {', '.join(secrets)}
This artifact was blocked from generation.
"""
            self.risks.append(f"Secret exposure blocked in {name}")

        sandbox_path = self.sandbox_writer.write(name, content)
        self.rollback_manager.register_generated_file(
            file_path=sandbox_path,
            sandbox_relative=name,
            content_preview=content[:100],
        )
        self.generated_artifacts.append({
            "name": name,
            "path": str(sandbox_path),
            "type": artifact_type,
            "size": len(content.encode("utf-8")),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        return sandbox_path

    def generate_readme(self, target_path: Path, scan_result: dict, stacks: list[dict]):
        lang_summary = ", ".join(
            f"{lang}: {info['files']} files ({info['lines']} lines)"
            for lang, info in scan_result.get("languages", {}).items()
        )
        files = scan_result.get("files", [])
        source_files = [f for f in files if f.get("category") == "source"]
        config_files = [f for f in files if f.get("category") == "config"]

        content = f"""# {target_path.name} — Generated Documentation

> **Auto-generated by AEOS v0.2 Governed Execution Layer**
> **Date:** {datetime.now(timezone.utc).isoformat()}
> **Mode:** Sandbox (no real files modified)

---

## Project Overview

**Root:** `{target_path}`
**Total Files:** {scan_result.get('total_files', 0)}
**Total Directories:** {scan_result.get('total_dirs', 0)}
**Total Lines:** {scan_result.get('total_lines', 0)}

### Detected Languages

{lang_summary}

### Detected Technology Stacks

"""
        for s in stacks:
            inds = s.get('indicators', [])
            ind_strs = [i.get('evidence', i.get('file', '')) if isinstance(i, dict) else str(i) for i in inds]
            content += f"- **{s.get('name', '?')}** — {', '.join(ind_strs[:5])}\n"

        content += f"""
### File Categories

| Category | Count |
|----------|-------|
| Source | {len(source_files)} |
| Configuration | {len(config_files)} |
"""
        cats = scan_result.get("file_categories", {})
        for cat, count in sorted(cats.items()):
            content += f"| {cat} | {count} |\n"

        content += """
## Key Source Files

| File | Language | Lines |
|------|----------|-------|
"""
        for f in source_files[:20]:
            content += f"| `{_markdown_escape(f['path'])}` | {f.get('language', '?')} | {f.get('lines', 0)} |\n"

        if source_files and len(source_files) > 20:
            content += f"| ... and {len(source_files) - 20} more source files | | |\n"

        content += """
> **Evidence:** All file listings based on actual scan results.
> **Assumptions:** None — all data is factual from repository scan.
"""
        self._write_artifact("README.generated.md", content)

    def generate_architecture(self, target_path: Path, scan_result: dict, stacks: list[dict]):
        files = scan_result.get("files", [])
        source_files = [f for f in files if f.get("category") == "source"]
        config_files = [f for f in files if f.get("category") == "config"]

        by_language = {}
        for f in source_files:
            lang = f.get("language", "other")
            if lang not in by_language:
                by_language[lang] = []
            by_language[lang].append(f)

        content = f"""# ARCHITECTURE.generated.md — Architecture Overview

> **Auto-generated by AEOS v0.2**
> **Date:** {datetime.now(timezone.utc).isoformat()}

---

## Source Structure

"""
        for lang, lang_files in sorted(by_language.items()):
            dirs = set(Path(f["path"]).parent for f in lang_files)
            content += f"### {lang.capitalize()} ({len(lang_files)} files, {len(dirs)} directories)\n\n"
            content += "```\n"
            for d in sorted(dirs):
                fs_in_dir = [f for f in lang_files if Path(f["path"]).parent == d]
                content += f"{d}/\n"
                for f in fs_in_dir:
                    content += f"  {Path(f['name'])}\n"
            content += "```\n\n"

        content += """## Configuration Files

| File | Type |
|------|------|
"""
        for f in config_files:
            content += f"| `{_markdown_escape(f['path'])}` | {f.get('type', '?')} |\n"

        content += f"""
## Architecture Notes

- **Assumption:** This project appears to use a {'multi-language' if len(by_language) > 1 else 'single-language'} architecture based on detected file types.
- **Assumption:** Dependency management is handled through {', '.join(f.get('name', '?') for f in config_files if f.get('type') in ('npm-package', 'maven-pom', 'pyproject', 'pip-requirements', 'cargo', 'go-mod'))[:3] or 'unknown mechanisms'}.
- **Fact:** {len(source_files)} source files analyzed across {len(by_language)} languages.

**Evidence:** All module listings are based on ProjectScanner results from `{target_path}`.
**Assumptions marked with "Assumption:" prefix.**
"""
        self._write_artifact("ARCHITECTURE.generated.md", content)

    def generate_runbook(self, target_path: Path, scan_result: dict, stacks: list[dict]):
        content = f"""# RUNBOOK.generated.md — Operational Runbook

> **Generated by AEOS v0.2**
> **Date:** {datetime.now(timezone.utc).isoformat()}

---

## Purpose

This runbook covers the operational procedures for the {target_path.name} project.

## Prerequisites

- Repository cloned at `{target_path}`
- Appropriate runtime environment for detected stacks

## Detected Project Commands

"""
        has_scripts = False
        for f in scan_result.get("files", []):
            if f.get("name") == "package.json":
                has_scripts = True
                content += f"""### npm scripts (from `{f['path']}`)

```json
# Run: npm run <script>
```
"""
            elif f.get("name") == "Makefile" or f.get("name") == "makefile":
                has_scripts = True
                content += f"""### Make targets (from `{f['path']}`)

```makefile
# Run: make <target>
```
"""
            elif f.get("name") == "pyproject.toml":
                has_scripts = True
                content += f"""### Python tasks (from `{f['path']}`)

```bash
# Run: python -m <module>
```
"""

        if not has_scripts:
            content += "**Assumption:** No common script configuration detected. Check project documentation for build/run instructions.\n"

        content += f"""
## Files Changed (sandbox only)

All generated files are in `.aeos/sandbox/{self.execution_id}/`. No real files were modified.

## Troubleshooting

- If generated documentation is incomplete, ensure the project has been fully scanned.
- If secrets are detected, the artifact is blocked — review and remove sensitive patterns.
- If the sandbox is corrupted, delete `.aeos/sandbox/{self.execution_id}/` and re-run.

## Rollback

To rollback this execution:

```bash
# Delete generated sandbox files
Remove-Item -Recurse -Force ".aeos/sandbox/{self.execution_id}/"
```
"""
        self._write_artifact("RUNBOOK.generated.md", content)

    def generate_dependency_overview(self, scan_result: dict, stacks: list[dict]):
        config_files = [f for f in scan_result.get("files", []) if f.get("category") == "config"]
        dependency_files = [f for f in config_files if f.get("type") in (
            "npm-package", "npm-lock", "pip-requirements", "pyproject",
            "maven-pom", "gradle-build", "cargo", "go-mod",
        )]

        content = f"""# DEPENDENCY_OVERVIEW.generated.md

> **Generated by AEOS v0.2**
> **Date:** {datetime.now(timezone.utc).isoformat()}

---

## Dependency Files Detected

| File | Type |
|------|------|
"""
        for f in dependency_files:
            content += f"| `{_markdown_escape(f['path'])}` | {f.get('type', '?')} |\n"

        if not dependency_files:
            content += "| *(no dependency files detected)* | |\n"
            content += "\n**Assumption:** This project may not use a standard dependency manager, or dependency files are not in standard locations.\n"

        content += f"""
## Stack Summary

| Stack | Indicators |
|-------|------------|
"""
        for s in stacks:
            inds = s.get('indicators', [])
            ind_strs = [i.get('evidence', i.get('file', '')) if isinstance(i, dict) else str(i) for i in inds]
            content += f"| {s.get('name', '?')} | {', '.join(ind_strs[:5])[:100]} |\n"

        content += """
### Evidence

All dependency file paths are based on actual scan results.
"""
        self._write_artifact("DEPENDENCY_OVERVIEW.generated.md", content)

    def generate_risk_summary(self, scan_result: dict, stacks: list[dict]):
        files = scan_result.get("files", [])
        security_issues = [f for f in files if f.get("type") in (
            "env-template", "env-file"
        )]
        large_files = [f for f in files if f.get("size", 0) > 500 * 1024]

        env_files = [f for f in files if ".env" in f.get("name", "")]
        for f in files:
            if ".env" in f.get("name", ""):
                if f not in env_files:
                    env_files.append(f)

        content = f"""# RISK_SUMMARY.generated.md — Risk Assessment

> **Generated by AEOS v0.2**
> **Date:** {datetime.now(timezone.utc).isoformat()}

---

## Detected Risks

| Risk | Severity | Evidence |
|------|----------|----------|
"""
        if env_files:
            for ef in env_files:
                content += f"| Environment file detected: `{ef['path']}` | Medium | File found at `{ef['path']}` |\n"
                self.risks.append(f"Environment file detected: {ef['path']}")

        if self.secrets_found:
            for sf in self.secrets_found:
                content += f"| Potential secret pattern | High | {sf} |\n"
                self.risks.append(sf)

        if large_files:
            for lf in large_files[:5]:
                content += f"| Large file: `{lf['path']}` ({lf.get('size', 0)} bytes) | Low | File size exceeds 500KB |\n"

        if not env_files and not self.secrets_found and not large_files:
            content += "| No significant risks detected | Low | Scan complete with no findings |\n"

        content += f"""
## Risk Mitigation

- **Environment files:** Ensure `.env*` files are in `.gitignore` and never committed.
- **Large files:** Consider splitting or using Git LFS.
- **Secrets:** Never hardcode secrets. Use environment variables or a secret manager.

## Assumptions

- Risk assessment is based on file structure analysis, not on content inspection beyond pattern matching.
- Dependency vulnerabilities require a dedicated `npm audit` or `pip audit` to confirm.
"""
        self._write_artifact("RISK_SUMMARY.generated.md", content)