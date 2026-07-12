$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "perf-skill-26"
name: "Performance Skill 26"
version: "1.0.0"
description: "Synthetic skill for performance testing (#26)"
tools:
  - name: "tool-26"
    tool_type: "bash"
    description: "Performance test tool"
    config:
      command_template: "echo perf-test-26"
