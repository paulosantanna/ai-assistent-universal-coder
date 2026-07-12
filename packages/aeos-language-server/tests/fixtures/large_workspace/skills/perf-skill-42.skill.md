$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "perf-skill-42"
name: "Performance Skill 42"
version: "1.0.0"
description: "Synthetic skill for performance testing (#42)"
tools:
  - name: "tool-42"
    tool_type: "bash"
    description: "Performance test tool"
    config:
      command_template: "echo perf-test-42"
