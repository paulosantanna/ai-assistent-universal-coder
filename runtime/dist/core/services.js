import { spawn } from "node:child_process";
import { appendFileSync, existsSync, mkdirSync, readdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { dirname, join, relative } from "node:path";
import { randomUUID } from "node:crypto";
function id() {
    return randomUUID();
}
function now() {
    return new Date().toISOString();
}
function readJson(path) {
    if (!existsSync(path))
        return null;
    return JSON.parse(readFileSync(path, "utf8"));
}
function writeJson(path, value) {
    mkdirSync(dirname(path), { recursive: true });
    writeFileSync(path, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}
function appendJsonl(path, value) {
    mkdirSync(dirname(path), { recursive: true });
    appendFileSync(path, `${JSON.stringify(value)}\n`, "utf8");
}
function truncateText(value, maxChars = 50000) {
    if (value.length <= maxChars)
        return value;
    const half = Math.floor(maxChars / 2);
    return `${value.slice(0, half)}\n... [TRUNCATED ${value.length - maxChars} chars] ...\n${value.slice(-half)}`;
}
function readJsonl(path) {
    if (!existsSync(path))
        return [];
    return readFileSync(path, "utf8")
        .split("\n")
        .filter(Boolean)
        .map((line) => JSON.parse(line));
}
function slug(input) {
    return input
        .toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .replace(/[^a-z0-9]+/g, "-")
        .replace(/(^-|-$)/g, "")
        .slice(0, 80) || "artifact";
}
function listMd(dir) {
    if (!existsSync(dir))
        return [];
    return readdirSync(dir).filter((name) => name.toLowerCase().endsWith(".md"));
}
export class AeosCore {
    version = "0.9.1";
    criticalFiles = [
        "AGENT.md",
        "foundation/ENGINEERING_CONSTITUTION.md",
        "foundation/N_LAYER_HIERARCHY.md",
        "foundation/ORGANIZATION_MODEL.md",
        "foundation/ENGINEERING_PRINCIPLES.md"
    ];
    init(projectPath) {
        const state = this.ensureRuntime(projectPath);
        this.memory(projectPath, "observation", `AEOS v${this.version} initialized.`);
        return state;
    }
    status(projectPath) {
        const state = this.ensureRuntime(projectPath);
        return {
            state,
            scan: this.loadOrCreateScan(projectPath),
            gates: this.gatesPlan(projectPath),
            provider: this.providerStatus(projectPath),
            counts: {
                tasks: this.tasks(projectPath).length,
                evidence: this.evidenceList(projectPath).length,
                memory: this.memoryList(projectPath).length,
                gateResults: this.gatesResults(projectPath).length,
                agentRuns: this.agentRuns(projectPath).length,
                reports: this.count(projectPath, "reports"),
                prompts: this.count(projectPath, "prompts"),
                context: this.count(projectPath, "context"),
                remediation: this.count(projectPath, "remediation"),
                backlog: this.count(projectPath, "backlog"),
                snapshots: this.count(projectPath, "snapshots"),
                delivery: this.count(projectPath, "delivery")
            }
        };
    }
    doctor(projectPath) {
        const state = this.ensureRuntime(projectPath);
        const scan = this.loadOrCreateScan(projectPath);
        const issues = [];
        const recommendations = [];
        if (!state.aeosInstalled) {
            issues.push("Missing .aeos/AGENT.md.");
            recommendations.push("Copy AEOS Chief/Staff framework into project root as .aeos.");
        }
        if (state.missingCriticalFiles.length > 0) {
            issues.push(`Missing critical AEOS files: ${state.missingCriticalFiles.join(", ")}`);
            recommendations.push("Restore missing critical AEOS framework files.");
        }
        if (scan.detectedLanguages.length === 0) {
            issues.push("No language detected.");
            recommendations.push("Check project path and scanner exclusions.");
        }
        return {
            projectPath,
            runtimeVersion: this.version,
            checkedAt: now(),
            issues,
            recommendations
        };
    }
    modules(projectPath) {
        const state = this.ensureRuntime(projectPath);
        return {
            aeosInstalled: state.aeosInstalled,
            loadedAeosFiles: state.loadedAeosFiles,
            missingCriticalFiles: state.missingCriticalFiles
        };
    }
    scan(projectPath) {
        this.ensureRuntime(projectPath);
        const ignored = new Set([".git", "node_modules", ".aeos-runtime", "dist", "build", "target", ".venv", "venv", "__pycache__", ".idea", ".vscode"]);
        const files = [];
        let directoryCount = 0;
        const walk = (dir) => {
            for (const entry of readdirSync(dir)) {
                if (ignored.has(entry))
                    continue;
                const abs = join(dir, entry);
                const st = statSync(abs);
                if (st.isDirectory()) {
                    directoryCount++;
                    walk(abs);
                }
                else if (st.isFile()) {
                    files.push(relative(projectPath, abs).replaceAll("\\", "/"));
                }
            }
        };
        walk(projectPath);
        const scan = {
            projectPath,
            scannedAt: now(),
            fileCount: files.length,
            directoryCount,
            detectedLanguages: this.detectLanguages(files),
            detectedBuildTools: this.detectBuildTools(files),
            manifests: this.detectManifests(files),
            testIndicators: files.filter((file) => file.toLowerCase().includes("test") || file.toLowerCase().includes("spec") || file.startsWith("tests/") || file.startsWith("src/test/")),
            ciIndicators: files.filter((file) => file.startsWith(".github/workflows/") || file.includes("gitlab-ci") || file.includes("azure-pipelines")),
            dockerIndicators: files.filter((file) => file.endsWith("Dockerfile") || file.includes("docker-compose")),
            aeosInstalled: existsSync(join(projectPath, ".aeos", "AGENT.md")),
            packageJson: this.readPackageJson(projectPath)
        };
        writeJson(join(projectPath, ".aeos-runtime", "scan", "project-scan.json"), scan);
        this.evidence(projectPath, "Repository scan completed", "config", ".aeos-runtime/scan/project-scan.json");
        return scan;
    }
    exportState(projectPath) {
        return {
            state: this.ensureRuntime(projectPath),
            doctor: this.doctor(projectPath),
            scan: this.loadOrCreateScan(projectPath),
            gates: this.gatesPlan(projectPath),
            gateResults: this.gatesResults(projectPath),
            tasks: this.tasks(projectPath),
            evidence: this.evidenceList(projectPath),
            memory: this.memoryList(projectPath),
            provider: this.providerStatus(projectPath),
            agentRuns: this.agentRuns(projectPath),
            latestReport: this.reportLatest(projectPath)
        };
    }
    gatesPlan(projectPath) {
        const scan = this.loadOrCreateScan(projectPath);
        const gates = [];
        if (scan.detectedBuildTools.includes("npm/node") && scan.packageJson.scripts.includes("build")) {
            gates.push({ gateId: "npm-build", title: "NPM build", command: "npm", args: ["run", "build"], timeoutMs: 120000 });
        }
        if (scan.detectedBuildTools.includes("npm/node") && scan.packageJson.scripts.includes("test")) {
            gates.push({ gateId: "npm-test", title: "NPM test", command: "npm", args: ["test"], timeoutMs: 120000 });
        }
        if (scan.detectedBuildTools.includes("maven")) {
            gates.push({ gateId: "java-maven-test", title: "Maven test", command: "mvn", args: ["test"], timeoutMs: 180000 });
        }
        if (scan.detectedBuildTools.includes("gradle")) {
            gates.push({ gateId: "java-gradle-test", title: "Gradle test", command: "gradle", args: ["test"], timeoutMs: 180000 });
        }
        if (scan.detectedLanguages.includes("Python")) {
            gates.push({ gateId: "python-compileall", title: "Python compileall", command: "python", args: ["-m", "compileall", "-q", "."], timeoutMs: 180000 });
            gates.push({ gateId: "python-pytest", title: "Python pytest", command: "python", args: ["-m", "pytest", "-q"], timeoutMs: 180000 });
        }
        writeJson(join(projectPath, ".aeos-runtime", "gates", "gate-plan.json"), gates);
        return gates;
    }
    gatesResults(projectPath) {
        const dir = join(projectPath, ".aeos-runtime", "gates");
        if (!existsSync(dir))
            return [];
        return readdirSync(dir)
            .filter((name) => name.startsWith("gate-result-") && name.endsWith(".json"))
            .map((name) => readJson(join(dir, name)))
            .filter((item) => item !== null)
            .sort((a, b) => a.startedAt.localeCompare(b.startedAt));
    }
    async gateRun(projectPath, gateId) {
        const gate = this.gatesPlan(projectPath).find((item) => item.gateId === gateId);
        if (!gate)
            throw new Error(`Gate not available for this project: ${gateId}`);
        const allowed = new Set(["npm-build", "npm-test", "java-maven-test", "java-gradle-test", "python-pytest", "python-compileall"]);
        if (!allowed.has(gate.gateId))
            throw new Error(`Gate is not allowlisted: ${gate.gateId}`);
        const startedAt = now();
        const result = await new Promise((resolve) => {
            const child = spawn(gate.command, gate.args, { cwd: projectPath, shell: process.platform === "win32" });
            let stdout = "";
            let stderr = "";
            let timedOut = false;
            const timer = setTimeout(() => {
                timedOut = true;
                child.kill("SIGTERM");
            }, gate.timeoutMs);
            child.stdout.on("data", (chunk) => { stdout += chunk.toString("utf8"); });
            child.stderr.on("data", (chunk) => { stderr += chunk.toString("utf8"); });
            child.on("close", (code) => {
                clearTimeout(timer);
                resolve({
                    gateId,
                    command: gate.command,
                    args: gate.args,
                    cwd: projectPath,
                    exitCode: code,
                    timedOut,
                    stdout: truncateText(stdout),
                    stderr: truncateText(stderr),
                    startedAt,
                    finishedAt: now()
                });
            });
        });
        const rel = `.aeos-runtime/gates/gate-result-${gateId}-${Date.now()}.json`;
        result.resultFile = rel;
        writeJson(join(projectPath, rel), result);
        this.evidence(projectPath, `Gate ${gateId} executed with exit code ${result.exitCode}`, "command", rel);
        return result;
    }
    async audit(projectPath, runGates) {
        const state = this.ensureRuntime(projectPath);
        const scan = this.scan(projectPath);
        const gates = this.gatesPlan(projectPath);
        if (runGates) {
            for (const gate of gates) {
                await this.gateRun(projectPath, gate.gateId);
            }
        }
        const results = this.gatesResults(projectPath);
        const failed = results.filter((result) => result.exitCode !== 0);
        const issues = [];
        if (!state.aeosInstalled)
            issues.push("AEOS framework not installed.");
        if (state.missingCriticalFiles.length > 0)
            issues.push("Critical AEOS files missing.");
        if (gates.length === 0)
            issues.push("No quality gates detected.");
        if (failed.length > 0)
            issues.push(`${failed.length} gate(s) failed.`);
        const recommendations = issues.length === 0 ? [] : [
            "Generate remediation plan with `aeos remediate plan`.",
            "Generate backlog with `aeos backlog generate`.",
            "Fix failed gates first.",
            "Re-run `aeos audit run-gates`."
        ];
        const score = Math.max(0, Number((10 - issues.length * 1.5).toFixed(2)));
        const report = {
            reportId: id(),
            projectPath,
            createdAt: now(),
            runtimeVersion: this.version,
            score,
            summary: issues.length ? "AEOS audit found issues." : "No blocking AEOS audit issues detected.",
            scan,
            gates,
            gateResults: results,
            issues,
            recommendations
        };
        const base = join(projectPath, ".aeos-runtime", "reports", `audit-${report.reportId}`);
        writeJson(`${base}.json`, report);
        writeFileSync(`${base}.md`, this.renderAuditMarkdown(report), "utf8");
        this.evidence(projectPath, "AEOS audit report generated", "config", `.aeos-runtime/reports/audit-${report.reportId}.json`);
        return report;
    }
    reportLatest(projectPath) {
        const latest = this.latestAudit(projectPath);
        return latest ? { latestReport: latest } : { message: "No audit report found." };
    }
    providerConfigureOllama(projectPath, baseUrl, model) {
        this.ensureRuntime(projectPath);
        const config = {
            provider: "ollama",
            baseUrl,
            model,
            updatedAt: now()
        };
        writeJson(join(projectPath, ".aeos-runtime", "providers", "provider-config.json"), config);
        this.evidence(projectPath, "Ollama provider configured", "config", ".aeos-runtime/providers/provider-config.json");
        return config;
    }
    providerStatus(projectPath) {
        this.ensureRuntime(projectPath);
        const config = readJson(join(projectPath, ".aeos-runtime", "providers", "provider-config.json"));
        return config ?? {
            configured: false,
            message: "No provider configured. Use: aeos provider configure ollama http://localhost:11434 <model> <projectPath>"
        };
    }
    async providerModels(projectPath) {
        this.ensureRuntime(projectPath);
        const config = readJson(join(projectPath, ".aeos-runtime", "providers", "provider-config.json"));
        const baseUrl = (config?.baseUrl ?? "http://localhost:11434").replace(/\/$/, "");
        const response = await fetch(`${baseUrl}/api/tags`, {
            method: "GET"
        });
        if (!response.ok) {
            const text = await response.text();
            throw new Error(`Ollama models request failed: HTTP ${response.status} ${text}`);
        }
        const data = await response.json();
        const models = (data.models ?? []).map((model) => ({
            name: model.name ?? model.model ?? "unknown",
            modifiedAt: model.modified_at,
            size: model.size,
            digest: model.digest,
            details: model.details
        }));
        return {
            provider: "ollama",
            baseUrl,
            count: models.length,
            models
        };
    }
    async agentRun(projectPath, objective, provider, modelOverride) {
        if (provider !== "ollama") {
            throw new Error("v9 supports real execution only for provider: ollama");
        }
        this.ensureRuntime(projectPath);
        const providerConfig = readJson(join(projectPath, ".aeos-runtime", "providers", "provider-config.json"));
        const baseUrl = providerConfig?.baseUrl ?? "http://localhost:11434";
        const model = modelOverride || providerConfig?.model;
        if (!model) {
            throw new Error("Missing Ollama model. Use: aeos provider configure ollama http://localhost:11434 <model> <projectPath>");
        }
        const runId = id();
        const startedAt = now();
        const prompt = this.renderAgentPrompt(projectPath, objective);
        const promptRel = `.aeos-runtime/agent-runs/agent-prompt-${objective}-${runId}.md`;
        const responseRel = `.aeos-runtime/agent-runs/agent-response-${objective}-${runId}.md`;
        const runRel = `.aeos-runtime/agent-runs/agent-run-${objective}-${runId}.json`;
        writeFileSync(join(projectPath, promptRel), `${prompt}\n`, "utf8");
        let success = false;
        let error;
        let responseText = "";
        try {
            responseText = await this.callOllama(baseUrl, model, prompt);
            success = true;
        }
        catch (err) {
            error = err instanceof Error ? err.message : String(err);
            responseText = [
                "# AEOS Agent Run Failed",
                "",
                `- Objective: ${objective}`,
                `- Provider: ${provider}`,
                `- Model: ${model}`,
                `- Error: ${error}`
            ].join("\n");
        }
        writeFileSync(join(projectPath, responseRel), `${responseText}\n`, "utf8");
        const run = {
            runId,
            objective,
            provider,
            model,
            projectPath,
            promptPath: promptRel,
            responsePath: responseRel,
            startedAt,
            finishedAt: now(),
            success,
            error
        };
        writeJson(join(projectPath, runRel), run);
        this.evidence(projectPath, `AEOS agent run ${objective} completed with success=${success}`, "command", runRel);
        this.memory(projectPath, success ? "evidence" : "finding", `Agent run ${objective} using ${provider}/${model}: success=${success}`);
        return run;
    }
    agentRuns(projectPath) {
        const dir = join(projectPath, ".aeos-runtime", "agent-runs");
        if (!existsSync(dir))
            return [];
        return readdirSync(dir)
            .filter((name) => name.startsWith("agent-run-") && name.endsWith(".json"))
            .map((name) => readJson(join(dir, name)))
            .filter((item) => item !== null)
            .sort((a, b) => a.startedAt.localeCompare(b.startedAt));
    }
    agentLatest(projectPath) {
        const runs = this.agentRuns(projectPath);
        if (runs.length === 0) {
            return { message: "No agent runs found." };
        }
        const latest = runs[runs.length - 1];
        const responseAbs = join(projectPath, latest.responsePath);
        return {
            latest,
            response: existsSync(responseAbs) ? readFileSync(responseAbs, "utf8") : null
        };
    }
    promptAudit(projectPath) {
        const content = [
            "# AEOS Chief/Staff Audit Prompt",
            "",
            this.renderContextPack(projectPath),
            "",
            "## Mission",
            "",
            "Audit the repository with evidence-first Staff/Chief rigor. No claim without file, command, test or report evidence.",
            "",
            "## Required output",
            "",
            "- Executive summary.",
            "- Evidence table.",
            "- Findings by severity.",
            "- Fix plan.",
            "- Required ADRs.",
            "- Required tests/gates.",
            "- Final score with deductions."
        ].join("\n");
        return this.artifact(projectPath, "prompts", "audit-prompt", "prompt", content);
    }
    promptFix(projectPath, finding) {
        const content = [
            "# AEOS Fix Prompt",
            "",
            "## Finding",
            finding,
            "",
            "## Execution rules",
            "",
            "1. Reproduce or confirm the finding.",
            "2. Identify root cause.",
            "3. Apply minimal safe fix.",
            "4. Run impacted gates.",
            "5. Register evidence.",
            "6. Add lesson if reusable."
        ].join("\n");
        return this.artifact(projectPath, "prompts", `fix-${slug(finding)}`, "prompt", content);
    }
    promptMigration(projectPath, target) {
        const content = [
            "# AEOS Migration Prompt",
            "",
            "## Target",
            target,
            "",
            this.renderContextPack(projectPath),
            "",
            "## Migration protocol",
            "",
            "1. Inspect manifests.",
            "2. Identify breaking changes.",
            "3. Create ADR if architecture/dependency behavior changes.",
            "4. Apply incremental changes.",
            "5. Run gates.",
            "6. Produce evidence-backed report."
        ].join("\n");
        return this.artifact(projectPath, "prompts", `migration-${slug(target)}`, "prompt", content);
    }
    subagentsPlan(projectPath, objective) {
        const content = [
            "# AEOS Subagent Plan",
            "",
            "## Objective",
            objective,
            "",
            "## Agents",
            "",
            "1. Root/Chief Agent — owns integration, evidence and final acceptance.",
            "2. Architecture Specialist — architecture, ADRs, boundaries.",
            "3. Implementation Specialist — code impact and safe changes.",
            "4. Verification Specialist — gates, tests, reproducibility.",
            "5. Security/Governance Specialist — security, compliance, clinical risk.",
            "6. JudgeAgent — independent final review.",
            "",
            "## Contract",
            "",
            "Each agent must return: files inspected, evidence, risks, commands run, findings, recommendation."
        ].join("\n");
        return this.artifact(projectPath, "subagents", `subagents-${slug(objective)}`, "subagents", content);
    }
    adrCreate(projectPath, title, decision) {
        const content = [
            `# ADR: ${title}`,
            "",
            "## Status",
            "Proposed",
            "",
            "## Context",
            "Pending evidence.",
            "",
            "## Decision",
            decision,
            "",
            "## Consequences",
            "- Positive: TBD.",
            "- Negative: TBD.",
            "",
            "## Validation",
            "- Run AEOS gates.",
            "- Attach evidence."
        ].join("\n");
        return this.artifact(projectPath, "adrs", `adr-${slug(title)}`, "adr", content);
    }
    lessonAdd(projectPath, summary) {
        this.memory(projectPath, "lesson", summary);
        const content = [
            "# AEOS Lesson",
            "",
            "## Summary",
            summary,
            "",
            "## What to do",
            "- Convert into concrete prevention guidance.",
            "",
            "## What not to do",
            "- Do not repeat the root cause.",
            "",
            "## Promotion",
            "Candidate. Promote only after validation."
        ].join("\n");
        return this.artifact(projectPath, "lessons", `lesson-${slug(summary)}`, "lesson", content);
    }
    bridge(projectPath, tool) {
        const content = [
            `# AEOS ${tool} Bridge`,
            "",
            "Load `.aeos/AGENT.md` first. Then use the context below.",
            "",
            this.renderContextPack(projectPath),
            "",
            "## Tool guidance",
            this.toolGuidance(tool)
        ].join("\n");
        return this.artifact(projectPath, "bridges", `${tool}-bridge`, "bridge", content);
    }
    contextPack(projectPath) {
        return this.artifact(projectPath, "context", "aeos-context-pack", "context", this.renderContextPack(projectPath));
    }
    remediatePlan(projectPath) {
        const latest = this.latestAudit(projectPath);
        const failed = this.gatesResults(projectPath).filter((result) => result.exitCode !== 0);
        const content = [
            "# AEOS Remediation Plan",
            "",
            `- Latest audit score: ${latest?.score ?? "no audit"}`,
            "",
            "## Failed gates",
            failed.length ? failed.map((gate) => `- ${gate.gateId}: exitCode=${gate.exitCode}, result=${gate.resultFile}`).join("\n") : "- None",
            "",
            "## Order",
            "1. Environment/tooling blockers.",
            "2. Syntax/compile failures.",
            "3. Test failures.",
            "4. Architecture/security/governance findings.",
            "5. Re-run audit."
        ].join("\n");
        return this.artifact(projectPath, "remediation", "remediation-plan", "remediation", content);
    }
    backlogGenerate(projectPath) {
        const latest = this.latestAudit(projectPath);
        const failed = this.gatesResults(projectPath).filter((result) => result.exitCode !== 0);
        const lines = ["# AEOS Technical Backlog", "", `- Generated at: ${now()}`, ""];
        let n = 1;
        for (const issue of (latest?.issues ?? [])) {
            lines.push(`## AEOS-${String(n++).padStart(3, "0")} Resolve audit issue`, "", `- Issue: ${issue}`, "- Acceptance: issue removed from next audit.", "");
        }
        for (const gate of failed) {
            lines.push(`## AEOS-${String(n++).padStart(3, "0")} Fix failing gate ${gate.gateId}`, "", `- Result: ${gate.resultFile ?? "unknown"}`, `- Acceptance: ${gate.gateId} exits with code 0.`, "");
        }
        if (n === 1) {
            lines.push("## AEOS-001 Maintain clean baseline", "", "- Acceptance: next AEOS audit remains clean.", "");
        }
        return this.artifact(projectPath, "backlog", "technical-backlog", "backlog", lines.join("\n"));
    }
    workflowAudit(projectPath) {
        const content = [
            "# AEOS Audit Workflow",
            "",
            "1. aeos doctor <project>",
            "2. aeos scan <project>",
            "3. aeos gates plan <project>",
            "4. aeos audit run-gates <project>",
            "5. aeos context pack <project>",
            "6. aeos remediate plan <project>",
            "7. aeos backlog generate <project>"
        ].join("\n");
        return this.artifact(projectPath, "workflows", "audit-workflow", "workflow", content);
    }
    workflowFix(projectPath, finding) {
        const content = [
            "# AEOS Fix Workflow",
            "",
            "## Finding",
            finding,
            "",
            "1. Confirm evidence.",
            "2. Root-cause.",
            "3. Patch.",
            "4. Run gate.",
            "5. Register evidence.",
            "6. Re-run audit."
        ].join("\n");
        return this.artifact(projectPath, "workflows", `fix-${slug(finding)}`, "workflow", content);
    }
    runbookGenerate(projectPath) {
        const content = [
            "# AEOS Project Runbook",
            "",
            "## Daily",
            "aeos doctor .",
            "aeos scan .",
            "aeos audit .",
            "",
            "## Before change",
            "aeos context pack .",
            "aeos workflow audit .",
            "",
            "## After change",
            "aeos audit run-gates .",
            "aeos remediate plan .",
            "aeos backlog generate ."
        ].join("\n");
        return this.artifact(projectPath, "runbooks", "project-runbook", "runbook", content);
    }
    policyGenerate(projectPath) {
        const content = [
            "# AEOS Execution Policy",
            "",
            "- No claim without evidence.",
            "- No completion without verification.",
            "- No architecture change without ADR.",
            "- No clinical/regulatory/security-impacting decision without human review.",
            "- No arbitrary shell execution outside allowlisted gates."
        ].join("\n");
        return this.artifact(projectPath, "policies", "execution-policy", "policy", content);
    }
    ciGithub(projectPath) {
        const scan = this.loadOrCreateScan(projectPath);
        const steps = ["      - uses: actions/checkout@v4"];
        if (scan.detectedBuildTools.includes("npm/node")) {
            steps.push("      - uses: actions/setup-node@v4");
            steps.push("        with:");
            steps.push("          node-version: '20'");
            steps.push("      - run: npm ci");
            if (scan.packageJson.scripts.includes("build"))
                steps.push("      - run: npm run build");
            if (scan.packageJson.scripts.includes("test"))
                steps.push("      - run: npm test");
        }
        if (scan.detectedLanguages.includes("Python")) {
            steps.push("      - uses: actions/setup-python@v5");
            steps.push("        with:");
            steps.push("          python-version: '3.11'");
            steps.push("      - run: python -m compileall -q .");
            steps.push("      - run: python -m pytest -q");
        }
        if (scan.detectedBuildTools.includes("maven")) {
            steps.push("      - uses: actions/setup-java@v4");
            steps.push("        with:");
            steps.push("          distribution: 'temurin'");
            steps.push("          java-version: '21'");
            steps.push("      - run: mvn test");
        }
        const content = [
            "# AEOS GitHub Actions Workflow",
            "",
            "Save as `.github/workflows/aeos-quality.yml`.",
            "",
            "```yaml",
            "name: AEOS Quality Gates",
            "on:",
            "  pull_request:",
            "  push:",
            "    branches: [ main ]",
            "jobs:",
            "  quality:",
            "    runs-on: ubuntu-latest",
            "    steps:",
            ...steps,
            "```"
        ].join("\n");
        return this.artifact(projectPath, "ci", "github-actions-aeos-quality", "ci", content);
    }
    releaseCheck(projectPath) {
        const latest = this.latestAudit(projectPath);
        const failed = this.gatesResults(projectPath).filter((result) => result.exitCode !== 0);
        const content = [
            "# AEOS Release Readiness",
            "",
            `- Latest audit score: ${latest?.score ?? "no audit"}`,
            `- Failed gates: ${failed.length}`,
            "",
            "- [ ] Latest audit exists.",
            "- [ ] No failed critical gate.",
            "- [ ] Evidence ledger contains current validation evidence.",
            "- [ ] ADRs created for architecture changes.",
            "- [ ] Security/governance risks reviewed.",
            "- [ ] Rollback plan documented.",
            "",
            failed.length === 0 ? "Decision: release may proceed after human review." : "Decision: release should not proceed before failed gates are resolved or accepted."
        ].join("\n");
        return this.artifact(projectPath, "release", "release-readiness", "release", content);
    }
    providerTemplate(projectPath, provider) {
        const envVar = provider === "openai" ? "OPENAI_API_KEY" : provider === "anthropic" ? "ANTHROPIC_API_KEY" : "OLLAMA_BASE_URL";
        const content = [
            `# AEOS Provider Template — ${provider}`,
            "",
            `- Required env: ${envVar}`,
            "",
            "## Rules",
            "- Provider output is not evidence.",
            "- Validate provider output with repo files, gates and judge.",
            "- Do not send secrets or sensitive data unless explicitly authorized and compliant.",
            "",
            provider === "ollama" ? "## v9 status\n\nOllama is executable in v9 through `aeos agent run ... ollama`." : "## v9 status\n\nThis is a template only. Cloud execution is intentionally not enabled in v9."
        ].join("\n");
        return this.artifact(projectPath, "providers", `${provider}-provider-template`, "provider", content);
    }
    plan(projectPath, objective) {
        this.ensureRuntime(projectPath);
        const task = {
            taskId: id(),
            objective,
            status: "planned",
            createdAt: now(),
            updatedAt: now(),
            acceptanceCriteria: [
                "Repository context inspected.",
                "Evidence requirements defined.",
                "Quality gates identified.",
                "Judge review required."
            ],
            specialistTasks: [
                { specialistId: id(), role: "Architecture Specialist", objective: "Assess architecture impact.", status: "pending" },
                { specialistId: id(), role: "Implementation Specialist", objective: "Assess implementation scope.", status: "pending" },
                { specialistId: id(), role: "Verification Specialist", objective: "Run or define gates.", status: "pending" },
                { specialistId: id(), role: "JudgeAgent", objective: "Review evidence.", status: "pending" }
            ]
        };
        writeJson(join(projectPath, ".aeos-runtime", "tasks", `${task.taskId}.json`), task);
        return task;
    }
    tasks(projectPath) {
        const dir = join(projectPath, ".aeos-runtime", "tasks");
        if (!existsSync(dir))
            return [];
        return readdirSync(dir).filter((name) => name.endsWith(".json")).map((name) => readJson(join(dir, name))).filter((item) => item !== null);
    }
    task(projectPath, taskId) {
        const task = readJson(join(projectPath, ".aeos-runtime", "tasks", `${taskId}.json`));
        if (!task)
            throw new Error(`Task not found: ${taskId}`);
        return task;
    }
    checkpoint(projectPath, summary) {
        const cp = { checkpointId: id(), timestamp: now(), projectPath, summary, taskIds: this.tasks(projectPath).map((task) => task.taskId) };
        writeJson(join(projectPath, ".aeos-runtime", "checkpoints", `${cp.checkpointId}.json`), cp);
        return cp;
    }
    checkpoints(projectPath) {
        const dir = join(projectPath, ".aeos-runtime", "checkpoints");
        if (!existsSync(dir))
            return [];
        return readdirSync(dir).filter((name) => name.endsWith(".json")).map((name) => readJson(join(dir, name))).filter((item) => item !== null);
    }
    evidenceAdd(projectPath, claim, type, reference) {
        const e = { evidenceId: id(), type, claim, reference, verified: true, timestamp: now(), limitations: [] };
        appendJsonl(join(projectPath, ".aeos-runtime", "evidence", "evidence.jsonl"), e);
        return e;
    }
    evidenceList(projectPath) {
        return readJsonl(join(projectPath, ".aeos-runtime", "evidence", "evidence.jsonl"));
    }
    memoryAdd(projectPath, type, summary) {
        const m = { id: id(), type, summary, timestamp: now(), evidenceIds: [] };
        appendJsonl(join(projectPath, ".aeos-runtime", "memory", "memory.jsonl"), m);
        return m;
    }
    memoryList(projectPath) {
        return readJsonl(join(projectPath, ".aeos-runtime", "memory", "memory.jsonl"));
    }
    judge(projectPath, taskId) {
        const task = this.task(projectPath, taskId);
        const evidence = this.evidenceList(projectPath);
        const deductions = [];
        if (evidence.length === 0)
            deductions.push("No evidence registered.");
        if (task.specialistTasks.some((specialist) => specialist.status !== "done"))
            deductions.push("Specialist tasks are not complete.");
        const score = Math.max(0, 10 - deductions.length * 2);
        const report = { reportId: id(), taskId, decision: deductions.length === 0 ? "accept" : "needs_rework", score, deductions, timestamp: now() };
        writeJson(join(projectPath, ".aeos-runtime", "judge-reports", `${report.reportId}.json`), report);
        return report;
    }
    snapshotCreate(projectPath) {
        const snapshot = [
            "# AEOS Snapshot",
            "",
            `- Project: ${projectPath}`,
            `- Created at: ${now()}`,
            "",
            "## State",
            "```json",
            JSON.stringify(this.exportState(projectPath), null, 2),
            "```"
        ].join("\n");
        return this.artifact(projectPath, "snapshots", "aeos-snapshot", "snapshot", snapshot);
    }
    checklistGenerate(projectPath) {
        const content = [
            "# AEOS Operational Checklist",
            "",
            "- [ ] Runtime initialized.",
            "- [ ] .aeos framework installed.",
            "- [ ] Scan completed.",
            "- [ ] Gates planned.",
            "- [ ] Audit run.",
            "- [ ] Agent provider configured.",
            "- [ ] Agent run completed.",
            "- [ ] Failed gates triaged.",
            "- [ ] Remediation plan generated.",
            "- [ ] Backlog generated.",
            "- [ ] Snapshot generated."
        ].join("\n");
        return this.artifact(projectPath, "checklists", "operational-checklist", "checklist", content);
    }
    deliveryPackage(projectPath) {
        const content = [
            "# AEOS Delivery Package",
            "",
            `- Project: ${projectPath}`,
            `- Generated at: ${now()}`,
            "",
            "## Included references",
            "- Latest audit report.",
            "- Context pack.",
            "- Agent run.",
            "- Remediation plan.",
            "- Technical backlog.",
            "- Release checklist.",
            "- Snapshot.",
            "",
            "## Handoff",
            "Use this package as the release/handoff entrypoint for human or agent review."
        ].join("\n");
        return this.artifact(projectPath, "delivery", "delivery-package", "delivery", content);
    }
    async callOllama(baseUrl, model, prompt) {
        const cleanBaseUrl = baseUrl.replace(/\/$/, "");
        const response = await fetch(`${cleanBaseUrl}/api/generate`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                model,
                prompt,
                stream: false
            })
        });
        if (!response.ok) {
            const text = await response.text();
            throw new Error(`Ollama request failed: HTTP ${response.status} ${text}`);
        }
        const data = await response.json();
        if (data.error) {
            throw new Error(data.error);
        }
        return data.response ?? "";
    }
    renderAgentPrompt(projectPath, objective) {
        const base = [
            "# AEOS Agent Runtime Prompt",
            "",
            "You are operating under AEOS Chief/Staff Edition.",
            "",
            "## Non-negotiable rules",
            "",
            "- Do not hallucinate.",
            "- Do not claim repository facts that are not present in the provided context.",
            "- Provider output is not evidence by itself.",
            "- Produce clear recommendations, but do not pretend commands were executed unless the context contains gate results.",
            "- Security, clinical and regulatory issues must be treated as high-risk.",
            "",
            "## Context",
            "",
            this.renderContextPack(projectPath),
            ""
        ];
        if (objective === "audit") {
            base.push("## Objective: audit", "", "Produce an evidence-aware audit with:", "", "- Executive summary.", "- Architecture findings.", "- Test/gate findings.", "- Security/governance findings.", "- AI/RAG/training findings if present.", "- Prioritized remediation plan.", "- Final score with explicit deductions.");
        }
        if (objective === "remediate") {
            base.push("## Objective: remediate", "", "Produce a practical remediation plan with:", "", "- Root issue categories.", "- Fix order.", "- Commands/gates to run.", "- Risks.", "- Backlog items.", "- Acceptance criteria.");
        }
        if (objective === "judge") {
            base.push("## Objective: judge", "", "Review whether the current project state is acceptable:", "", "- Check evidence adequacy.", "- Check gate results.", "- Identify missing proof.", "- Decide: accept, needs_rework, block.", "- Give score with deductions.");
        }
        return base.join("\n");
    }
    ensureRuntime(projectPath) {
        const runtimeDir = join(projectPath, ".aeos-runtime");
        const folders = [
            "tasks", "checkpoints", "memory", "evidence", "judge-reports", "scan", "gates", "reports",
            "prompts", "subagents", "adrs", "lessons", "bridges", "context", "remediation", "backlog",
            "workflows", "runbooks", "policies", "ci", "release", "providers", "snapshots", "checklists",
            "delivery", "agent-runs"
        ];
        mkdirSync(runtimeDir, { recursive: true });
        for (const folder of folders)
            mkdirSync(join(runtimeDir, folder), { recursive: true });
        const statePath = join(runtimeDir, "runtime-state.json");
        const previous = readJson(statePath);
        const aeosPath = join(projectPath, ".aeos");
        const loadedAeosFiles = existsSync(aeosPath)
            ? ["foundation", "execution", "reasoning", "knowledge", "engineering", "verification", "governance", "operations"]
                .map((folder) => listMd(join(aeosPath, folder)).length)
                .reduce((a, b) => a + b, 0) + (existsSync(join(aeosPath, "AGENT.md")) ? 1 : 0)
            : 0;
        const missingCriticalFiles = this.criticalFiles.filter((file) => !existsSync(join(aeosPath, file)));
        const timestamp = now();
        const state = {
            projectPath,
            runtimePath: runtimeDir,
            initializedAt: previous?.initializedAt ?? timestamp,
            updatedAt: timestamp,
            version: this.version,
            aeosInstalled: existsSync(join(aeosPath, "AGENT.md")),
            loadedAeosFiles,
            missingCriticalFiles
        };
        writeJson(statePath, state);
        return state;
    }
    loadOrCreateScan(projectPath) {
        return readJson(join(projectPath, ".aeos-runtime", "scan", "project-scan.json")) ?? this.scan(projectPath);
    }
    detectLanguages(files) {
        const langs = new Set();
        for (const file of files) {
            if (file.endsWith(".ts") || file.endsWith(".tsx"))
                langs.add("TypeScript");
            if (file.endsWith(".js") || file.endsWith(".jsx") || file.endsWith(".mjs") || file.endsWith(".cjs"))
                langs.add("JavaScript");
            if (file.endsWith(".py"))
                langs.add("Python");
            if (file.endsWith(".java"))
                langs.add("Java");
            if (file.endsWith(".kt") || file.endsWith(".kts"))
                langs.add("Kotlin");
            if (file.endsWith(".go"))
                langs.add("Go");
            if (file.endsWith(".rs"))
                langs.add("Rust");
            if (file.endsWith(".cs"))
                langs.add("C#");
            if (file.endsWith(".tf"))
                langs.add("Terraform");
            if (file.endsWith(".sql"))
                langs.add("SQL");
        }
        return [...langs].sort();
    }
    detectBuildTools(files) {
        const tools = new Set();
        if (files.includes("package.json"))
            tools.add("npm/node");
        if (files.includes("pom.xml"))
            tools.add("maven");
        if (files.some((file) => file.endsWith("build.gradle") || file.endsWith("build.gradle.kts")))
            tools.add("gradle");
        if (files.includes("pyproject.toml"))
            tools.add("python-pyproject");
        if (files.includes("requirements.txt"))
            tools.add("python-requirements");
        return [...tools].sort();
    }
    detectManifests(files) {
        const known = ["package.json", "pom.xml", "build.gradle", "build.gradle.kts", "pyproject.toml", "requirements.txt", "Dockerfile", "docker-compose.yml", "docker-compose.yaml"];
        return files.filter((file) => known.includes(file));
    }
    readPackageJson(projectPath) {
        const path = join(projectPath, "package.json");
        if (!existsSync(path))
            return { exists: false, scripts: [] };
        try {
            const parsed = JSON.parse(readFileSync(path, "utf8"));
            return { exists: true, scripts: Object.keys(parsed.scripts ?? {}).sort() };
        }
        catch {
            return { exists: true, scripts: [] };
        }
    }
    evidence(projectPath, claim, type, reference) {
        this.evidenceAdd(projectPath, claim, type, reference);
    }
    memory(projectPath, type, summary) {
        this.memoryAdd(projectPath, type, summary);
    }
    renderAuditMarkdown(report) {
        return [
            "# AEOS Audit Report",
            "",
            `- Report ID: ${report.reportId}`,
            `- Score: ${report.score}/10`,
            "",
            "## Summary",
            report.summary,
            "",
            "## Issues",
            report.issues.length ? report.issues.map((issue) => `- ${issue}`).join("\n") : "- None",
            "",
            "## Recommendations",
            report.recommendations.length ? report.recommendations.map((item) => `- ${item}`).join("\n") : "- None"
        ].join("\n");
    }
    renderContextPack(projectPath) {
        const state = this.ensureRuntime(projectPath);
        const scan = this.loadOrCreateScan(projectPath);
        const latest = this.latestAudit(projectPath);
        return [
            "# AEOS Context Pack",
            "",
            `- Project: ${projectPath}`,
            `- Runtime: ${state.version}`,
            `- Generated at: ${now()}`,
            "",
            "## Repository",
            `- Languages: ${scan.detectedLanguages.join(", ") || "none"}`,
            `- Build tools: ${scan.detectedBuildTools.join(", ") || "none"}`,
            `- Manifests: ${scan.manifests.join(", ") || "none"}`,
            `- Files: ${scan.fileCount}`,
            "",
            "## Latest audit",
            latest ? `- Score: ${latest.score}/10\n- Summary: ${latest.summary}` : "- No audit found.",
            "",
            "## Gate results",
            this.gatesResults(projectPath).slice(-10).map((gate) => `- ${gate.gateId}: exitCode=${gate.exitCode}`).join("\n") || "- None"
        ].join("\n");
    }
    toolGuidance(tool) {
        if (tool === "opencode")
            return "Point OpenCode instructions to `.aeos/AGENT.md`; use generated prompts as task specs.";
        if (tool === "codex")
            return "Paste the context pack before implementation requests and require evidence-backed changes.";
        return "Add `.aeos/AGENT.md` and generated bridge/context files to Cursor project rules.";
    }
    latestAudit(projectPath) {
        const dir = join(projectPath, ".aeos-runtime", "reports");
        if (!existsSync(dir))
            return null;
        const reports = readdirSync(dir)
            .filter((name) => name.endsWith(".json"))
            .map((name) => ({ path: join(dir, name), modified: statSync(join(dir, name)).mtime.toISOString() }))
            .sort((a, b) => b.modified.localeCompare(a.modified));
        return reports.length ? readJson(reports[0].path) : null;
    }
    artifact(projectPath, folder, base, type, content) {
        const artifactId = id();
        const rel = `.aeos-runtime/${folder}/${base}-${artifactId}.md`;
        const abs = join(projectPath, rel);
        mkdirSync(dirname(abs), { recursive: true });
        writeFileSync(abs, `${content}\n`, "utf8");
        this.memory(projectPath, "finding", `Generated ${type} artifact: ${rel}`);
        return { artifactId, type, path: rel, createdAt: now() };
    }
    count(projectPath, folder) {
        const dir = join(projectPath, ".aeos-runtime", folder);
        if (!existsSync(dir))
            return 0;
        return readdirSync(dir).filter((name) => name.endsWith(".md") || name.endsWith(".json")).length;
    }
}
//# sourceMappingURL=services.js.map