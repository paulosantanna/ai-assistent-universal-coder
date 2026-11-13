import { appendFileSync, mkdirSync, existsSync } from "node:fs";
import { dirname } from "node:path";
import { paths } from "./paths.mjs";
import { appendTranscript } from "./memory-layers.mjs";

const ALLOWED_TOOLS = new Set([
  "cursor",
  "codex",
  "opencode",
  "claude",
  "copilot",
  "windsurf",
  "trae",
  "kiro",
  "agent",
  "cli",
  "unknown",
]);

export function recordEvent({
  tool = "unknown",
  action,
  paths: filePaths = [],
  summary = "",
  meta = {},
}) {
  const p = paths();
  const toolId = ALLOWED_TOOLS.has(String(tool).toLowerCase()) ? String(tool).toLowerCase() : "unknown";
  const event = {
    ts: new Date().toISOString(),
    tool: toolId,
    action: String(action || "change"),
    paths: filePaths.map(String),
    summary: String(summary).slice(0, 2000),
    meta,
  };
  const file = p.events;
  const dir = dirname(file);
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  appendFileSync(file, JSON.stringify(event) + "\n", "utf8");
  appendTranscript({ kind: "tool_event", ...event });
  return event;
}
