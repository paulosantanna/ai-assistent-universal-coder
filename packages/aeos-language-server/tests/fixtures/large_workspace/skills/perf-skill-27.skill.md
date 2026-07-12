$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "perf-skill-27"
name: "Performance Skill 27"
version: "1.0.0"
description: "Synthetic skill for performance testing (#27)"
tools:
  - name: "tool-27"
    tool_type: "bash"
    description: "Performance test tool"
    config:
      command_template: "echo perf-test-27"
