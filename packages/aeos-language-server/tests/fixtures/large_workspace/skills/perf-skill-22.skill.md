$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "perf-skill-22"
name: "Performance Skill 22"
version: "1.0.0"
description: "Synthetic skill for performance testing (#22)"
tools:
  - name: "tool-22"
    tool_type: "bash"
    description: "Performance test tool"
    config:
      command_template: "echo perf-test-22"
