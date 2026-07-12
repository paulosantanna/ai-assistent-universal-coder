$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "perf-skill-43"
name: "Performance Skill 43"
version: "1.0.0"
description: "Synthetic skill for performance testing (#43)"
tools:
  - name: "tool-43"
    tool_type: "bash"
    description: "Performance test tool"
    config:
      command_template: "echo perf-test-43"
