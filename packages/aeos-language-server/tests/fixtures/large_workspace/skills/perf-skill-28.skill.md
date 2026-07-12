$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "perf-skill-28"
name: "Performance Skill 28"
version: "1.0.0"
description: "Synthetic skill for performance testing (#28)"
tools:
  - name: "tool-28"
    tool_type: "bash"
    description: "Performance test tool"
    config:
      command_template: "echo perf-test-28"
