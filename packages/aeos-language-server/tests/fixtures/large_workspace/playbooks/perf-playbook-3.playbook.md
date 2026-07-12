$schema: "https://aeos.ai/schemas/playbook.schema.json"
$id: "perf-playbook-3"
name: "Performance Playbook 3"
version: "1.0.0"
description: "Synthetic playbook for performance testing (#3)"
steps:
  - name: "step-1"
    skill: "perf-skill-3"
    description: "Performance test step"
    inputs:
      data: "test-3"
  - name: "step-2"
    tool: "bash"
    description: "Output step"
    inputs:
      command: "echo done-3"
