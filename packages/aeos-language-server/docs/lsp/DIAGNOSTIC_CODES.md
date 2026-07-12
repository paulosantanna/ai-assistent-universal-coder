# AEOS Language Server — Diagnostic Code Catalog

This document catalogs all diagnostic codes produced by the AEOS Language Server. Each entry includes the code, message, severity, description, and fix instructions.

## Code Ranges

| Range | Category |
|---|---|
| AEOS0001-AEOS0010 | Schema Validation Errors |
| AEOS0011-AEOS0020 | Semantic Validation Errors |
| AEOS0021-AEOS0030 | Reference Resolution Errors |
| AEOS0031-AEOS0040 | Security & Compliance Warnings |
| AEOS0041-AEOS0045 | Performance Warnings |
| AEOS0046-AEOS0050 | Configuration Warnings |
| AEOS0051-AEOS0055 | Informational Diagnostics |

## Diagnostics

---

### AEOS0001 — Schema validation failed

- **Message**: `Schema validation failed: {details}`
- **Severity**: Error
- **Description**: The document does not conform to its JSON Schema definition. This catches missing required properties, type mismatches, pattern violations, and other structural issues.
- **How to fix**: Review the validation message for the specific field and constraint that was violated. Common causes:
  - Missing required field (check the schema for `required` array)
  - Wrong type for a field (e.g., string instead of number)
  - Value does not match the expected pattern (e.g., semver for `version`)
  - Unknown property (if `additionalProperties` is `false`)
- **Auto-fix**: Available for simple fixes (e.g., adding default values, fixing types)

---

### AEOS0002 — Missing required property

- **Message**: `Missing required property '{property}' in '{path}'`
- **Severity**: Error
- **Description**: A property listed in the schema's `required` array is missing from the document.
- **How to fix**: Add the missing property with an appropriate value. See the schema definition for the expected type and format.
- **Auto-fix**: Available — inserts the property with a placeholder or default value.

---

### AEOS0003 — Invalid property type

- **Message**: `Expected type '{expected}' but got '{actual}' for property '{property}'`
- **Severity**: Error
- **Description**: The value for a property does not match the expected type defined in the schema.
- **How to fix**: Change the value to match the expected type. For example, change `"version": 1` to `"version": "1.0.0"`.
- **Auto-fix**: Available in simple cases (e.g., string to number conversion).

---

### AEOS0004 — Value does not match pattern

- **Message**: `Value '{value}' does not match pattern '{pattern}' for property '{property}'`
- **Severity**: Error
- **Description**: The value does not match the regex pattern defined in the schema.
- **How to fix**: Update the value to match the required pattern. Common pattern violations:
  - `$id` / `stable_id`: Must start with a letter and contain only alphanumeric, underscore, hyphen, or dot characters
  - `version`: Must follow semver format (e.g., `1.0.0`, `2.3.4-beta.1`)
- **Auto-fix**: Not available.

---

### AEOS0005 — Value not in enum

- **Message**: `Value '{value}' is not one of the allowed values: {allowed}`
- **Severity**: Error
- **Description**: The value is not in the list of allowed values defined in the schema's `enum` constraint.
- **How to fix**: Replace the value with one of the allowed values listed in the message.
- **Auto-fix**: Available — offers a quick-pick of allowed values.

---

### AEOS0006 — Value outside allowed range

- **Message**: `Value {value} is {issue} the allowed range ({min}-{max}) for property '{property}'`
- **Severity**: Error
- **Description**: A numeric value is outside the `minimum`/`maximum` range defined in the schema.
- **How to fix**: Adjust the value to fall within the allowed range.
- **Auto-fix**: Available — clamps the value to the nearest valid boundary.

---

### AEOS0007 — Array has too few items

- **Message**: `Array '{property}' has {count} items, minimum required is {min}`
- **Severity**: Error
- **Description**: An array property has fewer items than required by `minItems`.
- **How to fix**: Add more items to the array to meet the minimum requirement.
- **Auto-fix**: Not available.

---

### AEOS0008 — Array has duplicate items

- **Message**: `Array '{property}' contains duplicate items`
- **Severity**: Warning
- **Description**: An array with `uniqueItems: true` contains duplicate values.
- **How to fix**: Remove the duplicate items from the array.
- **Auto-fix**: Available — removes duplicates.

---

### AEOS0009 — Additional property not allowed

- **Message**: `Additional property '{property}' is not allowed in '{path}'`
- **Severity**: Error
- **Description**: The document contains a property that is not defined in the schema and `additionalProperties` is `false`.
- **How to fix**: Remove the unknown property, or add it to the schema if it should be allowed.
- **Auto-fix**: Not available.

---

### AEOS0010 — Invalid $ref target

- **Message**: `$ref target '{ref}' could not be resolved`
- **Severity**: Error
- **Description**: A `$ref` in the document points to a schema file or definition that does not exist.
- **How to fix**: Check that the referenced schema path is correct and the file exists.
- **Auto-fix**: Not available.

---

### AEOS0011 — Duplicate $id in workspace

- **Message**: `Duplicate $id '{id}' found in workspace. First defined at '{path1}', duplicate at '{path2}'`
- **Severity**: Error
- **Description**: Two artifacts in the workspace have the same `$id`. IDs must be unique within the workspace.
- **How to fix**: Rename one of the artifacts to use a different `$id`.
- **Auto-fix**: Not available (requires user intent).

---

### AEOS0012 — Unresolved reference

- **Message**: `Reference '{reference}' in '{source}' does not resolve to any artifact in the workspace`
- **Severity**: Error
- **Description**: A reference (e.g., skill `$id`, agent `$id`, playbook `$id`) points to an artifact that does not exist.
- **How to fix**: Create the referenced artifact, or correct the reference to point to an existing artifact.
- **Auto-fix**: Offers to create a stub artifact for the missing reference.

---

### AEOS0013 — Circular dependency detected

- **Message**: `Circular dependency detected: {chain}`
- **Severity**: Error
- **Description**: Artifacts form a circular dependency chain (e.g., Agent A delegates to Agent B, which delegates back to Agent A).
- **How to fix**: Break the cycle by removing or restructuring one of the dependencies.
- **Auto-fix**: Not available.

---

### AEOS0014 — Missing skill for capability

- **Message**: `Agent '{agent}' references capability '{capability}' but no skill provides it`
- **Severity**: Warning
- **Description**: An agent declares a capability that is not provided by any registered skill.
- **How to fix**: Either add a skill that provides the capability, or remove the capability from the agent.
- **Auto-fix**: Not available.

---

### AEOS0015 — Conflicting delegation policy

- **Message**: `Delegation policy allows agent '{agent}' to delegate to '{sub-agent}' but that agent does not exist or is not configured for delegation`
- **Severity**: Warning
- **Description**: The delegation policy references a sub-agent that either does not exist or does not accept delegation.
- **How to fix**: Ensure the sub-agent exists and has the appropriate delegation configuration.
- **Auto-fix**: Not available.

---

### AEOS0016 — Playbook step references missing artifact

- **Message**: `Playbook step '{step}' references '{artifact}' which is not defined in the workspace`
- **Severity**: Error
- **Description**: A playbook step uses a `tool`, `skill`, or `playbook` that does not exist in the workspace.
- **How to fix**: Create the missing artifact or correct the reference in the step.
- **Auto-fix**: Same as AEOS0012 — offers stub creation.

---

### AEOS0017 — Unused artifact

- **Message**: `Artifact '{id}' is defined but never referenced by any other artifact`
- **Severity**: Information
- **Description**: An artifact exists in the workspace but no other artifact references it. This may indicate dead configuration.
- **How to fix**: Remove the artifact if it is not needed, or ensure it is referenced.
- **Auto-fix**: Not available.

---

### AEOS0018 — Incompatible model requirements

- **Message**: `Skill '{skill}' requires model capability '{capability}' but agent '{agent}' model preferences do not provide it`
- **Severity**: Warning
- **Description**: A skill requires a model capability (e.g., vision, tool_use) that the agent's model preferences do not provide.
- **How to fix**: Update the agent's model preferences to include a model with the required capabilities, or use a different skill.
- **Auto-fix**: Not available.

---

### AEOS0019 — Environment variable mismatch

- **Message**: `Skill '{skill}' requires environment variable '{var}' which is not defined in the agent or workspace configuration`
- **Severity**: Warning
- **Description**: A skill's `dependencies.environment` declares a required environment variable that is not configured.
- **How to fix**: Add the required environment variable to the workspace or agent configuration.
- **Auto-fix**: Offers to add the variable with a placeholder value.

---

### AEOS0020 — Deprecated field usage

- **Message**: `Field '{field}' is deprecated in schema version {version}. Use '{alternative}' instead.`
- **Severity**: Warning
- **Description**: A field that has been deprecated in a newer schema version is being used.
- **How to fix**: Replace the deprecated field with the recommended alternative.
- **Auto-fix**: Available — migrates to the new field.

---

### AEOS0021 — Invalid version format

- **Message**: `Version '{version}' does not follow semantic versioning format (X.Y.Z)`
- **Severity**: Error
- **Description**: The `version` field does not match the semver pattern `MAJOR.MINOR.PATCH` with optional pre-release suffix.
- **How to fix**: Update the version to follow the semver format, e.g., `1.0.0` or `2.3.4-beta.1`.
- **Auto-fix**: Available in simple cases.

---

### AEOS0022 — Name does not match naming convention

- **Message**: `Name '{name}' does not match the expected naming convention: {convention}`
- **Severity**: Warning
- **Description**: The name does not follow the workspace's configured naming convention (e.g., kebab-case, snake_case).
- **How to fix**: Rename to match the convention.
- **Auto-fix**: Available — suggests the corrected name.

---

### AEOS0023 — Version downgrade detected

- **Message**: `Version downgrade detected: '{id}' changed from {old} to {new}`
- **Severity**: Warning
- **Description**: An artifact's version has decreased compared to a previously indexed version.
- **How to fix**: Ensure version numbers always increase.
- **Auto-fix**: Not available.

---

### AEOS0024 — Step has no action

- **Message**: `Step '{step}' has no tool, skill, or playbook configured`
- **Severity**: Error
- **Description**: A playbook step does not specify any of `tool`, `skill`, or `playbook`. At least one is required.
- **How to fix**: Add a `tool`, `skill`, or `playbook` property to the step.
- **Auto-fix**: Not available.

---

### AEOS0025 — Invalid condition expression

- **Message**: `Condition expression '{expression}' in '{context}' is invalid: {error}`
- **Severity**: Error
- **Description**: A condition expression (e.g., `run_if`, `run_unless`) cannot be parsed or evaluated.
- **How to fix**: Check the expression syntax. Refer to the expression language documentation for valid syntax.
- **Auto-fix**: Not available.

---

### AEOS0026 — Parallel step conflicts

- **Message**: `Parallel step '{step1}' and '{step2}' may conflict as both write to output variable '{variable}'`
- **Severity**: Warning
- **Description**: Two parallel steps produce the same output variable, which may cause non-deterministic results.
- **How to fix**: Rename the output variables to be unique, or make the steps sequential.
- **Auto-fix**: Not available.

---

### AEOS0027 — Unused playbook variable

- **Message**: `Playbook variable '{variable}' is defined but never used in any step`
- **Severity**: Information
- **Description**: A variable defined in the `variables` section is not referenced by any step.
- **How to fix**: Remove the unused variable or add it to a step.
- **Auto-fix**: Available — removes unused variable.

---

### AEOS0028 — Missing rollback for destructive step

- **Message**: `Step '{step}' performs a destructive action but has no rollback defined`
- **Severity**: Warning
- **Description**: A step that modifies state (write, delete, execute) does not have a rollback action, which may leave the workspace in an inconsistent state if a later step fails.
- **How to fix**: Add a `rollback` configuration to the step that can undo its effects.
- **Auto-fix**: Not available.

---

### AEOS0029 — Output variable never set

- **Message**: `Playbook output '{output}' is declared but never assigned by any step`
- **Severity**: Warning
- **Description**: An output variable declared in the playbook's `outputs` section is never produced by any step.
- **How to fix**: Ensure at least one step maps to this output variable.
- **Auto-fix**: Not available.

---

### AEOS0030 — Registry entry source not found

- **Message**: `Registry entry '{stable_id}' references source '{source}' which does not exist`
- **Severity**: Error
- **Description**: A registry entry's `source` field points to a file path that cannot be found.
- **How to fix**: Verify the source path is correct and the file exists.
- **Auto-fix**: Not available.

---

### AEOS0031 — Workspace trust not established

- **Message**: `Workspace is not trusted. Some features are disabled. To trust this workspace, add a .aeos directory or aeos.config.yaml`
- **Severity**: Warning
- **Description**: The workspace does not contain a trust marker. The server operates in restricted mode.
- **How to fix**: Add a `.aeos/` directory or `aeos.config.yaml`/`aeos.config.json` to the workspace root.
- **Auto-fix**: Offers to create the `.aeos/` directory.

---

### AEOS0032 — Path outside allowed scope

- **Message**: `Path '{path}' is outside the allowed workspace scope. Operation blocked.`
- **Severity**: Error
- **Description**: An operation attempted to access a file path outside the configured allowlist (path traversal protection).
- **How to fix**: Use a path within the allowed workspace scope. Check the `blocked_paths` and `allowed_paths` configuration.
- **Auto-fix**: Not available.

---

### AEOS0033 — Command not in allowlist

- **Message**: `Command '{command}' is not in the allowed command list or matches a blocked pattern`
- **Severity**: Error
- **Description**: A command execution request was blocked by the command policy.
- **How to fix**: Use an allowed command, or update the command allowlist in the configuration.
- **Auto-fix**: Not available.

---

### AEOS0034 — Secret detected in plaintext

- **Message**: `Potential secret detected in field '{field}'. Secrets should not be stored in plaintext in configuration files.`
- **Severity**: Warning
- **Description**: A field value matches a secret pattern (e.g., API key, password, token).
- **How to fix**: Remove the plaintext secret and use a secure secret store (e.g., environment variable reference, credential manager).
- **Auto-fix**: Not available.

---

### AEOS0035 — Plaintext secret in diagnostic

- **Message**: `Diagnostic output contains potential secret. Redaction applied.`
- **Severity**: Information
- **Description**: A diagnostic message contained a value that matched a secret pattern. The secret has been redacted from the output.
- **How to fix**: No action needed; this is informational.
- **Auto-fix**: Not applicable.

---

### AEOS0036 — Insufficient permissions for operation

- **Message**: `Operation '{operation}' requires '{capability}' capability which is not granted to the current role`
- **Severity**: Error
- **Description**: An operation was denied because the current role does not have the required capability.
- **How to fix**: Either use a role with the required capability, or request the capability be added to the current role.
- **Auto-fix**: Not available.

---

### AEOS0037 — Approval gate triggered

- **Message**: `Approval gate '{gate}' triggered. Operation requires approval from {level}.`
- **Severity**: Warning
- **Description**: An operation hit an approval gate and must be approved before proceeding.
- **How to fix**: Request approval from the required approver level.
- **Auto-fix**: Not available.

---

### AEOS0038 — Required evidence missing

- **Message**: `Required evidence type '{type}' is missing for execution '{execution_id}'`
- **Severity**: Error
- **Description**: The evidence configuration requires a specific evidence type that was not produced during execution.
- **How to fix**: Ensure the execution produces all required evidence types. Check that evidence collecting components are properly configured.
- **Auto-fix**: Not available.

---

### AEOS0039 — Evidence hash mismatch

- **Message**: `Evidence hash mismatch for '{evidence_id}'. Expected {expected}, got {actual}. Evidence may have been tampered with.`
- **Severity**: Error
- **Description**: The hash of an evidence record does not match the recorded hash, indicating possible tampering.
- **How to fix**: Investigate potential tampering. Restore evidence from a trusted backup if available.
- **Auto-fix**: Not available.

---

### AEOS0040 — Policy evaluation failed

- **Message**: `Policy '{policy}' evaluation failed: {error}`
- **Severity**: Error
- **Description**: An error occurred while evaluating a policy rule, preventing the policy from being enforced.
- **How to fix**: Check the policy definition for syntax errors or invalid conditions. Ensure all referenced fields exist in the execution context.
- **Auto-fix**: Not available.

---

### AEOS0041 — Large file may impact performance

- **Message**: `File '{path}' is {size} MB. Large files may impact server performance.`
- **Severity**: Information
- **Description**: A file exceeds 1 MB, which may slow down parsing and validation.
- **How to fix**: Consider splitting the file into smaller, focused configuration files.
- **Auto-fix**: Not available.

---

### AEOS0042 — Workspace has many files

- **Message**: `Workspace has {count} indexed files. Large workspaces may impact performance.`
- **Severity**: Information
- **Description**: The workspace contains more than 5,000 indexed files. Performance may degrade.
- **How to fix**: Consider excluding non-AEOS files from indexing using `.aeosignore` patterns.
- **Auto-fix**: Not available.

---

### AEOS0043 — Deeply nested structure

- **Message**: `Document '{path}' has {depth} levels of nesting. Deeply nested structures may impact performance.`
- **Severity**: Information
- **Description**: A document has more than 20 levels of nesting, which may slow down validation.
- **How to fix**: Flatten the document structure where possible.
- **Auto-fix**: Not available.

---

### AEOS0044 — Schema cache miss

- **Message**: `Schema '{schema}' was not cached and had to be loaded from disk. Consider pre-loading schemas for better performance.`
- **Severity**: Information
- **Description**: A schema was requested that was not in the cache, causing a disk load.
- **How to fix**: This is informational. For production, configure schema pre-loading.
- **Auto-fix**: Not available.

---

### AEOS0045 — Index rebuild triggered

- **Message**: `Workspace index rebuild triggered: {reason}. This may cause temporary slowdown.`
- **Severity**: Information
- **Description**: The workspace index was rebuilt due to a configuration change or file system event.
- **How to fix**: No action needed. Performance will return to normal once indexing completes.
- **Auto-fix**: Not available.

---

### AEOS0046 — Configuration file not found

- **Message**: `Configuration file '{path}' was not found. Using default settings.`
- **Severity**: Warning
- **Description**: A referenced configuration file does not exist.
- **How to fix**: Create the configuration file or update the reference to point to an existing file.
- **Auto-fix**: Not available.

---

### AEOS0047 — Invalid configuration value

- **Message**: `Configuration value '{key}' is invalid: {reason}`
- **Severity**: Warning
- **Description**: A configuration value is out of range or has an invalid format.
- **How to fix**: Correct the configuration value.
- **Auto-fix**: Offers valid alternatives in some cases.

---

### AEOS0048 — Feature disabled by configuration

- **Message**: `Feature '{feature}' is disabled by the current configuration. Enable it in settings to use this feature.`
- **Severity**: Information
- **Description**: A requested feature is disabled by the server or client configuration.
- **How to fix**: Enable the feature in the server or client settings.
- **Auto-fix**: Not available.

---

### AEOS0049 — Missing plugin dependency

- **Message**: `Plugin '{plugin}' requires dependency '{dependency}' which is not installed`
- **Severity**: Warning
- **Description**: A registered plugin has unmet dependencies.
- **How to fix**: Install the missing dependency or disable the plugin.
- **Auto-fix**: Not available.

---

### AEOS0050 — Plugin load error

- **Message**: `Plugin '{plugin}' failed to load: {error}`
- **Severity**: Error
- **Description**: A plugin could not be loaded due to an error.
- **How to fix**: Check the plugin code for errors. Ensure the plugin is compatible with the current server version.
- **Auto-fix**: Not available.

---

### AEOS0051 — Schema validation passed

- **Message**: `Schema validation passed for '{path}'`
- **Severity**: Information
- **Description**: The document passed schema validation. This diagnostic only appears when verbose mode is enabled.
- **How to fix**: No action needed.
- **Auto-fix**: Not applicable.

---

### AEOS0052 — Semantic validation passed

- **Message**: `Semantic validation passed for '{path}'`
- **Severity**: Information
- **Description**: The document passed all semantic validation rules.
- **How to fix**: No action needed.
- **Auto-fix**: Not applicable.

---

### AEOS0053 — No AEOS artifacts found in workspace

- **Message**: `No AEOS artifacts were found in the workspace. Create an agent, skill, or playbook definition to get started.`
- **Severity**: Information
- **Description**: The workspace index did not find any AEOS configuration files.
- **How to fix**: Create AEOS artifact files in the workspace.
- **Auto-fix**: Not available.

---

### AEOS0054 — Using cached index

- **Message**: `Using cached workspace index from {timestamp}. Cache validity: {validity}.`
- **Severity**: Information
- **Description**: The server is using a previously built index from cache.
- **How to fix**: No action needed.
- **Auto-fix**: Not applicable.

---

### AEOS0055 — Judge evaluation result

- **Message**: `Judge evaluation: Score {score}/{max} ({status})`
- **Severity**: Information / Warning
- **Description**: Reports the result of a judge evaluation. Severity depends on pass/fail status.
- **How to fix**: If failed, review the judge report for specific failing rules and remediation suggestions.
- **Auto-fix**: Not available.

---

## Diagnostic Severity Mapping

| Severity | Code | Description |
|---|---|---|
| `Error` (1) | AEOS0001-AEOS0010, AEOS0011, AEOS0012, AEOS0013, AEOS0016, AEOS0021, AEOS0024, AEOS0025, AEOS0030, AEOS0032, AEOS0033, AEOS0036, AEOS0038, AEOS0039, AEOS0040, AEOS0050 | Must fix before execution |
| `Warning` (2) | AEOS0008, AEOS0014, AEOS0015, AEOS0018, AEOS0019, AEOS0020, AEOS0022, AEOS0023, AEOS0026, AEOS0028, AEOS0029, AEOS0031, AEOS0034, AEOS0037, AEOS0046, AEOS0047, AEOS0049 | Should review |
| `Information` (3) | AEOS0017, AEOS0027, AEOS0035, AEOS0041, AEOS0042, AEOS0043, AEOS0044, AEOS0045, AEOS0048, AEOS0051, AEOS0052, AEOS0053, AEOS0054, AEOS0055 | Contextual information |

## Diagnostic Data Structure

Each diagnostic in the `textDocument/publishDiagnostics` notification includes a `data` field with:

```typescript
interface AeosDiagnosticData {
  /** The diagnostic code */
  code: string;
  /** Schema path that generated this diagnostic (if applicable) */
  schemaPath?: string;
  /** Semantic rule ID (if applicable) */
  ruleId?: string;
  /** Whether an auto-fix is available */
  fixable: boolean;
  /** Additional context for the diagnostic */
  context?: {
    /** Related artifact $id */
    artifactId?: string;
    /** Related reference */
    reference?: string;
    /** Suggested value for fix */
    suggestedValue?: unknown;
  };
}
```
