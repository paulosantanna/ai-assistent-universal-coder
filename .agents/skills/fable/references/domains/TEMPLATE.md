# Domain adapter: TEMPLATE (the schema every adapter conforms to)

This file is the explicit schema behind every adapter in this directory. `/fable-domain` generates new adapters against it; CI validates that every adapter carries its binding sections; fable-judge reads adapters through it.

An adapter changes only the nouns, never the loop. It answers, for one sector: what counts as evidence, who the authority is, what verification by observation means, and what the frauds are.

---

# Domain adapter: <sector>

Applies when the deliverable is <the sector's actual outputs, concretely>. The loop is unchanged; these definitions replace the coding defaults.

## Minimum evidence set (binding)

1. **<The governing document or ground truth of this sector>**: <what must actually be opened>.
2. **<The subject's own facts>**: <primary material claims trace to>.
3. **<One live external reference>**: <fetched now, not recalled>.

## Evidence and primary sources

Primary sources for this sector. Signature non-evidence.

## Authority order

Explicit user instruction > governing policy > platform behavior > stated intent > memory.

## Verification by observation

- Observed verification steps for this sector.

## Fraud table (for fable-judge)

| Fraud | Symptom |
|---|---|
| <Fraud name> | <Symptom> |

## Done, by example

"<Deliverable> is done" means: <observed checklist>.
