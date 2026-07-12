$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "perf-skill-9"
name: "Performance Skill 9"
version: "1.0.0"
description: "Synthetic skill for performance testing (#9)"
tools:
  - name: "tool-9"
    tool_type: "bash"
    description: "Performance test tool"
    config:
      command_template: "echo perf-test-9"
