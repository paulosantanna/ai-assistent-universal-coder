#!/usr/bin/env node
/**
 * Cookie Export Helper
 * 
 * Helps users export cookies from browsers for TikTok/Instagram authentication.
 * Provides instructions and can convert between formats.
 */

import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { resolve, extname } from "node:path";

const PLATFORM_COOKIE_DOMAINS = {
  tikok: [".tiktok.com", "tiktok.com"],
  instagram: [".instagram.com", "instagram.com", ".facebook.com", "facebook.com"]
};

function printUsage() {
  console.log(`
Cookie Export Helper for TikTok & Instagram
=============================================

This script helps you prepare cookie files for the social-media MCP.

SUPPORTED FORMATS:
  1. JSON Array (from Cookie Editor, EditThisCookie extensions)
  2. Netscape Format (from cookies.txt, wget/curl)
  3. Chrome DevTools Protocol (from DevTools Network tab)

QUICK START:
  1. Log into TikTok/Instagram in your browser
  2. Export cookies using one of the methods below
  3. Run: node export-helper.js <platform> <cookie-file>
  4. Use the output path with social_media.session.open_cookie_file

METHOD 1: Browser Extension (Easiest)
--------------------------------------
Chrome/Edge:
  - Install "Cookie Editor" or "EditThisCookie"
  - Go to tiktok.com or instagram.com
  - Click extension → Export → Save as JSON
  
Firefox:
  - Install "Cookie Quick Manager" or "cookies.txt"
  - Export as JSON or Netscape format

METHOD 2: DevTools (No Extension)
----------------------------------
1. Open DevTools (F12)
2. Go to Application/Storage tab
3. Expand Cookies → select platform domain
4. Right-click cookie table → "Copy All" (Firefox)
   Or manually create JSON array from the table
5. Paste into a .json file

METHOD 3: Command Line (curl/wget)
-----------------------------------
# Netscape format
curl -c cookies.txt -b cookies.txt -L "https://www.tiktok.com/login"
# Then manually log in in browser, cookies.txt will be updated

PLATFORM-SPECIFIC DOMAINS:
  TikTok:    .tiktok.com, tiktok.com
  Instagram: .instagram.com, instagram.com, .facebook.com, facebook.com

REQUIRED COOKIES:
  TikTok:    sessionid, tt_webid, s_v_web_id
  Instagram: sessionid, csrftoken, ds_user_id

USAGE:
  node export-helper.js tiktok ~/Downloads/tiktok-cookies.json
  node export-helper.js instagram ~/Downloads/ig-cookies.txt

OUTPUT:
  Validates cookie file and shows:
  - Platform detected
  - Cookie count
  - Required cookies present/missing
  - Expiry info
  - Ready-to-use path for MCP
`);

  process.exit(1);
}

function parseCookieFile(filePath) {
  const text = readFileSync(filePath, "utf8");
  const ext = extname(filePath).toLowerCase();
  
  if (ext === ".json") {
    try {
      const json = JSON.parse(text);
      if (Array.isArray(json)) return { format: "json_array", cookies: json };
      if (json.cookies && Array.isArray(json.cookies)) return { format: "cdp", cookies: json.cookies };
      throw new Error("Invalid JSON structure");
    } catch (e) {
      throw new Error(`Invalid JSON: ${e.message}`);
    }
  } else if (ext === ".txt" || filePath.includes("cookies.txt")) {
    return { format: "netscape", cookies: parseNetscape(text) };
  }
  
  // Try auto-detect
  try {
    const json = JSON.parse(text);
    if (Array.isArray(json)) return { format: "json_array", cookies: json };
    if (json.cookies && Array.isArray(json.cookies)) return { format: "cdp", cookies: json.cookies };
  } catch {
    return { format: "netscape", cookies: parseNetscape(text) };
  }
}

export function parseNetscape(text) {
  const cookies = [];
  for (const line of text.split("\n")) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const parts = trimmed.split("\t");
    if (parts.length >= 7) {
      cookies.push({
        domain: parts[0],
        path: parts[2],
        secure: parts[3] === "TRUE",
        expiresAtMs: parseInt(parts[4]) * 1000 || null,
        name: parts[5],
        value: parts[6]
      });
    }
  }
  return cookies;
}

function normalizeDomain(domain) {
  return domain.replace(/^\./, "").toLowerCase();
}

function cookieMatchesDomain(cookie, platform) {
  const cookieDomain = normalizeDomain(cookie.domain);
  return PLATFORM_COOKIE_DOMAINS[platform].some(d => {
    const pd = normalizeDomain(d);
    return cookieDomain === pd || cookieDomain.endsWith(`.${pd}`);
  });
}

function validateCookies(platform, cookies) {
  const required = {
    tiktok: ["sessionid", "tt_webid", "s_v_web_id"],
    instagram: ["sessionid", "csrftoken", "ds_user_id"]
  }[platform] || [];
  
  const platformCookies = cookies.filter(c => cookieMatchesDomain(c, platform));
  const found = new Set(platformCookies.map(c => c.name));
  const missing = required.filter(r => !found.has(r));
  const extra = platformCookies.filter(c => !required.includes(c.name));
  
  const now = Date.now();
  const withExpiry = platformCookies.filter(c => c.expiresAtMs && c.expiresAtMs > now);
  const expired = platformCookies.filter(c => c.expiresAtMs && c.expiresAtMs <= now);
  const noExpiry = platformCookies.filter(c => !c.expiresAtMs);
  
  const earliestExpiry = withExpiry.length > 0 
    ? Math.min(...withExpiry.map(c => c.expiresAtMs))
    : null;
  
  return {
    platform,
    total_cookies: cookies.length,
    platform_cookies: platformCookies.length,
    required_cookies: required,
    found_required: required.filter(r => found.has(r)),
    missing_required: missing,
    extra_cookies: extra.map(c => c.name),
    cookies_with_expiry: withExpiry.length,
    cookies_expired: expired.length,
    cookies_no_expiry: noExpiry.length,
    earliest_expiry: earliestExpiry ? new Date(earliestExpiry).toISOString() : null,
    days_until_expiry: earliestExpiry ? Math.ceil((earliestExpiry - now) / (24*60*60*1000)) : null,
    is_valid: missing.length === 0 && platformCookies.length > 0
  };
}

function main() {
  const args = process.argv.slice(2);
  
  if (args.length < 2 || args.includes("--help") || args.includes("-h")) {
    printUsage();
  }
  
  const [platform, filePath] = args;
  const normalizedPlatform = platform.toLowerCase();
  
  if (!["tiktok", "instagram"].includes(normalizedPlatform)) {
    console.error(`Error: Platform must be 'tiktok' or 'instagram', got '${platform}'`);
    process.exit(1);
  }
  
  const resolvedPath = resolve(filePath);
  
  if (!existsSync(resolvedPath)) {
    console.error(`Error: File not found: ${resolvedPath}`);
    process.exit(1);
  }
  
  try {
    const parsed = parseCookieFile(resolvedPath);
    const validation = validateCookies(normalizedPlatform, parsed.cookies);
    
    console.log(`
╔══════════════════════════════════════════════════════════════╗
║  Cookie Validation Report                                    ║
╠══════════════════════════════════════════════════════════════╣
║  Platform:          ${validation.platform.padEnd(40)} ║
║  File Format:       ${parsed.format.padEnd(40)} ║
║  File Path:         ${resolvedPath.padEnd(40)} ║
╠══════════════════════════════════════════════════════════════╣
║  Total Cookies:     ${String(validation.total_cookies).padEnd(40)} ║
║  Platform Cookies:  ${String(validation.platform_cookies).padEnd(40)} ║
╠══════════════════════════════════════════════════════════════╣
║  Required Cookies:  ${validation.required_cookies.join(", ").padEnd(40)} ║
║  Found:             ${validation.found_required.join(", ").padEnd(40)} ║
║  Missing:           ${validation.missing_required.join(", ") || "NONE".padEnd(40)} ║
╠══════════════════════════════════════════════════════════════╣
║  With Expiry:       ${String(validation.cookies_with_expiry).padEnd(40)} ║
║  Expired:           ${String(validation.cookies_expired).padEnd(40)} ║
║  No Expiry (session): ${String(validation.cookies_no_expiry).padEnd(40)} ║
║  Earliest Expiry:   ${(validation.earliest_expiry || "Session cookies only").padEnd(40)} ║
║  Days Until Expiry: ${validation.days_until_expiry !== null ? String(validation.days_until_expiry) : "N/A (session)".padEnd(40)} ║
╠══════════════════════════════════════════════════════════════╣
║  STATUS:            ${(validation.is_valid ? "✅ VALID - Ready to use" : "❌ INVALID - Missing required cookies").padEnd(40)} ║
╚══════════════════════════════════════════════════════════════╝
`);
    
    if (validation.is_valid) {
      console.log(`
NEXT STEP:
  Use this path with the MCP:
  
  social_media.session.open_cookie_file({
    platform: "${normalizedPlatform}",
    cookie_file_path: "${resolvedPath}"
  })
`);
    } else {
      console.log(`
ISSUES TO FIX:
${validation.missing_required.map(m => `  - Missing required cookie: ${m}`).join("\n")}
${validation.cookies_expired > 0 ? `  - ${validation.cookies_expired} cookies already expired` : ""}
${validation.platform_cookies === 0 ? `  - No cookies found for ${normalizedPlatform} domains` : ""}

TIPS:
  - Make sure you're LOGGED IN when exporting
  - Export from the ROOT domain (tiktok.com, not www.tiktok.com)
  - Include ALL cookies for the domain, not just a few
  - Try a different export method (extension vs DevTools)
`);
      process.exit(1);
    }
  } catch (e) {
    console.error(`Error: ${e.message}`);
    process.exit(1);
  }
}

// Only run main when executed directly, not when imported
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}