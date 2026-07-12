$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "perf-skill-7"
name: "Performance Skill 7"
version: "1.0.0"
description: "Synthetic skill for performance testing (#7)"
tools:
  - name: "tool-7"
    tool_type: "bash"
    description: "Performance test tool"
    config:
      command_template: "echo perf-test-7"
