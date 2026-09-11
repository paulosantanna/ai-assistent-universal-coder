#!/usr/bin/env node
import { existsSync, readFileSync } from 'node:fs';

const errors = [];
const contractPath = 'aeos/governance/codenavi-artifact-contract.v1.json';
const runtimePath = 'runtime/src/kernel/codenavi-governance.ts';
const loaderPath = 'runtime/src/kernel/registry-loader.ts';

for (const path of [contractPath, runtimePath, loaderPath]) {
  if (!existsSync(path)) errors.push(`missing:${path}`);
}

function functionWindow(source, functionName) {
  const start = source.indexOf(`${functionName}(`);
  if (start < 0) return null;
  const nextMethod = source.indexOf('\n  ', start + functionName.length + 1);
  const end = nextMethod > start ? nextMethod : Math.min(source.length, start + 5000);
  return source.slice(start, end);
}

if (!errors.length) {
  const contract = JSON.parse(readFileSync(contractPath, 'utf8'));
  const runtime = readFileSync(runtimePath, 'utf8');
  const loader = readFileSync(loaderPath, 'utf8');
  const expectedLifecycle = ['BRIEFING', 'RECON', 'PLAN', 'EXECUTE', 'VERIFY', 'DEBRIEF'];

  if (contract.standard !== 'CodENavi Artifact Contract v1') errors.push('invalid artifact contract standard');
  if (JSON.stringify(contract.lifecycle) !== JSON.stringify(expectedLifecycle)) errors.push('invalid artifact lifecycle');
  for (const key of ['agent','skill','playbook','mcp','lcp','lsp','registry','blueprint','eval','memory_knowledge','runtime_tool','ci_release','documentation']) {
    if (!contract.artifact_types?.[key]) errors.push(`artifact type missing:${key}`);
  }
  for (const key of ['evidence_required','verification_required','freshness_required','fail_closed']) {
    if (contract.universal?.[key] !== true) errors.push(`universal invariant missing:${key}`);
  }
  if (!runtime.includes('CodENavi Artifact Contract v1')) errors.push('runtime governance standard mismatch');
  if (!runtime.includes('CodENavi Full Workspace v2')) errors.push('runtime governance parent mismatch');
  if (!runtime.includes('governEntry') || !runtime.includes('governEntries')) errors.push('runtime normalizer missing');

  const requiredLoaders = new Map([
    ['loadPlaybooks', ['governPlaybookEntries']],
    ['loadSkills', ['governSkillEntries']],
    ['loadMCPs', ['governEntries']],
    ['loadLCPs', ['governEntries']],
    ['loadAgents', ['governEntries']],
    ['loadBlueprints', ['governEntries']],
    ['loadWorkbenchProfiles', ['governEntries']],
    ['loadMergedFromOverlay', ['governEntries', 'governSkillEntries', 'governPlaybookEntries']]
  ]);
  for (const [fn, requiredNormalizers] of requiredLoaders) {
    const window = functionWindow(loader, fn);
    if (!window) {
      errors.push(`registry loader missing:${fn}`);
      continue;
    }
    for (const normalizer of requiredNormalizers) {
      if (!window.includes(normalizer)) errors.push(`${fn} missing required governance normalizer:${normalizer}`);
    }
  }

  const requiredResolvers = new Map([
    ['resolvePlaybook', ['governPlaybookEntries']],
    ['resolveSkills', ['governSkillEntries']],
    ['resolveMCPs', ['governEntries']],
    ['resolveLCPs', ['governEntries']],
    ['resolveAgent', ['governEntry']]
  ]);
  for (const [fn, requiredNormalizers] of requiredResolvers) {
    const window = functionWindow(loader, fn);
    if (!window) {
      errors.push(`resolver missing:${fn}`);
      continue;
    }
    for (const normalizer of requiredNormalizers) {
      if (!window.includes(normalizer)) errors.push(`${fn} missing required governance normalizer:${normalizer}`);
    }
  }
}

if (errors.length) {
  console.error(JSON.stringify({ status: 'FAIL', standard: 'CodENavi Artifact Contract v1', errors }, null, 2));
  process.exit(1);
}

console.log(JSON.stringify({
  status: 'PASS',
  standard: 'CodENavi Artifact Contract v1',
  parent: 'CodENavi Full Workspace v2',
  runtimeNormalization: true,
  registriesCovered: ['agents','subagents','skills','playbooks','mcps','lcps','blueprints','lsp/workbench-profiles'],
  lifecycle: ['BRIEFING','RECON','PLAN','EXECUTE','VERIFY','DEBRIEF']
}, null, 2));