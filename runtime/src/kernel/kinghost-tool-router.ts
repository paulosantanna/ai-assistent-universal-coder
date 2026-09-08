import { spawn, type ChildProcessWithoutNullStreams } from "node:child_process";
import { createInterface, type Interface as ReadlineInterface } from "node:readline";
import { dirname, resolve } from "node:path";
import { randomUUID } from "node:crypto";
import { ToolRouter } from "./tool-router.js";
import { EvidenceStore } from "./evidence-store.js";
import type { MCPRegistryEntry, ToolResult } from "./types.js";

type Pending = {
  resolve: (result: ToolResult) => void;
  timer: NodeJS.Timeout;
};

const KINGHOST_ACTIONS = [
  "kinghost.health",
  "kinghost.session.open_ssh",
  "kinghost.session.open_mysql",
  "kinghost.session.open_postgres",
  "kinghost.session.info",
  "kinghost.session.close",
  "kinghost.fs.list",
  "kinghost.fs.read",
  "kinghost.fs.write",
  "kinghost.fs.mkdir",
  "kinghost.fs.rename",
  "kinghost.fs.delete",
  "kinghost.ssh.exec_readonly",
  "kinghost.db.query_readonly",
  "kinghost.db.query_mutation",
  "kinghost.knowledge_search",
  "kinghost.inspect_environment",
  "kinghost.performance_audit",
  "kinghost.deploy_plan",
  "kinghost.database_plan",
  "kinghost.dns_plan",
  "commerce.catalog_plan",
  "commerce.channel_mapping",
  "commerce.price_sync_plan",
  "commerce.logistics_plan",
  "web.modernization_plan",
  "web.performance_budget"
];

const FALLBACK_ENTRY: MCPRegistryEntry = {
  id: "kinghost-commerce",
  type: "hosting-commerce-knowledge",
  config: "aeos/mcps/kinghost-commerce.mcp.yaml",
  risk_level: "critical",
  capabilities: KINGHOST_ACTIONS,
  governing_skill: "kinghost-site-operator",
  skill_intent: "Governed KingHost adapter with ephemeral credentials and controlled mutations.",
  skill_enforced: true,
  write_allowed: true,
  approval_required: true,
  log_redaction_required: true
};

export class KingHostToolRouter extends ToolRouter {
  private kinghostEntry: MCPRegistryEntry = FALLBACK_ENTRY;
  private activeKingHostSkill: string | null = null;
  private process: ChildProcessWithoutNullStreams | null = null;
  private reader: ReadlineInterface | null = null;
  private pending = new Map<string, Pending>();
  private readonly adapterPath: string;

  constructor(evidenceStore: EvidenceStore, aeosRoot: string) {
    super(evidenceStore);
    this.adapterPath = resolve(aeosRoot, "kinghost-commerce-mcp", "index.mjs");
    super.registerMCP(FALLBACK_ENTRY);
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
      cwd: dirname(this.adapterPath),
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
        // Malformed adapter output is ignored; pending request times out fail-closed.
      }
    });

    child.stderr.on("data", () => {
      // Do not copy raw vendor stderr into durable AEOS evidence.
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
