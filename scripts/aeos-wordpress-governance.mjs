#!/usr/bin/env node
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, renameSync, writeFileSync } from "node:fs";
import { isIP } from "node:net";
import { join, resolve } from "node:path";

export const WORDPRESS_KNOWLEDGE_CATALOG = Object.freeze([
  { id: "wp-rest", authority: "normative", kind: "official", url: "https://developer.wordpress.org/rest-api/", topics: ["REST API", "authentication", "discovery", "routes"] },
  { id: "wp-rest-reference", authority: "normative", kind: "official", url: "https://developer.wordpress.org/rest-api/reference/", topics: ["posts", "pages", "media", "settings", "themes", "plugins", "templates", "global styles"] },
  { id: "wp-plugins", authority: "normative", kind: "official", url: "https://developer.wordpress.org/plugins/", topics: ["plugin development", "hooks", "security", "settings", "HTTP API"] },
  { id: "wp-themes", authority: "normative", kind: "official", url: "https://developer.wordpress.org/themes/", topics: ["themes", "templates", "theme.json", "assets", "accessibility"] },
  { id: "wp-block-editor", authority: "normative", kind: "official", url: "https://developer.wordpress.org/block-editor/", topics: ["Gutenberg", "blocks", "packages", "data", "site editor"] },
  { id: "wp-common-apis", authority: "normative", kind: "official", url: "https://developer.wordpress.org/apis/", topics: ["HTTP", "filesystem", "metadata", "options", "transients", "security"] },
  { id: "wp-advanced-admin", authority: "normative", kind: "official", url: "https://developer.wordpress.org/advanced-administration/", topics: ["administration", "security", "performance", "server", "multisite"] },
  { id: "wp-coding-standards", authority: "normative", kind: "official", url: "https://developer.wordpress.org/coding-standards/", topics: ["PHP", "JavaScript", "CSS", "HTML", "accessibility"] },
  { id: "wp-cli", authority: "normative", kind: "official", url: "https://developer.wordpress.org/cli/commands/", topics: ["WP-CLI", "maintenance", "search-replace", "plugins", "themes", "database"] },
  { id: "wp-core-field-guides", authority: "authoritative-change-log", kind: "official", url: "https://make.wordpress.org/core/tag/field-guide/", topics: ["release changes", "breaking changes", "deprecations", "developer notes"] },
  { id: "wp-news", authority: "authoritative-release", kind: "official", url: "https://wordpress.org/news/category/releases/", topics: ["releases", "security releases", "maintenance releases"] },
  { id: "reddit-wordpress", authority: "community-secondary", kind: "reddit", url: "https://www.reddit.com/r/Wordpress/", topics: ["operations", "plugins", "themes", "troubleshooting", "hosting"] },
  { id: "reddit-prowordpress", authority: "community-secondary", kind: "reddit", url: "https://www.reddit.com/r/ProWordPress/", topics: ["professional development", "architecture", "Gutenberg", "performance"] },
  { id: "reddit-woocommerce", authority: "community-secondary", kind: "reddit", url: "https://www.reddit.com/r/woocommerce/", topics: ["commerce", "checkout", "plugins", "integrations"] }
]);

export const WORDPRESS_CURRICULUM = Object.freeze([
  { order: 1, id: "core-model", topics: ["request lifecycle", "hooks", "roles/capabilities", "options", "metadata", "cron"] },
  { order: 2, id: "remote-operations", topics: ["REST discovery", "Application Passwords", "OPTIONS schema", "WP-CLI", "wp-admin boundaries"] },
  { order: 3, id: "content", topics: ["posts", "pages", "media", "taxonomies", "revisions", "navigation"] },
  { order: 4, id: "frontend-staff", topics: ["HTML", "CSS", "JavaScript", "PHP templates", "responsive design", "accessibility", "Core Web Vitals"] },
  { order: 5, id: "gutenberg", topics: ["blocks", "block.json", "theme.json", "global styles", "templates", "template parts", "data stores"] },
  { order: 6, id: "themes-plugins", topics: ["block themes", "classic themes", "child themes", "plugins", "hooks", "settings API", "security"] },
  { order: 7, id: "integrations", topics: ["REST", "HTTP API", "OAuth", "webhooks", "external commerce", "social links", "brand assets"] },
  { order: 8, id: "production", topics: ["backup", "rollback", "staging", "cache/CDN", "observability", "security hardening", "updates"] },
  { order: 9, id: "community-evidence", topics: ["Reddit troubleshooting", "failure patterns", "plugin compatibility reports", "operational trade-offs"] }
]);

const OFFICIAL_HOST_SUFFIXES = ["developer.wordpress.org", "wordpress.org", "make.wordpress.org", "wp-cli.org"];
const REDDIT_HOSTS = new Set(["reddit.com", "www.reddit.com", "old.reddit.com"]);

export function sha256(value) {
  return createHash("sha256").update(String(value)).digest("hex");
}

export function normalizeSiteUrl(value) {
  const raw = String(value || "").trim();
  if (!raw) throw new Error("site_url is required");
  const parsed = new URL(raw.includes("://") ? raw : `https://${raw}`);
  if (!["http:", "https:"].includes(parsed.protocol)) throw new Error("WordPress site must use http or https");
  parsed.hash = "";
  parsed.search = "";
  let pathname = parsed.pathname.replace(/\/{2,}/g, "/");
  if (!pathname.endsWith("/")) pathname += "/";
  parsed.pathname = pathname;
  return parsed.toString();
}

export function siteFingerprint(siteUrl) {
  return sha256(normalizeSiteUrl(siteUrl)).slice(0, 20);
}

export function defaultWordPressStateRoot(cwd = process.cwd()) {
  return resolve(process.env.AEOS_WORDPRESS_STATE_ROOT || join(cwd, ".aeos", "wordpress"));
}

export function betaMapPath(siteUrl, stateRoot = defaultWordPressStateRoot()) {
  return join(stateRoot, "sites", siteFingerprint(siteUrl), "beta-map.json");
}

export function betaMapStatus(siteUrl, stateRoot = defaultWordPressStateRoot()) {
  const path = betaMapPath(siteUrl, stateRoot);
  if (!existsSync(path)) return { exists: false, site_fingerprint: siteFingerprint(siteUrl), path };
  const parsed = JSON.parse(readFileSync(path, "utf8"));
  return { exists: true, site_fingerprint: siteFingerprint(siteUrl), path, created_at: parsed.created_at || null, map_schema_version: parsed.schema_version || null, map_sha256: sha256(JSON.stringify(parsed)) };
}

export function persistBetaMapOnce(siteUrl, map, stateRoot = defaultWordPressStateRoot()) {
  const path = betaMapPath(siteUrl, stateRoot);
  if (existsSync(path)) {
    const existing = JSON.parse(readFileSync(path, "utf8"));
    return { status: "REUSED", first_run: false, path, map: existing, map_sha256: sha256(JSON.stringify(existing)) };
  }
  mkdirSync(resolve(path, ".."), { recursive: true });
  const normalized = {
    schema_version: "1.0.0",
    map_type: "WORDPRESS_BETA_FIRST_RUN",
    mapping_policy: "CREATE_ONCE_REUSE_AFTERWARDS",
    site_url: normalizeSiteUrl(siteUrl),
    site_fingerprint: siteFingerprint(siteUrl),
    created_at: new Date().toISOString(),
    ...map
  };
  const tmp = `${path}.${process.pid}.${Date.now()}.tmp`;
  writeFileSync(tmp, `${JSON.stringify(normalized, null, 2)}\n`, { mode: 0o600 });
  renameSync(tmp, path);
  return { status: "CREATED", first_run: true, path, map: normalized, map_sha256: sha256(JSON.stringify(normalized)) };
}

export function readBetaMap(siteUrl, stateRoot = defaultWordPressStateRoot()) {
  const path = betaMapPath(siteUrl, stateRoot);
  if (!existsSync(path)) return null;
  return JSON.parse(readFileSync(path, "utf8"));
}

export function classifyKnowledgeUrl(value) {
  const url = new URL(String(value));
  if (url.protocol !== "https:") throw new Error("knowledge sources must use https");
  const host = url.hostname.toLowerCase().replace(/^www\./, "");
  if (REDDIT_HOSTS.has(url.hostname.toLowerCase()) || host === "reddit.com") return { allowed: true, authority: "community-secondary", kind: "reddit", host: url.hostname.toLowerCase() };
  if (OFFICIAL_HOST_SUFFIXES.some((allowed) => url.hostname.toLowerCase() === allowed || url.hostname.toLowerCase().endsWith(`.${allowed}`))) return { allowed: true, authority: "normative", kind: "official", host: url.hostname.toLowerCase() };
  throw new Error(`knowledge host is not allowlisted: ${url.hostname}`);
}

export function isPrivateAddress(value) {
  const address = String(value || "").toLowerCase();
  if (!address) return true;
  if (address === "::1" || address === "0:0:0:0:0:0:0:1") return true;
  if (address.startsWith("fe80:") || address.startsWith("fc") || address.startsWith("fd")) return true;
  if (isIP(address) === 4) {
    const [a, b] = address.split(".").map(Number);
    if (a === 10 || a === 127 || a === 0) return true;
    if (a === 169 && b === 254) return true;
    if (a === 172 && b >= 16 && b <= 31) return true;
    if (a === 192 && b === 168) return true;
    if (a === 100 && b >= 64 && b <= 127) return true;
  }
  return false;
}

export function isPrivateHostname(hostname) {
  const host = String(hostname || "").toLowerCase().replace(/\.$/, "");
  if (!host || host === "localhost" || host.endsWith(".localhost") || host.endsWith(".local")) return true;
  if (isIP(host)) return isPrivateAddress(host);
  return false;
}

export function mutationGate(operation, { env = process.env, permanent = false, confirmation = "" } = {}) {
  const mode = String(env.AEOS_WORDPRESS_MUTATION_MODE || "read-only").toLowerCase();
  if (mode !== "approved-write") return { allowed: false, decision: "DENY", reason: "WORDPRESS_MUTATION_MODE_READ_ONLY", operation };
  if (permanent) {
    if (String(env.AEOS_WORDPRESS_ALLOW_PERMANENT_DELETE || "false").toLowerCase() !== "true") return { allowed: false, decision: "DENY", reason: "PERMANENT_DELETE_RUNTIME_GATE_DISABLED", operation };
    if (confirmation !== "PERMANENT_DELETE") return { allowed: false, decision: "DENY", reason: "PERMANENT_DELETE_CONFIRMATION_REQUIRED", operation };
  }
  return { allowed: true, decision: "ALLOW_WITH_EXTERNAL_AEOS_APPROVAL", reason: "RUNTIME_GATE_OPEN", operation };
}

export function redactSensitive(value, env = process.env) {
  let text = String(value ?? "");
  const secrets = [env.AEOS_WORDPRESS_APP_PASSWORD, env.AEOS_WORDPRESS_ADMIN_PASSWORD, env.WORDPRESS_APP_PASSWORD].filter((item) => typeof item === "string" && item.length >= 4);
  for (const secret of secrets) text = text.split(secret).join("[REDACTED]");
  text = text.replace(/(authorization\s*:\s*(?:basic|bearer)\s+)[^\s]+/gi, "$1[REDACTED]");
  text = text.replace(/(password|token|secret|cookie)\s*[=:]\s*[^\s,;]+/gi, "$1=[REDACTED]");
  return text;
}

export function buildExternalLinkPlan({ service, href, label, icon_url: iconUrl = "" }) {
  const normalizedHref = new URL(String(href));
  if (!["https:", "http:"].includes(normalizedHref.protocol)) throw new Error("external integration href must use http or https");
  if (isPrivateHostname(normalizedHref.hostname)) throw new Error("external integration href cannot target a private/local host");
  let normalizedIcon = null;
  if (iconUrl) {
    const icon = new URL(String(iconUrl));
    if (icon.protocol !== "https:") throw new Error("icon_url must use https");
    if (isPrivateHostname(icon.hostname)) throw new Error("icon_url cannot target a private/local host");
    normalizedIcon = icon.toString();
  }
  const safeLabel = String(label || service || normalizedHref.hostname).trim();
  return {
    service: String(service || "external"), href: normalizedHref.toString(), presentation: "COMPACT_ICON_LINK",
    icon_policy: { preferred: ["official-brand-kit", "official-provider-icon", "local-wordpress-media-cache"], favicon_ico_fallback: true, hotlinking_default: false, licensing_must_be_respected: true, source_url: normalizedIcon },
    accessibility: { aria_label: safeLabel, visible_text_required: false, tooltip_recommended: true, keyboard_focus_required: true },
    html_attributes: { target: "_blank", rel: "noopener noreferrer external" }
  };
}

export function knowledgeCachePath(url, stateRoot = defaultWordPressStateRoot()) {
  return join(stateRoot, "knowledge", "cache", `${sha256(url).slice(0, 24)}.json`);
}
