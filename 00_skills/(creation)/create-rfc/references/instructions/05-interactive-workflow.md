<!-- Package: 00_skills/(creation)/create-rfc; relative command/resource examples resolve from that package or workspace root. -->

## Interactive Workflow

### Step 1: Gather Context (if not provided)

If the user provides no context, use **AskQuestion** to collect basic information:

```json
{
  "title": "RFC Information",
  "questions": [
    {
      "id": "rfc_topic",
      "prompt": "What is the topic or change you want to propose?",
      "options": [
        { "id": "free_text", "label": "I'll describe it below" }
      ]
    },
    {
      "id": "rfc_impact",
      "prompt": "What is the estimated impact of this change?",
      "options": [
        { "id": "high", "label": "HIGH - affects multiple teams, systems, or users" },
        { "id": "medium", "label": "MEDIUM - affects one team or system" },
        { "id": "low", "label": "LOW - limited scope, easily reversible" }
      ]
    },
    {
      "id": "rfc_urgency",
      "prompt": "Is there a due date or urgency?",
      "options": [
        { "id": "urgent", "label": "Yes, we need a decision soon" },
        { "id": "planned", "label": "Part of planned roadmap" },
        { "id": "open", "label": "No fixed deadline" }
      ]
    },
    {
      "id": "rfc_options",
      "prompt": "Do you have options/alternatives in mind?",
      "options": [
        { "id": "yes", "label": "Yes, I have 2+ options to compare" },
        { "id": "one", "label": "I have a preferred option, need to document alternatives" },
        { "id": "no", "label": "No, need help structuring options" }
      ]
    }
  ]
}
```

### Step 2: Validate Mandatory Fields

**MANDATORY fields — ask if missing**:

- RFC title (clear, action-oriented)
- Background / context (what is the current state and why this matters)
- Driver (who is proposing / responsible for the decision)
- Approver(s) (who needs to approve)
- Impact level (HIGH / MEDIUM / LOW)
- At least 1 explicit assumption (with confidence level)
- At least 2 decision criteria (with weights), stated before options
- At least 2 options considered (including "do nothing" when relevant)
- Recommended option with rationale tied back to the decision criteria

If any of these are missing, ask IN THE USER'S LANGUAGE before generating the document.

### Step 3: Detect RFC Type and Tailor Sections

| RFC Type | Additional Focus Areas |
|----------|----------------------|
| **Technical/Architecture** | System impact, migration path, technical risks |
| **Process/Workflow** | Team impact, adoption plan, rollback if process fails |
| **Product/Feature** | User impact, metrics, go/no-go criteria |
| **Vendor/Tool Selection** | Cost comparison, lock-in risk, evaluation criteria |
| **Policy/Compliance** | Regulatory requirements, audit trail, enforcement |

### Step 4: Generate RFC Document

Generate the RFC in Markdown following the templates below.

### Step 5: Offer Next Steps

After generating, offer:

```
RFC Created: "[Title]"

Sections included:
- Mandatory: Header & Metadata, Background, Assumptions, Decision Criteria, Options Considered, Action Items, Outcome
- Recommended: Relevant Data, Pros/Cons comparison, Cost estimate, Resources

Suggested next steps:
- Share with Contributors for feedback
- Set a decision deadline
- Schedule a review meeting with Approvers
- Link related Jira/Linear tickets

Would you like me to:
1. Add more options to compare?
2. Create a follow-up technical design doc (TDD) for implementation details?
3. Publish this to Confluence?
```
