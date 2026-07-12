$schema: "https://aeos.ai/schemas/playbook.schema.json"
$id: "perf-playbook-2"
name: "Performance Playbook 2"
version: "1.0.0"
description: "Synthetic playbook for performance testing (#2)"
steps:
  - name: "step-1"
    skill: "perf-skill-2"
    description: "Performance test step"
    inputs:
      data: "test-2"
  - name: "step-2"
    tool: "bash"
    description: "Output step"
    inputs:
      command: "echo done-2"
