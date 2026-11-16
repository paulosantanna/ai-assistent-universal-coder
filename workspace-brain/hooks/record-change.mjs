#!/usr/bin/env node
/**
 * Hook para IDE/CLI: node hooks/record-change.mjs --tool cursor --paths a.ts,b.ts --summary "..."
 */
import { recordEvent } from "../src/events.mjs";
import { ensureLayout } from "../src/paths.mjs";

const args = process.argv.slice(2);
const flags = { tool: "unknown", action: "change", paths: [], summary: "" };
for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a === "--tool") flags.tool = args[++i];
  else if (a === "--action") flags.action = args[++i];
  else if (a === "--paths") flags.paths = args[++i].split(",").map((s) => s.trim()).filter(Boolean);
  else if (a === "--summary") flags.summary = args[++i];
}

ensureLayout();
console.log(JSON.stringify(recordEvent(flags)));
