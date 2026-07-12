$schema: "https://aeos.ai/schemas/playbook.schema.json"
$id: "perf-playbook-10"
name: "Performance Playbook 10"
version: "1.0.0"
description: "Synthetic playbook for performance testing (#10)"
steps:
  - name: "step-1"
    skill: "perf-skill-10"
    description: "Performance test step"
    inputs:
      data: "test-10"
  - name: "step-2"
    tool: "bash"
    description: "Output step"
    inputs:
      command: "echo done-10"
