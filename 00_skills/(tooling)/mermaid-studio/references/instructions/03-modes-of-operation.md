<!-- Package: 00_skills/(tooling)/mermaid-studio; relative command/resource examples resolve from that package or workspace root. -->

## Modes of Operation

This skill operates in three modes based on user intent:

| Mode       | Trigger                                           | What happens               |
| ---------- | ------------------------------------------------- | -------------------------- |
| **Create** | "draw a diagram of...", "visualize my..."         | Generates .mmd code only   |
| **Render** | "render this mermaid", "convert to SVG/PNG/ASCII" | Renders existing .mmd      |
| **Full**   | "create and render...", ambiguous requests        | Create → Validate → Render |

Default to **Full** mode when intent is unclear.
