$schema: "https://aeos.ai/schemas/playbook.schema.json"
$id: "perf-playbook-7"
name: "Performance Playbook 7"
version: "1.0.0"
description: "Synthetic playbook for performance testing (#7)"
steps:
  - name: "step-1"
    skill: "perf-skill-7"
    description: "Performance test step"
    inputs:
      data: "test-7"
  - name: "step-2"
    tool: "bash"
    description: "Output step"
    inputs:
      command: "echo done-7"
