import type {
  AeosConfig,
  CapabilitiesConfig,
  PermissionsConfig,
  PoliciesConfig,
  PlaybooksRegistry,
  SkillsRegistry,
  MCPsRegistry,
  LCPsRegistry,
  AgentsRegistry
} from "./types.js";

export interface ValidationResult {
  valid: boolean;
  errors: string[];
  warnings: string[];
}

export class SchemaValidator {
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
    if (!c.registries?.playbooks) errors.push("Missing registries.playbooks");
    if (!c.registries?.skills) errors.push("Missing registries.skills");
    if (!c.registries?.mcps) errors.push("Missing registries.mcps");
    if (!c.registries?.lcps) errors.push("Missing registries.lcps");
    if (!c.registries?.agents) errors.push("Missing registries.agents");
    if (c.judge?.min_score === undefined) warnings.push("Using default judge min_score: 9.0");
    if (c.execution?.default_mode !== "dry-run-first") warnings.push("Execution mode is not dry-run-first");

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
    if (!c.policies.isolation?.all_access_through_mcp) {
      errors.push("Policy isolation.all_access_through_mcp must be true");
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

    for (const pb of c.playbooks) {
      if (!pb.id) errors.push("Playbook missing id");
      if (!pb.path) errors.push(`Playbook ${pb.id ?? "?"} missing path`);
      if (!pb.required_agents?.length) warnings.push(`Playbook ${pb.id} has no required agents`);
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

    for (const sk of c.skills) {
      if (!sk.id) errors.push("Skill missing id");
      if (!sk.path) errors.push(`Skill ${sk.id ?? "?"} missing path`);
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

    for (const mcp of c.mcps) {
      if (!mcp.id) errors.push("MCP missing id");
      if (mcp.risk_level === "critical" && !mcp.approval_required) {
        errors.push(`Critical MCP ${mcp.id} must have approval_required`);
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

    for (const agent of c.agents) {
      if (!agent.id) errors.push("Agent missing id");
      if (agent.role === "judge" && !agent.independence) {
        warnings.push(`Judge agent ${agent.id} should have independence: strict`);
      }
    }

    return { valid: errors.length === 0, errors, warnings };
  }
}
