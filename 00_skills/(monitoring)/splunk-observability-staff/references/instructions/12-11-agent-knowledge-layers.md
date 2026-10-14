<!-- Package: 00_skills/(monitoring)/splunk-observability-staff; relative command/resource examples resolve from that package or workspace root. -->

## 11. Agent knowledge layers

Use the generated Agent and knowledge files as layered context:

- `AGENT.md` defines the autonomous role, isolation rules, subagent boundaries and handoff format.
- `references/SOURCES.md` defines official source baselines for tool-specific analysis.
- `knowledge/NEGATIVE_KNOWLEDGE.md` blocks repeated failures and unsafe shortcuts.
- `knowledge/POSITIVE_KNOWLEDGE.md` captures validated successful patterns.
- `knowledge/KNOWLEDGE.md` stores promoted domain knowledge only after evidence.
- `memory/OPEN_RISKS.md`, `memory/DECISIONS.md` and `memory/FAILURES.md` preserve operational memory.
- `knowledge/KNOWLEDGE_PROMOTION.md` governs when observations become reusable knowledge.
