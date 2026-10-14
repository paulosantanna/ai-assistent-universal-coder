<!-- Package: 00_skills/(development)/tlc-implement; relative command/resource examples resolve from that package or workspace root. -->

## Examples

### Example 1: Decided work, one feature

User says: "Implement this spec."
Actions:
1. Read the source completely, then walk the code it touches.
2. Refuse vague claims. Sweep the nine unwritten requirements.
3. Read `references/checklist-format.md` and write `.checks/<feature>.md`.
4. Build from the checklist. Run each proof. Commit in coherent pieces.
5. After the last commit of the feature, dispatch a fresh Verifier with `references/verify.md`.
Result: a checklist with named proofs, green proofs, and a Verifier report that accounts for every check.

### Example 2: Nobody decided

User says: "Build a cache for the dashboard."
Actions: Do not run this skill. There is no prior artifact to extract from.
Result: hand off; no `.checks/` file from this skill.

### Example 3: Wrong skill

User says: "Should we add billing?"
Actions: Do not run this skill. Nobody has decided what to build.
Result: hand off; no checklist and no code from this skill.
