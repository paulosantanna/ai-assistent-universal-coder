<!-- Package: 00_skills/(creation)/skill-factory; relative command/resource examples resolve from that package or workspace root. -->

## 5. Architecture decision

Choose the smallest architecture that safely satisfies the request.

### Level 1 — Minimal skill

Use when the task is bounded and deterministic.

```text
<skill-name>/
├── SKILL.md
└── references/package-notes.md
```

### Level 2 — Standard skill

Use when validation, scripts or structured templates are required.

```text
<skill-name>/
├── SKILL.md
├── references/package-notes.md
├── scripts/
├── schemas/
├── templates/
└── tests/
```

### Level 3 — Governed learning skill

Use only when the skill must learn, preserve evidence, reuse lessons or coordinate agents.

```text
<skill-name>/
├── SKILL.md
├── references/package-notes.md
├── AGENT.md
├── scripts/
├── schemas/
├── templates/
├── tests/
├── knowledge/
│   ├── KNOWLEDGE.md
│   ├── NEGATIVE_KNOWLEDGE.md
│   ├── POSITIVE_KNOWLEDGE.md
│   ├── KNOWLEDGE_PROMOTION.md
│   └── CONTINUOUS_LEARNING.md
└── memory/
    ├── EXECUTIONS.md
    ├── LESSONS.md
    ├── FAILURES.md
    └── PATTERNS.md
```

Do not create Level 3 by default.

Complexity must be justified by actual reuse, risk or learning requirements.

---
