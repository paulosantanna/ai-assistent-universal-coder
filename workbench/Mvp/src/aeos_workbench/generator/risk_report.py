"""Risk Report Generator - produces risk-report.md."""

import re
from datetime import datetime, timezone


class RiskReportGenerator:
    def __init__(self, scan_result, stacks):
        self.scan = scan_result
        self.stacks = stacks

    def _assess_security_risks(self):
        risks = []
        files = self.scan.get("files", [])

        has_lockfile = any(f["name"] in ("package-lock.json", "yarn.lock", "Cargo.lock", "go.sum", "poetry.lock") for f in files)
        has_gitignore = any(f["name"] == ".gitignore" for f in files)
        has_env = any(f["name"] == ".env" or f["name"] == ".env.example" for f in files)
        has_secrets = any(".env" in f["path"] and f["name"] != ".env.example" for f in files if ".env" in f["path"])

        if not has_lockfile:
            risks.append({
                "id": "risk-sec-001",
                "category": "security",
                "severity": "medium",
                "description": "Nenhum arquivo de lockfile encontrado. Dependências não estão travadas.",
                "recommendation": "Gere lockfile (package-lock.json, Cargo.lock, etc.) para travar versões.",
            })

        if not has_gitignore:
            risks.append({
                "id": "risk-sec-002",
                "category": "security",
                "severity": "high",
                "description": "Nenhum .gitignore encontrado. Arquivos sensíveis podem ser versionados.",
                "recommendation": "Crie .gitignore com padrões para a stack detectada.",
            })

        if has_secrets:
            risks.append({
                "id": "risk-sec-003",
                "category": "security",
                "severity": "critical",
                "description": "Arquivo .env encontrado versionado. Segredos podem estar expostos.",
                "recommendation": "Adicione .env ao .gitignore e remova do histórico do Git.",
            })

        return risks

    def _assess_dependency_risks(self):
        risks = []
        stacks = self.stacks

        for stack in stacks:
            if not stack.get("missing"):
                continue
            if stack["confidence"] > 0.7:
                risks.append({
                    "id": f"risk-dep-{stack['id']}",
                    "category": "dependency",
                    "severity": "low" if len(stack["missing"]) <= 2 else "medium",
                    "description": f"Stack {stack['name']} detectada mas faltam indicadores: {', '.join(stack['missing'][:3])}",
                    "recommendation": f"Verifique se os arquivos típicos de {stack['name']} estão presentes.",
                })

        return risks

    def _assess_architecture_risks(self):
        risks = []
        files = self.scan.get("files", [])
        languages = self.scan.get("languages", {})

        total_lines = self.scan.get("total_lines", 0)
        if total_lines > 50000 and len(files) > 200:
            risks.append({
                "id": "risk-arch-001",
                "category": "architecture",
                "severity": "medium",
                "description": f"Projeto grande: {total_lines:,} linhas em {len(files)} arquivos. Possível débito de modularização.",
                "recommendation": "Considere modularizar em pacotes/serviços menores.",
            })

        for lang, info in languages.items():
            if info["files"] > 100:
                risks.append({
                    "id": f"risk-arch-{lang}",
                    "category": "architecture",
                    "severity": "low",
                    "description": f"Alta concentração de arquivos {lang} ({info['files']} arquivos). Possível falta de separação.",
                    "recommendation": f"Considere dividir {lang} em módulos por responsabilidade.",
                })

        has_docker = any(f["type"] == "dockerfile" for f in files)
        has_compose = any("docker-compose" in f["type"] for f in files)
        if has_docker and not has_compose:
            risks.append({
                "id": "risk-arch-002",
                "category": "architecture",
                "severity": "low",
                "description": "Dockerfile presente mas sem docker-compose.yml. Orquestração local limitada.",
                "recommendation": "Adicione docker-compose.yml para facilitar execução local.",
            })

        return risks

    def _assess_test_risks(self):
        risks = []
        files = self.scan.get("files", [])

        test_files = [f for f in files if "test" in f["name"].lower() or "spec" in f["name"].lower() or "test" in f["path"].lower()]
        source_files = [f for f in files if f["category"] == "source"]

        if source_files and not test_files:
            risks.append({
                "id": "risk-test-001",
                "category": "testing",
                "severity": "high",
                "description": "Código fonte encontrado mas nenhum arquivo de teste detectado.",
                "recommendation": "Implemente testes unitários e/ou de integração.",
            })
        elif source_files and len(test_files) < len(source_files) * 0.1:
            risks.append({
                "id": "risk-test-002",
                "category": "testing",
                "severity": "medium",
                "description": f"Baixa proporção de testes: {len(test_files)} testes para {len(source_files)} fontes.",
                "recommendation": "Aumente cobertura de testes para pelo menos 20% dos arquivos fonte.",
            })

        return risks

    def _assess_stack_risks(self):
        risks = []
        stacks = self.stacks

        if not stacks:
            risks.append({
                "id": "risk-stack-001",
                "category": "stack",
                "severity": "high",
                "description": "Nenhuma stack tecnológica identificada com confiança.",
                "recommendation": "Verifique se o diretório contém um projeto de software válido.",
            })

        return risks

    def generate(self):
        lines = []

        lines.append("# AEOS Risk Report\n")
        lines.append(f"**Generated:** {self.scan.get('scan_timestamp', datetime.now(timezone.utc).isoformat())}")
        lines.append(f"**Project:** {self.scan.get('project_name', 'unknown')}")
        lines.append(f"**Version:** 1.0.0\n")

        all_risks = []
        all_risks.extend(self._assess_security_risks())
        all_risks.extend(self._assess_dependency_risks())
        all_risks.extend(self._assess_architecture_risks())
        all_risks.extend(self._assess_test_risks())
        all_risks.extend(self._assess_stack_risks())

        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        all_risks.sort(key=lambda r: (severity_order.get(r["severity"], 99), r["id"]))

        # Summary
        critical_count = sum(1 for r in all_risks if r["severity"] == "critical")
        high_count = sum(1 for r in all_risks if r["severity"] == "high")
        medium_count = sum(1 for r in all_risks if r["severity"] == "medium")
        low_count = sum(1 for r in all_risks if r["severity"] == "low")

        lines.append("## Risk Summary\n")
        lines.append(f"| Severity | Count |")
        lines.append(f"|----------|-------|")
        lines.append(f"| 🔴 Critical | {critical_count} |")
        lines.append(f"| 🟠 High | {high_count} |")
        lines.append(f"| 🟡 Medium | {medium_count} |")
        lines.append(f"| 🟢 Low | {low_count} |")
        lines.append(f"| **Total** | **{len(all_risks)}** |\n")

        # Risk Details by Severity
        for severity in ["critical", "high", "medium", "low"]:
            severity_risks = [r for r in all_risks if r["severity"] == severity]
            if not severity_risks:
                continue

            sev_label = {"critical": "Critical 🔴", "high": "High 🟠", "medium": "Medium 🟡", "low": "Low 🟢"}[severity]
            lines.append(f"## {sev_label} Risks\n")

            for risk in severity_risks:
                lines.append(f"### {risk['id']}: {risk['description']}")
                lines.append(f"- **Category:** {risk['category']}")
                lines.append(f"- **Severity:** {risk['severity']}")
                lines.append(f"- **Recommendation:** {risk['recommendation']}")
                lines.append("")

        if not all_risks:
            lines.append("**No risks detected.**\n")

        lines.append("---\n")
        lines.append(f"*AEOS Risk Report v1.0.0 — {len(all_risks)} risks identified*")

        # Add evidence
        self.scan.setdefault("evidence", []).append({
            "evidence_id": "evt-risk-assessment",
            "type": "report",
            "claim": f"Risk assessment complete: {len(all_risks)} risks found ({critical_count} critical, {high_count} high)",
            "reference": "risk-report.md",
            "hash": self.scan.get("scan_id", "unknown"),
            "timestamp": self.scan.get("scan_timestamp", ""),
            "verified": True,
        })

        return "\n".join(lines)
