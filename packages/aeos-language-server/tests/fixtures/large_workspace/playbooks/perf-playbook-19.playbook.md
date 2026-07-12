$schema: "https://aeos.ai/schemas/playbook.schema.json"
$id: "perf-playbook-19"
name: "Performance Playbook 19"
version: "1.0.0"
description: "Synthetic playbook for performance testing (#19)"
steps:
  - name: "step-1"
    skill: "perf-skill-19"
    description: "Performance test step"
    inputs:
      data: "test-19"
  - name: "step-2"
    tool: "bash"
    description: "Output step"
    inputs:
      command: "echo done-19"
