#!/usr/bin/env node
import { readFileSync } from "node:fs";
import { join, resolve } from "node:path";

const repoRoot = resolve(process.cwd());
const skillsRegistry = join(repoRoot, "aeos", "registries", "skills.registry.yaml");
const mcpsRegistry = join(repoRoot, "aeos", "registries", "mcps.registry.yaml");
const lspConfig = join(repoRoot, "aeos", "config", "lsp-universal-project.config.yaml");

function parseIds(text) {
  return new Set([...text.matchAll(/^- id:\s*([^\n]+)/gm)].map((match) => match[1].trim()));
}

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

function fail(message, details) {
  console.error(JSON.stringify({ status: "FAIL", message, details }, null, 2));
  process.exit(1);
}

const skillIds = parseIds(readFileSync(skillsRegistry, "utf8"));
const mcpEntries = parseBlocks(readFileSync(mcpsRegistry, "utf8"));
const lspProfiles = parseBlocks(readFileSync(lspConfig, "utf8"));

const missingMcpSkills = mcpEntries.filter((entry) => !entry.governingSkill);
const unknownMcpSkills = mcpEntries.filter((entry) => entry.governingSkill && !skillIds.has(entry.governingSkill));
const unenforcedMcps = mcpEntries.filter((entry) => entry.skillEnforced !== "true");
const missingLspSkills = lspProfiles.filter((entry) => !entry.governingSkill);
const unknownLspSkills = lspProfiles.filter((entry) => entry.governingSkill && !skillIds.has(entry.governingSkill));

if (missingMcpSkills.length > 0) {
  fail("Every MCP must declare governing_skill.", missingMcpSkills);
}

if (unknownMcpSkills.length > 0) {
  fail("Every MCP governing_skill must exist in aeos/registries/skills.registry.yaml.", unknownMcpSkills);
}

if (unenforcedMcps.length > 0) {
  fail("Every MCP must enforce skill context with skill_enforced: true.", unenforcedMcps);
}

if (missingLspSkills.length > 0) {
  fail("Every LSP language profile must declare governing_skill.", missingLspSkills);
}

if (unknownLspSkills.length > 0) {
  fail("Every LSP governing_skill must exist in aeos/registries/skills.registry.yaml.", unknownLspSkills);
}

console.log(JSON.stringify({
  status: "PASS",
  mcpsChecked: mcpEntries.length,
  lspProfilesChecked: lspProfiles.length,
  governingSkills: [...new Set([
    ...mcpEntries.map((entry) => entry.governingSkill),
    ...lspProfiles.map((entry) => entry.governingSkill)
  ])].sort()
}, null, 2));
