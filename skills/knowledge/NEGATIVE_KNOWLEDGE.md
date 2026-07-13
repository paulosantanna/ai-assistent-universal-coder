# NEGATIVE_KNOWLEDGE.md

## Known failure patterns

### Overbroad activation

A skill that activates for generic words such as "create", "analyze" or "fix" will collide with unrelated workflows.

### Prompt-only validation

Telling a model to "verify perfectly" does not validate files, syntax, references or tests.

### Infinite completion loops

"Continue until 10/10" without a bounded rubric creates non-termination and fabricated scores.

### Memory without governance

Creating `memory.md` without schema, provenance, ownership and promotion rules produces noise.

### Subagent inflation

Adding many agents to a deterministic task increases context cost and coordination failure.

### Fictional authority

A skill must not claim access to tools, files, credentials or external systems that are unavailable.

### Universal skill design

A single skill that covers every domain becomes an unmaintainable meta-prompt rather than a reusable capability.
