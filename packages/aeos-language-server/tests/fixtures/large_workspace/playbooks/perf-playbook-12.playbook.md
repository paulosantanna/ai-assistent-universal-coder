$schema: "https://aeos.ai/schemas/playbook.schema.json"
$id: "perf-playbook-12"
name: "Performance Playbook 12"
version: "1.0.0"
description: "Synthetic playbook for performance testing (#12)"
steps:
  - name: "step-1"
    skill: "perf-skill-12"
    description: "Performance test step"
    inputs:
      data: "test-12"
  - name: "step-2"
    tool: "bash"
    description: "Output step"
    inputs:
      command: "echo done-12"
