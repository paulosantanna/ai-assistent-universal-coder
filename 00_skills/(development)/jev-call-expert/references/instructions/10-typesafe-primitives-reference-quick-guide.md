<!-- Package: 00_skills/(development)/jev-call-expert; relative command/resource examples resolve from that package or workspace root. -->

## TypeSafe Primitives Reference (Quick Guide)

### Choice

**Use when:** the answer is one of a fixed set of options with no order between them.

**Returns:** `choice` (selected option), `probabilities` (distribution across all options), `confidence` (0 to 1, how peaked the distribution is).

**Example:**
```python
from typesafe_sdk import Choice, TypeSafeClient

with TypeSafeClient() as client:
    response = client.system_one(
        state="My running shoes arrived in the wrong size",
        questions={
            "department": Choice(
                instructions="Which team should handle this?",
                criteria={
                    "returns": "Exchanges, wrong or damaged items",
                    "shipping": "Delivery status, delays, lost packages",
                    "billing": "Charges, invoices, payment problems",
                },
            ),
        },
    )
    print(response.answers["department"].choice)  # "returns"
    print(response.answers["department"].probabilities)  # {"returns": 1.0, "shipping": 0.0, "billing": 0.0}
    print(response.answers["department"].confidence)  # 1.0
```

### Score

**Use when:** the answer is a position on a spectrum you can describe in steps.

**Returns:** `score` (position on level number line, can fall between levels), `legend` (level number mapped to description), `probabilities` (distribution across levels), `confidence` (0 to 1).

**Example:**
```python
from typesafe_sdk import Score, TypeSafeClient

with TypeSafeClient() as client:
    response = client.system_one(
        state="The export button crashes the settings page in Safari",
        questions={
            "bug_severity": Score(
                instructions="How severe is the reported issue?",
                criteria=[
                    "Cosmetic; no impact to functionality",
                    "Broken or degraded feature, but workaround exists",
                    "Blocking issue; no workaround exists",
                ],
            ),
        },
    )
    print(response.answers["bug_severity"].score)  # 1.43
    print(response.answers["bug_severity"].confidence)  # 0.35
```

### Noul

**Use when:** the answer is yes or no.

**Returns:** `noul` (0 to 1, probability that answer is yes).

**Example:**
```python
from typesafe_sdk import Noul, TypeSafeClient

with TypeSafeClient() as client:
    response = client.system_one(
        state="I have asked three times now. Can I please just talk to a real person?",
        questions={
            "is_human_escalation": Noul(
                instructions="Is the customer asking for a human agent?",
            ),
        },
    )
    print(response.answers["is_human_escalation"].noul)  # 0.99
```
