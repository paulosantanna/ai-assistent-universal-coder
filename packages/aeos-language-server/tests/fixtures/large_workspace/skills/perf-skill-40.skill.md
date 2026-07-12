$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "perf-skill-40"
name: "Performance Skill 40"
version: "1.0.0"
description: "Synthetic skill for performance testing (#40)"
tools:
  - name: "tool-40"
    tool_type: "bash"
    description: "Performance test tool"
    config:
      command_template: "echo perf-test-40"
