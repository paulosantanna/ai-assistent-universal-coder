#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const successor = join(here, "aeos-python-workspace-guard.mjs");
const result = spawnSync(process.execPath, [successor, ...process.argv.slice(2)], {
  stdio: "inherit"
});

process.exit(result.status ?? 1);
