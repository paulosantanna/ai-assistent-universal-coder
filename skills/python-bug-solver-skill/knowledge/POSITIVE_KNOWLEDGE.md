# POSITIVE_KNOWLEDGE.md

## LSP Test Patterns

### Initialized notification must include params: null
- **Symptom**: `workspace/symbol` request gets no response after sending `initialized` notification
- **Root cause**: `lsprotocol`'s `InitializedNotification` type requires a `params` field. Missing it causes `JsonRpcInvalidParams` error, which triggers a `window/showMessage` error notification to stdout. The test's `recv_json` picks up this unexpected message instead of the expected `workspace/symbol` response.
- **Fix**: Always include `"params": null` in `initialized` notifications: `{"jsonrpc":"2.0","method":"initialized","params":null}`
- **Pattern**: When writing LSP client tests, all JSON-RPC messages must conform to the full message schema expected by `lsprotocol`/`pygls`, not just the bare minimum LSP spec.

### Stderr pipe draining prevents server deadlock
- **Symptom**: LSP server subprocess hangs when stderr pipe buffer fills up
- **Root cause**: Server writes error logs to stderr; if nothing reads from the pipe, the buffer fills up and the server blocks on write
- **Fix**: Drain stderr in a background daemon thread: `threading.Thread(target=_drain_stderr, args=(proc.stderr,), daemon=True)`
- **Pattern**: Always drain stdout/stderr pipes of LSP subprocesses to prevent deadlocks
