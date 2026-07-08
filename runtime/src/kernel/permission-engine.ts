import type {
  PermissionsConfig,
  AgentRegistryEntry,
  MCPRegistryEntry,
  SkillRegistryEntry,
  PermissionDecision,
  RiskLevel
} from "./types.js";

export interface PermissionRequest {
  agentId: string;
  action: string;
  resourceType: "mcp" | "skill" | "capability" | "filesystem" | "git" | "shell" | "secret";
  resourceId: string;
  riskLevel: RiskLevel;
  details?: string;
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

    if (this.config.permissions.default_policy !== "deny-all") {
      decision.allowed = true;
      decision.reason = "Default allow (non-deny-all policy)";
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
      (rule) => rule.agent === request.agentId
    );

    for (const rule of agentMcpRules) {
      if (rule.mcps.includes(request.resourceId) && rule.allow) {
        decision.allowed = true;
        decision.reason = `Agent '${request.agentId}' allowed MCP '${request.resourceId}' via permission rule`;
        return decision;
      }
    }

    decision.reason = `Agent '${request.agentId}' not authorized for MCP '${request.resourceId}' (deny-all)`;
    return decision;
  }

  private checkSkillPermission(
    request: PermissionRequest,
    decision: PermissionDecision
  ): PermissionDecision {
    const agentSkillRules = this.config.permissions.agent_to_skill.filter(
      (rule) => rule.agent === request.agentId
    );

    for (const rule of agentSkillRules) {
      if (rule.skills.includes(request.resourceId) && rule.allow) {
        decision.allowed = true;
        decision.reason = `Agent '${request.agentId}' allowed skill '${request.resourceId}' via permission rule`;
        return decision;
      }
    }

    decision.reason = `Agent '${request.agentId}' not authorized for skill '${request.resourceId}' (deny-all)`;
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
    if (playbookRequiredAgents.includes(agentId)) {
      return {
        action: "playbook-execution",
        agentId,
        resource: `playbook`,
        allowed: true,
        reason: `Agent '${agentId}' is in the playbook's required agents list`,
        timestamp
      };
    }
    return {
      action: "playbook-execution",
      agentId,
      resource: `playbook`,
      allowed: false,
      reason: `Agent '${agentId}' is not in the playbook's required agents list`,
      timestamp
    };
  }
}
