#!/usr/bin/env node
import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";

const REQUIRED_SECTIONS = [
  ["Problem", "Problem Statement"],
  ["Out of scope", "Out of Scope"],
  ["Assumptions", "Assumptions & Open Questions"],
  ["Criteria", "User Stories"],
  ["Traceability", "Requirement Traceability"],
  ["Observable"],
  ["Flow"],
  ["Relations"],
  ["Surface"],
  ["Landing"],
  ["Impact"]
];
const SHAPE_HINTS = {
  Flow: "state the hops in order, or `single module - <name>`",
  Relations: "state the entities and cardinality, or `None - no stored-data shape change`",
  Surface: "state the route signature, or `None - nothing consumed outside`",
  Impact: "state what changes underneath, or `nothing` - a missing row is not an answer"
};
const ID_RE = /^[A-Z][A-Z0-9]*-\d+$/;
const PLACEHOLDER_RE = /^\s*[\[<].+[\]>]\s*$/;
const CID_RE = /\bC\d+\b/;
const STATUS_RE = /\b[1-5]\d\d\b/;
const NONE_RE = /\b(none|nothing|n\/?a|single module)\b/i;
const VAGUE_RE = /\b(gracefully|properly|correctly|quickly|fast|slow|efficiently|reasonably|appropriately|as expected|user-friendly|robust)\b/i;
const ER_ATTRIBUTE_RE = /^\s*\w+\s*\{\s*$/;
const HOP_RESOLVED_RE = /\b(exists|existing|new\b|door\s*\d+)|out\s*:/i;
const MODULE_RE = /`([^`]+)`/g;
const NODE_LABEL_RE = /[\[(]\s*"?([^"\]()|]+?)"?\s*[\])]/g;
const EDGE_LINE_RE = /--+>|--+\s/;

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
  const features = readdirSync(base).filter((d) => existsSync(join(base, d, "plan.md"))).sort();
  if (features.length === 1) return join(base, features[0], "plan.md");
  if (!features.length) return null;
  console.error(`validate_plan: multiple features found; pass one explicitly:\n  ${features.map((f) => join(base, f, "plan.md")).join("\n  ")}`);
  process.exit(2);
}

function resolvePlan(target, root) {
  if (!target) return autodetect(root);
  if (existsSync(target) && statSync(target).isFile()) return target;
  if (existsSync(target) && statSync(target).isDirectory()) {
    const cand = join(target, "plan.md");
    return existsSync(cand) ? cand : autodetect(target);
  }
  const cand = join(root, ".specs", "features", target, "plan.md");
  return existsSync(cand) ? cand : null;
}

function splitRow(line) {
  return line.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((c) => c.trim());
}

function isSeparator(line) {
  return /^\s*\|?[\s:|-]+\|?\s*$/.test(line) && line.includes("-");
}

function sectionBounds(lines, names) {
  const list = Array.isArray(names) ? names : [names];
  const pattern = new RegExp(`^#{1,4}\\s+(?:${list.map((n) => n.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|")})\\b.*$`, "i");
  let start = null;
  for (let i = 0; i < lines.length; i += 1) {
    if (pattern.test(lines[i].trim())) {
      start = i + 1;
      break;
    }
  }
  if (start === null) return null;
  let end = lines.length;
  for (let j = start; j < lines.length; j += 1) {
    if (/^#{1,2}\s+\S/.test(lines[j])) {
      end = j;
      break;
    }
  }
  return [start, end];
}

function firstTable(lines, bounds) {
  if (!bounds) return [];
  const rows = [];
  let started = false;
  for (let i = bounds[0]; i < bounds[1]; i += 1) {
    const stripped = lines[i].trim();
    if (stripped.startsWith("|")) {
      started = true;
      rows.push(stripped);
    } else if (started && stripped === "") continue;
    else if (started) break;
  }
  const data = rows.filter((r) => !isSeparator(r));
  return data.slice(1);
}

function stripFences(lines, keep = ["mermaid"]) {
  const out = [];
  let fenceInfo = null;
  for (const ln of lines) {
    const stripped = ln.trim();
    if (stripped.startsWith("```")) {
      fenceInfo = fenceInfo === null ? stripped.replaceAll("`", "").trim().toLowerCase() : null;
      out.push("");
      continue;
    }
    out.push(fenceInfo === null || keep.includes(fenceInfo) ? ln : "");
  }
  return out;
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
  if (kws.length) return [true, { WHILE: "state-driven", WHEN: "event-driven", "IF/THEN": "unwanted-behavior", WHERE: "optional-feature" }[kws[0]]];
  if (/^\s*the\b/.test(low)) return [true, "ubiquitous"];
  return [true, "warn: SHALL present but no EARS lead keyword"];
}

function siblingProfile(planPath) {
  const checks = join(dirname(resolve(planPath)), "checks.md");
  if (!existsSync(checks)) return null;
  for (const ln of readFileSync(checks, "utf8").split(/\r?\n/)) {
    const match = /^\**Profile\**\s*:\s*`?(\w+)`?/i.exec(ln.trim());
    if (match) return match[1].toLowerCase();
  }
  return null;
}

function checkCriteria(lines) {
  const errors = [];
  const warnings = [];
  let inAc = false;
  let acCount = 0;
  let blanks = 0;
  lines.forEach((ln, idx) => {
    const stripped = ln.trim();
    if (/^\*{0,2}Acceptance Criteria\*{0,2}\s*:?\s*$/i.test(stripped)) {
      inAc = true;
      blanks = 0;
      return;
    }
    if (!inAc) return;
    if (stripped === "") {
      blanks += 1;
      if (blanks >= 2) inAc = false;
      return;
    }
    blanks = 0;
    const itemMatch = /^\s*\d+\.\s+(.*)$/.exec(ln);
    if (itemMatch) {
      const item = itemMatch[1].trim();
      if (PLACEHOLDER_RE.test(item)) return;
      acCount += 1;
      const [ok, note] = classifyEars(item);
      if (!ok) errors.push(`L${idx + 1}: acceptance criterion has no SHALL (not testable): ${item.slice(0, 70)}`);
      else if (note.startsWith("warn")) {
        warnings.push(`L${idx + 1}: AC has SHALL but no EARS keyword (WHEN/WHILE/WHERE/IF or ubiquitous 'The … shall'): ${item.slice(0, 60)}`);
      }
      const vague = VAGUE_RE.exec(item);
      if (vague) warnings.push(`L${idx + 1}: AC uses '${vague[0]}' instead of a concrete value: ${item.slice(0, 60)}`);
    } else if (/^#{1,4}\s/.test(ln) || stripped.startsWith("**") || /^\s*[-*+]\s/.test(ln)) {
      inAc = false;
    }
  });
  if (acCount === 0) warnings.push("no numbered acceptance criteria found - is the plan filled in?");
  return { errors, warnings };
}

function warnUnresolved(warnings, idx, names, landText, kind) {
  if (!names.length) return;
  if (names.some((n) => landText.includes(n.toLowerCase()))) return;
  warnings.push(`L${idx + 1}: Flow ${kind} names \`${names[0]}\` without marking it as existing or as a Landing door - if it is neither, it is placement and belongs in the diff`);
}

function checkFile(path) {
  const lines = stripFences(readFileSync(path, "utf8").split(/\r?\n/));
  const errors = [];
  const warnings = [];
  const present = {};
  for (const names of REQUIRED_SECTIONS) {
    const bounds = sectionBounds(lines, names);
    present[names[0]] = bounds;
    if (!bounds) errors.push(`missing required section: ## ${names[0]}`);
  }
  if (sectionBounds(lines, "Sources") === null && !lines.some((ln) => /^\**Sources\**\s*:/i.test(ln.trim()))) {
    warnings.push("no Sources section - 'nothing' is a valid answer, a missing section is not");
  }
  if (lines.some((ln) => /\bbinding\b/i.test(ln))) {
    const profile = siblingProfile(path);
    if (profile && profile !== "ui") {
      warnings.push(`a source is marked binding but checks.md declares profile ${profile}, so nobody opens it - raise the profile to ui or drop the marking`);
    }
  }
  const criteria = checkCriteria(lines);
  errors.push(...criteria.errors);
  warnings.push(...criteria.warnings);
  const assumptions = present.Assumptions;
  if (assumptions) {
    let templateSeen = false;
    for (const row of firstTable(lines, assumptions)) {
      const cells = splitRow(row);
      if (cells.length < 3) continue;
      const [assumption, chosen, rationale] = cells;
      if (PLACEHOLDER_RE.test(assumption) && PLACEHOLDER_RE.test(chosen)) {
        templateSeen = true;
        continue;
      }
      if (!assumption) continue;
      if (!chosen || PLACEHOLDER_RE.test(chosen)) errors.push(`assumption '${assumption.slice(0, 40)}' has empty 'Chosen default'`);
      if (!rationale || PLACEHOLDER_RE.test(rationale)) errors.push(`assumption '${assumption.slice(0, 40)}' has empty 'Rationale'`);
    }
    if (templateSeen) warnings.push("Assumptions table still contains template placeholder rows");
    const oq = lines.slice(...assumptions).filter((ln) => ln.toLowerCase().includes("open questions"));
    const oqClean = oq.join(" ").replace(/[*_]/g, "").toLowerCase();
    if (!oq.length) warnings.push("no 'Open questions:' line in the Assumptions section");
    else if (!/open questions.*:\s*none/.test(oqClean)) warnings.push("open questions do not read as resolved ('Open questions: none')");
  }
  const trace = present.Traceability;
  if (trace) {
    let templateSeen = false;
    let realIds = 0;
    for (const row of firstTable(lines, trace)) {
      const cells = splitRow(row);
      if (!cells.length || !cells[0]) continue;
      const rid = cells[0];
      if (PLACEHOLDER_RE.test(rid) || rid.includes("[") || rid.includes("<")) {
        templateSeen = true;
        continue;
      }
      if (!ID_RE.test(rid)) errors.push(`malformed requirement ID: '${rid}' (expected e.g. AUTH-01)`);
      else realIds += 1;
    }
    if (templateSeen && realIds === 0) warnings.push("Traceability has only template rows (no real IDs yet)");
  }
  const obs = present.Observable;
  if (obs) {
    const body = lines.slice(...obs).map((ln) => ln.trim()).filter(Boolean);
    const rows = firstTable(lines, obs);
    const declaresNone = body.some((x) => NONE_RE.test(x));
    if (!body.length) errors.push("Observable section is empty - walk each surface's decisions, or state `None - no user-facing surface`");
    else if (!rows.length && !declaresNone) errors.push("Observable has no rows and does not state `None - no user-facing surface`");
    for (const row of rows) {
      const cells = splitRow(row);
      if (cells.length < 3 || !cells[0] || PLACEHOLDER_RE.test(cells[0])) continue;
      const label = `${cells[0].slice(0, 28)} / ${cells[1].slice(0, 28)}`;
      const landing = cells[2];
      if (!landing || PLACEHOLDER_RE.test(landing) || landing === "-" || landing === "—") {
        errors.push(`Observable '${label}': landing is blank - a criterion, \`existing - <what>\`, or \`n/a - <reason>\``);
        continue;
      }
      const low = landing.toLowerCase();
      for (const kw of ["n/a", "na -", "existing"]) {
        if (low.startsWith(kw)) {
          const rest = landing.slice(kw.length).replace(/^[\s\-–—:]+/, "");
          if (rest.length < 3) errors.push(`Observable '${label}': \`${kw}\` with no reason - say why it does not apply, or name what already behaves that way`);
          break;
        }
      }
    }
  }
  for (const [sec, hint] of Object.entries(SHAPE_HINTS)) {
    const bounds = present[sec];
    if (!bounds) continue;
    const body = lines.slice(...bounds).map((ln) => ln.trim()).filter(Boolean);
    if (!body.length) errors.push(`${sec} section is empty - ${hint}`);
    else if (body.every((x) => PLACEHOLDER_RE.test(x))) errors.push(`${sec} section is still the template placeholder`);
  }
  const rel = present.Relations;
  if (rel) {
    for (let i = rel[0]; i < rel[1]; i += 1) {
      if (ER_ATTRIBUTE_RE.test(lines[i])) {
        errors.push(`L${i + 1}: Relations carries an attribute block ('${lines[i].trim()}') - columns and types are reversible, come from the repo's conventions, and go stale here`);
        break;
      }
    }
  }
  const surf = present.Surface;
  if (surf) {
    const body = lines.slice(...surf).map((ln) => ln.trim()).filter(Boolean);
    const declaresNone = body.some((x) => NONE_RE.test(x));
    const rows = firstTable(lines, surf);
    for (const row of rows) {
      const cells = splitRow(row);
      if (!cells.length || !cells[0] || PLACEHOLDER_RE.test(cells[0])) continue;
      const statusCell = cells[3] ?? "";
      if (!STATUS_RE.test(statusCell)) {
        errors.push(`Surface '${cells[0].slice(0, 48)}': Status names no status code - those statuses are the set that owes a Coverage row in checks.md`);
      }
    }
    for (let i = surf[0]; i < surf[1]; i += 1) {
      if (CID_RE.test(lines[i])) {
        errors.push(`L${i + 1}: Surface names a check id, but checks.md does not exist yet - each route's statuses become a Coverage set there instead`);
        break;
      }
    }
    if (!rows.length && !declaresNone) errors.push("Surface has no route rows and does not state `None - nothing consumed outside`");
  }
  const land = present.Landing;
  if (land) {
    const body = lines.slice(...land).map((ln) => ln.trim()).filter(Boolean);
    const rows = firstTable(lines, land);
    const declaresNone = body.some((x) => NONE_RE.test(x));
    if (!body.length) errors.push("Landing section is empty - state `None - <why nothing here is one-way>`");
    else if (!rows.length && !declaresNone) errors.push("Landing has no door rows and does not state `None - <why>` - the omission has to be contestable");
    for (const row of rows) {
      const cells = splitRow(row);
      if (cells.length >= 3 && cells[0] && !PLACEHOLDER_RE.test(cells[0])) {
        if (!cells[1] || PLACEHOLDER_RE.test(cells[1])) errors.push(`Landing '${cells[0].slice(0, 40)}': no literal shape - the next person copies this`);
        if (!cells[2] || PLACEHOLDER_RE.test(cells[2])) errors.push(`Landing '${cells[0].slice(0, 40)}': no rejected alternative named`);
      }
    }
  }
  const imp = present.Impact;
  if (imp) {
    const body = lines.slice(...imp).map((ln) => ln.trim()).filter(Boolean);
    if (body.length && !firstTable(lines, imp).length && !body.some((x) => x.startsWith("-") || x.startsWith("*"))) {
      warnings.push("Impact has neither rows nor bullets - name the fronts, even to say nothing changes");
    }
  }
  const flow = present.Flow;
  if (flow) {
    const landText = land ? lines.slice(...land).join("\n").toLowerCase() : "";
    for (let i = flow[0]; i < flow[1]; i += 1) {
      const ln = lines[i].trim();
      if (!/^\s*(\d+\.|[-*])\s/.test(ln) || HOP_RESOLVED_RE.test(ln)) continue;
      warnUnresolved(warnings, i, [...ln.matchAll(MODULE_RE)].map((m) => m[1]), landText, "hop");
    }
    for (let i = flow[0]; i < flow[1]; i += 1) {
      const ln = lines[i];
      if (!EDGE_LINE_RE.test(ln) || HOP_RESOLVED_RE.test(ln)) continue;
      const labels = [...ln.matchAll(NODE_LABEL_RE)].map((m) => m[1].trim()).filter(Boolean);
      warnUnresolved(warnings, i, labels, landText, "diagram node");
    }
  }
  return { errors, warnings };
}

const args = parseArgs(process.argv.slice(2));
const path = resolvePlan(args.target, resolve(args.root));
if (!path) {
  console.error("validate_plan: could not locate a plan.md. Pass a path or run from the project root.");
  process.exit(2);
}
const { errors, warnings } = checkFile(path);
for (const warning of warnings) console.log(`  WARN  ${warning}`);
for (const error of errors) console.log(`  ERROR ${error}`);
console.log(`\nvalidate_plan: ${errors.length} error(s), ${warnings.length} warning(s) in ${path}`);
process.exit(errors.length || (warnings.length && args.strict) ? 1 : 0);
