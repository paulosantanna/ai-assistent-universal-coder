$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "perf-skill-12"
name: "Performance Skill 12"
version: "1.0.0"
description: "Synthetic skill for performance testing (#12)"
tools:
  - name: "tool-12"
    tool_type: "bash"
    description: "Performance test tool"
    config:
      command_template: "echo perf-test-12"
