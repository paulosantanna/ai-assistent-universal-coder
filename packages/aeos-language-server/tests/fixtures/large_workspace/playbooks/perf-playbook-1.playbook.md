$schema: "https://aeos.ai/schemas/playbook.schema.json"
$id: "perf-playbook-1"
name: "Performance Playbook 1"
version: "1.0.0"
description: "Synthetic playbook for performance testing (#1)"
steps:
  - name: "step-1"
    skill: "perf-skill-1"
    description: "Performance test step"
    inputs:
      data: "test-1"
  - name: "step-2"
    tool: "bash"
    description: "Output step"
    inputs:
      command: "echo done-1"
