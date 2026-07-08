#!/usr/bin/env node
import { resolve } from "node:path";
import type { EvidenceType } from "../types.js";
import { AeosKernel } from "../kernel/AeosKernel.js";

const kernel = new AeosKernel();

function help(): void {
  console.log(`
AEOS Runtime MVP

Usage:
  aeos help
  aeos init [projectPath]
  aeos status [projectPath]
  aeos plan "<objective>" [projectPath]
  aeos checkpoint "<summary>" [projectPath]
  aeos evidence "<claim>" "<type>" "<reference>" [projectPath]
  aeos judge "<taskId>" [projectPath]

Evidence types:
  code, command, test, config, diff, source, benchmark, security, clinical, regulatory
`.trim());
}

function projectPathFromArg(value: string | undefined): string { return resolve(value ?? process.cwd()); }
function requireArg(value: string | undefined, name: string): string { if (!value || value.trim().length === 0) throw new Error(`Missing required argument: ${name}`); return value; }
function parseEvidenceType(value: string): EvidenceType {
  const allowed = new Set(["code", "command", "test", "config", "diff", "source", "benchmark", "security", "clinical", "regulatory"]);
  if (!allowed.has(value)) throw new Error(`Invalid evidence type: ${value}`);
  return value as EvidenceType;
}

async function main(): Promise<void> {
  const [, , command, ...args] = process.argv;
  try {
    switch (command) {
      case undefined:
      case "help":
      case "--help":
      case "-h": help(); return;
      case "init": kernel.init(projectPathFromArg(args[0])); return;
      case "status": kernel.status(projectPathFromArg(args[0])); return;
      case "plan": kernel.plan(projectPathFromArg(args[1]), requireArg(args[0], "objective")); return;
      case "checkpoint": kernel.checkpoint(projectPathFromArg(args[1]), requireArg(args[0], "summary")); return;
      case "evidence": kernel.addEvidence(projectPathFromArg(args[3]), requireArg(args[0], "claim"), parseEvidenceType(requireArg(args[1], "type")), requireArg(args[2], "reference")); return;
      case "judge": kernel.judge(projectPathFromArg(args[1]), requireArg(args[0], "taskId")); return;
      default: throw new Error(`Unknown command: ${command}`);
    }
  } catch (error) {
    console.error(error instanceof Error ? error.message : String(error));
    process.exitCode = 1;
  }
}

void main();
