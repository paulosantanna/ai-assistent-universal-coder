$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "perf-skill-25"
name: "Performance Skill 25"
version: "1.0.0"
description: "Synthetic skill for performance testing (#25)"
tools:
  - name: "tool-25"
    tool_type: "bash"
    description: "Performance test tool"
    config:
      command_template: "echo perf-test-25"
