#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { basename, join, resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { persistChromaticMemory } from "./aeos-chromatic-memory.mjs";
import { buildCriticalThinkingPlan } from "./aeos-critical-thinking-governance.mjs";

const repoRoot = resolve(process.cwd());
const registryPath = join(repoRoot, "aeos", "registries", "skills.registry.yaml");
const overlayIndexPath = join(repoRoot, "aeos", "registries", "overlay.registry.index.yaml");
const outputDir = join(repoRoot, ".aeos", "router");
const REGISTRY_ENTRY = /^[ \t]{0,2}-[ \t]+id:[ \t]*([^\n#]+)/m;

function hash(value) {
  return createHash("sha256").update(value).digest("hex");
}

function parseSkills(yamlText) {
  const blocks = yamlText.split(/\n(?=[ \t]{0,2}-[ \t]+id:[ \t]+)/g);
  return blocks
    .map((block) => {
      const id = block.match(REGISTRY_ENTRY)?.[1]?.trim();
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

function normalizeRegistryFragmentPath(rawPath) {
  return rawPath.trim().replace(/^['"]|['"]$/g, "");
}

export function resolveActiveSkillRegistryFragments(options = {}) {
  const root = options.repoRoot || repoRoot;
  const fallback = options.registryPath || join(root, "aeos", "registries", "skills.registry.yaml");
  const index = options.overlayIndexPath || join(root, "aeos", "registries", "overlay.registry.index.yaml");

  if (!existsSync(index)) return existsSync(fallback) ? [fallback] : [];

  const overlayText = readFileSync(index, "utf8");
  const fragments = [];
  for (const match of overlayText.matchAll(/^\s*-\s+path:\s*([^\n#]+)$/gm)) {
    const relativePath = normalizeRegistryFragmentPath(match[1]);
    const absolutePath = resolve(root, relativePath);
    if (!existsSync(absolutePath)) continue;

    // Registry naming is heterogeneous across historical overlays. Content shape,
    // not filename alone, decides whether a fragment contributes skill entries.
    const fragmentText = readFileSync(absolutePath, "utf8");
    if (!/^skills:\s*$/m.test(fragmentText)) continue;
    fragments.push(absolutePath);
  }

  if (!fragments.includes(fallback) && existsSync(fallback)) fragments.unshift(fallback);
  return fragments;
}

export function loadActiveSkills(options = {}) {
  const fragments = resolveActiveSkillRegistryFragments(options);
  const merged = new Map();

  for (const fragment of fragments) {
    const text = readFileSync(fragment, "utf8");
    for (const skill of parseSkills(text)) {
      // Overlay order is authoritative: later fragments may intentionally refine
      // metadata for an earlier skill id without duplicating runtime candidates.
      merged.set(skill.id, { ...skill, registryFragment: basename(fragment) });
    }
  }

  return [...merged.values()];
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
    ["observability", ["observability", "grafana", "opentelemetry", "logs", "metrics"]],
    ["devops", ["devops", "ci/cd", "pipeline", "esteira", "github actions", "workflow", "merge", "push", "pull request"]],
    ["spec-driven", ["spec-driven", "tlc-spec-driven", "specify", "ears"]],
    ["spec-driven-lean", ["spec-driven-lean", "tlc-spec-lean", "write the checks"]],
    ["not-your-babysitter", ["not-your-babysitter", "babysitter", "nanny mode", "hand-holding"]],
    ["cursor-subagent-creator", ["cursor subagent", "cursor agent", "subagent-creator"]],
    ["skill-architect", ["skill-architect", "create a skill", "design a skill"]],
    ["technical-design-doc-creator", ["technical-design-doc", "design doc", "tdd", "rfc"]],
    ["best-practices", ["best-practices", "best practices", "security audit"]],
    ["the-fool", ["the-fool", "devil's advocate", "pre-mortem", "red team"]],
    ["the-jury", ["the-jury", "convene a jury", "monte um juri", "painel"]],
    ["ai-seo", ["ai-seo", "programmatic seo", "ai overviews", "organic traffic"]],
    ["nx-workspace", ["nx-workspace", "nx monorepo", "nx affected", "nx.json"]],
    ["subagent-creator", ["subagent-creator", "create subagent", "specialized assistant", "create verifier"]],
    ["tlc-plan", ["tlc-plan", "write the task", "cut this prd", "turn this design doc"]],
    ["learning-opportunities", ["learning-opportunities", "learning exercise", "teach me", "help me understand"]],
    ["perf-astro", ["perf-astro", "astro performance", "astro lighthouse", "astro-critters"]],
    ["core-web-vitals", ["core-web-vitals", "core web vitals", "fix lcp", "reduce cls", "optimize inp"]],
    ["perf-lighthouse", ["perf-lighthouse", "run lighthouse", "lighthouse score", "performance budget"]],
    ["perf-web-optimization", ["perf-web-optimization", "bundle size", "page speed", "slow site", "lazy loading"]],
    ["security-best-practices", ["security-best-practices", "security best practices", "secure-by-default"]],
    ["security-ownership-map", ["security-ownership-map", "bus factor", "orphaned sensitive", "codeowners"]],
    ["security-threat-model", ["security-threat-model", "threat model", "abuse paths", "appsec threat"]],
    ["web-quality-audit", ["web-quality-audit", "audit my site", "review web quality", "check page quality"]]
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
  const skills = loadActiveSkills(options);
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
  const criticalThinkingPlans = selected.map((skill) => buildCriticalThinkingPlan({
    skillId: skill.id,
    riskLevel: skill.riskLevel,
    request,
    mission: skill.mission
  }));
  const invalidCriticalThinkingPlans = criticalThinkingPlans.filter((plan) => plan.status !== "PASS");
  if (invalidCriticalThinkingPlans.length > 0) {
    throw new Error(
      `Critical-thinking governance blocked routing: ${invalidCriticalThinkingPlans
        .flatMap((plan) => plan.blockingConditions)
        .join("; ")}`
    );
  }

  const memory = persistChromaticMemory(
    {
      executionId,
      request,
      selectedSkills: selected.map((skill) => skill.id)
    },
    { memoryRoot: options.memoryRoot }
  );

  const result = {
    executionId,
    request,
    selectedSkills: selected,
    criticalThinkingGovernance: {
      governingSkill: "critical-thinking-governor",
      plans: criticalThinkingPlans
    },
    rejectedTopCandidates: ranked.slice(selected.length, selected.length + 10),
    assumptions: [
      "Skill routing is based on active overlay registry metadata and request terms.",
      "Execution still requires each selected skill to have an implemented executor or playbook contract."
    ],
    gates: {
      chromaticMemoryPersisted: true,
      criticalThinkingGoverned: true,
      overlayRegistryResolved: true
    },
    memory
  };

  const targetDir = options.outputDir || outputDir;
  mkdirSync(targetDir, { recursive: true });
  writeFileSync(join(targetDir, `${executionId}.json`), `${JSON.stringify(result, null, 2)}\n`);
  return result;
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  const request = process.argv.slice(2).join(" ").trim();
  if (!request) {
    console.error("Usage: npm run aeos:route -- <request>");
    process.exit(1);
  }
  console.log(JSON.stringify(routeRequest(request), null, 2));
}
