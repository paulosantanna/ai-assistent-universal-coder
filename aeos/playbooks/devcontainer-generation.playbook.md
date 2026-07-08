# Playbook: Devcontainer Generation

## Objective

Generate a complete devcontainer.json and Docker configuration for a portable, reproducible development environment based on the detected project stack.

## Preconditions

- Workspace path exists.
- Project stack has been analyzed.
- MCPs for filesystem read/write and shell available.
- Global rules LCP loaded.

## Agents

- DevOps Agent
- Root Agent
- Judge Agent

## Skills

- repo-scanner
- architecture-mapper

## MCPs

- filesystem-readonly
- filesystem-write-sandbox
- shell-controlled

## Steps

1. Load project stack information.
2. Detect required languages, tools, and runtimes.
3. Detect Docker/Compose files already present.
4. Generate Dockerfile with appropriate base images.
5. Generate devcontainer.json with features and extensions.
6. Generate docker-compose.yml if services needed.
7. Generate post-create script for environment setup.
8. Test container configuration (validate syntax).
9. Generate devcontainer report.
10. Send outputs to Judge Agent.
11. Generate judge-report.md.

## Blocking Conditions

- Project stack not identified.
- Generated Dockerfile has syntax errors.
- Missing required tool for development.
- Incompatible base image selected.

## Outputs

- .aeos/devcontainer/Dockerfile
- .aeos/devcontainer/devcontainer.json
- .aeos/devcontainer/docker-compose.yml (if needed)
- .aeos/devcontainer/post-create.sh
- .aeos/devcontainer-report.md
- .aeos/judge-report.md
