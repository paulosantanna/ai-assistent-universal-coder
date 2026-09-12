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

type AdapterState = {
  process: ChildProcessWithoutNullStreams | null;
  reader: ReadlineInterface | null;
  pending: Map<string, Pending>;
  adapterPath: string;
  envMode: string;
};

const KINGHOST_COMMERCE_ACTIONS = [
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

const KINGHOST_CONTROL_ACTIONS = [
  "kinghost_control.health",
  "kinghost_control.environment.catalog",
  "kinghost_control.environment.select",
  "kinghost_control.plugin.catalog",
  "kinghost_control.credential.bind",
  "kinghost_control.credential.info",
  "kinghost_control.credential.close",
  "kinghost_control.fsm.state",
  "kinghost_control.fsm.advance",
  "kinghost_control.wordpress.inventory_plan",
  "kinghost_control.wordpress.change_plan",
  "kinghost_control.php.config_plan",
  "kinghost_control.mysql.plan_readonly",
  "kinghost_control.mysql.plan_mutation",
  "kinghost_control.mysql.session.open",
  "kinghost_control.mysql.query_readonly",
  "kinghost_control.mysql.query_mutation",
  "kinghost_control.ftp.session.open",
  "kinghost_control.ftp.list",
  "kinghost_control.ftp.read",
  "kinghost_control.ftp.upload",
  "kinghost_control.ftp.mkdir",
  "kinghost_control.ftp.delete",
  "kinghost_control.session.close",
  "kinghost_control.panel.auth_plan",
  "kinghost_control.backup.plan",
  "kinghost_control.rollback.plan",
  "kinghost_control.verify.smoke_plan",
  "kinghost_control.deploy.workspace_to_production",
  "kinghost_control.knowledge_search"
];

const FALLBACK_COMMERCE: MCPRegistryEntry = {
  id: "kinghost-commerce",
  type: "hosting-commerce-knowledge",
  config: "aeos/mcps/kinghost-commerce.mcp.yaml",
  risk_level: "critical",
  capabilities: KINGHOST_COMMERCE_ACTIONS,
  governing_skill: "kinghost-site-operator",
  skill_intent: "Governed KingHost adapter with ephemeral credentials and controlled mutations.",
  skill_enforced: true,
  write_allowed: true,
  approval_required: true,
  log_redaction_required: true
};

const FALLBACK_CONTROL: MCPRegistryEntry = {
  id: "kinghost-control",
  type: "hosting-control-plane",
  config: "aeos/mcps/kinghost-control.mcp.yaml",
  risk_level: "critical",
  capabilities: KINGHOST_CONTROL_ACTIONS,
  governing_skill: "kinghost-expert",
  skill_intent: "Deterministic KingHost control plane for environments, credential refs, WordPress/PHP/MySQL and FTP.",
  skill_enforced: true,
  write_allowed: true,
  approval_required: true,
  log_redaction_required: true
};

export class KingHostToolRouter extends ToolRouter {
  private kinghostEntries = new Map<string, MCPRegistryEntry>([
    ["kinghost-commerce", FALLBACK_COMMERCE],
    ["kinghost-control", FALLBACK_CONTROL]
  ]);
  private activeKingHostSkill: string | null = null;
  private readonly adapters = new Map<string, AdapterState>();

  constructor(evidenceStore: EvidenceStore, aeosRoot: string) {
    super(evidenceStore);
    this.adapters.set("kinghost-commerce", {
      process: null,
      reader: null,
      pending: new Map(),
      adapterPath: resolve(aeosRoot, "kinghost-commerce-mcp", "index.mjs"),
      envMode: "kinghost-commerce"
    });
    this.adapters.set("kinghost-control", {
      process: null,
      reader: null,
      pending: new Map(),
      adapterPath: resolve(aeosRoot, "kinghost-control-mcp", "index.mjs"),
      envMode: "kinghost-control"
    });
    super.registerMCP(FALLBACK_COMMERCE);
    super.registerMCP(FALLBACK_CONTROL);
  }

  override registerMCP(entry: MCPRegistryEntry): void {
    super.registerMCP(entry);
    if (entry.id === "kinghost-commerce" || entry.id === "kinghost-control") this.kinghostEntries.set(entry.id, entry);
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
    if (mcpId !== "kinghost-commerce" && mcpId !== "kinghost-control") {
      return super.callTool(mcpId, action, params);
    }

    const entry = this.kinghostEntries.get(mcpId) ?? (mcpId === "kinghost-control" ? FALLBACK_CONTROL : FALLBACK_COMMERCE);
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
    return this.callPersistentAdapter(mcpId, action, forwarded);
  }

  async shutdownKingHost(): Promise<void> {
    for (const [id, adapter] of this.adapters.entries()) {
      if (adapter.process && !adapter.process.killed) adapter.process.kill("SIGTERM");
      adapter.reader?.close();
      adapter.process = null;
      adapter.reader = null;
      for (const { resolve, timer } of adapter.pending.values()) {
        clearTimeout(timer);
        resolve({ success: false, error: "KingHost MCP bridge shut down" });
      }
      adapter.pending.clear();
      this.adapters.set(id, adapter);
    }
  }

  private ensureProcess(mcpId: string): ChildProcessWithoutNullStreams {
    const adapter = this.adapters.get(mcpId);
    if (!adapter) throw new Error(`Unknown KingHost adapter ${mcpId}`);
    if (adapter.process && !adapter.process.killed) return adapter.process;

    const child = spawn(process.execPath, [adapter.adapterPath], {
      cwd: dirname(adapter.adapterPath),
      stdio: ["pipe", "pipe", "pipe"],
      env: { ...process.env, AEOS_MCP_MODE: adapter.envMode }
    });

    const reader = createInterface({ input: child.stdout, crlfDelay: Infinity });
    reader.on("line", (line) => {
      try {
        const response = JSON.parse(line) as { request_id?: string; success?: boolean; data?: unknown; error?: string };
        if (!response.request_id) return;
        const pending = adapter.pending.get(response.request_id);
        if (!pending) return;
        clearTimeout(pending.timer);
        adapter.pending.delete(response.request_id);
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
      adapter.process = null;
      adapter.reader?.close();
      adapter.reader = null;
      for (const { resolve, timer } of adapter.pending.values()) {
        clearTimeout(timer);
        resolve({ success: false, error: "KingHost MCP process exited unexpectedly" });
      }
      adapter.pending.clear();
    });

    adapter.process = child;
    adapter.reader = reader;
    return child;
  }

  private callPersistentAdapter(mcpId: string, action: string, params: Record<string, unknown>): Promise<ToolResult> {
    const adapter = this.adapters.get(mcpId);
    if (!adapter) return Promise.resolve({ success: false, error: `Unknown KingHost adapter ${mcpId}` });
    const child = this.ensureProcess(mcpId);
    const requestId = randomUUID();
    const timeoutMs = Math.min(Math.max(Number(params.timeout_ms ?? 30000), 1000), 120000);

    return new Promise<ToolResult>((resolveResult) => {
      const timer = setTimeout(() => {
        adapter.pending.delete(requestId);
        resolveResult({ success: false, error: `KingHost MCP action '${action}' timed out` });
      }, timeoutMs);
      adapter.pending.set(requestId, { resolve: resolveResult, timer });
      child.stdin.write(JSON.stringify({ request_id: requestId, action, params }) + "\n");
    });
  }
}
