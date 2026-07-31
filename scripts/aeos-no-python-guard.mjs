#!/usr/bin/env node
import { readdirSync, statSync } from "node:fs";
import { join, relative, resolve } from "node:path";

const repoRoot = resolve(process.cwd());
const ignored = new Set([".git", "node_modules"]);
const blockedNames = new Set(["pyproject.toml", "pytest.ini", "behave.ini"]);

function walk(dir, files = []) {
  for (const item of readdirSync(dir)) {
    if (ignored.has(item)) continue;
    const full = join(dir, item);
    const stat = statSync(full);
    if (stat.isDirectory()) walk(full, files);
    else if (
      item.endsWith(".py") ||
      item.endsWith(".pyc") ||
      item.startsWith("requirements") ||
      blockedNames.has(item)
    ) {
      files.push(relative(repoRoot, full).replaceAll("\\", "/"));
    }
  }
  return files;
}

const blockers = walk(repoRoot);
const report = {
  policy: "AEOS WorkspaceSO is zero-Python. No *.py, *.pyc, pyproject.toml, pytest.ini, behave.ini or requirements files are allowed outside ignored dependency folders.",
  ignoredFolders: [...ignored],
  blockers,
  status: blockers.length ? "BLOCKED" : "PASS"
};

console.log(JSON.stringify(report, null, 2));
process.exit(blockers.length ? 1 : 0);
