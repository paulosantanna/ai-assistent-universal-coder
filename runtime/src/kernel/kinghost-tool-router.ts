import { spawn, type ChildProcessWithoutNullStreams } from "node:child_process";
import { createInterface, type Interface as ReadlineInterface } from "node:readline";
import { resolve } from "node:path";
import { randomUUID } from "node:crypto";
import { ToolRouter } from "./tool-router.js";
import { EvidenceStore } from "./evidence-store.js";
import type { MCPRegistryEntry, ToolResult } from "./types.js";

type Pending = {
  resolve: (result: ToolResult) => void;
  timer: NodeJS.Timeout;
};

export class KingHostToolRouter extends ToolRouter {
  private kinghostEntry: MCPRegistryEntry | null = null;
  private activeKingHostSkill: string | null = null;
  private process: ChildProcessWithoutNullStreams | null = null;
  private reader: ReadlineInterface | null = null;
  private pending = new Map<string, Pending>();
  private readonly adapterPath: string;

  constructor(evidenceStore: EvidenceStore, aeosRoot: string) {
    super(evidenceStore);
    this.adapterPath = resolve(aeosRoot, "kinghost-commerce-mcp", "index.mjs");
  }

  override registerMCP(entry: MCPRegistryEntry): void {
    super.registerMCP(entry);
    if (entry.id === "kinghost-commerce") this.kinghostEntry = entry;
  }

  override registerMCPs(entries: MCPRegistryEntry[]): void {
    for (const entry of entries) this.registerMCP(entry);
  }

  override setActiveSkill(skillId: string | null): void {
    this.activeKingHostSkill = skillId;
    super.setActiveSkill(skillId);
  }

  override async callTool(
    mcpId: string,
    action: string,
    params: Record<string, unknown>
  ): Promise<ToolResult> {
    if (mcpId !== "kinghost-commerce") return super.callTool(mcpId, action, params);

    const entry = this.kinghostEntry;
    if (!entry) return { success: false, error: "MCP 'kinghost-commerce' not registered" };
    if (!entry.governing_skill) return { success: false, error: "KingHost MCP blocked: missing governing_skill" };

    const skillId = typeof params.__aeosSkillId === "string"
      ? params.__aeosSkillId
      : this.activeKingHostSkill;
    if (entry.skill_enforced !== false && !skillId) {
      return { success: false, error: "KingHost MCP blocked: active AEOS skill context required" };
    }
    if (!entry.capabilities.includes(action)) {
      return { success: false, error: `Action '${action}' not allowlisted for KingHost MCP` };
    }

    const forwarded = { ...params };
    delete forwarded.__aeosSkillId;
    return this.callPersistentAdapter(action, forwarded);
  }

  async shutdownKingHost(): Promise<void> {
    if (this.process && !this.process.killed) this.process.kill("SIGTERM");
    this.reader?.close();
    this.process = null;
    this.reader = null;
    for (const { resolve, timer } of this.pending.values()) {
      clearTimeout(timer);
      resolve({ success: false, error: "KingHost MCP bridge shut down" });
    }
    this.pending.clear();
  }

  private ensureProcess(): ChildProcessWithoutNullStreams {
    if (this.process && !this.process.killed) return this.process;

    const child = spawn(process.execPath, [this.adapterPath], {
      cwd: resolve(this.adapterPath, ".."),
      stdio: ["pipe", "pipe", "pipe"],
      env: { ...process.env, AEOS_MCP_MODE: "kinghost-commerce" }
    });

    const reader = createInterface({ input: child.stdout, crlfDelay: Infinity });
    reader.on("line", (line) => {
      try {
        const response = JSON.parse(line) as { request_id?: string; success?: boolean; data?: unknown; error?: string };
        if (!response.request_id) return;
        const pending = this.pending.get(response.request_id);
        if (!pending) return;
        clearTimeout(pending.timer);
        this.pending.delete(response.request_id);
        pending.resolve(response.success
          ? { success: true, data: response.data }
          : { success: false, error: response.error || "KingHost adapter error" });
      } catch {
        // Malformed adapter output is ignored and its request will time out fail-closed.
      }
    });

    child.stderr.on("data", () => {
      // Deliberately do not copy adapter stderr into AEOS evidence: it may contain vendor errors.
    });
    child.on("exit", () => {
      this.process = null;
      this.reader?.close();
      this.reader = null;
      for (const { resolve, timer } of this.pending.values()) {
        clearTimeout(timer);
        resolve({ success: false, error: "KingHost MCP process exited unexpectedly" });
      }
      this.pending.clear();
    });

    this.process = child;
    this.reader = reader;
    return child;
  }

  private callPersistentAdapter(action: string, params: Record<string, unknown>): Promise<ToolResult> {
    const child = this.ensureProcess();
    const requestId = randomUUID();
    const timeoutMs = Math.min(Math.max(Number(params.timeout_ms ?? 30000), 1000), 120000);

    return new Promise<ToolResult>((resolveResult) => {
      const timer = setTimeout(() => {
        this.pending.delete(requestId);
        resolveResult({ success: false, error: `KingHost MCP action '${action}' timed out` });
      }, timeoutMs);
      this.pending.set(requestId, { resolve: resolveResult, timer });
      child.stdin.write(JSON.stringify({ request_id: requestId, action, params }) + "\n");
    });
  }
}
