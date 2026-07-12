$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "perf-skill-11"
name: "Performance Skill 11"
version: "1.0.0"
description: "Synthetic skill for performance testing (#11)"
tools:
  - name: "tool-11"
    tool_type: "bash"
    description: "Performance test tool"
    config:
      command_template: "echo perf-test-11"
