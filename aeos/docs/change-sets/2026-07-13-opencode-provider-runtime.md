# Change Set: OpenCode Provider Runtime

## Intent

Add OpenCode support to the AEOS portable LLM runtime without creating a second
provider execution stack.

## Changes

- Added `opencode` as an executable AEOS provider.
- Reused the OpenAI-compatible chat completions path for OpenCode-compatible
  local and gateway models.
- Added CLI help and validation for `aeos provider configure opencode`.
- Added `aeos provider template opencode` with an `opencode.json` starter block.
- Documented the Windows and runtime flows for OpenCode.

## Safety

- AEOS stores only provider metadata and environment variable names.
- Raw API keys must stay in environment variables or OpenCode auth.
- Economy defaults cap prompt and output size for low-quota providers.

## Verification

- Runtime TypeScript build.
- CLI smoke tests for provider configuration, status and template generation.
