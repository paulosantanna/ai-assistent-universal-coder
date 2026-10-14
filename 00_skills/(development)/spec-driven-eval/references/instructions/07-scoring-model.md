<!-- Package: 00_skills/(development)/spec-driven-eval; relative command/resource examples resolve from that package or workspace root. -->

## Scoring model

### Unit of scoring: the acceptance criterion (AC), decomposed into binary checks

For each in-scope AC, the frozen checklist holds two sets of atomic checks, each scored **MET (1) / UNMET (0)**:

**Implementation checks (`I`-checks)** — one per distinct observable behavior the AC asserts. A check is MET only if production code performs that behavior, evidenced `file:line`. Include only behaviorally-observable clauses (a verb the AC states: creates / returns / rejects / persists / grants / defaults-to). Non-functional polish (wording, logging) is **not** a check — note it separately so it never moves the score.

When parsing an AC into checks (done once, at baseline-freeze time), apply both rules below so verbs aren't the only thing captured:

**Conjunction / payload-field rule.** When an AC enumerates multiple items — joined by *"and"*, *","*, *"with [field]"*, *"including"* — *especially in the subject or payload of an emitted/returned/persisted artifact*, treat **each named field or entity as its own I-check**. Do not stop at confirming the parent method is called: for each named field, **open the actual data object constructed at `file:line` and verify the field is present in it** (score against the payload shape, not the call site). 
*Example:* "emit a trigger associated with the user **and** the trial end date" → two I-checks: (1) trigger payload carries `userId`, (2) trigger payload carries `trialEndsAt`. Confirming `emit(...)` is reached does **not** satisfy check (2) if the payload object omits the field.

**Disjunction / product-chosen rule.** When an AC presents alternatives ("A or B", "pause or cancel", "immediately or at period end"), decide the reading **once and freeze it in the baseline** (the reading itself must not vary per run):
- *Independent paths* — both are separately reachable behaviors (e.g. "cancel immediately **or** at period end"): **one I-check per path**, each independently MET/UNMET.
- *Product-controlled / configurable* — the AC frames the choice as product-driven (e.g. "apply the **product-chosen** behavior: pause or cancel"): **two I-checks** — (1) the recommended/default behavior is implemented, and (2) the alternative is *reachable without a code change* (config key / flag / env). Hard-coding one option with no switch to the other ⇒ check (2) UNMET. A different feature that happens to reach the other option (e.g. user-initiated cancel) does **not** satisfy (2) — it must be the *same* product-controlled decision point.
- If *"product-chosen"* is itself ambiguous between *runtime-configurable* and *design-time chosen*, resolve it against the PRD/spec wording and record the resolved reading in the baseline; only require reachability of the non-default path when the AC frames the choice as runtime/product-controlled.

**Wiring / ingress rule (asynchronously-delivered side-effects).** When an observable side-effect is delivered asynchronously through an inbound event (e.g. a Stripe webhook → handler → persisted status), add a dedicated **wiring I-check** *in addition to* the behavior I-check: the entry endpoint actually **receives, verifies, and dispatches the inbound event — by type — to the handler.** This is distinct from the `T-outcome` test that the handler produces the right state: a fully-tested handler sitting behind a dead, unregistered, or mis-routed endpoint still fails the wiring check. Without it, a correct-but-unreachable handler would earn full credit (the blind spot the `T-outcome` entry-point-neutrality opens up — letting the test bypass HTTP means *something else* must prove the route exists). Score the wiring I-check against the controller/route that maps the event type to the handler (signature/authenticity verification + dispatch), not against the handler internals. Freeze a wiring I-check on every AC whose observable effect arrives via an inbound async event.

```
I = (# I-checks MET) / (# I-checks)
```

**Test checks (`T`-checks)** — verification checks at the required level(s). Required levels are fixed by policy, not judged per-AC:

- pure / business logic ⇒ **unit required**
- observable HTTP / contract / persistence side-effect ⇒ **e2e / integration required**
- an AC with both ⇒ **both required**

**`T-outcome` — persistence / async side-effects (outcome-based, entry-point-neutral).** When the AC asserts a *resulting state* — phrased "results in / persisted / displayed status / reflects the change / updates the status" — the verification check is on the **real resulting state**, not on a call. Label these checks **`T-outcome`** (distinct from a plain synchronous-response `T-e2e`). The policy has four parts:

- **Assert the real outcome.** MET requires asserting the actual persisted state (a real DB row) or the actually-returned payload, against real infra. A test that only exercises the path without asserting the resulting state is UNMET (Core rule 3).
- **Entry point is the implementation's choice (entry-point-neutral).** Drive the real component via **any** entry point and assert the resulting state: the HTTP endpoint, OR by invoking the handler / queue-consumer / service method directly against the real DB. An async (ack-fast-then-process) design need **not** be tested through the full HTTP→queue→worker path — awaiting the handler and asserting the persisted row is sufficient and equivalent. Do **not** penalize a queue/async architecture for not being driven end-to-end through HTTP; the question is whether the real resulting state is asserted, not which door the test entered.
- **Mock-only exclusion (scoped precisely).** Asserting that a method was *called* on a mocked repository / state-machine (`expect(save).toHaveBeenCalled()` / `expect(transition).toHaveBeenCalledWith(...)`) proves a call, not a persisted outcome ⇒ **UNMET** for any "results in / persisted / displayed status" check (it may still count toward Robustness `R`). **The exclusion is scoped to outcome checks only — it must not over-fire:** a check whose proposition is *"invokes the external API"* (e.g. "immediate cancel calls `StripeClient.cancel`", "creates the subscription in Stripe") is *correctly* verified by a spy/mock, because the asserted proposition **is** the call. Mock-only is fine there; the exclusion does not apply.
- **Minimum-level floor.** The required level is a **floor, not an exact match.** A stronger-level test (an e2e/integration test covering a unit-required proposition) **satisfies** that proposition, provided the specific proposition (e.g. a named payload field, a default value) is actually asserted on the real artifact. Do not mark a unit-required check UNMET solely because the only assertion of it lives in an e2e/integration test.

For each required level, derive binary checks such as: *primary behavior asserted at this level* (MET only if asserted, not merely exercised), *relevant negative/error case asserted*, *each secondary clause asserted*. Mocked external systems (e.g. Stripe via nock) cannot prove the external side — write the check against the observable local contract and note the limitation.

The **conjunction rule applies to T-checks too**: each named payload field gets its own verification check. A test that asserts the artifact was emitted/returned but does **not** assert the field's presence/value is UNMET for that field's check (asserting `emit` was called ≠ asserting the payload carries `trialEndsAt`).

```
T = (# T-checks MET across all required levels) / (# T-checks)
```

> Both `I` and `T` land on a fine-grained value, but every underlying atom is a binary, evidence-backed yes/no — that is what makes them reproducible. There is no "minor vs meaningful" judgment: a clause either has its own check or it does not, and that decision was frozen in the baseline.

### Per-AC, per-story, final

```
AC_score    = 0.6 * I + 0.4 * T
Story_score = mean(AC_score over the story's ACs)      # ACs equally weighted by default
Final       = Σ(w_s * Story_score) / Σ(w_s)            # weighted by story priority
```

**Story priority weights `w_s`:**

| Priority | Weight | Rationale |
| --- | --- | --- |
| P0 | 3 | Core MVP |
| P1 | 2 | MVP-adjacent / launch |
| P2 / out-of-scope | 0 | Excluded from the grade; report separately as *roadmap readiness* |

> The 0.6/0.4 implementation/test split reflects "working software first, proven by tests". Keep these weights — and the P0/P1/P2 weights — fixed across the benchmark; changing them breaks comparability.

### Grade bands

| Final | Band |
| --- | --- |
| ≥ 0.90 | Spec-complete |
| 0.75–0.89 | Strong (minor gaps) |
| 0.60–0.74 | Partial (meaningful gaps) |
| 0.40–0.59 | Weak |
| < 0.40 | Inadequate |

### Bias controls

LLM judges have well-documented biases; hold these explicitly:

- **Verbosity / quantity bias** — more code or more tests **never** raises `I` or `T`. Only checks that map to an AC clause count. Surplus tests go to `R`/`D` (below), never into the grade.
- **Self-preference bias** — see Core rule 4 (judge ≠ author).
- **Anchoring** — score against the frozen baseline and the calibration anchors in `references/reference.md`, not against the previous implementation you happened to grade.

### Reported beside the grade (NOT folded into Final — keep comparable)

- **Robustness Index `R`** — extra tests beyond PRD cases, weighted High=1.0 / Med=0.5 / Low=0.25, summed. Signals defensive quality. Never inflates `Final`.
- **Scope Adherence `S`** — `pass` / `partial` / `fail`, governed by the **traceability principle: every built behavior must trace to a sanctioned source** (a PRD acceptance criterion → `Final`, or a *valid* `E`-addition). Three checks, each per built behavior:
  - **PRD-boundary** — built something on the PRD's explicit out-of-scope list ⇒ `fail`.
  - **Rogue build** — built something that traces to *neither* a PRD AC *nor* a valid `E`-addition (untraceable / invented) ⇒ `fail`.
  - **Plan drift** — `spec.md`/`tasks.md` sanctioned a behavior the code didn't build (or left half-built / inconsistent) ⇒ `partial`.
  Everything traces cleanly ⇒ `pass`. Report the failing/partial behaviors with `file:line`. **A valid requirement the framework derived into the spec but correctly did NOT build (because it is out of scope) is good discipline — it is *not* an `S` penalty;** record it as deferred-valid under `E`.
- **Engineering Gates `G`** — `build`, `lint`, `unit`, `e2e`. **Each gate must be an actually-executed `✓`/`✗` or an explicit `not-run` (with reason, e.g. e2e infra unavailable).** Never report a gate as passing without running it. **The `build` gate is pinned mechanically to remove evaluator discretion:** pick the project's canonical build command once per benchmark (the build script the repo documents) and define the gate as that command exiting `0` — nothing else decides it. Record the exact command in the report so every run uses the identical gate. A pre-existing, unrelated toolchain failure in code the change didn't touch (e.g. a known typecheck error in an untouched migration path) is a **documented non-graded NOTE**, not a `✗`: it does not gate `build` and does not trigger `Adjusted Final`. Record it in the report as a known note, but the `build` verdict follows only the pinned build command's exit code. **Probe-before-not-run:** a gate may only be reported `not-run` after a recorded real attempt — the command executed (or the prerequisite check, e.g. `docker ps` for e2e infra) and its error output pasted as evidence. A reason without an attempt is not valid; the gate stays *not yet scored*, exactly like an UNMET without a search (Core rule 2 applied to gates). **Only a confirmed-red gate (`✗`) triggers `Adjusted Final = Final × 0.5`**; a `not-run` gate cannot grant or deduct credit — it is reported as a known blind spot. The unadjusted `Final` stays reported for comparison. A red gate is **never** fixed by the evaluator (Core rule 5) — record `✗`, adjust, and list the fix.
- **Test Distribution `D`** — every feature test classified into one of three tiers, reported as counts **and** % of the suite. Shows where the testing effort went; never inflates `Final`. See below.

### Test distribution by tier `D` (reported beside)

Classify **every added feature test** (each `it`/test case, counting `it.each` rows individually) into exactly one tier. The classification reuses work already done in the test-check and robustness steps, so it is cheap and reproducible:

| Tier | Definition | Maps to |
| --- | --- | --- |
| **Necessary** (primary happy path) | Asserts the **primary success path** of a **P0/MVP** AC, or a dependency required for that path to work. | A T-check MET on a P0 main flow |
| **Secondary** (important) | Maps to an AC but is **not** the P0 primary path: P1 ACs, edge/negative/error paths, secondary clauses, security/authz, duplicate/idempotency/dedup, status-trigger emission. | A T-check MET that is not Necessary |
| **Nice-to-have** | Maps to **no** AC: defensive/exhaustive coverage (enum mapping, unknown-status, repo/infra internals, helper methods) or unit coverage redundant with an e2e-proven path. | The Robustness `R` extras |

**Rule of thumb:** AC-mapped tests split into Necessary + Secondary; the Robustness `R` inventory is the Nice-to-have tier. A test belongs to exactly one tier — do not double-count.

Report `D` as a table of `tier → count → %` over total feature tests, plus a one-line **shape** read. Healthy suites cover every P0 primary path with at least one Necessary test; a suite thin on Necessary but heavy on Nice-to-have is a smell (robustness without proven core), and the opposite (no defensive tests) is fragile. `D` is descriptive — it never changes `Final`.

---
