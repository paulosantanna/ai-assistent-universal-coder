# Local AGENT contract — architecture-decision-log

This file specializes root `AGENT.md`; it does not define another agent identity.

Map log maintenance onto `BRIEFING -> RECON -> PLAN -> EXECUTE -> VERIFY -> DEBRIEF`: locate the log and its convention before planning, run `scripts/adl_index.mjs` as the RECON baseline, change only status lines and the marked index block, and rescan as the VERIFY gate.
