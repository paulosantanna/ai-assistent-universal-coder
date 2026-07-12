# FAILURES.md

## 2026-07-11: LSP test `test_workspace_folder_changes` fails with `assert resp is not None`

**Symptom**: `workspace/symbol` request gets no response within 5s timeout

**Root cause analysis**:
1. `initialized` notification sent without `params: null`
2. `lsprotocol`'s `InitializedNotification` type requires `params` → `JsonRpcInvalidParams`
3. Server sends `window/showMessage` error notification to stdout
4. Test's `recv_json` reads the `window/showMessage` instead of `workspace/symbol` response
5. `resp.get("id")` is `None`, assertion fails

**Fix**: Added `"params": null` to `initialized` notification

**Lesson**: LSP client tests must include all fields expected by `lsprotocol` message types, not just the bare LSP spec minimum.

**Files changed**:
- `packages/aeos-language-server/tests/integration/test_multi_root.py` (new test)
- `packages/aeos-language-server/tests/integration/conftest.py` (already had `params: None` in `init_and_open_doc`)
