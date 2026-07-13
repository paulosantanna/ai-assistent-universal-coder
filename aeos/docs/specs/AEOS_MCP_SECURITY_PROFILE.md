# AEOS MCP Security Profile

## Default Security Posture

- deny-all by default;
- read-only first;
- write only to sandbox;
- explicit allowlists;
- no implicit trust;
- no direct agent invocation;
- no secrets by default;
- no production mutation.

## MCP Security Controls

1. Capability allowlist.
2. Tool allowlist.
3. Input schema validation.
4. Output schema validation.
5. Timeout.
6. Retry cap.
7. Redaction.
8. Secret scanner over outputs.
9. Path normalization.
10. Path traversal block.
11. Absolute path block unless target root-validated.
12. Evidence logging.
13. Judge validation.

## Critical MCPs Disabled by Default

- secrets;
- browser-authenticated;
- database-write;
- cloud-write;
- deploy;
- shell-unrestricted.

## ZIP/Package MCP Rule

Package extraction must occur only after verify PASS and only into a staging directory unless explicitly approved.
