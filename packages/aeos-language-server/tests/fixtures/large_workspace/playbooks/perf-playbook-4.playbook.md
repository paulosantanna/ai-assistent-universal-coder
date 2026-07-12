$schema: "https://aeos.ai/schemas/playbook.schema.json"
$id: "perf-playbook-4"
name: "Performance Playbook 4"
version: "1.0.0"
description: "Synthetic playbook for performance testing (#4)"
steps:
  - name: "step-1"
    skill: "perf-skill-4"
    description: "Performance test step"
    inputs:
      data: "test-4"
  - name: "step-2"
    tool: "bash"
    description: "Output step"
    inputs:
      command: "echo done-4"
