import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { dirname, join, relative, resolve, sep } from "node:path";

const DEFAULT_SKIP = new Set([".git", ".svn", "node_modules", ".aeos", "error_log"]);
const SECRET_FILES = new Set(["wp-config.php", "wp-config-sample.php"]);

export function parseFtpListing(text) {
  const entries = [];
  for (const raw of String(text || "").split(/\r?\n/)) {
    const line = raw.trimEnd();
    if (!line || /^total\s+\d+/i.test(line)) continue;
    if (line.startsWith("type=")) {
      const typeMatch = /(?:^|;)type=([^;]+)/i.exec(line);
      const name = line.split(";").pop()?.replace(/^\s+/, "") || "";
      if (!name || name === "." || name === "..") continue;
      const sizeMatch = /(?:^|;)size=(\d+)/i.exec(line);
      entries.push({
        name,
        type: String(typeMatch?.[1] || "").toLowerCase() === "dir" ? "dir" : "file",
        size: Number(sizeMatch?.[1] || 0)
      });
      continue;
    }
    const parts = line.trim().split(/\s+/);
    if (parts.length >= 9 && /^[bcdlps-]/.test(parts[0])) {
      const name = parts.slice(8).join(" ");
      if (!name || name === "." || name === "..") continue;
      entries.push({
        name,
        type: parts[0].startsWith("d") || parts[0].startsWith("l") && name.endsWith("/") ? "dir" : parts[0].startsWith("d") ? "dir" : "file",
        size: Number(parts[4] || 0)
      });
      if (parts[0].startsWith("d")) entries[entries.length - 1].type = "dir";
      continue;
    }
    if (parts.length === 1 && parts[0] !== "." && parts[0] !== "..") {
      entries.push({ name: parts[0], type: parts[0].endsWith("/") ? "dir" : "file", size: 0 });
    }
  }
  return entries;
}

function posixJoin(root, name) {
  const base = String(root || "").replace(/\\/g, "/").replace(/\/+$/, "");
  const leaf = String(name || "").replace(/\\/g, "/").replace(/^\/+/, "");
  return base ? `${base}/${leaf}` : leaf;
}

function shouldSkip(name, { includeUploads = false, skipWpConfig = true } = {}) {
  if (DEFAULT_SKIP.has(name)) return true;
  if (skipWpConfig && SECRET_FILES.has(name)) return true;
  if (!includeUploads && name === "uploads") return true;
  return false;
}

export async function listTree(client, remoteRoot, options = {}) {
  const maxEntries = Math.min(Math.max(Number(options.max_entries || 2000), 1), 10000);
  const includeUploads = options.include_uploads === true;
  const skipWpConfig = options.skip_wp_config !== false;
  const files = [];
  const dirs = [];
  const skipped = [];
  const errors = [];
  const queue = [String(remoteRoot || ".").replace(/\\/g, "/").replace(/\/+$/, "") || "."];

  while (queue.length && files.length + dirs.length < maxEntries) {
    const current = queue.shift();
    let listing;
    try {
      const result = await client.list(current);
      listing = parseFtpListing(result.listing);
    } catch (error) {
      errors.push({ path: current, error: error instanceof Error ? error.message : String(error) });
      continue;
    }
    dirs.push(current);
    for (const entry of listing) {
      if (files.length + dirs.length >= maxEntries) break;
      if (shouldSkip(entry.name, { includeUploads, skipWpConfig })) {
        skipped.push({ path: posixJoin(current, entry.name), reason: entry.name });
        continue;
      }
      const path = posixJoin(current, entry.name);
      if (entry.type === "dir") queue.push(path);
      else files.push({ path, size: entry.size, type: "file" });
    }
  }

  return {
    remote_root: remoteRoot,
    dirs: dirs.slice(0, maxEntries),
    files: files.slice(0, maxEntries),
    skipped,
    errors,
    truncated: queue.length > 0 || files.length + dirs.length >= maxEntries
  };
}

function resolveLocal(workspaceRoot, localPath) {
  const base = resolve(workspaceRoot);
  const target = resolve(base, localPath || ".");
  const rel = relative(base, target);
  if (rel.startsWith("..") || rel.startsWith(`..${sep}`)) throw new Error("Path escapes the approved root");
  return target;
}

export async function downloadTree(client, { remoteRoot, workspaceRoot, localDir, dryRun = true, includeUploads = false, skipWpConfig = true, maxFiles = 500, maxBytes = 50_000_000 } = {}) {
  const inventory = await listTree(client, remoteRoot, { include_uploads: includeUploads, skip_wp_config: skipWpConfig, max_entries: maxFiles * 2 });
  const selected = inventory.files.slice(0, maxFiles);
  const localRoot = resolveLocal(workspaceRoot, localDir || ".");
  const planned = [];
  let bytes = 0;
  for (const file of selected) {
    if (bytes >= maxBytes) break;
    const rel = String(file.path).replace(new RegExp(`^${String(remoteRoot).replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}/?`), "");
    planned.push({ remote_path: file.path, local_rel: rel, size: file.size });
    bytes += Number(file.size || 0);
  }
  if (dryRun !== false) {
    return {
      dry_run: true,
      local_root: localRoot,
      remote_root: remoteRoot,
      files: planned,
      skipped: inventory.skipped,
      errors: inventory.errors,
      truncated: inventory.truncated || planned.length < inventory.files.length
    };
  }
  mkdirSync(localRoot, { recursive: true });
  const written = [];
  for (const item of planned) {
    const result = await client.retrieve(item.remote_path, Math.min(maxBytes, 2_000_000));
    const dest = resolveLocal(localRoot, item.local_rel);
    mkdirSync(dirname(dest), { recursive: true });
    writeFileSync(dest, result.bytes);
    written.push({
      remote_path: item.remote_path,
      local_path: dest,
      sha256: createHash("sha256").update(result.bytes).digest("hex"),
      byte_length: result.bytes.length
    });
  }
  return {
    dry_run: false,
    local_root: localRoot,
    remote_root: remoteRoot,
    files: written,
    skipped: inventory.skipped,
    errors: inventory.errors
  };
}

function walkLocal(root, { includeUploads = false, skipWpConfig = true } = {}) {
  const files = [];
  function walk(dir, rel) {
    if (!existsSync(dir)) return;
    for (const ent of readdirSync(dir, { withFileTypes: true })) {
      if (shouldSkip(ent.name, { includeUploads, skipWpConfig })) continue;
      const relPath = rel ? `${rel}/${ent.name}` : ent.name;
      const abs = join(dir, ent.name);
      if (ent.isDirectory()) walk(abs, relPath);
      else if (ent.isFile()) files.push({ relPath, abs, size: statSync(abs).size });
    }
  }
  walk(root, "");
  return files;
}

export async function uploadTree(client, { remoteRoot, workspaceRoot, localDir, dryRun = true, includeUploads = false, skipWpConfig = true, maxFiles = 500, maxBytes = 50_000_000 } = {}) {
  const localRoot = resolveLocal(workspaceRoot, localDir || ".");
  if (!existsSync(localRoot)) throw new Error("local tree does not exist under workspace_root");
  const files = walkLocal(localRoot, { includeUploads, skipWpConfig }).slice(0, maxFiles);
  const planned = [];
  let bytes = 0;
  for (const file of files) {
    if (bytes + file.size > maxBytes) break;
    const remotePath = posixJoin(remoteRoot, file.relPath);
    planned.push({
      local_path: file.abs,
      remote_path: remotePath,
      sha256: createHash("sha256").update(readFileSync(file.abs)).digest("hex"),
      byte_length: file.size
    });
    bytes += file.size;
  }
  if (dryRun !== false) {
    return { dry_run: true, local_root: localRoot, remote_root: remoteRoot, files: planned };
  }
  const dirs = new Set();
  for (const item of planned) {
    const dir = item.remote_path.replace(/\/[^/]+$/, "");
    if (dir && dir !== remoteRoot) dirs.add(dir);
  }
  for (const dir of [...dirs].sort()) {
    try { await client.mkdir(dir); } catch { /* directory may already exist */ }
  }
  const written = [];
  for (const item of planned) {
    const bytesToStore = readFileSync(item.local_path);
    await client.store(item.remote_path, bytesToStore);
    written.push({ remote_path: item.remote_path, sha256: item.sha256, byte_length: item.byte_length });
  }
  return { dry_run: false, local_root: localRoot, remote_root: remoteRoot, files: written };
}

export { SECRET_FILES };
