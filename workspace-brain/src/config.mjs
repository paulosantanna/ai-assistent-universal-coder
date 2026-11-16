import { existsSync, readFileSync } from "node:fs";
import { homedir, platform } from "node:os";
import { join, resolve } from "node:path";

const isWin = platform() === "win32";

export function defaultBrainRoot() {
  if (process.env.WORKSPACE_BRAIN_ROOT) return resolve(process.env.WORKSPACE_BRAIN_ROOT);
  if (isWin) return "E:\\Github\\workspace-brain";
  return join(homedir(), "workspace-brain");
}

export function defaultJevDir() {
  if (process.env.JEV_CONFIG_DIR) return resolve(process.env.JEV_CONFIG_DIR);
  if (isWin) return "E:\\JEV";
  return join(homedir(), ".jev");
}

export function loadDotEnvFile(dir) {
  const path = join(dir, ".env");
  if (!existsSync(path)) return;
  for (const line of readFileSync(path, "utf8").split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const eq = trimmed.indexOf("=");
    if (eq < 1) continue;
    const key = trimmed.slice(0, eq).trim();
    let val = trimmed.slice(eq + 1).trim();
    if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
      val = val.slice(1, -1);
    }
    if (process.env[key] === undefined) process.env[key] = val;
  }
}

/** Lê o primeiro ficheiro existente com uma única linha de chave (sem logar valor). */
export function readSecretFromDir(dir, names) {
  for (const name of names) {
    const path = join(dir, name);
    if (!existsSync(path)) continue;
    const line = readFileSync(path, "utf8").split(/\r?\n/).find((l) => l.trim() && !l.trim().startsWith("#"));
    if (line) return line.trim();
  }
  return undefined;
}

export function getDeepSeekApiKey() {
  if (process.env.DEEPSEEK_API_KEY) return process.env.DEEPSEEK_API_KEY;
  const jev = defaultJevDir();
  return (
    readSecretFromDir(jev, ["deepseek.key", "deepseek_api_key.txt", "api_key.txt"]) ??
    readSecretFromDir(defaultBrainRoot(), [".deepseek.key"])
  );
}

export function getTypesafeApiKey() {
  if (process.env.TYPESAFE_API_KEY) return process.env.TYPESAFE_API_KEY;
  return readSecretFromDir(defaultJevDir(), [
    "typesafe.key",
    "typesafe_api_key.txt",
    "jev.key",
    "api_key.txt",
  ]);
}

export function getModelContract(brainRoot) {
  const path = join(brainRoot, "manifests", "model-contract.json");
  if (existsSync(path)) {
    return JSON.parse(readFileSync(path, "utf8"));
  }
  return {
    provider: "deepseek",
    chat_model: process.env.DEEPSEEK_CHAT_MODEL || "deepseek-chat",
    embedding_model: null,
    opencode_profile: "default",
    base_url: process.env.DEEPSEEK_BASE_URL || "https://api.deepseek.com",
  };
}

export function resolveUniversalCoderRoot() {
  if (process.env.UNIVERSAL_CODER_ROOT) return resolve(process.env.UNIVERSAL_CODER_ROOT);
  return undefined;
}

export function packageRoot() {
  return resolve(import.meta.dirname, "..");
}
