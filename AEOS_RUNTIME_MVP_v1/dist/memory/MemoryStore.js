import { appendFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
export class MemoryStore {
    append(projectPath, record) {
        const dir = join(projectPath, ".aeos-runtime", "memory");
        mkdirSync(dir, { recursive: true });
        const full = { id: crypto.randomUUID(), timestamp: new Date().toISOString(), ...record };
        appendFileSync(join(dir, "memory.jsonl"), `${JSON.stringify(full)}\n`, "utf8");
        return full;
    }
    list(projectPath) {
        const file = join(projectPath, ".aeos-runtime", "memory", "memory.jsonl");
        if (!existsSync(file))
            return [];
        return readFileSync(file, "utf8").split("\n").filter(Boolean).map((line) => JSON.parse(line));
    }
}
//# sourceMappingURL=MemoryStore.js.map