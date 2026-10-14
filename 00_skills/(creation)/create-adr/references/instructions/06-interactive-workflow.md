<!-- Package: 00_skills/(creation)/create-adr; relative command/resource examples resolve from that package or workspace root. -->

## Interactive Workflow

### Step 1: Gather Context (if not provided)

If the user provides minimal context, use **AskQuestion** to collect essential information:

```json
{
  "title": "ADR Information",
  "questions": [
    {
      "id": "adr_decision",
      "prompt": "What was the decision made? (e.g., 'Use PostgreSQL for primary storage')",
      "options": [
        { "id": "free_text", "label": "I'll describe it in my next message" }
      ]
    },
    {
      "id": "adr_format",
      "prompt": "Which ADR format would you like to use?",
      "options": [
        { "id": "madr", "label": "MADR — structured, with options comparison (recommended)" },
        { "id": "nygard", "label": "Nygard — minimal: Context / Decision / Consequences" },
        { "id": "y_statement", "label": "Y-Statement — single paragraph, very compact" }
      ]
    },
    {
      "id": "adr_status",
      "prompt": "What is the current status of this decision?",
      "options": [
        { "id": "accepted", "label": "Accepted — decision is final" },
        { "id": "proposed", "label": "Proposed — decision is being finalized" },
        { "id": "deprecated", "label": "Deprecated — this approach is no longer recommended" },
        { "id": "superseded", "label": "Superseded — replaced by a newer decision" }
      ]
    },
    {
      "id": "adr_supersedes",
      "prompt": "Does this ADR supersede a previous decision?",
      "options": [
        { "id": "yes", "label": "Yes — I'll provide the ADR number/title" },
        { "id": "no", "label": "No — this is a new decision" }
      ]
    }
  ]
}
```

### Step 2: Validate Mandatory Fields

**MANDATORY fields — ask if missing**:

- **Decision title** (noun phrase, not a question — e.g., "Use Redis for session storage")
- **Date** of the decision (or today's date)
- **Status** (Accepted / Proposed / Deprecated / Superseded)
- **Context** — the forces, constraints, and situation that made this decision necessary
- **The decision itself** — what was chosen and why
- **Consequences** — what becomes easier, harder, or different as a result

**RECOMMENDED fields**:
- **Decision drivers** — the key criteria or constraints
- **Options considered** — what alternatives were evaluated
- **Pros/cons per option** — honest trade-off assessment
- **Decision outcome rationale** — why this option over the others
- **Links** — related ADRs, RFCs, tickets, or documentation

If any mandatory fields are missing, ask IN THE USER'S LANGUAGE before generating the document.

### Step 3: Assign ADR Number

Scan the existing ADR directory for the next sequential number:

1. Check if an ADR directory exists (`docs/adr/`, `docs/decisions/`, `.adr/`, or `adr/`)
2. Find the highest existing number
3. Assign the next number (e.g., if ADR-007 exists, this becomes ADR-008)
4. If no directory exists, start at ADR-001 and suggest creating the directory

### Step 4: Generate the ADR

Generate the ADR following the format selected in Step 1.

### Step 5: Offer File Placement

After generating, ask where to save it:

```
ADR Created: "ADR-{NNN}: {Title}"

Suggested file path: docs/adr/{NNN}-{kebab-case-title}.md

Would you like me to:
1. Save it to docs/adr/ (recommended convention)
2. Save it to a different location
3. Just show the content (I'll place it manually)
```

---
