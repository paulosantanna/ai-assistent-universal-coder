import type { Evidence, EvidenceType } from "../types.js";
export declare class EvidenceLedger {
    add(projectPath: string, claim: string, type: EvidenceType, reference: string): Evidence;
    list(projectPath: string): Evidence[];
}
