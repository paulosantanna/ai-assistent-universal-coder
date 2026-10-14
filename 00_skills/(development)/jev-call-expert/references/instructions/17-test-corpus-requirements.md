<!-- Package: 00_skills/(development)/jev-call-expert; relative command/resource examples resolve from that package or workspace root. -->

## Test Corpus Requirements

Build a representative test corpus containing:

- one clear request per function;
- paraphrases and role reversals;
- omitted optional arguments and default preservation;
- multiple selected set members;
- unsupported open values and unknown tools;
- ambiguous, irrelevant, adversarial, and out-of-domain requests;
- low-confidence route and argument outcomes;
- service failures and malformed responses;
- authorization denial and confirmation-required actions.

**Assert that:**
- emitted names and arguments are allowlisted and type-valid;
- omitted values retain code defaults;
- uncertainty cannot trigger unsafe execution;
- irrelevant speculative answers are ignored.

Evaluate thresholds against target-domain outcomes and action consequences; cookbook values are examples, not universal gates.
