import { randomUUID } from "node:crypto";
import { lookup } from "node:dns/promises";
import type {
  ToolResult,
  FileInfo,
  ToolCallRecord,
  MCPRegistryEntry
} from "./types.js";
import { EvidenceStore } from "./evidence-store.js";
import { RuntimeAuthBroker } from "./runtime-auth-broker.js";

const AUTH_SESSION_KEY = "__aeosAuthSessionRef";
const SENSITIVE_KEY = /(secret|password|token|credential|cookie|authorization|nonce|private.?key)/i;

function isPrivateAddress(address: string): boolean {
  const value = address.toLowerCase();
  if (value === "::1" || value === "0.0.0.0" || value.startsWith("127.")) return true;
  if (value.startsWith("10.") || value.startsWith("192.168.") || value.startsWith("169.254.")) return true;
  const match = /^(172)\.(\d{1,3})\./.exec(value);
  if (match && Number(match[2]) >= 16 && Number(match[2]) <= 31) return true;
  return value.startsWith("fc") || value.startsWith("fd") || value.startsWith("fe80:");
}

async function assertPublicHttpsTarget(rawUrl: string): Promise<URL> {
  const target = new URL(rawUrl);
  if (target.protocol !== "https:") throw new Error("Authenticated runtime HTTP requires HTTPS");
  if (target.username || target.password) throw new Error("Credentials in target URL are forbidden");
  const host = target.hostname.toLowerCase();
  if (host === "localhost" || host.endsWith(".localhost")) throw new Error("Authenticated runtime HTTP blocks localhost targets");
  const addresses = await lookup(host, { all: true, verbatim: true });
  if (addresses.length === 0 || addresses.some((entry) => isPrivateAddress(entry.address))) {
    throw new Error("Authenticated runtime HTTP blocks private/local network targets");
  }
  return target;
}

export class ToolRouter {
  private evidenceStore: EvidenceStore;
  private registeredMCPs: Map<string, MCPRegistryEntry> = new Map();
  private toolCalls: ToolCallRecord[] = [];
  private activeSkillId: string | null = null;
  private readonly runtimeAuthBroker: RuntimeAuthBroker;

  constructor(evidenceStore: EvidenceStore, runtimeAuthBroker?: RuntimeAuthBroker) {
    this.evidenceStore = evidenceStore;
    this.runtimeAuthBroker = runtimeAuthBroker ?? new RuntimeAuthBroker();
  }

  registerMCP(entry: MCPRegistryEntry): void {
    this.registeredMCPs.set(entry.id, entry);
  }

  registerMCPs(entries: MCPRegistryEntry[]): void {
    for (const entry of entries) this.registerMCP(entry);
  }

  setActiveSkill(skillId: string | null): void {
    this.activeSkillId = skillId;
  }

  shutdownRuntimeAuth(): void {
    this.runtimeAuthBroker.closeAll();
  }

  async callTool(
    mcpId: string,
    action: string,
    params: Record<string, unknown>
  ): Promise<ToolResult> {
    const mcp = this.registeredMCPs.get(mcpId);
    if (!mcp) {
      return this.recordCall(mcpId, action, params, { success: false, error: `MCP '${mcpId}' not registered` });
    }

    const skillId = this.resolveSkillContext(params);
    const skillGate = this.validateSkillGate(mcp, skillId);
    if (!skillGate.success) return this.recordCall(mcpId, action, params, skillGate);

    if (!mcp.capabilities.includes(action)) {
      return this.recordCall(mcpId, action, params, { success: false, error: `Action '${action}' not in MCP '${mcpId}' capabilities` });
    }

    const sessionRef = params[AUTH_SESSION_KEY];
    if (mcp.type !== "runtime-auth" && sessionRef !== undefined) {
      if (typeof sessionRef !== "string" || !this.runtimeAuthBroker.hasSession(sessionRef)) {
        return this.recordCall(mcpId, action, params, { success: false, error: "Runtime auth session is missing or expired" });
      }
    }

    const start = Date.now();
    let result: ToolResult;
    if (mcp.type === "filesystem") result = await this.handleFilesystem(action, params);
    else if (mcp.type === "git") result = await this.handleGit(action, params);
    else if (mcp.type === "test-runner") result = await this.handleTestRunner(action, params);
    else if (mcp.type === "runtime-auth") result = await this.handleRuntimeAuth(action, params);
    else if (mcp.type === "runtime-http") result = await this.handleRuntimeHttp(action, params);
    else result = { success: false, error: `Unsupported MCP type: ${mcp.type}` };
    return this.recordCall(mcpId, action, params, result, Date.now() - start);
  }

  getToolCalls(): ToolCallRecord[] {
    return this.toolCalls;
  }

  protected runtimeCookieHeader(sessionRef: string, targetUrl: string): string {
    return this.runtimeAuthBroker.cookieHeader(sessionRef, targetUrl);
  }

  protected runtimeSecretValue(sessionRef: string, targetHost?: string): string {
    return this.runtimeAuthBroker.secretValue(sessionRef, targetHost);
  }

  private resolveSkillContext(params: Record<string, unknown>): string | null {
    const explicit = params.__aeosSkillId;
    return typeof explicit === "string" && explicit.trim().length > 0 ? explicit.trim() : this.activeSkillId;
  }

  private validateSkillGate(mcp: MCPRegistryEntry, skillId: string | null): ToolResult {
    if (!mcp.governing_skill || mcp.governing_skill.trim().length === 0) {
      return { success: false, error: `MCP '${mcp.id}' blocked: missing governing_skill contract` };
    }
    if (mcp.skill_enforced === false) return { success: true };
    if (!skillId) return { success: false, error: `MCP '${mcp.id}' blocked: calls must run inside an AEOS skill context` };
    return { success: true };
  }

  private async handleRuntimeAuth(action: string, params: Record<string, unknown>): Promise<ToolResult> {
    try {
      if (action === "auth.session.open_cookie_file") {
        const path = String(params.cookie_file_path ?? params.path ?? "").trim();
        const allowedHosts = Array.isArray(params.allowed_hosts) ? params.allowed_hosts.map(String) : [];
        const info = this.runtimeAuthBroker.openCookieFile({ path, allowedHosts, ttlSeconds: Number(params.ttl_seconds ?? 900) });
        return { success: true, data: info };
      }
      if (action === "auth.session.open_environment") {
        const variable = String(params.variable ?? "").trim();
        const allowedHosts = Array.isArray(params.allowed_hosts) ? params.allowed_hosts.map(String) : [];
        const info = this.runtimeAuthBroker.openEnvironment({ variable, allowedHosts, ttlSeconds: Number(params.ttl_seconds ?? 900) });
        return { success: true, data: info };
      }
      if (action === "auth.session.info") {
        return { success: true, data: this.runtimeAuthBroker.sessionInfo(String(params.session_ref ?? "")) };
      }
      if (action === "auth.session.list") {
        return { success: true, data: { sessions: this.runtimeAuthBroker.listSessions() } };
      }
      if (action === "auth.session.close") {
        return { success: true, data: { closed: this.runtimeAuthBroker.closeSession(String(params.session_ref ?? "")) } };
      }
      return { success: false, error: `Unknown runtime-auth action: ${action}` };
    } catch (err) {
      return { success: false, error: `Runtime auth error: ${err instanceof Error ? err.message : String(err)}` };
    }
  }

  private async handleRuntimeHttp(action: string, params: Record<string, unknown>): Promise<ToolResult> {
    if (action !== "http.authenticated.request") return { success: false, error: `Unknown runtime-http action: ${action}` };
    const sessionRef = String(params[AUTH_SESSION_KEY] ?? params.session_ref ?? "").trim();
    if (!sessionRef) return { success: false, error: "Authenticated runtime HTTP requires an opaque auth session_ref" };
    const rawUrl = String(params.url ?? "").trim();
    if (!rawUrl) return { success: false, error: "Authenticated runtime HTTP requires url" };
    const method = String(params.method ?? "GET").toUpperCase();
    const allowedMethods = new Set(["GET", "HEAD", "OPTIONS", "POST", "PUT", "PATCH", "DELETE"]);
    if (!allowedMethods.has(method)) return { success: false, error: `HTTP method '${method}' is not allowlisted` };
    if (!["GET", "HEAD", "OPTIONS"].includes(method) && params.approved !== true) {
      return { success: false, error: "Authenticated HTTP mutation requires approved=true from a governed change gate" };
    }

    try {
      const target = await assertPublicHttpsTarget(rawUrl);
      const cookie = this.runtimeAuthBroker.cookieHeader(sessionRef, target.toString());
      const headers = new Headers();
      headers.set("Accept", "application/json, text/html;q=0.9, */*;q=0.8");
      headers.set("Cookie", cookie);
      headers.set("User-Agent", "AEOS-Runtime-HTTP/1.0");
      if (params.headers && typeof params.headers === "object") {
        for (const [key, value] of Object.entries(params.headers as Record<string, unknown>)) {
          if (/^(cookie|authorization|proxy-authorization)$/i.test(key)) continue;
          headers.set(key, String(value));
        }
      }

      let body: BodyInit | undefined;
      if (params.body !== undefined && method !== "GET" && method !== "HEAD") {
        if (typeof params.body === "string") body = params.body;
        else {
          body = JSON.stringify(params.body);
          if (!headers.has("Content-Type")) headers.set("Content-Type", "application/json");
        }
      }

      const timeoutMs = Math.min(Math.max(Number(params.timeout_ms ?? 15000), 1000), 60000);
      const maxBytes = Math.min(Math.max(Number(params.max_bytes ?? 1024 * 1024), 1024), 5 * 1024 * 1024);
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), timeoutMs);
      try {
        const response = await fetch(target, { method, headers, body, redirect: "manual", signal: controller.signal });
        const contentLength = Number(response.headers.get("content-length") ?? 0);
        if (contentLength > maxBytes) return { success: false, error: `Authenticated HTTP response exceeds ${maxBytes} bytes` };
        const bytes = new Uint8Array(await response.arrayBuffer());
        if (bytes.byteLength > maxBytes) return { success: false, error: `Authenticated HTTP response exceeds ${maxBytes} bytes` };
        const text = Buffer.from(bytes).toString("utf8");
        const contentType = response.headers.get("content-type") ?? "";
        let data: unknown = text;
        if (contentType.includes("json") || text.trim().startsWith("{") || text.trim().startsWith("[")) {
          try { data = text ? JSON.parse(text) : null; } catch { data = text; }
        }
        return {
          success: response.ok,
          data: {
            status: response.status,
            content_type: contentType,
            location: response.headers.get("location"),
            body: data,
            bytes: bytes.byteLength,
            redirect_followed: false
          },
          ...(response.ok ? {} : { error: `Authenticated HTTP returned ${response.status}` })
        };
      } finally {
        clearTimeout(timer);
      }
    } catch (err) {
      return { success: false, error: `Authenticated HTTP error: ${err instanceof Error ? err.message : String(err)}` };
    }
  }

  private async handleFilesystem(action: string, params: Record<string, unknown>): Promise<ToolResult> {
    switch (action) {
      case "READ_FILES":
      case "read_file": {
        const path = params.path as string;
        if (!path) return { success: false, error: "Missing path parameter" };
        try {
          const { existsSync, readFileSync, statSync } = await import("node:fs");
          if (!existsSync(path)) return { success: false, error: `File not found: ${path}` };
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
          if (!existsSync(path)) return { success: false, error: `Directory not found: ${path}` };
          const entries = readdirSync(path);
          const files: FileInfo[] = entries.map((entry) => {
            const full = join(path, entry);
            try {
              const stat = statSync(full);
              return { path: entry, size: stat.size, isDirectory: stat.isDirectory(), extension: stat.isFile() ? (entry.includes(".") ? entry.split(".").pop() ?? "" : "") : "", lastModified: stat.mtime.toISOString() };
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
        return { success: true, data: { path: filePath, written: true, note: "Write allowed (sandbox)" } };
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

  private async handleGit(action: string, params: Record<string, unknown>): Promise<ToolResult> {
    const { execFileSync } = await import("node:child_process");
    const cwd = (params.workdir as string) || process.cwd();
    try {
      switch (action) {
        case "GIT_STATUS":
        case "git_status": {
          const output = execFileSync("git", ["status", "--short"], { cwd, encoding: "utf-8", maxBuffer: 1024 * 1024 });
          return { success: true, data: { status: output.trim() || "(clean)" } };
        }
        case "GIT_DIFF":
        case "git_diff": {
          const args = ["diff"];
          if (params.path !== undefined) {
            if (typeof params.path !== "string" || params.path.length === 0) return { success: false, error: "Git diff path must be a non-empty string" };
            args.push("--", params.path);
          }
          const output = execFileSync("git", args, { cwd, encoding: "utf-8", maxBuffer: 1024 * 1024 });
          return { success: true, data: { diff: output || "(no diff)" } };
        }
        case "GIT_LOG":
        case "git_log": {
          const parsedMax = Number(params.max_count ?? 10);
          const maxCount = Number.isFinite(parsedMax) ? Math.min(Math.max(Math.trunc(parsedMax), 1), 100) : 10;
          const output = execFileSync("git", ["log", "--oneline", `-${maxCount}`], { cwd, encoding: "utf-8", maxBuffer: 1024 * 1024 });
          return { success: true, data: { log: output.trim() || "(no commits)" } };
        }
        default:
          return { success: false, error: `Unknown git action: ${action}` };
      }
    } catch (err) {
      return { success: false, error: `Git error: ${err instanceof Error ? err.message : String(err)}` };
    }
  }

  private async handleTestRunner(action: string, params: Record<string, unknown>): Promise<ToolResult> {
    switch (action) {
      case "RUN_TESTS":
      case "run_tests": {
        const cwd = (params.workdir as string) || process.cwd();
        const framework = (params.framework as string) || "unknown";
        return { success: true, data: { framework, note: "Test runner in mock mode for v0.1", cwd } };
      }
      case "list_test_files": {
        const pattern = (params.pattern as string) || "**/*test*";
        return { success: true, data: { pattern, note: "Test file listing in mock mode for v0.1" } };
      }
      default:
        return { success: false, error: `Unknown test-runner action: ${action}` };
    }
  }

  private recordCall(mcpId: string, action: string, params: Record<string, unknown>, result: ToolResult, durationMs: number = 0): ToolResult {
    const record: ToolCallRecord = {
      callId: randomUUID(),
      tool: mcpId,
      action,
      skillId: this.resolveSkillContext(params) ?? undefined,
      governingSkill: this.registeredMCPs.get(mcpId)?.governing_skill,
      params: this.sanitizeParams(params),
      result: result.success ? "success" : `error: ${result.error ?? "unknown"}`,
      allowed: result.success,
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
      if (SENSITIVE_KEY.test(key)) sanitized[key] = "***REDACTED***";
      else if (key === AUTH_SESSION_KEY || key === "session_ref") sanitized[key] = typeof value === "string" ? `opaque:${value.slice(-8)}` : "opaque";
      else sanitized[key] = this.sanitizeValue(value);
    }
    return sanitized;
  }

  private sanitizeValue(value: unknown): unknown {
    if (Array.isArray(value)) return value.map((item) => this.sanitizeValue(item));
    if (value && typeof value === "object") {
      const nested: Record<string, unknown> = {};
      for (const [key, nestedValue] of Object.entries(value as Record<string, unknown>)) {
        if (SENSITIVE_KEY.test(key)) nested[key] = "***REDACTED***";
        else if (key === AUTH_SESSION_KEY || key === "session_ref") nested[key] = typeof nestedValue === "string" ? `opaque:${nestedValue.slice(-8)}` : "opaque";
        else nested[key] = this.sanitizeValue(nestedValue);
      }
      return nested;
    }
    return value;
  }
}
