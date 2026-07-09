# Playbook: tool-router-audit

## Objective

Validate that all external access paths go through Tool Router.

## Checks

- registered MCPs;
- direct filesystem calls in AEOS code;
- direct subprocess usage;
- direct git shell calls;
- direct secret access;
- unlogged tool calls.

## Blocking Conditions

- direct tool bypass found;
- missing permission decision log;
- missing policy decision log;
- missing tool-call evidence.
