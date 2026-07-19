import { createHash, randomUUID } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, readdirSync, renameSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";

export type SpecPriority = "must" | "should" | "could";
export type VerificationMethod = "test" | "inspection" | "metric" | "manual";
export type SpecStatus = "draft" | "ready" | "approved" | "implementing" | "verifying" | "accepted" | "rejected";

export interface SpecRequirement { id: string; statement: string; priority: SpecPriority }
export interface AcceptanceCriterion {
  id: string;
  requirementIds: string[];
  statement: string;
  verification: VerificationMethod;
  evidence?: { passed: boolean; reference: string; recordedAt: string };
}
export interface SpecApproval { actor: string; evidenceRef: string; normativeHash: string; approvedAt: string }
export interface DrivenSpec {
  schemaVersion: 1;
  slug: string;
  objective: string;
  revision: number;
  status: SpecStatus;
  requirements: SpecRequirement[];
  acceptanceCriteria: AcceptanceCriterion[];
  outOfScope: string[];
  risks: string[];
  approval?: SpecApproval;
  createdAt: string;
  updatedAt: string;
}
export interface SpecValidation { valid: boolean; errors: string[]; warnings: string[]; normativeHash: string }

const now = (): string => new Date().toISOString();
const root = (projectPath: string): string => join(projectPath, ".aeos-runtime", "specs");
const file = (projectPath: string, slug: string): string => join(root(projectPath), slug, "spec.json");

function validSlug(value: string): string {
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(value)) throw new Error("Spec slug must use lowercase kebab-case.");
  return value;
}

function atomicJson(path: string, value: unknown): void {
  mkdirSync(dirname(path), { recursive: true });
  const temporary = `${path}.${randomUUID()}.tmp`;
  writeFileSync(temporary, `${JSON.stringify(value, null, 2)}\n`, "utf8");
  renameSync(temporary, path);
}

function normative(spec: DrivenSpec): unknown {
  return {
    slug: spec.slug,
    objective: spec.objective,
    revision: spec.revision,
    requirements: spec.requirements,
    acceptanceCriteria: spec.acceptanceCriteria.map(({ evidence: _evidence, ...criterion }) => criterion),
    outOfScope: spec.outOfScope,
    risks: spec.risks
  };
}

export function specHash(spec: DrivenSpec): string {
  return createHash("sha256").update(JSON.stringify(normative(spec))).digest("hex");
}

function renderSpecification(spec: DrivenSpec): string {
  const requirements = spec.requirements.map((r) => `- **${r.id}** [${r.priority.toUpperCase()}] ${r.statement}`).join("\n") || "- None";
  const criteria = spec.acceptanceCriteria.map((c) => `- **${c.id}** (${c.requirementIds.join(", ")}; ${c.verification}) ${c.statement}`).join("\n") || "- None";
  return `# ${spec.slug}\n\nStatus: **${spec.status}**  \nRevision: **${spec.revision}**\n\n## Objective\n\n${spec.objective}\n\n## Requirements\n\n${requirements}\n\n## Acceptance Criteria\n\n${criteria}\n\n## Out Of Scope\n\n${spec.outOfScope.map((v) => `- ${v}`).join("\n") || "- None defined"}\n\n## Risks\n\n${spec.risks.map((v) => `- ${v}`).join("\n") || "- None defined"}\n`;
}

function renderPlan(spec: DrivenSpec): string {
  return `# Implementation Plan: ${spec.slug}\n\n1. Validate the specification and traceability matrix.\n2. Obtain explicit approval bound to hash \`${specHash(spec)}\`.\n3. Implement only approved requirements.\n4. Record evidence for every acceptance criterion.\n5. Accept only after deterministic verification.\n`;
}

function writeArtifacts(projectPath: string, spec: DrivenSpec): void {
  const dir = dirname(file(projectPath, spec.slug));
  atomicJson(join(dir, "spec.json"), spec);
  writeFileSync(join(dir, "SPECIFICATION.md"), renderSpecification(spec), "utf8");
  writeFileSync(join(dir, "IMPLEMENTATION_PLAN.md"), renderPlan(spec), "utf8");
  atomicJson(join(dir, "TRACEABILITY.json"), {
    slug: spec.slug,
    normativeHash: specHash(spec),
    requirements: spec.requirements.map((requirement) => ({
      requirementId: requirement.id,
      criteria: spec.acceptanceCriteria.filter((criterion) => criterion.requirementIds.includes(requirement.id)).map((criterion) => ({ id: criterion.id, evidence: criterion.evidence ?? null }))
    }))
  });
}

export function loadSpec(projectPath: string, slug: string): DrivenSpec {
  const path = file(projectPath, validSlug(slug));
  if (!existsSync(path)) throw new Error(`Spec not found: ${slug}`);
  return JSON.parse(readFileSync(path, "utf8")) as DrivenSpec;
}

export function initSpec(projectPath: string, slug: string, objective: string): DrivenSpec {
  validSlug(slug);
  if (!objective.trim()) throw new Error("Spec objective is required.");
  if (existsSync(file(projectPath, slug))) throw new Error(`Spec already exists: ${slug}`);
  const timestamp = now();
  const spec: DrivenSpec = { schemaVersion: 1, slug, objective: objective.trim(), revision: 1, status: "draft", requirements: [], acceptanceCriteria: [], outOfScope: [], risks: [], createdAt: timestamp, updatedAt: timestamp };
  writeArtifacts(projectPath, spec);
  return spec;
}

export function listSpecs(projectPath: string): DrivenSpec[] {
  const dir = root(projectPath);
  if (!existsSync(dir)) return [];
  return readdirSync(dir).filter((name) => existsSync(file(projectPath, name))).sort().map((name) => loadSpec(projectPath, name));
}

function mutate(projectPath: string, slug: string, update: (spec: DrivenSpec) => void): DrivenSpec {
  const spec = loadSpec(projectPath, slug);
  if (["implementing", "verifying", "accepted"].includes(spec.status)) throw new Error(`Normative spec is locked in status: ${spec.status}`);
  update(spec);
  spec.revision += 1;
  spec.status = "draft";
  spec.approval = undefined;
  spec.updatedAt = now();
  writeArtifacts(projectPath, spec);
  return spec;
}

export function addRequirement(projectPath: string, slug: string, statement: string, priority: SpecPriority): DrivenSpec {
  if (!(["must", "should", "could"] as string[]).includes(priority)) throw new Error(`Invalid priority: ${priority}`);
  return mutate(projectPath, slug, (spec) => {
    spec.requirements.push({ id: `REQ-${String(spec.requirements.length + 1).padStart(3, "0")}`, statement: statement.trim(), priority });
  });
}

export function addCriterion(projectPath: string, slug: string, requirementIds: string[], statement: string, verification: VerificationMethod): DrivenSpec {
  if (!(["test", "inspection", "metric", "manual"] as string[]).includes(verification)) throw new Error(`Invalid verification method: ${verification}`);
  return mutate(projectPath, slug, (spec) => {
    spec.acceptanceCriteria.push({ id: `AC-${String(spec.acceptanceCriteria.length + 1).padStart(3, "0")}`, requirementIds: [...new Set(requirementIds)], statement: statement.trim(), verification });
  });
}

export function validateSpec(projectPath: string, slug: string): SpecValidation {
  const spec = loadSpec(projectPath, slug);
  const errors: string[] = [];
  const warnings: string[] = [];
  if (!spec.requirements.length) errors.push("At least one requirement is required.");
  if (!spec.acceptanceCriteria.length) errors.push("At least one acceptance criterion is required.");
  const requirementIds = new Set(spec.requirements.map((r) => r.id));
  if (requirementIds.size !== spec.requirements.length) errors.push("Requirement IDs must be unique.");
  const criterionIds = new Set(spec.acceptanceCriteria.map((c) => c.id));
  if (criterionIds.size !== spec.acceptanceCriteria.length) errors.push("Acceptance criterion IDs must be unique.");
  for (const criterion of spec.acceptanceCriteria) {
    if (!criterion.requirementIds.length) errors.push(`${criterion.id} has no linked requirement.`);
    for (const id of criterion.requirementIds) if (!requirementIds.has(id)) errors.push(`${criterion.id} references unknown requirement ${id}.`);
  }
  for (const requirement of spec.requirements) {
    if (!spec.acceptanceCriteria.some((c) => c.requirementIds.includes(requirement.id))) errors.push(`${requirement.id} is not covered by an acceptance criterion.`);
  }
  if (!spec.outOfScope.length) warnings.push("Out-of-scope items are not defined.");
  if (!spec.risks.length) warnings.push("Risks are not defined.");
  return { valid: errors.length === 0, errors, warnings, normativeHash: specHash(spec) };
}

export function approveSpec(projectPath: string, slug: string, actor: string, evidenceRef: string): DrivenSpec {
  const spec = loadSpec(projectPath, slug);
  const validation = validateSpec(projectPath, slug);
  if (!validation.valid) throw new Error(`Spec validation failed: ${validation.errors.join(" ")}`);
  spec.status = "approved";
  spec.approval = { actor: actor.trim(), evidenceRef: evidenceRef.trim(), normativeHash: validation.normativeHash, approvedAt: now() };
  spec.updatedAt = now();
  writeArtifacts(projectPath, spec);
  return spec;
}

export function startImplementation(projectPath: string, slug: string): DrivenSpec {
  const spec = loadSpec(projectPath, slug);
  if (spec.status !== "approved" || !spec.approval) throw new Error("A current approval is required before implementation.");
  if (spec.approval.normativeHash !== specHash(spec)) throw new Error("Spec changed after approval; re-approval is required.");
  spec.status = "implementing";
  spec.updatedAt = now();
  writeArtifacts(projectPath, spec);
  return spec;
}

export function addEvidence(projectPath: string, slug: string, criterionId: string, passed: boolean, reference: string): DrivenSpec {
  const spec = loadSpec(projectPath, slug);
  if (!["implementing", "verifying"].includes(spec.status)) throw new Error("Evidence is allowed only during implementation or verification.");
  const criterion = spec.acceptanceCriteria.find((item) => item.id === criterionId);
  if (!criterion) throw new Error(`Acceptance criterion not found: ${criterionId}`);
  if (!reference.trim()) throw new Error("Evidence reference is required.");
  criterion.evidence = { passed, reference: reference.trim(), recordedAt: now() };
  spec.status = passed ? "verifying" : "rejected";
  spec.updatedAt = now();
  writeArtifacts(projectPath, spec);
  return spec;
}

export function verifySpec(projectPath: string, slug: string): DrivenSpec {
  const spec = loadSpec(projectPath, slug);
  if (spec.status === "rejected") throw new Error("Rejected specification cannot be accepted.");
  if (!spec.approval || spec.approval.normativeHash !== specHash(spec)) throw new Error("Approval is missing or stale.");
  const incomplete = spec.acceptanceCriteria.filter((criterion) => !criterion.evidence?.passed || !criterion.evidence.reference);
  if (incomplete.length) throw new Error(`Missing passing evidence for: ${incomplete.map((item) => item.id).join(", ")}`);
  spec.status = "accepted";
  spec.updatedAt = now();
  writeArtifacts(projectPath, spec);
  return spec;
}
