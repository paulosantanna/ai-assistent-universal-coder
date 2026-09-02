#!/usr/bin/env node
import { existsSync, readFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";
import {
  buildCriticalThinkingPlan,
  loadCriticalThinkingConfig,
  validateCriticalThinkingConfig
} from "./aeos-critical-thinking-governance.mjs";

function parseSkillBlocks(text) {
  return text
    .split(/\n(?=- id: )/g)
    .filter((block) => /^- id: /m.test(block))
    .map((block) => ({
      id: block.match(/^- id:\s*([^\n]+)/m)?.[1]?.trim() ?? "",
      riskLevel: block.match(/^\s*risk_level:\s*([^\n]+)/m)?.[1]?.trim() ?? "",
      mission: block.match(/^\s*mission:\s*([^\n]+)/m)?.[1]?.trim() ?? ""
    }));
}

function parseAgentBlocks(text) {
  return text
    .split(/\n(?=\s{2}- id: )/g)
    .filter((block) => /^\s{2}- id: /m.test(block))
    .map((block) => ({
      id: block.match(/^\s{2}- id:\s*([^\n]+)/m)?.[1]?.trim() ?? "",
      path: block.match(/^\s{4}path:\s*([^\n]+)/m)?.[1]?.trim() ?? "",
      role: block.match(/^\s{4}role:\s*([^\n]+)/m)?.[1]?.trim() ?? "",
      allowedMcps: block.match(/^\s{4}allowed_mcps:\s*([^\n]+)/m)?.[1]?.trim() ?? ""
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
  const registeredAgents = parseAgentBlocks(agentsText);
  const agentIndex = new Map(registeredAgents.map((agent) => [agent.id, agent]));
  const skillIds = new Set(skills.map((skill) => skill.id));

  if (!skillIds.has(config.governing_skill)) {
    errors.push(`governing skill is not registered: ${config.governing_skill}`);
  }

  const rootAgent = agentIndex.get("critical-thinking-root");
  if (!rootAgent) errors.push("critical-thinking-root is not registered");
  if (rootAgent && rootAgent.path !== "skills/critical-thinking-governor/AGENT.md") {
    errors.push("critical-thinking-root path is invalid");
  }

  for (const definition of config.agents) {
    const registered = agentIndex.get(definition.id);
    if (!registered) {
      errors.push(`critical-thinking agent is not registered: ${definition.id}`);
      continue;
    }
    if (registered.path !== definition.path) errors.push(`registry path mismatch for ${definition.id}`);
    if (registered.role !== "critical-thinking-specialist") errors.push(`invalid role for ${definition.id}`);
    if (registered.allowedMcps !== "[]") errors.push(`${definition.id} must have allowed_mcps: []`);
    const absolutePath = join(repoRoot, definition.path);
    if (!existsSync(absolutePath)) {
      errors.push(`agent contract not found: ${definition.path}`);
      continue;
    }
    const contract = readFileSync(absolutePath, "utf8");
    if (!contract.includes(definition.prompt_id)) errors.push(`agent contract missing prompt id ${definition.prompt_id}`);
    if (!contract.includes("Não execute ferramentas")) errors.push(`agent contract missing no-tool boundary: ${definition.id}`);
    if (conflictMarkers(contract)) errors.push(`merge conflict marker found in ${definition.path}`);
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
    "package.json",
    "aeos/registries/agents.registry.yaml",
    "aeos/registries/skills.registry.yaml",
    "aeos/config/critical-thinking-governance.config.json",
    "skills/critical-thinking-governor/SKILL.md",
    "skills/critical-thinking-governor/AGENT.md",
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
    specialistAgentsChecked: config.agents.length,
    skillsChecked: skills.length,
    baselineAgents: config.baseline_agents,
    maxAgentsPerPlan: config.max_agents,
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
