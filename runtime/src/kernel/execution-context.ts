import { randomUUID } from "node:crypto";
import type {
  AeosConfig,
  ExecutionContext,
  PlaybookRegistryEntry,
  SkillRegistryEntry,
  MCPRegistryEntry,
  LCPRegistryEntry,
  LCPContent,
  AgentRegistryEntry,
  PermissionDecision,
  ToolCallRecord,
  EvidenceRecord,
  JudgeReport,
  ExecutionStatus
} from "./types.js";

export function createExecutionContext(
  playbookId: string,
  targetPath: string,
  aeosRoot: string,
  config: AeosConfig
): ExecutionContext {
  return {
    executionId: randomUUID(),
    playbookId,
    targetPath,
    aeosRoot,
    status: "pending",
    startedAt: new Date().toISOString(),
    config,
    resolvedPlaybook: null,
    resolvedSkills: [],
    resolvedMCPs: [],
    resolvedLCPs: [],
    loadedLCPContents: [],
    agent: null,
    permissionDecisions: [],
    toolCalls: [],
    evidenceRecords: [],
    judgeReport: null,
    artifacts: []
  };
}

export function setContextStatus(ctx: ExecutionContext, status: ExecutionStatus, error?: string): void {
  ctx.status = status;
  if (status === "completed" || status === "failed" || status === "blocked") {
    ctx.completedAt = new Date().toISOString();
  }
  if (error) {
    ctx.error = error;
  }
}

export function addPermissionDecision(ctx: ExecutionContext, decision: PermissionDecision): void {
  ctx.permissionDecisions.push(decision);
}

export function addToolCall(ctx: ExecutionContext, call: ToolCallRecord): void {
  ctx.toolCalls.push(call);
}

export function addEvidence(ctx: ExecutionContext, evidence: EvidenceRecord): void {
  ctx.evidenceRecords.push(evidence);
}

export function addArtifact(ctx: ExecutionContext, path: string): void {
  ctx.artifacts.push(path);
}
