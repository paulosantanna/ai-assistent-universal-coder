"""Playbook Recommender - produces recommended-playbooks.md."""

from datetime import datetime, timezone


PLAYBOOK_TEMPLATES = {
    "java-spring": [
        {
            "id": "pb-java-migrate-21",
            "name": "Java 21 Migration",
            "objective": "Migrate codebase to Java 21 features",
            "risk_level": "medium",
            "phases": ["Audit current Java version", "Update language features", "Test compatibility"],
        },
        {
            "id": "pb-spring-boot-upgrade",
            "name": "Spring Boot Upgrade",
            "objective": "Upgrade Spring Boot to latest stable version",
            "risk_level": "high",
            "phases": ["Review changelog", "Update dependencies", "Fix breaking changes", "Run full test suite"],
        },
        {
            "id": "pb-spring-security-audit",
            "name": "Spring Security Audit",
            "objective": "Audit and harden Spring Security configuration",
            "risk_level": "high",
            "phases": ["Review security config", "Check authentication", "Audit authorization rules", "Penetration test"],
        },
    ],
    "python-fastapi": [
        {
            "id": "pb-python-modernize",
            "name": "Python Modernization",
            "objective": "Modernize Python codebase to 3.12+ patterns",
            "risk_level": "low",
            "phases": ["Update syntax", "Add type hints", "Modernize dependencies"],
        },
        {
            "id": "pb-fastapi-production",
            "name": "FastAPI Production Readiness",
            "objective": "Harden FastAPI application for production",
            "risk_level": "medium",
            "phases": ["Add middleware", "Configure CORS", "Setup logging", "Add rate limiting"],
        },
    ],
    "python-ai-rag": [
        {
            "id": "pb-rag-optimization",
            "name": "RAG Pipeline Optimization",
            "objective": "Optimize retrieval-augmented generation pipeline",
            "risk_level": "medium",
            "phases": ["Audit embedding strategy", "Optimize chunking", "Evaluate retrieval quality", "Benchmark latency"],
        },
        {
            "id": "pb-ai-security-review",
            "name": "AI Security Review",
            "objective": "Review AI pipeline for security and prompt injection",
            "risk_level": "high",
            "phases": ["Review prompt templates", "Audit input sanitization", "Check output filtering", "Rate limit assessment"],
        },
    ],
    "typescript-react": [
        {
            "id": "pb-react-performance",
            "name": "React Performance Optimization",
            "objective": "Optimize React application performance",
            "risk_level": "medium",
            "phases": ["Audit renders", "Implement code splitting", "Optimize bundle size", "Add caching"],
        },
        {
            "id": "pb-npm-audit-fix",
            "name": "NPM Dependency Audit",
            "objective": "Audit and fix NPM dependencies",
            "risk_level": "high",
            "phases": ["Run npm audit", "Update vulnerable packages", "Test breaking changes"],
        },
    ],
    "fullstack-docker": [
        {
            "id": "pb-docker-hardening",
            "name": "Docker Hardening",
            "objective": "Harden Docker configuration for production",
            "risk_level": "high",
            "phases": ["Review Dockerfiles", "Implement multi-stage builds", "Scan images", "Configure resource limits"],
        },
        {
            "id": "pb-compose-orchestration",
            "name": "Docker Compose Orchestration",
            "objective": "Set up Docker Compose for local development",
            "risk_level": "low",
            "phases": ["Create compose file", "Configure services", "Set up volumes", "Add health checks"],
        },
    ],
}

CROSS_STACK_PLAYBOOKS = [
    {
        "id": "pb-ci-setup",
        "name": "CI/CD Pipeline Setup",
        "objective": "Set up continuous integration pipeline",
        "risk_level": "low",
        "stacks": ["all"],
        "phases": ["Choose CI provider", "Configure build", "Set up test automation", "Add deployment"],
    },
    {
        "id": "pb-documentation",
        "name": "Project Documentation",
        "objective": "Create comprehensive project documentation",
        "risk_level": "low",
        "stacks": ["all"],
        "phases": ["Create README", "Document API", "Add architecture docs", "Create contributing guide"],
    },
    {
        "id": "pb-security-baseline",
        "name": "Security Baseline",
        "objective": "Establish security baseline for the project",
        "risk_level": "high",
        "stacks": ["all"],
        "phases": ["Audit dependencies", "Check secrets", "Review access controls", "Set up scanning"],
    },
    {
        "id": "pb-test-coverage",
        "name": "Test Coverage Improvement",
        "objective": "Improve test coverage to meet minimum thresholds",
        "risk_level": "medium",
        "stacks": ["all"],
        "phases": ["Measure current coverage", "Identify gaps", "Implement critical tests", "Set up coverage gates"],
    },
]


class PlaybookRecommender:
    def __init__(self, scan_result, stacks):
        self.scan = scan_result
        self.stacks = stacks

    def generate(self):
        lines = []

        lines.append("# AEOS Recommended Playbooks\n")
        lines.append(f"**Generated:** {self.scan.get('scan_timestamp', datetime.now(timezone.utc).isoformat())}")
        lines.append(f"**Project:** {self.scan.get('project_name', 'unknown')}")
        lines.append(f"**Stacks Detected:** {', '.join(s['name'] for s in self.stacks) if self.stacks else 'None'}")
        lines.append(f"**Version:** 1.0.0\n")

        if not self.stacks:
            lines.append("**No stacks detected. No playbooks can be recommended.**\n")
            return "\n".join(lines)

        # Stack-specific playbooks
        lines.append("## Stack-Specific Playbooks\n")

        for stack in self.stacks:
            stack_id = stack["id"]
            playbooks = PLAYBOOK_TEMPLATES.get(stack_id, [])
            if not playbooks:
                continue

            lines.append(f"### {stack['name']}\n")
            for pb in playbooks:
                risk_icon = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(pb["risk_level"], "⚪")
                lines.append(f"#### {risk_icon} {pb['name']} (`{pb['id']}`)")
                lines.append(f"- **Objective:** {pb['objective']}")
                lines.append(f"- **Risk Level:** {pb['risk_level']}")
                lines.append(f"- **Phases:**")
                for i, phase in enumerate(pb["phases"], 1):
                    lines.append(f"  {i}. {phase}")
                lines.append("")

        # Cross-stack playbooks
        lines.append("## Cross-Stack Playbooks\n")
        lines.append("These playbooks apply regardless of the detected stack:\n")
        for pb in CROSS_STACK_PLAYBOOKS:
            risk_icon = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(pb["risk_level"], "⚪")
            lines.append(f"### {risk_icon} {pb['name']} (`{pb['id']}`)")
            lines.append(f"- **Objective:** {pb['objective']}")
            lines.append(f"- **Risk Level:** {pb['risk_level']}")
            lines.append(f"- **Phases:**")
            for i, phase in enumerate(pb["phases"], 1):
                lines.append(f"  {i}. {phase}")
            lines.append("")

        lines.append("---\n")
        lines.append(f"*AEOS Playbook Recommendations v1.0.0 — {len(self.stacks)} stacks analyzed*")

        # Add evidence
        total_pbs = sum(len(PLAYBOOK_TEMPLATES.get(s["id"], [])) for s in self.stacks) + len(CROSS_STACK_PLAYBOOKS)
        self.scan.setdefault("evidence", []).append({
            "evidence_id": "evt-playbook-recs",
            "type": "report",
            "claim": f"Playbook recommendations generated: {total_pbs} playbooks for {len(self.stacks)} stacks",
            "reference": "recommended-playbooks.md",
            "hash": self.scan.get("scan_id", "unknown"),
            "timestamp": self.scan.get("scan_timestamp", ""),
            "verified": True,
        })

        return "\n".join(lines)
