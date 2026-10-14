<!-- Package: 00_skills/(tooling)/nx-generate; relative command/resource examples resolve from that package or workspace root. -->

## Execution

Keep in mind that you might have to prefix things with npx/pnpx/yarn if the user doesn't have nx installed globally.
Many generators will behave differently based on where they are executed. For example, first-party nx library generators use the cwd to determine the directory that the library should be placed in. This is highly important.

### Consider Dry-Run (Optional)

Running with `--dry-run` first is strongly encouraged but not mandatory. Use your judgment:

- For complex generators or unfamiliar territory: do a dry-run first
- For simple, well-understood generators: may proceed directly
- Dry-run shows file names and created/deleted/modified markers, but not content
- There are cases where a generator does not support dry-run (for example if it had to install an npm package) - in that case --dry-run might fail. Don't be discouraged but simply move on to running the generator for real and iterating from there.

### Running the Generator

Execute the generator with:

```bash
nx generate <generator-name> <options> --no-interactive
```

**CRITICAL**: Always include `--no-interactive` to prevent prompts that would hang the execution.

Example:

```bash
nx generate @nx/react:library --name=my-utils --no-interactive
```

### Handling Generator Failures

If the generator fails:

1. **Diagnose the error** - Read the error message carefully
2. **Identify the cause** - Missing options, invalid values, conflicts, etc.
3. **Attempt automatic fix** - Adjust options or resolve conflicts
4. **Retry** - Run the generator again with corrected options

Common failure reasons:

- Missing required options
- Invalid option values
- Conflicting with existing files
- Missing dependencies
- Generator doesn't support certain flag combinations
