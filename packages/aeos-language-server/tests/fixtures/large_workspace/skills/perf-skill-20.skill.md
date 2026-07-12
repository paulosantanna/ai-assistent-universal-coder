$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "perf-skill-20"
name: "Performance Skill 20"
version: "1.0.0"
description: "Synthetic skill for performance testing (#20)"
tools:
  - name: "tool-20"
    tool_type: "bash"
    description: "Performance test tool"
    config:
      command_template: "echo perf-test-20"
