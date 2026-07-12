$schema: "https://aeos.ai/schemas/playbook.schema.json"
$id: "perf-playbook-8"
name: "Performance Playbook 8"
version: "1.0.0"
description: "Synthetic playbook for performance testing (#8)"
steps:
  - name: "step-1"
    skill: "perf-skill-8"
    description: "Performance test step"
    inputs:
      data: "test-8"
  - name: "step-2"
    tool: "bash"
    description: "Output step"
    inputs:
      command: "echo done-8"
