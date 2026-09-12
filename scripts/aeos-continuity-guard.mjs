#!/usr/bin/env node
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import yaml from "js-yaml";
import { listGitTrackedFiles } from "./lib/git-tracked-files.mjs";

const ROOT = resolve(process.cwd());
const REQUIRED = [
  "references/CODENAVI_CONTINUITY_STANDARD.md",
  "templates/codenavi-continuity/HANDOFF.md",
  "templates/codenavi-continuity/MEMORY.md",
  "templates/codenavi-continuity/PROGRESS.md",
  "templates/codenavi-continuity/LEARNING.md",
  ".notebook/INDEX.md",
  ".notebook/HANDOFF.md",
  ".notebook/MEMORY.md",
  ".notebook/PROGRESS.md",
  ".notebook/LEARNING.md",
  "skills/continuity-bootstrapper/SKILL.md",
  "skills/handoff-manager/SKILL.md",
  "skills/memory-curator/SKILL.md",
  "skills/progress-tracker/SKILL.md",
  "skills/learning-curator/SKILL.md",
  "aeos/registries/skills.codenavi-continuity.additions.yaml"
];
const SKILLS = ["continuity-bootstrapper", "handoff-manager", "memory-curator", "progress-tracker", "learning-curator"];

function tracked() {
  return new Set(listGitTrackedFiles({ cwd: ROOT }));
}
function read(path) { return readFileSync(resolve(ROOT, path), "utf8"); }

const files = tracked();
const errors = [];
for (const path of REQUIRED) if (!files.has(path)) errors.push(`${path}: required continuity artifact is not tracked`);

for (const path of ["AGENT.md", "AGENTS.md"]) {
  const text = read(path);
  for (const token of ["HANDOFF.md", "MEMORY.md", "PROGRESS.md", "LEARNING.md", "CODENAVI_CONTINUITY_STANDARD.md"]) {
    if (!text.includes(token)) errors.push(`${path}: missing continuity token '${token}'`);
  }
}
if (read("AGENT.md") !== read("AGENTS.md")) errors.push("AGENT.md and AGENTS.md must be byte-identical");

const index = read(".notebook/INDEX.md");
for (const file of ["HANDOFF.md", "MEMORY.md", "PROGRESS.md", "LEARNING.md"]) {
  if (!index.includes(`(${file})`)) errors.push(`.notebook/INDEX.md: missing ${file}`);
}

for (const skill of SKILLS) {
  const path = `skills/${skill}/SKILL.md`;
  if (!read(path).includes("Governance: CodENavi v1")) errors.push(`${path}: missing CodENavi governance marker`);
}

try {
  const parsed = yaml.load(read("aeos/registries/skills.codenavi-continuity.additions.yaml"));
  const entries = Array.isArray(parsed?.skills) ? parsed.skills : [];
  const ids = new Set(entries.map((entry) => entry?.id));
  for (const skill of SKILLS) if (!ids.has(skill)) errors.push(`continuity registry: missing skill '${skill}'`);
  for (const entry of entries) if (entry.owner_agent !== "codenavi-agent") errors.push(`continuity registry: '${entry.id}' owner must be codenavi-agent`);
} catch (error) {
  errors.push(`continuity registry invalid: ${error instanceof Error ? error.message : String(error)}`);
}

const secretPatterns = [
  /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/,
  /\b(?:ghp|github_pat|sk)-[A-Za-z0-9_-]{20,}\b/,
  /\b(?:password|passwd|secret|token)\s*[:=]\s*["']?[^\s"'`]{8,}/i
];
for (const path of [".notebook/HANDOFF.md", ".notebook/MEMORY.md", ".notebook/PROGRESS.md", ".notebook/LEARNING.md"]) {
  const text = read(path);
  for (const pattern of secretPatterns) if (pattern.test(text)) errors.push(`${path}: potential raw secret detected`);
}

if (errors.length) {
  console.error(JSON.stringify({ status: "FAIL", standard: "CodENavi Continuity", errors }, null, 2));
  process.exit(1);
}
console.log(JSON.stringify({ status: "PASS", standard: "CodENavi Continuity", skills: SKILLS, continuityArtifacts: 4 }, null, 2));
