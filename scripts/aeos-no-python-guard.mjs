#!/usr/bin/env node
import { readdirSync, statSync } from "node:fs";
import { join, relative, resolve } from "node:path";

const repoRoot = resolve(process.cwd());
const ignored = new Set([".git", "node_modules", ".pytest_cache", "__pycache__"]);
const ignoredPrefixes = [".aeos/tmp"];
const blockedNames = new Set(["pyproject.toml", "pytest.ini", "behave.ini"]);

function repoRelative(filePath) {
  return relative(repoRoot, filePath).replaceAll("\\", "/");
}

function isIgnoredPath(filePath) {
  const rel = repoRelative(filePath);
  return ignoredPrefixes.some((prefix) => rel === prefix || rel.startsWith(`${prefix}/`));
}

function walk(dir, files = []) {
  if (isIgnoredPath(dir)) return files;

  let entries;
  try {
    entries = readdirSync(dir);
  } catch (error) {
    if (error && (error.code === "EACCES" || error.code === "EPERM")) return files;
    throw error;
  }

  for (const item of entries) {
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
      files.push(repoRelative(full));
    }
  }
  return files;
}

const blockers = walk(repoRoot);
const report = {
  policy: "AEOS WorkspaceSO is zero-Python. No *.py, *.pyc, pyproject.toml, pytest.ini, behave.ini or requirements files are allowed outside ignored dependency and runtime-cache folders.",
  ignoredFolders: [...ignored, ...ignoredPrefixes],
  blockers,
  status: blockers.length ? "BLOCKED" : "PASS"
};

console.log(JSON.stringify(report, null, 2));
process.exit(blockers.length ? 1 : 0);
