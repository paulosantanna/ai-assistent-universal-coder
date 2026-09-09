import type {
  PermissionsConfig,
  AgentRegistryEntry,
  MCPRegistryEntry,
  SkillRegistryEntry,
  PermissionDecision,
  RiskLevel
} from "./types.js";
import { CODENAVI_AGENT_ID } from "./codenavi-governance.js";

export interface PermissionRequest {
  agentId: string;
  action: string;
  resourceType: "mcp" | "skill" | "capability" | "filesystem" | "git" | "shell" | "secret";
  resourceId: string;
  riskLevel: RiskLevel;
  details?: string;
}

function resourceAllowed(values: string[], resourceId: string): boolean {
  return values.includes(resourceId) || values.includes("all") || values.includes("*");
}

export class PermissionEngine {
  private config: PermissionsConfig;

  constructor(config: PermissionsConfig) {
    this.config = config;
  }

  checkPermission(request: PermissionRequest): PermissionDecision {
    const timestamp = new Date().toISOString();

    const decision: PermissionDecision = {
      action: request.action,
      agentId: request.agentId,
      resource: `${request.resourceType}:${request.resourceId}`,
      allowed: false,
      reason: "Default deny-all",
      timestamp
    };

    if (request.agentId !== CODENAVI_AGENT_ID) {
      decision.reason = `Only '${CODENAVI_AGENT_ID}' may request AEOS permissions`;
      return decision;
    }

    if (this.config.permissions.default_policy !== "deny-all") {
      decision.reason = "Invalid permissions configuration: default policy must be deny-all";
      return decision;
    }

    if (request.resourceType === "mcp") {
      return this.checkMCPPermission(request, decision);
    }

    if (request.resourceType === "skill") {
      return this.checkSkillPermission(request, decision);
    }

    if (request.resourceType === "capability") {
      return this.checkCapabilityPermission(request, decision);
    }

    decision.reason = `Resource type '${request.resourceType}' not covered by permission rules`;
    return decision;
  }

  private checkMCPPermission(
    request: PermissionRequest,
    decision: PermissionDecision
  ): PermissionDecision {
    const agentMcpRules = this.config.permissions.agent_to_mcp.filter(
      (rule) => rule.agent === CODENAVI_AGENT_ID
    );

    for (const rule of agentMcpRules) {
      if (resourceAllowed(rule.mcps, request.resourceId) && rule.allow) {
        decision.allowed = true;
        decision.reason = `Canonical agent allowed resolved MCP '${request.resourceId}' via permission rule`;
        return decision;
      }
    }

    decision.reason = `Canonical agent not authorized for MCP '${request.resourceId}' (deny-all)`;
    return decision;
  }

  private checkSkillPermission(
    request: PermissionRequest,
    decision: PermissionDecision
  ): PermissionDecision {
    const agentSkillRules = this.config.permissions.agent_to_skill.filter(
      (rule) => rule.agent === CODENAVI_AGENT_ID
    );

    for (const rule of agentSkillRules) {
      if (resourceAllowed(rule.skills, request.resourceId) && rule.allow) {
        decision.allowed = true;
        decision.reason = `Canonical agent allowed resolved skill '${request.resourceId}' via permission rule`;
        return decision;
      }
    }

    decision.reason = `Canonical agent not authorized for skill '${request.resourceId}' (deny-all)`;
    return decision;
  }

  private checkCapabilityPermission(
    request: PermissionRequest,
    decision: PermissionDecision
  ): PermissionDecision {
    if (request.riskLevel === "critical") {
      decision.reason = `Capability '${request.resourceId}' is critical; requires human approval`;
      return decision;
    }

    if (request.riskLevel === "high" || request.riskLevel === "medium") {
      decision.reason = `Capability '${request.resourceId}' risk level '${request.riskLevel}'; requires review`;
      return decision;
    }

    decision.allowed = true;
    decision.reason = `Capability '${request.resourceId}' risk level '${request.riskLevel}' auto-allowed`;
    return decision;
  }

  validateAgentForPlaybook(
    playbookRequiredAgents: string[],
    agentId: string
  ): PermissionDecision {
    const timestamp = new Date().toISOString();
    const canonicalPlaybook = playbookRequiredAgents.length === 1 && playbookRequiredAgents[0] === CODENAVI_AGENT_ID;
    const canonicalAgent = agentId === CODENAVI_AGENT_ID;
    const allowed = canonicalPlaybook && canonicalAgent;
    return {
      action: "playbook-execution",
      agentId,
      resource: "playbook",
      allowed,
      reason: allowed
        ? `Canonical agent '${CODENAVI_AGENT_ID}' is authorized for the canonicalized playbook`
        : `Single-agent governance requires '${CODENAVI_AGENT_ID}' as the only playbook agent`,
      timestamp
    };
  }
}
