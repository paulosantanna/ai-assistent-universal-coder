#!/usr/bin/env node
import { lookup } from "node:dns/promises";
import { existsSync, mkdirSync, readdirSync, statSync, writeFileSync } from "node:fs";
import { basename, dirname, join, resolve } from "node:path";
import { pathToFileURL } from "node:url";
import {
  WORDPRESS_CURRICULUM,
  WORDPRESS_KNOWLEDGE_CATALOG,
  betaMapStatus,
  buildExternalLinkPlan,
  classifyKnowledgeUrl,
  defaultWordPressStateRoot,
  isPrivateAddress,
  isPrivateHostname,
  knowledgeCachePath,
  mutationGate,
  normalizeSiteUrl,
  persistBetaMapOnce,
  readBetaMap,
  redactSensitive,
  sha256,
  siteFingerprint
} from "../../scripts/aeos-wordpress-governance.mjs";

const SERVER_VERSION = "1.0.0";
const DEFAULT_TIMEOUT_MS = 12000;
const MAX_TEXT_BYTES = 1_500_000;
const MAX_MEDIA_BYTES = 10_000_000;
const MAX_CRAWL_PAGES = 100;
const ALLOWED_CONTENT_RESOURCES = new Set(["posts", "pages"]);
const SAFE_SETTINGS = new Set(["title", "description", "timezone", "date_format", "time_format", "start_of_week", "language", "posts_per_page", "default_category", "show_on_front", "page_on_front", "page_for_posts"]);
const DESIGN_ROUTE = /^\/wp-json\/wp\/v2\/(templates|template-parts|global-styles|navigation)(?:\/|$)/;

function tool(name, description, inputSchema = {}, security = "read-only") {
  return { name, description, inputSchema: { type: "object", properties: inputSchema, additionalProperties: false }, annotations: { security } };
}

export function toolsForWordPress() {
  return [
    tool("wordpress.knowledge.catalog", "Return the curated WordPress source catalog and authority hierarchy."),
    tool("wordpress.knowledge.curriculum", "Return the structured Staff-level WordPress learning curriculum."),
    tool("wordpress.knowledge.source_policy", "Return source authority, freshness, Reddit corroboration and production evidence rules."),
    tool("wordpress.knowledge.fetch", "Fetch and optionally cache an allowlisted WordPress/Reddit knowledge source.", { url: { type: "string" }, max_chars: { type: "integer" }, persist: { type: "boolean" } }),
    tool("wordpress.knowledge.search", "Search official Developer.WordPress.org pages or Reddit WordPress communities with bounded results.", { query: { type: "string" }, provider: { type: "string", enum: ["official", "reddit", "both"] }, max_results: { type: "integer" } }),
    tool("wordpress.knowledge.crawl_official", "Boundedly crawl official WordPress documentation roots and cache structured text snapshots.", { seed_urls: { type: "array", items: { type: "string" } }, max_pages: { type: "integer" }, max_depth: { type: "integer" } }),
    tool("wordpress.knowledge.index_status", "Return local WordPress knowledge-cache status."),
    tool("wordpress.site.discover", "Discover a WordPress site's REST API and capability surface without persisting the Beta map.", { site_url: { type: "string" } }),
    tool("wordpress.site.map_status", "Return whether the one-shot Beta map already exists for a site.", { site_url: { type: "string" } }),
    tool("wordpress.site.map_beta", "Create the persistent Beta site map on the first run only; later calls reuse it without remapping.", { site_url: { type: "string" } }),
    tool("wordpress.site.map_get", "Read the persisted Beta map for subsequent WordPress work.", { site_url: { type: "string" } }),
    tool("wordpress.rest.options", "Inspect a WordPress REST route schema with OPTIONS.", { site_url: { type: "string" }, route: { type: "string" } }),
    tool("wordpress.content.list", "List posts or pages through authenticated WordPress REST API.", { site_url: { type: "string" }, resource: { type: "string", enum: ["posts", "pages"] }, per_page: { type: "integer" }, page: { type: "integer" }, search: { type: "string" } }),
    tool("wordpress.content.get", "Get one WordPress post or page.", { site_url: { type: "string" }, resource: { type: "string", enum: ["posts", "pages"] }, id: { type: "integer" }, context: { type: "string" } }),
    tool("wordpress.content.upsert", "Create or update a WordPress post/page after AEOS approval and runtime write gate.", { site_url: { type: "string" }, resource: { type: "string", enum: ["posts", "pages"] }, id: { type: "integer" }, payload: { type: "object" } }, "production-write"),
    tool("wordpress.content.trash", "Move a WordPress post/page to trash; trash-first is the default deletion behavior.", { site_url: { type: "string" }, resource: { type: "string", enum: ["posts", "pages"] }, id: { type: "integer" } }, "production-write"),
    tool("wordpress.content.delete_permanent", "Permanently delete content only with an additional runtime gate and literal confirmation.", { site_url: { type: "string" }, resource: { type: "string", enum: ["posts", "pages"] }, id: { type: "integer" }, confirmation: { type: "string" } }, "destructive-production-write"),
    tool("wordpress.settings.read", "Read WordPress settings available to the authenticated principal.", { site_url: { type: "string" } }),
    tool("wordpress.settings.update", "Update only the safe allowlisted WordPress settings after approval.", { site_url: { type: "string" }, settings: { type: "object" } }, "production-write"),
    tool("wordpress.plugins.list", "List WordPress plugins exposed by the REST plugin endpoint.", { site_url: { type: "string" } }),
    tool("wordpress.plugins.install", "Install a plugin from the official WordPress.org directory by slug after approval.", { site_url: { type: "string" }, slug: { type: "string" }, status: { type: "string", enum: ["active", "inactive"] } }, "production-write"),
    tool("wordpress.plugins.set_status", "Activate or deactivate an installed plugin after approval.", { site_url: { type: "string" }, plugin: { type: "string" }, status: { type: "string", enum: ["active", "inactive"] } }, "production-write"),
    tool("wordpress.design.update", "Update block-theme templates, template parts, navigation or global styles through allowlisted REST routes.", { site_url: { type: "string" }, route: { type: "string" }, method: { type: "string", enum: ["POST", "PUT", "PATCH"] }, payload: { type: "object" } }, "production-write"),
    tool("wordpress.media.import_url", "Import a public image/icon into the WordPress Media Library after SSRF and MIME checks.", { site_url: { type: "string" }, source_url: { type: "string" }, filename: { type: "string" }, alt_text: { type: "string" } }, "production-write"),
    tool("wordpress.integrations.link_plan", "Build an accessible icon-link integration plan for 99, Mercado Livre/Pago, Keeta, TikTok, iFood, social networks or another service.", { service: { type: "string" }, href: { type: "string" }, label: { type: "string" }, icon_url: { type: "string" }, api_integration: { type: "boolean" } }),
    tool("wordpress.admin.session_plan", "Return the governed remote wp-admin access contract. Application Passwords are API credentials, not interactive wp-admin passwords.", { site_url: { type: "string" } })
  ];
}

function runtimeSite(input = {}) {
  return normalizeSiteUrl(input.site_url || process.env.AEOS_WORDPRESS_SITE_URL);
}

function authHeaders(siteUrl) {
  const configured = process.env.AEOS_WORDPRESS_SITE_URL ? normalizeSiteUrl(process.env.AEOS_WORDPRESS_SITE_URL) : null;
  const user = process.env.AEOS_WORDPRESS_USER || "";
  const password = process.env.AEOS_WORDPRESS_APP_PASSWORD || "";
  if (!configured || !user || !password) return {};
  if (new URL(configured).origin !== new URL(siteUrl).origin) return {};
  return { Authorization: `Basic ${Buffer.from(`${user}:${password}`).toString("base64")}` };
}

async function assertNetworkTarget(url, { allowPrivate = false } = {}) {
  const parsed = url instanceof URL ? url : new URL(String(url));
  if (!["http:", "https:"].includes(parsed.protocol)) throw new Error("network target must use http or https");
  if (isPrivateHostname(parsed.hostname)) {
    if (!allowPrivate) throw new Error(`private/local network target denied: ${parsed.hostname}`);
    return parsed;
  }
  const records = await lookup(parsed.hostname, { all: true, verbatim: true });
  if (!records.length) throw new Error(`DNS resolution returned no addresses for ${parsed.hostname}`);
  if (!allowPrivate && records.some((record) => isPrivateAddress(record.address))) throw new Error(`DNS resolved to a private/local address: ${parsed.hostname}`);
  return parsed;
}

function allowPrivateWordPress() {
  return String(process.env.AEOS_WORDPRESS_ALLOW_PRIVATE_NETWORK || "false").toLowerCase() === "true";
}

async function fetchBounded(url, { method = "GET", headers = {}, body, timeoutMs = DEFAULT_TIMEOUT_MS, maxBytes = MAX_TEXT_BYTES, allowPrivate = false } = {}) {
  const target = await assertNetworkTarget(url, { allowPrivate });
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), Math.min(Math.max(Number(timeoutMs) || DEFAULT_TIMEOUT_MS, 1000), 30000));
  try {
    const response = await fetch(target, { method, headers: { "User-Agent": "AEOS-WordPress-Expert/1.0", ...headers }, body, redirect: "follow", signal: controller.signal });
    await assertNetworkTarget(new URL(response.url), { allowPrivate });
    const contentLength = Number(response.headers.get("content-length") || 0);
    if (contentLength && contentLength > maxBytes) throw new Error(`response exceeds byte limit (${contentLength} > ${maxBytes})`);
    const array = new Uint8Array(await response.arrayBuffer());
    if (array.byteLength > maxBytes) throw new Error(`response exceeds byte limit (${array.byteLength} > ${maxBytes})`);
    return { response, bytes: Buffer.from(array) };
  } finally { clearTimeout(timer); }
}

async function wpRequest(siteUrl, route, { method = "GET", payload, rawBody, headers = {}, authenticated = true, maxBytes = MAX_TEXT_BYTES } = {}) {
  const site = new URL(normalizeSiteUrl(siteUrl));
  const target = new URL(String(route).replace(/^\//, ""), site);
  if (target.origin !== site.origin) throw new Error("WordPress REST route must remain on the configured site origin");
  const requestHeaders = { Accept: "application/json", ...(authenticated ? authHeaders(siteUrl) : {}), ...headers };
  let body = rawBody;
  if (payload !== undefined) { requestHeaders["Content-Type"] = "application/json"; body = JSON.stringify(payload); }
  const { response, bytes } = await fetchBounded(target, { method, headers: requestHeaders, body, maxBytes, allowPrivate: allowPrivateWordPress() });
  const text = bytes.toString("utf8");
  let data = text;
  const contentType = response.headers.get("content-type") || "";
  if (contentType.includes("json") || text.trim().startsWith("{") || text.trim().startsWith("[")) { try { data = text ? JSON.parse(text) : null; } catch { data = text; } }
  if (!response.ok) {
    const detail = redactSensitive(typeof data === "string" ? data.slice(0, 1000) : JSON.stringify(data).slice(0, 1000));
    throw new Error(`WordPress HTTP ${response.status} ${response.statusText}: ${detail}`);
  }
  return { status: response.status, headers: Object.fromEntries(response.headers.entries()), data };
}

function compactWpEntity(value) {
  if (!value || typeof value !== "object") return value;
  const keys = ["id", "date", "modified", "slug", "status", "type", "link", "template", "plugin", "name", "version", "author", "theme", "stylesheet"];
  return Object.fromEntries(keys.filter((key) => value[key] !== undefined).map((key) => [key, value[key]]));
}

function stripHtml(html) {
  return String(html || "").replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, " ").replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, " ").replace(/<!--([\s\S]*?)-->/g, " ").replace(/<[^>]+>/g, " ").replace(/&nbsp;/gi, " ").replace(/&amp;/gi, "&").replace(/&lt;/gi, "<").replace(/&gt;/gi, ">").replace(/&quot;/gi, '"').replace(/&#39;/gi, "'").replace(/\s+/g, " ").trim();
}

function htmlTitle(html) { return stripHtml(String(html).match(/<title[^>]*>([\s\S]*?)<\/title>/i)?.[1] || "").slice(0, 300); }
function linksFromHtml(html, baseUrl) {
  const links = [];
  for (const match of String(html).matchAll(/href=["']([^"'#]+)["']/gi)) { try { const url = new URL(match[1], baseUrl); if (url.protocol === "https:") links.push(url.toString().split("#")[0]); } catch {} }
  return [...new Set(links)];
}

async function fetchKnowledge(url, { maxChars = 40000, persist = false } = {}) {
  const source = classifyKnowledgeUrl(url);
  const { response, bytes } = await fetchBounded(url, { maxBytes: MAX_TEXT_BYTES, allowPrivate: false });
  const html = bytes.toString("utf8");
  const fullText = stripHtml(html);
  const text = fullText.slice(0, Math.min(Math.max(Number(maxChars) || 40000, 1000), 80000));
  const result = { url: response.url, title: htmlTitle(html), authority: source.authority, source_kind: source.kind, fetched_at: new Date().toISOString(), sha256: sha256(bytes), text, truncated: fullText.length > text.length };
  if (persist) { const path = knowledgeCachePath(response.url); mkdirSync(dirname(path), { recursive: true }); writeFileSync(path, `${JSON.stringify(result, null, 2)}\n`, { mode: 0o600 }); result.cache_path = path; }
  return result;
}

async function searchOfficial(query, maxResults) {
  const target = new URL("https://developer.wordpress.org/"); target.searchParams.set("s", query);
  const { response, bytes } = await fetchBounded(target, { maxBytes: MAX_TEXT_BYTES });
  return linksFromHtml(bytes.toString("utf8"), response.url).filter((link) => { try { return new URL(link).hostname === "developer.wordpress.org"; } catch { return false; } }).filter((link) => !/\/(feed|wp-json)(\/|$)/.test(new URL(link).pathname)).slice(0, maxResults).map((url) => ({ url, authority: "normative", source_kind: "official" }));
}

async function searchReddit(query, maxResults) {
  const communities = ["Wordpress", "ProWordPress", "woocommerce"]; const results = [];
  for (const community of communities) {
    if (results.length >= maxResults) break;
    const url = new URL(`https://www.reddit.com/r/${community}/search.json`); url.searchParams.set("q", query); url.searchParams.set("restrict_sr", "1"); url.searchParams.set("sort", "relevance"); url.searchParams.set("t", "all"); url.searchParams.set("limit", String(Math.min(maxResults, 10)));
    try {
      const { bytes } = await fetchBounded(url, { maxBytes: MAX_TEXT_BYTES }); const payload = JSON.parse(bytes.toString("utf8"));
      for (const child of payload?.data?.children || []) { const data = child?.data || {}; results.push({ title: String(data.title || "").slice(0, 300), url: data.permalink ? new URL(data.permalink, "https://www.reddit.com").toString() : null, subreddit: data.subreddit || community, score: data.score ?? null, comments: data.num_comments ?? null, authority: "community-secondary", source_kind: "reddit" }); if (results.length >= maxResults) break; }
    } catch (error) { results.push({ subreddit: community, authority: "community-secondary", source_kind: "reddit", status: "UNAVAILABLE", error: redactSensitive(error.message) }); }
  }
  return results.slice(0, maxResults);
}

async function crawlOfficial(input = {}) {
  const requested = Array.isArray(input.seed_urls) && input.seed_urls.length ? input.seed_urls : WORDPRESS_KNOWLEDGE_CATALOG.filter((source) => source.kind === "official").map((source) => source.url);
  const maxPages = Math.min(Math.max(Number(input.max_pages) || 25, 1), MAX_CRAWL_PAGES); const maxDepth = Math.min(Math.max(Number(input.max_depth) || 1, 0), 3);
  const queue = requested.map((url) => ({ url, depth: 0 })); const seen = new Set(); const stored = []; const failures = [];
  while (queue.length && seen.size < maxPages) {
    const item = queue.shift(); if (!item || seen.has(item.url)) continue;
    try { const classified = classifyKnowledgeUrl(item.url); if (classified.kind !== "official") continue; } catch { continue; }
    seen.add(item.url);
    try {
      const source = await fetchKnowledge(item.url, { maxChars: 60000, persist: true }); stored.push({ url: source.url, cache_path: source.cache_path, sha256: source.sha256, depth: item.depth });
      if (item.depth < maxDepth) { const { bytes } = await fetchBounded(item.url, { maxBytes: MAX_TEXT_BYTES }); for (const link of linksFromHtml(bytes.toString("utf8"), item.url)) { try { const kind = classifyKnowledgeUrl(link); if (kind.kind === "official" && !seen.has(link) && queue.length < maxPages * 8) queue.push({ url: link, depth: item.depth + 1 }); } catch {} } }
    } catch (error) { failures.push({ url: item.url, error: redactSensitive(error.message) }); }
  }
  return { status: failures.length && !stored.length ? "BLOCKED" : "PASS", pages_attempted: seen.size, pages_cached: stored.length, stored, failures: failures.slice(0, 20), bounded: true, note: "Crawl is intentionally bounded. Re-run periodically to expand/refresh coverage without freezing a stale copy of all WordPress documentation." };
}

function indexStatus() {
  const root = join(defaultWordPressStateRoot(), "knowledge", "cache"); if (!existsSync(root)) return { cached_sources: 0, cache_root: root, total_bytes: 0 };
  const files = readdirSync(root).filter((name) => name.endsWith(".json")); return { cached_sources: files.length, cache_root: root, total_bytes: files.reduce((sum, name) => sum + statSync(join(root, name)).size, 0) };
}

async function safeProbe(siteUrl, route, mapper = (value) => value, authenticated = true) {
  try { const result = await wpRequest(siteUrl, route, { authenticated }); return { available: true, status: result.status, value: mapper(result.data) }; }
  catch (error) { return { available: false, error: redactSensitive(error.message).slice(0, 500) }; }
}

async function discoverSite(siteUrl) {
  const normalized = normalizeSiteUrl(siteUrl);
  const root = await safeProbe(normalized, "/wp-json/", (data) => ({ name: data?.name || null, description: data?.description || null, url: data?.url || normalized, namespaces: Array.isArray(data?.namespaces) ? data.namespaces : [], routes: data?.routes ? Object.keys(data.routes) : [] }), false);
  const routes = root.available ? root.value.routes : [];
  const homepage = await safeProbe(normalized, "/", (data) => data, false);
  let versionHint = null; if (homepage.available && typeof homepage.value === "string") versionHint = homepage.value.match(/<meta[^>]+name=["']generator["'][^>]+content=["']WordPress\s+([^"']+)/i)?.[1] || null;
  const probes = {
    types: await safeProbe(normalized, "/wp-json/wp/v2/types?context=edit", (data) => Object.values(data || {}).map((type) => ({ slug: type.slug, name: type.name, rest_base: type.rest_base, viewable: type.viewable }))),
    active_themes: await safeProbe(normalized, "/wp-json/wp/v2/themes?status=active", (data) => (Array.isArray(data) ? data : []).map(compactWpEntity)),
    plugins: await safeProbe(normalized, "/wp-json/wp/v2/plugins?per_page=100", (data) => (Array.isArray(data) ? data : []).map(compactWpEntity)),
    settings: await safeProbe(normalized, "/wp-json/wp/v2/settings", (data) => Object.keys(data || {}).filter((key) => SAFE_SETTINGS.has(key)).reduce((acc, key) => ({ ...acc, [key]: data[key] }), {})),
    templates: await safeProbe(normalized, "/wp-json/wp/v2/templates?per_page=100", (data) => (Array.isArray(data) ? data : []).map((item) => ({ id: item.id, slug: item.slug, theme: item.theme, source: item.source, type: item.type }))),
    template_parts: await safeProbe(normalized, "/wp-json/wp/v2/template-parts?per_page=100", (data) => (Array.isArray(data) ? data : []).map((item) => ({ id: item.id, slug: item.slug, theme: item.theme, area: item.area, source: item.source }))),
    navigation: await safeProbe(normalized, "/wp-json/wp/v2/navigation?per_page=100", (data) => (Array.isArray(data) ? data : []).map(compactWpEntity)),
    abilities: routes.some((route) => route.includes("wp-abilities")) ? await safeProbe(normalized, routes.find((route) => route.includes("wp-abilities")) || "/wp-json/wp-abilities/v1", (data) => data) : { available: false, reason: "route-not-advertised" }
  };
  return { discovered_at: new Date().toISOString(), site_url: normalized, site_fingerprint: siteFingerprint(normalized), wordpress_version_hint: versionHint, rest: { available: root.available, namespaces: root.available ? root.value.namespaces : [], route_count: routes.length, route_prefixes: [...new Set(routes.map((route) => route.split("/").slice(0, 4).join("/")))].filter(Boolean).slice(0, 100) }, authentication: { method: authHeaders(normalized).Authorization ? "application-password" : "anonymous", application_password_configured: Boolean(authHeaders(normalized).Authorization), interactive_wp_admin: "SEPARATE_GOVERNED_BROWSER_SESSION" }, capabilities: probes };
}

function requireWrite(operation, options = {}) { const gate = mutationGate(operation, options); if (!gate.allowed) throw new Error(`${gate.reason}: ${operation}`); return gate; }
function ensureContentResource(resource) { const value = String(resource || ""); if (!ALLOWED_CONTENT_RESOURCES.has(value)) throw new Error(`unsupported content resource: ${value}`); return value; }
function responseSummary(result) { if (Array.isArray(result.data)) return { status: result.status, items: result.data.map(compactWpEntity), count: result.data.length }; return { status: result.status, item: compactWpEntity(result.data) }; }

export async function executeWordPressTool(name, input = {}) {
  switch (name) {
    case "wordpress.knowledge.catalog": return { sources: WORDPRESS_KNOWLEDGE_CATALOG, source_count: WORDPRESS_KNOWLEDGE_CATALOG.length };
    case "wordpress.knowledge.curriculum": return { curriculum: WORDPRESS_CURRICULUM, model: "official-normative-plus-reddit-secondary" };
    case "wordpress.knowledge.source_policy": return { hierarchy: ["official WordPress developer/core documentation", "official release notes and source reference", "community support evidence", "Reddit experience reports"], reddit_policy: "Reddit is secondary evidence. Production decisions require corroboration from official documentation or multiple independent reports plus local reproduction.", freshness: "Re-check official documentation at execution time for version-sensitive claims.", copyright: "Cache bounded text snapshots for internal retrieval; do not republish complete documentation or Reddit threads." };
    case "wordpress.knowledge.fetch": return fetchKnowledge(input.url, { maxChars: input.max_chars, persist: Boolean(input.persist) });
    case "wordpress.knowledge.search": { const query = String(input.query || "").trim(); if (!query) throw new Error("query is required"); const max = Math.min(Math.max(Number(input.max_results) || 10, 1), 30); const provider = input.provider || "both"; const official = provider === "official" || provider === "both" ? await searchOfficial(query, max) : []; const reddit = provider === "reddit" || provider === "both" ? await searchReddit(query, max) : []; return { query, provider, official: official.slice(0, max), reddit: reddit.slice(0, max) }; }
    case "wordpress.knowledge.crawl_official": return crawlOfficial(input);
    case "wordpress.knowledge.index_status": return indexStatus();
    case "wordpress.site.discover": return discoverSite(runtimeSite(input));
    case "wordpress.site.map_status": return betaMapStatus(runtimeSite(input));
    case "wordpress.site.map_beta": { const site = runtimeSite(input); const existing = readBetaMap(site); if (existing) return { status: "REUSED", first_run: false, map: existing, ...betaMapStatus(site) }; const discovery = await discoverSite(site); return persistBetaMapOnce(site, { beta_status: "CONSOLIDATED", discovery }); }
    case "wordpress.site.map_get": { const site = runtimeSite(input); const map = readBetaMap(site); if (!map) throw new Error("BETA_MAP_NOT_FOUND: run wordpress.site.map_beta once before subsequent site mutations"); return { status: "PASS", map, ...betaMapStatus(site) }; }
    case "wordpress.rest.options": { const site = runtimeSite(input); const route = String(input.route || ""); if (!route.startsWith("/wp-json/")) throw new Error("route must begin with /wp-json/"); return wpRequest(site, route, { method: "OPTIONS" }); }
    case "wordpress.content.list": { const site = runtimeSite(input); const resource = ensureContentResource(input.resource); const params = new URLSearchParams({ context: "edit", per_page: String(Math.min(Math.max(Number(input.per_page) || 20, 1), 100)), page: String(Math.max(Number(input.page) || 1, 1)) }); if (input.search) params.set("search", String(input.search)); return responseSummary(await wpRequest(site, `/wp-json/wp/v2/${resource}?${params}`)); }
    case "wordpress.content.get": { const site = runtimeSite(input); const resource = ensureContentResource(input.resource); const id = Number(input.id); if (!Number.isInteger(id) || id <= 0) throw new Error("id must be a positive integer"); return wpRequest(site, `/wp-json/wp/v2/${resource}/${id}?context=${encodeURIComponent(input.context || "edit")}`); }
    case "wordpress.content.upsert": { const site = runtimeSite(input); requireWrite(name); const resource = ensureContentResource(input.resource); const route = input.id ? `/wp-json/wp/v2/${resource}/${Number(input.id)}` : `/wp-json/wp/v2/${resource}`; return responseSummary(await wpRequest(site, route, { method: "POST", payload: input.payload || {} })); }
    case "wordpress.content.trash": { const site = runtimeSite(input); requireWrite(name); const resource = ensureContentResource(input.resource); return responseSummary(await wpRequest(site, `/wp-json/wp/v2/${resource}/${Number(input.id)}?force=false`, { method: "DELETE" })); }
    case "wordpress.content.delete_permanent": { const site = runtimeSite(input); requireWrite(name, { permanent: true, confirmation: input.confirmation }); const resource = ensureContentResource(input.resource); return responseSummary(await wpRequest(site, `/wp-json/wp/v2/${resource}/${Number(input.id)}?force=true`, { method: "DELETE" })); }
    case "wordpress.settings.read": return wpRequest(runtimeSite(input), "/wp-json/wp/v2/settings");
    case "wordpress.settings.update": { const site = runtimeSite(input); requireWrite(name); const requested = input.settings || {}; const denied = Object.keys(requested).filter((key) => !SAFE_SETTINGS.has(key)); if (denied.length) throw new Error(`settings keys not allowlisted: ${denied.join(", ")}`); return wpRequest(site, "/wp-json/wp/v2/settings", { method: "POST", payload: requested }); }
    case "wordpress.plugins.list": return wpRequest(runtimeSite(input), "/wp-json/wp/v2/plugins?per_page=100");
    case "wordpress.plugins.install": { const site = runtimeSite(input); requireWrite(name); const slug = String(input.slug || "").trim(); if (!/^[a-z0-9][a-z0-9-]{1,100}$/.test(slug)) throw new Error("plugin slug must be a WordPress.org-style slug"); return wpRequest(site, "/wp-json/wp/v2/plugins", { method: "POST", payload: { slug, status: input.status || "inactive" } }); }
    case "wordpress.plugins.set_status": { const site = runtimeSite(input); requireWrite(name); const plugin = encodeURIComponent(String(input.plugin || "").trim()); if (!plugin) throw new Error("plugin is required"); return wpRequest(site, `/wp-json/wp/v2/plugins/${plugin}`, { method: "POST", payload: { status: input.status } }); }
    case "wordpress.design.update": { const site = runtimeSite(input); requireWrite(name); const route = String(input.route || ""); if (!DESIGN_ROUTE.test(route)) throw new Error("design route is outside templates/template-parts/global-styles/navigation allowlist"); const method = String(input.method || "POST").toUpperCase(); if (!["POST", "PUT", "PATCH"].includes(method)) throw new Error("design update supports POST, PUT or PATCH only"); return wpRequest(site, route, { method, payload: input.payload || {} }); }
    case "wordpress.media.import_url": { const site = runtimeSite(input); requireWrite(name); const sourceUrl = new URL(String(input.source_url || "")); if (sourceUrl.protocol !== "https:") throw new Error("media source_url must use https"); const { response, bytes } = await fetchBounded(sourceUrl, { maxBytes: MAX_MEDIA_BYTES, allowPrivate: false }); const mime = (response.headers.get("content-type") || "").split(";")[0].toLowerCase(); if (!mime.startsWith("image/") && mime !== "image/x-icon" && mime !== "image/vnd.microsoft.icon") throw new Error(`source is not an image/icon MIME: ${mime}`); const filename = String(input.filename || basename(sourceUrl.pathname) || "external-icon").replace(/[^A-Za-z0-9._-]/g, "-").slice(0, 120); const uploaded = await wpRequest(site, "/wp-json/wp/v2/media", { method: "POST", rawBody: bytes, headers: { "Content-Type": mime || "application/octet-stream", "Content-Disposition": `attachment; filename="${filename}"` }, maxBytes: MAX_MEDIA_BYTES }); if (input.alt_text && uploaded.data?.id) await wpRequest(site, `/wp-json/wp/v2/media/${uploaded.data.id}`, { method: "POST", payload: { alt_text: String(input.alt_text).slice(0, 500) } }); return responseSummary(uploaded); }
    case "wordpress.integrations.link_plan": { const plan = buildExternalLinkPlan(input); return { ...plan, api_integration: Boolean(input.api_integration), api_rule: input.api_integration ? "Retrieve and verify the third-party provider's official API/OAuth/webhook documentation at execution time; never invent endpoints or embed secrets client-side." : "Use an outbound icon link; no API credentials are required." }; }
    case "wordpress.admin.session_plan": { const site = runtimeSite(input); return { site_url: site, wp_admin_url: new URL("wp-admin/", site).toString(), interactive_access: "SEPARATE_GOVERNED_BROWSER_ADAPTER_REQUIRED", rest_access: authHeaders(site).Authorization ? "APPLICATION_PASSWORD_READY" : "APPLICATION_PASSWORD_NOT_CONFIGURED", rules: ["Application Passwords authenticate API requests; they are not interactive wp-admin passwords.", "Browser credentials/cookies must stay runtime-only and must never be exported or persisted by AEOS.", "Production wp-admin mutations require explicit approval, evidence and rollback."] }; }
    default: throw new Error(`unknown WordPress tool: ${name}`);
  }
}

function resultContent(value) { return [{ type: "text", text: JSON.stringify(value, null, 2) }]; }
async function handle(message) {
  if (Array.isArray(message)) { const responses = []; for (const item of message) { const response = await handle(item); if (response) responses.push(response); } return responses.length ? responses : null; }
  const { id, method, params = {} } = message;
  if (method === "initialize") return { jsonrpc: "2.0", id, result: { protocolVersion: params.protocolVersion || "2025-06-18", capabilities: { tools: { listChanged: false }, prompts: { listChanged: false }, resources: { subscribe: false, listChanged: false } }, serverInfo: { name: "aeos-wordpress-expert", version: SERVER_VERSION }, instructions: "Governed WordPress knowledge and operations MCP. Read-only by default; production writes require AEOS approval plus AEOS_WORDPRESS_MUTATION_MODE=approved-write. Secrets never enter tool arguments or output." } };
  if (method === "notifications/initialized") return null;
  if (method === "tools/list") return { jsonrpc: "2.0", id, result: { tools: toolsForWordPress() } };
  if (method === "tools/call") { try { const value = await executeWordPressTool(params.name, params.arguments || {}); return { jsonrpc: "2.0", id, result: { content: resultContent(value), isError: false } }; } catch (error) { return { jsonrpc: "2.0", id, result: { content: resultContent({ status: "BLOCKED", error: redactSensitive(error.message) }), isError: true } }; } }
  if (method === "prompts/list") return { jsonrpc: "2.0", id, result: { prompts: [] } };
  if (method === "resources/list") return { jsonrpc: "2.0", id, result: { resources: [] } };
  if (method === "ping") return { jsonrpc: "2.0", id, result: {} };
  if (id === undefined || id === null) return null;
  return { jsonrpc: "2.0", id, error: { code: -32601, message: `Unknown method: ${method}` } };
}

function send(message) { if (!message) return; const payload = JSON.stringify(message); process.stdout.write(`Content-Length: ${Buffer.byteLength(payload, "utf8")}\r\n\r\n${payload}`); }
export function startWordPressMcpServer() {
  let buffer = Buffer.alloc(0); let queue = Promise.resolve();
  function dispatch(raw) { queue = queue.then(async () => { try { send(await handle(JSON.parse(raw))); } catch { send({ jsonrpc: "2.0", id: null, error: { code: -32700, message: "Invalid JSON" } }); } }); }
  function parseBuffer() {
    while (buffer.length) {
      let headerEnd = buffer.indexOf("\r\n\r\n"); let separatorLength = 4;
      if (headerEnd < 0) { headerEnd = buffer.indexOf("\n\n"); separatorLength = 2; }
      if (headerEnd >= 0) { const header = buffer.slice(0, headerEnd).toString("utf8"); const match = /Content-Length:\s*(\d+)/i.exec(header); if (!match) { buffer = buffer.slice(headerEnd + separatorLength); continue; } const length = Number(match[1]); const start = headerEnd + separatorLength; if (buffer.length < start + length) return; const body = buffer.slice(start, start + length).toString("utf8"); buffer = buffer.slice(start + length); dispatch(body); continue; }
      const newline = buffer.indexOf("\n"); if (newline < 0) return; const line = buffer.slice(0, newline).toString("utf8").trim(); buffer = buffer.slice(newline + 1); if (line) dispatch(line);
    }
  }
  process.stdin.on("data", (chunk) => { buffer = Buffer.concat([buffer, chunk]); parseBuffer(); });
  process.on("uncaughtException", (error) => { process.stderr.write(`aeos-wordpress-expert error: ${redactSensitive(error.message)}\n`); });
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) startWordPressMcpServer();
