import { randomUUID } from "node:crypto";
import type {
  ToolResult,
  FileInfo,
  ToolCallRecord,
  MCPRegistryEntry
} from "./types.js";
import { EvidenceStore } from "./evidence-store.js";

export class ToolRouter {
  private evidenceStore: EvidenceStore;
  private registeredMCPs: Map<string, MCPRegistryEntry> = new Map();
  private toolCalls: ToolCallRecord[] = [];

  constructor(evidenceStore: EvidenceStore) {
    this.evidenceStore = evidenceStore;
  }

  registerMCP(entry: MCPRegistryEntry): void {
    this.registeredMCPs.set(entry.id, entry);
  }

  registerMCPs(entries: MCPRegistryEntry[]): void {
    for (const entry of entries) {
      this.registerMCP(entry);
    }
  }

  async callTool(
    mcpId: string,
    action: string,
    params: Record<string, unknown>
  ): Promise<ToolResult> {
    const mcp = this.registeredMCPs.get(mcpId);
    if (!mcp) {
      return this.recordCall(mcpId, action, params, {
        success: false,
        error: `MCP '${mcpId}' not registered`
      });
    }

    if (!mcp.capabilities.includes(action)) {
      return this.recordCall(mcpId, action, params, {
        success: false,
        error: `Action '${action}' not in MCP '${mcpId}' capabilities`
      });
    }

    const start = Date.now();

    if (mcp.type === "filesystem") {
      const result = await this.handleFilesystem(action, params);
      return this.recordCall(mcpId, action, params, result, Date.now() - start);
    }

    if (mcp.type === "git") {
      const result = await this.handleGit(action, params);
      return this.recordCall(mcpId, action, params, result, Date.now() - start);
    }

    if (mcp.type === "test-runner") {
      const result = await this.handleTestRunner(action, params);
      return this.recordCall(mcpId, action, params, result, Date.now() - start);
    }

    return this.recordCall(mcpId, action, params, {
      success: false,
      error: `Unsupported MCP type: ${mcp.type}`
    });
  }

  getToolCalls(): ToolCallRecord[] {
    return this.toolCalls;
  }

  private async handleFilesystem(
    action: string,
    params: Record<string, unknown>
  ): Promise<ToolResult> {
    switch (action) {
      case "READ_FILES":
      case "read_file": {
        const path = params.path as string;
        if (!path) return { success: false, error: "Missing path parameter" };
        try {
          const { existsSync, readFileSync, statSync } = await import("node:fs");
          if (!existsSync(path)) {
            return { success: false, error: `File not found: ${path}` };
          }
          const content = readFileSync(path, "utf-8");
          const stat = statSync(path);
          this.evidenceStore.writeFilesInspected(path, { size: stat.size, action: "read" });
          return { success: true, data: { content, size: stat.size, path } };
        } catch (err) {
          return { success: false, error: `Read error: ${err instanceof Error ? err.message : String(err)}` };
        }
      }

      case "LIST_DIRECTORIES":
      case "list_directory": {
        const path = params.path as string;
        if (!path) return { success: false, error: "Missing path parameter" };
        try {
          const { existsSync, readdirSync, statSync } = await import("node:fs");
          const { join } = await import("node:path");
          if (!existsSync(path)) {
            return { success: false, error: `Directory not found: ${path}` };
          }
          const entries = readdirSync(path);
          const files: FileInfo[] = entries.map((entry) => {
            const full = join(path, entry);
            try {
              const stat = statSync(full);
              return {
                path: entry,
                size: stat.size,
                isDirectory: stat.isDirectory(),
                extension: stat.isFile() ? (entry.includes(".") ? entry.split(".").pop() ?? "" : "") : "",
                lastModified: stat.mtime.toISOString()
              };
            } catch {
              return { path: entry, size: 0, isDirectory: false, extension: "", lastModified: "" };
            }
          });
          this.evidenceStore.writeFilesInspected(path, { entries: files.length, action: "list" });
          return { success: true, data: { path, files, count: files.length } };
        } catch (err) {
          return { success: false, error: `List error: ${err instanceof Error ? err.message : String(err)}` };
        }
      }

      case "WRITE_SANDBOX_FILES":
      case "write_file": {
        const filePath = params.path as string;
        const content = params.content as string;
        if (!filePath) return { success: false, error: "Missing path parameter" };
        if (content === undefined) return { success: false, error: "Missing content parameter" };
        return {
          success: true,
          data: { path: filePath, written: true, note: "Write allowed (sandbox)" }
        };
      }

      case "file_exists": {
        const checkPath = params.path as string;
        if (!checkPath) return { success: false, error: "Missing path parameter" };
        try {
          const { existsSync } = await import("node:fs");
          return { success: true, data: { path: checkPath, exists: existsSync(checkPath) } };
        } catch {
          return { success: true, data: { path: checkPath, exists: false } };
        }
      }

      default:
        return { success: false, error: `Unknown filesystem action: ${action}` };
    }
  }

  private async handleGit(
    action: string,
    params: Record<string, unknown>
  ): Promise<ToolResult> {
    const { execSync } = await import("node:child_process");
    const cwd = (params.workdir as string) || process.cwd();

    try {
      switch (action) {
        case "GIT_STATUS":
        case "git_status": {
          const output = execSync("git status --short", { cwd, encoding: "utf-8", maxBuffer: 1024 * 1024 });
          return { success: true, data: { status: output.trim() || "(clean)" } };
        }

        case "GIT_DIFF":
        case "git_diff": {
          const pathArg = params.path ? ` -- "${params.path}"` : "";
          const output = execSync(`git diff${pathArg}`, { cwd, encoding: "utf-8", maxBuffer: 1024 * 1024 });
          return { success: true, data: { diff: output || "(no diff)" } };
        }

        case "GIT_LOG":
        case "git_log": {
          const maxCount = (params.max_count as number) || 10;
          const output = execSync(
            `git log --oneline -${maxCount}`,
            { cwd, encoding: "utf-8", maxBuffer: 1024 * 1024 }
          );
          return { success: true, data: { log: output.trim() || "(no commits)" } };
        }

        default:
          return { success: false, error: `Unknown git action: ${action}` };
      }
    } catch (err) {
      return { success: false, error: `Git error: ${err instanceof Error ? err.message : String(err)}` };
    }
  }

  private async handleTestRunner(
    action: string,
    params: Record<string, unknown>
  ): Promise<ToolResult> {
    switch (action) {
      case "RUN_TESTS":
      case "run_tests": {
        const cwd = (params.workdir as string) || process.cwd();
        const framework = (params.framework as string) || "unknown";
        return {
          success: true,
          data: {
            framework,
            note: "Test runner in mock mode for v0.1",
            cwd
          }
        };
      }

      case "list_test_files": {
        const pattern = (params.pattern as string) || "**/*test*";
        return {
          success: true,
          data: { pattern, note: "Test file listing in mock mode for v0.1" }
        };
      }

      default:
        return { success: false, error: `Unknown test-runner action: ${action}` };
    }
  }

  private recordCall(
    mcpId: string,
    action: string,
    params: Record<string, unknown>,
    result: ToolResult,
    durationMs: number = 0
  ): ToolResult {
    const record: ToolCallRecord = {
      callId: randomUUID(),
      tool: mcpId,
      action,
      params: this.sanitizeParams(params),
      result: result.success ? "success" : `error: ${result.error ?? "unknown"}`,
      allowed: true,
      timestamp: new Date().toISOString(),
      durationMs
    };
    this.toolCalls.push(record);
    this.evidenceStore.writeToolCall(record);
    return result;
  }

  private sanitizeParams(params: Record<string, unknown>): Record<string, unknown> {
    const sanitized: Record<string, unknown> = {};
    for (const [key, value] of Object.entries(params)) {
      if (key.toLowerCase().includes("secret") || key.toLowerCase().includes("password") || key.toLowerCase().includes("token") || key.toLowerCase().includes("key") || key.toLowerCase().includes("credential")) {
        sanitized[key] = "***REDACTED***";
      } else {
        sanitized[key] = value;
      }
    }
    return sanitized;
  }
}
