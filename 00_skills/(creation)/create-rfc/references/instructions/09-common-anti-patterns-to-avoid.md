<!-- Package: 00_skills/(creation)/create-rfc; relative command/resource examples resolve from that package or workspace root. -->

## Common Anti-Patterns to Avoid

### Predetermined Conclusion Disguised as RFC

**BAD**:
```
We should use Kubernetes. Here are some reasons. Option 2 is to not use Kubernetes (obviously wrong).
```

**GOOD**:
```
Option 1: Adopt Kubernetes — [genuine pros and cons]
Option 2: Stick with Docker Compose — [genuine pros and cons]
Option 3: Move to managed container platform (ECS/Cloud Run) — [genuine pros and cons]
```

### Vague Background

**BAD**:
```
Our current deployment process has some issues.
```

**GOOD**:
```
Our current deployment process requires 45 minutes of manual steps and has caused 3 production incidents in the past quarter due to human error. The team spends ~8 hours/week on deployment-related tasks.
```

### Missing "Do Nothing" Option

Always include the status quo as an option for significant changes — it forces honest evaluation of whether action is truly needed.

### No Decision Criteria (or criteria defined after options)

**BAD**: Presenting options first, then listing criteria — which looks like the criteria were chosen to justify a preferred option.

**GOOD**: Define criteria with weights *before* listing options. Then evaluate each option against them explicitly. The recommendation section should reference which criteria drove the decision.

### Hidden or Unstated Assumptions

**BAD**:
```
We'll migrate to the new system over 6 months.
```

**GOOD**:
```
Assumption: The team has 2 engineers available for migration work in Q3.
Confidence: Medium. Invalidated if Q3 headcount changes.
```

Unstated assumptions become invisible time bombs. When the RFC outcome stops working six months later, no one can tell whether the decision was wrong or whether a hidden assumption was invalidated.

---
