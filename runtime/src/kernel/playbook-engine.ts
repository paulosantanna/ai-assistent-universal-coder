import type {
  ExecutionContext,
  PlaybookRegistryEntry,
  SkillRegistryEntry,
  MCPRegistryEntry,
  LCPRegistryEntry,
  LCPContent,
  AgentRegistryEntry
} from "./types.js";
import { setContextStatus, addEvidence } from "./execution-context.js";
import { ConfigLoader } from "./config-loader.js";
import { PermissionEngine, type PermissionRequest } from "./permission-engine.js";
import { PolicyEngine, type ActionRequest } from "./policy-engine.js";
import { EvidenceStore } from "./evidence-store.js";
import { ToolRouter } from "./tool-router.js";
import { SkillExecutor, type SkillContext } from "./skill-executor.js";
import { DeterministicJudge } from "./deterministic-judge.js";
import { ReportWriter } from "./report-writer.js";
import { randomUUID } from "node:crypto";
import { join, resolve } from "node:path";

export class PlaybookEngine {
  private configLoader: ConfigLoader;
  private permissionEngine: PermissionEngine;
  private policyEngine: PolicyEngine;
  private skillExecutor: SkillExecutor;
  private judge: DeterministicJudge;
  private reportWriter: ReportWriter;

  constructor(
    configLoader: ConfigLoader,
    permissionEngine: PermissionEngine,
    policyEngine: PolicyEngine,
    skillExecutor: SkillExecutor,
    judge: DeterministicJudge,
    reportWriter: ReportWriter
  ) {
    this.configLoader = configLoader;
    this.permissionEngine = permissionEngine;
    this.policyEngine = policyEngine;
    this.skillExecutor = skillExecutor;
    this.judge = judge;
    this.reportWriter = reportWriter;
  }

  async execute(
    playbook: PlaybookRegistryEntry,
    skills: SkillRegistryEntry[],
    mcps: MCPRegistryEntry[],
    lcpContents: LCPContent[],
    agent: AgentRegistryEntry,
    targetPath: string,
    aeosRoot: string,
    config: any
  ): Promise<ExecutionContext> {
    const { createExecutionContext } = await import("./execution-context.js");

    const ctx = createExecutionContext(playbook.id, targetPath, aeosRoot, config);
    setContextStatus(ctx, "running");

    try {
      ctx.resolvedPlaybook = playbook;
      ctx.resolvedSkills = skills;
      ctx.resolvedMCPs = mcps;
      ctx.resolvedLCPs = lcpContents.map((l) => ({
        id: l.id,
        path: "",
        priority: l.priority,
        scope: l.context_type,
        applies_to: []
      }));
      ctx.agent = agent;

      const evidenceBase = join(targetPath, ".aeos", "evidence", ctx.executionId);
      const evidenceStore = new EvidenceStore(evidenceBase);
      const toolRouter = new ToolRouter(evidenceStore);

      toolRouter.registerMCPs(mcps);

      // Step 1: Permission check for agent
      this.checkAndRecord(
        ctx,
        evidenceStore,
        this.permissionEngine.checkPermission({
          agentId: agent.id,
          action: "playbook-execution",
          resourceType: "mcp",
          resourceId: "filesystem-readonly",
          riskLevel: playbook.risk_level,
          details: `Executing playbook: ${playbook.id}`
        })
      );

      // Step 2: Policy check
      const policyResult = this.policyEngine.checkAction({
        actionType: "filesystem_write",
        actionName: "read",
        details: { direct: false }
      });

      const permDecision = {
        action: "filesystem-write-check",
        agentId: agent.id,
        resource: "policy:filesystem",
        allowed: policyResult.allowed,
        reason: policyResult.reason,
        timestamp: new Date().toISOString()
      };
      ctx.permissionDecisions.push(permDecision);
      evidenceStore.writePermissionDecision(permDecision);

      // Step 3: Execute skills sequentially
      for (const skillEntry of skills) {
        const skillCheck = this.permissionEngine.checkPermission({
          agentId: agent.id,
          action: "skill-execution",
          resourceType: "skill",
          resourceId: skillEntry.id,
          riskLevel: skillEntry.risk_level
        });

        ctx.permissionDecisions.push(skillCheck);
        evidenceStore.writePermissionDecision(skillCheck);

        if (!skillCheck.allowed) {
          addEvidence(ctx, {
            id: randomUUID(),
            type: "security",
            claim: `Skill '${skillEntry.id}' skipped: ${skillCheck.reason}`,
            reference: "permission-decision",
            source: "permission-engine",
            timestamp: new Date().toISOString(),
            verified: true
          });
          continue;
        }

        const skillContext: SkillContext = {
          registryEntry: skillEntry,
          input: {
            workspacePath: targetPath,
            scanDepth: 3,
            ignoredDirectories: [".git", "node_modules", "dist", "build", "target", ".venv"],
            outputDir: evidenceBase,
            evidenceDir: evidenceBase
          },
          toolRouter,
          evidenceStore,
          executionContext: ctx
        };

        const output = await this.skillExecutor.execute(skillEntry.id, skillContext);

        // Record evidence from skill output
        for (const ev of output.evidence) {
          addEvidence(ctx, ev);
          evidenceStore.writeEvidence(ev);
        }

        // Add risks to context
        for (const risk of output.risks) {
          addEvidence(ctx, {
            id: randomUUID(),
            type: "security",
            claim: risk,
            reference: "skill-output",
            source: skillEntry.id,
            timestamp: new Date().toISOString(),
            verified: true
          });
        }
      }

      // Step 4: Run Judge
      const reportDir = join(targetPath, ".aeos", "reports");
      const judgeReport = this.judge.evaluate(ctx, evidenceStore);
      ctx.judgeReport = judgeReport;

      // Determine final status before writing reports
      if (judgeReport.verdict === "BLOCKED") {
        ctx.status = "blocked";
        ctx.judgeReport = judgeReport;
      } else {
        setContextStatus(ctx, "completed");
      }

      // Step 5: Write reports (status is already set)
      const judgeArtifact = evidenceStore.writeGeneratedArtifact(
        "../../reports/judge-report.md",
        this.reportWriter.writeJudgeReport(judgeReport)
      );
      ctx.artifacts.push(judgeArtifact);

      const executionArtifact = evidenceStore.writeGeneratedArtifact(
        "../../reports/execution-summary.md",
        this.reportWriter.writeExecutionSummary(ctx)
      );
      ctx.artifacts.push(executionArtifact);

      // Write permission decisions summary
      evidenceStore.writeGeneratedArtifact(
        "../../reports/permission-decisions.md",
        this.reportWriter.writePermissionDecisions(ctx.permissionDecisions)
      );

      for (const artifact of ctx.artifacts) {
        const relPath = artifact;
        ctx.evidenceRecords.push({
          id: randomUUID(),
          type: "source",
          claim: `Generated artifact: ${relPath}`,
          reference: relPath,
          source: "playbook-engine",
          timestamp: new Date().toISOString(),
          verified: true
        });
      }
    } catch (err) {
      setContextStatus(ctx, "failed", err instanceof Error ? err.message : String(err));
    }

    return ctx;
  }

  private checkAndRecord(ctx: ExecutionContext, store: EvidenceStore, decision: any): void {
    ctx.permissionDecisions.push(decision);
    store.writePermissionDecision(decision);
  }
}
