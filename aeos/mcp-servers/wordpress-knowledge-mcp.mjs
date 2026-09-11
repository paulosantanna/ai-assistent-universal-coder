#!/usr/bin/env node

const OFFICIAL_SOURCES = [
  { id: "wp-dev", name: "WordPress Developer Resources", base: "https://developer.wordpress.org/", authority: "official", weight: 100 },
  { id: "wp-rest", name: "REST API Handbook", base: "https://developer.wordpress.org/rest-api/", authority: "official", weight: 100 },
  { id: "wp-plugin", name: "Plugin Handbook", base: "https://developer.wordpress.org/plugins/", authority: "official", weight: 100 },
  { id: "wp-theme", name: "Theme Handbook", base: "https://developer.wordpress.org/themes/", authority: "official", weight: 100 },
  { id: "wp-block", name: "Block Editor Handbook", base: "https://developer.wordpress.org/block-editor/", authority: "official", weight: 100 },
  { id: "wp-cli", name: "WP-CLI", base: "https://developer.wordpress.org/cli/commands/", authority: "official", weight: 95 },
  { id: "wp-core", name: "WordPress Code Reference", base: "https://developer.wordpress.org/reference/", authority: "official", weight: 100 },
  { id: "wp-support", name: "WordPress Documentation", base: "https://wordpress.org/documentation/", authority: "official", weight: 90 },
  { id: "make-core", name: "Make WordPress Core", base: "https://make.wordpress.org/core/", authority: "official", weight: 90 }
];

const COMMUNITY_SOURCES = [
  { id: "reddit-wordpress", name: "r/Wordpress", base: "https://www.reddit.com/r/Wordpress/", authority: "community", weight: 45 },
  { id: "reddit-plugins", name: "r/WordpressPlugins", base: "https://www.reddit.com/r/WordpressPlugins/", authority: "community", weight: 40 },
  { id: "reddit-themes", name: "r/WordpressThemes", base: "https://www.reddit.com/r/WordpressThemes/", authority: "community", weight: 40 }
];

const TOPICS = {
  architecture: ["core lifecycle", "hooks", "actions", "filters", "template hierarchy", "REST API", "capabilities"],
  frontend: ["block editor", "Site Editor", "theme.json", "templates", "patterns", "responsive CSS", "JavaScript", "accessibility", "performance"],
  themes: ["block themes", "classic themes", "child themes", "assets", "template hierarchy", "global styles"],
  plugins: ["plugin architecture", "hooks", "activation", "uninstall", "settings", "custom post types", "REST endpoints"],
  security: ["capabilities", "nonces", "sanitization", "escaping", "validation", "CSRF", "XSS", "SQL injection", "file uploads"],
  operations: ["wp-admin", "cookie auth", "REST nonce", "WP-CLI", "staging", "backup", "rollback", "cache", "cron"],
  integrations: ["external APIs", "webhooks", "deep links", "payments", "marketplaces", "social links", "brand icons", "favicons"],
  commerce: ["checkout handoff", "payment gateway patterns", "order links", "tracking", "consent", "failure fallback"],
  production: ["staging-first", "backup", "database drift", "maintenance window", "observability", "rollback", "cache invalidation"]
};

function tool(name, description, properties = {}) {
  return { name, description, inputSchema: { type: "object", properties, additionalProperties: false } };
}

function listTools() {
  return [
    tool("wordpress_knowledge.source_catalog", "Return governed WordPress source catalog and authority ranking."),
    tool("wordpress_knowledge.topic_map", "Return structured WordPress expertise topics.", { topic: { type: "string" } }),
    tool("wordpress_knowledge.search_plan", "Build an evidence-first search plan across official WordPress docs and Reddit community sources.", { query: { type: "string" }, include_reddit: { type: "boolean" }, max_results: { type: "integer" } }),
    tool("wordpress_knowledge.fetch_policy", "Validate whether a URL is allowed and classify its authority.", { url: { type: "string" } }),
    tool("wordpress_knowledge.reddit_pattern_plan", "Build a Reddit community-evidence plan for operational patterns and failure modes.", { query: { type: "string" }, max_results: { type: "integer" } }),
    tool("wordpress_knowledge.integration_map", "Return WordPress-side integration concerns for an external provider.", { provider: { type: "string" }, interaction: { type: "string" } }),
    tool("wordpress_knowledge.security_gate", "Return WordPress security checklist for a proposed change.", { change_type: { type: "string" } }),
    tool("wordpress_knowledge.beta_mapping_plan", "Return one-shot read-only Beta Mapping plan for a remote WordPress site."),
    tool("wordpress_knowledge.source_policy", "Return source authority, freshness, contradiction and citation policy.")
  ];
}

function normalizeUrl(raw) {
  try { return new URL(String(raw)); } catch { return null; }
}

function classifyUrl(raw) {
  const url = normalizeUrl(raw);
  if (!url || url.protocol !== "https:") return { allowed: false, reason: "HTTPS_REQUIRED" };
  const host = url.hostname.toLowerCase();
  const all = [...OFFICIAL_SOURCES, ...COMMUNITY_SOURCES];
  const matched = all.find((source) => {
    const baseHost = new URL(source.base).hostname.toLowerCase();
    return host === baseHost || host.endsWith(`.${baseHost}`);
  });
  if (!matched) return { allowed: false, reason: "DOMAIN_NOT_ALLOWLISTED", host };
  return { allowed: true, source: matched, url: url.toString() };
}

function searchPlan(input = {}) {
  const query = String(input.query || "").trim();
  if (!query) return { status: "BLOCKED", reason: "QUERY_REQUIRED" };
  const includeReddit = input.include_reddit !== false;
  const maxResults = Math.max(1, Math.min(Number(input.max_results || 20), 50));
  const official = OFFICIAL_SOURCES.map((source) => ({ ...source, query }));
  const community = includeReddit ? COMMUNITY_SOURCES.map((source) => ({ ...source, query })) : [];
  return {
    status: "PLAN",
    query,
    max_results: maxResults,
    execution_order: ["official", "community"],
    official,
    community,
    reconciliation: "Official documentation wins normative conflicts. Reddit is retained as experiential evidence and must be corroborated for material technical claims."
  };
}

function integrationMap(input = {}) {
  const provider = String(input.provider || "unknown").trim().toLowerCase();
  const interaction = String(input.interaction || "external-link").trim().toLowerCase();
  return {
    provider,
    interaction,
    wordpress_side: [
      "prefer plugin/block/theme extension points over WordPress core edits",
      "store provider URL/config in WordPress options or block attributes with validation",
      "render compact brand icon/favico control with accessible aria-label/title and text fallback",
      "use rel=noopener noreferrer for external targets when applicable",
      "sanitize URLs and escape output",
      "define failure fallback when external service is unavailable",
      "do not embed third-party secrets in theme/plugin source",
      "verify provider trademark/icon usage and official API/deep-link documentation before production"
    ]
  };
}

function securityGate(input = {}) {
  return {
    change_type: String(input.change_type || "generic"),
    required: [
      "current_user_can/capability check for privileged operations",
      "nonce/CSRF protection for wp-admin/AJAX/REST cookie-auth writes",
      "sanitize and validate every external input",
      "escape late for HTML/attribute/URL/JS output",
      "prepared queries for direct database access",
      "no raw secret/cookie/token persistence",
      "backup/rollback before production mutation",
      "staging or dry-run when change risk is medium/high"
    ]
  };
}

function betaMappingPlan() {
  return {
    mode: "ONE_SHOT_READ_ONLY",
    trigger: "only when no valid beta-map exists for site_id",
    auth: "external runtime cookie/cookie-jar reference",
    collect: [
      "site URL and WordPress version",
      "REST API index and namespaces",
      "active theme + parent/child relationship",
      "installed plugins + activation state + versions",
      "block/classic theme mode and Site Editor capability",
      "pages/posts/content types counts and IDs without unnecessary body duplication",
      "menus/navigation structures",
      "registered sidebars/widgets where applicable",
      "templates/template parts/patterns",
      "media configuration and representative metadata",
      "permalink/site settings safe metadata",
      "roles/capabilities summary without personal user data",
      "cache/security/CDN indicators",
      "known custom REST routes and plugin namespaces",
      "front-end asset graph and externally integrated domains",
      "deployment/backup/rollback affordances visible to the authenticated session"
    ],
    persist: ".aeos/wordpress/sites/<site-id>/beta-map.json",
    never_persist: ["cookie contents", "session tokens", "nonces", "passwords", "personal user data", "secret option values"],
    subsequent_runs: "reuse beta-map; run lightweight delta/preflight only; never full-remap automatically",
    explicit_remap: "allowed only when user explicitly requests remap or stored map is invalid/corrupt"
  };
}

function call(name, input = {}) {
  if (name === "wordpress_knowledge.source_catalog") return { official: OFFICIAL_SOURCES, community: COMMUNITY_SOURCES };
  if (name === "wordpress_knowledge.topic_map") {
    const topic = String(input.topic || "").trim();
    return topic ? { topic, items: TOPICS[topic] || [], available_topics: Object.keys(TOPICS) } : { topics: TOPICS };
  }
  if (name === "wordpress_knowledge.search_plan") return searchPlan(input);
  if (name === "wordpress_knowledge.fetch_policy") return classifyUrl(input.url);
  if (name === "wordpress_knowledge.reddit_pattern_plan") return searchPlan({ query: input.query, include_reddit: true, max_results: input.max_results });
  if (name === "wordpress_knowledge.integration_map") return integrationMap(input);
  if (name === "wordpress_knowledge.security_gate") return securityGate(input);
  if (name === "wordpress_knowledge.beta_mapping_plan") return betaMappingPlan();
  if (name === "wordpress_knowledge.source_policy") return {
    normative_priority: ["WordPress official developer documentation", "WordPress official project/support documentation", "current source/code evidence", "Reddit community evidence"],
    reddit_role: "operational experience, edge cases, failure modes and community patterns; never normative authority by itself",
    freshness_required: true,
    citations_required: true,
    contradiction_policy: "prefer current official docs for API/security semantics; retain community disagreement as a risk signal"
  };
  return { status: "ERROR", reason: "UNKNOWN_TOOL", tool: name };
}

function resultContent(value) { return [{ type: "text", text: JSON.stringify(value, null, 2) }]; }

function handle(message) {
  if (Array.isArray(message)) return message.map(handle).filter(Boolean);
  const { id, method, params = {} } = message;
  if (method === "initialize") return { jsonrpc: "2.0", id, result: { protocolVersion: params.protocolVersion || "2024-11-05", capabilities: { tools: { listChanged: false } }, serverInfo: { name: "aeos-wordpress-knowledge", version: "1.0.0" }, instructions: "Evidence-first WordPress knowledge MCP. Official WordPress sources are normative; Reddit is community evidence." } };
  if (method === "notifications/initialized") return null;
  if (method === "tools/list") return { jsonrpc: "2.0", id, result: { tools: listTools() } };
  if (method === "tools/call") return { jsonrpc: "2.0", id, result: { content: resultContent(call(params.name, params.arguments || {})), isError: false } };
  if (method === "ping") return { jsonrpc: "2.0", id, result: {} };
  if (id == null) return null;
  return { jsonrpc: "2.0", id, error: { code: -32601, message: `Unknown method: ${method}` } };
}

function send(message) {
  if (!message) return;
  const payload = JSON.stringify(message);
  process.stdout.write(`Content-Length: ${Buffer.byteLength(payload, "utf8")}\r\n\r\n${payload}`);
}

let buffer = Buffer.alloc(0);
process.stdin.on("data", (chunk) => { buffer = Buffer.concat([buffer, chunk]); parse(); });
function parse() {
  while (buffer.length) {
    let headerEnd = buffer.indexOf("\r\n\r\n");
    let sep = 4;
    if (headerEnd < 0) { headerEnd = buffer.indexOf("\n\n"); sep = 2; }
    if (headerEnd < 0) {
      const newline = buffer.indexOf("\n");
      if (newline < 0) return;
      const line = buffer.slice(0, newline).toString("utf8").trim();
      buffer = buffer.slice(newline + 1);
      if (line) dispatch(line);
      continue;
    }
    const header = buffer.slice(0, headerEnd).toString("utf8");
    const match = /Content-Length:\s*(\d+)/i.exec(header);
    if (!match) { buffer = buffer.slice(headerEnd + sep); continue; }
    const length = Number(match[1]);
    const start = headerEnd + sep;
    if (buffer.length < start + length) return;
    const body = buffer.slice(start, start + length).toString("utf8");
    buffer = buffer.slice(start + length);
    dispatch(body);
  }
}
function dispatch(raw) {
  try { send(handle(JSON.parse(raw))); }
  catch { send({ jsonrpc: "2.0", id: null, error: { code: -32700, message: "Invalid JSON" } }); }
}
