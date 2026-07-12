---
$schema: "https://aeos.ai/schemas/playbook.schema.json"
$id: "deploy-playbook"
name: "Deploy Playbook"
version: "1.0.0"
description: "Safe deployment workflow that builds, tests, stages, and deploys with approval gates at each critical transition."
author: "AEOS LSP Team"
inputs:
  required:
    - environment
    - version
  properties:
    environment:
      type: string
      description: "Target deployment environment"
      enum:
        - "development"
        - "staging"
        - "production"
    version:
      type: string
      description: "Semantic version to deploy"
      pattern: "^\\d+\\.\\d+\\.\\d+$"
    dry_run:
      type: boolean
      description: "Simulate deployment without changes"
      default: true
variables:
  build_status: ""
  test_results: ""
  deploy_output: ""
config:
  default_timeout: 300000
  max_concurrent_steps: 2
steps:
  - name: "validate-inputs"
    tool: "bash"
    description: "Validate deployment inputs and prerequisites"
    inputs:
      command: "node scripts/validate-deploy.js --env {{inputs.environment}} --version {{inputs.version}}"
    timeout: 30000

  - name: "build-artifacts"
    tool: "bash"
    description: "Build deployable artifacts"
    inputs:
      command: "npm run build -- --env {{inputs.environment}} --version {{inputs.version}}"
    outputs:
      build_output: "$.stdout"
    conditions:
      run_if: "steps.validate-inputs.exit_code == 0"
    rollback:
      tool: "bash"
      description: "Clean up build artifacts on failure"
      inputs:
        command: "npm run clean -- --env {{inputs.environment}}"
    timeout: 120000

  - name: "run-tests"
    tool: "bash"
    description: "Execute test suite before deployment"
    inputs:
      command: "npm run test:ci -- --coverage"
    outputs:
      test_output: "$.stdout"
    conditions:
      on_failure: "notify-failure"
    timeout: 180000

  - name: "stage-approval"
    description: "Require deployment approval for staging or production targets"
    approval:
      required: true
      prompt: "Deploy version {{inputs.version}} to {{inputs.environment}}?"
      timeout_ms: 600000
      auto_approve_if: "inputs.environment == 'development' || inputs.dry_run == true"
    conditions:
      run_unless: "inputs.dry_run == true"

  - name: "deploy"
    skill: "skill-deployer"
    description: "Execute deployment to target environment"
    inputs:
      environment: "{{inputs.environment}}"
      version: "{{inputs.version}}"
      artifacts_path: "{{steps.build-artifacts.build_output}}"
    outputs:
      deploy_output: "$.result"
    conditions:
      run_if: "steps.stage-approval.approved == true || inputs.dry_run == true"
    rollback:
      skill: "skill-deployer"
      description: "Rollback to previous version"
      inputs:
        action: "rollback"
        environment: "{{inputs.environment}}"
        version: "{{inputs.version}}"

  - name: "verify-deployment"
    tool: "bash"
    description: "Verify deployment health and smoke tests"
    inputs:
      command: "node scripts/verify-deploy.js --env {{inputs.environment}} --version {{inputs.version}}"
    timeout: 60000

  - name: "notify-failure"
    tool: "bash"
    description: "Send failure notification"
    inputs:
      command: "echo 'Deployment failed for version {{inputs.version}} to {{inputs.environment}}'"

  - name: "cleanup"
    tool: "bash"
    description: "Post-deployment cleanup"
    inputs:
      command: "npm run cleanup -- --env {{inputs.environment}}"
    rollback:
      tool: "bash"
      description: "Restore previous deployment state"
      inputs:
        command: "npm run restore -- --env {{inputs.environment}}"

outputs:
  properties:
    deploy_output:
      type: object
      description: "Deployment result"
    test_results:
      type: object
      description: "Test execution results"
dependencies:
  skills:
    - "skill-deployer"
  playbooks: []
  agents: []
---

# Deploy Playbook

Safe, gated deployment workflow with approval checkpoints and
automated rollback capabilities across all environments.
