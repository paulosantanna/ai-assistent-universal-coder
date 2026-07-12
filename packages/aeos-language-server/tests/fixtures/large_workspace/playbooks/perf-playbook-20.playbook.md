$schema: "https://aeos.ai/schemas/playbook.schema.json"
$id: "perf-playbook-20"
name: "Performance Playbook 20"
version: "1.0.0"
description: "Synthetic playbook for performance testing (#20)"
steps:
  - name: "step-1"
    skill: "perf-skill-20"
    description: "Performance test step"
    inputs:
      data: "test-20"
  - name: "step-2"
    tool: "bash"
    description: "Output step"
    inputs:
      command: "echo done-20"
