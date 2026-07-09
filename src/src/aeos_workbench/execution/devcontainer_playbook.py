"""Devcontainer Generation Playbook — generates devcontainer files in sandbox only."""

import json
from datetime import datetime, timezone
from pathlib import Path

from aeos_workbench.scanner.scanner import ProjectScanner
from aeos_workbench.stack_detector.detector import StackDetector


class DevcontainerPlaybook:
    def __init__(self, sandbox_writer, rollback_manager, step_engine, execution_id: str):
        self.sandbox_writer = sandbox_writer
        self.rollback_manager = rollback_manager
        self.step_engine = step_engine
        self.execution_id = execution_id
        self.generated_artifacts: list[dict] = []
        self.risks: list[str] = []

    def execute(self, target_path: Path) -> dict:
        step_id = self.step_engine.register_step({
            "step_id": "devcontainer-generation",
            "skill": "architecture-mapper",
            "status": "running",
            "inputs": {"target_path": str(target_path)},
            "outputs": {},
            "evidence": [],
            "permission_decisions": [],
            "risks": [],
            "errors": [],
        })

        scanner = ProjectScanner(target_path)
        scan_result = scanner.scan()
        detector = StackDetector(scan_result)
        stacks = detector.detect()

        self.step_engine.update_step(step_id, {
            "status": "completed",
            "outputs": {
                "total_files": scan_result.get("total_files", 0),
                "stacks": [s.get("name", "?") for s in stacks],
            },
            "evidence": [
                {"type": "scan", "files_found": scan_result.get("total_files", 0)}
            ],
        })
        self.step_engine.save_all()

        self._generate_devcontainer_json(stacks)
        self._generate_dockerfile(stacks)
        self._generate_docker_compose(stacks)
        self._generate_readme(stacks)

        return {
            "generated_artifacts": self.generated_artifacts,
            "risks": self.risks,
        }

    def _write_artifact(self, relative_path: str, content: str, artifact_type: str = "devcontainer"):
        sandbox_path = self.sandbox_writer.write(relative_path, content)
        self.rollback_manager.register_generated_file(
            file_path=sandbox_path,
            sandbox_relative=relative_path,
            content_preview=content[:100],
        )
        self.generated_artifacts.append({
            "name": relative_path.split("/")[-1],
            "path": str(sandbox_path),
            "type": artifact_type,
            "size": len(content.encode("utf-8")),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        return sandbox_path

    def _generate_devcontainer(self, stacks):
        features = {}
        stack_names = [s.get("name", "") for s in stacks]

        if any("Python" in s for s in stack_names):
            features["ghcr.io/devcontainers/features/python:1"] = {}
        if any("TypeScript" in s or "Node" in s for s in stack_names):
            features["ghcr.io/devcontainers/features/node:1"] = {}
        if any("Java" in s for s in stack_names):
            features["ghcr.io/devcontainers/features/java:1"] = {"version": "21"}
        if any("Go" in s for s in stack_names):
            features["ghcr.io/devcontainers/features/go:1"] = {}
        if any("Rust" in s for s in stack_names):
            features["ghcr.io/devcontainers/features/rust:1"] = {}
        if any("Docker" in s for s in stack_names):
            features["ghcr.io/devcontainers/features/docker-in-docker:2"] = {}
        if any("Terraform" in s for s in stack_names):
            features["ghcr.io/devcontainers/features/terraform:1"] = {}
        if any("Kubernetes" in s for s in stack_names):
            features["ghcr.io/devcontainers/features/kubectl-helm-minikube:1"] = {}

        devcontainer = {
            "name": "AEOS Generated Devcontainer",
            "image": self._select_base_image(stacks),
            "features": features,
            "customizations": {
                "vscode": {
                    "extensions": self._select_extensions(stacks),
                    "settings": {
                        "terminal.integrated.defaultProfile.linux": "bash",
                        "files.autoSave": "onFocusChange",
                    },
                },
            },
            "postCreateCommand": self._post_create_command(stacks),
            "remoteUser": "vscode",
            "mounts": [
                "source=/var/run/docker.sock,target=/var/run/docker.sock,type=bind",
            ],
        }

        self._write_artifact(
            "devcontainer/devcontainer.json",
            json.dumps(devcontainer, indent=2, ensure_ascii=False),
        )

    def _select_base_image(self, stacks):
        stack_names = [s.get("name", "") for s in stacks]
        if any("Python" in s for s in stack_names):
            return "mcr.microsoft.com/devcontainers/python:3.12"
        if any("Java" in s for s in stack_names):
            return "mcr.microsoft.com/devcontainers/java:21"
        if any("TypeScript" in s for s in stack_names):
            return "mcr.microsoft.com/devcontainers/typescript-node:22"
        if any("Go" in s for s in stack_names):
            return "mcr.microsoft.com/devcontainers/go:1.23"
        if any("Rust" in s for s in stack_names):
            return "mcr.microsoft.com/devcontainers/rust:1.80"
        if any(".NET" in s for s in stack_names):
            return "mcr.microsoft.com/devcontainers/dotnet:9.0"
        return "mcr.microsoft.com/devcontainers/universal:2"

    def _select_extensions(self, stacks):
        extensions = []
        stack_names = [s.get("name", "") for s in stacks]
        if any("Python" in s for s in stack_names):
            extensions.extend(["ms-python.python", "ms-python.vscode-pylance", "charliermarsh.ruff"])
        if any("Java" in s for s in stack_names):
            extensions.extend(["vscjava.vscode-java-pack", "vscjava.vscode-spring-initializr"])
        if any("TypeScript" in s or "React" in s or "Vue" in s for s in stack_names):
            extensions.extend(["dbaeumer.vscode-eslint", "esbenp.prettier-vscode"])
        if any("Go" in s for s in stack_names):
            extensions.extend(["golang.go"])
        if any("Rust" in s for s in stack_names):
            extensions.extend(["rust-lang.rust-analyzer"])
        if any("Terraform" in s for s in stack_names):
            extensions.extend(["hashicorp.terraform"])
        if any("Docker" in s for s in stack_names):
            extensions.extend(["ms-azuretools.vscode-docker"])
        if any("Kubernetes" in s for s in stack_names):
            extensions.extend(["ms-kubernetes-tools.vscode-kubernetes-tools"])
        return extensions

    def _post_create_command(self, stacks):
        commands = []
        stack_names = [s.get("name", "") for s in stacks]
        if any("Python" in s for s in stack_names):
            commands.append("pip install --upgrade pip")
        if any("TypeScript" in s or "Node" in s for s in stack_names):
            commands.append("npm install -g npm@latest")
        return commands or ["echo 'AEOS devcontainer ready'"]

    def _generate_dockerfile(self, stacks):
        stack_names = [s.get("name", "") for s in stacks]
        dockerfile = f"""# AEOS Generated Dockerfile
# Based on detected stacks: {', '.join(stack_names) if stack_names else 'detected stacks'}

FROM {self._select_base_image(stacks)}

# Install additional tools
"""
        if any("Python" in s for s in stack_names):
            dockerfile += "RUN pip install --no-cache-dir ruff mypy black\n"
        if any("TypeScript" in s or "Node" in s for s in stack_names):
            dockerfile += "RUN npm install -g typescript eslint prettier\n"

        dockerfile += """
# Set environment variables
ENV DEVCONTAINER=true

# Default command
CMD ["sleep", "infinity"]
"""
        self._write_artifact("devcontainer/Dockerfile", dockerfile)

    def _generate_docker_compose(self, stacks):
        stack_names = [s.get("name", "") for s in stacks]
        compose = {
            "version": "3.8",
            "services": {
                "devcontainer": {
                    "build": {
                        "context": ".",
                        "dockerfile": "Dockerfile",
                    },
                    "volumes": [
                        "..:/workspace:cached",
                    ],
                    "environment": {
                        "DEVCONTAINER": "true",
                    },
                    "command": ["sleep", "infinity"],
                },
            },
        }

        if any("Python" in s for s in stack_names):
            compose["services"]["devcontainer"]["environment"].update({
                "PYTHONUNBUFFERED": "1",
                "PYTHONDONTWRITEBYTECODE": "1",
            })

        if any("Database" in s or "db" in s.get("frameworks", []) for s in stacks):
            compose["services"]["db"] = {
                "image": "postgres:16-alpine",
                "environment": {
                    "POSTGRES_USER": "vscode",
                    "POSTGRES_PASSWORD": "vscode",
                    "POSTGRES_DB": "app",
                },
                "ports": ["5432:5432"],
                "volumes": ["postgres-data:/var/lib/postgresql/data"],
            }
            compose["volumes"] = {"postgres-data": {}}

        self._write_artifact(
            "devcontainer/docker-compose.generated.yml",
            json.dumps(compose, indent=2, ensure_ascii=False),
        )

    def _generate_readme(self, stacks):
        stack_names = [s.get("name", "") for s in stacks]
        content = f"""# AEOS Generated Devcontainer

> **Auto-generated by AEOS v0.2**
> **Date:** {datetime.now(timezone.utc).isoformat()}

## Detected Stacks

{chr(10).join(f'- {s}' for s in stack_names) if stack_names else '- (none detected)'}

## Usage

1. Open the project in VS Code
2. When prompted, "Reopen in Container"
3. Or run: `Dev Containers: Reopen in Container`

## Included Tools

- Base image: {self._select_base_image(stacks)}
- Extensions configured for detected stacks
- Docker-in-Docker for containerized development

## Notes

- All generated files are in `.aeos/sandbox/{self.execution_id}/devcontainer/`
- Copy to `.devcontainer/` to activate: `cp -r .aeos/sandbox/{self.execution_id}/devcontainer/ .devcontainer/`
- No real `.devcontainer` directory was modified by AEOS
"""
        self._write_artifact("devcontainer/README.generated.md", content)