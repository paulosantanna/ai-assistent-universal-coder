$schema: "https://aeos.ai/schemas/playbook.schema.json"
$id: "perf-playbook-6"
name: "Performance Playbook 6"
version: "1.0.0"
description: "Synthetic playbook for performance testing (#6)"
steps:
  - name: "step-1"
    skill: "perf-skill-6"
    description: "Performance test step"
    inputs:
      data: "test-6"
  - name: "step-2"
    tool: "bash"
    description: "Output step"
    inputs:
      command: "echo done-6"
