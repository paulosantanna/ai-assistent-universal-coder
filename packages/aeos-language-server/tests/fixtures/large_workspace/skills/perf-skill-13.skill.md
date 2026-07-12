$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "perf-skill-13"
name: "Performance Skill 13"
version: "1.0.0"
description: "Synthetic skill for performance testing (#13)"
tools:
  - name: "tool-13"
    tool_type: "bash"
    description: "Performance test tool"
    config:
      command_template: "echo perf-test-13"
