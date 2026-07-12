$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "perf-skill-14"
name: "Performance Skill 14"
version: "1.0.0"
description: "Synthetic skill for performance testing (#14)"
tools:
  - name: "tool-14"
    tool_type: "bash"
    description: "Performance test tool"
    config:
      command_template: "echo perf-test-14"
