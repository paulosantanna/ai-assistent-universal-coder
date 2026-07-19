export type SpecPriority = "must" | "should" | "could";
export type VerificationMethod = "test" | "inspection" | "metric" | "manual";
export type SpecStatus = "draft" | "ready" | "approved" | "implementing" | "verifying" | "accepted" | "rejected";
export interface SpecRequirement {
    id: string;
    statement: string;
    priority: SpecPriority;
}
export interface AcceptanceCriterion {
    id: string;
    requirementIds: string[];
    statement: string;
    verification: VerificationMethod;
    evidence?: {
        passed: boolean;
        reference: string;
        recordedAt: string;
    };
}
export interface SpecApproval {
    actor: string;
    evidenceRef: string;
    normativeHash: string;
    approvedAt: string;
}
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
export interface SpecValidation {
    valid: boolean;
    errors: string[];
    warnings: string[];
    normativeHash: string;
}
export declare function specHash(spec: DrivenSpec): string;
export declare function loadSpec(projectPath: string, slug: string): DrivenSpec;
export declare function initSpec(projectPath: string, slug: string, objective: string): DrivenSpec;
export declare function listSpecs(projectPath: string): DrivenSpec[];
export declare function addRequirement(projectPath: string, slug: string, statement: string, priority: SpecPriority): DrivenSpec;
export declare function addCriterion(projectPath: string, slug: string, requirementIds: string[], statement: string, verification: VerificationMethod): DrivenSpec;
export declare function validateSpec(projectPath: string, slug: string): SpecValidation;
export declare function approveSpec(projectPath: string, slug: string, actor: string, evidenceRef: string): DrivenSpec;
export declare function startImplementation(projectPath: string, slug: string): DrivenSpec;
export declare function addEvidence(projectPath: string, slug: string, criterionId: string, passed: boolean, reference: string): DrivenSpec;
export declare function verifySpec(projectPath: string, slug: string): DrivenSpec;
