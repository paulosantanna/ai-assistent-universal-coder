#!/usr/bin/env node
import { existsSync, readFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";
import {
  buildCriticalThinkingPlan,
  loadCriticalThinkingConfig,
  validateCriticalThinkingConfig
} from "./aeos-critical-thinking-governance.mjs";

const CODENAVI_AGENT_ID = "codenavi-agent";
const REGISTRY_ENTRY = /^[ \t]{0,2}-[ \t]+id:[ \t]*([^\n#]+)/m;

function parseSkillBlocks(text) {
  return text
    .split(/\n(?=[ \t]{0,2}-[ \t]+id:[ \t]+)/g)
    .filter((block) => REGISTRY_ENTRY.test(block))
    .map((block) => ({
      id: block.match(REGISTRY_ENTRY)?.[1]?.trim() ?? "",
      riskLevel: block.match(/^\s*risk_level:\s*([^\n]+)/m)?.[1]?.trim() ?? "",
      mission: block.match(/^\s*mission:\s*([^\n]+)/m)?.[1]?.trim() ?? ""
    }));
}

function conflictMarkers(text) {
  return /^(<<<<<<<|=======|>>>>>>>)(?:\s|$)/m.test(text);
}

export function validateCriticalThinkingGovernance(repoRoot = resolve(process.cwd())) {
  const config = loadCriticalThinkingConfig(repoRoot);
  const configValidation = validateCriticalThinkingConfig(config);
  const errors = [...configValidation.errors];
  const skillsRegistryPath = join(repoRoot, "aeos", "registries", "skills.registry.yaml");
  const agentsRegistryPath = join(repoRoot, "aeos", "registries", "agents.registry.yaml");
  const skillsText = readFileSync(skillsRegistryPath, "utf8");
  const agentsText = readFileSync(agentsRegistryPath, "utf8");
  const skills = parseSkillBlocks(skillsText);
  const skillIds = new Set(skills.map((skill) => skill.id));

  if (!skillIds.has(config.governing_skill)) {
    errors.push(`governing skill is not registered: ${config.governing_skill}`);
  }

  const agentIds = [...agentsText.matchAll(/^\s*- id:\s*([^\n]+)/gm)].map((match) => match[1].trim());
  if (agentIds.length !== 1 || agentIds[0] !== CODENAVI_AGENT_ID) {
    errors.push(`agent registry must contain only ${CODENAVI_AGENT_ID}`);
  }
  if (!agentsText.includes("path: AGENT.md")) errors.push(`${CODENAVI_AGENT_ID} must point to AGENT.md`);
  if (!/subagents:\s*\[\s*\]/m.test(agentsText)) errors.push("subagents must be an empty list");

  for (const lens of config.lenses) {
    if (!lens.prompt_id || !lens.id || !lens.name) errors.push("critical-thinking lens is incomplete");
    if (!Array.isArray(lens.triggers) || lens.triggers.length === 0) errors.push(`lens ${lens.id ?? "?"} has no triggers`);
  }

  const invalidRiskSkills = skills.filter((skill) => !["low", "medium", "high", "critical"].includes(skill.riskLevel));
  if (invalidRiskSkills.length > 0) {
    errors.push(`skills with invalid or missing risk level: ${invalidRiskSkills.map((skill) => skill.id).join(", ")}`);
  }

  const uncoveredSkills = skills.filter((skill) => {
    const plan = buildCriticalThinkingPlan({
      skillId: skill.id,
      riskLevel: skill.riskLevel,
      request: `Governar a execução da skill ${skill.id}`,
      mission: skill.mission,
      config
    });
    return plan.status !== "PASS";
  });
  if (uncoveredSkills.length > 0) {
    errors.push(`skills without a valid critical-thinking plan: ${uncoveredSkills.map((skill) => skill.id).join(", ")}`);
  }

  const governedFiles = [
    "AGENT.md",
    "AGENTS.md",
    "package.json",
    "aeos/registries/agents.registry.yaml",
    "aeos/registries/skills.registry.yaml",
    "aeos/config/critical-thinking-governance.config.json",
    "skills/critical-thinking-governor/SKILL.md",
    "scripts/aeos-critical-thinking-governance.mjs",
    "scripts/aeos-critical-thinking-guard.mjs",
    "runtime/src/kernel/critical-thinking-governor.ts",
    "runtime/src/kernel/playbook-engine.ts",
    "runtime/src/kernel/skill-executor.ts"
  ];
  for (const relativePath of governedFiles) {
    const absolutePath = join(repoRoot, relativePath);
    if (!existsSync(absolutePath)) {
      errors.push(`governed file not found: ${relativePath}`);
      continue;
    }
    if (conflictMarkers(readFileSync(absolutePath, "utf8"))) {
      errors.push(`merge conflict marker found in ${relativePath}`);
    }
  }

  return {
    status: errors.length === 0 ? "PASS" : "FAIL",
    governingSkill: config.governing_skill,
    lensesChecked: config.lenses.length,
    skillsChecked: skills.length,
    baselineLenses: config.baseline_lenses,
    maxLensesPerPlan: config.max_lenses,
    agentId: CODENAVI_AGENT_ID,
    errors
  };
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  const result = validateCriticalThinkingGovernance();
  const output = JSON.stringify(result, null, 2);
  if (result.status === "PASS") console.log(output);
  else {
    console.error(output);
    process.exit(1);
  }
}
