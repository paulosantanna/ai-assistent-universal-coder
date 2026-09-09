export const CODENAVI_STANDARD = "CodENavi Artifact Contract v1" as const;
export const CODENAVI_PARENT_STANDARD = "CodENavi Full Workspace v2" as const;
export const CODENAVI_AGENT_ID = "codenavi-agent" as const;
export const CODENAVI_LIFECYCLE = [
  "BRIEFING",
  "RECON",
  "PLAN",
  "EXECUTE",
  "VERIFY",
  "DEBRIEF"
] as const;

export interface CodENaviRuntimeGovernance {
  standard: typeof CODENAVI_STANDARD;
  parent_standard: typeof CODENAVI_PARENT_STANDARD;
  canonical_agent: typeof CODENAVI_AGENT_ID;
  lifecycle: typeof CODENAVI_LIFECYCLE;
  evidence_required: true;
  verification_required: true;
  freshness_required: true;
  notebook_required_for_material_missions: true;
  fail_closed: true;
  secret_policy: "runtime-only-masked-non-persistent";
  authority_policy: "deny-by-default-no-self-escalation";
  change_policy: "smallest-sufficient-surgical-change";
  production_mutation_policy: "approval-judge-rollback-required";
}

export const CODENAVI_RUNTIME_GOVERNANCE: CodENaviRuntimeGovernance = Object.freeze({
  standard: CODENAVI_STANDARD,
  parent_standard: CODENAVI_PARENT_STANDARD,
  canonical_agent: CODENAVI_AGENT_ID,
  lifecycle: CODENAVI_LIFECYCLE,
  evidence_required: true,
  verification_required: true,
  freshness_required: true,
  notebook_required_for_material_missions: true,
  fail_closed: true,
  secret_policy: "runtime-only-masked-non-persistent",
  authority_policy: "deny-by-default-no-self-escalation",
  change_policy: "smallest-sufficient-surgical-change",
  production_mutation_policy: "approval-judge-rollback-required"
});

/**
 * Registry files contain domain metadata; governance is attached at the runtime
 * boundary so legacy and overlay entries cannot bypass the current constitution.
 * Existing entry fields win only for domain semantics, never for governance.
 */
export function governEntry<T extends object>(entry: T): T & { governance: CodENaviRuntimeGovernance } {
  return {
    ...entry,
    governance: CODENAVI_RUNTIME_GOVERNANCE
  };
}

export function governEntries<T extends object>(entries: T[]): Array<T & { governance: CodENaviRuntimeGovernance }> {
  return entries.map(governEntry);
}

/**
 * Skill ownership is runtime-authoritative. Legacy owner_agent values describe
 * former personas only; they cannot create or select a second agent identity.
 */
export function governSkillEntry<T extends object>(entry: T): T & {
  owner_agent: typeof CODENAVI_AGENT_ID;
  governance: CodENaviRuntimeGovernance;
} {
  return {
    ...entry,
    owner_agent: CODENAVI_AGENT_ID,
    governance: CODENAVI_RUNTIME_GOVERNANCE
  };
}

export function governSkillEntries<T extends object>(entries: T[]): Array<ReturnType<typeof governSkillEntry<T>>> {
  return entries.map(governSkillEntry);
}

/**
 * Playbooks may retain historical role labels in source registries for migration
 * traceability, but execution is always resolved to the single CodENavi agent.
 */
export function governPlaybookEntry<T extends object>(entry: T): T & {
  required_agents: [typeof CODENAVI_AGENT_ID];
  governance: CodENaviRuntimeGovernance;
} {
  return {
    ...entry,
    required_agents: [CODENAVI_AGENT_ID],
    governance: CODENAVI_RUNTIME_GOVERNANCE
  };
}

export function governPlaybookEntries<T extends object>(entries: T[]): Array<ReturnType<typeof governPlaybookEntry<T>>> {
  return entries.map(governPlaybookEntry);
}

export function hasCurrentGovernance(value: unknown): boolean {
  if (!value || typeof value !== "object") return false;
  const governance = (value as { governance?: Partial<CodENaviRuntimeGovernance> }).governance;
  return governance?.standard === CODENAVI_STANDARD
    && governance.parent_standard === CODENAVI_PARENT_STANDARD
    && governance.canonical_agent === CODENAVI_AGENT_ID
    && Array.isArray(governance.lifecycle)
    && governance.lifecycle.join("|") === CODENAVI_LIFECYCLE.join("|")
    && governance.evidence_required === true
    && governance.verification_required === true
    && governance.freshness_required === true
    && governance.fail_closed === true;
}
