<!-- Package: 00_skills/(architecture)/legacy-migration-planner; relative command/resource examples resolve from that package or workspace root. -->

## Core Principles

These are non-negotiable. Violating any of these invalidates your output.

1. **Never assume.** If you encounter an acronym, term, pattern, or technology you are not 100% certain about, stop and either research it (web search, context7) or ask the user. Say "I don't know what X means — can you clarify?" rather than guessing.
2. **Always cite evidence.** Every claim in your output must reference either a specific `file:line` from the user's codebase or a verified external URL. No unreferenced assertions.
3. **Always research before recommending.** Before suggesting any technology, pattern, or approach, use web search and context7 (when available) to verify it is current, maintained, and appropriate. Never recommend based solely on training data.
4. **Minimize token consumption.** Write output files per domain. Never dump entire file contents — reference by `file:line` ranges. Keep each output file focused on one bounded context.
5. **Direction-agnostic.** This skill handles ANY migration direction: monolith to microservices, microservices to modular monolith, microfrontends to SPA, cross-language, cross-framework, or any combination.
