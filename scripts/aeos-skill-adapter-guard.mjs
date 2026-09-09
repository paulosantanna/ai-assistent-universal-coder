#!/usr/bin/env node
import { existsSync, readFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";
import yaml from "js-yaml";

const { load } = yaml;
const repoRoot = resolve(process.cwd());
const overlayIndex = join(repoRoot, "aeos", "registries", "overlay.registry.index.yaml");
const mcpsRegistry = join(repoRoot, "aeos", "registries", "mcps.registry.yaml");
const lspConfig = join(repoRoot, "aeos", "config", "lsp-universal-project.config.yaml");

function parseBlocks(text) {
  return text
    .split(/\n(?=\s*- id: )/g)
    .filter((block) => /^\s*- id: /m.test(block))
    .map((block) => ({
      id: block.match(/^\s*- id:\s*([^\n]+)/m)?.[1]?.trim() || "",
      governingSkill: block.match(/^\s*governing_skill:\s*([^\n]+)/m)?.[1]?.trim() || "",
      skillEnforced: block.match(/^\s*skill_enforced:\s*([^\n]+)/m)?.[1]?.trim() || ""
    }));
}

function loadEffectiveSkillIds() {
  const index = load(readFileSync(overlayIndex, "utf8"));
  const fragments = Array.isArray(index?.registry_fragments) ? index.registry_fragments : [];
  const skillIds = new Set();
  const scannedFragments = [];

  for (const fragment of fragments) {
    const relativePath = typeof fragment === "string" ? fragment : fragment?.path;
    if (!relativePath) continue;
    const absolutePath = resolve(repoRoot, relativePath);
    if (!existsSync(absolutePath)) continue;

    const parsed = load(readFileSync(absolutePath, "utf8"));
    if (!Array.isArray(parsed?.skills)) continue;

    scannedFragments.push(relativePath);
    for (const skill of parsed.skills) {
      if (typeof skill?.id === "string" && skill.id.trim()) skillIds.add(skill.id.trim());
    }
  }

  return { skillIds, scannedFragments };
}

function failure(message, details) {
  return { status: "FAIL", message, details };
}

export function validateSkillAdapters() {
  const { skillIds, scannedFragments } = loadEffectiveSkillIds();
  const mcpEntries = parseBlocks(readFileSync(mcpsRegistry, "utf8"));
  const lspProfiles = parseBlocks(readFileSync(lspConfig, "utf8"));

  const missingMcpSkills = mcpEntries.filter((entry) => !entry.governingSkill);
  const unknownMcpSkills = mcpEntries.filter((entry) => entry.governingSkill && !skillIds.has(entry.governingSkill));
  const unenforcedMcps = mcpEntries.filter((entry) => entry.skillEnforced !== "true");
  const missingLspSkills = lspProfiles.filter((entry) => !entry.governingSkill);
  const unknownLspSkills = lspProfiles.filter((entry) => entry.governingSkill && !skillIds.has(entry.governingSkill));

  if (missingMcpSkills.length > 0) return failure("Every MCP must declare governing_skill.", missingMcpSkills);
  if (unknownMcpSkills.length > 0) return failure("Every MCP governing_skill must exist in the effective overlay skill registry.", unknownMcpSkills);
  if (unenforcedMcps.length > 0) return failure("Every MCP must enforce skill context with skill_enforced: true.", unenforcedMcps);
  if (missingLspSkills.length > 0) return failure("Every LSP language profile must declare governing_skill.", missingLspSkills);
  if (unknownLspSkills.length > 0) return failure("Every LSP governing_skill must exist in the effective overlay skill registry.", unknownLspSkills);

  return {
    status: "PASS",
    effectiveSkillsChecked: skillIds.size,
    skillRegistryFragmentsChecked: scannedFragments.length,
    mcpsChecked: mcpEntries.length,
    lspProfilesChecked: lspProfiles.length,
    governingSkills: [...new Set([
      ...mcpEntries.map((entry) => entry.governingSkill),
      ...lspProfiles.map((entry) => entry.governingSkill)
    ])].sort()
  };
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  const result = validateSkillAdapters();
  const output = JSON.stringify(result, null, 2);
  if (result.status === "PASS") {
    console.log(output);
  } else {
    console.error(output);
    process.exit(1);
  }
}
