# SECURITY_ENGINEERING.md

> **AEOS Chief/Staff Edition**
>
> This document is part of the AI Engineering Operating System.
> It is designed for AI agents acting as Chief AI Architect, Chief Software Architect,
> Principal Engineer, Staff Software Engineer and Staff AI Engineer.
>
> Core invariants:
> - Evidence before claims.
> - Architecture before implementation.
> - Delegation before context bloat.
> - Verification before completion.
> - Knowledge persistence after every material outcome.
> - Human authority over unsafe or high-impact decisions.


## Purpose

Define secure engineering behavior.

## Core practices

- least privilege;
- input validation;
- output encoding;
- secret management;
- secure logging;
- dependency scanning;
- SAST/DAST where applicable;
- threat modeling;
- audit trails;
- secure CI/CD.

## AI-specific threats

- prompt injection;
- tool misuse;
- data exfiltration;
- model inversion;
- poisoning;
- unsafe autonomous actions;
- excessive permissions.

## Rule

Security is a design constraint, not a final checklist.
