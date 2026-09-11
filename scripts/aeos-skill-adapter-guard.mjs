#!/usr/bin/env node
import { existsSync, readFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const repoRoot = resolve(process.cwd());
const overlayIndex = join(repoRoot, "aeos", "registries", "overlay.registry.index.yaml");
const skillsRegistry = join(repoRoot, "aeos", "registries", "skills.registry.yaml");
const mcpsRegistry = join(repoRoot, "aeos", "registries", "mcps.registry.yaml");
const lspConfig = join(repoRoot, "aeos", "config", "lsp-universal-project.config.yaml");

function parseIds(text) {
  return new Set([...text.matchAll(/^[ \t]{0,2}-[ \t]+id:[ \t]*([^\n#]+)/gm)].map((match) => match[1].trim()));
}

function parseBlocks(text) {
  return text.split(/\n(?=\s*- id: )/g).filter((block) => /^\s*- id: /m.test(block)).map((block) => ({
    id: block.match(/^\s*- id:\s*([^\n]+)/m)?.[1]?.trim() || "",
    governingSkill: block.match(/^\s*governing_skill:\s*([^\n]+)/m)?.[1]?.trim() || "",
    skillEnforced: block.match(/^\s*skill_enforced:\s*([^\n]+)/m)?.[1]?.trim() || ""
  }));
}

function activeFragments(topLevelKey, fallbackPath) {
  const paths = [];
  if (existsSync(overlayIndex)) {
    const indexText = readFileSync(overlayIndex, "utf8");
    for (const match of indexText.matchAll(/^\s*-\s+path:\s*([^\n#]+)$/gm)) {
      const relative = match[1].trim().replace(/^['"]|['"]$/g, "");
      const absolute = resolve(repoRoot, relative);
      if (!existsSync(absolute)) continue;
      const text = readFileSync(absolute, "utf8");
      if (new RegExp(`^${topLevelKey}:\\s*$`, "m").test(text)) paths.push(absolute);
    }
  }
  if (!paths.includes(fallbackPath) && existsSync(fallbackPath)) paths.unshift(fallbackPath);
  return paths;
}

function failure(message, details) { return { status: "FAIL", message, details }; }

export function validateSkillAdapters() {
  const skillIds = new Set();
  for (const fragment of activeFragments("skills", skillsRegistry)) for (const id of parseIds(readFileSync(fragment, "utf8"))) skillIds.add(id);
  const mcpById = new Map();
  for (const fragment of activeFragments("mcps", mcpsRegistry)) for (const entry of parseBlocks(readFileSync(fragment, "utf8"))) mcpById.set(entry.id, entry);
  const mcpEntries = [...mcpById.values()];
  const lspProfiles = parseBlocks(readFileSync(lspConfig, "utf8"));

  const missingMcpSkills = mcpEntries.filter((entry) => !entry.governingSkill);
  const unknownMcpSkills = mcpEntries.filter((entry) => entry.governingSkill && !skillIds.has(entry.governingSkill));
  const unenforcedMcps = mcpEntries.filter((entry) => entry.skillEnforced !== "true");
  const missingLspSkills = lspProfiles.filter((entry) => !entry.governingSkill);
  const unknownLspSkills = lspProfiles.filter((entry) => entry.governingSkill && !skillIds.has(entry.governingSkill));

  if (missingMcpSkills.length > 0) return failure("Every MCP must declare governing_skill.", missingMcpSkills);
  if (unknownMcpSkills.length > 0) return failure("Every MCP governing_skill must exist in the active skill overlay registry.", unknownMcpSkills);
  if (unenforcedMcps.length > 0) return failure("Every MCP must enforce skill context with skill_enforced: true.", unenforcedMcps);
  if (missingLspSkills.length > 0) return failure("Every LSP language profile must declare governing_skill.", missingLspSkills);
  if (unknownLspSkills.length > 0) return failure("Every LSP governing_skill must exist in the active skill overlay registry.", unknownLspSkills);

  return {
    status: "PASS",
    skillsChecked: skillIds.size,
    mcpsChecked: mcpEntries.length,
    lspProfilesChecked: lspProfiles.length,
    governingSkills: [...new Set([...mcpEntries.map((entry) => entry.governingSkill), ...lspProfiles.map((entry) => entry.governingSkill)])].sort()
  };
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  const result = validateSkillAdapters();
  const output = JSON.stringify(result, null, 2);
  if (result.status === "PASS") console.log(output);
  else { console.error(output); process.exit(1); }
}
