#!/usr/bin/env node
import { createInterface } from "node:readline";
import { randomUUID, createHash } from "node:crypto";
import { readFileSync, existsSync, statSync } from "node:fs";
import { resolve, relative, sep, dirname, join } from "node:path";
import { pathToFileURL, fileURLToPath } from "node:url";
import { FtpClient } from "./ftp-client.mjs";

const credentials = new Map();
const ftpSessions = new Map();
const mysqlSessions = new Map();
const fsmRuns = new Map();
const selectedEnvironment = new Map();

const MAX_READ_BYTES = 2_000_000;
const DEFAULT_TTL_MS = 15 * 60 * 1000;
const FSM_ORDER = [
  "IDLE",
  "ENV_SELECTED",
  "CREDENTIALS_BOUND",
  "PANEL_AUTH",
  "INVENTORY",
  "SNAPSHOT",
  "DIFF",
  "DRY_RUN",
  "BACKUP",
  "APPLY",
  "VERIFY",
  "CLOSE"
];

const ENVIRONMENTS = [
  { id: "local", label: "Local WordPress runtime", mutation_default: "workspace-only", ftp_default: false },
  { id: "staging", label: "KingHost staging or preview host", mutation_default: "approval-required", ftp_default: true },
  { id: "production", label: "KingHost production", mutation_default: "approval-dry-run-rollback", ftp_default: true }
];

const KINGHOST_TOOLS = [
  { id: "ftp", family: "publish", title: "FTP" },
  { id: "sftp", family: "publish", title: "SFTP" },
  { id: "ssh", family: "publish", title: "SSH" },
  { id: "file-manager", family: "files", title: "File Manager" },
  { id: "mysql", family: "database", title: "MySQL" },
  { id: "phpmyadmin", family: "database", title: "phpMyAdmin" },
  { id: "postgres", family: "database", title: "PostgreSQL" },
  { id: "php-version", family: "runtime", title: "PHP version manager" },
  { id: "wordpress", family: "application", title: "WordPress" },
  { id: "dns", family: "network", title: "DNS" },
  { id: "ssl", family: "network", title: "SSL certificates" },
  { id: "email", family: "network", title: "Email" },
  { id: "backup", family: "operations", title: "Backups" },
  { id: "cron", family: "operations", title: "Cron" },
  { id: "logs", family: "operations", title: "Logs" },
  { id: "resources", family: "operations", title: "Resource monitor" },
  { id: "git-deploy", family: "publish", title: "Git publication" },
  { id: "domains", family: "network", title: "Domains and subdomains" }
];

const WP_BLOCKED_REMOTE = [
  /^\/?wp-admin(\/|$)/i,
  /^\/?wp-includes(\/|$)/i,
  /(^|\/)wp-config\.php$/i,
  /(^|\/)wp-config-sample\.php$/i
];

const SECRET_KEYS = /(password|passwd|secret|token|cookie|authorization|private[_-]?key|nonce)/i;
const READONLY_SQL = /^\s*(select|show|describe|desc|explain|with\b[\s\S]*select)\b/i;
const MUTATING_SQL = /\b(insert|update|delete|replace|merge|truncate|drop|alter|create|grant|revoke|rename|call|load\s+data)\b/i;
const HIGH_RISK_SQL = /\b(truncate|drop|grant|revoke|load\s+data)\b/i;

function now() { return Date.now(); }
function sha256(value) { return createHash("sha256").update(value).digest("hex"); }
function ok(data = {}) { return { success: true, data }; }
function fail(error, code = "BLOCKED") { return { success: false, error, code }; }

function redact(value) {
  return String(value ?? "").replace(/(password|passwd|token|secret|cookie|authorization|private[_-]?key)\s*[=:]\s*\S+/gi, "$1=***REDACTED***");
}

function redactObject(input) {
  if (!input || typeof input !== "object") return input;
  const out = Array.isArray(input) ? [] : {};
  for (const [key, value] of Object.entries(input)) {
    if (SECRET_KEYS.test(key)) out[key] = "***REDACTED***";
    else if (value && typeof value === "object") out[key] = redactObject(value);
    else out[key] = value;
  }
  return out;
}

function requireNoCredentialDiscovery(params) {
  const blob = JSON.stringify(params || {}).toLowerCase();
  if (/(discover|extract|harvest|dump|scrape|brute|stuffing|credential_scan|session_dump)/.test(blob) && /credential|password|cookie|secret/.test(blob)) {
    throw new Error("Credential discovery, scraping or dumping is forbidden; bind already-provisioned runtime credentials");
  }
}

function requireMutationGate(params) {
  if (params?.approved !== true) throw new Error("approved=true is required for mutating operations");
  if (!String(params?.change_id || "").trim()) throw new Error("change_id is required for mutating operations");
  if (!String(params?.rollback_ref || "").trim()) throw new Error("rollback_ref is required for mutating operations");
}

function envRecord(id) {
  return ENVIRONMENTS.find((item) => item.id === id) || null;
}

function credentialMeta(entry) {
  return {
    credential_ref: entry.id,
    kind: entry.kind,
    source_class: entry.sourceClass,
    host: entry.host,
    port: entry.port,
    username: entry.username,
    environment_id: entry.environmentId,
    has_secret: Boolean(entry.secret),
    created_at: new Date(entry.createdAt).toISOString(),
    expires_at: new Date(entry.expiresAt).toISOString()
  };
}

function getCredential(ref, kind) {
  const entry = credentials.get(ref);
  if (!entry) throw new Error("Unknown or expired credential_ref");
  if (entry.expiresAt <= now()) {
    credentials.delete(ref);
    throw new Error("Credential binding expired");
  }
  if (kind && entry.kind !== kind) throw new Error(`Credential kind mismatch: expected ${kind}, got ${entry.kind}`);
  entry.expiresAt = now() + DEFAULT_TTL_MS;
  return entry;
}

function getFtp(ref) {
  const session = ftpSessions.get(ref);
  if (!session) throw new Error("Unknown or expired ftp session_ref");
  if (session.expiresAt <= now()) {
    session.client.close();
    ftpSessions.delete(ref);
    throw new Error("FTP session expired");
  }
  session.expiresAt = now() + DEFAULT_TTL_MS;
  return session;
}

function resolveUnderRoot(root, candidate) {
  const base = resolve(root);
  const target = resolve(base, candidate || ".");
  const rel = relative(base, target);
  if (rel.startsWith("..") || rel.startsWith(`..${sep}`)) throw new Error("Path escapes the approved root");
  return target;
}

function remoteAllowed(remoteRoot, remotePath, { highRisk = false } = {}) {
  const normalized = String(remotePath || "").replace(/\\/g, "/").replace(/^\/+/, "");
  const root = String(remoteRoot || "").replace(/\\/g, "/").replace(/^\/+|\/+$/g, "");
  if (root && !(normalized === root || normalized.startsWith(`${root}/`))) {
    throw new Error("Remote path is outside the approved FTP root");
  }
  if (!highRisk && WP_BLOCKED_REMOTE.some((pattern) => pattern.test(normalized))) {
    throw new Error("WordPress core or wp-config.php mutation requires high_risk_approved=true");
  }
  return normalized;
}

function bindCredential(params) {
  requireNoCredentialDiscovery(params);
  const kind = String(params.kind || "").trim().toLowerCase();
  if (!["ftp", "sftp", "mysql", "panel", "wp-admin"].includes(kind)) {
    return fail("kind must be ftp|sftp|mysql|panel|wp-admin");
  }
  const sourceClass = String(params.source_class || "env_reference").trim();
  const allowedSources = ["env_reference", "secret_reference", "runtime_memory", "cookie_session_panel"];
  if (!allowedSources.includes(sourceClass)) return fail(`source_class must be one of ${allowedSources.join(", ")}`);

  let username = String(params.username || "").trim();
  let secret = params.password || params.secret || "";
  let host = String(params.host || "").trim();
  let port = Number(params.port || (kind === "ftp" ? 21 : kind === "mysql" ? 3306 : 443));

  if (sourceClass === "env_reference") {
    const userKey = String(params.username_env || "").trim();
    const secretKey = String(params.password_env || params.secret_env || "").trim();
    const hostKey = String(params.host_env || "").trim();
    const portKey = String(params.port_env || "").trim();
    if (userKey) username = String(process.env[userKey] || username).trim();
    if (secretKey) secret = String(process.env[secretKey] || secret);
    if (hostKey) host = String(process.env[hostKey] || host).trim();
    if (portKey && process.env[portKey]) port = Number(process.env[portKey]);
  }

  if (sourceClass === "secret_reference") {
    const name = String(params.secret_ref || "").trim();
    if (!name) return fail("secret_ref is required for secret_reference");
    return fail(`Secret reference '${name}' must be materialized by runtime-auth/Tool Router; this MCP does not read secret stores`);
  }

  if (sourceClass === "cookie_session_panel") {
    if (!params.session_ref && !params.__aeosAuthSessionRef) {
      return fail("cookie_session_panel requires an opaque runtime-auth session_ref");
    }
    return ok({
      status: "PLAN",
      source_class: sourceClass,
      kind,
      session_ref_present: true,
      next: "Use Playwright/browser with the cookie session to confirm the KingHost panel identity, then bind FTP/MySQL via env_reference or runtime_memory. Never copy panel passwords into evidence."
    });
  }

  if (!username) return fail("username is required to bind an already-provisioned credential");
  if ((kind === "ftp" || kind === "sftp" || kind === "mysql") && !secret) {
    return fail("password/secret is required as ephemeral runtime input or env_reference");
  }
  if ((kind === "ftp" || kind === "sftp" || kind === "mysql") && !host) {
    return fail("host is required");
  }

  const id = `cred_${randomUUID()}`;
  const entry = {
    id,
    kind,
    sourceClass,
    username,
    secret,
    host,
    port,
    environmentId: String(params.environment_id || selectedEnvironment.get("default") || ""),
    createdAt: now(),
    expiresAt: now() + DEFAULT_TTL_MS
  };
  credentials.set(id, entry);
  return ok(credentialMeta(entry));
}

function environmentSelect(params) {
  const id = String(params.environment_id || params.id || "").trim();
  const env = envRecord(id);
  if (!env) return fail(`Unknown environment_id. Allowed: ${ENVIRONMENTS.map((item) => item.id).join(", ")}`);
  selectedEnvironment.set("default", env.id);
  const changeId = String(params.change_id || randomUUID());
  fsmRuns.set(changeId, { change_id: changeId, state: "ENV_SELECTED", environment_id: env.id, history: ["IDLE", "ENV_SELECTED"] });
  return ok({ environment: env, change_id: changeId, fsm_state: "ENV_SELECTED" });
}

function fsmGet(changeId) {
  const run = fsmRuns.get(changeId);
  if (!run) throw new Error("Unknown change_id; select an environment first");
  return run;
}

function fsmAdvance(params) {
  const changeId = String(params.change_id || "").trim();
  if (!changeId) return fail("change_id is required");
  const run = fsmGet(changeId);
  const next = String(params.to_state || "").trim();
  if (next === "ROLLBACK") {
    run.state = "ROLLBACK";
    run.history.push("ROLLBACK");
    return ok({ ...run, rolled_back: true });
  }
  const currentIndex = FSM_ORDER.indexOf(run.state);
  const nextIndex = FSM_ORDER.indexOf(next);
  if (nextIndex < 0) return fail(`Unknown FSM state ${next}`);
  if (nextIndex !== currentIndex + 1) {
    return fail(`Illegal FSM transition ${run.state} -> ${next}. Next required state is ${FSM_ORDER[currentIndex + 1]}`);
  }
  if (next === "APPLY" && params.approved !== true) return fail("APPLY requires approved=true");
  run.state = next;
  run.history.push(next);
  return ok(run);
}

function wordpressChangePlan(params) {
  const scope = String(params.scope_root || "wp-content").replace(/\\/g, "/");
  return ok({
    status: "PLAN",
    environment_id: params.environment_id || selectedEnvironment.get("default") || null,
    mutation_hierarchy: [
      "existing plugin/theme/site-editor configuration",
      "child theme or site-specific plugin in the workspace",
      "scoped FTP publish of wp-content artifacts",
      "direct MySQL only when no safer WordPress API exists"
    ],
    allowed_remote_roots: ["wp-content/themes", "wp-content/plugins", "wp-content/mu-plugins", "wp-content/uploads"],
    blocked_without_high_risk: ["wp-admin", "wp-includes", "wp-config.php", "WordPress core"],
    workspace_scope: scope,
    verify: ["php lint when PHP is available", "HTTP smoke via cookie or Playwright", "no leaked secrets"]
  });
}

function phpConfigPlan(params) {
  return ok({
    status: "PLAN",
    environment_id: params.environment_id || selectedEnvironment.get("default") || null,
    panel_tool: "php-version",
    inspect: ["PHP version", "memory_limit", "max_execution_time", "upload_max_filesize", "extensions"],
    change_channel: "KingHost panel PHP manager via cookie or Playwright; do not invent undocumented APIs",
    verify: ["phpinfo or panel confirmation", "site HTTP 200", "fatal-log absence"]
  });
}

function mysqlPlan(params, mutation) {
  return ok({
    status: "PLAN",
    mutation,
    environment_id: params.environment_id || selectedEnvironment.get("default") || null,
    steps: mutation
      ? ["bind mysql credential_ref", "EXPLAIN/read-first", "dry-run", "approved mutation", "row-count verify", "rollback SQL"]
      : ["bind mysql credential_ref", "SHOW/SELECT/DESCRIBE/EXPLAIN only", "redact secrets in rows"],
    never: ["DROP DATABASE", "unscoped DELETE", "persist dumps with passwords"]
  });
}

function panelAuthPlan(params) {
  const method = String(params.method || "cookie").toLowerCase();
  if (!["cookie", "playwright", "browser"].includes(method)) return fail("method must be cookie|playwright|browser");
  return ok({
    status: "PLAN",
    method,
    allowed_hosts: ["king.host", "*.king.host", "*.kinghost.com.br"],
    cookie: {
      source: "external runtime cookie/cookie-jar file reference",
      open_via: "runtime-auth auth.session.open_cookie_file",
      never_persist: ["cookie values", "panel passwords", "FTP passwords shown in UI"]
    },
    playwright: {
      use: "browser MCP or Playwright with the same cookie session",
      goals: ["confirm account/site identity", "select environment/domain", "open PHP/MySQL/FTP tool pages", "verify post-deploy"],
      forbidden: ["copy passwords into chat, notebook or evidence"]
    },
    next: "After panel identity is confirmed, bind FTP/MySQL credentials from env_reference or runtime_memory"
  });
}

function backupPlan(params) {
  return ok({
    status: "PLAN",
    environment_id: params.environment_id || selectedEnvironment.get("default") || null,
    required: ["remote file snapshot or KingHost backup", "database dump when SQL changes", "rollback_ref"],
    ftp_snapshot: ["list scoped remote files", "hash contents", "store hashes in evidence without file bodies unless needed"]
  });
}

function verifySmokePlan(params) {
  const urls = Array.isArray(params.urls) ? params.urls : [String(params.url || "")].filter(Boolean);
  return ok({
    status: "PLAN",
    method: params.method || "cookie_or_playwright",
    urls,
    checks: ["HTTPS identity", "HTTP status", "no PHP fatal", "changed selector/text present", "desktop and mobile when layout changed"],
    pass_rule: "HTTP 200 alone is insufficient; confirm resulting WordPress/PHP state"
  });
}

function knowledgeSearch(params) {
  return ok({
    status: "PLAN",
    query: String(params.query || ""),
    source_registry: "aeos/knowledge/kinghost-control.sources.yaml",
    freshness_policy: "aeos/policies/kinghost-commerce-freshness.policy.md",
    official: ["https://king.host/", "https://king.host/wiki/", "https://king.host/blog/"]
  });
}

function deployWorkspacePlan(params) {
  return ok({
    status: "PLAN",
    fsm: FSM_ORDER,
    workspace_root: params.workspace_root || null,
    remote_root: params.remote_root || "wp-content",
    steps: [
      "select environment",
      "bind FTP and optional MySQL/wp-admin credentials",
      "panel auth via cookie or Playwright",
      "inventory remote scoped tree",
      "snapshot hashes",
      "diff workspace vs remote",
      "dry-run FTP STOR list",
      "backup/rollback_ref",
      "approved scoped upload",
      "smoke via cookie/Playwright",
      "close sessions"
    ],
    required_gates: ["approved=true", "change_id", "rollback_ref", "dry_run evidence"]
  });
}

async function openFtp(params) {
  const cred = getCredential(params.credential_ref, "ftp");
  const client = new FtpClient({ timeoutMs: Number(params.timeout_ms || 30000) });
  await client.connect(cred.host, cred.port);
  await client.login(cred.username, cred.secret);
  const remoteRoot = String(params.remote_root || "wp-content").replace(/\\/g, "/").replace(/^\/+|\/+$/g, "");
  const id = `ftp_${randomUUID()}`;
  ftpSessions.set(id, {
    id,
    client,
    credential_ref: cred.id,
    remoteRoot,
    host: cred.host,
    createdAt: now(),
    expiresAt: now() + DEFAULT_TTL_MS
  });
  return ok({
    session_ref: id,
    kind: "ftp",
    host: cred.host,
    port: cred.port,
    username: cred.username,
    remote_root: remoteRoot
  });
}

async function ftpList(params) {
  const session = getFtp(params.session_ref);
  const remotePath = remoteAllowed(session.remoteRoot, params.path || session.remoteRoot);
  const result = await session.client.list(remotePath);
  return ok({ path: remotePath, listing: result.listing.split(/\r?\n/).filter(Boolean).slice(0, 5000) });
}

async function ftpRead(params) {
  const session = getFtp(params.session_ref);
  const remotePath = remoteAllowed(session.remoteRoot, params.path);
  const result = await session.client.retrieve(remotePath, MAX_READ_BYTES);
  const encoding = params.encoding === "base64" ? "base64" : "utf8";
  return ok({
    path: remotePath,
    encoding,
    sha256: sha256(result.bytes),
    byte_length: result.bytes.length,
    content: encoding === "base64" ? result.bytes.toString("base64") : result.bytes.toString("utf8")
  });
}

async function ftpUpload(params) {
  const session = getFtp(params.session_ref);
  requireMutationGate(params);
  const highRisk = params.high_risk_approved === true;
  const remotePath = remoteAllowed(session.remoteRoot, params.remote_path, { highRisk });
  const workspaceRoot = resolve(String(params.workspace_root || process.cwd()));
  const localPath = resolveUnderRoot(workspaceRoot, params.local_path);
  if (!existsSync(localPath) || !statSync(localPath).isFile()) return fail("local_path is not a readable file under workspace_root");
  const bytes = readFileSync(localPath);
  if (bytes.length > MAX_READ_BYTES) return fail(`File exceeds ${MAX_READ_BYTES} bytes`);
  if (params.dry_run !== false) {
    return ok({
      dry_run: true,
      local_path: localPath,
      remote_path: remotePath,
      sha256: sha256(bytes),
      byte_length: bytes.length,
      change_id: params.change_id,
      rollback_ref: params.rollback_ref
    });
  }
  await session.client.store(remotePath, bytes);
  return ok({
    dry_run: false,
    remote_path: remotePath,
    sha256: sha256(bytes),
    byte_length: bytes.length,
    change_id: params.change_id,
    rollback_ref: params.rollback_ref
  });
}

async function ftpMkdir(params) {
  const session = getFtp(params.session_ref);
  requireMutationGate(params);
  const remotePath = remoteAllowed(session.remoteRoot, params.path, { highRisk: params.high_risk_approved === true });
  if (params.dry_run !== false) return ok({ dry_run: true, path: remotePath, change_id: params.change_id });
  await session.client.mkdir(remotePath);
  return ok({ dry_run: false, path: remotePath });
}

async function ftpDelete(params) {
  const session = getFtp(params.session_ref);
  requireMutationGate(params);
  if (params.high_risk_approved !== true) return fail("FTP delete requires high_risk_approved=true");
  const remotePath = remoteAllowed(session.remoteRoot, params.path, { highRisk: true });
  if (params.dry_run !== false) return ok({ dry_run: true, path: remotePath, change_id: params.change_id });
  await session.client.delete(remotePath);
  return ok({ dry_run: false, path: remotePath });
}

async function loadMysql() {
  const here = dirname(fileURLToPath(import.meta.url));
  const candidates = [
    join(here, "..", "kinghost-commerce-mcp", "node_modules", "mysql2", "promise.js"),
    join(process.cwd(), "kinghost-commerce-mcp", "node_modules", "mysql2", "promise.js")
  ];
  for (const candidate of candidates) {
    if (existsSync(candidate)) return import(pathToFileURL(candidate).href);
  }
  throw new Error("mysql2 is unavailable; run npm run aeos:kinghost:deps");
}

async function openMysql(params) {
  const cred = getCredential(params.credential_ref, "mysql");
  const mysql = await loadMysql();
  const db = await mysql.createConnection({
    host: cred.host,
    port: cred.port,
    user: cred.username,
    password: cred.secret,
    database: params.database || process.env[String(params.database_env || "")] || undefined,
    connectTimeout: 15000
  });
  const id = `mysql_${randomUUID()}`;
  mysqlSessions.set(id, { id, db, credential_ref: cred.id, createdAt: now(), expiresAt: now() + DEFAULT_TTL_MS });
  return ok({ session_ref: id, kind: "mysql", host: cred.host, port: cred.port, username: cred.username, database: params.database || null });
}

function getMysql(ref) {
  const session = mysqlSessions.get(ref);
  if (!session) throw new Error("Unknown or expired mysql session_ref");
  if (session.expiresAt <= now()) {
    session.db.end().catch(() => {});
    mysqlSessions.delete(ref);
    throw new Error("MySQL session expired");
  }
  session.expiresAt = now() + DEFAULT_TTL_MS;
  return session;
}

async function mysqlQuery(params, mutation) {
  const session = getMysql(params.session_ref);
  const sql = String(params.sql || "").trim();
  if (!sql) return fail("sql is required");
  const readonly = READONLY_SQL.test(sql) && !MUTATING_SQL.test(sql);
  const mutating = MUTATING_SQL.test(sql);
  if (!mutation && !readonly) return fail("Only SELECT/SHOW/DESCRIBE/EXPLAIN are allowed in read-only mode");
  if (mutation) {
    requireMutationGate(params);
    if (!mutating) return fail("Mutation tool requires a mutating SQL statement");
    if (HIGH_RISK_SQL.test(sql) && params.high_risk_approved !== true) {
      return fail("High-risk SQL requires high_risk_approved=true");
    }
    if (params.dry_run !== false) return ok({ dry_run: true, sql_sha256: sha256(sql), change_id: params.change_id });
  }
  const [rows, fields] = await session.db.execute(sql, Array.isArray(params.values) ? params.values : []);
  const normalized = Array.isArray(rows) ? rows.slice(0, 5000) : rows;
  return ok({
    rows: redactObject(normalized),
    row_count: Array.isArray(rows) ? rows.length : undefined,
    fields: fields?.map?.((field) => field.name) || [],
    truncated: Array.isArray(rows) && rows.length > 5000
  });
}

async function closeRef(params) {
  const ref = String(params.session_ref || params.credential_ref || "").trim();
  if (ftpSessions.has(ref)) {
    ftpSessions.get(ref).client.close();
    ftpSessions.delete(ref);
    return ok({ closed: true, kind: "ftp", session_ref: ref });
  }
  if (mysqlSessions.has(ref)) {
    await mysqlSessions.get(ref).db.end().catch(() => {});
    mysqlSessions.delete(ref);
    return ok({ closed: true, kind: "mysql", session_ref: ref });
  }
  if (credentials.has(ref)) {
    credentials.delete(ref);
    return ok({ closed: true, kind: "credential", credential_ref: ref });
  }
  return fail("Unknown session_ref or credential_ref");
}

async function dispatch(action, params = {}) {
  switch (action) {
    case "kinghost_control.health":
      return ok({
        adapter: "kinghost-control-mcp",
        credentials: credentials.size,
        ftp_sessions: ftpSessions.size,
        mysql_sessions: mysqlSessions.size,
        fsm_runs: fsmRuns.size,
        uptime_seconds: Math.round(process.uptime())
      });
    case "kinghost_control.environment.catalog":
      return ok({ environments: ENVIRONMENTS });
    case "kinghost_control.environment.select":
      return environmentSelect(params);
    case "kinghost_control.plugin.catalog":
      return ok({ tools: KINGHOST_TOOLS, note: "Catalog is the governed KingHost control-panel surface; undocumented private APIs are unsupported." });
    case "kinghost_control.credential.bind":
      return bindCredential(params);
    case "kinghost_control.credential.info":
      return ok(credentialMeta(getCredential(params.credential_ref)));
    case "kinghost_control.credential.close":
      return closeRef(params);
    case "kinghost_control.fsm.state":
      return ok(fsmGet(String(params.change_id || "")));
    case "kinghost_control.fsm.advance":
      return fsmAdvance(params);
    case "kinghost_control.wordpress.inventory_plan":
      return ok({
        status: "PLAN",
        collect: ["WordPress version", "active theme", "plugins", "php version", "scoped wp-content tree"],
        persist: ".aeos/wordpress/sites/<site-id>/beta-map.json via wordpress-expert",
        never_persist: ["passwords", "cookies", "nonces", "wp-config secrets"]
      });
    case "kinghost_control.wordpress.change_plan":
      return wordpressChangePlan(params);
    case "kinghost_control.php.config_plan":
      return phpConfigPlan(params);
    case "kinghost_control.mysql.plan_readonly":
      return mysqlPlan(params, false);
    case "kinghost_control.mysql.plan_mutation":
      return mysqlPlan(params, true);
    case "kinghost_control.mysql.session.open":
      return openMysql(params);
    case "kinghost_control.mysql.query_readonly":
      return mysqlQuery(params, false);
    case "kinghost_control.mysql.query_mutation":
      return mysqlQuery(params, true);
    case "kinghost_control.ftp.session.open":
      return openFtp(params);
    case "kinghost_control.ftp.list":
      return ftpList(params);
    case "kinghost_control.ftp.read":
      return ftpRead(params);
    case "kinghost_control.ftp.upload":
      return ftpUpload(params);
    case "kinghost_control.ftp.mkdir":
      return ftpMkdir(params);
    case "kinghost_control.ftp.delete":
      return ftpDelete(params);
    case "kinghost_control.session.close":
      return closeRef(params);
    case "kinghost_control.panel.auth_plan":
      return panelAuthPlan(params);
    case "kinghost_control.backup.plan":
      return backupPlan(params);
    case "kinghost_control.rollback.plan":
      return ok({ status: "PLAN", restore: ["re-upload snapshot files", "restore SQL if mutated", "purge cache", "repeat smoke"], change_id: params.change_id || null });
    case "kinghost_control.verify.smoke_plan":
      return verifySmokePlan(params);
    case "kinghost_control.deploy.workspace_to_production":
      return deployWorkspacePlan(params);
    case "kinghost_control.knowledge_search":
      return knowledgeSearch(params);
    default:
      return fail(`Unknown action: ${action}`, "UNKNOWN_ACTION");
  }
}

async function handleEnvelope(envelope) {
  const requestId = envelope?.request_id || randomUUID();
  try {
    const result = await dispatch(envelope?.action, envelope?.params || {});
    return { request_id: requestId, ...result };
  } catch (error) {
    return {
      request_id: requestId,
      success: false,
      error: redact(error instanceof Error ? error.message : String(error)),
      code: "ERROR"
    };
  }
}

export { dispatch, handleEnvelope, FSM_ORDER };

const isMain = process.argv[1]
  ? resolve(process.argv[1]).toLowerCase() === fileURLToPath(import.meta.url).toLowerCase()
  : false;

if (isMain && process.argv.includes("--self-test")) {
  const health = await handleEnvelope({ request_id: "self-test", action: "kinghost_control.health", params: {} });
  const catalog = await handleEnvelope({ request_id: "self-env", action: "kinghost_control.environment.catalog", params: {} });
  console.log(JSON.stringify({ health, catalog_ok: catalog.success === true }));
  process.exit(health.success && catalog.success ? 0 : 1);
}

if (isMain) {
  const rl = createInterface({ input: process.stdin, crlfDelay: Infinity });
  rl.on("line", async (line) => {
    const trimmed = line.trim();
    if (!trimmed) return;
    let envelope;
    try { envelope = JSON.parse(trimmed); } catch {
      process.stdout.write(`${JSON.stringify({ success: false, error: "Invalid JSON envelope", code: "ERROR" })}\n`);
      return;
    }
    const result = await handleEnvelope(envelope);
    process.stdout.write(`${JSON.stringify(redactObject(result))}\n`);
  });
}
