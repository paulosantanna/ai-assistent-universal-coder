<!-- Package: 00_skills/(creation)/create-adr; relative command/resource examples resolve from that package or workspace root. -->

## ADR File Naming Convention

```
docs/adr/
├── 001-use-postgresql-for-primary-storage.md
├── 002-adopt-event-driven-architecture.md
├── 003-replace-jenkins-with-github-actions.md   ← supersedes ADR-001 if relevant
└── README.md                                     ← optional index
```

- Zero-padded numbers: `001`, `002`, ... `099`, `100`
- Kebab-case title
- `.md` extension
- Common directories: `docs/adr/`, `docs/decisions/`, `adr/`, `.adr/`

---
