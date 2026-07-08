import type { PoliciesConfig } from "./types.js";

export interface PolicyCheckResult {
  allowed: boolean;
  policy: string;
  reason: string;
}

export interface ActionRequest {
  actionType: string;
  actionName: string;
  details?: Record<string, unknown>;
}

export class PolicyEngine {
  private config: PoliciesConfig;

  constructor(config: PoliciesConfig) {
    this.config = config;
  }

  checkAction(request: ActionRequest): PolicyCheckResult {
    if (request.actionType === "destructive") {
      return this.checkDestructiveAction(request);
    }

    if (request.actionType === "secret") {
      return this.checkSecretAction(request);
    }

    if (request.actionType === "network") {
      return this.checkNetworkAction(request);
    }

    if (request.actionType === "filesystem_write") {
      return this.checkFilesystemWrite(request);
    }

    return { allowed: true, policy: "default", reason: "No specific policy for this action type" };
  }

  private checkDestructiveAction(request: ActionRequest): PolicyCheckResult {
    const pol = this.config.policies.security.destructive_actions;
    if (!pol) {
      return { allowed: true, policy: "destructive", reason: "No destructive action policy defined" };
    }

    if (pol.actions.includes(request.actionName)) {
      return {
        allowed: false,
        policy: "destructive",
        reason: `Destructive action '${request.actionName}' requires human approval and rollback plan`
      };
    }

    if (pol.require_human_approval) {
      return {
        allowed: false,
        policy: "destructive",
        reason: `Action '${request.actionName}' requires human approval per policy`
      };
    }

    return { allowed: true, policy: "destructive", reason: "Action is not in blocked destructive list" };
  }

  private checkSecretAction(request: ActionRequest): PolicyCheckResult {
    const secrets = this.config.policies.security.secrets;
    if (!secrets) {
      return { allowed: true, policy: "secret", reason: "No secret policy defined" };
    }

    if (request.actionName === "read_secret_value") {
      return {
        allowed: false,
        policy: "secret",
        reason: "Reading secret values is blocked in v0.1"
      };
    }

    if (request.actionName === "log_secret" || request.actionName === "write_secret_to_file") {
      return {
        allowed: false,
        policy: "secret",
        reason: "Logging or persisting secrets is prohibited"
      };
    }

    return { allowed: true, policy: "secret", reason: "Secret action allowed" };
  }

  private checkNetworkAction(request: ActionRequest): PolicyCheckResult {
    const net = this.config.policies.security.network;
    if (!net) {
      return { allowed: true, policy: "network", reason: "No network policy defined" };
    }

    if (net.block_exfiltration && request.actionName === "network_request") {
      return {
        allowed: false,
        policy: "network",
        reason: "Network exfiltration is blocked by policy"
      };
    }

    return { allowed: true, policy: "network", reason: "Network action allowed" };
  }

  private checkFilesystemWrite(request: ActionRequest): PolicyCheckResult {
    const isolation = this.config.policies.isolation;
    if (!isolation) {
      return { allowed: true, policy: "filesystem_write", reason: "No isolation policy defined" };
    }

    if (isolation.no_direct_filesystem_access && request.details?.direct === true) {
      return {
        allowed: false,
        policy: "filesystem_write",
        reason: "Direct filesystem access is blocked by isolation policy"
      };
    }

    return { allowed: true, policy: "filesystem_write", reason: "Filesystem write allowed" };
  }
}
