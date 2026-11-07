import { existsSync, readFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

export function resolveOpenCodeConfigPath() {
  if (process.env.OPENCODE_CONFIG_PATH) return process.env.OPENCODE_CONFIG_PATH;
  const candidates = [
    join(homedir(), ".config", "opencode", "config.json"),
    join(homedir(), ".opencode", "config.json"),
    join(homedir(), "AppData", "Roaming", "opencode", "config.json"),
  ];
  return candidates.find((p) => existsSync(p));
}

/** Lê overrides não secretos do OpenCode (modelo, perfil). */
export function loadOpenCodeHints() {
  const path = resolveOpenCodeConfigPath();
  if (!path) return { path: null, hints: {} };
  try {
    const json = JSON.parse(readFileSync(path, "utf8"));
    return {
      path,
      hints: {
        model: json.model ?? json.defaultModel ?? json.llm?.model,
        provider: json.provider ?? json.llm?.provider,
        profile: json.profile,
      },
    };
  } catch {
    return { path, hints: {}, parse_error: true };
  }
}
