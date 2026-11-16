#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

// Keep legacy Node invocations on the official Python gate.
const script = fileURLToPath(new URL("./check_commit.py", import.meta.url));
const result = spawnSync(process.env.PYTHON || "python", [script, ...process.argv.slice(2)], { stdio: "inherit" });
if (result.error) {
  console.error(`Cannot run the TLC gate: ${result.error.message}`);
  process.exit(2);
}
process.exit(result.status ?? 2);
