$schema: "https://aeos.ai/schemas/playbook.schema.json"
$id: "perf-playbook-18"
name: "Performance Playbook 18"
version: "1.0.0"
description: "Synthetic playbook for performance testing (#18)"
steps:
  - name: "step-1"
    skill: "perf-skill-18"
    description: "Performance test step"
    inputs:
      data: "test-18"
  - name: "step-2"
    tool: "bash"
    description: "Output step"
    inputs:
      command: "echo done-18"
