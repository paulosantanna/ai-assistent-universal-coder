<!-- Package: 00_skills/(architecture)/legacy-migration-planner; relative command/resource examples resolve from that package or workspace root. -->

## Constraints

### MUST DO

- Research every technology recommendation via web search before including it
- Use context7 for library documentation when available
- Cite `file:line` for every codebase observation
- Ask the user when encountering unknown terms, acronyms, or ambiguous requirements
- Produce one output file per domain to keep context manageable
- Include rollback strategy for every migration step
- Validate that current stack versions match what is actually in the codebase (package.json, requirements.txt, etc.)

### MUST NOT DO

- Guess the meaning of acronyms, internal terms, or business logic
- Recommend technologies without web search verification
- Write implementation code (this skill produces plans, not code)
- Assume migration direction without evidence from RESEARCH
- Skip the RESEARCH phase or combine it with PLAN
- Reference files or lines that were not actually read
- Include unreferenced claims in any output file
