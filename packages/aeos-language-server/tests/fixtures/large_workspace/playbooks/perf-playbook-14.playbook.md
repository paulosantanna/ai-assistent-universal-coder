$schema: "https://aeos.ai/schemas/playbook.schema.json"
$id: "perf-playbook-14"
name: "Performance Playbook 14"
version: "1.0.0"
description: "Synthetic playbook for performance testing (#14)"
steps:
  - name: "step-1"
    skill: "perf-skill-14"
    description: "Performance test step"
    inputs:
      data: "test-14"
  - name: "step-2"
    tool: "bash"
    description: "Output step"
    inputs:
      command: "echo done-14"
