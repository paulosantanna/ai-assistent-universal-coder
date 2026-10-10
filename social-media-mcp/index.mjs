#!/usr/bin/env node
/**
 * Social Media MCP - TikTok & Instagram Browser-Based Authentication
 * 
 * Provides governed access to TikTok and Instagram through browser-based sessions.
 * Sessions are stored encrypted locally for up to 30 days or until cookies expire.
 * 
 * Security: Never logs cookies, credentials, or session tokens.
 * All authentication happens via external browser - user logs in manually.
 */

import { randomUUID, createHash } from "node:crypto";
import { readFileSync, existsSync, statSync } from "node:fs";
import { resolve } from "node:path";
import {
  PLATFORMS,
  MAX_SESSION_AGE_MS,
  parseCookies,
  createSession,
  getSession,
  getSessionInfo,
  getAllSessions,
  buildCookieHeader,
  validateSession,
  closeSession,
  getLoginInstructions,
  pruneSessions,
  filterPlatformCookies,
  hasValidSessionCookies
} from "./session-manager.mjs";

const SESSION_CACHE = new Map();
const FETCH_CACHE = new Map();
const DEFAULT_TTL_MS = 15 * 60 * 1000;

function now() { return Date.now(); }
function sha256(value) { return createHash("sha256").update(value).digest("hex"); }
function ok(data = {}) { return { success: true, data }; }
function fail(error, code = "BLOCKED") { return { success: false, error, code }; }

function redact(value) {
  return String(value ?? "").replace(/(sessionid|csrftoken|ds_user_id|tt_webid|msToken|password|token|secret|cookie|authorization)\s*[=:]\s*\S+/gi, "$1=***REDACTED***");
}

function redactObject(input) {
  if (!input || typeof input !== "object") return input;
  const out = Array.isArray(input) ? [] : {};
  for (const [key, value] of Object.entries(input)) {
    if (/(sessionid|csrftoken|ds_user_id|tt_webid|mstoken|password|passwd|token|secret|cookie|authorization|private[_-]?key)/i.test(key)) {
      out[key] = "***REDACTED***";
    } else if (value && typeof value === "object") {
      out[key] = redactObject(value);
    } else {
      out[key] = value;
    }
  }
  return out;
}

function requireApproved(params) {
  if (params?.approved !== true) throw new Error("approved=true required for mutating operations");
  if (!String(params?.change_id || "").trim()) throw new Error("change_id required for mutating operations");
  if (!String(params?.rollback_ref || "").trim()) throw new Error("rollback_ref required for mutating operations");
}

function getPlatform(platformId) {
  const platform = PLATFORMS[platformId];
  if (!platform) throw new Error(`Unknown platform: ${platformId}. Supported: ${Object.keys(PLATFORMS).join(", ")}`);
  return platform;
}

/**
 * Open session from cookie file (exported from browser)
 */
async function openCookieFile(params) {
  pruneSessions();
  
  const platformId = String(params.platform || "").toLowerCase();
  const platform = getPlatform(platformId);
  
  const requestedPath = String(params.cookie_file_path || params.path || "").trim();
  if (!requestedPath) throw new Error("cookie_file_path is required");
  
  if (!existsSync(requestedPath)) throw new Error("Cookie file does not exist");
  const stat = statSync(requestedPath);
  if (!stat.isFile()) throw new Error("Cookie reference must point to a file");
  if (stat.size > 5 * 1024 * 1024) throw new Error("Cookie file exceeds 5MB limit");
  
  const text = readFileSync(requestedPath, "utf8");
  let cookies;
  
  try {
    const json = JSON.parse(text);
    cookies = parseCookies(json, platform);
  } catch {
    // Try Netscape format
    cookies = parseCookies(text, platform);
  }
  
  if (cookies.length === 0) {
    throw new Error(`No valid cookies found for ${platform.name} in file`);
  }
  
  if (!hasValidSessionCookies(cookies, platform)) {
    throw new Error(`Missing required cookies for ${platform.name}: ${platform.requiredCookies.join(", ")}`);
  }
  
  const sourceRef = `cookie_file:${requestedPath}:${sha256(text).slice(0, 12)}`;
  const session = createSession(platformId, cookies, sourceRef);
  
  return ok({
    status: "SESSION_CREATED",
    platform: platformId,
    platform_name: platform.name,
    session_ref: session.id,
    cookie_count: session.cookies.length,
    cookie_names: session.cookies.map(c => c.name),
    expires_at: new Date(session.expiresAt).toISOString(),
    cookie_expires_at: session.cookieExpiry ? new Date(session.cookieExpiry).toISOString() : null,
    days_valid: Math.ceil((session.expiresAt - now()) / (24 * 60 * 60 * 1000)),
    next: "Use session_ref for authenticated operations. Session valid for 30 days or until cookies expire."
  });
}

/**
 * Get session info
 */
function sessionInfo(params) {
  const platformId = String(params.platform || "").toLowerCase();
  const sessionRef = String(params.session_ref || params.ref || "").trim();
  if (!sessionRef) throw new Error("session_ref is required");
  
  const info = getSessionInfo(platformId, sessionRef);
  return ok(info);
}

/**
 * List all sessions for a platform
 */
function listSessions(params) {
  const platformId = String(params.platform || "").toLowerCase();
  const platform = getPlatform(platformId);
  
  const sessions = getAllSessions(platformId);
  return ok({
    platform: platformId,
    platform_name: platform.name,
    sessions,
    count: sessions.length
  });
}

/**
 * Close/remove session
 */
function closeSessionHandler(params) {
  const platformId = String(params.platform || "").toLowerCase();
  const sessionRef = String(params.session_ref || params.ref || "").trim();
  if (!sessionRef) throw new Error("session_ref is required");
  
  closeSession(platformId, sessionRef);
  return ok({ closed: true, platform: platformId, session_ref: sessionRef });
}

/**
 * Validate session with test request
 */
async function validateSessionHandler(params) {
  const platformId = String(params.platform || "").toLowerCase();
  const sessionRef = String(params.session_ref || params.ref || "").trim();
  if (!sessionRef) throw new Error("session_ref is required");
  
  const result = await validateSession(platformId, sessionRef);
  return ok(result);
}

/**
 * Get login instructions for manual browser authentication
 */
function loginInstructions(params) {
  const platformId = String(params.platform || "").toLowerCase();
  const instructions = getLoginInstructions(platformId);
  return ok(instructions);
}

/**
 * Make authenticated request to platform API
 */
async function authenticatedFetch(params) {
  const platformId = String(params.platform || "").toLowerCase();
  const platform = getPlatform(platformId);
  const sessionRef = String(params.session_ref || "").trim();
  if (!sessionRef) throw new Error("session_ref is required");
  
  const session = getSession(platformId, sessionRef);
  const url = String(params.url || "").trim();
  if (!url) throw new Error("url is required");
  
  const target = new URL(url);
  if (target.protocol !== "https:") throw new Error("Only HTTPS URLs allowed");
  
  // Validate domain is allowed for platform
  const targetHost = target.hostname.toLowerCase();
  const allowed = platform.cookieDomains.some(d => 
    targetHost === d.replace(/^\./, "") || targetHost.endsWith(`.${d.replace(/^\./, "")}`)
  );
  if (!allowed) {
    throw new Error(`URL domain not allowed for ${platform.name}: ${target.hostname}`);
  }
  
  const cookieHeader = buildCookieHeader(session, url);
  
  const method = String(params.method || "GET").toUpperCase();
  const headers = {
    Accept: "application/json, text/html;q=0.9, */*;q=0.8",
    Cookie: cookieHeader,
    "User-Agent": "AEOS-SocialMedia/1.0",
    ...(params.headers || {})
  };
  
  const fetchOptions = {
    method,
    redirect: "manual",
    headers
  };
  
  if (method !== "GET" && method !== "HEAD") {
    if (params.body) {
      headers["Content-Type"] = params.content_type || "application/json";
      fetchOptions.body = typeof params.body === "string" ? params.body : JSON.stringify(params.body);
    }
  }
  
  // Check cache for GET requests
  const cacheKey = `${sessionRef}:${method}:${url}:${sha256(JSON.stringify(params.body || {}))}`;
  if (method === "GET" && FETCH_CACHE.has(cacheKey)) {
    const cached = FETCH_CACHE.get(cacheKey);
    if (cached.expiresAt > now()) {
      return ok({ ...cached.data, cached: true });
    }
    FETCH_CACHE.delete(cacheKey);
  }
  
  const response = await fetch(url, fetchOptions);
  const responseText = await response.text();
  
  let responseData;
  try {
    responseData = JSON.parse(responseText);
  } catch {
    responseData = { raw: responseText };
  }
  
  const result = {
    url: target.toString(),
    status: response.status,
    status_text: response.statusText,
    headers: Object.fromEntries(response.headers.entries()),
    data: responseData,
    redirected: response.status >= 300 && response.status < 400,
    login_page: responseText.includes("login") || responseText.includes("Login") || response.status === 401
  };
  
  // Cache successful GET responses for 30 seconds
  if (method === "GET" && response.status === 200 && !result.login_page) {
    FETCH_CACHE.set(cacheKey, {
      data: result,
      expiresAt: now() + 30000
    });
  }
  
  // Check if session expired (redirected to login)
  if (result.login_page) {
    // Don't throw - let caller handle re-authentication
    result.session_expired = true;
  }
  
  return ok(result);
}

/**
 * TikTok-specific: Get user profile
 */
async function tiktokGetProfile(params) {
  const result = await authenticatedFetch({
    platform: "tiktok",
    session_ref: params.session_ref,
    url: "https://www.tiktok.com/api/user/profile/",
    method: "GET"
  });
  return result;
}

/**
 * TikTok-specific: Get user videos
 */
async function tiktokGetVideos(params) {
  const cursor = params.cursor || 0;
  const count = params.count || 20;
  const url = `https://www.tiktok.com/api/user/posts/?cursor=${cursor}&count=${count}`;
  
  return authenticatedFetch({
    platform: "tiktok",
    session_ref: params.session_ref,
    url,
    method: "GET"
  });
}

/**
 * Instagram-specific: Get user profile
 */
async function instagramGetProfile(params) {
  const username = params.username || "self";
  const url = username === "self" 
    ? "https://www.instagram.com/api/v1/accounts/current_user/?edit=true"
    : `https://www.instagram.com/api/v1/users/web_profile_info/?username=${encodeURIComponent(username)}`;
  
  return authenticatedFetch({
    platform: "instagram",
    session_ref: params.session_ref,
    url,
    method: "GET"
  });
}

/**
 * Instagram-specific: Get user media
 */
async function instagramGetMedia(params) {
  const userId = params.user_id;
  if (!userId) throw new Error("user_id is required for Instagram media");
  
  const url = `https://www.instagram.com/api/v1/feed/user/${userId}/?count=${params.count || 20}`;
  
  return authenticatedFetch({
    platform: "instagram",
    session_ref: params.session_ref,
    url,
    method: "GET"
  });
}

/**
 * Instagram-specific: Get media insights (requires business/creator account)
 */
async function instagramGetInsights(params) {
  const mediaId = params.media_id;
  if (!mediaId) throw new Error("media_id is required");
  
  const url = `https://www.instagram.com/api/v1/media/${mediaId}/insights/`;
  
  return authenticatedFetch({
    platform: "instagram",
    session_ref: params.session_ref,
    url,
    method: "GET"
  });
}

/**
 * Main dispatch
 */
async function dispatch(action, params = {}) {
  try {
    switch (action) {
      case "social_media.health":
        return ok({
          adapter: "social-media-mcp",
          platforms: Object.keys(PLATFORMS),
          active_sessions: [...SESSION_CACHE.keys()].length,
          uptime_seconds: Math.round(process.uptime())
        });
      
      case "social_media.platforms.list":
        return ok({
          platforms: Object.entries(PLATFORMS).map(([id, p]) => ({
            id,
            name: p.name,
            login_url: p.loginUrl,
            api_base: p.apiBaseUrl,
            required_cookies: p.requiredCookies
          }))
        });
      
      case "social_media.session.open_cookie_file":
        return openCookieFile(params);
      
      case "social_media.session.info":
        return sessionInfo(params);
      
      case "social_media.session.list":
        return listSessions(params);
      
      case "social_media.session.close":
        return closeSessionHandler(params);
      
      case "social_media.session.validate":
        return validateSessionHandler(params);
      
      case "social_media.auth.login_instructions":
        return loginInstructions(params);
      
      case "social_media.api.fetch":
        return authenticatedFetch(params);
      
      case "social_media.tiktok.profile":
        return tiktokGetProfile(params);
      
      case "social_media.tiktok.videos":
        return tiktokGetVideos(params);
      
      case "social_media.instagram.profile":
        return instagramGetProfile(params);
      
      case "social_media.instagram.media":
        return instagramGetMedia(params);
      
      case "social_media.instagram.insights":
        return instagramGetInsights(params);
      
      default:
        return fail(`Unknown action: ${action}`, "UNKNOWN_ACTION");
    }
  } catch (error) {
    return fail(redact(error instanceof Error ? error.message : String(error)), "ERROR");
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

export { dispatch, handleEnvelope, PLATFORMS };

// CLI for testing
const isMain = process.argv[1]
  ? resolve(process.argv[1]).toLowerCase() === fileURLToPath(import.meta.url).toLowerCase()
  : false;

if (isMain) {
  const readline = await import("node:readline/promises");
  const rl = readline.createInterface({ input: process.stdin });
  
  console.log("Social Media MCP ready. Send JSON envelopes via stdin.");
  
  for await (const line of rl) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    let envelope;
    try { envelope = JSON.parse(trimmed); } catch {
      console.log(JSON.stringify({ success: false, error: "Invalid JSON", code: "ERROR" }));
      continue;
    }
    const result = await handleEnvelope(envelope);
    console.log(JSON.stringify(redactObject(result)));
  }
}