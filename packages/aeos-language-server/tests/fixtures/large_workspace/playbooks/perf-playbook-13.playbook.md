$schema: "https://aeos.ai/schemas/playbook.schema.json"
$id: "perf-playbook-13"
name: "Performance Playbook 13"
version: "1.0.0"
description: "Synthetic playbook for performance testing (#13)"
steps:
  - name: "step-1"
    skill: "perf-skill-13"
    description: "Performance test step"
    inputs:
      data: "test-13"
  - name: "step-2"
    tool: "bash"
    description: "Output step"
    inputs:
      command: "echo done-13"
