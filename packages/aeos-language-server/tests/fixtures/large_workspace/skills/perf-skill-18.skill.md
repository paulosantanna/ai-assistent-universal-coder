$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "perf-skill-18"
name: "Performance Skill 18"
version: "1.0.0"
description: "Synthetic skill for performance testing (#18)"
tools:
  - name: "tool-18"
    tool_type: "bash"
    description: "Performance test tool"
    config:
      command_template: "echo perf-test-18"
