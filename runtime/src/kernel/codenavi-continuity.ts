export const CODENAVI_CONTINUITY_SKILLS = new Set([
  "continuity-bootstrapper",
  "handoff-manager",
  "memory-curator",
  "progress-tracker",
  "learning-curator"
] as const);

export const CODENAVI_CONTINUITY_FILES = [
  ".notebook/HANDOFF.md",
  ".notebook/MEMORY.md",
  ".notebook/PROGRESS.md",
  ".notebook/LEARNING.md"
] as const;

export type ContinuitySkillId =
  | "continuity-bootstrapper"
  | "handoff-manager"
  | "memory-curator"
  | "progress-tracker"
  | "learning-curator";

const SECRET_PATTERNS = [
  /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/,
  /\b(?:ghp|github_pat|sk)-[A-Za-z0-9_-]{20,}\b/,
  /\b(?:password|passwd|secret|token)\s*[:=]\s*["']?[^\s"'`]{8,}/i
];

export function validateContinuityText(text: string): string[] {
  const errors: string[] = [];
  if (text.length > 250_000) errors.push("continuity payload exceeds 250KB");
  for (const pattern of SECRET_PATTERNS) {
    if (pattern.test(text)) {
      errors.push("potential raw secret detected in continuity payload");
      break;
    }
  }
  return errors;
}

export function continuitySkillFacts(skillId: ContinuitySkillId): string[] {
  switch (skillId) {
    case "continuity-bootstrapper":
      return [
        `Required continuity artifacts: ${CODENAVI_CONTINUITY_FILES.join(", ")}.`,
        "Missing artifacts must be created from canonical templates; populated files must not be overwritten blindly."
      ];
    case "handoff-manager":
      return ["HANDOFF stores only the last verified transfer state and exact next actions."];
    case "memory-curator":
      return ["MEMORY accepts durable evidence-backed facts and decisions, not transient task status."];
    case "progress-tracker":
      return ["PROGRESS is the live source of truth and closes items only after their acceptance gates pass."];
    case "learning-curator":
      return ["LEARNING promotes generalized evidence-backed lessons only after verification."];
  }
}
