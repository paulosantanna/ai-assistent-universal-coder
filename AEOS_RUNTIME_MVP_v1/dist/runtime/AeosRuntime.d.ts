import type { RuntimeState } from "../types.js";
export declare class AeosRuntime {
    private readonly version;
    runtimeDir(projectPath: string): string;
    ensureInitialized(projectPath: string): RuntimeState;
    readState(projectPath: string): RuntimeState | null;
}
