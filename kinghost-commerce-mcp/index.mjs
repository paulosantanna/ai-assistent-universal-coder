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
const READONLY_SHELL = new Set(["pwd", "ls", "find", "stat", "du", "df", "cat", "head", "tail", "grep", "wc", "file", "uname", "node", "php"]);

function now() { return Date.now(); }
function sha256(value) { return createHash("sha256").update(String(value)).digest("hex"); }
function ok(data = {}) { return { success: true, data }; }
function fail(error, code = "BLOCKED") { return { success: false, error, code }; }
function redactMessage(message) {
  return String(message ?? "").replace(/(password|passwd|token|secret|private[_-]?key)\s*[=:]\s*\S+/gi, "$1=***REDACTED***");
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

async function writeRemote(params) {
  requireMutationGate(params);
  const s = getSession(params.session_ref, "ssh");
  const path = String(params.path || "");
  const content = params.encoding === "base64" ? Buffer.from(String(params.content || ""), "base64") : Buffer.from(String(params.content || ""), "utf8");
  if (!path) return fail("path is required");
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
  if (params.dry_run === true) return ok({ dry_run: true, from, to, change_id: params.change_id });
  await new Promise((resolve, reject) => s.sftp.rename(from, to, err => err ? reject(err) : resolve()));
  return ok({ from, to, renamed: true, change_id: params.change_id });
}

async function deleteRemote(params) {
  requireMutationGate(params);
  const s = getSession(params.session_ref, "ssh");
  const path = String(params.path || "");
  if (!path || path === "/" || path === ".") return fail("unsafe delete path");
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
