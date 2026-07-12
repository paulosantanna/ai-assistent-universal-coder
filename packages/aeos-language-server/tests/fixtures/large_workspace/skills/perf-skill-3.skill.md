$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "perf-skill-3"
name: "Performance Skill 3"
version: "1.0.0"
description: "Synthetic skill for performance testing (#3)"
tools:
  - name: "tool-3"
    tool_type: "bash"
    description: "Performance test tool"
    config:
      command_template: "echo perf-test-3"
