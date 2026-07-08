import { appendFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
export class EvidenceLedger {
    add(projectPath, claim, type, reference) {
        const dir = join(projectPath, ".aeos-runtime", "evidence");
        mkdirSync(dir, { recursive: true });
        const evidence = {
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
    list(projectPath) {
        const file = join(projectPath, ".aeos-runtime", "evidence", "evidence.jsonl");
        if (!existsSync(file))
            return [];
        return readFileSync(file, "utf8").split("\n").filter(Boolean).map((line) => JSON.parse(line));
    }
}
//# sourceMappingURL=EvidenceLedger.js.map