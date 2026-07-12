$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "perf-skill-1"
name: "Performance Skill 1"
version: "1.0.0"
description: "Synthetic skill for performance testing (#1)"
tools:
  - name: "tool-1"
    tool_type: "bash"
    description: "Performance test tool"
    config:
      command_template: "echo perf-test-1"
