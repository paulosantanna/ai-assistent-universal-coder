import type {
  SkillRegistryEntry,
  SkillInput,
  SkillOutput,
  ExecutionContext
} from "./types.js";
import { ToolRouter } from "./tool-router.js";
import { EvidenceStore } from "./evidence-store.js";
import { RepoScannerSkill } from "./skills/repo-scanner.js";

export interface SkillContext {
  registryEntry: SkillRegistryEntry;
  input: SkillInput;
  toolRouter: ToolRouter;
  evidenceStore: EvidenceStore;
  executionContext: ExecutionContext;
}

export class SkillExecutor {
  async execute(skillId: string, context: SkillContext): Promise<SkillOutput> {
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

        // Evidence and artifacts are collected by PlaybookEngine from skill output
        context.executionContext.artifacts.push(...output.artifacts);

        return output;
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
        defaultOutput.assumptions.push("Node runtime returns a governed chromatic scaffold; Python runtime produces the full evidence record.");
        defaultOutput.risks.push("Chromatic synthesis must go through Judge before high-impact implementation.");

        if (highImpact && evidenceRefs.length === 0) {
          defaultOutput.errors.push("Evidence refs are required for high-impact chromatic decisions.");
        }

        return defaultOutput;
      }

      case "architecture-mapper":
      case "security-audit":
      case "documentation":
      case "java-migration":
      case "python-rag-audit":
      case "test-generation":
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
      if (terms.some((term) => lower.includes(term)) && !colors.includes(color)) {
        colors.push(color);
      }
    };

    add("BLUE", ["architecture", "system", "dependency", "migration", "cloud"]);
    add("RED", ["security", "risk", "failure", "threat", "regression"]);
    add("GREEN", ["implement", "delivery", "test", "deploy", "fix"]);
    add("YELLOW", ["optimize", "performance", "opportunity", "evolve"]);
    add("PURPLE", ["knowledge", "memory", "lesson", "context"]);
    add("ORANGE", ["user", "product", "workflow", "operation"]);
    add("BLACK", ["constraint", "approval", "legal", "secret", "policy"]);

    if (colors.length < 2) {
      colors.push("BLUE");
    }
    return colors.slice(0, 5);
  }
}
