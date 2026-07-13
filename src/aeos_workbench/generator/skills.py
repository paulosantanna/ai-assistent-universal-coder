"""Skill Generator - produces skills based on detected stacks."""

from datetime import datetime, timezone


SKILL_TEMPLATES = {
    "java-spring": [
        {
            "skill_id": "skill-java-test",
            "name": "Java Unit Test Creation",
            "description": "Create JUnit 5 unit tests for Java classes",
            "objective": "Ensure code coverage with JUnit 5 tests",
            "steps": [
                "Identify class under test",
                "Create test class with JUnit 5",
                "Implement test methods (given/when/then)",
                "Add assertions for edge cases",
                "Run tests with mvn test or gradle test",
            ],
            "evidence_requirements": ["code", "test", "command"],
        },
        {
            "skill_id": "skill-spring-rest",
            "name": "Spring REST Controller Creation",
            "description": "Create a REST controller following Spring Boot best practices",
            "objective": "Implement RESTful endpoints with Spring Boot",
            "steps": [
                "Define REST controller class with @RestController",
                "Implement endpoint methods with proper HTTP mappings",
                "Add request validation with @Valid",
                "Implement error handling with @ControllerAdvice",
                "Document with OpenAPI annotations",
            ],
            "evidence_requirements": ["code", "test"],
        },
    ],
    "python-fastapi": [
        {
            "skill_id": "skill-fastapi-endpoint",
            "name": "FastAPI Endpoint Creation",
            "description": "Create a FastAPI endpoint with Pydantic models",
            "objective": "Implement FastAPI API endpoints",
            "steps": [
                "Define Pydantic models for request/response",
                "Create router with APIRouter",
                "Implement endpoint with type validation",
                "Add dependency injection",
                "Test with pytest and httpx",
            ],
            "evidence_requirements": ["code", "test"],
        },
    ],
    "python-ai-rag": [
        {
            "skill_id": "skill-rag-pipeline",
            "name": "RAG Pipeline Implementation",
            "description": "Implement a retrieval-augmented generation pipeline",
            "objective": "Create a RAG pipeline with vector store and LLM",
            "steps": [
                "Initialize embedding model",
                "Set up vector store (Chroma/Pinecone/FAISS)",
                "Implement document chunking strategy",
                "Create retrieval chain with LangChain/LlamaIndex",
                "Add prompt template with context injection",
                "Test retrieval quality and latency",
            ],
            "evidence_requirements": ["code", "test", "benchmark"],
        },
    ],
    "typescript-react": [
        {
            "skill_id": "skill-react-component",
            "name": "React Component Creation",
            "description": "Create a React component with TypeScript",
            "objective": "Implement a reusable React component",
            "steps": [
                "Define component props interface",
                "Implement component with React hooks",
                "Add unit tests with React Testing Library",
                "Ensure accessibility (ARIA attributes)",
            ],
            "evidence_requirements": ["code", "test"],
        },
    ],
    "fullstack-docker": [
        {
            "skill_id": "skill-docker-multistage",
            "name": "Docker Multi-Stage Build",
            "description": "Create optimized multi-stage Docker build",
            "objective": "Reduce image size with multi-stage builds",
            "steps": [
                "Identify build and runtime dependencies",
                "Create build stage with SDK image",
                "Create runtime stage with slim image",
                "Copy artifacts from build stage",
                "Test image with docker scan",
            ],
            "evidence_requirements": ["code", "command", "config"],
        },
    ],
}

COMMON_SKILLS = [
    {
        "skill_id": "skill-git-workflow",
        "name": "Git Workflow Best Practices",
        "description": "Apply git workflow best practices for the project",
        "objective": "Maintain clean git history and collaboration workflow",
        "steps": [
            "Define branching strategy (GitFlow/Trunk-based)",
            "Set up branch protection rules",
            "Create commit message convention",
            "Configure .gitignore",
        ],
        "evidence_requirements": ["config", "command"],
    },
    {
        "skill_id": "skill-code-review",
        "name": "Code Review Checklist",
        "description": "Run code review checklist before merging",
        "objective": "Ensure code quality before merge",
        "steps": [
            "Check for secrets in code",
            "Verify tests pass",
            "Review diff for logic errors",
            "Check documentation is updated",
            "Verify no breaking changes",
        ],
        "evidence_requirements": ["diff", "code"],
    },
]


class SkillGenerator:
    def __init__(self, scan_result, stacks):
        self.scan = scan_result
        self.stacks = stacks

    def generate(self):
        skills = []

        for stack in self.stacks:
            stack_id = stack["id"]
            templates = SKILL_TEMPLATES.get(stack_id, [])
            for tmpl in templates:
                content = self._render_skill(tmpl, stack)
                skills.append({
                    "skill_id": tmpl["skill_id"],
                    "stack": stack_id,
                    "name": tmpl["name"],
                    "content": content,
                })

        # Add common skills (for first stack or if no stacks)
        if self.stacks:
            stack = self.stacks[0]
        else:
            stack = {"name": "Generic", "id": "generic", "confidence": 0}

        for tmpl in COMMON_SKILLS:
            content = self._render_skill(tmpl, stack)
            skills.append({
                "skill_id": tmpl["skill_id"],
                "stack": "common",
                "name": tmpl["name"],
                "content": content,
            })

        # Add evidence
        self.scan.setdefault("evidence", []).append({
            "evidence_id": "evt-skills-generated",
            "type": "report",
            "claim": f"{len(skills)} skills generated for {len(self.stacks)} stacks",
            "reference": "skills/",
            "hash": self.scan.get("scan_id", "unknown"),
            "timestamp": self.scan.get("scan_timestamp", ""),
            "verified": True,
        })

        return skills

    def _render_skill(self, tmpl, stack):
        lines = []
        lines.append(f"# {tmpl['name']}\n")
        lines.append(f"**Skill ID:** `{tmpl['skill_id']}`")
        lines.append(f"**Stack:** {stack.get('name', 'Generic')}")
        lines.append(f"**Description:** {tmpl['description']}")
        lines.append(f"**Objective:** {tmpl['objective']}\n")
        lines.append("## Steps\n")
        for i, step in enumerate(tmpl["steps"], 1):
            lines.append(f"{i}. {step}")
        lines.append("")
        lines.append("## Evidence Requirements\n")
        for req in tmpl["evidence_requirements"]:
            lines.append(f"- `{req}`")
        lines.append("")
        lines.append("## Preconditions\n")
        lines.append("- Stack must be detected and verified")
        lines.append("- Agent must have appropriate permissions")
        lines.append("- Target files must exist and be writable\n")
        lines.append("## Postconditions\n")
        lines.append("- Steps executed successfully")
        lines.append("- Evidence collected and registered")
        lines.append("- Judge evaluation completed\n")
        lines.append("---")
        lines.append(f"*Generated by AEOS Skill Factory — {datetime.now(timezone.utc).isoformat()}*")
        return "\n".join(lines)
