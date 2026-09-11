#!/usr/bin/env node
import { readFileSync } from "node:fs";

const AUTH_REVOKED_CODES = new Set([
  "token_revoked",
  "invalid_grant",
  "unauthorized_client",
]);

const FORBIDDEN_RECOVERY_PATTERNS = [
  /extract(?:ing|ion)?\s+(?:oauth\s+)?(?:token|cookie|credential)/i,
  /(?:token|cookie|credential)\s+extract(?:ing|ion)?/i,
  /cookie\s+dump/i,
  /browser\s+storage\s+(?:token|cookie|credential)/i,
  /persist\s+(?:oauth\s+)?(?:token|cookie|credential)/i,
];

function parseArgs(argv) {
  const args = { logFile: null, strict: false };
  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (value === "--log-file") {
      args.logFile = argv[index + 1] ?? null;
      index += 1;
    } else if (value === "--strict") {
      args.strict = true;
    } else if (value === "--help" || value === "-h") {
      args.help = true;
    }
  }
  return args;
}

function readInput(logFile) {
  if (logFile) {
    return readFileSync(logFile, "utf8");
  }

  if (!process.stdin.isTTY) {
    return readFileSync(0, "utf8");
  }

  return "";
}

function detectAuthRevocation(text) {
  const lowerText = text.toLowerCase();
  const matchedCode = [...AUTH_REVOKED_CODES].find((code) => lowerText.includes(code));
  const mentionsCodexApps = /codex[_-]apps/i.test(text);
  const mentionsOauth = /oauth|http\s*401|unauthorized/i.test(text);

  if (!matchedCode || (!mentionsCodexApps && !mentionsOauth)) {
    return null;
  }

  return {
    connector: mentionsCodexApps ? "codex_apps" : "external_mcp_connector",
    code: matchedCode,
  };
}

function detectForbiddenRecovery(text) {
  return FORBIDDEN_RECOVERY_PATTERNS
    .filter((pattern) => pattern.test(text))
    .map((pattern) => pattern.source);
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    console.log([
      "Usage: node scripts/aeos-codex-apps-oauth-guard.mjs [--log-file <path>] [--strict]",
      "",
      "Classifies revoked OAuth failures for external Codex Apps MCP connectors.",
      "This guard never extracts, stores, or repairs credentials.",
    ].join("\n"));
    return 0;
  }

  const input = readInput(args.logFile);
  const forbiddenRecovery = detectForbiddenRecovery(input);
  const authRevocation = detectAuthRevocation(input);

  if (forbiddenRecovery.length > 0) {
    console.error(JSON.stringify({
      status: "blocked",
      reason: "forbidden_credential_recovery",
      matched_patterns: forbiddenRecovery,
      remediation: "Do not extract cookies, tokens, or credentials. Reconnect the app through the approved connector UI.",
    }, null, 2));
    return 2;
  }

  if (authRevocation) {
    const result = {
      status: "blocked_external_auth",
      connector: authRevocation.connector,
      code: authRevocation.code,
      fail_soft: true,
      secret_material_accessed: false,
      remediation: [
        "Reconnect the affected app/account in Codex or ChatGPT connectors.",
        "Rerun the MCP health check after reconnection.",
        "Keep tokens, cookies, and passwords out of repository files and logs.",
      ],
    };
    console.log(JSON.stringify(result, null, 2));
    return args.strict ? 1 : 0;
  }

  console.log(JSON.stringify({
    status: "ok",
    connector: "codex_apps",
    auth_revocation_detected: false,
    secret_material_accessed: false,
  }, null, 2));
  return 0;
}

process.exitCode = main();
