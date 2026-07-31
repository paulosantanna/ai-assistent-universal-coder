#!/usr/bin/env node
import { mkdirSync, appendFileSync, existsSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { join, resolve } from "node:path";

const repoRoot = resolve(process.cwd());
const memoryRoot = join(repoRoot, "skills", "chromatic-mega-brain", "memory");
const files = {
  memory: "MEMORY.md",
  learning: "LEARNING.md",
  handoff: "HANDOFF.md",
  progress: "PROGRESS.md"
};

function now() {
  return new Date().toISOString();
}

function hash(value) {
  return createHash("sha256").update(value).digest("hex");
}

function ensureFile(path, title) {
  if (!existsSync(path)) {
    writeFileSync(path, `# ${title}\n\nManaged by AEOS Chromatic Mega Brain memory protocol.\n`, "utf8");
  }
}

export function persistChromaticMemory(entry) {
  mkdirSync(memoryRoot, { recursive: true });
  const timestamp = now();
  const request = String(entry.request || "unspecified request");
  const selectedSkills = Array.isArray(entry.selectedSkills) ? entry.selectedSkills : [];
  const executionId = entry.executionId || `chromatic-${hash(`${timestamp}:${request}`).slice(0, 12)}`;
  const digest = hash(JSON.stringify({ timestamp, request, selectedSkills, executionId }));

  const paths = Object.fromEntries(
    Object.entries(files).map(([key, file]) => [key, join(memoryRoot, file)])
  );

  ensureFile(paths.memory, "MEMORY.md");
  ensureFile(paths.learning, "LEARNING.md");
  ensureFile(paths.handoff, "HANDOFF.md");
  ensureFile(paths.progress, "PROGRESS.md");

  appendFileSync(
    paths.memory,
    `\n## ${timestamp} ${executionId}\n\n- Request: ${request}\n- Selected skills: ${selectedSkills.join(", ") || "none"}\n- Evidence hash: ${digest}\n`,
    "utf8"
  );
  appendFileSync(
    paths.learning,
    `\n## ${timestamp} ${executionId}\n\n- Request: ${request}\n- Learning candidate: Route requests through skill registry before execution.\n- Validation requirement: Persist handoff and progress evidence for every material task.\n- Evidence hash: ${digest}\n`,
    "utf8"
  );
  appendFileSync(
    paths.handoff,
    `\n## ${timestamp} ${executionId}\n\n- Source: ROOT Agent\n- Target: Skill Router / selected skill owners\n- Scope: ${request}\n- Required outputs: routed skills, evidence, progress, verification\n- Stop conditions: missing registry, missing memory persistence, unresolved high risk\n- Evidence hash: ${digest}\n`,
    "utf8"
  );
  appendFileSync(
    paths.progress,
    `\n## ${timestamp} ${executionId}\n\n- Status: ROUTED\n- Request: ${request}\n- Selected skills: ${selectedSkills.join(", ") || "none"}\n- Next gate: execute selected skills and verify outputs\n- Evidence hash: ${digest}\n`,
    "utf8"
  );

  return { executionId, digest, memoryRoot, paths };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const request = process.argv.slice(2).join(" ").trim() || "manual memory update";
  const result = persistChromaticMemory({ request, selectedSkills: ["chromatic-mega-brain"] });
  console.log(JSON.stringify(result, null, 2));
}
