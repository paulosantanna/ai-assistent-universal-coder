<!-- Package: 00_skills/(mapping)/documentation-mapper; relative command/resource examples resolve from that package or workspace root. -->

## 10. Skill Generation Workflow

```
User Request (target repo)
  ↓
ROOT Agent — Deep Understanding
  → Clone/read repository
  → Identify tech stack, languages, frameworks
  → Identify all config files, data files, CI/CD
  → Identify all source code directories
  ↓
PARENT Agents (10 parallel analyses)
  → Layer 1: Infrastructure
  → Layer 2: Data & Persistence
  → Layer 3: Backend & API
  → Layer 4: Frontend & Presentation
  → Layer 5: Business Logic & Domain
  → Layer 6: Integrations & External Systems
  → Layer 7: Security & Compliance
  → Layer 8: DevOps & CI/CD
  → Layer 9: Observability & Monitoring
  → Layer 10: Governance & Documentation
  ↓
Data Dictionary Extraction
  → MongoDB: connect or scan model files
  → ChromaDB: scan config and collection references
  → SQL: scan schema/migration files
  ↓
Stakeholder Views Generation
  → Business view
  → Developer view
  → Director view
  ↓
Mermaid Diagram Generation
  → Write .mmd source files for ALL 14 diagram types
  → Run mmdc to export SVG + PNG
  ↓
Interactive HTML Assembly
  → Generate single HTML file with all content
  → Implement click-to-expand entity navigation
  ↓
PDF Generation
  → Generate full documentation PDF via HTML print
  → Generate improvement plan PDF
  ↓
Evidence Consolidation
  → Collect all file references, command outputs, analysis results
  → Generate evidence_log.jsonl
  ↓
JUDGE (CHIEF STAFF) Evaluation
  → Evaluate every artifact against 10-criterion rubric
  → Score: 0.0–10.0 per criterion
  → If overall < 10.0/10 → pass findings back, re-execute (max 10×)
  → If overall == 10.0/10 → approve
  ↓
Save to Desktop/documentação_v1/
  ↓
Return: package location + evaluation report + verdict
```

---
