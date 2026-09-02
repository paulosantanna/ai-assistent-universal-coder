import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { load } from "js-yaml";
import type {
  CriticalThinkingAgentDefinition,
  CriticalThinkingConfig,
  CriticalThinkingPlan,
  CriticalThinkingSelectedAgent,
  SkillRegistryEntry
} from "./types.js";

const CONFIG_PATH = join("aeos", "config", "critical-thinking-governance.config.json");
const VALID_RISK_LEVELS = new Set(["low", "medium", "high", "critical"]);

function normalize(value: unknown): string {
  return String(value ?? "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
}

function includesTerm(context: string, term: string): boolean {
  const normalizedTerm = normalize(term).trim();
  if (!normalizedTerm) return false;
  const escaped = normalizedTerm
    .replace(/[.*+?^${}()|[\]\\]/g, "\\$&")
    .replace(/\s+/g, "\\s+");
  return new RegExp(`(^|[^a-z0-9])${escaped}($|[^a-z0-9])`).test(context);
}

function unique(values: string[]): string[] {
  return [...new Set(values)];
}

function hash(value: string): string {
  return createHash("sha256").update(value).digest("hex");
}

export class CriticalThinkingGovernor {
  private readonly aeosRoot: string;
  private readonly config: CriticalThinkingConfig;

  constructor(aeosRoot: string, config?: CriticalThinkingConfig) {
    this.aeosRoot = resolve(aeosRoot);
    this.config = config ?? JSON.parse(
      readFileSync(join(this.aeosRoot, CONFIG_PATH), "utf8")
    ) as CriticalThinkingConfig;
  }

  planForSkill(skill: SkillRegistryEntry, request = ""): CriticalThinkingPlan {
    const configErrors = this.validateConfig();
    const riskLevel = normalize(skill.risk_level);

    if (configErrors.length > 0) {
      return this.failedPlan(skill.id, riskLevel, configErrors);
    }
    if (!VALID_RISK_LEVELS.has(riskLevel)) {
      return this.failedPlan(skill.id, riskLevel, [`unsupported risk level: ${skill.risk_level}`]);
    }

    const context = normalize(`${skill.id} ${skill.mission ?? ""} ${request}`);
    const byId = new Map(this.config.agents.map((agent) => [agent.id, agent]));
    const riskAgents = this.config.risk_overlays[riskLevel] ?? [];
    const requiredIds = unique([...this.config.baseline_agents, ...riskAgents]);
    const reasons = new Map<string, string>([
      ...this.config.baseline_agents.map((id) => [id, "baseline"] as const),
      ...riskAgents.map((id) => [id, `risk:${riskLevel}`] as const)
    ]);

    const triggered = this.config.agents
      .filter((agent) => !requiredIds.includes(agent.id))
      .map((agent) => {
        const matches = agent.triggers.filter((trigger) => includesTerm(context, trigger));
        const explicit = includesTerm(context, agent.id) || includesTerm(context, agent.name);
        const score = matches.reduce((total, trigger) => total + normalize(trigger).length, 0) + (explicit ? 1000 : 0);
        return { agent, matches, score };
      })
      .filter((candidate) => candidate.score > 0)
      .sort((left, right) => right.score - left.score || left.agent.order - right.agent.order);

    const selectedIds = [...requiredIds];
    for (const candidate of triggered) {
      if (selectedIds.length >= this.config.max_agents) break;
      selectedIds.push(candidate.agent.id);
      reasons.set(candidate.agent.id, `trigger:${candidate.matches.join("|") || "explicit"}`);
    }

    for (const agent of this.config.agents) {
      if (selectedIds.length >= this.config.min_agents) break;
      if (!selectedIds.includes(agent.id)) {
        selectedIds.push(agent.id);
        reasons.set(agent.id, "minimum-set");
      }
    }

    const selectedAgents = selectedIds
      .map((id) => byId.get(id))
      .filter((agent): agent is CriticalThinkingAgentDefinition => Boolean(agent))
      .sort((left, right) => left.order - right.order)
      .map<CriticalThinkingSelectedAgent>((agent) => ({
        id: agent.id,
        promptId: agent.prompt_id,
        name: agent.name,
        path: agent.path,
        reason: reasons.get(agent.id) ?? "selected"
      }));

    const blockingConditions: string[] = [];
    if (selectedAgents.length < this.config.min_agents) blockingConditions.push("selected agent count is below min_agents");
    if (selectedAgents.length > this.config.max_agents) blockingConditions.push("selected agent count exceeds max_agents");
    for (const id of requiredIds) {
      if (!selectedAgents.some((agent) => agent.id === id)) blockingConditions.push(`required agent missing: ${id}`);
    }

    const planData = {
      version: this.config.version,
      governingSkill: this.config.governing_skill,
      skillId: skill.id,
      riskLevel,
      selectedAgents,
      requiredOutputFields: this.config.required_output_fields,
      failClosed: this.config.fail_closed
    };

    return {
      status: blockingConditions.length === 0 ? "PASS" : "FAIL",
      ...planData,
      blockingConditions,
      planHash: hash(JSON.stringify(planData))
    };
  }

  private validateConfig(): string[] {
    const errors: string[] = [];
    const ids = this.config.agents.map((agent) => agent.id);
    const idSet = new Set(ids);
    const promptIds = this.config.agents.map((agent) => agent.prompt_id);
    const paths = this.config.agents.map((agent) => agent.path);
    const orders = this.config.agents.map((agent) => agent.order).sort((left, right) => left - right);
    const expectedOrders = Array.from({ length: 20 }, (_, index) => index + 1);
    if (this.config.scope !== "all_registered_skills") errors.push("scope must be all_registered_skills");
    if (this.config.fail_closed !== true) errors.push("fail_closed must be true");
    if (this.config.agents.length !== 20) errors.push(`expected 20 specialist agents, found ${this.config.agents.length}`);
    if (idSet.size !== ids.length) errors.push("agent ids must be unique");
    if (new Set(promptIds).size !== promptIds.length) errors.push("prompt ids must be unique");
    if (new Set(paths).size !== paths.length) errors.push("agent paths must be unique");
    if (JSON.stringify(orders) !== JSON.stringify(expectedOrders)) errors.push("agent orders must be the complete range 1..20");
    if (this.config.baseline_agents.length !== 4) errors.push("baseline_agents must contain exactly four agents");
    for (const id of this.config.baseline_agents) if (!idSet.has(id)) errors.push(`unknown baseline agent: ${id}`);
    if (this.config.min_agents < this.config.baseline_agents.length) errors.push("min_agents is below baseline size");
    if (this.config.max_agents < this.config.min_agents || this.config.max_agents >= 20) errors.push("max_agents is invalid");

    const agentsRegistry = load(
      readFileSync(join(this.aeosRoot, "aeos", "registries", "agents.registry.yaml"), "utf8")
    ) as { agents?: Array<{ id?: string; path?: string; role?: string; allowed_mcps?: string[] }> };
    const skillsRegistry = load(
      readFileSync(join(this.aeosRoot, "aeos", "registries", "skills.registry.yaml"), "utf8")
    ) as { skills?: Array<{ id?: string }> };
    const registeredAgents = new Map((agentsRegistry.agents ?? []).map((agent) => [agent.id, agent]));
    const registeredSkills = new Set((skillsRegistry.skills ?? []).map((skill) => skill.id));

    if (!registeredSkills.has(this.config.governing_skill)) {
      errors.push(`governing skill is not registered: ${this.config.governing_skill}`);
    }
    const rootAgent = registeredAgents.get("critical-thinking-root");
    if (!rootAgent || rootAgent.path !== "skills/critical-thinking-governor/AGENT.md") {
      errors.push("critical-thinking-root is missing or invalid");
    }

    for (const agent of this.config.agents) {
      const expectedPromptId = `CT-${String(agent.order).padStart(2, "0")}`;
      if (agent.prompt_id !== expectedPromptId) errors.push(`${agent.id} must use ${expectedPromptId}`);
      if (!existsSync(join(this.aeosRoot, agent.path))) errors.push(`agent contract not found: ${agent.path}`);
      const registered = registeredAgents.get(agent.id);
      if (!registered) errors.push(`critical-thinking agent is not registered: ${agent.id}`);
      else {
        if (registered.path !== agent.path) errors.push(`registry path mismatch for ${agent.id}`);
        if (registered.role !== "critical-thinking-specialist") errors.push(`invalid role for ${agent.id}`);
        if (!Array.isArray(registered.allowed_mcps) || registered.allowed_mcps.length !== 0) {
          errors.push(`${agent.id} must not have MCP access`);
        }
      }
    }
    return errors;
  }

  private failedPlan(skillId: string, riskLevel: string, errors: string[]): CriticalThinkingPlan {
    return {
      status: "FAIL",
      version: this.config.version ?? "unknown",
      governingSkill: this.config.governing_skill ?? "critical-thinking-governor",
      skillId,
      riskLevel,
      selectedAgents: [],
      requiredOutputFields: this.config.required_output_fields ?? [],
      failClosed: true,
      blockingConditions: errors,
      planHash: hash(JSON.stringify(errors))
    };
  }
}
