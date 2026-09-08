import { spawn, type ChildProcessWithoutNullStreams } from "node:child_process";
import { createInterface, type Interface as ReadlineInterface } from "node:readline";
import { dirname, resolve } from "node:path";
import { randomUUID } from "node:crypto";
import { KingHostToolRouter } from "./kinghost-tool-router.js";
import { EvidenceStore } from "./evidence-store.js";
import type { MCPRegistryEntry, ToolResult } from "./types.js";

type Pending = { resolve: (result: ToolResult) => void; timer: NodeJS.Timeout };

const AURA_ACTIONS = [
  "aura.health",
  "aura.media.inspect",
  "aura.media.extract_audio",
  "aura.transcript.read",
  "aura.transcribe.local",
  "aura.analyze.transcript",
  "aura.corpus.ingest"
];

const FALLBACK_AURA: MCPRegistryEntry = {
  id: "aura-voice",
  type: "media-intelligence",
  config: "aeos/mcps/aura-voice.mcp.yaml",
  risk_level: "high",
  capabilities: AURA_ACTIONS,
  governing_skill: "aura-voice",
  skill_intent: "Governed transcription and conversation analysis with terminology preservation and humor separation.",
  skill_enforced: true,
  write_allowed: true,
  approval_required: false,
  log_redaction_required: true
};

export class AuraVoiceToolRouter extends KingHostToolRouter {
  private auraEntry: MCPRegistryEntry = FALLBACK_AURA;
  private activeAuraSkill: string | null = null;
  private auraProcess: ChildProcessWithoutNullStreams | null = null;
  private auraReader: ReadlineInterface | null = null;
  private auraPending = new Map<string, Pending>();
  private readonly auraAdapterPath: string;

  constructor(evidenceStore: EvidenceStore, aeosRoot: string) {
    super(evidenceStore, aeosRoot);
    this.auraAdapterPath = resolve(aeosRoot, "aura-voice-tool", "index.mjs");
    super.registerMCP(FALLBACK_AURA);
  }

  override registerMCP(entry: MCPRegistryEntry): void {
    super.registerMCP(entry);
    if (entry.id === "aura-voice") this.auraEntry = entry;
  }

  override setActiveSkill(skillId: string | null): void {
    this.activeAuraSkill = skillId;
    super.setActiveSkill(skillId);
  }

  override async callTool(mcpId: string, action: string, params: Record<string, unknown>): Promise<ToolResult> {
    if (mcpId !== "aura-voice") return super.callTool(mcpId, action, params);
    const entry = this.auraEntry;
    const skillId = typeof params.__aeosSkillId === "string" ? params.__aeosSkillId : this.activeAuraSkill;
    if (entry.skill_enforced !== false && !skillId) {
      return { success: false, error: "Aura Voice MCP blocked: active AEOS skill context required" };
    }
    if (!entry.capabilities.includes(action)) {
      return { success: false, error: `Action '${action}' not allowlisted for Aura Voice MCP` };
    }
    const forwarded = { ...params };
    delete forwarded.__aeosSkillId;
    return this.callAuraAdapter(action, forwarded);
  }

  async shutdownAuraVoice(): Promise<void> {
    if (this.auraProcess && !this.auraProcess.killed) this.auraProcess.kill("SIGTERM");
    this.auraReader?.close();
    this.auraProcess = null;
    this.auraReader = null;
    for (const { resolve, timer } of this.auraPending.values()) {
      clearTimeout(timer);
      resolve({ success: false, error: "Aura Voice MCP bridge shut down" });
    }
    this.auraPending.clear();
    await this.shutdownKingHost();
  }

  private ensureAuraProcess(): ChildProcessWithoutNullStreams {
    if (this.auraProcess && !this.auraProcess.killed) return this.auraProcess;
    const child = spawn(process.execPath, [this.auraAdapterPath], {
      cwd: dirname(this.auraAdapterPath),
      stdio: ["pipe", "pipe", "pipe"],
      env: { ...process.env, AEOS_MCP_MODE: "aura-voice" }
    });
    const reader = createInterface({ input: child.stdout, crlfDelay: Infinity });
    reader.on("line", line => {
      try {
        const response = JSON.parse(line) as { request_id?: string; success?: boolean; data?: unknown; error?: string };
        if (!response.request_id) return;
        const pending = this.auraPending.get(response.request_id);
        if (!pending) return;
        clearTimeout(pending.timer);
        this.auraPending.delete(response.request_id);
        pending.resolve(response.success ? { success: true, data: response.data } : { success: false, error: response.error || "Aura Voice adapter error" });
      } catch {
        // Ignore malformed child output; pending call times out fail-closed.
      }
    });
    child.stderr.on("data", () => { /* raw ASR/media stderr is intentionally not copied to evidence */ });
    child.on("exit", () => {
      this.auraProcess = null;
      this.auraReader?.close();
      this.auraReader = null;
      for (const { resolve, timer } of this.auraPending.values()) {
        clearTimeout(timer);
        resolve({ success: false, error: "Aura Voice MCP process exited unexpectedly" });
      }
      this.auraPending.clear();
    });
    this.auraProcess = child;
    this.auraReader = reader;
    return child;
  }

  private callAuraAdapter(action: string, params: Record<string, unknown>): Promise<ToolResult> {
    const child = this.ensureAuraProcess();
    const requestId = randomUUID();
    const timeoutMs = Math.min(Math.max(Number(params.timeout_ms ?? 30000), 1000), 3600000);
    return new Promise<ToolResult>(resolveResult => {
      const timer = setTimeout(() => {
        this.auraPending.delete(requestId);
        resolveResult({ success: false, error: `Aura Voice action '${action}' timed out` });
      }, timeoutMs);
      this.auraPending.set(requestId, { resolve: resolveResult, timer });
      child.stdin.write(JSON.stringify({ request_id: requestId, action, params }) + "\n");
    });
  }
}
