#!/usr/bin/env node
import { existsSync, readFileSync } from 'node:fs';

const errors = [];
const contractPath = 'aeos/governance/codenavi-artifact-contract.v1.json';
const runtimePath = 'runtime/src/kernel/codenavi-governance.ts';
const loaderPath = 'runtime/src/kernel/registry-loader.ts';

for (const path of [contractPath, runtimePath, loaderPath]) {
  if (!existsSync(path)) errors.push(`missing:${path}`);
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

  const requiredLoaders = ['loadPlaybooks','loadSkills','loadMCPs','loadLCPs','loadAgents','loadBlueprints','loadWorkbenchProfiles','loadMergedFromOverlay'];
  for (const fn of requiredLoaders) {
    const start = loader.indexOf(`${fn}(`);
    if (start < 0) {
      errors.push(`registry loader missing:${fn}`);
      continue;
    }
    const window = loader.slice(start, start + 900);
    if (!window.includes('governEntr')) errors.push(`${fn} does not normalize governance`);
  }

  for (const fn of ['resolvePlaybook','resolveSkills','resolveMCPs','resolveLCPs','resolveAgent']) {
    const start = loader.indexOf(`${fn}(`);
    if (start < 0) {
      errors.push(`resolver missing:${fn}`);
      continue;
    }
    const window = loader.slice(start, start + 700);
    if (!window.includes('governEntr')) errors.push(`${fn} may return ungoverned artifact`);
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
