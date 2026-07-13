# Change Set: portable-llm-provider-runtime

Date: 2026-07-13

## Scope

Prepare AEOS runtime execution for portable, low-cost and open-source LLM usage.

## Changes

- Generalizes runtime provider configuration beyond Ollama.
- Adds executable `deepseek` provider support through a chat-completions API.
- Adds executable `openai-compatible` provider support for OpenRouter, LM Studio,
  llama.cpp server and compatible local gateways.
- Keeps provider secrets out of repository files by storing only environment
  variable names.
- Adds economy-mode prompt compaction and capped output token defaults for free
  or low-quota providers.
- Updates CLI help and Windows/provider documentation.

## Guardrails

- Provider output is not evidence by itself.
- Long prompts are compacted before cloud-compatible calls.
- Raw API keys must remain in environment variables or external secret stores.
- Local Ollama remains the default portable/offline path.

## Rollback

Revert this change set as a group:

- `runtime/src/core/types.ts`
- `runtime/src/core/services.ts`
- `runtime/src/cli/index.ts`
- `runtime/README.md`
- `runtime/docs/INSTALL_WINDOWS.md`
- `aeos/docs/change-sets/2026-07-13-portable-llm-provider-runtime.md`
