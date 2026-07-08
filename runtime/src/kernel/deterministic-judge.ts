import type {
  ExecutionContext,
  EvidenceRecord,
  JudgeReport,
  JudgeVerdict,
  PermissionDecision
} from "./types.js";
import { EvidenceStore } from "./evidence-store.js";

export class DeterministicJudge {
  evaluate(ctx: ExecutionContext, evidenceStore: EvidenceStore): JudgeReport {
    const timestamp = new Date().toISOString();
    const minScore = ctx.config.judge.min_score ?? 9.0;

    const failures: string[] = [];
    const risks: string[] = [];
    const requiredNextSteps: string[] = [];
    let score = 10.0;
    let verdict: JudgeVerdict = "PASS";

    // Check 1: Missing evidence (count artifacts as evidence too)
    const totalEvidence = ctx.evidenceRecords.length + ctx.artifacts.length;
    if (ctx.config.judge.block_on_missing_evidence) {
      if (totalEvidence === 0) {
        failures.push("No evidence or artifacts found");
        score -= 3.0;
      } else if (totalEvidence < 3) {
        risks.push(`Minimal evidence: ${totalEvidence} record(s) total`);
      }
    }

    // Check 2: No artifacts generated
    if (ctx.artifacts.length === 0) {
      failures.push("No artifacts were generated");
      score -= 2.0;
    }

    // Check 3: Permission denied actions (noted as risks, not failures in v0.1)
    const deniedPermissions = ctx.permissionDecisions.filter((d) => !d.allowed);
    if (deniedPermissions.length > 0) {
      risks.push(`${deniedPermissions.length} permission(s) denied: ${deniedPermissions.map((d) => d.resource).join(", ")}`);
    }

    // Check 4: Security risks
    if (ctx.config.judge.block_on_security_risk) {
      const securityRisks = ctx.evidenceRecords.filter(
        (e) => e.type === "security" && e.claim.toLowerCase().includes("secret")
      );
      if (securityRisks.length > 0) {
        risks.push(`${securityRisks.length} secret indicator(s) found`);
        requiredNextSteps.push("Run security-secrets-audit playbook for detailed scan");
        score -= 1.0;
      }
    }

    // Check 5: Missing rollback plan (noted as risk for read-only playbooks)
    if (ctx.config.judge.block_on_missing_rollback && ctx.playbookId !== "project-analysis") {
      const hasRollback = ctx.evidenceRecords.some(
        (e) => e.claim.toLowerCase().includes("rollback")
      );
      if (!hasRollback) {
        failures.push("No rollback plan evidence found");
        score -= 1.0;
      }
    }

    // Check 6: Errors in execution
    if (ctx.error) {
      failures.push(`Execution error: ${ctx.error}`);
      score -= 3.0;
      verdict = "BLOCKED";
    }

    // Check 7: Tool call audit
    if (ctx.config.observability?.tool_call_audit) {
      // Check for unpermitted tool calls
      const toolCalls = evidenceStore.readJsonl("tool-calls.jsonl");
      if (toolCalls.length === 0 && ctx.status !== "blocked" && ctx.status !== "failed") {
        risks.push("No tool calls were recorded");
      }
    }

    // Clamp score
    score = Math.max(0, Math.min(10, score));

    // Determine verdict
    if (score < minScore) {
      verdict = "BLOCKED";
      failures.push(`Score ${score.toFixed(1)} is below minimum ${minScore}`);
    }

    if (failures.length > 0) {
      requiredNextSteps.unshift("Review and address all failures listed above");
    }

    return {
      executionId: ctx.executionId,
      verdict,
      score,
      minScore,
      summary: verdict === "PASS"
        ? `All checks passed with score ${score.toFixed(1)}/${minScore}`
        : `Blocked: score ${score.toFixed(1)}/${minScore}. ${failures.length} failure(s).`,
      evidenceReviewed: ctx.evidenceRecords.length,
      risks,
      failures,
      filesAffected: ctx.artifacts.map((a) => a.replace(/\\/g, "/")),
      testsExecuted: ctx.toolCalls.filter((t) => t.tool === "test-runner").length,
      requiredNextSteps,
      timestamp
    };
  }
}
