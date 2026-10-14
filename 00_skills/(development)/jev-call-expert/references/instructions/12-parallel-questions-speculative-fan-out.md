<!-- Package: 00_skills/(development)/jev-call-expert; relative command/resource examples resolve from that package or workspace root. -->

## Parallel Questions & Speculative Fan-Out

**Principle:** Ask many narrow, independent questions about the same state in one request. Questions are evaluated in parallel, so adding more questions usually has little effect on response time.

**Pattern: Speculative Fan-Out**

Send all questions your code might need in one call, including ones whose answer only matters for some inputs. Let your code decide which answers to use based on earlier results.

**Example: Support Ticket Triage**

```python
questions = {
    "category": Choice(
        instructions="Determine the broad category",
        criteria={
            "bug_report": "User reporting something broken or producing errors",
            "billing": "Charges, invoices, refunds, subscriptions",
            "feature_request": "User requesting new functionality",
            "account": "Login, permissions, profile, security",
        },
    ),
    "bug_severity": Score(
        instructions="How severe is the reported issue?",
        criteria=["Cosmetic", "Broken with workaround", "Blocking issue, no workaround"],
    ),
    "has_reproducible_steps": Noul(
        instructions="User describes specific steps to reproduce the issue",
    ),
    "refund_requested": Noul(
        instructions="User is explicitly asking for a refund or credit",
    ),
    "frustration": Score(
        instructions="How frustrated the user appears?",
        criteria=["Calm", "Frustrated but civil", "Very angry"],
    ),
}

# Code then routes based on category:
if answers["category"].choice == "bug_report":
    if answers["bug_severity"].score > 1.5 and answers["has_reproducible_steps"].noul > 0.6:
        escalate_to_engineering()
    else:
        add_to_bug_backlog()
elif answers["category"].choice == "billing":
    if answers["refund_requested"].noul > 0.7:
        route_to_billing_with_flag()
    else:
        route_to_billing()
# Frustration is useful regardless of category
if answers["frustration"].score > 1.5:
    flag_for_priority_response()
```

Everything needed for the full decision tree comes from one call. Speculative questions are ignored when irrelevant and save a round trip when they are not.
