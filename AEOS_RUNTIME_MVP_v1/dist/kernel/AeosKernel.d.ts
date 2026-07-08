import type { EvidenceType } from "../types.js";
export declare class AeosKernel {
    private readonly runtime;
    private readonly scheduler;
    private readonly evidence;
    private readonly memory;
    private readonly judgeEngine;
    init(projectPath: string): void;
    status(projectPath: string): void;
    plan(projectPath: string, objective: string): void;
    checkpoint(projectPath: string, summary: string): void;
    addEvidence(projectPath: string, claim: string, type: EvidenceType, reference: string): void;
    judge(projectPath: string, taskId: string): void;
}
