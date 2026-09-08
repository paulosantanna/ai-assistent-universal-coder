export const CODENAVI_STANDARD = "CodENavi Full Workspace v3" as const;
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

export function hasCurrentGovernance(value: unknown): boolean {
  if (!value || typeof value !== "object") return false;
  const governance = (value as { governance?: Partial<CodENaviRuntimeGovernance> }).governance;
  return governance?.standard === CODENAVI_STANDARD
    && Array.isArray(governance.lifecycle)
    && governance.lifecycle.join("|") === CODENAVI_LIFECYCLE.join("|")
    && governance.evidence_required === true
    && governance.verification_required === true
    && governance.freshness_required === true
    && governance.fail_closed === true;
}
