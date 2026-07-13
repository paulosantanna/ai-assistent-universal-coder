#!/usr/bin/env node
import { resolve } from "node:path";
import { AeosCore } from "../core/services.js";
import type { AgentObjective, EvidenceType, MemoryType, ProviderName } from "../core/types.js";
import { handleRun } from "../kernel/cli-run.js";
import { KernelRuntime } from "../kernel/kernel-runtime.js";

const core = new AeosCore();

function help(): void {
  console.log(`
AEOS Runtime Core v0.1 (Governed Vertical Slice)

Kernel (v0.1):
  aeos run <playbook-id> --target <path>
  aeos list-playbooks

v9.1 legacy commands:

Core:
  aeos init [projectPath]
  aeos status [projectPath]
  aeos doctor [projectPath]
  aeos modules [projectPath]
  aeos scan [projectPath]
  aeos export [projectPath]

Gates and audit:
  aeos gates plan [projectPath]
  aeos gates results [projectPath]
  aeos gate run "<gateId>" [projectPath]
  aeos audit [projectPath]
  aeos audit run-gates [projectPath]
  aeos report latest [projectPath]

Provider and agent execution:
  aeos provider configure ollama [baseUrl] [model] [projectPath]
  aeos provider configure deepseek [model] [apiKeyEnv] [projectPath]
  aeos provider configure openai-compatible [baseUrl] [model] [apiKeyEnv] [projectPath]
  aeos provider status [projectPath]
  aeos provider models [projectPath]
  aeos agent run audit ollama [model] [projectPath]
  aeos agent run audit deepseek [model] [projectPath]
  aeos agent run audit openai-compatible [model] [projectPath]
  aeos agent run judge ollama [model] [projectPath]
  aeos agent run remediate ollama [model] [projectPath]
  aeos agent runs [projectPath]
  aeos agent latest [projectPath]

Prompts / agents:
  aeos prompt audit [projectPath]
  aeos prompt fix "<finding>" [projectPath]
  aeos prompt migration "<target>" [projectPath]
  aeos subagents plan "<objective>" [projectPath]
  aeos adr create "<title>" "<decision>" [projectPath]
  aeos lessons add "<summary>" [projectPath]

Bridge / context:
  aeos bridge opencode [projectPath]
  aeos bridge codex [projectPath]
  aeos bridge cursor [projectPath]
  aeos context pack [projectPath]
  aeos remediate plan [projectPath]
  aeos backlog generate [projectPath]

Operationalization:
  aeos workflow audit [projectPath]
  aeos workflow fix "<finding>" [projectPath]
  aeos runbook generate [projectPath]
  aeos policy generate [projectPath]
  aeos ci github [projectPath]
  aeos release check [projectPath]
  aeos provider template openai [projectPath]
  aeos provider template anthropic [projectPath]
  aeos provider template ollama [projectPath]
  aeos provider template deepseek [projectPath]
  aeos provider template openai-compatible [projectPath]

Task/evidence/memory:
  aeos plan "<objective>" [projectPath]
  aeos tasks [projectPath]
  aeos task "<taskId>" [projectPath]
  aeos checkpoint "<summary>" [projectPath]
  aeos checkpoints [projectPath]
  aeos evidence add "<claim>" "<type>" "<reference>" [projectPath]
  aeos evidence list [projectPath]
  aeos memory add "<type>" "<summary>" [projectPath]
  aeos memory list [projectPath]
  aeos judge "<taskId>" [projectPath]

Stable baseline:
  aeos snapshot create [projectPath]
  aeos checklist generate [projectPath]
  aeos delivery package [projectPath]
`.trim());
}

function p(v: string | undefined): string {
  return resolve(v ?? process.cwd());
}

function req(v: string | undefined, name: string): string {
  if (!v || !v.trim()) throw new Error(`Missing required argument: ${name}`);
  return v;
}

function print(v: unknown): void {
  console.log(JSON.stringify(v, null, 2));
}

function evidenceType(v: string): EvidenceType {
  const allowed: EvidenceType[] = ["code", "command", "test", "config", "diff", "source", "benchmark", "security", "clinical", "regulatory"];
  if (!allowed.includes(v as EvidenceType)) throw new Error(`Invalid evidence type: ${v}`);
  return v as EvidenceType;
}

function memoryType(v: string): MemoryType {
  const allowed: MemoryType[] = ["observation", "evidence", "finding", "lesson", "validated_lesson", "golden_knowledge", "principle"];
  if (!allowed.includes(v as MemoryType)) throw new Error(`Invalid memory type: ${v}`);
  return v as MemoryType;
}

function objective(v: string): AgentObjective {
  const allowed: AgentObjective[] = ["audit", "judge", "remediate"];
  if (!allowed.includes(v as AgentObjective)) throw new Error(`Invalid agent objective: ${v}`);
  return v as AgentObjective;
}

function providerName(v: string): ProviderName {
  const allowed: ProviderName[] = ["ollama", "deepseek", "openai-compatible"];
  if (!allowed.includes(v as ProviderName)) throw new Error(`Invalid executable provider: ${v}`);
  return v as ProviderName;
}

async function main(): Promise<void> {
  const [, , command, ...args] = process.argv;

  try {
    switch (command) {
      case undefined:
      case "help":
      case "--help":
      case "-h":
        help(); return;

      case "init": print(core.init(p(args[0]))); return;
      case "status": print(core.status(p(args[0]))); return;
      case "doctor": print(core.doctor(p(args[0]))); return;
      case "modules": print(core.modules(p(args[0]))); return;
      case "scan": print(core.scan(p(args[0]))); return;
      case "export": print(core.exportState(p(args[0]))); return;

      case "gates": {
        const sub = req(args[0], "gates subcommand");
        if (sub === "plan") { print(core.gatesPlan(p(args[1]))); return; }
        if (sub === "results") { print(core.gatesResults(p(args[1]))); return; }
        throw new Error(`Unknown gates subcommand: ${sub}`);
      }

      case "gate": {
        const sub = req(args[0], "gate subcommand");
        if (sub === "run") { print(await core.gateRun(p(args[2]), req(args[1], "gateId"))); return; }
        throw new Error(`Unknown gate subcommand: ${sub}`);
      }

      case "audit": {
        if (args[0] === "run-gates") { print(await core.audit(p(args[1]), true)); return; }
        print(await core.audit(p(args[0]), false)); return;
      }

      case "report": {
        const sub = req(args[0], "report subcommand");
        if (sub === "latest") { print(core.reportLatest(p(args[1]))); return; }
        throw new Error(`Unknown report subcommand: ${sub}`);
      }

      case "provider": {
        const sub = req(args[0], "provider subcommand");
        if (sub === "configure") {
          const provider = providerName(req(args[1], "provider"));
          if (provider === "ollama") {
            print(core.providerConfigureOllama(p(args[4]), req(args[2], "baseUrl"), req(args[3], "model")));
            return;
          }
          if (provider === "deepseek") {
            print(core.providerConfigure(p(args[4]), provider, undefined, req(args[2], "model"), args[3] || "DEEPSEEK_API_KEY"));
            return;
          }
          print(core.providerConfigure(p(args[5]), provider, req(args[2], "baseUrl"), req(args[3], "model"), args[4] || ""));
          return;
        }
        if (sub === "status") {
          print(core.providerStatus(p(args[1])));
          return;
        }
        if (sub === "models") {
          print(await core.providerModels(p(args[1])));
          return;
        }
        if (sub === "template") {
          const provider = req(args[1], "provider name");
          if (provider === "openai" || provider === "anthropic" || provider === "ollama" || provider === "deepseek" || provider === "openai-compatible") { print(core.providerTemplate(p(args[2]), provider)); return; }
        }
        throw new Error(`Unknown provider command.`);
      }

      case "agent": {
        const sub = req(args[0], "agent subcommand");
        if (sub === "run") {
          const obj = objective(req(args[1], "objective"));
          const provider = providerName(req(args[2], "provider"));
          print(await core.agentRun(p(args[4]), obj, provider, args[3]));
          return;
        }
        if (sub === "runs") { print(core.agentRuns(p(args[1]))); return; }
        if (sub === "latest") { print(core.agentLatest(p(args[1]))); return; }
        throw new Error(`Unknown agent subcommand: ${sub}`);
      }

      case "prompt": {
        const sub = req(args[0], "prompt subcommand");
        if (sub === "audit") { print(core.promptAudit(p(args[1]))); return; }
        if (sub === "fix") { print(core.promptFix(p(args[2]), req(args[1], "finding"))); return; }
        if (sub === "migration") { print(core.promptMigration(p(args[2]), req(args[1], "target"))); return; }
        throw new Error(`Unknown prompt subcommand: ${sub}`);
      }

      case "subagents": {
        const sub = req(args[0], "subagents subcommand");
        if (sub === "plan") { print(core.subagentsPlan(p(args[2]), req(args[1], "objective"))); return; }
        throw new Error(`Unknown subagents subcommand: ${sub}`);
      }

      case "adr": {
        const sub = req(args[0], "adr subcommand");
        if (sub === "create") { print(core.adrCreate(p(args[3]), req(args[1], "title"), req(args[2], "decision"))); return; }
        throw new Error(`Unknown adr subcommand: ${sub}`);
      }

      case "lessons": {
        const sub = req(args[0], "lessons subcommand");
        if (sub === "add") { print(core.lessonAdd(p(args[2]), req(args[1], "summary"))); return; }
        throw new Error(`Unknown lessons subcommand: ${sub}`);
      }

      case "bridge": {
        const tool = req(args[0], "bridge tool");
        if (tool === "opencode" || tool === "codex" || tool === "cursor") { print(core.bridge(p(args[1]), tool)); return; }
        throw new Error(`Unknown bridge tool: ${tool}`);
      }

      case "context": {
        const sub = req(args[0], "context subcommand");
        if (sub === "pack") { print(core.contextPack(p(args[1]))); return; }
        throw new Error(`Unknown context subcommand: ${sub}`);
      }

      case "remediate": {
        const sub = req(args[0], "remediate subcommand");
        if (sub === "plan") { print(core.remediatePlan(p(args[1]))); return; }
        throw new Error(`Unknown remediate subcommand: ${sub}`);
      }

      case "backlog": {
        const sub = req(args[0], "backlog subcommand");
        if (sub === "generate") { print(core.backlogGenerate(p(args[1]))); return; }
        throw new Error(`Unknown backlog subcommand: ${sub}`);
      }

      case "workflow": {
        const sub = req(args[0], "workflow subcommand");
        if (sub === "audit") { print(core.workflowAudit(p(args[1]))); return; }
        if (sub === "fix") { print(core.workflowFix(p(args[2]), req(args[1], "finding"))); return; }
        throw new Error(`Unknown workflow subcommand: ${sub}`);
      }

      case "runbook": {
        const sub = req(args[0], "runbook subcommand");
        if (sub === "generate") { print(core.runbookGenerate(p(args[1]))); return; }
        throw new Error(`Unknown runbook subcommand: ${sub}`);
      }

      case "policy": {
        const sub = req(args[0], "policy subcommand");
        if (sub === "generate") { print(core.policyGenerate(p(args[1]))); return; }
        throw new Error(`Unknown policy subcommand: ${sub}`);
      }

      case "ci": {
        const sub = req(args[0], "ci subcommand");
        if (sub === "github") { print(core.ciGithub(p(args[1]))); return; }
        throw new Error(`Unknown ci subcommand: ${sub}`);
      }

      case "release": {
        const sub = req(args[0], "release subcommand");
        if (sub === "check") { print(core.releaseCheck(p(args[1]))); return; }
        throw new Error(`Unknown release subcommand: ${sub}`);
      }

      case "plan": print(core.plan(p(args[1]), req(args[0], "objective"))); return;
      case "tasks": print(core.tasks(p(args[0]))); return;
      case "task": print(core.task(p(args[1]), req(args[0], "taskId"))); return;
      case "checkpoint": print(core.checkpoint(p(args[1]), req(args[0], "summary"))); return;
      case "checkpoints": print(core.checkpoints(p(args[0]))); return;

      case "evidence": {
        const sub = req(args[0], "evidence subcommand");
        if (sub === "add") { print(core.evidenceAdd(p(args[4]), req(args[1], "claim"), evidenceType(req(args[2], "type")), req(args[3], "reference"))); return; }
        if (sub === "list") { print(core.evidenceList(p(args[1]))); return; }
        throw new Error(`Unknown evidence subcommand: ${sub}`);
      }

      case "memory": {
        const sub = req(args[0], "memory subcommand");
        if (sub === "add") { print(core.memoryAdd(p(args[3]), memoryType(req(args[1], "type")), req(args[2], "summary"))); return; }
        if (sub === "list") { print(core.memoryList(p(args[1]))); return; }
        throw new Error(`Unknown memory subcommand: ${sub}`);
      }

      case "judge": print(core.judge(p(args[1]), req(args[0], "taskId"))); return;

      case "snapshot": {
        const sub = req(args[0], "snapshot subcommand");
        if (sub === "create") { print(core.snapshotCreate(p(args[1]))); return; }
        throw new Error(`Unknown snapshot subcommand: ${sub}`);
      }

      case "checklist": {
        const sub = req(args[0], "checklist subcommand");
        if (sub === "generate") { print(core.checklistGenerate(p(args[1]))); return; }
        throw new Error(`Unknown checklist subcommand: ${sub}`);
      }

      case "delivery": {
        const sub = req(args[0], "delivery subcommand");
        if (sub === "package") { print(core.deliveryPackage(p(args[1]))); return; }
        throw new Error(`Unknown delivery subcommand: ${sub}`);
      }

      case "run":
        await handleRun(args);
        return;

      case "list-playbooks": {
        const { detectAeosRoot } = await import("../kernel/cli-run.js");
        const aeosRoot = detectAeosRoot ? detectAeosRoot() : process.cwd();
        const kernel = new KernelRuntime(aeosRoot);
        const playbooks = await kernel.listPlaybooks();
        console.log("\nAvailable Playbooks:");
        for (const pb of playbooks) {
          console.log(`  - ${pb.id} (${pb.name}) [${pb.riskLevel}]`);
        }
        console.log("");
        return;
      }

      default:
        throw new Error(`Unknown command: ${command}`);
    }
  } catch (error) {
    console.error(error instanceof Error ? error.message : String(error));
    process.exitCode = 1;
  }
}

void main();
