$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "perf-skill-36"
name: "Performance Skill 36"
version: "1.0.0"
description: "Synthetic skill for performance testing (#36)"
tools:
  - name: "tool-36"
    tool_type: "bash"
    description: "Performance test tool"
    config:
      command_template: "echo perf-test-36"
