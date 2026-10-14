<!-- Package: 00_skills/(tooling)/nx-generate; relative command/resource examples resolve from that package or workspace root. -->

## Pre-Execution Checklist

Before running any generator, complete these steps:

### 1. Fetch Generator Schema

Use the `--help` flag to understand all available options:

```bash
npx nx g @nx/react:library --help
```

Pay attention to:

- Required options that must be provided
- Optional options that may be relevant to the user's request
- Default values that might need to be overridden

### 2. Read Generator Source Code

Understanding what the generator actually does helps you:

- Know what files will be created/modified
- Understand any side effects (updating configs, installing deps, etc.)
- Identify options that might not be obvious from the schema

To find generator source code:

- For plugin generators: Use `node -e "console.log(require.resolve('@nx/<plugin>/generators.json'));"` to find the generators.json, then locate the source from there
- If that fails, read directly from `node_modules/<plugin>/generators.json`
- For local generators: They are typically in `tools/generators/` or a local plugin directory. You can search the repo for the generator name to find it.

### 2.5 Reevaluate if the generator is right

Once you have built up an understanding of what the selected generator does, reconsider: Is this the right generator to service the user request?
If not, it's okay to go back to the Generator Discovery Flow and select a different generator before proceeding. If you do, make sure to go through the entire pre-execution checklist once more.

### 3. Understand Repo Context

Before generating, examine the target area of the codebase:

- Look at similar existing artifacts (other libraries, applications, etc.)
- Identify patterns and conventions used in the repo
- Note naming conventions, file structures, and configuration patterns
- Try to match these patterns when configuring the generator

For example, if similar libraries are using a specific test runner, build tool or linter, try to match that if possible.
If projects or other artifacts are organized with a specific naming convention, try to match it.

### 4. Validate Required Options

Ensure all required options have values:

- Map the user's request to generator options
- Infer values from context where possible
- Ask the user for any critical missing information
