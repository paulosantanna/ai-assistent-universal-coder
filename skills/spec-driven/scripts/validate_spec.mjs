#!/usr/bin/env node
import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import { join, resolve } from "node:path";

const REQUIRED_SECTIONS = ["Problem Statement", "Out of Scope", "Assumptions & Open Questions", "User Stories", "Requirement Traceability"];
const ID_RE = /^[A-Z][A-Z0-9]*-\d+$/;
const PLACEHOLDER_RE = /^\s*\[.+\]\s*$/;

function parseArgs(argv) {
  const args = { target: null, root: ".", strict: false };
  for (let i = 0; i < argv.length; i += 1) {
    if (argv[i] === "--root") args.root = argv[++i];
    else if (argv[i] === "--strict") args.strict = true;
    else if (!argv[i].startsWith("-") && !args.target) args.target = argv[i];
  }
  return args;
}

function autodetect(root) {
  const base = join(root, ".specs", "features");
  if (!existsSync(base) || !statSync(base).isDirectory()) return null;
  const features = readdirSync(base).filter((d) => existsSync(join(base, d, "spec.md"))).sort();
  if (features.length === 1) return join(base, features[0], "spec.md");
  if (features.length === 0) return null;
  console.error(`validate_spec: multiple features found; pass one explicitly:\n  ${features.map((f) => join(base, f, "spec.md")).join("\n  ")}`);
  process.exit(2);
}

function resolveSpec(target, root) {
  if (!target) return autodetect(root);
  if (existsSync(target) && statSync(target).isFile()) return target;
  if (existsSync(target) && statSync(target).isDirectory()) {
    const cand = join(target, "spec.md");
    return existsSync(cand) ? cand : autodetect(target);
  }
  const cand = join(root, ".specs", "features", target, "spec.md");
  return existsSync(cand) ? cand : null;
}

function splitRow(line) {
  return line.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((c) => c.trim());
}

function isSeparator(line) {
  return /^\s*\|?[\s:|-]+\|?\s*$/.test(line) && line.includes("-");
}

function sectionBounds(lines, name) {
  let start = null;
  const heading = new RegExp(`^#{1,3}\\s+${name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\s*$`);
  for (let i = 0; i < lines.length; i += 1) {
    if (heading.test(lines[i].trim())) {
      start = i + 1;
      break;
    }
  }
  if (start === null) return null;
  let end = lines.length;
  for (let j = start; j < lines.length; j += 1) {
    if (/^#{1,3}\s+\S/.test(lines[j])) {
      end = j;
      break;
    }
  }
  return [start, end];
}

function classifyEars(text) {
  const low = text.trim().toLowerCase();
  if (!/\bshall\b/.test(low)) return [false, "no SHALL"];
  const kws = [];
  if (/\bwhile\b/.test(low)) kws.push("WHILE");
  if (/\bwhen\b/.test(low)) kws.push("WHEN");
  if (/^\s*if\b/.test(low) || /\bif\b.*\bthen\b/.test(low)) kws.push("IF/THEN");
  if (/\bwhere\b/.test(low)) kws.push("WHERE");
  if (kws.length >= 2) return [true, `complex (${kws.join("+")})`];
  if (kws.length) {
    return [true, { WHILE: "state-driven", WHEN: "event-driven", "IF/THEN": "unwanted-behavior", WHERE: "optional-feature" }[kws[0]]];
  }
  if (/^\s*the\b/.test(low)) return [true, "ubiquitous"];
  return [true, "warn: SHALL present but no EARS lead keyword"];
}

function check(specPath) {
  const lines = readFileSync(specPath, "utf8").split(/\r?\n/);
  const errors = [];
  const warnings = [];
  for (const name of REQUIRED_SECTIONS) {
    if (!sectionBounds(lines, name)) errors.push(`missing required section: ## ${name}`);
  }
  let inAc = false;
  lines.forEach((ln, idx) => {
    const stripped = ln.trim();
    if (/^\*{0,2}Acceptance Criteria\*{0,2}\s*:?\s*$/.test(stripped)) {
      inAc = true;
      return;
    }
    if (!inAc) return;
    const itemMatch = /^\s*\d+\.\s+(.*)$/.exec(ln);
    if (itemMatch) {
      const item = itemMatch[1].trim();
      if (PLACEHOLDER_RE.test(item)) return;
      const [ok, note] = classifyEars(item);
      if (!ok) errors.push(`L${idx + 1}: acceptance criterion has no SHALL (not testable): ${item.slice(0, 70)}`);
      else if (note.startsWith("warn")) {
        warnings.push(`L${idx + 1}: AC has SHALL but no EARS keyword (WHEN/WHILE/WHERE/IF or ubiquitous 'The … shall'): ${item.slice(0, 60)}`);
      }
    } else if (stripped === "" || /^#{1,3}\s/.test(ln) || stripped.startsWith("**")) {
      inAc = false;
    }
  });
  const assumptions = sectionBounds(lines, "Assumptions & Open Questions");
  if (assumptions) {
    const rows = lines.slice(...assumptions).filter((ln) => ln.trim().startsWith("|") && !isSeparator(ln)).slice(1);
    let templateSeen = false;
    for (const row of rows) {
      const cells = splitRow(row);
      if (cells.length < 3) continue;
      const [assumption, chosen, rationale] = cells;
      if (PLACEHOLDER_RE.test(assumption) && PLACEHOLDER_RE.test(chosen)) {
        templateSeen = true;
        continue;
      }
      if (!chosen || PLACEHOLDER_RE.test(chosen)) errors.push(`assumption '${assumption.slice(0, 40)}' has empty 'Chosen default'`);
      if (!rationale || PLACEHOLDER_RE.test(rationale)) errors.push(`assumption '${assumption.slice(0, 40)}' has empty 'Rationale'`);
    }
    if (templateSeen) warnings.push("Assumptions table still contains template placeholder rows");
    const oq = lines.slice(...assumptions).filter((ln) => ln.toLowerCase().includes("open questions"));
    const oqClean = oq.join(" ").replace(/[*_]/g, "").toLowerCase();
    if (!oq.length) warnings.push("no 'Open questions:' line in Assumptions section");
    else if (!/open questions.*:\s*none/.test(oqClean)) warnings.push("open questions do not read as resolved ('Open questions: none')");
  }
  const trace = sectionBounds(lines, "Requirement Traceability");
  if (trace) {
    const rows = lines.slice(...trace).filter((ln) => ln.trim().startsWith("|") && !isSeparator(ln)).slice(1);
    let templateSeen = false;
    let realIds = 0;
    for (const row of rows) {
      const cells = splitRow(row);
      if (!cells.length) continue;
      const rid = cells[0];
      if (PLACEHOLDER_RE.test(rid) || rid.includes("[")) {
        templateSeen = true;
        continue;
      }
      if (!rid) continue;
      if (!ID_RE.test(rid)) errors.push(`malformed requirement ID: '${rid}' (expected e.g. AUTH-01)`);
      else realIds += 1;
    }
    if (templateSeen && realIds === 0) warnings.push("Requirement Traceability has only template rows (no real IDs yet)");
  }
  return { errors, warnings };
}

const args = parseArgs(process.argv.slice(2));
const spec = resolveSpec(args.target, resolve(args.root));
if (!spec) {
  console.error("validate_spec: could not locate a spec.md. Pass a path or run from the project root.");
  process.exit(2);
}
const { errors, warnings } = check(spec);
for (const warning of warnings) console.log(`  WARN  ${warning}`);
for (const error of errors) console.log(`  ERROR ${error}`);
console.log(`\nvalidate_spec: ${errors.length} error(s), ${warnings.length} warning(s) in ${spec}`);
process.exit(errors.length || (warnings.length && args.strict) ? 1 : 0);
