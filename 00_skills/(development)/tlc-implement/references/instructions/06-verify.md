<!-- Package: 00_skills/(development)/tlc-implement; relative command/resource examples resolve from that package or workspace root. -->

## Verify

When the last commit lands, dispatch the Verifier automatically. See [verify.md](../tlc/references/verify.md). The work is not done at the last commit; it is done when the Verifier's report accounts for every check.

**"After the last commit" means the last one of the feature, not of your batch.** With handoff on there are two different lasts, and collapsing them is the shortcut that looks like saving a hop: the agent closing the final batch tells its own sub-agent to verify on the way out. Even with a clean context that sub-agent is briefed by someone who only saw the final batch, so it verifies that slice's range and reports a pass that reads as if it covered the feature. And the verdict goes back to the author, who is then the one deciding what to do about it.

So a build agent finishes, reports, and stops. Verification is the orchestrator's step: it waits for the last batch, then dispatches one agent over `<feature base>..HEAD` with **every** check. If you find yourself writing "when you commit, dispatch the verifier" into a builder's prompt, that is the mistake with a friendly face.
