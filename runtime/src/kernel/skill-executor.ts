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
}
