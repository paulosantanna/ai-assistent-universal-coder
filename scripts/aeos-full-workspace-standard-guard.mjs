#!/usr/bin/env node
import { existsSync, readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';

const manifestPath = 'aeos/governance/workspace-governance.manifest.json';
const errors = [];

function norm(p) {
  const value = String(p ?? '').replaceAll('\\', '/').replace(/^\.\//, '').replace(/\/$/, '');
  return value === '' ? '.' : value;
}

function under(file, root) {
  file = norm(file);
  root = norm(root);
  if (root === '.') return true;
  return file === root || file.startsWith(`${root}/`);
}

function contractPath(root) {
  return norm(root) === '.' ? 'AGENT.md' : `${norm(root)}/AGENT.md`;
}

function readText(file) {
  try { return readFileSync(file, 'utf8'); } catch { return ''; }
}

if (!existsSync(manifestPath)) {
  console.error(JSON.stringify({ status: 'FAIL', errors: [`missing:${manifestPath}`] }, null, 2));
  process.exit(1);
}

const manifest = JSON.parse(readText(manifestPath));
const requiredRootFiles = [
  'AGENT.md',
  'AGENTS.md',
  'references/CODENAVI_WORKSPACE_STANDARD.md',
  'references/CODENAVI_FULL_WORKSPACE_STANDARD.md',
  'references/CODENAVI_NOTEBOOK_SPEC.md',
  '.notebook/INDEX.md'
];

for (const file of requiredRootFiles) {
  if (!existsSync(file)) errors.push(`missing:${file}`);
}

const rootContract = readText('AGENT.md');
for (const phrase of [
  manifest.standard,
  manifest.requiredLifecycle,
  'skills',
  'playbooks',
  'MCP',
  'LCP',
  'LSP',
  'registries',
  'blueprints',
  'evals',
  'runtime',
  'policies',
  'CI/CD'
]) {
  if (!rootContract.toLowerCase().includes(String(phrase).toLowerCase())) {
    errors.push(`AGENT.md missing full-workspace scope: ${phrase}`);
  }
}

const allTracked = execFileSync('git', ['ls-files', '-z'], { encoding: 'utf8' })
  .split('\0')
  .filter(Boolean)
  .map(norm);

const ignored = (file) => (manifest.ignoredPathPrefixes || []).some(prefix => under(file, prefix));
const governed = allTracked.filter(file =>
  !ignored(file) && (manifest.governedRoots || []).some(root => under(file, root))
);

if (manifest.coveragePolicy === 'all-tracked-files-governed-by-default') {
  const unexpectedlyOutside = allTracked.filter(file => !ignored(file) && !governed.includes(file));
  for (const file of unexpectedlyOutside) errors.push(`tracked file escaped governance:${file}`);
}

const localContracts = new Map();
for (const root of manifest.localContractRoots || []) {
  const contract = contractPath(root);
  if (!existsSync(contract)) {
    errors.push(`missing local governance contract:${contract}`);
    continue;
  }
  const text = readText(contract);
  localContracts.set(norm(root), { contract, text });
  if (!text.includes(manifest.standard)) errors.push(`${contract} missing standard marker:${manifest.standard}`);
  if (contract !== 'AGENT.md' && !text.includes('AGENT.md')) errors.push(`${contract} must chain to root AGENT.md`);
  if (!text.includes('CODENAVI_FULL_WORKSPACE_STANDARD.md')) errors.push(`${contract} must chain to full workspace standard`);
}

function effectiveGovernance(file) {
  return [...localContracts.entries()]
    .filter(([root]) => under(file, root))
    .sort((a, b) => norm(b[0]).length - norm(a[0]).length)
    .find(([, value]) => value.text.includes(manifest.standard));
}

let legacyInheritedAgents = 0;
let explicitV2Agents = 0;
for (const file of governed.filter(f => /(^|\/)(AGENT|AGENTS)\.md$/i.test(f))) {
  const text = readText(file);
  if (text.includes(manifest.standard)) {
    explicitV2Agents += 1;
    continue;
  }
  const inherited = effectiveGovernance(file);
  if (!inherited) {
    errors.push(`${file} has no effective CodENavi v2 ancestor contract`);
    continue;
  }
  // Preserve specialized legacy instructions, but root/local v2 governance has higher precedence.
  legacyInheritedAgents += 1;
}

for (const file of governed) {
  const coverage = effectiveGovernance(file);
  if (!coverage) errors.push(`ungoverned tracked artifact:${file}`);
}

const counts = {
  totalTracked: allTracked.length,
  totalGoverned: governed.length,
  ignored: allTracked.length - governed.length,
  explicitV2Agents,
  legacyInheritedAgents
};
for (const [kind, markers] of Object.entries(manifest.artifactMatchers || {})) {
  counts[kind] = governed.filter(file => markers.some(marker => file.toLowerCase().includes(marker.toLowerCase()))).length;
}

const fullStandard = readText(manifest.standardPath);
for (const section of [
  'Agents and subagents',
  'Skills',
  'Playbooks',
  'MCPs/tools/provider adapters',
  'LCPs / LSP / language intelligence',
  'Registries / overlays / manifests',
  'Policies / permissions / configuration',
  'Blueprints / architecture artifacts',
  'Evals / tests',
  'Memory / knowledge / notebook',
  'Runtime / routers / executors',
  'CI/CD / release automation',
  'Documentation'
]) {
  if (!fullStandard.includes(section)) errors.push(`full standard missing section:${section}`);
}

if (errors.length) {
  console.error(JSON.stringify({ status: 'FAIL', standard: manifest.standard, coveragePolicy: manifest.coveragePolicy, counts, errors }, null, 2));
  process.exit(1);
}

console.log(JSON.stringify({
  status: 'PASS',
  standard: manifest.standard,
  coveragePolicy: manifest.coveragePolicy,
  lifecycle: manifest.requiredLifecycle,
  governedRoots: manifest.governedRoots.length,
  localContracts: manifest.localContractRoots.length,
  counts
}, null, 2));
