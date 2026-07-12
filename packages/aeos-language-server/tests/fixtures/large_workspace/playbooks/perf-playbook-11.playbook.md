$schema: "https://aeos.ai/schemas/playbook.schema.json"
$id: "perf-playbook-11"
name: "Performance Playbook 11"
version: "1.0.0"
description: "Synthetic playbook for performance testing (#11)"
steps:
  - name: "step-1"
    skill: "perf-skill-11"
    description: "Performance test step"
    inputs:
      data: "test-11"
  - name: "step-2"
    tool: "bash"
    description: "Output step"
    inputs:
      command: "echo done-11"
