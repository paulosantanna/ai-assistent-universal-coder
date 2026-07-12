$schema: "https://aeos.ai/schemas/playbook.schema.json"
$id: "perf-playbook-16"
name: "Performance Playbook 16"
version: "1.0.0"
description: "Synthetic playbook for performance testing (#16)"
steps:
  - name: "step-1"
    skill: "perf-skill-16"
    description: "Performance test step"
    inputs:
      data: "test-16"
  - name: "step-2"
    tool: "bash"
    description: "Output step"
    inputs:
      command: "echo done-16"
