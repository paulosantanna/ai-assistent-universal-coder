import { createHash, randomUUID } from "node:crypto";
import { existsSync, lstatSync, readFileSync, realpathSync, statSync } from "node:fs";
import { basename, isAbsolute, posix, relative, resolve, win32 } from "node:path";

const DEFAULT_TTL_MS = 15 * 60 * 1000;
const MAX_COOKIE_BYTES = 2 * 1024 * 1024;
const DEFAULT_HOSTS = ["painel.kinghost.com.br", "kinghost.com.br", "king.host", "kinghost.net"];

const panelSessions = new Map();

function portableAbsolute(path) {
  return isAbsolute(path) || win32.isAbsolute(path) || posix.isAbsolute(path);
}

function normalizeHost(value) {
  return String(value || "").trim().toLowerCase().replace(/^\.+/, "").replace(/\.+$/, "");
}

function hostMatches(host, pattern) {
  const normalizedHost = normalizeHost(host);
  const normalizedPattern = normalizeHost(pattern);
  return normalizedHost === normalizedPattern || normalizedHost.endsWith(`.${normalizedPattern}`);
}

function parseExpires(value) {
  const numeric = Number(value);
  if (!Number.isFinite(numeric) || numeric <= 0) return undefined;
  return numeric > 10_000_000_000 ? numeric : numeric * 1000;
}

function parseJsonCookies(input) {
  const values = Array.isArray(input)
    ? input
    : input && typeof input === "object" && Array.isArray(input.cookies)
      ? input.cookies
      : [];
  const cookies = [];
  for (const item of values) {
    if (!item || typeof item !== "object") continue;
    const name = String(item.name ?? "").trim();
    const domain = normalizeHost(String(item.domain ?? ""));
    if (!name || !domain) continue;
    cookies.push({
      name,
      value: String(item.value ?? ""),
      domain,
      path: String(item.path ?? "/") || "/",
      secure: Boolean(item.secure),
      expiresAtMs: parseExpires(item.expirationDate ?? item.expires ?? item.expiry)
    });
  }
  return cookies;
}

function parseNetscapeCookies(text) {
  const cookies = [];
  for (const rawLine of String(text).split(/\r?\n/)) {
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

function parseCookieFile(text) {
  try {
    const json = JSON.parse(text);
    const parsed = parseJsonCookies(json);
    if (parsed.length > 0) return parsed;
  } catch {
    // Netscape / raw header next.
  }
  return parseNetscapeCookies(text);
}

function assertOutsideWorkspace(realPath, workspaceRoot) {
  const root = resolve(workspaceRoot);
  const rel = relative(root, realPath);
  if (rel === "" || (!rel.startsWith("..") && !portableAbsolute(rel))) {
    throw new Error("Runtime cookie file must remain outside the tracked workspace");
  }
}

function prune() {
  const now = Date.now();
  for (const [id, session] of panelSessions.entries()) {
    if (session.expiresAt <= now) panelSessions.delete(id);
  }
}

function publicInfo(session) {
  return {
    panel_session_ref: session.id,
    kind: "panel_cookie",
    source_ref: session.sourceRef,
    allowed_hosts: [...session.allowedHosts],
    cookie_count: session.cookies.length,
    created_at: new Date(session.createdAt).toISOString(),
    expires_at: new Date(session.expiresAt).toISOString()
  };
}

export function openCookieFile(params = {}, { workspaceRoot = process.cwd() } = {}) {
  prune();
  const requestedPath = String(params.cookie_file_path || params.path || "").trim();
  if (!requestedPath) throw new Error("cookie_file_path is required");
  if (!portableAbsolute(requestedPath)) throw new Error("cookie_file_path must be an absolute external path");
  if (!existsSync(requestedPath)) throw new Error("Runtime cookie file does not exist");
  const realPath = realpathSync(requestedPath);
  const stat = statSync(realPath);
  if (!stat.isFile()) throw new Error("Runtime cookie reference must point to a file");
  if (stat.size > MAX_COOKIE_BYTES) throw new Error(`Runtime cookie file exceeds ${MAX_COOKIE_BYTES} bytes`);
  if (lstatSync(realPath).isDirectory()) throw new Error("Runtime cookie reference cannot be a directory");
  if (params.allow_workspace_cookie_file !== true) assertOutsideWorkspace(realPath, workspaceRoot);

  const text = readFileSync(realPath, "utf8");
  const cookies = parseCookieFile(text);
  if (cookies.length === 0) throw new Error("Runtime cookie file contains no usable cookies");

  const requestedHosts = [...new Set((Array.isArray(params.allowed_hosts) ? params.allowed_hosts : DEFAULT_HOSTS).map(normalizeHost).filter(Boolean))];
  const derivedHosts = [...new Set(cookies.map((cookie) => cookie.domain).filter(Boolean))];
  const allowedHosts = requestedHosts.length > 0 ? requestedHosts : derivedHosts;
  const inScope = cookies.some((cookie) => allowedHosts.some((pattern) => hostMatches(cookie.domain, pattern) || hostMatches(pattern, cookie.domain)));
  if (!inScope) throw new Error("Cookie jar has no cookies scoped to KingHost panel hosts");

  const id = `panel_${randomUUID()}`;
  const now = Date.now();
  const digest = createHash("sha256").update(realPath).digest("hex").slice(0, 12);
  const session = {
    id,
    cookies,
    allowedHosts,
    sourceRef: `cookie_file:${basename(realPath)}:${digest}`,
    createdAt: now,
    expiresAt: now + DEFAULT_TTL_MS
  };
  panelSessions.set(id, session);
  return publicInfo(session);
}

export function getPanelSession(ref) {
  prune();
  const session = panelSessions.get(String(ref || ""));
  if (!session) throw new Error("Unknown or expired panel_session_ref");
  if (session.expiresAt <= Date.now()) {
    panelSessions.delete(session.id);
    throw new Error("Panel cookie session expired");
  }
  session.expiresAt = Date.now() + DEFAULT_TTL_MS;
  return session;
}

export function panelSessionInfo(ref) {
  return publicInfo(getPanelSession(ref));
}

export function closePanelSession(ref) {
  return panelSessions.delete(String(ref || ""));
}

export function cookieHeaderFor(session, targetUrl) {
  const target = new URL(targetUrl);
  if (target.protocol !== "https:") throw new Error("Panel HTTP requires HTTPS");
  if (!session.allowedHosts.some((pattern) => hostMatches(target.hostname, pattern))) {
    throw new Error(`Panel session is not scoped for host '${target.hostname}'`);
  }
  const now = Date.now();
  const targetPath = target.pathname || "/";
  const values = session.cookies.filter((cookie) => {
    if (!(hostMatches(target.hostname, cookie.domain) || hostMatches(cookie.domain, target.hostname))) return false;
    if (cookie.secure && target.protocol !== "https:") return false;
    if (cookie.expiresAtMs && cookie.expiresAtMs <= now) return false;
    if (!targetPath.startsWith(cookie.path || "/")) return false;
    return true;
  }).map((cookie) => `${cookie.name}=${cookie.value}`);
  if (values.length === 0) throw new Error("Panel cookie session has no cookies applicable to target URL");
  return values.join("; ");
}

const BLOCKED_DOMAIN_SUFFIXES = [
  "kinghost.com.br",
  "king.host",
  "kinghost.net",
  "google.com",
  "gstatic.com",
  "googleapis.com",
  "facebook.com",
  "cloudflare.com",
  "w3.org",
  "schema.org"
];

export function extractDomainsFromHtml(html) {
  const text = String(html || "");
  const found = new Set();
  const patterns = [
    /data-domain=["']([^"']+)["']/gi,
    /["']domain["']\s*:\s*["']([^"']+)["']/gi,
    /href=["'][^"']*\/(?:dominio|domain|site|hospedagem)\/([^"'/?#]+)["']/gi,
    /\b((?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+(?:com\.br|net\.br|org\.br|com|net|org|app|store|blog|dev|io|host))\b/gi
  ];
  for (const pattern of patterns) {
    pattern.lastIndex = 0;
    let match;
    while ((match = pattern.exec(text))) {
      const candidate = normalizeHost(match[1]);
      if (!candidate.includes(".")) continue;
      if (BLOCKED_DOMAIN_SUFFIXES.some((suffix) => candidate === suffix || candidate.endsWith(`.${suffix}`))) continue;
      if (candidate.split(".").length < 2) continue;
      found.add(candidate);
    }
  }
  return [...found].sort();
}

export function looksLikeLoginPage(html) {
  return /entrar no painel|login do painel|senha de acesso/i.test(String(html || ""));
}

export async function fetchPanelReadonly(params = {}) {
  const session = getPanelSession(params.panel_session_ref || params.session_ref);
  const url = String(params.url || "https://painel.kinghost.com.br/").trim();
  const target = new URL(url);
  if (target.protocol !== "https:") throw new Error("Panel fetch requires HTTPS");
  const cookie = cookieHeaderFor(session, target.toString());
  const response = await fetch(target.toString(), {
    method: "GET",
    redirect: "manual",
    headers: {
      Accept: "text/html,application/json;q=0.9,*/*;q=0.8",
      Cookie: cookie,
      "User-Agent": "AEOS-KingHost-Control/1.1"
    }
  });
  const body = await response.text();
  return {
    url: target.toString(),
    status: response.status,
    redirected: response.status >= 300 && response.status < 400,
    login_page: looksLikeLoginPage(body),
    byte_length: Buffer.byteLength(body),
    sha256: createHash("sha256").update(body).digest("hex"),
    domains: extractDomainsFromHtml(body)
  };
}

export function panelSessionCount() {
  prune();
  return panelSessions.size;
}

export { DEFAULT_HOSTS };
