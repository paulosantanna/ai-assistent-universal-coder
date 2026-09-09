import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { load } from "js-yaml";
import type {
  CriticalThinkingConfig,
  CriticalThinkingLensDefinition,
  CriticalThinkingPlan,
  CriticalThinkingSelectedLens,
  SkillRegistryEntry
} from "./types.js";

const CONFIG_PATH = join("aeos", "config", "critical-thinking-governance.config.json");
const VALID_RISK_LEVELS = new Set(["low", "medium", "high", "critical"]);
const CODENAVI_AGENT_ID = "codenavi-agent";

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
    const byId = new Map(this.config.lenses.map((lens) => [lens.id, lens]));
    const riskLenses = this.config.risk_overlays[riskLevel] ?? [];
    const requiredIds = unique([...this.config.baseline_lenses, ...riskLenses]);
    const reasons = new Map<string, string>([
      ...this.config.baseline_lenses.map((id) => [id, "baseline"] as const),
      ...riskLenses.map((id) => [id, `risk:${riskLevel}`] as const)
    ]);

    const triggered = this.config.lenses
      .filter((lens) => !requiredIds.includes(lens.id))
      .map((lens) => {
        const matches = lens.triggers.filter((trigger) => includesTerm(context, trigger));
        const explicit = includesTerm(context, lens.id) || includesTerm(context, lens.name);
        const score = matches.reduce((total, trigger) => total + normalize(trigger).length, 0) + (explicit ? 1000 : 0);
        return { lens, matches, score };
      })
      .filter((candidate) => candidate.score > 0)
      .sort((left, right) => right.score - left.score || left.lens.order - right.lens.order);

    const selectedIds = [...requiredIds];
    for (const candidate of triggered) {
      if (selectedIds.length >= this.config.max_lenses) break;
      selectedIds.push(candidate.lens.id);
      reasons.set(candidate.lens.id, `trigger:${candidate.matches.join("|") || "explicit"}`);
    }

    for (const lens of this.config.lenses) {
      if (selectedIds.length >= this.config.min_lenses) break;
      if (!selectedIds.includes(lens.id)) {
        selectedIds.push(lens.id);
        reasons.set(lens.id, "minimum-set");
      }
    }

    const selectedLenses = selectedIds
      .map((id) => byId.get(id))
      .filter((lens): lens is CriticalThinkingLensDefinition => Boolean(lens))
      .sort((left, right) => left.order - right.order)
      .map<CriticalThinkingSelectedLens>((lens) => ({
        id: lens.id,
        promptId: lens.prompt_id,
        name: lens.name,
        reason: reasons.get(lens.id) ?? "selected"
      }));

    const blockingConditions: string[] = [];
    if (selectedLenses.length < this.config.min_lenses) blockingConditions.push("selected lens count is below min_lenses");
    if (selectedLenses.length > this.config.max_lenses) blockingConditions.push("selected lens count exceeds max_lenses");
    for (const id of requiredIds) {
      if (!selectedLenses.some((lens) => lens.id === id)) blockingConditions.push(`required lens missing: ${id}`);
    }

    const planData = {
      version: this.config.version,
      governingSkill: this.config.governing_skill,
      skillId: skill.id,
      riskLevel,
      selectedLenses,
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
    const ids = this.config.lenses.map((lens) => lens.id);
    const idSet = new Set(ids);
    const promptIds = this.config.lenses.map((lens) => lens.prompt_id);
    const orders = this.config.lenses.map((lens) => lens.order).sort((left, right) => left - right);
    const expectedOrders = Array.from({ length: 20 }, (_, index) => index + 1);

    if (this.config.scope !== "all_registered_skills") errors.push("scope must be all_registered_skills");
    if (this.config.fail_closed !== true) errors.push("fail_closed must be true");
    if (this.config.lenses.length !== 20) errors.push(`expected 20 critical-thinking lenses, found ${this.config.lenses.length}`);
    if (idSet.size !== ids.length) errors.push("lens ids must be unique");
    if (new Set(promptIds).size !== promptIds.length) errors.push("lens prompt ids must be unique");
    if (JSON.stringify(orders) !== JSON.stringify(expectedOrders)) errors.push("lens orders must be the complete range 1..20");
    if (this.config.baseline_lenses.length !== 4) errors.push("baseline_lenses must contain exactly four lenses");
    for (const id of this.config.baseline_lenses) if (!idSet.has(id)) errors.push(`unknown baseline lens: ${id}`);
    if (this.config.min_lenses < this.config.baseline_lenses.length) errors.push("min_lenses is below baseline size");
    if (this.config.max_lenses < this.config.min_lenses || this.config.max_lenses >= 20) errors.push("max_lenses is invalid");

    const agentsRegistry = load(
      readFileSync(join(this.aeosRoot, "aeos", "registries", "agents.registry.yaml"), "utf8")
    ) as { agents?: Array<{ id?: string; path?: string }>; subagents?: unknown[] };
    const skillsRegistry = load(
      readFileSync(join(this.aeosRoot, "aeos", "registries", "skills.registry.yaml"), "utf8")
    ) as { skills?: Array<{ id?: string }> };
    const registeredAgents = agentsRegistry.agents ?? [];
    const registeredSkills = new Set((skillsRegistry.skills ?? []).map((skill) => skill.id));

    if (!registeredSkills.has(this.config.governing_skill)) {
      errors.push(`governing skill is not registered: ${this.config.governing_skill}`);
    }
    if (registeredAgents.length !== 1 || registeredAgents[0]?.id !== CODENAVI_AGENT_ID) {
      errors.push(`agent registry must contain only ${CODENAVI_AGENT_ID}`);
    }
    if (registeredAgents[0]?.path !== "AGENT.md") errors.push(`${CODENAVI_AGENT_ID} must point to AGENT.md`);
    if ((agentsRegistry.subagents ?? []).length !== 0) errors.push("subagents are forbidden by the CodENavi single-agent standard");

    for (const lens of this.config.lenses) {
      const expectedPromptId = `CT-${String(lens.order).padStart(2, "0")}`;
      if (lens.prompt_id !== expectedPromptId) errors.push(`${lens.id} must use ${expectedPromptId}`);
      if (!Array.isArray(lens.triggers) || lens.triggers.length === 0) errors.push(`${lens.id} must declare triggers`);
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
      selectedLenses: [],
      requiredOutputFields: this.config.required_output_fields ?? [],
      failClosed: true,
      blockingConditions: errors,
      planHash: hash(JSON.stringify(errors))
    };
  }
}
