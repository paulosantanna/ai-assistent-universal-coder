import { appendFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import type { Evidence, EvidenceType } from "../types.js";

export class EvidenceLedger {
  public add(projectPath: string, claim: string, type: EvidenceType, reference: string): Evidence {
    const dir = join(projectPath, ".aeos-runtime", "evidence");
    mkdirSync(dir, { recursive: true });
    const evidence: Evidence = {
      evidenceId: crypto.randomUUID(),
      type,
      claim,
      reference,
      verified: true,
      timestamp: new Date().toISOString(),
      limitations: []
    };
    appendFileSync(join(dir, "evidence.jsonl"), `${JSON.stringify(evidence)}\n`, "utf8");
    return evidence;
  }

  public list(projectPath: string): Evidence[] {
    const file = join(projectPath, ".aeos-runtime", "evidence", "evidence.jsonl");
    if (!existsSync(file)) return [];
    return readFileSync(file, "utf8").split("\n").filter(Boolean).map((line) => JSON.parse(line) as Evidence);
  }
}
