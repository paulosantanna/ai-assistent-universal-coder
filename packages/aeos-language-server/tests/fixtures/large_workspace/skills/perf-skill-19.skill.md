$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "perf-skill-19"
name: "Performance Skill 19"
version: "1.0.0"
description: "Synthetic skill for performance testing (#19)"
tools:
  - name: "tool-19"
    tool_type: "bash"
    description: "Performance test tool"
    config:
      command_template: "echo perf-test-19"
