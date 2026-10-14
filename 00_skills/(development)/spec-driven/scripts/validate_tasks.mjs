#!/usr/bin/env node
import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import { join, resolve } from "node:path";

const REQUIRED_SECTIONS = ["Test Coverage Matrix", "Gate Check Commands", "Execution Plan", "Task Breakdown"];
const TASK_RE = /^#{2,4}\s+(T\d+)\s*:/i;
const EDGE_RE = /\bT\d+\b/g;
const FILE_HINT_RE = /[\w./-]+\.\w{1,6}\b/g;

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
  const features = readdirSync(base).filter((d) => existsSync(join(base, d, "tasks.md"))).sort();
  if (features.length === 1) return join(base, features[0], "tasks.md");
  if (features.length === 0) return null;
  console.error(`validate_tasks: multiple features found; pass one explicitly:\n  ${features.map((f) => join(base, f, "tasks.md")).join("\n  ")}`);
  process.exit(2);
}

function resolveTasks(target, root) {
  if (!target) return autodetect(root);
  if (existsSync(target) && statSync(target).isFile()) return target;
  if (existsSync(target) && statSync(target).isDirectory()) {
    const cand = join(target, "tasks.md");
    return existsSync(cand) ? cand : autodetect(target);
  }
  const cand = join(root, ".specs", "features", target, "tasks.md");
  return existsSync(cand) ? cand : null;
}

function sectionPresent(lines, name) {
  const re = new RegExp(`^#{1,4}\\s+${name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\b`);
  return lines.some((ln) => re.test(ln.trim()));
}

function parseTasks(lines) {
  const tasks = {};
  let current = null;
  for (const ln of lines) {
    const header = TASK_RE.exec(ln.trim());
    if (header) {
      current = header[1].toUpperCase();
      tasks[current] = { deps: new Set(), tests: null, gate: null, where: "" };
      continue;
    }
    if (!current) continue;
    const stripped = ln.trim();
    const dep = /^\*{0,2}Depends on\*{0,2}\s*:\s*(.*)$/i.exec(stripped);
    if (dep && !dep[1].toLowerCase().includes("none")) {
      for (const edge of dep[1].toUpperCase().match(EDGE_RE) ?? []) tasks[current].deps.add(edge);
    }
    const where = /^\*{0,2}Where\*{0,2}\s*:\s*(.*)$/i.exec(stripped);
    if (where) tasks[current].where = where[1];
    const tests = /^\*{0,2}Tests\*{0,2}\s*:\s*(.*)$/i.exec(stripped);
    if (tests) tasks[current].tests = tests[1].trim();
    const gate = /^\*{0,2}Gate\*{0,2}\s*:\s*(.*)$/i.exec(stripped);
    if (gate) tasks[current].gate = gate[1].trim();
  }
  return tasks;
}

function parsePhaseMembership(lines) {
  const membership = {};
  let phaseIdx = 0;
  let inPhase = false;
  for (const ln of lines) {
    const phase = /^#{2,4}\s+Phase\s+(\d+)/i.exec(ln.trim());
    if (phase) {
      phaseIdx = Number(phase[1]);
      inPhase = true;
      continue;
    }
    if (!inPhase) continue;
    const header = TASK_RE.exec(ln.trim());
    if (header) membership[header[1].toUpperCase()] = phaseIdx;
  }
  return membership;
}

function parseDiagramEdges(lines) {
  const edges = new Set();
  let inFence = false;
  let found = false;
  for (const ln of lines) {
    if (ln.trim().startsWith("```")) {
      inFence = !inFence;
      continue;
    }
    if (!inFence) continue;
    const norm = ln.replaceAll("→", "->");
    if (!norm.includes("->")) continue;
    const seq = norm.split("->").map((seg) => {
      const ids = seg.toUpperCase().match(EDGE_RE) ?? [];
      return ids.length ? ids[ids.length - 1] : null;
    });
    for (let i = 0; i < seq.length - 1; i += 1) {
      if (seq[i] && seq[i + 1]) {
        edges.add(`${seq[i]}->${seq[i + 1]}`);
        found = true;
      }
    }
  }
  return { edges, found };
}

function check(path) {
  const lines = readFileSync(path, "utf8").split(/\r?\n/);
  const errors = [];
  const warnings = [];
  for (const name of REQUIRED_SECTIONS) {
    if (!sectionPresent(lines, name)) errors.push(`missing required section: ## ${name}`);
  }
  const tasks = parseTasks(lines);
  if (!Object.keys(tasks).length) {
    warnings.push("no tasks (### T1: ...) parsed - is this file filled in?");
    return { errors, warnings };
  }
  for (const [tid, task] of Object.entries(tasks)) {
    if (task.tests === null) errors.push(`${tid}: missing \`Tests\` field`);
    else if (task.tests.toLowerCase().startsWith("none")) {
      warnings.push(`${tid}: Tests: none - confirm the Test Coverage Matrix says 'none' for this layer`);
    }
    if (task.gate === null) errors.push(`${tid}: missing \`Gate\` field`);
    const files = [...new Set(task.where.match(FILE_HINT_RE) ?? [])];
    if (files.length > 1) warnings.push(`${tid}: \`Where\` names multiple files ${files.sort().join(", ")} - granularity smell, consider splitting`);
  }
  const membership = parsePhaseMembership(lines);
  for (const [tid, task] of Object.entries(tasks)) {
    const here = membership[tid];
    if (here === undefined) continue;
    for (const dep of task.deps) {
      const depPhase = membership[dep];
      if (depPhase !== undefined && depPhase > here) {
        errors.push(`${tid} (phase ${here}) depends on ${dep} (phase ${depPhase}) - dependencies must point backward or within the same phase`);
      }
    }
  }
  const { edges, found } = parseDiagramEdges(lines);
  if (!found) warnings.push("diagram arrows not parsed confidently - diagram/definition cross-check skipped (verify by hand)");
  else {
    const intra = (a, b) => {
      const pa = membership[a];
      const pb = membership[b];
      if (pa === undefined || pb === undefined) return true;
      return pa === pb;
    };
    const depEdges = new Set();
    for (const [tid, task] of Object.entries(tasks)) {
      for (const dep of task.deps) depEdges.add(`${dep}->${tid}`);
    }
    for (const edge of edges) {
      const [a, b] = edge.split("->");
      if (intra(a, b) && !depEdges.has(edge) && tasks[a] && tasks[b]) {
        errors.push(`diagram shows ${a} -> ${b} but ${b} has no matching \`Depends on: ${a}\``);
      }
    }
    for (const edge of depEdges) {
      const [a, b] = edge.split("->");
      if (intra(a, b) && !edges.has(edge)) {
        errors.push(`${b} declares \`Depends on: ${a}\` but the diagram has no ${a} -> ${b} arrow`);
      }
    }
  }
  return { errors, warnings };
}

const args = parseArgs(process.argv.slice(2));
const path = resolveTasks(args.target, resolve(args.root));
if (!path) {
  console.error("validate_tasks: could not locate a tasks.md. Pass a path or run from the project root.");
  process.exit(2);
}
const { errors, warnings } = check(path);
for (const warning of warnings) console.log(`  WARN  ${warning}`);
for (const error of errors) console.log(`  ERROR ${error}`);
console.log(`\nvalidate_tasks: ${errors.length} error(s), ${warnings.length} warning(s) in ${path}`);
process.exit(errors.length || (warnings.length && args.strict) ? 1 : 0);
