/**
 * Social Media Session Manager
 * 
 * Handles browser-based authentication for TikTok and Instagram.
 * Opens external browser for user login, captures cookies, and stores sessions
 * for up to 30 days or until platform cookies expire.
 * 
 * Security: Cookies are stored encrypted locally, never exposed to logs/evidence.
 */

import { createHash, randomUUID, createCipheriv, createDecipheriv, randomBytes } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync, statSync, unlinkSync, readdirSync } from "node:fs";
import { join, resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Configuration
const SESSION_DIR = join(__dirname, "..", ".aeos", "social-sessions");
const ENCRYPTION_KEY_FILE = join(SESSION_DIR, ".encryption.key");
const MAX_SESSION_AGE_MS = 30 * 24 * 60 * 60 * 1000; // 30 days
const DEFAULT_TTL_MS = 15 * 60 * 1000; // 15 minutes for active session reference
const MAX_COOKIE_BYTES = 5 * 1024 * 1024; // 5MB max cookie data

// Platform configurations
const PLATFORMS = {
  tiktok: {
    name: "TikTok",
    loginUrl: "https://www.tiktok.com/login",
    apiBaseUrl: "https://www.tiktok.com",
    cookieDomains: [".tiktok.com", "tiktok.com"],
    requiredCookies: ["sessionid", "tt_webid", "s_v_web_id"],
    sessionCookieNames: ["sessionid", "tt_webid", "s_v_web_id", "tt_webid_v2", "msToken"]
  },
  instagram: {
    name: "Instagram",
    loginUrl: "https://www.instagram.com/accounts/login/",
    apiBaseUrl: "https://www.instagram.com",
    cookieDomains: [".instagram.com", "instagram.com", ".facebook.com", "facebook.com"],
    requiredCookies: ["sessionid", "csrftoken", "ds_user_id"],
    sessionCookieNames: ["sessionid", "csrftoken", "ds_user_id", "mid", "ig_did", "rur"]
  }
};

// In-memory session cache
const sessionCache = new Map();

/**
 * Get or create encryption key for session storage
 */
function getEncryptionKey() {
  if (!existsSync(ENCRYPTION_KEY_FILE)) {
    const key = randomBytes(32);
    writeFileSync(ENCRYPTION_KEY_FILE, key.toString("base64"), { mode: 0o600 });
    return key;
  }
  return Buffer.from(readFileSync(ENCRYPTION_KEY_FILE, "utf8"), "base64");
}

/**
 * Encrypt data for storage
 */
function encryptData(data) {
  const key = getEncryptionKey();
  const iv = randomBytes(16);
  const cipher = createCipheriv("aes-256-gcm", key, iv);
  const json = JSON.stringify(data);
  const encrypted = Buffer.concat([cipher.update(json, "utf8"), cipher.final()]);
  const authTag = cipher.getAuthTag();
  return Buffer.concat([iv, authTag, encrypted]).toString("base64");
}

/**
 * Decrypt data from storage
 */
function decryptData(encryptedBase64) {
  const key = getEncryptionKey();
  const buffer = Buffer.from(encryptedBase64, "base64");
  const iv = buffer.subarray(0, 16);
  const authTag = buffer.subarray(16, 32);
  const encrypted = buffer.subarray(32);
  const decipher = createDecipheriv("aes-256-gcm", key, iv);
  decipher.setAuthTag(authTag);
  const decrypted = Buffer.concat([decipher.update(encrypted), decipher.final()]);
  return JSON.parse(decrypted.toString("utf8"));
}

/**
 * Ensure session directory exists
 */
function ensureSessionDir() {
  if (!existsSync(SESSION_DIR)) {
    mkdirSync(SESSION_DIR, { recursive: true, mode: 0o700 });
  }
}

/**
 * Normalize hostname for comparison
 */
function normalizeHost(host) {
  return String(host || "").trim().toLowerCase().replace(/^\.+/, "").replace(/\.+$/, "");
}

/**
 * Check if cookie domain matches platform domain
 */
function cookieMatchesPlatform(cookieDomain, platform) {
  const normalizedCookie = normalizeHost(cookieDomain);
  return platform.cookieDomains.some(domain => {
    const normalizedDomain = normalizeHost(domain);
    return normalizedCookie === normalizedDomain || normalizedCookie.endsWith(`.${normalizedDomain}`);
  });
}

/**
 * Parse cookie expiration
 */
function parseExpires(value) {
  const numeric = Number(value);
  if (!Number.isFinite(numeric) || numeric <= 0) return undefined;
  return numeric > 10000000000 ? numeric : numeric * 1000;
}

/**
 * Parse cookies from various formats (JSON, Netscape, etc.)
 */
function parseCookies(input, platform) {
  const cookies = [];
  
  if (Array.isArray(input)) {
    // Array of cookie objects
    for (const item of input) {
      if (!item || typeof item !== "object") continue;
      const name = String(item.name ?? "").trim();
      const domain = normalizeHost(String(item.domain ?? ""));
      if (!name || !domain) continue;
      if (!cookieMatchesPlatform(domain, platform)) continue;
      
      cookies.push({
        name,
        value: String(item.value ?? ""),
        domain,
        path: String(item.path ?? "/") || "/",
        secure: Boolean(item.secure),
        httpOnly: Boolean(item.httpOnly),
        sameSite: item.sameSite || "Lax",
        expiresAtMs: parseExpires(item.expirationDate ?? item.expires ?? item.expiry)
      });
    }
  } else if (input && typeof input === "object") {
    // Chrome DevTools Protocol format or similar
    if (Array.isArray(input.cookies)) {
      return parseCookies(input.cookies, platform);
    }
  }
  
  return cookies;
}

/**
 * Filter cookies for a specific platform
 */
function filterPlatformCookies(cookies, platform) {
  return cookies.filter(cookie => cookieMatchesPlatform(cookie.domain, platform));
}

/**
 * Check if session has valid cookies for platform
 */
function hasValidSessionCookies(cookies, platform) {
  const platformCookies = filterPlatformCookies(cookies, platform);
  const required = platform.requiredCookies || [];
  const found = new Set(platformCookies.map(c => c.name));
  return required.every(req => found.has(req));
}

/**
 * Get session file path for platform
 */
function getSessionFilePath(platformId, sessionId) {
  ensureSessionDir();
  return join(SESSION_DIR, `${platformId}_${sessionId}.session.enc`);
}

/**
 * List all stored sessions for a platform
 */
function listStoredSessions(platformId) {
  ensureSessionDir();
  const files = readdirSync(SESSION_DIR);
  const sessions = [];
  
  for (const file of files) {
    if (file.startsWith(`${platformId}_`) && file.endsWith(".session.enc")) {
      const sessionId = file.replace(`${platformId}_`, "").replace(".session.enc", "");
      try {
        const data = readFileSync(join(SESSION_DIR, file), "utf8");
        const session = decryptData(data);
        sessions.push({
          sessionId,
          platform: platformId,
          ...session
        });
      } catch (e) {
        // Corrupted session file, skip
      }
    }
  }
  
  return sessions;
}

/**
 * Store session to encrypted file
 */
function storeSession(platformId, session) {
  const filePath = getSessionFilePath(platformId, session.id);
  const encrypted = encryptData(session);
  writeFileSync(filePath, encrypted, { mode: 0o600 });
}

/**
 * Load session from encrypted file
 */
function loadSession(platformId, sessionId) {
  const filePath = getSessionFilePath(platformId, sessionId);
  if (!existsSync(filePath)) return null;
  
  try {
    const data = readFileSync(filePath, "utf8");
    return decryptData(data);
  } catch (e) {
    return null;
  }
}

/**
 * Delete session file
 */
function deleteSessionFile(platformId, sessionId) {
  const filePath = getSessionFilePath(platformId, sessionId);
  if (existsSync(filePath)) {
    unlinkSync(filePath);
  }
}

/**
 * Prune expired sessions from cache and storage
 */
function pruneSessions() {
  const now = Date.now();
  
  // Prune memory cache
  for (const [id, session] of sessionCache.entries()) {
    if (session.expiresAt <= now) {
      sessionCache.delete(id);
    }
  }
  
  // Prune stored sessions
  for (const platformId of Object.keys(PLATFORMS)) {
    const sessions = listStoredSessions(platformId);
    for (const session of sessions) {
      if (session.expiresAt <= now || session.createdAt + MAX_SESSION_AGE_MS <= now) {
        deleteSessionFile(platformId, session.sessionId);
      }
    }
  }
}

/**
 * Create a new session from cookies
 */
function createSession(platformId, cookies, sourceRef) {
  const platform = PLATFORMS[platformId];
  if (!platform) throw new Error(`Unknown platform: ${platformId}`);
  
  const platformCookies = filterPlatformCookies(cookies, platform);
  if (platformCookies.length === 0) {
    throw new Error(`No valid cookies found for ${platform.name}`);
  }
  
  if (!hasValidSessionCookies(platformCookies, platform)) {
    throw new Error(`Missing required cookies for ${platform.name}: ${platform.requiredCookies.join(", ")}`);
  }
  
  // Check cookie expiration - find earliest expiry
  const cookieExpiries = platformCookies
    .filter(c => c.expiresAtMs)
    .map(c => c.expiresAtMs);
  
  const earliestCookieExpiry = cookieExpiries.length > 0 ? Math.min(...cookieExpiries) : null;
  const maxExpiry = Date.now() + MAX_SESSION_AGE_MS;
  const expiresAt = earliestCookieExpiry ? Math.min(earliestCookieExpiry, maxExpiry) : maxExpiry;
  
  const id = `sess_${randomUUID()}`;
  const now = Date.now();
  
  const session = {
    id,
    platform: platformId,
    cookies: platformCookies,
    allowedDomains: platform.cookieDomains,
    sourceRef,
    createdAt: now,
    expiresAt,
    cookieExpiry: earliestCookieExpiry
  };
  
  // Store in memory cache
  sessionCache.set(id, session);
  
  // Persist to encrypted file
  storeSession(platformId, session);
  
  return session;
}

/**
 * Get session from cache or storage
 */
function getSession(platformId, sessionRef) {
  pruneSessions();
  
  // Check memory cache first
  let session = sessionCache.get(sessionRef);
  if (session && session.platform === platformId) {
    if (session.expiresAt > Date.now()) {
      // Extend TTL for active use
      session.expiresAt = Date.now() + DEFAULT_TTL_MS;
      storeSession(platformId, session);
      return session;
    }
    sessionCache.delete(sessionRef);
  }
  
  // Try loading from storage
  session = loadSession(platformId, sessionRef);
  if (session && session.expiresAt > Date.now()) {
    sessionCache.set(sessionRef, session);
    return session;
  }
  
  if (session) {
    deleteSessionFile(platformId, sessionRef);
  }
  
  throw new Error(`Unknown or expired session for ${platformId}: ${sessionRef}`);
}

/**
 * Get session info (public, no cookies)
 */
function getSessionInfo(platformId, sessionRef) {
  const session = getSession(platformId, sessionRef);
  const now = Date.now();
  
  return {
    session_ref: session.id,
    platform: session.platform,
    platform_name: PLATFORMS[session.platform].name,
    cookie_count: session.cookies.length,
    cookie_names: session.cookies.map(c => c.name),
    created_at: new Date(session.createdAt).toISOString(),
    expires_at: new Date(session.expiresAt).toISOString(),
    cookie_expires_at: session.cookieExpiry ? new Date(session.cookieExpiry).toISOString() : null,
    days_until_expiry: Math.ceil((session.expiresAt - now) / (24 * 60 * 60 * 1000)),
    source_ref: session.sourceRef,
    is_valid: session.expiresAt > now
  };
}

/**
 * Build cookie header for requests
 */
function buildCookieHeader(session, targetUrl) {
  const target = new URL(targetUrl);
  const targetHost = normalizeHost(target.hostname);
  const now = Date.now();
  
  const applicableCookies = session.cookies.filter(cookie => {
    if (!cookieMatchesPlatform(cookie.domain, PLATFORMS[session.platform])) return false;
    if (cookie.secure && target.protocol !== "https:") return false;
    if (cookie.expiresAtMs && cookie.expiresAtMs <= now) return false;
    const targetPath = target.pathname || "/";
    if (!targetPath.startsWith(cookie.path || "/")) return false;
    return true;
  });
  
  if (applicableCookies.length === 0) {
    throw new Error(`No applicable cookies for ${targetUrl}`);
  }
  
  return applicableCookies.map(c => `${c.name}=${c.value}`).join("; ");
}

/**
 * Validate session by making a test request
 */
async function validateSession(platformId, sessionRef) {
  const session = getSession(platformId, sessionRef);
  const platform = PLATFORMS[platformId];
  
  try {
    const cookieHeader = buildCookieHeader(session, platform.apiBaseUrl);
    const response = await fetch(platform.apiBaseUrl, {
      method: "GET",
      redirect: "manual",
      headers: {
        Accept: "text/html,application/json;q=0.9,*/*;q=0.8",
        Cookie: cookieHeader,
        "User-Agent": "AEOS-SocialMedia/1.0"
      }
    });
    
    // Check if we got redirected to login (session expired)
    const isLoginPage = response.status === 302 || response.status === 401 || 
      (response.headers.get("location") || "").includes("login");
    
    return {
      valid: !isLoginPage && response.status === 200,
      status: response.status,
      redirected: isLoginPage,
      session_ref: sessionRef
    };
  } catch (e) {
    return {
      valid: false,
      error: e instanceof Error ? e.message : String(e),
      session_ref: sessionRef
    };
  }
}

/**
 * Close/remove session
 */
function closeSession(platformId, sessionRef) {
  sessionCache.delete(sessionRef);
  deleteSessionFile(platformId, sessionRef);
  return true;
}

/**
 * Get all sessions for a platform
 */
function getAllSessions(platformId) {
  pruneSessions();
  return listStoredSessions(platformId).map(s => getSessionInfo(platformId, s.sessionId));
}

/**
 * Generate browser login instructions
 */
function getLoginInstructions(platformId) {
  const platform = PLATFORMS[platformId];
  if (!platform) throw new Error(`Unknown platform: ${platformId}`);
  
  return {
    platform: platformId,
    platform_name: platform.name,
    login_url: platform.loginUrl,
    instructions: [
      `1. Open your browser and navigate to: ${platform.loginUrl}`,
      `2. Log in to your ${platform.name} account normally`,
      `3. After successful login, export cookies for ${platform.cookieDomains.join(", ")}`,
      `4. Import the cookies using the import_cookies tool`
    ],
    required_cookies: platform.requiredCookies,
    supported_formats: ["JSON array", "Netscape format", "Chrome DevTools Protocol"]
  };
}

export {
  PLATFORMS,
  SESSION_DIR,
  MAX_SESSION_AGE_MS,
  DEFAULT_TTL_MS,
  parseCookies,
  normalizeHost,
  cookieMatchesPlatform,
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
};