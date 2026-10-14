<!-- Package: 00_skills/(tooling)/nx-generate; relative command/resource examples resolve from that package or workspace root. -->

## Key Principles

1. **Local generators first** - Always prefer workspace/local generators over external plugin generators when both could work

2. **Understand before running** - Read both the schema AND the source code to fully understand what will happen

3. **No prompts** - Always use `--no-interactive` to prevent hanging

4. **Generators are starting points** - Modify the output as needed to fully satisfy the user's requirements

5. **Verify changes work** - Don't just generate; ensure the code builds, lints, and tests pass

6. **Be proactive about fixes** - Don't just report errors; attempt to resolve them automatically when possible

7. **Match repo patterns** - Study existing similar code in the repo and match its conventions
