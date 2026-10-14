<!-- Package: 00_skills/(cloud)/kubernetes-code-context-mapper; relative command/resource examples resolve from that package or workspace root. -->

## 11. Agent knowledge layers

Use the generated Agent and knowledge files as layered context:

- `AGENT.md` defines the operating role, loading order and execution rules.
- `references/SOURCES.md` lists Kubernetes and OpenTelemetry source baselines.
- `templates/WORKLOAD_CODE_MAP.template.md` defines the map shape.
- `knowledge/NEGATIVE_KNOWLEDGE.md` blocks repeated failures and unsafe shortcuts.
- `knowledge/POSITIVE_KNOWLEDGE.md` captures validated successful patterns.
- `knowledge/KNOWLEDGE.md` stores promoted domain knowledge only after evidence.
- `memory/OPEN_RISKS.md`, `memory/DECISIONS.md` and `memory/FAILURES.md` preserve operational memory.
- `knowledge/KNOWLEDGE_PROMOTION.md` governs when observations become reusable knowledge.
