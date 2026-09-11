import { createInterface } from "node:readline";
import { randomUUID, createHash } from "node:crypto";
import { Client as SSHClient } from "ssh2";
import mysql from "mysql2/promise";
import pg from "pg";

const { Client: PgClient } = pg;
const sessions = new Map();
const MAX_READ_BYTES = 2_000_000;
const MAX_LIST_ENTRIES = 5000;
const MAX_QUERY_ROWS = 5000;
const DEFAULT_TTL_MS = 15 * 60 * 1000;

const READONLY_SQL = /^\s*(select|show|describe|desc|explain|with\b[\s\S]*select)\b/i;
const MUTATING_SQL = /\b(insert|update|delete|replace|merge|truncate|drop|alter|create|grant|revoke|rename|call|load\s+data|lock\s+tables|unlock\s+tables)\b/i;
const HIGH_RISK_SQL = /\b(truncate|drop|grant|revoke|load\s+data|lock\s+tables|unlock\s+tables)\b/i;
const READONLY_SHELL = new Set(["pwd", "ls", "find", "stat", "du", "df", "cat", "head", "tail", "grep", "wc", "file", "uname", "node", "php"]);

function now() { return Date.now(); }
function sha256(value) { return createHash("sha256").update(String(value)).digest("hex"); }
function ok(data = {}) { return { success: true, data }; }
function fail(error, code = "BLOCKED") { return { success: false, error, code }; }
function redactMessage(message) {
  return String(message ?? "").replace(/(password|passwd|token|secret|private[_-]?key)\s*[=:]\s*\S+/gi, "$1=***REDACTED***");
}
function asList(value) { return Array.isArray(value) ? value.filter(Boolean).map(String) : []; }
function requireNoCredentialDiscovery(params) {
  const mode = String(params?.access_mode || params?.mode || "").toLowerCase();
  if (/(discover|extract|harvest|cookie|session_dump|credential_scan)/.test(mode)) {
    throw new Error("Credential discovery/extraction is forbidden; use ephemeral runtime credentials or approved secret references");
  }
}

function ensureAuthorized(params) {
  if (params?.authorized !== true) throw new Error("authorized=true is required for remote connection operations");
}

function sessionMeta(session) {
  return {
    session_ref: session.id,
    kind: session.kind,
    host: session.host,
    port: session.port,
    username: session.username,
    created_at: new Date(session.createdAt).toISOString(),
    expires_at: new Date(session.expiresAt).toISOString(),
    target_fingerprint: session.targetFingerprint,
    capabilities: session.capabilities
  };
}

function getSession(ref, kind) {
  const session = sessions.get(ref);
  if (!session) throw new Error("Unknown or expired session_ref");
  if (session.expiresAt <= now()) {
    closeSession(session).catch(() => {});
    sessions.delete(ref);
    throw new Error("Session expired");
  }
  if (kind && session.kind !== kind) throw new Error(`Session kind mismatch: expected ${kind}, got ${session.kind}`);
  session.expiresAt = now() + DEFAULT_TTL_MS;
  return session;
}

async function closeSession(session) {
  try { session.sftp?.end?.(); } catch {}
  try { session.ssh?.end?.(); } catch {}
  try { await session.db?.end?.(); } catch {}
}

async function openSsh(params) {
  ensureAuthorized(params);
  const host = String(params.host || "").trim();
  const username = String(params.username || "").trim();
  const password = params.password;
  const privateKey = params.private_key;
  const port = Number(params.port || 22);
  if (!host || !username) return fail("host and username are required");
  if (!password && !privateKey) return fail("password or private_key is required as ephemeral runtime input");

  const ssh = new SSHClient();
  const id = randomUUID();
  const hostKeyHash = [];
  await new Promise((resolve, reject) => {
    ssh.on("ready", resolve);
    ssh.on("error", reject);
    ssh.connect({
      host,
      port,
      username,
      password: password ? String(password) : undefined,
      privateKey: privateKey ? String(privateKey) : undefined,
      readyTimeout: Number(params.timeout_ms || 15000),
      keepaliveInterval: 10000,
      keepaliveCountMax: 3,
      hostVerifier: (key) => {
        const digest = sha256(key);
        hostKeyHash.push(digest);
        if (params.expected_host_fingerprint) return digest === String(params.expected_host_fingerprint);
        return params.allow_first_use === true;
      }
    });
  });

  const sftp = await new Promise((resolve, reject) => ssh.sftp((err, handle) => err ? reject(err) : resolve(handle)));
  const session = {
    id, kind: "ssh", host, port, username, ssh, sftp,
    createdAt: now(), expiresAt: now() + DEFAULT_TTL_MS,
    targetFingerprint: hostKeyHash[0] || "unknown",
    capabilities: ["sftp.list", "sftp.read", "sftp.write", "sftp.mkdir", "sftp.rename", "sftp.delete", "ssh.exec_readonly"]
  };
  sessions.set(id, session);
  return ok(sessionMeta(session));
}

async function openMysql(params) {
  ensureAuthorized(params);
  const host = String(params.host || "").trim();
  const username = String(params.username || "").trim();
  const password = params.password;
  const database = String(params.database || "").trim();
  const port = Number(params.port || 3306);
  if (!host || !username || !database || password === undefined) return fail("host, username, password and database are required");
  const db = await mysql.createConnection({ host, port, user: username, password: String(password), database, ssl: params.ssl === false ? undefined : { rejectUnauthorized: params.reject_unauthorized !== false }, connectTimeout: Number(params.timeout_ms || 15000) });
  const id = randomUUID();
  const session = { id, kind: "mysql", host, port, username, db, createdAt: now(), expiresAt: now() + DEFAULT_TTL_MS, targetFingerprint: sha256(`${host}:${port}/${database}`), capabilities: ["db.query_readonly", "db.query_mutation"] };
  sessions.set(id, session);
  return ok(sessionMeta(session));
}

async function openPostgres(params) {
  ensureAuthorized(params);
  const host = String(params.host || "").trim();
  const username = String(params.username || "").trim();
  const password = params.password;
  const database = String(params.database || "").trim();
  const port = Number(params.port || 5432);
  if (!host || !username || !database || password === undefined) return fail("host, username, password and database are required");
  const db = new PgClient({ host, port, user: username, password: String(password), database, ssl: params.ssl === false ? false : { rejectUnauthorized: params.reject_unauthorized !== false }, connectionTimeoutMillis: Number(params.timeout_ms || 15000) });
  await db.connect();
  const id = randomUUID();
  const session = { id, kind: "postgres", host, port, username, db, createdAt: now(), expiresAt: now() + DEFAULT_TTL_MS, targetFingerprint: sha256(`${host}:${port}/${database}`), capabilities: ["db.query_readonly", "db.query_mutation"] };
  sessions.set(id, session);
  return ok(sessionMeta(session));
}

async function listRemote(params) {
  const s = getSession(params.session_ref, "ssh");
  const path = String(params.path || ".");
  const entries = await new Promise((resolve, reject) => s.sftp.readdir(path, (err, list) => err ? reject(err) : resolve(list)));
  return ok({ path, entries: entries.slice(0, MAX_LIST_ENTRIES).map(e => ({ name: e.filename, size: e.attrs?.size ?? 0, mode: e.attrs?.mode ?? 0, mtime: e.attrs?.mtime ?? 0 })) });
}

async function readRemote(params) {
  const s = getSession(params.session_ref, "ssh");
  const path = String(params.path || "");
  if (!path) return fail("path is required");
  const chunks = [];
  let size = 0;
  await new Promise((resolve, reject) => {
    const stream = s.sftp.createReadStream(path, { start: 0, end: Number(params.max_bytes || MAX_READ_BYTES) - 1 });
    stream.on("data", chunk => { size += chunk.length; chunks.push(chunk); });
    stream.on("error", reject);
    stream.on("end", resolve);
  });
  const content = Buffer.concat(chunks).toString(params.encoding === "base64" ? "base64" : "utf8");
  return ok({ path, size, content, sha256: sha256(content), truncated: size >= Number(params.max_bytes || MAX_READ_BYTES) });
}

function requireMutationGate(params) {
  if (params.approved !== true) throw new Error("approved=true required for remote mutation");
  if (!params.change_id) throw new Error("change_id required for remote mutation evidence");
  if (!params.rollback_ref && params.operation !== "mkdir") throw new Error("rollback_ref required for remote mutation");
}

function requireScopedPath(params, path) {
  const scopeRoot = String(params.scope_root || params.remote_scope_root || "").trim();
  if (!scopeRoot) return;
  const normalizedRoot = scopeRoot.endsWith("/") ? scopeRoot : `${scopeRoot}/`;
  if (!(path === scopeRoot || path.startsWith(normalizedRoot))) {
    throw new Error("remote path is outside the approved scope_root");
  }
}

async function writeRemote(params) {
  requireMutationGate(params);
  const s = getSession(params.session_ref, "ssh");
  const path = String(params.path || "");
  const content = params.encoding === "base64" ? Buffer.from(String(params.content || ""), "base64") : Buffer.from(String(params.content || ""), "utf8");
  if (!path) return fail("path is required");
  requireScopedPath(params, path);
  if (params.dry_run === true) return ok({ dry_run: true, path, bytes: content.length, sha256: sha256(content), change_id: params.change_id });
  await new Promise((resolve, reject) => {
    const stream = s.sftp.createWriteStream(path, { flags: params.append === true ? "a" : "w", mode: params.mode || 0o640 });
    stream.on("error", reject);
    stream.on("close", resolve);
    stream.end(content);
  });
  return ok({ path, bytes: content.length, sha256: sha256(content), change_id: params.change_id });
}

async function mkdirRemote(params) {
  requireMutationGate({ ...params, operation: "mkdir" });
  const s = getSession(params.session_ref, "ssh");
  const path = String(params.path || "");
  requireScopedPath(params, path);
  if (params.dry_run === true) return ok({ dry_run: true, path, change_id: params.change_id });
  await new Promise((resolve, reject) => s.sftp.mkdir(path, { mode: params.mode || 0o750 }, err => err ? reject(err) : resolve()));
  return ok({ path, created: true, change_id: params.change_id });
}

async function renameRemote(params) {
  requireMutationGate(params);
  const s = getSession(params.session_ref, "ssh");
  const from = String(params.from || "");
  const to = String(params.to || "");
  if (!from || !to) return fail("from and to are required");
  requireScopedPath(params, from);
  requireScopedPath(params, to);
  if (params.dry_run === true) return ok({ dry_run: true, from, to, change_id: params.change_id });
  await new Promise((resolve, reject) => s.sftp.rename(from, to, err => err ? reject(err) : resolve()));
  return ok({ from, to, renamed: true, change_id: params.change_id });
}

async function deleteRemote(params) {
  requireMutationGate(params);
  const s = getSession(params.session_ref, "ssh");
  const path = String(params.path || "");
  if (!path || path === "/" || path === ".") return fail("unsafe delete path");
  requireScopedPath(params, path);
  if (params.dry_run === true) return ok({ dry_run: true, path, change_id: params.change_id });
  await new Promise((resolve, reject) => s.sftp.unlink(path, err => err ? reject(err) : resolve()));
  return ok({ path, deleted: true, change_id: params.change_id });
}

async function execReadonly(params) {
  const s = getSession(params.session_ref, "ssh");
  const command = String(params.command || "").trim();
  if (!command) return fail("command is required");
  if (/[;&|`$><\\]/.test(command)) return fail("shell metacharacters are blocked");
  const argv0 = command.split(/\s+/)[0];
  if (!READONLY_SHELL.has(argv0)) return fail(`command '${argv0}' is not allowlisted`);
  const output = await new Promise((resolve, reject) => {
    s.ssh.exec(command, (err, stream) => {
      if (err) return reject(err);
      let stdout = "", stderr = "";
      stream.on("data", d => { if (stdout.length < MAX_READ_BYTES) stdout += d.toString(); });
      stream.stderr.on("data", d => { if (stderr.length < 200000) stderr += d.toString(); });
      stream.on("close", code => resolve({ code, stdout, stderr }));
    });
  });
  return ok(output);
}

function classifySql(sql) {
  const clean = String(sql || "").trim();
  return { readonly: READONLY_SQL.test(clean) && !MUTATING_SQL.test(clean), mutating: MUTATING_SQL.test(clean) };
}

async function queryDb(params, mutation) {
  const s = getSession(params.session_ref);
  if (!['mysql','postgres'].includes(s.kind)) return fail("database session required");
  const sql = String(params.sql || "");
  const classification = classifySql(sql);
  if (!mutation && !classification.readonly) return fail("Only SELECT/SHOW/DESCRIBE/EXPLAIN queries are allowed in read-only mode");
  if (mutation) {
    requireMutationGate(params);
    if (!classification.mutating) return fail("Mutation tool requires a mutating SQL statement");
    if (HIGH_RISK_SQL.test(sql) && params.high_risk_approved !== true) return fail("High-risk SQL requires high_risk_approved=true in addition to the normal mutation gate");
    if (params.dry_run !== false) return ok({ dry_run: true, classification, sql_sha256: sha256(sql), change_id: params.change_id });
  }
  if (s.kind === "mysql") {
    const [rows, fields] = await s.db.execute(sql, Array.isArray(params.values) ? params.values : []);
    const normalized = Array.isArray(rows) ? rows.slice(0, MAX_QUERY_ROWS) : rows;
    return ok({ rows: normalized, row_count: Array.isArray(rows) ? rows.length : undefined, fields: fields?.map?.(f => f.name) || [], truncated: Array.isArray(rows) && rows.length > MAX_QUERY_ROWS });
  }
  const result = await s.db.query(sql, Array.isArray(params.values) ? params.values : []);
  return ok({ rows: result.rows.slice(0, MAX_QUERY_ROWS), row_count: result.rowCount, fields: result.fields?.map(f => f.name) || [], truncated: result.rows.length > MAX_QUERY_ROWS });
}

function accessRequestPlan(params) {
  requireNoCredentialDiscovery(params);
  return ok({
    status: "PLAN",
    target: String(params.target || ""),
    supported_access_methods: [
      "ephemeral username/password supplied at execution time",
      "approved secret reference resolved outside source control",
      "SSH private key reference from an approved secret provider",
      "short-lived official token/session when KingHost supports it"
    ],
    forbidden_access_methods: [
      "cookie/session extraction",
      "credential discovery or scraping",
      "password/token persistence in Git, evidence, memory or logs",
      "host-key or TLS validation bypass"
    ],
    required_evidence: ["operator authorization", "target host/account", "protocol", "scope_root", "rollback path for mutations"],
    next_actions: ["open an ephemeral session", "inspect capabilities", "return only an opaque session_ref"]
  });
}

function adminSuperPlan(params) {
  requireNoCredentialDiscovery(params);
  const objectives = asList(params.objectives);
  return ok({
    status: "PLAN",
    target: String(params.target || ""),
    objectives,
    phases: [
      "BRIEFING: prove authorization, scope and mutation risk",
      "RECON: inventory plan, domains, SSL, runtimes, databases, files, logs and WordPress/CMS state",
      "PLAN: produce bounded change-set, backups, preflight checks and rollback",
      "EXECUTE: run only approved MCP actions with dry-run evidence first",
      "VERIFY: HTTP health, logs, database checks, assets, checkout/login flows and performance budget",
      "DEBRIEF: redacted evidence, session close, residual risks and follow-up"
    ],
    capabilities: [
      "SFTP file read/write in approved scope",
      "read-only SSH diagnostics",
      "MySQL/PostgreSQL read-only query and gated mutation",
      "deployment/database/DNS/performance planning",
      "CDC workspace change planning and verification"
    ],
    blocked: ["credential extraction", "unrestricted shell", "unscoped deletion", "DNS/database destructive mutation without high-risk approval"]
  });
}

function cdcWorkspacePlan(params) {
  return ok({
    status: "PLAN",
    mode: "change-diff-control",
    target: String(params.target || ""),
    workflow: [
      "capture remote inventory hashes for selected files/database objects",
      "compare workspace artifact hashes against remote evidence",
      "generate a bounded diff/change-set",
      "dry-run write/query operations",
      "apply only approved scoped mutations",
      "verify post-state hashes, HTTP behavior and rollback viability"
    ],
    required_inputs: ["session_ref", "scope_root", "change_id", "rollback_ref", "approved artifact paths"],
    outputs: ["pre_state", "diff", "dry_run_result", "post_state", "rollback_evidence"]
  });
}

function knowledgeSearch(params) {
  return ok({
    status: "PLAN",
    query: String(params.query || ""),
    source_registry: "aeos/knowledge/kinghost-commerce.sources.yaml",
    freshness_policy: "aeos/policies/kinghost-commerce-freshness.policy.md",
    note: "Use official KingHost/provider documentation before material decisions; this adapter does not fabricate undocumented APIs."
  });
}

function inspectEnvironmentPlan(params) {
  return ok({
    status: "PLAN",
    target: String(params.target || ""),
    checks: ["hosting plan", "domains", "DNS", "SSL", "PHP/Node/runtime versions", "databases", "disk usage", "logs", "CMS/plugins/themes", "backup posture"],
    read_only_actions: ["kinghost.fs.list", "kinghost.fs.read", "kinghost.ssh.exec_readonly", "kinghost.db.query_readonly"],
    evidence_required: true
  });
}

function namedPlan(name, params, steps) {
  return ok({
    status: "PLAN",
    plan_type: name,
    target: String(params.target || params.site || ""),
    steps,
    approval_required_for_mutation: true,
    dry_run_required: true,
    rollback_required: true
  });
}

async function dispatch(action, params = {}) {
  switch (action) {
    case "kinghost.session.open_ssh": return openSsh(params);
    case "kinghost.session.open_mysql": return openMysql(params);
    case "kinghost.session.open_postgres": return openPostgres(params);
    case "kinghost.session.info": return ok(sessionMeta(getSession(params.session_ref)));
    case "kinghost.session.close": {
      const s = getSession(params.session_ref);
      await closeSession(s); sessions.delete(s.id); return ok({ session_ref: s.id, closed: true });
    }
    case "kinghost.fs.list": return listRemote(params);
    case "kinghost.fs.read": return readRemote(params);
    case "kinghost.fs.write": return writeRemote(params);
    case "kinghost.fs.mkdir": return mkdirRemote(params);
    case "kinghost.fs.rename": return renameRemote(params);
    case "kinghost.fs.delete": return deleteRemote(params);
    case "kinghost.ssh.exec_readonly": return execReadonly(params);
    case "kinghost.db.query_readonly": return queryDb(params, false);
    case "kinghost.db.query_mutation": return queryDb(params, true);
    case "kinghost.access.request_plan": return accessRequestPlan(params);
    case "kinghost.admin.super_plan": return adminSuperPlan(params);
    case "kinghost.cdc.workspace_plan": return cdcWorkspacePlan(params);
    case "kinghost.knowledge_search": return knowledgeSearch(params);
    case "kinghost.inspect_environment": return inspectEnvironmentPlan(params);
    case "kinghost.performance_audit": return namedPlan("kinghost.performance_audit", params, ["capture baseline", "inspect logs/resources", "analyze cache/assets/database", "define budgets", "verify after change"]);
    case "kinghost.deploy_plan": return namedPlan("kinghost.deploy_plan", params, ["identify publish method", "snapshot remote state", "prepare diff", "dry-run", "deploy approved changes", "health check", "rollback on failure"]);
    case "kinghost.database_plan": return namedPlan("kinghost.database_plan", params, ["inventory schema", "run read-only diagnostics", "EXPLAIN first", "prepare reversible SQL", "dry-run", "apply only approved mutation"]);
    case "kinghost.dns_plan": return namedPlan("kinghost.dns_plan", params, ["inventory records", "plan TTL window", "prepare exact record changes", "verify propagation", "rollback record set"]);
    case "commerce.catalog_plan": return namedPlan("commerce.catalog_plan", params, ["normalize products/SKUs", "map categories", "validate prices", "plan import/update", "verify catalog"]);
    case "commerce.channel_mapping": return namedPlan("commerce.channel_mapping", params, ["map canonical catalog", "verify provider contract", "define payload transforms", "plan reconciliation"]);
    case "commerce.price_sync_plan": return namedPlan("commerce.price_sync_plan", params, ["calculate fees/floors/margins", "prepare channel prices", "dry-run sync", "verify deltas"]);
    case "commerce.logistics_plan": return namedPlan("commerce.logistics_plan", params, ["map stock source", "define SLA/shipping rules", "plan provider handoff", "verify fulfillment states"]);
    case "web.modernization_plan": return namedPlan("web.modernization_plan", params, ["inventory frontend/backend stack", "define safe UI changes", "prepare diff", "performance/accessibility checks", "rollback"]);
    case "web.performance_budget": return namedPlan("web.performance_budget", params, ["set Core Web Vitals targets", "set backend/query budgets", "set asset budgets", "define regression gates"]);
    case "kinghost.health": return ok({ adapter: "kinghost-commerce-mcp", sessions: sessions.size, uptime_seconds: Math.round(process.uptime()) });
    default: return fail(`Unknown action: ${action}`, "UNKNOWN_ACTION");
  }
}

async function handleEnvelope(envelope) {
  const requestId = envelope?.request_id || randomUUID();
  try {
    const result = await dispatch(envelope?.action, envelope?.params || {});
    return { request_id: requestId, ...result };
  } catch (error) {
    return { request_id: requestId, success: false, error: redactMessage(error instanceof Error ? error.message : String(error)), code: "ERROR" };
  }
}

if (process.argv.includes("--self-test")) {
  console.log(JSON.stringify(await handleEnvelope({ request_id: "self-test", action: "kinghost.health", params: {} })));
  process.exit(0);
}

const rl = createInterface({ input: process.stdin, crlfDelay: Infinity });
rl.on("line", async line => {
  if (!line.trim()) return;
  try {
    const envelope = JSON.parse(line);
    const response = await handleEnvelope(envelope);
    process.stdout.write(JSON.stringify(response) + "\n");
  } catch (error) {
    process.stdout.write(JSON.stringify({ request_id: null, success: false, error: "Invalid JSON request", code: "BAD_REQUEST" }) + "\n");
  }
});

process.on("SIGTERM", async () => {
  for (const s of sessions.values()) await closeSession(s).catch(() => {});
  process.exit(0);
});