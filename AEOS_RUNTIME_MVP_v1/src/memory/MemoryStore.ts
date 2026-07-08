import { appendFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

export interface MemoryRecord {
  id: string;
  type: "observation" | "evidence" | "finding" | "lesson" | "validated_lesson" | "golden_knowledge" | "principle";
  summary: string;
  timestamp: string;
  evidenceIds: string[];
}

export class MemoryStore {
  public append(projectPath: string, record: Omit<MemoryRecord, "id" | "timestamp">): MemoryRecord {
    const dir = join(projectPath, ".aeos-runtime", "memory");
    mkdirSync(dir, { recursive: true });
    const full: MemoryRecord = { id: crypto.randomUUID(), timestamp: new Date().toISOString(), ...record };
    appendFileSync(join(dir, "memory.jsonl"), `${JSON.stringify(full)}\n`, "utf8");
    return full;
  }

  public list(projectPath: string): MemoryRecord[] {
    const file = join(projectPath, ".aeos-runtime", "memory", "memory.jsonl");
    if (!existsSync(file)) return [];
    return readFileSync(file, "utf8").split("\n").filter(Boolean).map((line) => JSON.parse(line) as MemoryRecord);
  }
}
