<!-- Package: 00_skills/(development)/jev-call-expert; relative command/resource examples resolve from that package or workspace root. -->

## Confidence Thresholds Guide

| Stakes | Confidence Threshold | Action |
|--------|---------------------|--------|
| Low (read-only) | ≥ 0.5 | Proceed automatically |
| Medium | ≥ 0.7 | Flag for review or ask user to confirm |
| High | ≥ 0.85 | Require explicit user confirmation |
| Critical | ≥ 0.95 | Human-supervised only, never auto-execute |

**Key insight:** The 0.5 floor catches anything the model reports as genuinely uncertain. Above that floor, each action type has its own threshold based on the consequences of acting on a wrong classification.

Check [Confidence](https://docs.typesafe.ai/confidence) for the exact formulas on how confidence is derived from probabilities.
