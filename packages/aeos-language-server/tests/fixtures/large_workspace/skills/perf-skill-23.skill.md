$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "perf-skill-23"
name: "Performance Skill 23"
version: "1.0.0"
description: "Synthetic skill for performance testing (#23)"
tools:
  - name: "tool-23"
    tool_type: "bash"
    description: "Performance test tool"
    config:
      command_template: "echo perf-test-23"
