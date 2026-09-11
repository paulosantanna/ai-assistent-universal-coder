import { createHash, randomUUID } from "node:crypto";
import { existsSync, lstatSync, readFileSync, realpathSync, statSync } from "node:fs";
import { basename, isAbsolute, posix, relative, resolve, win32 } from "node:path";

export type RuntimeAuthKind = "cookie_file" | "environment";

export interface RuntimeAuthSessionInfo {
  sessionRef: string;
  kind: RuntimeAuthKind;
  sourceRef: string;
  createdAt: string;
  expiresAt: string;
  allowedHosts: string[];
  cookieCount?: number;
}

export interface RuntimeAuthBrokerOptions {
  workspaceRoot?: string;
  defaultTtlSeconds?: number;
  maxTtlSeconds?: number;
  maxCookieFileBytes?: number;
  allowWorkspaceCookieFile?: boolean;
}

type ParsedCookie = {
  name: string;
  value: string;
  domain: string;
  path: string;
  secure: boolean;
  expiresAtMs?: number;
};

type InternalSession = RuntimeAuthSessionInfo & {
  expiresAtMs: number;
  secretValue?: string;
  cookies?: ParsedCookie[];
};

function portableAbsolute(path: string): boolean {
  return isAbsolute(path) || win32.isAbsolute(path) || posix.isAbsolute(path);
}

function normalizeHost(value: string): string {
  return value.trim().toLowerCase().replace(/^\.+/, "").replace(/\.+$/, "");
}

function hostMatches(host: string, pattern: string): boolean {
  const normalizedHost = normalizeHost(host);
  const normalizedPattern = normalizeHost(pattern);
  return normalizedHost === normalizedPattern || normalizedHost.endsWith(`.${normalizedPattern}`);
}

function safeSourceRef(kind: RuntimeAuthKind, source: string): string {
  const digest = createHash("sha256").update(source).digest("hex").slice(0, 12);
  const label = kind === "cookie_file" ? basename(source) : source;
  return `${kind}:${label}:${digest}`;
}

function parseExpires(value: unknown): number | undefined {
  const numeric = Number(value);
  if (!Number.isFinite(numeric) || numeric <= 0) return undefined;
  return numeric > 10_000_000_000 ? numeric : numeric * 1000;
}

function parseJsonCookies(input: unknown): ParsedCookie[] {
  const values = Array.isArray(input)
    ? input
    : input && typeof input === "object" && Array.isArray((input as { cookies?: unknown[] }).cookies)
      ? (input as { cookies: unknown[] }).cookies
      : [];
  const cookies: ParsedCookie[] = [];
  for (const item of values) {
    if (!item || typeof item !== "object") continue;
    const row = item as Record<string, unknown>;
    const name = String(row.name ?? "").trim();
    const value = String(row.value ?? "");
    const domain = normalizeHost(String(row.domain ?? ""));
    if (!name || !domain) continue;
    cookies.push({
      name,
      value,
      domain,
      path: String(row.path ?? "/") || "/",
      secure: Boolean(row.secure),
      expiresAtMs: parseExpires(row.expirationDate ?? row.expires ?? row.expiry)
    });
  }
  return cookies;
}

function parseNetscapeCookies(text: string): ParsedCookie[] {
  const cookies: ParsedCookie[] = [];
  for (const rawLine of text.split(/\r?\n/)) {
    let line = rawLine.trim();
    if (!line) continue;
    if (line.startsWith("#HttpOnly_")) line = line.slice("#HttpOnly_".length);
    else if (line.startsWith("#")) continue;
    const parts = line.split("\t");
    if (parts.length < 7) continue;
    const [domainRaw, , pathRaw, secureRaw, expiresRaw, nameRaw, ...valueParts] = parts;
    const name = String(nameRaw ?? "").trim();
    const domain = normalizeHost(String(domainRaw ?? ""));
    if (!name || !domain) continue;
    cookies.push({
      name,
      value: valueParts.join("\t"),
      domain,
      path: pathRaw || "/",
      secure: String(secureRaw).toUpperCase() === "TRUE",
      expiresAtMs: parseExpires(expiresRaw)
    });
  }
  return cookies;
}

function parseRawCookieHeader(text: string, allowedHosts: string[]): ParsedCookie[] {
  if (allowedHosts.length === 0) return [];
  const line = text.trim().replace(/^cookie\s*:\s*/i, "");
  if (!line || line.includes("\n")) return [];
  const domain = normalizeHost(allowedHosts[0]);
  return line.split(";").map((part) => part.trim()).filter(Boolean).flatMap((part) => {
    const index = part.indexOf("=");
    if (index <= 0) return [];
    return [{ name: part.slice(0, index).trim(), value: part.slice(index + 1), domain, path: "/", secure: true }];
  });
}

function parseCookieFile(text: string, allowedHosts: string[]): ParsedCookie[] {
  try {
    const json = JSON.parse(text) as unknown;
    const parsed = parseJsonCookies(json);
    if (parsed.length > 0) return parsed;
  } catch {
    // Not JSON; continue with Netscape/raw formats.
  }
  const netscape = parseNetscapeCookies(text);
  if (netscape.length > 0) return netscape;
  return parseRawCookieHeader(text, allowedHosts);
}

export class RuntimeAuthBroker {
  private readonly sessions = new Map<string, InternalSession>();
  private readonly workspaceRoot: string;
  private readonly defaultTtlSeconds: number;
  private readonly maxTtlSeconds: number;
  private readonly maxCookieFileBytes: number;
  private readonly allowWorkspaceCookieFile: boolean;

  constructor(options: RuntimeAuthBrokerOptions = {}) {
    this.workspaceRoot = resolve(options.workspaceRoot ?? process.cwd());
    this.defaultTtlSeconds = Math.max(60, Number(options.defaultTtlSeconds ?? 900));
    this.maxTtlSeconds = Math.max(this.defaultTtlSeconds, Number(options.maxTtlSeconds ?? 7200));
    this.maxCookieFileBytes = Math.max(1024, Number(options.maxCookieFileBytes ?? 2 * 1024 * 1024));
    this.allowWorkspaceCookieFile = options.allowWorkspaceCookieFile === true;
  }

  openCookieFile(options: { path: string; allowedHosts?: string[]; ttlSeconds?: number }): RuntimeAuthSessionInfo {
    this.pruneExpired();
    const requestedPath = String(options.path ?? "").trim();
    if (!requestedPath) throw new Error("Runtime cookie file path is required");
    if (!portableAbsolute(requestedPath)) throw new Error("Runtime cookie file must use an absolute external path");
    if (!existsSync(requestedPath)) throw new Error("Runtime cookie file does not exist");
    const realPath = realpathSync(requestedPath);
    const stat = statSync(realPath);
    if (!stat.isFile()) throw new Error("Runtime cookie reference must point to a file");
    if (stat.size > this.maxCookieFileBytes) throw new Error(`Runtime cookie file exceeds ${this.maxCookieFileBytes} bytes`);
    if (lstatSync(realPath).isDirectory()) throw new Error("Runtime cookie reference cannot be a directory");

    if (!this.allowWorkspaceCookieFile) {
      const rel = relative(this.workspaceRoot, realPath);
      if (rel === "" || (!rel.startsWith("..") && !portableAbsolute(rel))) {
        throw new Error("Runtime cookie file must remain outside the tracked workspace");
      }
    }

    const allowedHosts = [...new Set((options.allowedHosts ?? []).map(normalizeHost).filter(Boolean))];
    const text = readFileSync(realPath, "utf8");
    const cookies = parseCookieFile(text, allowedHosts);
    if (cookies.length === 0) throw new Error("Runtime cookie file contains no usable cookies");

    const derivedHosts = [...new Set(cookies.map((cookie) => normalizeHost(cookie.domain)).filter(Boolean))];
    const sessionHosts = allowedHosts.length > 0 ? allowedHosts : derivedHosts;
    if (sessionHosts.length === 0) throw new Error("Runtime cookie session requires at least one allowed host");

    return this.storeSession({
      kind: "cookie_file",
      source: realPath,
      allowedHosts: sessionHosts,
      ttlSeconds: options.ttlSeconds,
      cookies
    });
  }

  openEnvironment(options: { variable: string; allowedHosts?: string[]; ttlSeconds?: number }): RuntimeAuthSessionInfo {
    this.pruneExpired();
    const variable = String(options.variable ?? "").trim();
    if (!/^[A-Za-z_][A-Za-z0-9_]*$/.test(variable)) throw new Error("Invalid runtime environment variable name");
    const value = process.env[variable];
    if (!value) throw new Error(`Runtime environment credential '${variable}' is unavailable`);
    return this.storeSession({
      kind: "environment",
      source: variable,
      allowedHosts: [...new Set((options.allowedHosts ?? []).map(normalizeHost).filter(Boolean))],
      ttlSeconds: options.ttlSeconds,
      secretValue: value
    });
  }

  hasSession(sessionRef: string): boolean {
    this.pruneExpired();
    return this.sessions.has(sessionRef);
  }

  sessionInfo(sessionRef: string): RuntimeAuthSessionInfo {
    const session = this.requireSession(sessionRef);
    return this.publicInfo(session);
  }

  listSessions(): RuntimeAuthSessionInfo[] {
    this.pruneExpired();
    return [...this.sessions.values()].map((session) => this.publicInfo(session));
  }

  closeSession(sessionRef: string): boolean {
    return this.sessions.delete(sessionRef);
  }

  closeAll(): void {
    this.sessions.clear();
  }

  cookieHeader(sessionRef: string, targetUrl: string): string {
    const session = this.requireSession(sessionRef);
    if (session.kind !== "cookie_file" || !session.cookies) throw new Error("Runtime auth session is not a cookie session");
    const target = new URL(targetUrl);
    this.assertAllowedHost(session, target.hostname);
    const now = Date.now();
    const secure = target.protocol === "https:";
    const targetPath = target.pathname || "/";
    const values = session.cookies.filter((cookie) => {
      if (!hostMatches(target.hostname, cookie.domain)) return false;
      if (cookie.secure && !secure) return false;
      if (cookie.expiresAtMs && cookie.expiresAtMs <= now) return false;
      if (!targetPath.startsWith(cookie.path || "/")) return false;
      return true;
    }).map((cookie) => `${cookie.name}=${cookie.value}`);
    if (values.length === 0) throw new Error("Runtime cookie session has no cookies applicable to target URL");
    return values.join("; ");
  }

  secretValue(sessionRef: string, targetHost?: string): string {
    const session = this.requireSession(sessionRef);
    if (session.kind !== "environment" || session.secretValue === undefined) throw new Error("Runtime auth session is not a secret-value session");
    if (targetHost) this.assertAllowedHost(session, targetHost);
    return session.secretValue;
  }

  private storeSession(input: {
    kind: RuntimeAuthKind;
    source: string;
    allowedHosts: string[];
    ttlSeconds?: number;
    secretValue?: string;
    cookies?: ParsedCookie[];
  }): RuntimeAuthSessionInfo {
    const ttlSeconds = Math.min(Math.max(Number(input.ttlSeconds ?? this.defaultTtlSeconds), 60), this.maxTtlSeconds);
    const now = Date.now();
    const sessionRef = `auth_${randomUUID()}`;
    const session: InternalSession = {
      sessionRef,
      kind: input.kind,
      sourceRef: safeSourceRef(input.kind, input.source),
      createdAt: new Date(now).toISOString(),
      expiresAt: new Date(now + ttlSeconds * 1000).toISOString(),
      expiresAtMs: now + ttlSeconds * 1000,
      allowedHosts: input.allowedHosts,
      cookieCount: input.cookies?.length,
      secretValue: input.secretValue,
      cookies: input.cookies
    };
    this.sessions.set(sessionRef, session);
    return this.publicInfo(session);
  }

  private requireSession(sessionRef: string): InternalSession {
    this.pruneExpired();
    const session = this.sessions.get(String(sessionRef ?? ""));
    if (!session) throw new Error("Runtime auth session is missing or expired");
    return session;
  }

  private assertAllowedHost(session: InternalSession, host: string): void {
    if (session.allowedHosts.length === 0) return;
    if (!session.allowedHosts.some((pattern) => hostMatches(host, pattern))) {
      throw new Error(`Runtime auth session is not scoped for host '${host}'`);
    }
  }

  private publicInfo(session: InternalSession): RuntimeAuthSessionInfo {
    return {
      sessionRef: session.sessionRef,
      kind: session.kind,
      sourceRef: session.sourceRef,
      createdAt: session.createdAt,
      expiresAt: session.expiresAt,
      allowedHosts: [...session.allowedHosts],
      ...(session.cookieCount === undefined ? {} : { cookieCount: session.cookieCount })
    };
  }

  private pruneExpired(): void {
    const now = Date.now();
    for (const [ref, session] of this.sessions.entries()) {
      if (session.expiresAtMs <= now) this.sessions.delete(ref);
    }
  }
}
