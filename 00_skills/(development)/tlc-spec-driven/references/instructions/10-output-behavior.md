<!-- Package: 00_skills/(development)/tlc-spec-driven; relative command/resource examples resolve from that package or workspace root. -->

## Output Behavior

**Do the work; do not narrate the machinery.** Produce the right artifact for the phase instead of announcing the phase ("I will now run the Specify phase"). The user judges the output, not a play-by-play of the process. This keeps the flow from reading as robotic.

**Match effort to the work.** Lightweight steps (feature-level checks, validation, mechanical tasks) do not need top-tier reasoning; heavy steps (complex design, ambiguous features) do. If the harness lets you pick a model per sub-agent, apply the tier rubric in [sub-agents.md](../tlc/references/sub-agents.md); otherwise proceed and simply invest more care on the heavy steps. Mention this once per session at most, and only if it helps; skip it for an experienced user.

**Write generated artifacts in a plain, decided voice.** Specs, ADRs, validation reports, commit messages, and chat summaries follow the writing rules in [coding-principles.md](../tlc/references/coding-principles.md): lead with the verdict, state decisions definitively, cut filler and mechanical hedging.
