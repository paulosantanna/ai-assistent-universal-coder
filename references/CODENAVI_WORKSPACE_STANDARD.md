# CodENavi Workspace Standard

The canonical agent contract is `AGENT.md`/`AGENTS.md`. Both files are identical by design.

Every skill, super-skill, MCP, LSP, LCP, playbook, tool, adapter, runtime extension and governed artifact must follow the single CodENavi agent standard and the mission lifecycle:

**BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF**

The workspace has one agent identity only: `codenavi-agent`.

Specialization is expressed through skills, lenses, MCPs, LSPs, playbooks and tools. Creating additional agent or subagent identities is prohibited.

All implementation must use the coding principles and `.notebook/` rules from the canonical agent contract. Secrets remain runtime-only, masked and non-persistent.
