import { existsSync, mkdirSync, appendFileSync, writeFileSync, readFileSync } from "node:fs";
import { join, resolve, dirname } from "node:path";
import type { EvidenceRecord, ToolCallRecord, PermissionDecision } from "./types.js";

export class EvidenceStore {
  private baseDir: string;

  constructor(baseDir: string) {
    this.baseDir = resolve(baseDir);
    this.ensureDir();
  }

  private ensureDir(): void {
    mkdirSync(this.baseDir, { recursive: true });
  }

  get evidenceDir(): string {
    return this.baseDir;
  }

  writeEvidence(record: EvidenceRecord): void {
    this.appendJsonl("evidence.jsonl", record);
  }

  writeToolCall(record: ToolCallRecord): void {
    this.appendJsonl("tool-calls.jsonl", record);
  }

  writePermissionDecision(record: PermissionDecision): void {
    this.appendJsonl("permission-decisions.jsonl", record);
  }

  writeFilesInspected(filePath: string, details: Record<string, unknown>): void {
    this.appendJsonl("files-inspected.jsonl", { filePath, ...details, timestamp: new Date().toISOString() });
  }

  writeGeneratedArtifact(relativePath: string, content: string): string {
    const abs = resolve(this.baseDir, relativePath);
    mkdirSync(dirname(abs), { recursive: true });
    writeFileSync(abs, content, "utf-8");
    this.appendJsonl("generated-artifacts.jsonl", {
      path: relativePath,
      size: content.length,
      timestamp: new Date().toISOString()
    });
    return abs;
  }

  readJsonl(filename: string): string[] {
    const filePath = join(this.baseDir, filename);
    if (!existsSync(filePath)) return [];
    const content = readFileSync(filePath, "utf-8");
    return content.split("\n").filter(Boolean);
  }

  private appendJsonl(filename: string, record: unknown): void {
    const filePath = join(this.baseDir, filename);
    mkdirSync(dirname(filePath), { recursive: true });
    appendFileSync(filePath, JSON.stringify(record) + "\n", "utf-8");
  }
}
