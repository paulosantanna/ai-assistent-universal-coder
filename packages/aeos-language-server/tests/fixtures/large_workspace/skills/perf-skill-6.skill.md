$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "perf-skill-6"
name: "Performance Skill 6"
version: "1.0.0"
description: "Synthetic skill for performance testing (#6)"
tools:
  - name: "tool-6"
    tool_type: "bash"
    description: "Performance test tool"
    config:
      command_template: "echo perf-test-6"
