#!/usr/bin/env node
import { existsSync, readFileSync } from 'node:fs';

const required = [
  'AGENT.md',
  'AGENTS.md',
  'references/CODENAVI_WORKSPACE_STANDARD.md',
  'references/CODENAVI_NOTEBOOK_SPEC.md',
  '.notebook/INDEX.md',
  'skills/codenavi/SKILL.md',
  'skills/notebook-intelligence/SKILL.md',
  'skills/dependency-updater/SKILL.md',
  'skills/pr-reviewer/SKILL.md',
  'skills/docs-writer/SKILL.md',
  'skills/local-secret-vault/SKILL.md',
  'skills/jira-confluence-assistant/SKILL.md',
  'skills/java-version-expert/SKILL.md'
];

const errors = [];
for (const path of required) {
  if (!existsSync(path)) errors.push(`missing:${path}`);
}

if (existsSync('AGENT.md')) {
  const text = readFileSync('AGENT.md', 'utf8');
  for (const phrase of ['BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF', '.notebook/INDEX.md', 'CODENAVI_WORKSPACE_STANDARD.md']) {
    if (!text.includes(phrase)) errors.push(`AGENT.md missing required contract: ${phrase}`);
  }
}

if (existsSync('AGENTS.md')) {
  const text = readFileSync('AGENTS.md', 'utf8');
  if (!text.includes('AGENT.md')) errors.push('AGENTS.md must point to canonical AGENT.md');
  if (!text.includes('CODENAVI_WORKSPACE_STANDARD.md')) errors.push('AGENTS.md must load CodENavi standard');
}

for (const path of required.filter(x => x.endsWith('/SKILL.md'))) {
  if (!existsSync(path)) continue;
  const text = readFileSync(path, 'utf8');
  if (!text.includes('Governance: CodENavi v1')) errors.push(`${path} missing CodENavi governance marker`);
}

if (errors.length) {
  console.error(JSON.stringify({ status: 'FAIL', errors }, null, 2));
  process.exit(1);
}

console.log(JSON.stringify({ status: 'PASS', standard: 'CodENavi v1', requiredFiles: required.length }, null, 2));
