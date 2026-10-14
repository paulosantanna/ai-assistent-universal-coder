<!-- Package: 00_skills/(development)/jev-call-expert; relative command/resource examples resolve from that package or workspace root. -->

## Composite Scoring

Break a complex judgment into atomic scores, combine with weights you control in code.

**Example: Resume Screening**

```python
questions = {
    "python_depth": Score(
        instructions="How much depth of python experience does this candidate have?",
        criteria=["No Python experience mentioned", "Mentioned but no detail", "Used in projects, some specifics", "Primary language, multiple projects", "Deep expertise: architecture, performance, libraries"],
    ),
    "team_leadership": Score(
        instructions="How much experience managing engineering teams?",
        criteria=["No management experience", "Informal mentorship or tech lead", "Led a small team or project", "Managed a team with direct reports", "Managed multiple teams or an engineering org"],
    ),
    "system_design": Score(
        instructions="How much experience designing large-scale systems?",
        criteria=["No architecture work", "Contributed to design discussions", "Designed components of a larger system", "Owned architecture of a significant system", "Designed systems at scale across multiple domains"],
    ),
    "generalist": Score(
        instructions="How much evidence they pick up unfamiliar tools/roles?",
        criteria=["Only one domain", "Some variety within narrow field", "Worked across a few areas/tech stacks", "Regularly moved between domains", "Track record of ramping up in unfamiliar areas"],
    ),
}

with TypeSafeClient() as client:
    response = client.system_one(state=resume, questions=questions)

# Normalize each score to 0-1 (divide by top level number = 4)
py = response.answers["python_depth"].score / 4
lead = response.answers["team_leadership"].score / 4
arch = response.answers["system_design"].score / 4
general = response.answers["generalist"].score / 4

# Senior IC: 40% Python + 10% leadership + 40% design + 10% generalist
ic_score = (0.40 * py) + (0.10 * lead) + (0.40 * arch) + (0.10 * general)

# Engineering Manager: 15% Python + 40% leadership + 20% design + 25% generalist
em_score = (0.15 * py) + (0.40 * lead) + (0.20 * arch) + (0.25 * general)
```

Weights live in your code, so you can adjust them when ranking doesn't match expectations.
