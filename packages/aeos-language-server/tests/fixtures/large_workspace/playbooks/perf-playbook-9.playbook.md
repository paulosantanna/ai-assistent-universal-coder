$schema: "https://aeos.ai/schemas/playbook.schema.json"
$id: "perf-playbook-9"
name: "Performance Playbook 9"
version: "1.0.0"
description: "Synthetic playbook for performance testing (#9)"
steps:
  - name: "step-1"
    skill: "perf-skill-9"
    description: "Performance test step"
    inputs:
      data: "test-9"
  - name: "step-2"
    tool: "bash"
    description: "Output step"
    inputs:
      command: "echo done-9"
