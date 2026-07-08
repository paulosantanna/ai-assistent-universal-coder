import { existsSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { KernelRuntime, type KernelResult } from "./kernel-runtime.js";

export function detectAeosRoot(): string {
  let current = resolve(process.cwd());
  // Walk up to find aeos/config/aeos.config.yaml
  while (current !== dirname(current)) {
    if (existsSync(resolve(current, "aeos", "config", "aeos.config.yaml"))) {
      return current;
    }
    current = dirname(current);
  }
  // Fallback to cwd (will fail with clear error)
  return process.cwd();
}

export async function handleRun(args: string[]): Promise<void> {
  const playbookId = args[0];
  const targetIndex = args.indexOf("--target");
  const targetPath = targetIndex !== -1 && args[targetIndex + 1] ? args[targetIndex + 1] : process.cwd();

  if (!playbookId) {
    console.error("Usage: aeos run <playbook-id> --target <path>");
    console.error("       aeos run project-analysis --target .");
    process.exitCode = 1;
    return;
  }

  const aeosRoot = detectAeosRoot();
  const kernel = new KernelRuntime(aeosRoot);

  // Check if playbook exists via list
  const playbooks = await kernel.listPlaybooks();
  const pbExists = playbooks.some((pb) => pb.id === playbookId);
  if (!pbExists) {
    const available = playbooks.map((pb) => `  - ${pb.id} (${pb.name})`).join("\n");
    console.error(`Playbook '${playbookId}' not found. Available playbooks:\n${available}`);
    process.exitCode = 1;
    return;
  }

  console.log(`\n🚀 AEOS Kernel Runtime v0.1`);
  console.log(`   Playbook: ${playbookId}`);
  console.log(`   Target:   ${targetPath}`);
  console.log(`   AEOS:     ${aeosRoot}`);
  console.log("");

  const result = await kernel.runPlaybook(playbookId, targetPath);

  const duration = (result.durationMs / 1000).toFixed(1);
  const icon = result.success ? "✅" : result.status === "blocked" ? "🔒" : "❌";

  console.log(`\n${icon} Execution: ${result.executionId}`);
  console.log(`   Status:   ${result.status}`);
  console.log(`   Duration: ${duration}s`);

  if (result.error) {
    console.log(`   Error:    ${result.error}`);
  }

  if (result.judgeVerdict) {
    const judgeIcon = result.judgeVerdict === "PASS" ? "✅" : "🔴";
    console.log(`\n${judgeIcon} Judge:     ${result.judgeVerdict}`);
    console.log(`   Score:     ${result.judgeScore?.toFixed(1)}`);
  }

  if (result.artifacts.length > 0) {
    console.log(`\n📄 Artifacts:`);
    for (const artifact of result.artifacts) {
      console.log(`   - ${artifact}`);
    }
  }

  if (result.evidenceDir) {
    console.log(`\n📁 Evidence: ${result.evidenceDir}`);
  }

  console.log("");
}
