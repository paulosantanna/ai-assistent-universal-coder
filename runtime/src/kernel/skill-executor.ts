import type {
  SkillRegistryEntry,
  SkillInput,
  SkillOutput,
  ExecutionContext,
  CriticalThinkingPlan
} from "./types.js";
import { ToolRouter } from "./tool-router.js";
import { EvidenceStore } from "./evidence-store.js";
import { RepoScannerSkill } from "./skills/repo-scanner.js";
import { basename, extname, join } from "node:path";

export interface SkillContext {
  registryEntry: SkillRegistryEntry;
  input: SkillInput;
  toolRouter: ToolRouter;
  evidenceStore: EvidenceStore;
  executionContext: ExecutionContext;
  criticalThinkingPlan: CriticalThinkingPlan;
}

export class SkillExecutor {
  async execute(skillId: string, context: SkillContext): Promise<SkillOutput> {
    if (
      !context.criticalThinkingPlan ||
      context.criticalThinkingPlan.status !== "PASS" ||
      context.criticalThinkingPlan.skillId !== skillId ||
      context.criticalThinkingPlan.selectedLenses.length === 0
    ) {
      throw new Error(`Critical-thinking governance is missing or invalid for skill '${skillId}'.`);
    }

    const defaultOutput: SkillOutput = {
      artifacts: [],
      evidence: [],
      risks: [],
      facts: [],
      assumptions: [],
      errors: []
    };

    switch (skillId) {
      case "repo-scanner": {
        const skill = new RepoScannerSkill();
        const output = await skill.execute(context.input, context.toolRouter, context.evidenceStore);
        context.executionContext.artifacts.push(...output.artifacts);
        return output;
      }

      case "aura-voice": {
        const rawInput = context.input as unknown as Record<string, unknown>;
        const sourcePath = String(rawInput.sourcePath ?? rawInput.source_path ?? rawInput.mediaPath ?? rawInput.transcriptPath ?? "").trim();
        const health = await context.toolRouter.callTool("aura-voice", "aura.health", { __aeosSkillId: "aura-voice" });
        if (!health.success) {
          defaultOutput.errors.push(health.error || "Aura Voice health check failed");
          return defaultOutput;
        }
        defaultOutput.facts.push("Aura Voice tool is available and governed by the active skill context.");
        if (!sourcePath) {
          defaultOutput.assumptions.push("No sourcePath was supplied; health verification completed without ingesting media.");
          return defaultOutput;
        }

        const ext = extname(sourcePath).toLowerCase();
        const textExts = new Set([".txt", ".tft", ".srt", ".vtt", ".md", ".json", ".csv", ".tsv"]);
        const mediaExts = new Set([".mp4", ".mov", ".mkv", ".webm", ".avi", ".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg", ".opus"]);
        let transcriptText = "";

        if (textExts.has(ext)) {
          const read = await context.toolRouter.callTool("aura-voice", "aura.transcript.read", { path: sourcePath, __aeosSkillId: "aura-voice" });
          if (!read.success) {
            defaultOutput.errors.push(read.error || "Transcript read failed");
            return defaultOutput;
          }
          const data = read.data as { text?: string; hash?: string };
          transcriptText = data.text || "";
          defaultOutput.facts.push(`Transcript loaded with SHA-256 ${data.hash || "unknown"}.`);
        } else if (mediaExts.has(ext)) {
          const inspect = await context.toolRouter.callTool("aura-voice", "aura.media.inspect", { path: sourcePath, __aeosSkillId: "aura-voice" });
          if (!inspect.success) {
            defaultOutput.errors.push(inspect.error || "Media inspection failed");
            return defaultOutput;
          }
          const base = basename(sourcePath, ext).replace(/[^a-zA-Z0-9._-]+/g, "_");
          const auraDir = join(context.input.workspacePath, ".aeos", "aura-voice");
          const wavPath = join(auraDir, `${base}.wav`);
          const transcriptPrefix = join(auraDir, base);
          const extracted = await context.toolRouter.callTool("aura-voice", "aura.media.extract_audio", { input: sourcePath, output: wavPath, __aeosSkillId: "aura-voice", timeout_ms: 300000 });
          if (!extracted.success) {
            defaultOutput.errors.push(extracted.error || "Audio extraction failed");
            return defaultOutput;
          }
          const transcribed = await context.toolRouter.callTool("aura-voice", "aura.transcribe.local", {
            input: wavPath,
            output_prefix: transcriptPrefix,
            language: String(rawInput.language ?? "auto"),
            __aeosSkillId: "aura-voice",
            timeout_ms: Number(rawInput.timeout_ms ?? 3600000)
          });
          if (!transcribed.success) {
            defaultOutput.errors.push(transcribed.error || "Local transcription failed");
            return defaultOutput;
          }
          const data = transcribed.data as { text?: string; txt?: string; srt?: string; vtt?: string };
          transcriptText = data.text || "";
          for (const artifact of [data.txt, data.srt, data.vtt, wavPath]) if (artifact) defaultOutput.artifacts.push(artifact);
          defaultOutput.facts.push(`Media '${sourcePath}' was extracted and transcribed locally.`);
        } else {
          defaultOutput.errors.push(`Unsupported Aura Voice source extension: ${ext || "(none)"}`);
          return defaultOutput;
        }

        const analysis = await context.toolRouter.callTool("aura-voice", "aura.analyze.transcript", { text: transcriptText, __aeosSkillId: "aura-voice" });
        if (!analysis.success) {
          defaultOutput.errors.push(analysis.error || "Conversation analysis failed");
          return defaultOutput;
        }
        const data = analysis.data as { statistics?: { total?: number; serious?: number; humor?: number; ambiguous?: number }; serious_text?: string };
        const stats = data.statistics || {};
        defaultOutput.facts.push(`Aura Voice classified ${stats.total ?? 0} segments: ${stats.serious ?? 0} serious, ${stats.humor ?? 0} humor and ${stats.ambiguous ?? 0} ambiguous/mixed.`);
        defaultOutput.facts.push("Only the serious lane is eligible for factual critical analysis; humor and ambiguous lanes remain evidence context.");
        if (!data.serious_text) defaultOutput.risks.push("No high-confidence serious statements were found; conclusions must remain limited.");
        return defaultOutput;
      }

      case "chromatic-mega-brain": {
        const rawInput = context.input as unknown as Record<string, unknown>;
        const objective = String(rawInput.objective ?? rawInput.problem ?? "AEOS strategic decision");
        const decisionType = String(rawInput.decision_type ?? "architecture");
        const evidenceRefs = Array.isArray(rawInput.evidence_refs) ? rawInput.evidence_refs : [];
        const selectedColors = this.selectChromaticColors(`${objective} ${decisionType}`);
        const highImpact = ["architecture", "cloud-readiness", "migration", "security", "production-readiness"].includes(decisionType);

        defaultOutput.facts.push(`Chromatic Mega Brain selected colors: ${selectedColors.join(", ")}`);
        defaultOutput.facts.push(`Decision type: ${decisionType}`);
        defaultOutput.assumptions.push("The Node runtime returns a governed chromatic scaffold; the governed execution path must persist the complete evidence record.");
        defaultOutput.risks.push("Chromatic synthesis must go through Judge before high-impact implementation.");
        if (highImpact && evidenceRefs.length === 0) defaultOutput.errors.push("Evidence refs are required for high-impact chromatic decisions.");
        return defaultOutput;
      }

      case "critical-thinking-governor": {
        const selected = context.criticalThinkingPlan.selectedLenses.map((lens) => lens.id);
        defaultOutput.facts.push(`Critical-thinking plan ${context.criticalThinkingPlan.planHash} selected lenses: ${selected.join(", ")}`);
        defaultOutput.facts.push(`Governed skill: ${context.criticalThinkingPlan.skillId}`);
        defaultOutput.assumptions.push("Selected lenses provide structured findings without exposing private chain-of-thought.");
        return defaultOutput;
      }

      case "architecture-mapper":
      case "security-audit":
      case "documentation":
      case "java-migration":
      case "python-rag-audit":
      case "test-generation":
      case "tool-adapter-governor":
        defaultOutput.facts.push(`Skill '${skillId}' is recognized but not yet implemented in v0.1`);
        defaultOutput.assumptions.push(`Using stub implementation for '${skillId}'`);
        return defaultOutput;

      default:
        defaultOutput.errors.push(`Unknown skill: ${skillId}`);
        return defaultOutput;
    }
  }

  private selectChromaticColors(problem: string): string[] {
    const lower = problem.toLowerCase();
    const colors: string[] = ["WHITE"];
    const add = (color: string, terms: string[]): void => {
      if (terms.some((term) => lower.includes(term)) && !colors.includes(color)) colors.push(color);
    };
    add("BLUE", ["architecture", "system", "dependency", "migration", "cloud"]);
    add("RED", ["security", "risk", "failure", "threat", "regression"]);
    add("GREEN", ["implement", "delivery", "test", "deploy", "fix"]);
    add("YELLOW", ["optimize", "performance", "opportunity", "evolve"]);
    add("PURPLE", ["knowledge", "memory", "lesson", "context"]);
    add("ORANGE", ["user", "product", "workflow", "operation"]);
    add("BLACK", ["constraint", "approval", "legal", "secret", "policy"]);
    if (colors.length < 2) colors.push("BLUE");
    return colors.slice(0, 5);
  }
}
