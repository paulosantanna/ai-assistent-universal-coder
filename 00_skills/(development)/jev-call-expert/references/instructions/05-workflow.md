<!-- Package: 00_skills/(development)/jev-call-expert; relative command/resource examples resolve from that package or workspace root. -->

## Workflow

### 1. Map the callable contract

Inspect real function signatures and create an allowlisted tool table with purpose, parameter type, accepted values, default, required/optional status, side effects, authorization rule, and confirmation rule. Keep exact lookups, calculations, syntactic parsing, permission checks, and execution in code.

Classify each parameter:

- one value from a closed set: one Choice whose option keys exactly match accepted runtime values;
- zero or more values from a closed set: one Noul per candidate member;
- optional closed-set value: one presence Noul plus one Choice; omit the argument when presence is below the evaluated threshold so the function default remains authoritative;
- boolean flag: one narrow Noul when the request can state the flag;
- free text, number, date, identifier, or other open value: use deterministic parsing, retrieve a bounded candidate set and select from it, ask for clarification, or preserve the function default. Never force an open value through an invented closed set.

Include a `no_match` route when requests may legitimately fit no tool. Never expose arbitrary function names supplied by the user.

### 2. Design state and questions

Build one minimal structured state object containing the user's request plus only the application facts needed for the judgments. Give fields descriptive names and preserve role relationships.

Use a Choice to select exactly one route, and make its criteria describe each function's behavior rather than merely repeat its name. For each argument, write one narrow question about meaning and role. Distinguish repeated domains explicitly, such as primary symbol versus benchmark.

Question IDs are code-only; make instructions self-contained. Describe ambiguous option boundaries in criteria. Candidate keys must remain the values accepted by code. TypeSafe cannot select an omitted candidate.

Ask independent route and argument questions over the same state in one request when possible. State speculative premises explicitly, because questions are evaluated independently and cannot see each other's answers. Make a second request only when an earlier answer is needed to fetch evidence or construct the next bounded candidate set.

### 3. Compose the call in code

Read only answers relevant to the selected route. Apply presence judgments before optional values, preserve defaults by omitting unstated arguments, deduplicate set members, and validate the assembled call against the real signature or schema. Recheck the function name against the allowlist immediately before invocation.

Keep raw probabilities available. Choice confidence summarizes concentration of its distribution; it is not proof that the call is correct. Noul has no separate confidence: values near `0.5` mean yes and no are similarly probable, not medium intensity.

Define a risk-aware policy in code:

- uncertain route or required argument: do not invoke; clarify, reject, or hand off;
- recoverable read-only action: allow a lower evaluated threshold if target-domain tests support it;
- consequential mutation: require stricter evidence, authorization, and explicit confirmation regardless of model confidence;
- unused speculative branch: ignore its uncertainty.

For a call-level signal, use the weakest consumed judgment or another documented policy validated on representative data. Do not multiply probabilities and present the result as universal correctness.

### 4. Integrate safely

Use the repository's existing language, package manager, module style, retry policy, logging, and error handling. Add a current SDK dependency only when implementation requires it and the user authorized the integration scope. Keep `TYPESAFE_API_KEY` server-side in the runtime secret provider; never commit or log it.

Handle authentication, validation, rate-limit, overload, timeout, and network failures explicitly. SDK default retries may cover retryable service responses; verify current behavior before relying on it. Never retry a side-effecting function merely because the semantic evaluation was retried.

Separate evaluation from invocation so tests can assert the proposed call without executing the tool. Produce an execution preview for actions that require confirmation.

### 5. Verify behavior

Test contracts rather than prompt wording. Build a representative corpus containing:

- one clear request per function;
- paraphrases and role reversals;
- omitted optional arguments and default preservation;
- multiple selected set members;
- unsupported open values and unknown tools;
- ambiguous, irrelevant, adversarial, and out-of-domain requests;
- low-confidence route and argument outcomes;
- service failures and malformed responses;
- authorization denial and confirmation-required actions.

Assert that emitted names and arguments are allowlisted and type-valid, omitted values retain code defaults, uncertainty cannot trigger unsafe execution, and irrelevant speculative answers are ignored. Evaluate thresholds against target-domain outcomes and action consequences; cookbook values are examples, not universal gates.
