#!/usr/bin/env node
import { existsSync, readdirSync, statSync } from "node:fs";
import { join, relative, resolve } from "node:path";

const repoRoot = resolve(process.cwd());
const ignored = new Set([".git", "node_modules", ".pytest_cache", "__pycache__", ".work"]);
const ignoredPrefixes = [".aeos/tmp"];
const metadataNames = new Set(["pyproject.toml", "pytest.ini", "behave.ini"]);

const requiredSkillScripts = [
  "skills/spec-driven/scripts/validate_spec.py",
  "skills/spec-driven/scripts/validate_tasks.py",
  "skills/spec-driven/scripts/validate_state.py",
  "skills/spec-driven/scripts/check_commit.py",
  "skills/spec-driven/scripts/lessons.py",
  "skills/spec-driven-lean/scripts/validate_plan.py",
  "skills/spec-driven-lean/scripts/validate_checks.py",
  "skills/spec-driven-lean/scripts/validate_verification.py",
  "skills/spec-driven-lean/scripts/check_commit.py",
  "skills/spec-driven-lean/scripts/lessons.py",
  "skills/spec-driven-lean/scripts/selftest.py",
  "skills/skill-architect/scripts/validate_skill.py",
  "skills/the-jury/scripts/tally.py",
  "skills/security-ownership-map/scripts/run_ownership_map.py",
  "skills/security-ownership-map/scripts/query_ownership.py",
  "skills/security-ownership-map/scripts/build_ownership_map.py",
  "skills/security-ownership-map/scripts/community_maintainers.py"
];

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
      metadataNames.has(item)
    ) {
      files.push(repoRelative(full));
    }
  }
  return files;
}

const inventory = walk(repoRoot).sort();
const missingSkillScripts = requiredSkillScripts.filter((file) => !existsSync(join(repoRoot, file)));
const blockers = missingSkillScripts.map((file) => `missing required Python skill script: ${file}`);

const report = {
  policy: "AEOS workspace allows Python. Skill-local *.py validators and Python project metadata are first-class. Kernel orchestration remains Node/TypeScript unless a later mission changes that surface.",
  policyRef: "references/PYTHON_WORKSPACE_POLICY.md",
  pythonAllowed: true,
  ignoredFolders: [...ignored, ...ignoredPrefixes],
  inventoryCount: inventory.length,
  inventory,
  missingSkillScripts,
  blockers,
  status: blockers.length ? "BLOCKED" : "PASS"
};

console.log(JSON.stringify(report, null, 2));
process.exit(blockers.length ? 1 : 0);
