$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "perf-skill-17"
name: "Performance Skill 17"
version: "1.0.0"
description: "Synthetic skill for performance testing (#17)"
tools:
  - name: "tool-17"
    tool_type: "bash"
    description: "Performance test tool"
    config:
      command_template: "echo perf-test-17"
