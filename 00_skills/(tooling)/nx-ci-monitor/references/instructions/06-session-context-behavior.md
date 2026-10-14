<!-- Package: 00_skills/(tooling)/nx-ci-monitor; relative command/resource examples resolve from that package or workspace root. -->

## Session Context Behavior

**Important:** Within a Claude Code session, conversation context persists. If you Ctrl+C to interrupt the monitor and re-run `/ci-monitor`, Claude remembers the previous state and may continue from where it left off.

- **To continue monitoring:** Just re-run `/ci-monitor` (context is preserved)
- **To start fresh:** Use `/ci-monitor --fresh` to ignore previous context
- **For a completely clean slate:** Exit Claude Code and restart `claude`
