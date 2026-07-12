---
$schema: "https://aeos.ai/schemas/playbook.schema.json"
$id: "full-ci-cd-playbook"
name: "Full CI/CD Pipeline Playbook"
version: "2.0.0"
description: "Enterprise-grade CI/CD pipeline with parallel stages, conditional branching, approval gates, evidence collection, and full rollback support."
author: "AEOS LSP Team"
inputs:
  required:
    - repository
    - branch
    - commit_sha
  properties:
    repository:
      type: string
      description: "Git repository URL"
    branch:
      type: string
      description: "Branch to build and deploy"
      pattern: "^[a-zA-Z0-9_/.-]+$"
    commit_sha:
      type: string
      description: "Full commit SHA to deploy"
      pattern: "^[a-f0-9]{40}$"
    skip_tests:
      type: boolean
      description: "Skip test execution"
      default: false
    environment:
      type: string
      description: "Target deployment environment"
      default: "development"
      enum:
        - "development"
        - "staging"
        - "production"
    dry_run:
      type: boolean
      description: "Run in dry-run mode without making changes"
      default: true
variables:
  build_artifacts: {}
  test_results: {}
  security_scan: {}
  approval_status: ""
  deploy_result: {}
  evidence_id: ""
config:
  default_timeout: 600000
  default_retry:
    max_attempts: 3
    delay_ms: 2000
    backoff_multiplier: 2.0
  max_concurrent_steps: 4
steps:
  - name: "checkout"
    tool: "bash"
    description: "Check out the repository at the specified commit"
    inputs:
      command: "git clone --depth 1 {{inputs.repository}} /workspace/build/{{inputs.commit_sha}} && cd /workspace/build/{{inputs.commit_sha}} && git checkout {{inputs.commit_sha}}"
    outputs:
      checkout_path: "$.stdout"
    timeout: 120000
    retry:
      max_attempts: 2
      delay_ms: 5000
    rollback:
      tool: "bash"
      description: "Remove checked-out repository"
      inputs:
        command: "rm -rf /workspace/build/{{inputs.commit_sha}}"

  - name: "install-dependencies"
    tool: "bash"
    description: "Install project dependencies"
    inputs:
      command: "cd /workspace/build/{{inputs.commit_sha}} && npm ci"
    outputs:
      install_log: "$.stdout"
    conditions:
      run_if: "steps.checkout.exit_code == 0"
    timeout: 180000
    retry:
      max_attempts: 3
      delay_ms: 5000
      backoff_multiplier: 3.0

  - name: "lint"
    tool: "bash"
    description: "Run linter on source code"
    inputs:
      command: "cd /workspace/build/{{inputs.commit_sha}} && npm run lint"
    conditions:
      on_failure: "lint-fix"
    timeout: 60000

  - name: "lint-fix"
    tool: "bash"
    description: "Attempt to auto-fix lint issues"
    inputs:
      command: "cd /workspace/build/{{inputs.commit_sha}} && npm run lint:fix"
    timeout: 60000

  - name: "build"
    tool: "bash"
    description: "Build the project"
    inputs:
      command: "cd /workspace/build/{{inputs.commit_sha}} && npm run build"
    outputs:
      build_output: "$.stdout"
    conditions:
      run_if: "steps.lint.exit_code == 0 || steps.lint-fix.exit_code == 0"
    timeout: 300000
    rollback:
      tool: "bash"
      description: "Clean build output"
      inputs:
        command: "cd /workspace/build/{{inputs.commit_sha}} && npm run clean"

  - name: "unit-tests"
    tool: "bash"
    description: "Run unit tests"
    inputs:
      command: "cd /workspace/build/{{inputs.commit_sha}} && npm run test:unit -- --coverage"
    outputs:
      unit_results: "$.stdout"
    conditions:
      run_unless: "inputs.skip_tests == true"
    parallel: true
    timeout: 180000

  - name: "integration-tests"
    tool: "bash"
    description: "Run integration tests"
    inputs:
      command: "cd /workspace/build/{{inputs.commit_sha}} && npm run test:integration"
    outputs:
      integration_results: "$.stdout"
    conditions:
      run_unless: "inputs.skip_tests == true"
    parallel: true
    timeout: 300000

  - name: "security-scan"
    skill: "skill-security-scanner"
    description: "Scan for security vulnerabilities"
    inputs:
      path: "/workspace/build/{{inputs.commit_sha}}"
      scan_type: "full"
      fail_on_critical: true
    outputs:
      security_report: "$.report"
    parallel: true
    timeout: 120000

  - name: "quality-gate"
    skill: "skill-quality-gate"
    description: "Check quality metrics against thresholds"
    inputs:
      coverage_path: "/workspace/build/{{inputs.commit_sha}}/coverage/lcov.info"
      min_coverage: 80
    outputs:
      quality_result: "$.passed"
    conditions:
      run_if: "steps.unit-tests.exit_code == 0"
    on_failure: "notify-quality-fail"

  - name: "approval"
    description: "Require human approval for production deployment"
    approval:
      required: true
      prompt: "Deploy commit {{inputs.commit_sha}} on branch {{inputs.branch}} to {{inputs.environment}}?"
      timeout_ms: 1800000
      auto_approve_if: "inputs.environment != 'production' || inputs.dry_run == true"
    conditions:
      run_if: "steps.quality-gate.quality_result == true"
    outputs:
      approval_status: "$.approved"

  - name: "deploy"
    skill: "skill-deployer"
    description: "Deploy to target environment"
    inputs:
      environment: "{{inputs.environment}}"
      commit_sha: "{{inputs.commit_sha}}"
      artifacts: "{{steps.build.build_output}}"
      dry_run: "{{inputs.dry_run}}"
    outputs:
      deploy_result: "$.result"
    conditions:
      run_if: "steps.approval.approved == true || inputs.dry_run == true"
    rollback:
      playbook: "rollback-playbook"
      description: "Full rollback to previous known-good state"
      inputs:
        environment: "{{inputs.environment}}"
        previous_version: "{{steps.build.build_output.previous}}"

  - name: "smoke-tests"
    tool: "bash"
    description: "Run smoke tests against deployed environment"
    inputs:
      command: "node /workspace/build/{{inputs.commit_sha}}/scripts/smoke-test.js --env {{inputs.environment}}"
    timeout: 60000

  - name: "post-deploy"
    tool: "bash"
    description: "Post-deployment tasks: tag, notify, cleanup"
    inputs:
      command: >
        git tag deploy-{{inputs.environment}}-{{inputs.commit_sha}} &&
        echo "Deployment complete" &&
        curl -X POST -H "Content-Type: application/json"
        -d '{"commit":"{{inputs.commit_sha}}","env":"{{inputs.environment}}"}'
        {{inputs.notification_url}}
    conditions:
      run_if: "steps.smoke-tests.exit_code == 0"
    rollback:
      tool: "bash"
      description: "Revert git tag on failure"
      inputs:
        command: "git tag -d deploy-{{inputs.environment}}-{{inputs.commit_sha}} || true"

  - name: "notify-quality-fail"
    tool: "bash"
    description: "Notify team about quality gate failure"
    inputs:
      command: "echo 'Quality gate failed for commit {{inputs.commit_sha}} on branch {{inputs.branch}}'"

outputs:
  properties:
    deploy_result:
      type: object
      description: "Deployment result with status and metadata"
    test_results:
      type: object
      description: "Aggregated test results"
    security_report:
      type: object
      description: "Security scan findings"
dependencies:
  skills:
    - "skill-security-scanner"
    - "skill-quality-gate"
    - "skill-deployer"
  playbooks:
    - "rollback-playbook"
  agents:
    - "full-analysis-agent"

---

# Full CI/CD Pipeline Playbook

## Pipeline Stages

1. **Checkout & Setup** — Clone repository at specified commit
2. **Dependencies** — Install npm dependencies with retry
3. **Lint** — Run linter with auto-fix capability
4. **Build** — Compile and package application
5. **Test** — Parallel unit + integration tests
6. **Security** — Parallel security vulnerability scan
7. **Quality Gate** — Enforce quality thresholds
8. **Approval** — Human-in-the-loop for production
9. **Deploy** — Deploy with rollback support
10. **Smoke Tests** — Verify deployment health
11. **Post-Deploy** — Tag, notify, and cleanup

## Rollback

The playbook defines rollback steps for every mutating operation,
ensuring the system can always be restored to a known-good state.
