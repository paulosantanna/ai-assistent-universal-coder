export interface MemoryRecord {
    id: string;
    type: "observation" | "evidence" | "finding" | "lesson" | "validated_lesson" | "golden_knowledge" | "principle";
    summary: string;
    timestamp: string;
    evidenceIds: string[];
}
export declare class MemoryStore {
    append(projectPath: string, record: Omit<MemoryRecord, "id" | "timestamp">): MemoryRecord;
    list(projectPath: string): MemoryRecord[];
}
