<!-- Package: 00_skills/(tooling)/nx-generate; relative command/resource examples resolve from that package or workspace root. -->

## Post-Generation

### 1. Modify Generated Code (If Needed)

Generators provide a starting point, but the output may need adjustment to match the user's specific requirements:

- Add or modify functionality as requested
- Adjust imports, exports, or configurations
- Integrate with existing code patterns in the repo

### 2. Format Code

Run formatting on all generated/modified files:

```bash
nx format --fix
```

Languages other than javascript/typescript might need other formatting invocations too.

### 3. Run Verification

Verify that the generated code works correctly. What this looks like will vary depending on the type of generator and the targets available.
If the generator created a new project, run its targets directly
Use your best judgement to determine what needs to be verified.

Example:

```bash
nx lint <new-project>
nx test <new-project>
nx build <new-project>
```

### 4. Handle Verification Failures

When verification fails:

**If scope is manageable** (a few lint errors, minor type issues):

- Fix the issues
- Re-run verification to confirm

**If issues are extensive** (many errors, complex problems):

- Attempt simple, obvious fixes first
- If still failing, escalate to the user with:
  - Description of what was generated
  - What verification is failing
  - What you've attempted to fix
  - Remaining issues that need user input
