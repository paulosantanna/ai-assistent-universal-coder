<!-- Package: 00_skills/(tooling)/mermaid-studio; relative command/resource examples resolve from that package or workspace root. -->

## Step 3: Validate

Before rendering, ALWAYS validate the Mermaid syntax:

```bash
node $SKILL_DIR/scripts/validate.mjs <file.mmd>
```

If validation fails:

1. Read the error message carefully
2. Consult `references/troubleshooting.md` for common fixes
3. Fix the syntax and re-validate
4. Maximum 3 fix attempts before asking the user for clarification
