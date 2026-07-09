import { existsSync } from "node:fs";
import { resolve } from "node:path";
import type {
  AeosConfig,
  CapabilitiesConfig,
  PermissionsConfig,
  PoliciesConfig,
  PlaybooksRegistry,
  SkillsRegistry,
  MCPsRegistry,
  LCPsRegistry,
  AgentsRegistry,
  BlueprintsRegistry,
  WorkbenchProfilesRegistry,
  EnterpriseSkillsRegistry,
  EnterprisePlaybooksRegistry,
  OverlayRegistryIndex,
  MergeResult,
  PlaybookRegistryEntry,
  SkillRegistryEntry,
  AgentRegistryEntry,
  SubAgentRegistryEntry,
  CrossReferenceIssue,
  CrossReferenceValidation,
  ValidationResult
} from "./types.js";

export class SchemaValidator {
  private aeosRoot: string;

  constructor(aeosRoot: string = ".") {
    this.aeosRoot = resolve(aeosRoot);
  }

  validateAeosConfig(config: unknown): ValidationResult {
    const errors: string[] = [];
    const warnings: string[] = [];
    const c = config as AeosConfig;

    if (!c || typeof c !== "object") {
      errors.push("Config must be an object");
      return { valid: false, errors, warnings };
    }
    if (!c.aeos?.name) errors.push("Missing aeos.name");
    if (!c.aeos?.version) errors.push("Missing aeos.version");
    if (!c.registries?.agents) errors.push("Missing registries.agents");
    if (!c.registries?.skills) errors.push("Missing registries.skills");
    if (!c.registries?.playbooks) errors.push("Missing registries.playbooks");
    if (!c.registries?.mcps) errors.push("Missing registries.mcps");
    if (!c.registries?.lcps) errors.push("Missing registries.lcps");
    if (c.runtime?.require_judge && c.judge?.min_score === undefined) warnings.push("Using default judge min_score: 9.0");
    if (c.execution?.default_mode !== "dry-run-first") warnings.push("Execution mode is not dry-run-first");
    if (!c.execution?.allow_direct_write) warnings.push("Direct write disabled as expected");

    return { valid: errors.length === 0, errors, warnings };
  }

  validateCapabilities(config: unknown): ValidationResult {
    const errors: string[] = [];
    const warnings: string[] = [];
    const c = config as CapabilitiesConfig;

    if (!c?.capabilities || !Array.isArray(c.capabilities)) {
      errors.push("capabilities must be an array");
      return { valid: false, errors, warnings };
    }

    for (const cap of c.capabilities) {
      if (!cap.id) errors.push("Capability missing id");
      if (!cap.name) errors.push(`Capability ${cap.id ?? "?"} missing name`);
      if (!cap.risk_level) warnings.push(`Capability ${cap.id} missing risk_level`);
    }

    return { valid: errors.length === 0, errors, warnings };
  }

  validatePermissions(config: unknown): ValidationResult {
    const errors: string[] = [];
    const warnings: string[] = [];
    const c = config as PermissionsConfig;

    if (!c?.permissions) {
      errors.push("Missing permissions root");
      return { valid: false, errors, warnings };
    }
    if (c.permissions.default_policy !== "deny-all") {
      warnings.push("Default policy is not deny-all");
    }
    if (!c.permissions.agent_to_mcp?.length) {
      warnings.push("No agent_to_mcp permissions defined");
    }

    return { valid: errors.length === 0, errors, warnings };
  }

  validatePolicies(config: unknown): ValidationResult {
    const errors: string[] = [];
    const warnings: string[] = [];
    const c = config as PoliciesConfig;

    if (!c?.policies) {
      errors.push("Missing policies root");
      return { valid: false, errors, warnings };
    }

    return { valid: errors.length === 0, errors, warnings };
  }

  validatePlaybooksRegistry(config: unknown): ValidationResult {
    const errors: string[] = [];
    const warnings: string[] = [];
    const c = config as PlaybooksRegistry;

    if (!c?.playbooks || !Array.isArray(c.playbooks)) {
      errors.push("playbooks must be an array");
      return { valid: false, errors, warnings };
    }

    const ids = new Set<string>();
    for (const pb of c.playbooks) {
      if (!pb.id) errors.push("Playbook missing id");
      else if (ids.has(pb.id)) errors.push(`Duplicate playbook id: ${pb.id}`);
      else ids.add(pb.id);

      if (!pb.path) errors.push(`Playbook ${pb.id ?? "?"} missing path`);
      else if (!this.fileExists(pb.path)) warnings.push(`Playbook file not found: ${pb.path}`);
      if (!pb.required_agents?.length) warnings.push(`Playbook ${pb.id} has no required agents`);
      if (!pb.required_skills?.length) warnings.push(`Playbook ${pb.id} has no required skills`);
    }

    return { valid: errors.length === 0, errors, warnings };
  }

  validateSkillsRegistry(config: unknown): ValidationResult {
    const errors: string[] = [];
    const warnings: string[] = [];
    const c = config as SkillsRegistry;

    if (!c?.skills || !Array.isArray(c.skills)) {
      errors.push("skills must be an array");
      return { valid: false, errors, warnings };
    }

    const ids = new Set<string>();
    for (const sk of c.skills) {
      if (!sk.id) errors.push("Skill missing id");
      else if (ids.has(sk.id)) errors.push(`Duplicate skill id: ${sk.id}`);
      else ids.add(sk.id);

      if (!sk.path) errors.push(`Skill ${sk.id ?? "?"} missing path`);
      else if (!this.fileExists(sk.path)) warnings.push(`Skill file not found: ${sk.path}`);
      if (!sk.capabilities?.length) warnings.push(`Skill ${sk.id} has no capabilities`);
    }

    return { valid: errors.length === 0, errors, warnings };
  }

  validateMCPsRegistry(config: unknown): ValidationResult {
    const errors: string[] = [];
    const warnings: string[] = [];
    const c = config as MCPsRegistry;

    if (!c?.mcps || !Array.isArray(c.mcps)) {
      errors.push("mcps must be an array");
      return { valid: false, errors, warnings };
    }

    const ids = new Set<string>();
    for (const mcp of c.mcps) {
      if (!mcp.id) errors.push("MCP missing id");
      else if (ids.has(mcp.id)) errors.push(`Duplicate MCP id: ${mcp.id}`);
      else ids.add(mcp.id);

      if (mcp.risk_level === "critical" && !mcp.approval_required) {
        errors.push(`Critical MCP ${mcp.id} must have approval_required`);
      }
      if (mcp.config && !this.fileExists(mcp.config)) {
        warnings.push(`MCP config file not found: ${mcp.config}`);
      }
    }

    return { valid: errors.length === 0, errors, warnings };
  }

  validateLCPsRegistry(config: unknown): ValidationResult {
    const errors: string[] = [];
    const warnings: string[] = [];
    const c = config as LCPsRegistry;

    if (!c?.lcps || !Array.isArray(c.lcps)) {
      errors.push("lcps must be an array");
      return { valid: false, errors, warnings };
    }

    const ids = new Set<string>();
    for (const lcp of c.lcps) {
      if (!lcp.id) errors.push("LCP missing id");
      else if (ids.has(lcp.id)) errors.push(`Duplicate LCP id: ${lcp.id}`);
      else ids.add(lcp.id);

      if (lcp.path && !this.fileExists(lcp.path)) {
        warnings.push(`LCP file not found: ${lcp.path}`);
      }
    }

    return { valid: errors.length === 0, errors, warnings };
  }

  validateAgentsRegistry(config: unknown): ValidationResult {
    const errors: string[] = [];
    const warnings: string[] = [];
    const c = config as AgentsRegistry;

    if (!c?.agents || !Array.isArray(c.agents)) {
      errors.push("agents must be an array");
      return { valid: false, errors, warnings };
    }

    const ids = new Set<string>();
    for (const agent of c.agents) {
      if (!agent.id) errors.push("Agent missing id");
      else if (ids.has(agent.id)) errors.push(`Duplicate agent id: ${agent.id}`);
      else ids.add(agent.id);

      if (agent.path && !this.fileExists(agent.path)) {
        warnings.push(`Agent file not found: ${agent.path}`);
      }
      if (agent.role === "judge" && !agent.independence) {
        warnings.push(`Judge agent ${agent.id} should have independence: strict`);
      }
    }

    return { valid: errors.length === 0, errors, warnings };
  }

  validateBlueprintsRegistry(config: unknown): ValidationResult {
    const errors: string[] = [];
    const warnings: string[] = [];
    const c = config as BlueprintsRegistry;

    if (!c?.blueprints || !Array.isArray(c.blueprints)) {
      errors.push("blueprints must be an array");
      return { valid: false, errors, warnings };
    }

    for (const bp of c.blueprints) {
      if (!bp.id) errors.push("Blueprint missing id");
      if (bp.path && !this.fileExists(bp.path)) {
        warnings.push(`Blueprint file not found: ${bp.path}`);
      }
    }

    return { valid: errors.length === 0, errors, warnings };
  }

  validateWorkbenchProfilesRegistry(config: unknown): ValidationResult {
    const errors: string[] = [];
    const warnings: string[] = [];
    const c = config as WorkbenchProfilesRegistry;

    if (!c?.profiles || !Array.isArray(c.profiles)) {
      errors.push("profiles must be an array");
      return { valid: false, errors, warnings };
    }

    const ids = new Set<string>();
    for (const p of c.profiles) {
      if (!p.id) errors.push("Profile missing id");
      else if (ids.has(p.id)) errors.push(`Duplicate profile id: ${p.id}`);
      else ids.add(p.id);
    }

    return { valid: errors.length === 0, errors, warnings };
  }

  validateEnterpriseSkillsRegistry(config: unknown): ValidationResult {
    return this.validateSkillsRegistry(config);
  }

  validateEnterprisePlaybooksRegistry(config: unknown): ValidationResult {
    return this.validatePlaybooksRegistry(config);
  }

  validateOverlayRegistryIndex(config: unknown): ValidationResult {
    const errors: string[] = [];
    const warnings: string[] = [];
    const c = config as OverlayRegistryIndex;

    if (!c?.registry_fragments || !Array.isArray(c.registry_fragments)) {
      errors.push("registry_fragments must be an array");
      return { valid: false, errors, warnings };
    }

    for (const f of c.registry_fragments) {
      if (!f.path) errors.push("Fragment missing path");
      else if (!this.fileExists(f.path)) warnings.push(`Fragment not found: ${f.path}`);
    }

    return { valid: errors.length === 0, errors, warnings };
  }

  crossReferenceValidations(
    allAgents: AgentRegistryEntry[],
    allSkills: SkillRegistryEntry[],
    allPlaybooks: PlaybookRegistryEntry[],
    allMCPs: { id: string }[],
    allLCPs: { id: string }[]
  ): CrossReferenceValidation {
    const issues: CrossReferenceIssue[] = [];
    const agentIds = new Set(allAgents.map(a => a.id));
    const skillIds = new Set(allSkills.map(s => s.id));
    const mcpIds = new Set(allMCPs.map(m => m.id));
    const lcpIds = new Set(allLCPs.map(l => l.id));

    const allRegisteredSkillIds = new Set(allSkills.map(s => s.id));

    for (const pb of allPlaybooks) {
      for (const agentId of (pb as any).required_agents ?? []) {
        if (!agentIds.has(agentId)) {
          issues.push({
            severity: "error",
            registry: "playbooks",
            field: "required_agents",
            reference: agentId,
            message: `Playbook "${pb.id}" references unknown agent "${agentId}"`
          });
        }
      }
      for (const skillId of (pb as any).required_skills ?? []) {
        if (!allRegisteredSkillIds.has(skillId)) {
          issues.push({
            severity: "error",
            registry: "playbooks",
            field: "required_skills",
            reference: skillId,
            message: `Playbook "${pb.id}" references unknown skill "${skillId}"`
          });
        }
      }
      for (const mcpId of (pb as any).allowed_mcps ?? []) {
        if (!mcpIds.has(mcpId)) {
          issues.push({
            severity: "warning",
            registry: "playbooks",
            field: "allowed_mcps",
            reference: mcpId,
            message: `Playbook "${pb.id}" references unknown MCP "${mcpId}"`
          });
        }
      }
      for (const lcpId of (pb as any).required_lcps ?? []) {
        if (!lcpIds.has(lcpId)) {
          issues.push({
            severity: "warning",
            registry: "playbooks",
            field: "required_lcps",
            reference: lcpId,
            message: `Playbook "${pb.id}" references unknown LCP "${lcpId}"`
          });
        }
      }
    }

    return { valid: issues.filter(i => i.severity === "error").length === 0, issues };
  }

  validateMergeResult(result: MergeResult): ValidationResult {
    const errors: string[] = [];
    const warnings: string[] = [];

    if (!result.merged) {
      errors.push("Merge failed — unresolved conflicts remain");
    }

    for (const conflict of result.conflicts) {
      errors.push(`Conflict: ${conflict.registry} — "${conflict.existing_id}" from ${conflict.source}: ${conflict.reason}`);
    }

    warnings.push(...result.warnings);

    const agentIds = new Set<string>();
    for (const agent of result.agents) {
      if (agentIds.has(agent.id)) errors.push(`Duplicate agent after merge: ${agent.id}`);
      agentIds.add(agent.id);
    }

    const skillIds = new Set<string>();
    for (const skill of result.skills) {
      if (skillIds.has(skill.id)) errors.push(`Duplicate skill after merge: ${skill.id}`);
      skillIds.add(skill.id);
    }

    const playbookIds = new Set<string>();
    for (const pb of result.playbooks) {
      if (playbookIds.has(pb.id)) errors.push(`Duplicate playbook after merge: ${pb.id}`);
      playbookIds.add(pb.id);
    }

    return { valid: errors.length === 0, errors, warnings };
  }

  private fileExists(relativePath: string): boolean {
    return existsSync(resolve(this.aeosRoot, relativePath));
  }
}