# LESSONS.md

## Lesson 1: LSP `initialized` notification requires `params: null`

When testing LSP servers that use `lsprotocol`/`pygls`, the `initialized` notification MUST include `"params": null`. Without it, message deserialization fails with `JsonRpcInvalidParams`, causing the server to send an error notification that disrupts the test's message reading.

**Detection heuristic**: If `workspace/symbol` (or any subsequent request) times out but `initialize` succeeds, check if the `initialized` notification includes `"params": null`.

## Lesson 2: Subprocess pipe buffers can deadlock LSP servers

When spawning an LSP server subprocess with `stdout=PIPE, stderr=PIPE`, both pipes must be actively read. If stderr is not drained, the pipe buffer fills up and the server's async event loop blocks on stderr writes, preventing it from processing requests or sending responses.

**Detection heuristic**: If the server responds to the first request but subsequent requests time out, and stderr is piped but not read, the stderr buffer is likely full.

## Lesson 3: `recv_json` can receive out-of-band messages

The `recv_json` function reads any JSON-RPC message from stdout, including unexpected error notifications from the server. Tests should either:
- Drain unexpected messages before reading the expected one, or
- Filter responses by message type/id to ensure they're consuming the right message
