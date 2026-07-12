# NEGATIVE_KNOWLEDGE.md

## Known Failures and Prohibited Patterns

### LSP: Sending `initialized` without `params: null`
- **Prohibited**: `{"jsonrpc":"2.0","method":"initialized"}` (missing `params`)
- **Why**: `lsprotocol`'s `InitializedNotification` type requires a `params` field. Missing it triggers `JsonRpcInvalidParams`, causing the server to send a `window/showMessage` error instead of processing subsequent requests correctly.
- **Consequence**: The test's `recv_json` receives the `window/showMessage` notification instead of the expected response, causing assertion failures and timeouts.

### LSP: Not draining subprocess stderr
- **Prohibited**: Creating an LSP server subprocess with `stderr=subprocess.PIPE` without reading from it
- **Why**: The pipe buffer fills up, blocking the server when it writes error logs, causing cascading timeouts
- **Fix**: Always start a daemon thread to drain stderr: `threading.Thread(target=_drain_stderr, args=(proc.stderr,), daemon=True).start()`
