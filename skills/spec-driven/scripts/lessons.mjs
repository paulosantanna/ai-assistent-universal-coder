#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";

const STORE_REL = join(".specs", "lessons.json");
const RENDER_REL = join(".specs", "LESSONS.md");
const SIGNALS = {
  ac_gap: "Acceptance criterion not covered / failed",
  surviving_mutant: "Discrimination sensor mutant survived (weak test)",
  spec_precision_gap: "Spec did not define a precise outcome",
  spec_deviation: "Implementation diverged from spec/design (SPEC_DEVIATION)",
  gate_fail: "Build-level gate check failed"
};
const DEFAULTS = { promote_threshold: 2, window_days: 45, quarantine_threshold: 2 };

function now() {
  return new Date().toISOString().replace(/\.\d+Z$/, "Z");
}

function parseDate(value) {
  const parsed = Date.parse(value);
  return Number.isNaN(parsed) ? Date.now() : parsed;
}

function norm(text) {
  return text
    .normalize("NFD")
    .toLowerCase()
    .replace(/\p{M}/gu, "")
    .replace(/[^\p{L}\p{N}\s]/gu, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function load(root) {
  const path = join(root, STORE_REL);
  if (!existsSync(path)) {
    return { schema: 1, ...DEFAULTS, next_id: 1, lessons: [] };
  }
  const data = JSON.parse(readFileSync(path, "utf8"));
  return { schema: 1, ...DEFAULTS, next_id: 1, lessons: [], ...data };
}

function render(root, data) {
  const byStatus = { confirmed: [], candidate: [], quarantined: [] };
  for (const lesson of data.lessons) (byStatus[lesson.status] ?? byStatus.candidate).push(lesson);
  const block = (title, items, note) => {
    const out = [`## ${title}`, "", note, ""];
    if (!items.length) return [...out, "_none_", ""];
    for (const lesson of items.sort((a, b) => a.id.localeCompare(b.id))) {
      const scope = lesson.scope ? ` · scope: \`${lesson.scope}\`` : "";
      out.push(`### ${lesson.id} - ${lesson.text}`);
      out.push(`- signal: \`${lesson.signal}\` · recurrence: ${lesson.recurrence} feature(s)${scope} · harmful: ${lesson.harmful ?? 0}`);
      out.push(`- features: ${lesson.features?.join(", ") || "-"}`);
      if (lesson.evidence?.length) {
        out.push(`- evidence: ${lesson.evidence[0]}${lesson.evidence.length > 1 ? ` (+${lesson.evidence.length - 1} more)` : ""}`);
      }
      out.push(`- last seen: ${lesson.last_seen ?? "-"}`, "");
    }
    return out;
  };
  const lines = [
    "# LESSONS - auto-maintained by scripts/lessons.mjs",
    "",
    "> Machine-owned. Do NOT hand-edit. Changes are overwritten on the next `lessons.mjs` write.",
    "> Canonical state lives in `.specs/lessons.json`. Edit lessons only via the script.",
    `> promote_threshold=${data.promote_threshold} distinct features · window_days=${data.window_days} · quarantine_threshold=${data.quarantine_threshold}`,
    "",
    ...block("Confirmed (load these at Specify/Design)", byStatus.confirmed, "Corroborated across multiple features. Safe to apply as guidance."),
    ...block("Candidates (under observation - do NOT load as guidance yet)", byStatus.candidate, "Seen once or not yet corroborated. Tracked, not trusted."),
    ...block("Quarantined (failed when applied - ignore)", byStatus.quarantined, "A confirmed lesson that recurred alongside failure. Kept for the maintainer to review.")
  ];
  writeFileSync(join(root, RENDER_REL), `${lines.join("\n").replace(/\s+$/, "")}\n`);
}

function save(root, data) {
  mkdirSync(dirname(join(root, STORE_REL)), { recursive: true });
  writeFileSync(join(root, STORE_REL), `${JSON.stringify(data, null, 2)}\n`);
  render(root, data);
}

function autoPrune(data) {
  const dropped = [];
  const nowMs = Date.now();
  data.lessons = data.lessons.filter((lesson) => {
    if (lesson.status === "candidate" && lesson.recurrence < data.promote_threshold) {
      const ageDays = (nowMs - parseDate(lesson.last_seen ?? lesson.created ?? now())) / 86400000;
      if (ageDays > data.window_days) {
        dropped.push(lesson.id);
        return false;
      }
    }
    return true;
  });
  return dropped;
}

function keyOf(signal, text) {
  return `${signal}::${norm(text)}`;
}

function parseArgs(argv) {
  const args = { root: ".", cmd: null, feature: "", signal: "", source: "", text: "", scope: "", id: "", status: "confirmed", query: "" };
  const rest = [];
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (token === "--root") args.root = argv[++i];
    else if (token === "--feature") args.feature = argv[++i];
    else if (token === "--signal") args.signal = argv[++i];
    else if (token === "--source") args.source = argv[++i];
    else if (token === "--text") args.text = argv[++i];
    else if (token === "--scope") args.scope = argv[++i];
    else if (token === "--id") args.id = argv[++i];
    else if (token === "--status") args.status = argv[++i];
    else if (token === "--query") args.query = argv[++i];
    else rest.push(token);
  }
  args.cmd = rest[0] ?? null;
  return args;
}

function selftestNorm() {
  const failures = [];
  const check = (cond, msg) => {
    if (!cond) failures.push(msg);
  };
  check(norm("Não use datas locais") === "nao use datas locais", "PT diacritics");
  check(norm("Nao use datas locais") === "nao use datas locais", "PT ascii");
  check(norm("日本語の文です") !== "" && norm("日本語の文です") !== norm("別の日本語文"), "JP distinct");
  check(norm("café") === "cafe", "cafe");
  if (failures.length) {
    for (const failure of failures) console.error(`FAIL: ${failure}`);
    return 1;
  }
  console.log("selftest_norm: ok");
  return 0;
}

const args = parseArgs(process.argv.slice(2));
const root = resolve(args.root);
if (!args.cmd) {
  console.error("lessons: command required (init|add|list|penalize|prune|status|selftest)");
  process.exit(2);
}

if (args.cmd === "selftest") process.exit(selftestNorm());

if (args.cmd === "init") {
  save(root, load(root));
  console.log(`Initialized lessons store at ${join(root, STORE_REL)} and ${join(root, RENDER_REL)}`);
  process.exit(0);
}

if (args.cmd === "add") {
  if (!SIGNALS[args.signal]) {
    console.error(`ERROR: --signal must be one of ${Object.keys(SIGNALS).sort().join(", ")}`);
    process.exit(2);
  }
  if (!args.feature.trim()) {
    console.error("ERROR: --feature is required (the feature the signal came from).");
    process.exit(2);
  }
  if (!args.source.trim()) {
    console.error("ERROR: --source is required (file:line / AC id / mutant id / SPEC_DEVIATION ref).");
    process.exit(2);
  }
  if (args.text.trim().length < 12) {
    console.error("ERROR: --text too short. State the actionable lesson in one terse sentence.");
    process.exit(2);
  }
  const data = load(root);
  autoPrune(data);
  const existing = data.lessons.find((lesson) => lesson.key === keyOf(args.signal, args.text));
  const stamp = now();
  if (existing) {
    if (!existing.features.includes(args.feature)) existing.features.push(args.feature);
    existing.recurrence = existing.features.length;
    existing.last_seen = stamp;
    const evidence = args.scope ? `${args.source} (${args.scope})` : args.source;
    if (!existing.evidence.includes(evidence)) existing.evidence.push(evidence);
    let promoted = false;
    if (existing.status === "candidate" && existing.recurrence >= data.promote_threshold) {
      existing.status = "confirmed";
      promoted = true;
    }
    save(root, data);
    console.log(`UPDATED ${existing.id} (recurrence=${existing.recurrence}, status=${existing.status})${promoted ? " - PROMOTED to confirmed" : ""}`);
  } else {
    const id = `L-${String(data.next_id).padStart(3, "0")}`;
    data.next_id += 1;
    data.lessons.push({
      id,
      key: keyOf(args.signal, args.text),
      text: args.text.trim(),
      signal: args.signal,
      scope: args.scope.trim(),
      status: "candidate",
      features: [args.feature.trim()],
      recurrence: 1,
      harmful: 0,
      evidence: [args.scope ? `${args.source} (${args.scope})` : args.source],
      created: stamp,
      last_seen: stamp
    });
    save(root, data);
    console.log(`ADDED ${id} (status=candidate, recurrence=1)`);
  }
  process.exit(0);
}

if (args.cmd === "penalize") {
  const data = load(root);
  const target = data.lessons.find((lesson) => lesson.id.toLowerCase() === args.id.toLowerCase());
  if (!target) {
    console.error(`ERROR: no lesson with id ${args.id}`);
    process.exit(2);
  }
  target.harmful = (target.harmful ?? 0) + 1;
  target.last_seen = now();
  if (target.harmful >= data.quarantine_threshold) target.status = "quarantined";
  save(root, data);
  console.log(`PENALIZED ${target.id} (harmful=${target.harmful}, status=${target.status})`);
  process.exit(0);
}

if (args.cmd === "list") {
  const data = load(root);
  if (autoPrune(data).length) save(root, data);
  const query = args.query.toLowerCase();
  const scope = args.scope.toLowerCase();
  const rows = data.lessons.filter((lesson) => {
    if (args.status !== "all" && lesson.status !== args.status) return false;
    if (query && !lesson.text.toLowerCase().includes(query)) return false;
    if (scope && !(lesson.scope ?? "").toLowerCase().includes(scope)) return false;
    return true;
  });
  if (!rows.length) {
    console.log(`(no ${args.status} lessons${query || scope ? ` matching '${query || scope}'` : ""})`);
    process.exit(0);
  }
  for (const lesson of rows.sort((a, b) => a.id.localeCompare(b.id))) {
    const extra = lesson.scope ? ` [scope:${lesson.scope}]` : "";
    console.log(`${lesson.id} (${lesson.status}, x${lesson.recurrence})${extra}: ${lesson.text}`);
  }
  process.exit(0);
}

if (args.cmd === "prune") {
  const data = load(root);
  const dropped = autoPrune(data);
  save(root, data);
  console.log(`Pruned ${dropped.length} stale candidate(s): ${dropped.join(", ") || "-"}`);
  process.exit(0);
}

if (args.cmd === "status") {
  const data = load(root);
  const counts = { confirmed: 0, candidate: 0, quarantined: 0 };
  for (const lesson of data.lessons) counts[lesson.status] = (counts[lesson.status] ?? 0) + 1;
  console.log(`lessons: ${data.lessons.length} total | confirmed=${counts.confirmed} candidate=${counts.candidate} quarantined=${counts.quarantined}`);
  process.exit(0);
}

console.error(`lessons: unknown command ${args.cmd}`);
process.exit(2);
