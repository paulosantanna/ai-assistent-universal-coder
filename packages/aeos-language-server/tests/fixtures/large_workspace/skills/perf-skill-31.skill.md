$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "perf-skill-31"
name: "Performance Skill 31"
version: "1.0.0"
description: "Synthetic skill for performance testing (#31)"
tools:
  - name: "tool-31"
    tool_type: "bash"
    description: "Performance test tool"
    config:
      command_template: "echo perf-test-31"
