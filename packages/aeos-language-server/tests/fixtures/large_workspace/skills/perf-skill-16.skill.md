$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "perf-skill-16"
name: "Performance Skill 16"
version: "1.0.0"
description: "Synthetic skill for performance testing (#16)"
tools:
  - name: "tool-16"
    tool_type: "bash"
    description: "Performance test tool"
    config:
      command_template: "echo perf-test-16"
