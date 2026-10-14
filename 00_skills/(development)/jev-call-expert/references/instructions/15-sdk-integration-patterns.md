<!-- Package: 00_skills/(development)/jev-call-expert; relative command/resource examples resolve from that package or workspace root. -->

## SDK Integration Patterns

### Python SDK

```python
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

questions = {
    "topic": Choice(
        instructions="Which team should handle this?",
        criteria={"billing": null, "technical": null, "support": null},
    ),
    "urgency": Score(
        instructions="How urgent is this?",
        criteria=["can wait", "this week", "today"],
    ),
    "needs_human": Noul(
        instructions="Does this require human intervention?",
    ),
}

with TypeSafeClient() as client:
    response = client.system_one(state=ticket, questions=questions)

# Access answers
topic_choice = response.answers["topic"].choice
urgency_score = response.answers["urgency"].score
needs_human = response.answers["needs_human"].noul

# Use confidence for thresholding
if response.answers["topic"].confidence < 0.7:
    route_to_human()
```

**Installation:**
```bash
uv add typesafe-sdk  # or: pip install typesafe-sdk
# Set TYPESAFE_API_KEY in environment
```

**Async usage:**
```python
from typesafe_sdk import AsyncTypeSafeClient, Choice, Noul, Score

async def main():
    async with AsyncTypeSafeClient() as client:
        response = await client.system_one(
            state=ticket,
            questions=questions,
        )
        # same access pattern as sync
```

### JavaScript/TypeScript SDK

```typescript
import { choice, TypeSafeClient } from "@typesafe-ai/sdk";

const client = new TypeSafeClient();
const response = await client.systemOne({
  state: { document: "I was charged twice. Please fix this ASAP." },
  questions: {
    category: choice("What is this ticket about?", {
      billing: null,
      technical: null,
      other: null,
    }),
  },
});

console.log(response.answers.category.choice);
```

**Installation:**
```bash
npm install @typesafe-ai/sdk
# Set TYPESAFE_API_KEY in environment
```

**TypeScript types are inferred from your questions.** The package includes ESM, CommonJS, and TypeScript declarations.
