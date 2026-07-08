import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import { join, relative, resolve, extname } from "node:path";
import { randomUUID } from "node:crypto";
import type { SkillInput, SkillOutput, EvidenceRecord, FileInfo } from "../types.js";
import { ToolRouter } from "../tool-router.js";
import { EvidenceStore } from "../evidence-store.js";

const IGNORED_DIRECTORIES = new Set([
  ".git", "node_modules", ".aeos-runtime", "dist", "build", "target",
  ".venv", "venv", "__pycache__", ".idea", ".vscode", ".gitlab",
  "coverage", ".next", ".nuxt", ".cache", "tmp", "temp", "logs"
]);

const IGNORED_FILES = new Set([
  ".DS_Store", "Thumbs.db", ".gitignore", ".gitkeep"
]);

export class RepoScannerSkill {
  async execute(
    input: SkillInput,
    toolRouter: ToolRouter,
    evidenceStore: EvidenceStore
  ): Promise<SkillOutput> {
    const artifacts: string[] = [];
    const evidence: EvidenceRecord[] = [];
    const risks: string[] = [];
    const facts: string[] = [];
    const assumptions: string[] = [];
    const errors: string[] = [];

    const ws = resolve(input.workspacePath);

    if (!existsSync(ws)) {
      errors.push(`Workspace path does not exist: ${ws}`);
      return { artifacts, evidence, risks, facts, assumptions, errors };
    }

    const scanResult = await this.scanDirectory(ws, ws, input.scanDepth, toolRouter, evidenceStore);

    facts.push(`Workspace: ${ws}`);
    facts.push(`Files scanned: ${scanResult.totalFiles}`);
    facts.push(`Directories scanned: ${scanResult.totalDirs}`);
    facts.push(`Languages detected: ${[...scanResult.languages].join(", ") || "none"}`);
    facts.push(`Build tools detected: ${[...scanResult.buildTools].join(", ") || "none"}`);

    if (scanResult.hasDocker) facts.push("Docker configuration detected");
    if (scanResult.hasCICD) facts.push("CI/CD configuration detected");
    if (scanResult.hasTests) facts.push("Test files detected");

    const secretCount = scanResult.secretIndicators.length;
    if (secretCount > 0) {
      risks.push(`Possible secrets detected in ${secretCount} locations (not revealed)`);
      for (const si of scanResult.secretIndicators.slice(0, 20)) {
        evidence.push(this.makeEvidence("security", `Secret pattern match: ${si.pattern}`, si.file));
      }
    }

    if (scanResult.languages.size === 0) {
      assumptions.push("No programming language detected; project may be configuration-only or binary");
    }

    const ecosystemMap = this.generateEcosystemMap(ws, scanResult);
    const riskReport = this.generateRiskReport(scanResult, risks);
    const recommendedPlaybooks = this.generateRecommendedPlaybooks(scanResult);

    const ecoArtifact = evidenceStore.writeGeneratedArtifact("ecosystem-map.md", ecosystemMap);
    const riskArtifact = evidenceStore.writeGeneratedArtifact("risk-report.md", riskReport);
    const pbArtifact = evidenceStore.writeGeneratedArtifact("recommended-playbooks.md", recommendedPlaybooks);

    artifacts.push(ecoArtifact, riskArtifact, pbArtifact);

    const evIndex = this.generateEvidenceIndex(evidenceStore);
    evidenceStore.writeGeneratedArtifact("index.md", evIndex);

    evidence.push(this.makeEvidence("source", "Repository scan completed", "ecosystem-map.md"));
    evidence.push(this.makeEvidence("security", "Risk assessment completed", "risk-report.md"));

    return { artifacts, evidence, risks, facts, assumptions, errors };
  }

  private async scanDirectory(
    root: string,
    current: string,
    depth: number,
    toolRouter: ToolRouter,
    evidenceStore: EvidenceStore,
    currentDepth: number = 0
  ): Promise<ScanResult> {
    const result: ScanResult = {
      totalFiles: 0,
      totalDirs: 0,
      languages: new Set<string>(),
      buildTools: new Set<string>(),
      frameworks: new Set<string>(),
      hasDocker: false,
      hasCICD: false,
      hasTests: false,
      testFiles: [],
      ciFiles: [],
      dockerFiles: [],
      dependencyFiles: [],
      secretIndicators: [],
      fileNames: [],
      extensions: new Map<string, number>()
    };

    if (currentDepth > depth) return result;

    let entries: string[];
    try {
      entries = readdirSync(current);
    } catch {
      return result;
    }

    for (const entry of entries) {
      if (IGNORED_DIRECTORIES.has(entry) || IGNORED_FILES.has(entry)) continue;

      const fullPath = join(current, entry);
      const relPath = relative(root, fullPath).replaceAll("\\", "/");

      try {
        const stat = statSync(fullPath);
        if (stat.isSymbolicLink()) continue;

        if (stat.isDirectory()) {
          result.totalDirs++;
          const subResult = await this.scanDirectory(root, fullPath, depth, toolRouter, evidenceStore, currentDepth + 1);
          this.mergeScanResult(result, subResult);
        } else if (stat.isFile()) {
          result.totalFiles++;
          result.fileNames.push(relPath);

          const ext = extname(entry).toLowerCase();
          result.extensions.set(ext, (result.extensions.get(ext) ?? 0) + 1);

          this.detectLanguage(entry, ext, result);
          this.detectBuildTool(entry, relPath, result);
          this.detectFramework(entry, relPath, result);
          this.detectSpecialFile(entry, relPath, result);

          if (result.totalFiles <= 1000) {
            this.detectSecretPattern(entry, relPath, result);
          }
        }
      } catch {
        // skip inaccessible files
      }
    }

    return result;
  }

  private detectLanguage(entry: string, ext: string, result: ScanResult): void {
    const langMap: Record<string, string> = {
      ".ts": "TypeScript", ".tsx": "TypeScript", ".js": "JavaScript",
      ".jsx": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript",
      ".py": "Python", ".java": "Java", ".kt": "Kotlin", ".kts": "Kotlin",
      ".go": "Go", ".rs": "Rust", ".cs": "C#", ".rb": "Ruby",
      ".php": "PHP", ".swift": "Swift", ".scala": "Scala",
      ".tf": "Terraform", ".sql": "SQL", ".r": "R", ".m": "MATLAB",
      ".vue": "Vue", ".svelte": "Svelte", ".astro": "Astro"
    };
    if (langMap[ext]) result.languages.add(langMap[ext]);
  }

  private detectBuildTool(entry: string, relPath: string, result: ScanResult): void {
    if (entry === "package.json") result.buildTools.add("npm/node");
    if (entry === "pom.xml") result.buildTools.add("maven");
    if (entry === "build.gradle" || entry === "build.gradle.kts" || entry === "settings.gradle.kts") {
      result.buildTools.add("gradle");
    }
    if (entry === "pyproject.toml") result.buildTools.add("python-pyproject");
    if (entry === "requirements.txt") result.buildTools.add("python-requirements");
    if (entry === "Cargo.toml") result.buildTools.add("cargo");
    if (entry === "go.mod") result.buildTools.add("go-modules");
    if (entry === "Gemfile") result.buildTools.add("bundler");
    if (entry === "CMakeLists.txt") result.buildTools.add("cmake");
    if (entry.endsWith(".csproj")) result.buildTools.add("dotnet");
    if (entry.endsWith(".sln")) result.buildTools.add("dotnet");

    const deps = ["package.json", "pom.xml", "build.gradle", "build.gradle.kts",
      "pyproject.toml", "requirements.txt", "Cargo.toml", "go.mod",
      "Gemfile", "yarn.lock", "package-lock.json", "pnpm-lock.yaml"];
    if (deps.includes(entry)) result.dependencyFiles.push(relPath);
  }

  private detectFramework(entry: string, relPath: string, result: ScanResult): void {
    const lower = entry.toLowerCase();
    if (lower === "angular.json" || lower === "angular-cli.json") result.frameworks.add("Angular");
    if (lower === "next.config.js" || lower === "next.config.mjs" || lower === "next.config.ts") result.frameworks.add("Next.js");
    if (lower === "nuxt.config.js" || lower === "nuxt.config.ts") result.frameworks.add("Nuxt");
    if (lower === "vite.config.ts" || lower === "vite.config.js") result.frameworks.add("Vite");
    if (lower === "astro.config.mjs") result.frameworks.add("Astro");
    if (relPath.includes("spring") || entry === "application.properties" || entry === "application.yml") result.frameworks.add("Spring");
    if (relPath.includes("fastapi") || entry === "main.py" && relPath.includes("api")) result.frameworks.add("FastAPI");
  }

  private detectSpecialFile(entry: string, relPath: string, result: ScanResult): void {
    if (entry === "Dockerfile" || entry.toLowerCase().startsWith("dockerfile")) {
      result.hasDocker = true;
      result.dockerFiles.push(relPath);
    }
    if (/^docker-compose\.(yml|yaml)$/i.test(entry)) {
      result.hasDocker = true;
      result.dockerFiles.push(relPath);
    }
    if (relPath.startsWith(".github/workflows/") || relPath.includes(".gitlab-ci.yml") || relPath.includes("azure-pipelines")) {
      result.hasCICD = true;
      result.ciFiles.push(relPath);
    }
    if (entry.toLowerCase().includes("test") || entry.toLowerCase().includes("spec") || relPath.startsWith("tests/") || relPath.startsWith("src/test/") || relPath.startsWith("test/")) {
      result.hasTests = true;
      result.testFiles.push(relPath);
    }
  }

  private detectSecretPattern(entry: string, relPath: string, result: ScanResult): void {
    const secretPatterns = [
      { pattern: "API key pattern", regex: /\b[Aa][Pp][Ii]_?[Kk][Ee][Yy]\b/ },
      { pattern: "Secret pattern", regex: /\b[Ss][Ee][Cc][Rr][Ee][Tt]\b/ },
      { pattern: "Password pattern", regex: /\b[Pp][Aa][Ss][Ss][Ww][Oo][Rr][Dd]\b/ },
      { pattern: "Token pattern", regex: /\b[Tt][Oo][Kk][Ee][Nn]\b/ },
      { pattern: "Credential pattern", regex: /\b[Cc][Rr][Ee][Dd][Ee][Nn][Tt][Ii][Aa][Ll][Ss]?\b/ },
      { pattern: "Authorization header", regex: /\b[Aa]uth[Oo]rization\b/ },
      { pattern: "JWT pattern", regex: /\b[Jj][Ww][Tt]\b/ },
      { pattern: ".env file", regex: /\.env$/ }
    ];

    if (entry === ".env" || entry.startsWith(".env.")) {
      result.secretIndicators.push({ pattern: ".env file", file: relPath, severity: "high" });
      return;
    }

    if (relPath.endsWith(".md") || relPath.endsWith(".yaml") || relPath.endsWith(".yml") || relPath.endsWith(".json") || relPath.endsWith(".ts") || relPath.endsWith(".js") || relPath.endsWith(".py")) {
      try {
        const content = readFileSync(join(resolve("."), relPath), "utf-8").slice(0, 5000);
        for (const sp of secretPatterns) {
          if (sp.regex.test(content)) {
            result.secretIndicators.push({ pattern: sp.pattern, file: relPath, severity: "medium" });
            break;
          }
        }
      } catch {
        // skip unreadable
      }
    }
  }

  private mergeScanResult(target: ScanResult, source: ScanResult): void {
    target.totalFiles += source.totalFiles;
    target.totalDirs += source.totalDirs;
    source.languages.forEach((l) => target.languages.add(l));
    source.buildTools.forEach((b) => target.buildTools.add(b));
    source.frameworks.forEach((f) => target.frameworks.add(f));
    if (source.hasDocker) target.hasDocker = true;
    if (source.hasCICD) target.hasCICD = true;
    if (source.hasTests) target.hasTests = true;
    target.testFiles.push(...source.testFiles);
    target.ciFiles.push(...source.ciFiles);
    target.dockerFiles.push(...source.dockerFiles);
    target.dependencyFiles.push(...source.dependencyFiles);
    target.secretIndicators.push(...source.secretIndicators);
    target.fileNames.push(...source.fileNames);
    for (const [ext, count] of source.extensions) {
      target.extensions.set(ext, (target.extensions.get(ext) ?? 0) + count);
    }
  }

  private generateEcosystemMap(workspace: string, scan: ScanResult): string {
    const lines: string[] = [];
    lines.push("# Ecosystem Map");
    lines.push("");
    lines.push(`- **Workspace:** ${workspace}`);
    lines.push(`- **Generated:** ${new Date().toISOString()}`);
    lines.push(`- **Total files:** ${scan.totalFiles}`);
    lines.push(`- **Total directories:** ${scan.totalDirs}`);
    lines.push("");
    lines.push("## Languages");
    lines.push("");
    const sortedLangs = [...scan.languages].sort();
    if (sortedLangs.length === 0) {
      lines.push("_No languages detected._");
    } else {
      for (const lang of sortedLangs) {
        lines.push(`- ${lang}`);
      }
    }
    lines.push("");
    lines.push("## Build Tools");
    lines.push("");
    const sortedTools = [...scan.buildTools].sort();
    if (sortedTools.length === 0) {
      lines.push("_No build tools detected._");
    } else {
      for (const tool of sortedTools) {
        lines.push(`- ${tool}`);
      }
    }
    lines.push("");
    lines.push("## Frameworks");
    lines.push("");
    const sortedFrameworks = [...scan.frameworks].sort();
    if (sortedFrameworks.length === 0) {
      lines.push("_No frameworks detected._");
    } else {
      for (const fw of sortedFrameworks) {
        lines.push(`- ${fw}`);
      }
    }
    lines.push("");
    lines.push("## Infrastructure");
    lines.push("");
    lines.push(`- **Docker:** ${scan.hasDocker ? "yes" : "no"}`);
    if (scan.dockerFiles.length > 0) {
      for (const df of scan.dockerFiles) lines.push(`  - \`${df}\``);
    }
    lines.push(`- **CI/CD:** ${scan.hasCICD ? "yes" : "no"}`);
    if (scan.ciFiles.length > 0) {
      for (const cf of scan.ciFiles) lines.push(`  - \`${cf}\``);
    }
    lines.push(`- **Tests:** ${scan.hasTests ? "yes" : "no"}`);
    lines.push("");
    lines.push("## Dependency Files");
    lines.push("");
    if (scan.dependencyFiles.length === 0) {
      lines.push("_No dependency files detected._");
    } else {
      for (const df of scan.dependencyFiles) lines.push(`- \`${df}\``);
    }
    lines.push("");
    lines.push("## File Extensions");
    lines.push("");
    const sortedExts = [...scan.extensions.entries()].sort((a, b) => b[1] - a[1]);
    if (sortedExts.length > 0) {
      for (const [ext, count] of sortedExts.slice(0, 20)) {
        lines.push(`- \`${ext || "(no ext)"}\`: ${count} files`);
      }
    }
    lines.push("");
    lines.push("---");
    lines.push("");
    lines.push("_Facts are based on file presence analysis. Assumptions are explicitly noted._");
    return lines.join("\n");
  }

  private generateRiskReport(scan: ScanResult, risks: string[]): string {
    const lines: string[] = [];
    lines.push("# Risk Report");
    lines.push("");
    lines.push(`- **Generated:** ${new Date().toISOString()}`);
    lines.push("");
    lines.push("## Identified Risks");
    lines.push("");
    if (risks.length === 0) {
      lines.push("_No risks automatically identified._");
    } else {
      for (const risk of risks) {
        lines.push(`- ${risk}`);
      }
    }
    lines.push("");
    lines.push("## Secret Indicators");
    lines.push("");
    if (scan.secretIndicators.length === 0) {
      lines.push("_No secret indicators detected._");
    } else {
      lines.push(`> ${scan.secretIndicators.length} potential secret indicator(s) found. Values are NOT inspected or revealed.`);
      lines.push("");
      for (const si of scan.secretIndicators) {
        lines.push(`- [${si.severity}] \`${si.file}\` — ${si.pattern}`);
      }
    }
    lines.push("");
    lines.push("## Test Coverage Signal");
    lines.push("");
    if (scan.hasTests) {
      lines.push(`- **Test files detected:** ${scan.testFiles.length}`);
      if (scan.testFiles.length > 0) {
        lines.push("- Top test files:");
        for (const tf of scan.testFiles.slice(0, 10)) {
          lines.push(`  - \`${tf}\``);
        }
      }
    } else {
      lines.push("_No test files detected._");
    }
    lines.push("");
    lines.push("---");
    lines.push("");
    lines.push("_Risks are indicators, not confirmed vulnerabilities. Manual review recommended._");
    return lines.join("\n");
  }

  private generateRecommendedPlaybooks(scan: ScanResult): string {
    const lines: string[] = [];
    lines.push("# Recommended Playbooks");
    lines.push("");
    lines.push(`- **Generated:** ${new Date().toISOString()}`);
    lines.push("");
    lines.push("Based on the detected project stack, the following playbooks are recommended:");
    lines.push("");

    const recommendations: Array<{ playbook: string; reason: string; priority: string }> = [];

    recommendations.push({
      playbook: "project-analysis",
      reason: "Always run first to establish baseline",
      priority: "high"
    });

    if (scan.languages.has("Java") || scan.buildTools.has("maven") || scan.buildTools.has("gradle")) {
      recommendations.push({
        playbook: "java21-migration",
        reason: "Java project detected",
        priority: "medium"
      });
    }

    if (scan.languages.has("Python") && (scan.frameworks.has("FastAPI") || scan.dependencyFiles.some((f) => f.includes("requirements")))) {
      recommendations.push({
        playbook: "python-ai-hardening",
        reason: "Python AI/RAG project detected",
        priority: "medium"
      });
    }

    if (scan.secretIndicators.length > 0) {
      recommendations.push({
        playbook: "security-secrets-audit",
        reason: `${scan.secretIndicators.length} secret indicators found`,
        priority: "high"
      });
    }

    if (scan.hasDocker || scan.hasCICD) {
      recommendations.push({
        playbook: "devcontainer-generation",
        reason: "Docker or CI/CD configuration detected",
        priority: "low"
      });
    }

    if (scan.hasTests && scan.testFiles.length > 0) {
      recommendations.push({
        playbook: "test-recovery",
        reason: "Test files detected",
        priority: "medium"
      });
    }

    recommendations.push({
      playbook: "documentation-generation",
      reason: "Recommended for all projects",
      priority: "low"
    });

    for (const rec of recommendations) {
      lines.push(`### ${rec.playbook}`);
      lines.push("");
      lines.push(`- **Priority:** ${rec.priority}`);
      lines.push(`- **Reason:** ${rec.reason}`);
      lines.push("");
    }

    lines.push("---");
    lines.push("");
    lines.push("_Recommendations are automated suggestions. Review and prioritize manually._");
    return lines.join("\n");
  }

  private generateEvidenceIndex(evidenceStore: EvidenceStore): string {
    const lines: string[] = [];
    lines.push("# Evidence Index");
    lines.push("");
    lines.push(`- **Generated:** ${new Date().toISOString()}`);
    lines.push("");
    lines.push("## Evidence Files");
    lines.push("");
    lines.push("- `evidence.jsonl` — All evidence records");
    lines.push("- `tool-calls.jsonl` — All tool call records");
    lines.push("- `permission-decisions.jsonl` — All permission decisions");
    lines.push("- `files-inspected.jsonl` — Files inspected during execution");
    lines.push("- `generated-artifacts.jsonl` — Generated artifact manifest");
    lines.push("");
    lines.push("## Generated Artifacts");
    lines.push("");
    lines.push("- `ecosystem-map.md` — Full ecosystem map");
    lines.push("- `risk-report.md` — Risk assessment");
    lines.push("- `recommended-playbooks.md` — Playbook recommendations");
    return lines.join("\n");
  }

  private makeEvidence(type: string, claim: string, reference: string): EvidenceRecord {
    return {
      id: randomUUID(),
      type,
      claim,
      reference,
      source: "repo-scanner",
      timestamp: new Date().toISOString(),
      verified: true
    };
  }
}

interface ScanResult {
  totalFiles: number;
  totalDirs: number;
  languages: Set<string>;
  buildTools: Set<string>;
  frameworks: Set<string>;
  hasDocker: boolean;
  hasCICD: boolean;
  hasTests: boolean;
  testFiles: string[];
  ciFiles: string[];
  dockerFiles: string[];
  dependencyFiles: string[];
  secretIndicators: Array<{ pattern: string; file: string; severity: string }>;
  fileNames: string[];
  extensions: Map<string, number>;
}
