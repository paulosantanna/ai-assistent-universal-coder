# AEOS Judge v6 — MCP Runtime Rules

Judge v6 must block when:

- MCP registry is missing.
- MCP config is missing.
- enabled MCP exposes tools not allowlisted.
- critical MCP is enabled by default.
- MCP call lacks permission decision.
- MCP call lacks policy decision.
- MCP call lacks evidence.
- Tool Router was bypassed.
- raw output persisted with secrets.
- timeout/retry policy missing.
- write occurred outside sandbox.
- git mutation occurred outside allowed actions.
- test runner executed non-allowlisted command.
- package extraction occurred without verify PASS.

Judge v6 must PASS only when:

- all MCP calls are routed through Tool Router;
- all MCP calls are logged;
- all permission/policy decisions exist;
- all output is redacted;
- all evidence hashes verify;
- no forbidden MCP is enabled.
