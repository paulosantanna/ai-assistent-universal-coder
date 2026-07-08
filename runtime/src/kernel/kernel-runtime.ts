import { resolve, join } from "node:path";
import { existsSync, mkdirSync } from "node:fs";
import { ConfigLoader } from "./config-loader.js";
import { SchemaValidator } from "./schema-validator.js";
import { RegistryLoader } from "./registry-loader.js";
import { PermissionEngine } from "./permission-engine.js";
import { PolicyEngine } from "./policy-engine.js";
import { SkillExecutor } from "./skill-executor.js";
import { PlaybookEngine } from "./playbook-engine.js";
import { DeterministicJudge } from "./deterministic-judge.js";
import { ReportWriter } from "./report-writer.js";
import type {
  ExecutionContext,
  AeosConfig,
  PermissionsConfig,
  PoliciesConfig,
  PlaybookRegistryEntry,
  SkillRegistryEntry,
  MCPRegistryEntry,
  LCPContent,
  AgentRegistryEntry
} from "./types.js";

export interface KernelResult {
  success: boolean;
  executionId: string;
  targetPath: string;
  status: string;
  durationMs: number;
  error?: string;
  judgeVerdict?: string;
  judgeScore?: number;
  artifacts: string[];
  evidenceDir: string;
  reportDir: string;
}

export class KernelRuntime {
  private aeosRoot: string;
  private configLoader: ConfigLoader;
  private schemaValidator: SchemaValidator;
  private registryLoader: RegistryLoader;

  constructor(aeosRoot: string) {
    this.aeosRoot = resolve(aeosRoot);
    this.configLoader = new ConfigLoader(this.aeosRoot);
    this.schemaValidator = new SchemaValidator();
    this.registryLoader = new RegistryLoader(this.aeosRoot);
  }

  async runPlaybook(playbookId: string, targetPath: string): Promise<KernelResult> {
    const startTime = Date.now();

    try {
      targetPath = resolve(targetPath);
      if (!existsSync(targetPath)) {
        return this.errorResult(`Target path does not exist: ${targetPath}`, playbookId, targetPath, startTime);
      }

      // Step 1: Load aeos.config.yaml
      const config = this.configLoader.loadAeosConfig();
      const configValidation = this.schemaValidator.validateAeosConfig(config);
      if (!configValidation.valid) {
        return this.errorResult(
          `Config validation failed: ${configValidation.errors.join("; ")}`,
          playbookId, targetPath, startTime
        );
      }

      // Step 2: Load capabilities, permissions, policies
      const capabilities = this.configLoader.loadCapabilities();
      const capValidation = this.schemaValidator.validateCapabilities(capabilities);

      const permissions = this.configLoader.loadPermissions();
      const permValidation = this.schemaValidator.validatePermissions(permissions);
      if (!permValidation.valid) {
        return this.errorResult(
          `Permissions validation failed: ${permValidation.errors.join("; ")}`,
          playbookId, targetPath, startTime
        );
      }

      const policies = this.configLoader.loadPolicies();
      const polValidation = this.schemaValidator.validatePolicies(policies);

      // Step 3: Load registries
      const playbooksRegistry = this.registryLoader.loadPlaybooks();
      const skillsRegistry = this.registryLoader.loadSkills();
      const mcpsRegistry = this.registryLoader.loadMCPs();
      const lcpsRegistry = this.registryLoader.loadLCPs();
      const agentsRegistry = this.registryLoader.loadAgents();

      const pbValidation = this.schemaValidator.validatePlaybooksRegistry(playbooksRegistry);
      const skValidation = this.schemaValidator.validateSkillsRegistry(skillsRegistry);
      const mcpValidation = this.schemaValidator.validateMCPsRegistry(mcpsRegistry);
      const lcpValidation = this.schemaValidator.validateLCPsRegistry(lcpsRegistry);
      const agValidation = this.schemaValidator.validateAgentsRegistry(agentsRegistry);

      // Step 4: Resolve playbook
      const playbook = this.registryLoader.resolvePlaybook(playbooksRegistry.playbooks, playbookId);
      if (!playbook) {
        return this.errorResult(
          `Playbook '${playbookId}' not found in registry`,
          playbookId, targetPath, startTime
        );
      }

      // Step 5: Resolve skills, MCPs, LCPs
      const skills = this.registryLoader.resolveSkills(skillsRegistry.skills, playbook.required_skills);
      const mcps = this.registryLoader.resolveMCPs(mcpsRegistry.mcps, playbook.allowed_mcps);
      const lcps = this.registryLoader.resolveLCPs(lcpsRegistry.lcps, playbook.required_lcps);

      // Step 6: Load LCP contents (sorted by priority descending)
      const lcpContents: LCPContent[] = [];
      for (const lcpEntry of lcps.sort((a, b) => b.priority - a.priority)) {
        try {
          const lcpContent = this.configLoader.loadYaml<LCPContent>(lcpEntry.path);
          lcpContents.push(lcpContent);
        } catch {
          // LCP file may not exist yet; skip
        }
      }

      // Step 7: Resolve agent
      const rootAgent = this.registryLoader.resolveAgent(agentsRegistry.agents, "root");
      if (!rootAgent) {
        return this.errorResult("Root agent not found in registry", playbookId, targetPath, startTime);
      }

      // Step 8: Create engines
      const permissionEngine = new PermissionEngine(permissions);
      const policyEngine = new PolicyEngine(policies);
      const skillExecutor = new SkillExecutor();
      const judge = new DeterministicJudge();
      const reportWriter = new ReportWriter();
      const playbookEngine = new PlaybookEngine(
        this.configLoader,
        permissionEngine,
        policyEngine,
        skillExecutor,
        judge,
        reportWriter
      );

      // Step 9: Ensure target .aeos directories
      const aeosDir = resolve(targetPath, ".aeos");
      mkdirSync(joinPath(aeosDir, "evidence"), { recursive: true });
      mkdirSync(joinPath(aeosDir, "reports"), { recursive: true });

      // Step 10: Execute playbook
      const ctx = await playbookEngine.execute(
        playbook, skills, mcps, lcpContents, rootAgent,
        targetPath, this.aeosRoot, config
      );

      const duration = Date.now() - startTime;
      const evidenceDir = resolve(targetPath, ".aeos", "evidence", ctx.executionId);
      const reportDir = resolve(targetPath, ".aeos", "reports");

      return {
        success: ctx.status === "completed",
        executionId: ctx.executionId,
        targetPath,
        status: ctx.status,
        durationMs: duration,
        error: ctx.error,
        judgeVerdict: ctx.judgeReport?.verdict,
        judgeScore: ctx.judgeReport?.score,
        artifacts: ctx.artifacts,
        evidenceDir: evidenceDir,
        reportDir: reportDir
      };

    } catch (err) {
      return this.errorResult(
        err instanceof Error ? err.message : String(err),
        playbookId, targetPath, startTime
      );
    }
  }

  async listPlaybooks(): Promise<Array<{ id: string; name: string; riskLevel: string }>> {
    const registry = this.registryLoader.loadPlaybooks();
    return registry.playbooks.map((pb) => ({
      id: pb.id,
      name: pb.name,
      riskLevel: pb.risk_level
    }));
  }

  private errorResult(
    error: string,
    playbookId: string,
    targetPath: string,
    startTime: number
  ): KernelResult {
    return {
      success: false,
      executionId: "error",
      targetPath,
      status: "failed",
      durationMs: Date.now() - startTime,
      error,
      artifacts: [],
      evidenceDir: "",
      reportDir: ""
    };
  }
}

function joinPath(...parts: string[]): string {
  return join(...parts);
}
