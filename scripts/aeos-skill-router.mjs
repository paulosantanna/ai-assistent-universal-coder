#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { persistChromaticMemory } from "./aeos-chromatic-memory.mjs";

const repoRoot = resolve(process.cwd());
const registryPath = join(repoRoot, "aeos", "registries", "skills.registry.yaml");
const outputDir = join(repoRoot, ".aeos", "router");

function hash(value) {
  return createHash("sha256").update(value).digest("hex");
}

function parseSkills(yamlText) {
  const blocks = yamlText.split(/\n(?=- id: )/g);
  return blocks
    .map((block) => {
      const id = block.match(/^- id:\s*([^\n]+)/m)?.[1]?.trim();
      if (!id) return null;
      return {
        id,
        path: block.match(/^\s*path:\s*([^\n]+)/m)?.[1]?.trim() || "",
        ownerAgent: block.match(/^\s*owner_agent:\s*([^\n]+)/m)?.[1]?.trim() || "unknown",
        riskLevel: block.match(/^\s*risk_level:\s*([^\n]+)/m)?.[1]?.trim() || "unknown",
        mission: block.match(/^\s*mission:\s*([^\n]+)/m)?.[1]?.trim() || "",
        capabilities: [...block.matchAll(/^\s*-\s*([A-Z_]{3,})\s*$/gm)].map((m) => m[1])
      };
    })
    .filter(Boolean);
}

function scoreSkill(skill, request) {
  const text = `${skill.id} ${skill.mission} ${skill.capabilities.join(" ")} ${skill.path}`.toLowerCase();
  const requestLower = request.toLowerCase();
  const terms = requestLower.split(/[^a-z0-9_.-]+/).filter((term) => term.length > 2);
  let score = 0;
  for (const term of terms) {
    if (text.includes(term)) score += 3;
    if (skill.id.toLowerCase().includes(term)) score += 5;
  }

  const boosts = [
    ["bug", ["bug", "fix", "erro", "corrigir", "falha"]],
    ["test", ["test", "teste", "coverage", "cobertura"]],
    ["security", ["security", "seguranca", "vulnerabilidade", "secret"]],
    ["architecture", ["arquitetura", "architecture", "modernization", "migration"]],
    ["documentation", ["documentacao", "documentation", "mermaid", "docs"]],
    ["performance", ["performance", "latency", "throughput", "otimizar"]],
    ["token", ["token", "budget", "desperdicio"]],
    ["observability", ["observability", "grafana", "opentelemetry", "logs", "metrics"]]
  ];
  for (const [needle, aliases] of boosts) {
    if (aliases.some((alias) => requestLower.includes(alias)) && text.includes(needle)) score += 8;
  }

  const requestedJava = /\bjava\b/.test(requestLower) && !/\bjavascript\b/.test(requestLower);
  if (requestedJava && /\b(javascript|typescript|node|angular|python)\b/.test(skill.id.toLowerCase())) {
    score -= 25;
  }

  return score;
}

export function routeRequest(request, options = {}) {
  const yamlText = readFileSync(registryPath, "utf8");
  const skills = parseSkills(yamlText);
  const ranked = skills
    .map((skill) => ({ ...skill, score: scoreSkill(skill, request) }))
    .filter((skill) => skill.score > 0)
    .sort((a, b) => b.score - a.score || a.id.localeCompare(b.id));

  const selected = ranked.slice(0, Number(options.limit || 5));
  if (!selected.some((skill) => skill.id === "chromatic-mega-brain")) {
    const chromatic = skills.find((skill) => skill.id === "chromatic-mega-brain");
    if (chromatic) selected.unshift({ ...chromatic, score: 999 });
  }

  const executionId = `route-${hash(`${Date.now()}:${request}`).slice(0, 12)}`;
  const memory = persistChromaticMemory({
    executionId,
    request,
    selectedSkills: selected.map((skill) => skill.id)
  });

  const result = {
    executionId,
    request,
    selectedSkills: selected,
    rejectedTopCandidates: ranked.slice(selected.length, selected.length + 10),
    assumptions: [
      "Skill routing is based on registry metadata and request terms.",
      "Execution still requires each selected skill to have an implemented executor or playbook contract."
    ],
    gates: {
      chromaticMemoryPersisted: true,
      explicitArchitectureChangeRequired: /architecture|arquitetura|migration|migracao|refactor/i.test(request),
      noPythonRuntimePolicy: "active orchestration must use Node/TypeScript or declarative skills"
    },
    memory
  };

  mkdirSync(outputDir, { recursive: true });
  writeFileSync(join(outputDir, "latest-skill-route.json"), JSON.stringify(result, null, 2), "utf8");
  writeFileSync(join(outputDir, `${executionId}.json`), JSON.stringify(result, null, 2), "utf8");
  return result;
}

if (import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  const request = process.argv.slice(2).join(" ").trim();
  if (!request) {
    console.error("Usage: node scripts/aeos-skill-router.mjs \"user request\"");
    process.exit(2);
  }
  console.log(JSON.stringify(routeRequest(request), null, 2));
}


