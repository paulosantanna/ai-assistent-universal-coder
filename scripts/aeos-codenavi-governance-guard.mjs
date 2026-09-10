#!/usr/bin/env node
import { existsSync, readFileSync } from 'node:fs';

const required = [
  'AGENT.md',
  'AGENTS.md',
  '.notebook/INDEX.md',
  'references/CODENAVI_CONTINUITY_STANDARD.md',
  'skills/codenavi/SKILL.md',
  'skills/notebook-intelligence/SKILL.md',
  'skills/dependency-updater/SKILL.md',
  'skills/pr-reviewer/SKILL.md',
  'skills/docs-writer/SKILL.md',
  'skills/local-secret-vault/SKILL.md',
  'skills/jira-confluence-assistant/SKILL.md',
  'skills/java-version-expert/SKILL.md',
  'skills/continuity-bootstrapper/SKILL.md',
  'skills/handoff-manager/SKILL.md',
  'skills/memory-curator/SKILL.md',
  'skills/progress-tracker/SKILL.md',
  'skills/learning-curator/SKILL.md'
];

const errors = [];
for (const path of required) {
  if (!existsSync(path)) errors.push(`missing:${path}`);
}

const lifecycle = 'BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF';
const continuityTokens = [
  'CODENAVI_CONTINUITY_STANDARD.md',
  'HANDOFF.md',
  'MEMORY.md',
  'PROGRESS.md',
  'LEARNING.md'
];

if (existsSync('AGENT.md') && existsSync('AGENTS.md')) {
  const agent = readFileSync('AGENT.md', 'utf8');
  const agents = readFileSync('AGENTS.md', 'utf8');
  if (agent !== agents) errors.push('AGENT.md and AGENTS.md must be byte-identical canonical contracts');
  for (const phrase of [lifecycle, '.notebook/INDEX.md', ...continuityTokens]) {
    if (!agent.includes(phrase)) errors.push(`AGENT.md missing required contract: ${phrase}`);
  }
  if (!agent.includes('exactly **one** agent identity in AEOS: `codenavi-agent`')) {
    errors.push('AGENT.md must enforce the single codenavi-agent identity');
  }
}

for (const path of required.filter((x) => x.endsWith('/SKILL.md'))) {
  if (!existsSync(path)) continue;
  const text = readFileSync(path, 'utf8');
  if (!text.includes('Governance: CodENavi v1')) errors.push(`${path} missing CodENavi governance marker`);
}

if (errors.length) {
  console.error(JSON.stringify({ status: 'FAIL', standard: 'CodENavi v1', errors }, null, 2));
  process.exit(1);
}

console.log(JSON.stringify({
  status: 'PASS',
  standard: 'CodENavi v1',
  canonicalAgent: 'codenavi-agent',
  requiredFiles: required.length,
  continuityArtifacts: 4
}, null, 2));
