import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { ModuleLoader } from "../config/ModuleLoader.js";
export class AeosRuntime {
    version = "0.1.0";
    runtimeDir(projectPath) {
        return join(projectPath, ".aeos-runtime");
    }
    ensureInitialized(projectPath) {
        const runtimeDir = this.runtimeDir(projectPath);
        const statePath = join(runtimeDir, "runtime-state.json");
        mkdirSync(runtimeDir, { recursive: true });
        mkdirSync(join(runtimeDir, "tasks"), { recursive: true });
        mkdirSync(join(runtimeDir, "checkpoints"), { recursive: true });
        mkdirSync(join(runtimeDir, "memory"), { recursive: true });
        mkdirSync(join(runtimeDir, "evidence"), { recursive: true });
        const now = new Date().toISOString();
        const moduleStatus = new ModuleLoader().load(projectPath);
        let initializedAt = now;
        if (existsSync(statePath)) {
            const previous = JSON.parse(readFileSync(statePath, "utf8"));
            initializedAt = previous.initializedAt;
        }
        const state = { projectPath, initializedAt, updatedAt: now, version: this.version, moduleStatus };
        writeFileSync(statePath, `${JSON.stringify(state, null, 2)}\n`, "utf8");
        return state;
    }
    readState(projectPath) {
        const statePath = join(this.runtimeDir(projectPath), "runtime-state.json");
        if (!existsSync(statePath))
            return null;
        return JSON.parse(readFileSync(statePath, "utf8"));
    }
}
//# sourceMappingURL=AeosRuntime.js.map