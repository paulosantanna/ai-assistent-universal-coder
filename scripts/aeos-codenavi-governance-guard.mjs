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

const lifecycle = 'BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF';
const canonicalAgent = 'codenavi-agent';

if (existsSync('AGENT.md') && existsSync('AGENTS.md')) {
  const agent = readFileSync('AGENT.md', 'utf8');
  const agents = readFileSync('AGENTS.md', 'utf8');

  // In the single-agent model both discovery filenames are canonical mirrors.
  // Requiring one file to point at the other would reintroduce the obsolete shim model.
  if (agent !== agents) errors.push('AGENT.md and AGENTS.md must be byte-identical canonical mirrors');

  for (const [name, text] of [['AGENT.md', agent], ['AGENTS.md', agents]]) {
    for (const phrase of [lifecycle, '.notebook/INDEX.md', canonicalAgent]) {
      if (!text.includes(phrase)) errors.push(`${name} missing required single-agent contract: ${phrase}`);
    }
    if (!text.includes('exactly **one** agent identity')) {
      errors.push(`${name} must declare the single-agent invariant`);
    }
  }
}

for (const path of required.filter((x) => x.endsWith('/SKILL.md'))) {
  if (!existsSync(path)) continue;
  const text = readFileSync(path, 'utf8');
  const governed = text.includes('Governance: CodENavi v1') || text.includes('Governance: CodENavi Image Standard');
  if (!governed) errors.push(`${path} missing CodENavi governance marker`);
}

if (errors.length) {
  console.error(JSON.stringify({ status: 'FAIL', standard: 'CodENavi Single Agent', canonicalAgent, errors }, null, 2));
  process.exit(1);
}

console.log(JSON.stringify({
  status: 'PASS',
  standard: 'CodENavi Single Agent',
  canonicalAgent,
  canonicalMirrors: ['AGENT.md', 'AGENTS.md'],
  requiredFiles: required.length
}, null, 2));
