"""Agent Registry - agent specifications and lifecycle management."""

import json
import uuid
from datetime import datetime, timezone


AGENT_SPECS = {
    "root": {
        "agent_id": "agent-root-001",
        "role": "root",
        "name": "Root Agent",
        "version": "1.0.0",
        "objective": "Orchestrate and decompose user requests into specialist tasks",
        "scope": ["all"],
        "max_subagents": 7,
        "allowed_tools": ["kernel.*", "scheduler.*", "policy.*", "agent.*"],
        "forbidden_actions": ["destructive", "bypass_kernel"],
        "evidence_requirements": ["command"],
        "contract_version": "1.0.0",
    },
    "architect": {
        "agent_id": "agent-arch-001",
        "role": "architect",
        "name": "Architecture Agent",
        "version": "1.0.0",
        "objective": "Analyze architecture, design patterns, and technology decisions",
        "scope": ["architecture", "design", "tech-debt"],
        "max_subagents": 3,
        "allowed_tools": ["tool.fs.read", "tool.fs.search", "tool.git.log", "tool.ai.analyze"],
        "forbidden_actions": ["write_code", "modify_production"],
        "evidence_requirements": ["code", "config", "report"],
        "contract_version": "1.0.0",
    },
    "coder": {
        "agent_id": "agent-coder-001",
        "role": "coder",
        "name": "Implementation Agent",
        "version": "1.0.0",
        "objective": "Write, refactor, and optimize source code",
        "scope": ["implementation", "refactoring"],
        "max_subagents": 3,
        "allowed_tools": ["tool.fs.read", "tool.fs.write", "tool.fs.edit", "tool.git.diff"],
        "forbidden_actions": ["delete_production", "modify_security"],
        "evidence_requirements": ["code", "test", "diff"],
        "contract_version": "1.0.0",
    },
    "tester": {
        "agent_id": "agent-tester-001",
        "role": "tester",
        "name": "Test Agent",
        "version": "1.0.0",
        "objective": "Create and execute tests, measure coverage",
        "scope": ["testing", "quality"],
        "max_subagents": 2,
        "allowed_tools": ["tool.fs.read", "tool.process.run", "tool.ai.analyze"],
        "forbidden_actions": ["modify_production_code"],
        "evidence_requirements": ["test", "code"],
        "contract_version": "1.0.0",
    },
    "security": {
        "agent_id": "agent-sec-001",
        "role": "security",
        "name": "Security Agent",
        "version": "1.0.0",
        "objective": "Audit security, detect vulnerabilities, enforce policies",
        "scope": ["security", "compliance"],
        "max_subagents": 2,
        "allowed_tools": ["tool.fs.read", "tool.fs.search", "tool.ai.analyze", "tool.security.*"],
        "forbidden_actions": ["bypass_security", "disable_audit"],
        "evidence_requirements": ["security", "config", "report"],
        "contract_version": "1.0.0",
    },
    "devops": {
        "agent_id": "agent-devops-001",
        "role": "devops",
        "name": "DevOps Agent",
        "version": "1.0.0",
        "objective": "Manage infrastructure, CI/CD, and deployment",
        "scope": ["infrastructure", "ci-cd"],
        "max_subagents": 2,
        "allowed_tools": ["tool.fs.read", "tool.process.run", "tool.git.*"],
        "forbidden_actions": ["modify_production_without_approval"],
        "evidence_requirements": ["config", "command"],
        "contract_version": "1.0.0",
    },
    "documenter": {
        "agent_id": "agent-doc-001",
        "role": "documenter",
        "name": "Documentation Agent",
        "version": "1.0.0",
        "objective": "Generate and maintain project documentation",
        "scope": ["documentation"],
        "max_subagents": 1,
        "allowed_tools": ["tool.fs.read", "tool.fs.write"],
        "forbidden_actions": ["modify_source_code", "modify_config"],
        "evidence_requirements": ["code"],
        "contract_version": "1.0.0",
    },
    "judge": {
        "agent_id": "agent-judge-001",
        "role": "judge",
        "name": "Judge Agent",
        "version": "1.0.0",
        "objective": "Evaluate evidence, score results, block or approve",
        "scope": ["evaluation"],
        "max_subagents": 0,
        "allowed_tools": ["tool.fs.read", "tool.evidence.*", "tool.judge.*"],
        "forbidden_actions": ["implement_changes", "modify_evidence"],
        "evidence_requirements": ["all"],
        "contract_version": "1.0.0",
        "independence": "strict",
        "cannot_be_same_as_implementer": True,
    },
}


class AgentRegistry:
    def __init__(self, storage_dir=None):
        self.storage_dir = storage_dir
        self._agents = {}

    def register(self, spec):
        agent_id = spec.get("agent_id", "agent-" + uuid.uuid4().hex[:8])
        entry = {
            "agent_id": agent_id,
            "status": "registered",
            "spec": spec,
            "created": datetime.now(timezone.utc).isoformat(),
        }
        self._agents[agent_id] = entry
        return entry

    def get(self, agent_id):
        return self._agents.get(agent_id)

    def list_by_role(self, role):
        return [a for a in self._agents.values() if a["spec"].get("role") == role]

    def all(self):
        return list(self._agents.values())

    def load_defaults(self):
        for spec in AGENT_SPECS.values():
            self.register(spec)

    def to_dict(self):
        result = {}
        for aid, entry in self._agents.items():
            result[aid] = {
                "agent_id": aid,
                "role": entry["spec"]["role"],
                "status": entry["status"],
                "objective": entry["spec"]["objective"],
                "scope": entry["spec"]["scope"],
            }
        return result
