#!/usr/bin/env node
import { readdirSync, statSync } from "node:fs";
import { join, relative, resolve } from "node:path";

const repoRoot = resolve(process.cwd());
const ignored = new Set([".git", "node_modules", ".pytest_cache", "__pycache__", ".aeos"]);
const legacyAllowedRoots = [
  "aeos",
  "features",
  "java-bug-solver",
  "skills",
  "unsloth_compiled_cache",
  "references/legacy-python",
  "playbooks/aeos_improve",
  "medical-research-mcp",
  "continuous-training-mcp",
  "complete-docs-mcp",
  "language-docs-mcp",
  "universal-project-mcp",
  "packages/aeos-language-server",
  "src/aeos_workbench",
  "conftest.py"
];

function walk(dir, files = []) {
  for (const item of readdirSync(dir)) {
    if (ignored.has(item)) continue;
    const full = join(dir, item);
    const stat = statSync(full);
    if (stat.isDirectory()) walk(full, files);
    else if (item.endsWith(".py")) files.push(relative(repoRoot, full).replaceAll("\\", "/"));
  }
  return files;
}

function isLegacyAllowed(path) {
  return legacyAllowedRoots.some((root) => path === root || path.startsWith(`${root}/`));
}

const pythonFiles = walk(repoRoot);
const activeBlockers = pythonFiles.filter((path) => !isLegacyAllowed(path));
const report = {
  policy: "AEOS active runtime must not introduce or depend on Python orchestration. Existing Python is retired legacy inventory until ported or archived.",
  totalPythonFiles: pythonFiles.length,
  legacyAllowed: pythonFiles.length - activeBlockers.length,
  activeBlockers,
  status: activeBlockers.length ? "BLOCKED" : "PASS"
};

console.log(JSON.stringify(report, null, 2));
process.exit(activeBlockers.length ? 1 : 0);
