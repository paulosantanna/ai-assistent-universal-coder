import type { RandomUUIDOptions } from "node:crypto";

// =============================================================================
// AEOS Kernel Types
// =============================================================================

export type RiskLevel = "low" | "medium" | "high" | "critical";

export type JudgeVerdict = "PASS" | "BLOCKED";

export type ExecutionStatus = "pending" | "running" | "completed" | "blocked" | "failed";

export interface ValidationResult {
  valid: boolean;
  errors: string[];
  warnings: string[];
}

// =============================================================================
// Config Schema
// =============================================================================

export interface AeosConfig {
  aeos: {
    name: string;
    version: string;
    mode: string;
  };
  runtime: {
    workspace_root: string;
    default_output_dir: string;
    require_kernel: boolean;
    require_policy_check: boolean;
    require_permission_check: boolean;
    require_evidence: boolean;
    require_judge: boolean;
    require_evidence_integrity?: boolean;
    require_tool_router?: boolean;
    require_mcp_runtime?: boolean;
    require_agent_runtime?: boolean;
    require_observability?: boolean;
    require_parallel_execution?: boolean;
  };
  registries: {
    agents: string;
    skills: string;
    playbooks: string;
    mcps: string;
    lcps: string;
    blueprints?: string;
    enterprise_skills?: string;
    enterprise_playbooks?: string;
    workbench_profiles?: string;
    overlay_index?: string;
  };
  execution: {
    default_mode: string;
    allow_direct_write: boolean;
    require_branch_for_code_changes: boolean;
    require_rollback_plan: boolean;
    require_diff_summary: boolean;
    require_test_evidence: boolean;
    require_evidence_integrity?: boolean;
    require_judge_report?: boolean;
    max_parallel_steps?: number;
    conflict_detection_enabled?: boolean;
    protected_branches?: string[];
  };
  security: {
    block_plaintext_secrets: boolean;
    block_secret_logging: boolean;
    block_destructive_actions_without_approval: boolean;
    block_network_exfiltration: boolean;
    block_direct_tool_access?: boolean;
    block_direct_mcp_access?: boolean;
    block_wildcard_approval?: boolean;
    block_auto_merge?: boolean;
    block_auto_deploy?: boolean;
    block_unverified_package_extract?: boolean;
    block_direct_active_pack_import?: boolean;
    redaction_required?: boolean;
    threat_model_required?: boolean;
    package_quarantine_required?: boolean;
    allowed_secret_sources: string[];
  };
  judge: {
    min_score: number;
    deterministic_first?: boolean;
    block_on_missing_evidence: boolean;
    block_on_failing_tests: boolean;
    block_on_security_risk: boolean;
    block_on_missing_rollback: boolean;
    block_on_hash_mismatch?: boolean;
    block_on_tool_router_bypass?: boolean;
    block_on_policy_bypass?: boolean;
    block_on_permission_bypass?: boolean;
    block_on_wildcard_approval?: boolean;
    block_on_auto_merge?: boolean;
    block_on_auto_deploy?: boolean;
    block_on_unsupported_claim?: boolean;
    enterprise_gates_enabled?: boolean;
  };
  observability: {
    logs: boolean;
    traces: boolean;
    metrics: boolean;
    token_usage: boolean;
    tool_call_audit: boolean;
    cost_tracking?: boolean;
    audit_export?: boolean;
    timeline?: boolean;
  };
}

// =============================================================================
// Capabilities Schema
// =============================================================================

export interface CapabilityDef {
  id: string;
  name: string;
  description: string;
  risk_level: RiskLevel;
  requires_mcp: string;
  requires_approval?: boolean;
  requires_rollback?: boolean;
  log_redaction_required?: boolean;
}

export interface CapabilitiesConfig {
  capabilities: CapabilityDef[];
}

// =============================================================================
// Permissions Schema
// =============================================================================

export interface AgentMCPPermission {
  agent: string;
  mcps: string[];
  allow: boolean;
}

export interface AgentSkillPermission {
  agent: string;
  skills: string[];
  allow: boolean;
}

export interface EscalationRule {
  when: string;
  then: string;
}

export interface PermissionsConfig {
  permissions: {
    default_policy: "deny-all" | "allow-all";
    agent_to_mcp: AgentMCPPermission[];
    agent_to_skill: AgentSkillPermission[];
    escalation_rules: EscalationRule[];
  };
}

// =============================================================================
// Policies Schema
// =============================================================================

export interface PoliciesConfig {
  policies: {
    security: {
      secrets: Record<string, boolean>;
      destructive_actions: {
        require_human_approval: boolean;
        require_rollback_plan: boolean;
        require_impact_analysis: boolean;
        require_test_evidence: boolean;
        actions: string[];
      };
      network: {
        block_exfiltration: boolean;
        allow_only_approved_endpoints: boolean;
        require_approval_for_external_calls: boolean;
      };
    };
    audit: Record<string, unknown>;
    evidence: Record<string, unknown>;
    approvals: {
      human_approval_required_for: Array<{ capability?: string; risk_level?: string; when?: string }>;
    };
    isolation: Record<string, boolean>;
  };
}

// =============================================================================
// Registry Schema
// =============================================================================

export interface PlaybookRegistryEntry {
  id: string;
  name: string;
  path: string;
  risk_level: RiskLevel;
  required_agents: string[];
  required_skills: string[];
  required_lcps: string[];
  allowed_mcps: string[];
}

export interface PlaybooksRegistry {
  playbooks: PlaybookRegistryEntry[];
}

export interface SkillRegistryEntry {
  id: string;
  path: string;
  version: string;
  owner_agent: string;
  risk_level: RiskLevel;
  capabilities: string[];
  requires_human_approval_for?: string[];
}

export interface SkillsRegistry {
  skills: SkillRegistryEntry[];
}

export interface MCPRegistryEntry {
  id: string;
  type: string;
  config: string;
  risk_level: RiskLevel;
  capabilities: string[];
  write_allowed?: boolean;
  approval_required?: boolean;
  sandbox_required?: boolean;
  destructive_commands_blocked?: boolean;
  log_redaction_required?: boolean;
}

export interface MCPsRegistry {
  mcps: MCPRegistryEntry[];
}

export interface LCPRegistryEntry {
  id: string;
  path: string;
  priority: number;
  scope: string;
  applies_to: string[];
}

export interface LCPsRegistry {
  lcps: LCPRegistryEntry[];
}

export interface AgentRegistryEntry {
  id: string;
  name: string;
  role: string;
  description: string;
  max_subagents: number;
  allowed_domains: string[];
  allowed_skills: string[];
  allowed_mcps: string[];
  path: string;
  independence?: string;
  cannot_be_same_as_implementer?: boolean;
}

export interface AgentsRegistry {
  agents: AgentRegistryEntry[];
}

// =============================================================================
// Overlay Registry Types
// =============================================================================

export interface OverlayIndexFragment {
  path: string;
}

export interface OverlayRegistryIndex {
  generated_at: string;
  note?: string;
  registry_fragments: OverlayIndexFragment[];
}

export interface BlueprintRegistryEntry {
  id: string;
  type: string;
  path: string;
}

export interface BlueprintsRegistry {
  blueprints: BlueprintRegistryEntry[];
}

export interface WorkbenchProfileRegistryEntry {
  id: string;
  path: string;
}

export interface WorkbenchProfilesRegistry {
  profiles: WorkbenchProfileRegistryEntry[];
}

export interface EnterpriseSkillRegistryEntry extends SkillRegistryEntry {
  production_ready?: boolean;
}

export interface EnterprisePlaybookRegistryEntry extends PlaybookRegistryEntry {
  version?: string;
  production_ready?: boolean;
}

export interface EnterpriseSkillsRegistry {
  skills: EnterpriseSkillRegistryEntry[];
}

export interface EnterprisePlaybooksRegistry {
  playbooks: EnterprisePlaybookRegistryEntry[];
}

// =============================================================================
// Additions Registry Types
// =============================================================================

export interface SkillsAdditionsConfig {
  skills: SkillRegistryEntry[];
}

export interface PlaybooksAdditionsConfig {
  playbooks: PlaybookRegistryEntry[];
}

export interface AgentsAdditionsConfig {
  agents: AgentRegistryEntry[];
  subagents?: SubAgentRegistryEntry[];
}

export interface SubAgentRegistryEntry {
  id: string;
  parent_roles: string[];
  path: string;
}

// =============================================================================
// Merge Result Types
// =============================================================================

export interface MergeConflict {
  registry: string;
  existing_id: string;
  source: string;
  reason: string;
}

export interface MergeResult {
  merged: boolean;
  conflicts: MergeConflict[];
  warnings: string[];
  agents: AgentRegistryEntry[];
  subagents: SubAgentRegistryEntry[];
  skills: SkillRegistryEntry[];
  playbooks: PlaybookRegistryEntry[];
}

// =============================================================================
// Cross-Reference Validation Types
// =============================================================================

export interface CrossReferenceIssue {
  severity: "error" | "warning";
  registry: string;
  field: string;
  reference: string;
  message: string;
}

export interface CrossReferenceValidation {
  valid: boolean;
  issues: CrossReferenceIssue[];
}

// =============================================================================
// LCP Content
// =============================================================================

export interface LCPContent {
  id: string;
  name: string;
  version: string;
  context_type: string;
  priority: number;
  applies_when: Record<string, string[] | boolean>;
  load_order: string[];
  rules: string[];
  required_evidence?: string[];
  forbidden?: string[];
}

// =============================================================================
// Execution Context
// =============================================================================

export interface ExecutionContext {
  executionId: string;
  playbookId: string;
  targetPath: string;
  aeosRoot: string;
  status: ExecutionStatus;
  startedAt: string;
  completedAt?: string;
  config: AeosConfig;
  resolvedPlaybook: PlaybookRegistryEntry | null;
  resolvedSkills: SkillRegistryEntry[];
  resolvedMCPs: MCPRegistryEntry[];
  resolvedLCPs: LCPRegistryEntry[];
  loadedLCPContents: LCPContent[];
  agent: AgentRegistryEntry | null;
  permissionDecisions: PermissionDecision[];
  toolCalls: ToolCallRecord[];
  evidenceRecords: EvidenceRecord[];
  judgeReport: JudgeReport | null;
  artifacts: string[];
  error?: string;
}

export interface PermissionDecision {
  action: string;
  agentId: string;
  resource: string;
  allowed: boolean;
  reason: string;
  timestamp: string;
}

export interface ToolCallRecord {
  callId: string;
  tool: string;
  action: string;
  params: Record<string, unknown>;
  result: string;
  allowed: boolean;
  timestamp: string;
  durationMs: number;
}

export interface EvidenceRecord {
  id: string;
  type: string;
  claim: string;
  reference: string;
  source: string;
  timestamp: string;
  verified: boolean;
}

// =============================================================================
// Judge
// =============================================================================

export interface JudgeReport {
  executionId: string;
  verdict: JudgeVerdict;
  score: number;
  minScore: number;
  summary: string;
  evidenceReviewed: number;
  risks: string[];
  failures: string[];
  filesAffected: string[];
  testsExecuted: number;
  requiredNextSteps: string[];
  timestamp: string;
}

// =============================================================================
// Tool Router
// =============================================================================

export interface ToolResult {
  success: boolean;
  data?: unknown;
  error?: string;
  truncated?: boolean;
}

export interface FileInfo {
  path: string;
  size: number;
  isDirectory: boolean;
  extension: string;
  lastModified: string;
}

// =============================================================================
// Skill Context
// =============================================================================

export interface SkillInput {
  workspacePath: string;
  scanDepth: number;
  ignoredDirectories: string[];
  outputDir: string;
  evidenceDir: string;
}

export interface SkillOutput {
  artifacts: string[];
  evidence: EvidenceRecord[];
  risks: string[];
  facts: string[];
  assumptions: string[];
  errors: string[];
}
