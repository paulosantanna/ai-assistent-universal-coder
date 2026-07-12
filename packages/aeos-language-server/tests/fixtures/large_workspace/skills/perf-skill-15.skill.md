$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "perf-skill-15"
name: "Performance Skill 15"
version: "1.0.0"
description: "Synthetic skill for performance testing (#15)"
tools:
  - name: "tool-15"
    tool_type: "bash"
    description: "Performance test tool"
    config:
      command_template: "echo perf-test-15"
