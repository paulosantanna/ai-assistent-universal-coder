#!/usr/bin/env node
import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import { basename, join, resolve } from "node:path";

const EVIDENCE_RE = /[\w./-]+\.[A-Za-z0-9]+:\d+/;

function parseArgs(argv) {
  const args = { feature: null, root: "." };
  for (let i = 0; i < argv.length; i += 1) {
    if (argv[i] === "--root") args.root = argv[++i];
    else if (!argv[i].startsWith("-") && !args.feature) args.feature = argv[i];
  }
  return args;
}

function featureDirs(root) {
  const base = join(root, ".specs", "features");
  if (!existsSync(base) || !statSync(base).isDirectory()) return { base, dirs: [] };
  return { base, dirs: readdirSync(base).filter((d) => statSync(join(base, d)).isDirectory()).sort() };
}

function verdict(text) {
  const lines = text.split(/\r?\n/);
  const candidates = lines.filter((ln) => /^#{1,4}\s*validation\b/i.test(ln.trim()) || /\*{0,2}result\*{0,2}\s*:/i.test(ln.trim()));
  const hay = candidates.length ? candidates.join(" ") : text;
  const hasPass = /\bPASS\b/.test(hay);
  const hasFail = /\bFAIL\b/.test(hay);
  if (hasPass && hasFail) return "unfilled";
  if (hasPass) return "pass";
  if (hasFail) return "fail";
  return null;
}

function appearsComplete(fdir) {
  if (existsSync(join(fdir, "validation.md"))) return true;
  const tasks = join(fdir, "tasks.md");
  if (!existsSync(tasks)) return false;
  const body = readFileSync(tasks, "utf8");
  if (!/^#{2,4}\s+T\d+\s*:/m.test(body)) return false;
  if (/^\s*-\s*\[\s\]/m.test(body)) return false;
  return true;
}

function checkFeature(fdir, name) {
  const errors = [];
  const vpath = join(fdir, "validation.md");
  if (!existsSync(vpath)) {
    errors.push(`${name}: no validation.md - Execute is not done until the Verifier writes it (author != verifier). Dispatch validation before marking done.`);
    return errors;
  }
  const text = readFileSync(vpath, "utf8");
  const result = verdict(text);
  if (result === null) errors.push(`${name}: validation.md has no PASS/FAIL verdict (a prose-only report does not count)`);
  else if (result === "unfilled") errors.push(`${name}: validation.md verdict is still the template placeholder '[PASS | FAIL]' - not filled`);
  else if (result === "fail") errors.push(`${name}: validation.md verdict is FAIL - route the ranked gaps to fix tasks, then re-verify (feature is not done)`);
  if (result === "pass" && !EVIDENCE_RE.test(text)) {
    errors.push(`${name}: validation.md is PASS but cites no file:line evidence - evidence-or-zero not satisfied`);
  }
  return errors;
}

function resolveTargets(root, feature) {
  const { base, dirs } = featureDirs(root);
  if (feature) {
    const fdir = existsSync(feature) && statSync(feature).isDirectory() ? feature : join(base, feature);
    if (!existsSync(fdir) || !statSync(fdir).isDirectory()) {
      console.error(`validate_state: feature not found: ${feature}`);
      process.exit(2);
    }
    return [[fdir, basename(fdir)]];
  }
  if (!existsSync(base) || !statSync(base).isDirectory()) {
    console.log(`validate_state: no ${base} directory - nothing to check.`);
    return [];
  }
  if (dirs.length === 1) return [[join(base, dirs[0]), dirs[0]]];
  if (!dirs.length) {
    console.log("validate_state: no features under .specs/features/ - nothing to check.");
    return [];
  }
  const picked = dirs.filter((d) => appearsComplete(join(base, d))).map((d) => [join(base, d), d]);
  if (!picked.length) console.log("validate_state: no completed feature detected (all in progress) - nothing to gate.");
  return picked;
}

const args = parseArgs(process.argv.slice(2));
const targets = resolveTargets(resolve(args.root), args.feature);
const allErrors = targets.flatMap(([fdir, name]) => checkFeature(fdir, name));
for (const error of allErrors) console.log(`  ERROR ${error}`);
const checked = targets.map(([, name]) => name).join(", ") || "(none)";
console.log(`\nvalidate_state: ${allErrors.length} error(s) across [${checked}]`);
process.exit(allErrors.length ? 1 : 0);
