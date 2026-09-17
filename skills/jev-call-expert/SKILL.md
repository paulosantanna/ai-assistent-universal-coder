---
name: jev-call-expert
description: Design, implement, review, and test confidence-aware function calling with TypeSafe Jev, typed tool signatures, Choice and Noul questions, speculative fan-out, and code-owned execution policy. Use when the user asks for Jev tool calling, TypeSafe function routing, natural-language dispatch into typed functions, or repair of a Jev dispatcher. Do NOT use for generic LLM tool calling that does not use TypeSafe, open-ended text generation, or direct execution of untrusted or unapproved actions.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
---

# Jev Call Expert

Governance: CodENavi Full Workspace v2

```yaml
skill:
  name: Jev Call Expert
  slug: jev-call-expert
  version: 1.0.0
  description: Builds confidence-aware natural-language dispatch into ordinary typed functions with TypeSafe Jev while code retains validation, authorization, and execution control.
  category: AI_ML
  architecture_level: 1
  risk_level: HIGH
  activation:
    - Jev or TypeSafe function calling, tool routing, typed dispatch, implementation, review, or repair
  exclusions:
    - generic non-TypeSafe LLM tool calling
    - open-ended text generation
    - unapproved destructive or production execution
  inputs:
    - user objective and representative utterances
    - allowlisted function signatures and side-effect classification
    - target language, runtime, and repository conventions
  outputs:
    - dispatcher implementation or review
    - typed question and execution policy
    - tests, confidence behavior, and evidence
  tools:
    - repository tools
    - live TypeSafe documentation
    - project test runner
  memory: false
  human_approval: conditional
  maintainer: AEOS
  owner_agent: codenavi-agent
```

## Identity and mission

This is a skill of the single `codenavi-agent`, not another agent identity. Convert natural-language requests into bounded calls to ordinary typed functions by letting Jev supply narrow semantic judgments while deterministic code owns parsing, validation, authorization, defaults, confidence policy, and execution.

## Preconditions

Require a concrete target behavior, an allowlist of callable functions, their real signatures, representative user requests, and the consequence of each action. If these are not yet explicit, inspect the repository and derive them from code; ask only for choices that materially change safety or behavior.

Before writing version-dependent integration code, read the live [TypeSafe documentation index](https://docs.typesafe.ai/llms.txt), then the current [function-calling cookbook](https://docs.typesafe.ai/cookbooks/function_calling.md) and the selected [JavaScript SDK](https://docs.typesafe.ai/sdk/javascript.md), [Python SDK](https://docs.typesafe.ai/sdk/python.md), or [HTTP API](https://docs.typesafe.ai/api.md) page. Treat live docs and installed SDK types as authoritative. Do not copy a cookbook's pinned model or dependency version into production without checking current docs.

## Scope and authority

Included:

- route a request to one allowlisted function;
- fill closed-set scalar, set, optional, and boolean arguments;
- design Choice and Noul questions over structured state;
- batch independent speculative questions;
- compose typed answers into a validated call;
- define confidence, clarification, confirmation, fallback, and test behavior;
- implement or review server-side TypeSafe SDK or HTTP integrations.

Excluded:

- inventing functions, arguments, permissions, defaults, or candidate values;
- using Jev as a free-text generator or reasoning transcript;
- bypassing application authorization, schema validation, business rules, rate limits, or user confirmation;
- sending credentials, secrets, or unnecessary personal data in state;
- executing production, destructive, financial, security-sensitive, or irreversible calls without the repository's required approval path.

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

## Output contract

Return the smallest repository-native implementation or review that includes:

1. callable-contract inventory;
2. state and typed-question design;
3. deterministic composition and execution policy;
4. confidence and fallback behavior;
5. tests and exact verification evidence;
6. assumptions, residual risks, and blocking conditions.

## Examples

### Closed-set routing

User says: "Use Jev to route support messages to our typed handlers."

Result: inspect the handler signatures, create a route Choice with `no_match`, batch branch argument questions, validate the selected handler and arguments in code, and test clear, ambiguous, and unsupported requests.

### Optional argument

User says: "For `plot_price`, keep its default window unless the user names a time range."

Result: ask a window-presence Noul and a window Choice in the same request; consume the Choice only when presence passes the tested policy, otherwise omit `window`.

### Unsafe mutation

User says: "Let high Jev confidence execute any admin tool automatically."

Result: reject confidence as authorization. Restrict routing to the allowlist, preserve permission checks, require the configured confirmation path for consequential actions, and test denial behavior.

## Failure behavior and stop conditions

Stop with a concrete blocker when callable signatures or candidate sets cannot be verified, a required live API contract is unavailable and no installed type evidence exists, credentials would need to enter tracked or client-side code, authorization or confirmation rules are missing for consequential tools, or deterministic validation cannot guarantee an allowlisted type-valid call.

On model or service failure, return no executable call unless a separately authorized deterministic fallback exists. Never guess a route, argument, or approval.

## Completion criteria

Complete only when current TypeSafe contracts were checked, every executable function and argument is bounded by code, uncertainty and failures have non-executing paths, required approvals remain intact, representative behavior tests pass, and claims cite files, commands, or authoritative documentation.
