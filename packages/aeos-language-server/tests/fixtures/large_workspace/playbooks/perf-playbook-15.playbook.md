$schema: "https://aeos.ai/schemas/playbook.schema.json"
$id: "perf-playbook-15"
name: "Performance Playbook 15"
version: "1.0.0"
description: "Synthetic playbook for performance testing (#15)"
steps:
  - name: "step-1"
    skill: "perf-skill-15"
    description: "Performance test step"
    inputs:
      data: "test-15"
  - name: "step-2"
    tool: "bash"
    description: "Output step"
    inputs:
      command: "echo done-15"
