$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "perf-skill-5"
name: "Performance Skill 5"
version: "1.0.0"
description: "Synthetic skill for performance testing (#5)"
tools:
  - name: "tool-5"
    tool_type: "bash"
    description: "Performance test tool"
    config:
      command_template: "echo perf-test-5"
