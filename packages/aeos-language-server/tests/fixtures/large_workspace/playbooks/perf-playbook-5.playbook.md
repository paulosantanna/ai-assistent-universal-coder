$schema: "https://aeos.ai/schemas/playbook.schema.json"
$id: "perf-playbook-5"
name: "Performance Playbook 5"
version: "1.0.0"
description: "Synthetic playbook for performance testing (#5)"
steps:
  - name: "step-1"
    skill: "perf-skill-5"
    description: "Performance test step"
    inputs:
      data: "test-5"
  - name: "step-2"
    tool: "bash"
    description: "Output step"
    inputs:
      command: "echo done-5"
