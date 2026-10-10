/**
 * Tests for Social Media Session Manager
 */

import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import { 
  parseCookies, 
  filterPlatformCookies, 
  hasValidSessionCookies,
  normalizeHost,
  cookieMatchesPlatform,
  PLATFORMS,
  getLoginInstructions
} from "./session-manager.mjs";

describe("Social Media Session Manager", () => {
  
  describe("normalizeHost", () => {
    it("normalizes domains correctly", () => {
      expect(normalizeHost(".tiktok.com")).toBe("tiktok.com");
      expect(normalizeHost("TIKTOK.COM")).toBe("tiktok.com");
      expect(normalizeHost("  .instagram.com  ")).toBe("instagram.com");
    });
  });

  describe("cookieMatchesPlatform", () => {
    it("matches TikTok cookies", () => {
      const tiktok = PLATFORMS.tiktok;
      expect(cookieMatchesPlatform(".tiktok.com", tiktok)).toBe(true);
      expect(cookieMatchesPlatform("tiktok.com", tiktok)).toBe(true);
      expect(cookieMatchesPlatform("www.tiktok.com", tiktok)).toBe(true);
      expect(cookieMatchesPlatform("google.com", tiktok)).toBe(false);
    });

    it("matches Instagram cookies", () => {
      const instagram = PLATFORMS.instagram;
      expect(cookieMatchesPlatform(".instagram.com", instagram)).toBe(true);
      expect(cookieMatchesPlatform("instagram.com", instagram)).toBe(true);
      expect(cookieMatchesPlatform(".facebook.com", instagram)).toBe(true);
      expect(cookieMatchesPlatform("tiktok.com", instagram)).toBe(false);
    });
  });

  describe("parseCookies", () => {
    it("parses JSON array format", () => {
      const input = [
        { name: "sessionid", value: "abc123", domain: ".tiktok.com", path: "/", secure: true },
        { name: "tt_webid", value: "xyz789", domain: "tiktok.com", path: "/", secure: true }
      ];
      const result = parseCookies(input, PLATFORMS.tiktok);
      expect(result.length).toBe(2);
      expect(result[0].name).toBe("sessionid");
      expect(result[0].domain).toBe("tiktok.com");
    });

    it("parses Chrome DevTools Protocol format", () => {
      const input = {
        cookies: [
          { name: "sessionid", value: "abc123", domain: ".instagram.com", path: "/", secure: true }
        ]
      };
      const result = parseCookies(input, PLATFORMS.instagram);
      expect(result.length).toBe(1);
      expect(result[0].name).toBe("sessionid");
    });

    it("filters out non-platform cookies", () => {
      const input = [
        { name: "sessionid", value: "abc123", domain: ".tiktok.com", path: "/", secure: true },
        { name: "GA_ID", value: "ga123", domain: ".google.com", path: "/", secure: true },
        { name: "tt_webid", value: "xyz789", domain: "tiktok.com", path: "/", secure: true }
      ];
      const result = parseCookies(input, PLATFORMS.tiktok);
      expect(result.length).toBe(2);
      expect(result.every(c => c.domain.includes("tiktok"))).toBe(true);
    });

    it("handles missing fields gracefully", () => {
      const input = [
        { name: "sessionid", value: "abc123" }, // missing domain
        { domain: ".tiktok.com" }, // missing name
        { name: "tt_webid", value: "xyz789", domain: ".tiktok.com", path: "/", secure: true }
      ];
      const result = parseCookies(input, PLATFORMS.tiktok);
      expect(result.length).toBe(1);
      expect(result[0].name).toBe("tt_webid");
    });
  });

  describe("filterPlatformCookies", () => {
    it("filters cookies for platform", () => {
      const cookies = [
        { name: "a", domain: ".tiktok.com", value: "1" },
        { name: "b", domain: ".google.com", value: "2" },
        { name: "c", domain: "tiktok.com", value: "3" }
      ];
      const result = filterPlatformCookies(cookies, PLATFORMS.tiktok);
      expect(result.length).toBe(2);
    });
  });

  describe("hasValidSessionCookies", () => {
    it("detects valid TikTok session", () => {
      const cookies = [
        { name: "sessionid", value: "abc", domain: ".tiktok.com" },
        { name: "tt_webid", value: "def", domain: "tiktok.com" },
        { name: "s_v_web_id", value: "ghi", domain: ".tiktok.com" }
      ];
      expect(hasValidSessionCookies(cookies, PLATFORMS.tiktok)).toBe(true);
    });

    it("detects missing required cookies", () => {
      const cookies = [
        { name: "sessionid", value: "abc", domain: ".tiktok.com" }
        // missing tt_webid, s_v_web_id
      ];
      expect(hasValidSessionCookies(cookies, PLATFORMS.tiktok)).toBe(false);
    });

    it("detects valid Instagram session", () => {
      const cookies = [
        { name: "sessionid", value: "abc", domain: ".instagram.com" },
        { name: "csrftoken", value: "def", domain: "instagram.com" },
        { name: "ds_user_id", value: "ghi", domain: ".instagram.com" }
      ];
      expect(hasValidSessionCookies(cookies, PLATFORMS.instagram)).toBe(true);
    });
  });

  describe("getLoginInstructions", () => {
    it("returns TikTok instructions", () => {
      const inst = getLoginInstructions("tiktok");
      expect(inst.platform).toBe("tiktok");
      expect(inst.platform_name).toBe("TikTok");
      expect(inst.login_url).toBe("https://www.tiktok.com/login");
      expect(inst.required_cookies).toContain("sessionid");
      expect(inst.required_cookies).toContain("tt_webid");
    });

    it("returns Instagram instructions", () => {
      const inst = getLoginInstructions("instagram");
      expect(inst.platform).toBe("instagram");
      expect(inst.platform_name).toBe("Instagram");
      expect(inst.login_url).toBe("https://www.instagram.com/accounts/login/");
      expect(inst.required_cookies).toContain("sessionid");
      expect(inst.required_cookies).toContain("csrftoken");
    });

    it("throws for unknown platform", () => {
      expect(() => getLoginInstructions("unknown")).toThrow("Unknown platform");
    });
  });

  describe("PLATFORMS config", () => {
    it("has correct TikTok config", () => {
      const t = PLATFORMS.tiktok;
      expect(t.name).toBe("TikTok");
      expect(t.loginUrl).toBe("https://www.tiktok.com/login");
      expect(t.requiredCookies).toEqual(["sessionid", "tt_webid", "s_v_web_id"]);
      expect(t.cookieDomains).toContain(".tiktok.com");
    });

    it("has correct Instagram config", () => {
      const i = PLATFORMS.instagram;
      expect(i.name).toBe("Instagram");
      expect(i.loginUrl).toBe("https://www.instagram.com/accounts/login/");
      expect(i.requiredCookies).toEqual(["sessionid", "csrftoken", "ds_user_id"]);
      expect(i.cookieDomains).toContain(".instagram.com");
      expect(i.cookieDomains).toContain(".facebook.com");
    });
  });
});

describe("Integration: Cookie Export Helper", () => {
  let parseNetscape;
  
  beforeEach(async () => {
    const mod = await import("./export-helper.js");
    parseNetscape = mod.parseNetscape;
  });
  
  it("parses Netscape format", () => {
    const netscape = `# Netscape HTTP Cookie File
.tiktok.com	TRUE	/	TRUE	1735689600	sessionid	abc123
.tiktok.com	TRUE	/	TRUE	1735689600	tt_webid	xyz789
.google.com	TRUE	/	FALSE	0	GA_ID	ga123
`;
    const result = parseNetscape(netscape);
    expect(result.length).toBe(3);
    expect(result[0].name).toBe("sessionid");
    expect(result[0].domain).toBe(".tiktok.com");
    expect(result[0].expiresAtMs).toBe(1735689600000);
  });

  it("handles comments and empty lines", () => {
    const netscape = `
# Comment
.tiktok.com	TRUE	/	TRUE	1735689600	sessionid	abc123

# Another comment
`;
    const result = parseNetscape(netscape);
    expect(result.length).toBe(1);
  });
});