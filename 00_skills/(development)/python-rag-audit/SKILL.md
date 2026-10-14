---
name: python-rag-audit
description: Audit Python RAG (Retrieval-Augmented Generation) pipelines for security, data leakage, prompt injection risks, and production readiness. Use when the user requests python rag audit or invokes python-rag-audit. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: Python RAG Audit

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Audit Python RAG (Retrieval-Augmented Generation) pipelines for security, data leakage, prompt injection risks, and production readiness.

## Allowed Actions

- Read Python source files.
- Read requirements and dependency files.
- Analyze RAG pipeline code.
- Detect prompt injection vulnerabilities.
- Detect PII/PHI exposure in data processing.
- Detect hardcoded API keys and secrets.
- Analyze embedding and vector store configurations.
- Generate audit reports.

## Forbidden Actions

- Modify production data.
- Access external APIs without approval.
- Read secret values.
- Execute model inference.
- Disable safety guardrails.

## Inputs

- workspace path
- pipeline entry points
- data source paths

## Outputs

- rag-security-report.md
- dependency-vulnerability-report.md
- data-exposure-report.md
- hardening-recommendations.md

## Evidence Required

- pipeline code with line references
- dependency list with versions
- data processing flow
- vector store configuration
- prompt template citations

## Prompt Contract

- State the objective, target scope, assumptions and constraints before execution.
- Use only evidence-backed facts; mark uncertainty explicitly.
- Route tool access through approved command, MCP or Tool Router paths.
- Redact secrets, credentials, tokens and sensitive values.
- Return facts, assumptions, risks, recommendations, evidence_refs and blocking_conditions when applicable.
- Stop when required evidence, permissions, policy approval or input context is missing.

## Quality Gates

- Must identify each vulnerability with code location.
- Must classify severity with rationale.
- Must not expose actual data samples in report.
- Must provide actionable fix recommendations.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
