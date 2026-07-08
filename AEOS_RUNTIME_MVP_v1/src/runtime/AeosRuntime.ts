import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import type { RuntimeState } from "../types.js";
import { ModuleLoader } from "../config/ModuleLoader.js";

export class AeosRuntime {
  private readonly version = "0.1.0";

  public runtimeDir(projectPath: string): string {
    return join(projectPath, ".aeos-runtime");
  }

  public ensureInitialized(projectPath: string): RuntimeState {
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
      const previous = JSON.parse(readFileSync(statePath, "utf8")) as RuntimeState;
      initializedAt = previous.initializedAt;
    }

    const state: RuntimeState = { projectPath, initializedAt, updatedAt: now, version: this.version, moduleStatus };
    writeFileSync(statePath, `${JSON.stringify(state, null, 2)}\n`, "utf8");
    return state;
  }

  public readState(projectPath: string): RuntimeState | null {
    const statePath = join(this.runtimeDir(projectPath), "runtime-state.json");
    if (!existsSync(statePath)) return null;
    return JSON.parse(readFileSync(statePath, "utf8")) as RuntimeState;
  }
}
