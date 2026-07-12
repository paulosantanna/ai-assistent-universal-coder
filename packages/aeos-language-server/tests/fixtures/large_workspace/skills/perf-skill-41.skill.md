$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "perf-skill-41"
name: "Performance Skill 41"
version: "1.0.0"
description: "Synthetic skill for performance testing (#41)"
tools:
  - name: "tool-41"
    tool_type: "bash"
    description: "Performance test tool"
    config:
      command_template: "echo perf-test-41"
