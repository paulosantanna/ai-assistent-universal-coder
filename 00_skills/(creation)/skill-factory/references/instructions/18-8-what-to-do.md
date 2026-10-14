<!-- Package: 00_skills/(creation)/skill-factory; relative command/resource examples resolve from that package or workspace root. -->

## 8. What to do

### 8.1 Understand before generating

Identify:

- what problem repeats;
- who invokes the skill;
- what context it receives;
- what files or tools it may access;
- what output is expected;
- what quality means;
- what can go wrong;
- whether the task is reversible;
- whether memory is genuinely useful.

### 8.2 Keep activation precise

Activation rules must be broad enough to recognize equivalent user intent and narrow enough to avoid false positives.

Include both:

- positive triggers;
- explicit exclusions.

### 8.3 Separate orchestration from execution

When subagents are needed:

- the skill orchestrates;
- specialists execute bounded tasks;
- validators inspect evidence;
- judges do not implement the same work they approve.

### 8.4 Prefer deterministic checks

Use scripts and schemas for:

- required files;
- metadata;
- naming;
- directory structure;
- broken references;
- empty sections;
- forbidden placeholders;
- version format;
- manifest integrity.

Do not rely on the language model for checks that code can perform.

### 8.5 Preserve evidence

Generated skills should define evidence appropriate to their purpose.

Examples:

- command output;
- test report;
- file diff;
- benchmark;
- cited source;
- schema validation;
- generated artifact hash.

### 8.6 Bound memory

Use memory only for:

- recurring validated lessons;
- known failures;
- reusable patterns;
- execution history with provenance.

Do not treat every output as permanent knowledge.

### 8.7 Make completion measurable

A skill must not end with vague completion language.

Define concrete criteria such as:

- required files exist;
- validator exits with code `0`;
- tests pass;
- no unresolved blocking findings remain;
- output matches schema;
- evidence index exists.

---
