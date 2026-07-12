# AEOS Language Server — Golden Test Fixtures

This directory contains golden test fixtures for the AEOS Language Server (LSP).
Golden tests establish a known-correct baseline: the LSP should produce exactly
the expected diagnostics when processing each file.

## Directory Structure

```
golden/
  README.md                        # This file
  valid_agent.yaml                 # Valid AEOS agent definition
  valid_skill.yaml                 # Valid AEOS skill definition
  valid_playbook.yaml              # Valid AEOS playbook with steps, conditions, approval
  valid_policy.yaml                # Valid AEOS policy definition
  valid_permissions.yaml           # Valid AEOS permissions configuration
  valid_registry.yaml              # Valid AEOS registry
  valid_agent.agent.md             # Valid agent in markdown format with front matter
  valid_skill.skill.md             # Valid skill in markdown format
  valid_playbook.playbook.md       # Valid playbook in markdown format
  valid_full_agent.md              # Comprehensive AGENT.md file
  valid_full_playbook.md           # Comprehensive PLAYBOOK.md file
  valid_aeos_config.yaml           # Valid aeos.config.yaml
  valid_overlay_index.yaml         # Valid overlay registry index
  valid_expression.txt             # File with valid AEOS expressions (CEL syntax)
  valid_aeos.json                  # Valid AEOS JSON config
  valid_aeos.toml                  # Valid AEOS TOML config
  valid_multi_doc.yaml             # Valid multi-document YAML with AEOS artifacts
  invalid_syntax.yaml              # YAML with syntax errors
  invalid_schema.yaml              # Valid YAML but invalid schema (missing required fields)
  duplicate_ids.yaml               # Multiple artifacts with same $id
  dangling_reference.yaml          # References to non-existent agents/skills/playbooks
  cycle_playbooks.yaml             # Circular dependency between playbooks
  cycle_agent_inheritance.yaml     # Circular agent inheritance via parent field
  missing_permission.yaml          # Step requiring permission without it
  missing_rollback.yaml            # Mutating step without rollback
  insecure_command.yaml            # Shell command with injection risk / secrets
  no_timeout.yaml                  # Steps without timeout configured
  unlimited_retry.yaml             # Steps with dangerous retry configurations
  invalid_token_budget.yaml        # Invalid token budget configuration
  deprecated_field.yaml            # Uses deprecated fields (AEOS0020)
  cross_file_ref.yaml              # Cross-file references that don't resolve
  expected/                        # Expected diagnostic outputs (one JSON per fixture)
    valid_agent.yaml.json
    ...
    cross_file_ref.yaml.json
```

## Usage in Tests

```typescript
// Example: golden test runner
import { readFileSync, readdirSync } from "fs";
import { validateDocument } from "../src/validator";

const goldenDir = path.join(__dirname, "golden");
const expectedDir = path.join(goldenDir, "expected");

for (const file of readdirSync(goldenDir)) {
  if (!file.endsWith(".yaml") && !file.endsWith(".md") &&
      !file.endsWith(".json") && !file.endsWith(".toml") &&
      !file.endsWith(".txt")) continue;

  const uri = `file:///tests/golden/${file}`;
  const document = readFileSync(path.join(goldenDir, file), "utf-8");
  const actualDiagnostics = await validateDocument(uri, document);

  const expectedPath = path.join(expectedDir, `${file}.json`);
  const { diagnostics: expected } = JSON.parse(
    readFileSync(expectedPath, "utf-8")
  );

  expect(actualDiagnostics).toEqual(expected);
}
```

## File Categories

### Valid Files (pass)
Files that are syntactically correct YAML/JSON/TOML/Markdown and conform
to their respective AEOS JSON Schemas. They should produce no errors and
at most informational diagnostics (AEOS0051, AEOS0052) in verbose mode.

### Invalid Files (fail)
Files with specific, documented errors. Each file has comments explaining
the intentional errors and expected diagnostic codes. The corresponding
`expected/<file>.json` file contains the full expected diagnostic output.

### Error Types Covered

| Category | Files | Diagnostic Codes |
|---|---|---|
| Schema validation | invalid_schema.yaml | AEOS0001, AEOS0002 |
| YAML parse errors | invalid_syntax.yaml | AEOS0001 |
| Duplicate IDs | duplicate_ids.yaml | AEOS0011 |
| Dangling references | dangling_reference.yaml, cross_file_ref.yaml | AEOS0012, AEOS0016 |
| Circular dependencies | cycle_playbooks.yaml, cycle_agent_inheritance.yaml | AEOS0013 |
| Permission errors | missing_permission.yaml | AEOS0036 |
| Missing rollbacks | missing_rollback.yaml | AEOS0028 |
| Security violations | insecure_command.yaml | AEOS0032, AEOS0033, AEOS0034 |
| Missing timeouts | no_timeout.yaml | AEOS0047 |
| Retry misconfiguration | unlimited_retry.yaml | AEOS0006, AEOS0047 |
| Invalid enums/ranges | invalid_token_budget.yaml | AEOS0003, AEOS0005, AEOS0006 |
| Deprecated fields | deprecated_field.yaml | AEOS0020 |

## Adding New Tests

1. Create the fixture file in `golden/` with a descriptive name
2. Add comments explaining intentional errors
3. Create the expected output in `expected/<name>.json`
4. Ensure the test runner picks up the new file
5. Run `npm test` to verify the golden test passes

## Diagnostic Data Structure

Expected diagnostic files follow this structure:

```json
{
  "uri": "file:///tests/golden/<filename>",
  "diagnostics": [
    {
      "range": { "start": { "line": N, "character": C }, "end": { "line": N, "character": C } },
      "severity": 1|2|3,
      "code": "AEOSXXXX",
      "message": "Description of the diagnostic",
      "source": "aeos-language-server"
    }
  ]
}
```

Severity: 1=Error, 2=Warning, 3=Information
