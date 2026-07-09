import { existsSync, readFileSync } from "node:fs";
import { join, resolve } from "node:path";
import * as yaml from "js-yaml";
import type {
  AeosConfig,
  CapabilitiesConfig,
  PermissionsConfig,
  PoliciesConfig,
  PlaybooksRegistry,
  SkillsRegistry,
  MCPsRegistry,
  LCPsRegistry,
  AgentsRegistry,
  BlueprintsRegistry,
  WorkbenchProfilesRegistry,
  EnterpriseSkillsRegistry,
  EnterprisePlaybooksRegistry,
  OverlayRegistryIndex,
  SkillsAdditionsConfig,
  PlaybooksAdditionsConfig,
  AgentsAdditionsConfig,
  SkillRegistryEntry,
  PlaybookRegistryEntry,
  AgentRegistryEntry
} from "./types.js";
import { SchemaValidator, type ValidationResult } from "./schema-validator.js";

export class ConfigLoadError extends Error {
  constructor(message: string, public filePath: string) {
    super(`ConfigLoadError [${filePath}]: ${message}`);
    this.name = "ConfigLoadError";
  }
}

export class ConfigLoader {
  private readonly aeosRoot: string;
  private readonly validator: SchemaValidator;

  constructor(aeosRoot: string) {
    this.aeosRoot = resolve(aeosRoot);
    this.validator = new SchemaValidator(this.aeosRoot);
  }

  loadAeosConfig(): AeosConfig {
    const config = this.loadYaml<AeosConfig>("aeos/config/aeos.config.yaml");
    const result = this.validator.validateAeosConfig(config);
    this.reportValidation("aeos.config.yaml", result);
    return config;
  }

  loadCapabilities(): CapabilitiesConfig {
    const config = this.loadYaml<CapabilitiesConfig>("aeos/config/capabilities.yaml");
    const result = this.validator.validateCapabilities(config);
    this.reportValidation("capabilities.yaml", result);
    return config;
  }

  loadPermissions(): PermissionsConfig {
    const config = this.loadYaml<PermissionsConfig>("aeos/config/permissions.yaml");
    const result = this.validator.validatePermissions(config);
    this.reportValidation("permissions.yaml", result);
    return config;
  }

  loadPolicies(): PoliciesConfig {
    const config = this.loadYaml<PoliciesConfig>("aeos/config/policies.yaml");
    const result = this.validator.validatePolicies(config);
    this.reportValidation("policies.yaml", result);
    return config;
  }

  loadPlaybooksRegistry(): PlaybooksRegistry {
    const config = this.loadYaml<PlaybooksRegistry>("aeos/registries/playbooks.registry.yaml");
    const result = this.validator.validatePlaybooksRegistry(config);
    this.reportValidation("playbooks.registry.yaml", result);
    return config;
  }

  loadSkillsRegistry(): SkillsRegistry {
    const config = this.loadYaml<SkillsRegistry>("aeos/registries/skills.registry.yaml");
    const result = this.validator.validateSkillsRegistry(config);
    this.reportValidation("skills.registry.yaml", result);
    return config;
  }

  loadMCPsRegistry(): MCPsRegistry {
    const config = this.loadYaml<MCPsRegistry>("aeos/registries/mcps.registry.yaml");
    const result = this.validator.validateMCPsRegistry(config);
    this.reportValidation("mcps.registry.yaml", result);
    return config;
  }

  loadLCPsRegistry(): LCPsRegistry {
    const config = this.loadYaml<LCPsRegistry>("aeos/registries/lcps.registry.yaml");
    const result = this.validator.validateLCPsRegistry(config);
    this.reportValidation("lcps.registry.yaml", result);
    return config;
  }

  loadAgentsRegistry(): AgentsRegistry {
    const config = this.loadYaml<AgentsRegistry>("aeos/registries/agents.registry.yaml");
    const result = this.validator.validateAgentsRegistry(config);
    this.reportValidation("agents.registry.yaml", result);
    return config;
  }

  loadBlueprintsRegistry(): BlueprintsRegistry {
    const config = this.loadYaml<BlueprintsRegistry>("aeos/registries/blueprints.registry.yaml");
    const result = this.validator.validateBlueprintsRegistry(config);
    this.reportValidation("blueprints.registry.yaml", result);
    return config;
  }

  loadWorkbenchProfilesRegistry(): WorkbenchProfilesRegistry {
    const config = this.loadYaml<WorkbenchProfilesRegistry>("aeos/registries/workbench-profiles.registry.yaml");
    const result = this.validator.validateWorkbenchProfilesRegistry(config);
    this.reportValidation("workbench-profiles.registry.yaml", result);
    return config;
  }

  loadEnterpriseSkillsRegistry(): EnterpriseSkillsRegistry {
    const config = this.loadYaml<EnterpriseSkillsRegistry>("aeos/registries/enterprise-skills.registry.yaml");
    const result = this.validator.validateEnterpriseSkillsRegistry(config);
    this.reportValidation("enterprise-skills.registry.yaml", result);
    return config;
  }

  loadEnterprisePlaybooksRegistry(): EnterprisePlaybooksRegistry {
    const config = this.loadYaml<EnterprisePlaybooksRegistry>("aeos/registries/enterprise-playbooks.registry.yaml");
    const result = this.validator.validateEnterprisePlaybooksRegistry(config);
    this.reportValidation("enterprise-playbooks.registry.yaml", result);
    return config;
  }

  loadOverlayRegistryIndex(): OverlayRegistryIndex {
    const config = this.loadYaml<OverlayRegistryIndex>("aeos/registries/overlay.registry.index.yaml");
    const result = this.validator.validateOverlayRegistryIndex(config);
    this.reportValidation("overlay.registry.index.yaml", result);
    return config;
  }

  loadSkillsAdditions(version: string): SkillsAdditionsConfig | null {
    const path = `aeos/registries/skills.${version}.additions.yaml`;
    if (!this.fileExists(path)) return null;
    const config = this.loadYaml<SkillsAdditionsConfig>(path);
    const result = this.validator.validateSkillsRegistry(config);
    this.reportValidation(path, result);
    return config;
  }

  loadPlaybooksAdditions(version: string): PlaybooksAdditionsConfig | null {
    const path = `aeos/registries/playbooks.${version}.additions.yaml`;
    if (!this.fileExists(path)) return null;
    const config = this.loadYaml<PlaybooksAdditionsConfig>(path);
    const result = this.validator.validatePlaybooksRegistry(config);
    this.reportValidation(path, result);
    return config;
  }

  loadAgentsAdditions(version: string): AgentsAdditionsConfig | null {
    const path = `aeos/registries/agents.${version}.additions.yaml`;
    if (!this.fileExists(path)) return null;
    return this.loadYaml<AgentsAdditionsConfig>(path);
  }

  loadAllRegistryData(): {
    playbooks: PlaybookRegistryEntry[];
    skills: SkillRegistryEntry[];
    agents: AgentRegistryEntry[];
    mcps: any[];
    lcps: any[];
    blueprints: any[];
    profiles: any[];
    enterpriseSkills: any[];
    enterprisePlaybooks: any[];
    validations: { file: string; result: ValidationResult }[];
  } {
    const validations: { file: string; result: ValidationResult }[] = [];

    const load = <T>(file: string, fn: () => T): T | null => {
      try {
        return fn();
      } catch (e: any) {
        validations.push({ file, result: { valid: false, errors: [e.message], warnings: [] } });
        return null;
      }
    };

    const pbConfig = load("playbooks.registry.yaml", () => this.loadPlaybooksRegistry());
    const skConfig = load("skills.registry.yaml", () => this.loadSkillsRegistry());
    const agConfig = load("agents.registry.yaml", () => this.loadAgentsRegistry());
    const mcpConfig = load("mcps.registry.yaml", () => this.loadMCPsRegistry());
    const lcpConfig = load("lcps.registry.yaml", () => this.loadLCPsRegistry());
    const bpConfig = load("blueprints.registry.yaml", () => this.loadBlueprintsRegistry());
    const prConfig = load("workbench-profiles.registry.yaml", () => this.loadWorkbenchProfilesRegistry());
    const esConfig = load("enterprise-skills.registry.yaml", () => this.loadEnterpriseSkillsRegistry());
    const epConfig = load("enterprise-playbooks.registry.yaml", () => this.loadEnterprisePlaybooksRegistry());
    load("overlay.registry.index.yaml", () => this.loadOverlayRegistryIndex());

    const playbookVersions = ["v0_6", "v0_7", "v0_8_to_v1_0", "v1_1_enterprise"];
    const skillVersions = ["v0_6", "v0_7", "v0_8_to_v1_0", "v1_1_enterprise"];

    const playbooks = [...(pbConfig?.playbooks ?? [])];
    const skills = [...(skConfig?.skills ?? [])];
    const agents = [...(agConfig?.agents ?? [])];
    const mcps = [...(mcpConfig?.mcps ?? [])];
    const lcps = [...(lcpConfig?.lcps ?? [])];
    const blueprints = [...(bpConfig?.blueprints ?? [])];
    const profiles = [...(prConfig?.profiles ?? [])];
    const enterpriseSkills = [...(esConfig?.skills ?? [])];
    const enterprisePlaybooks = [...(epConfig?.playbooks ?? [])];

    for (const v of playbookVersions) {
      const add = load(`playbooks.${v}.additions.yaml`, () => this.loadPlaybooksAdditions(v));
      if (add?.playbooks) playbooks.push(...add.playbooks);
    }
    for (const v of skillVersions) {
      const add = load(`skills.${v}.additions.yaml`, () => this.loadSkillsAdditions(v));
      if (add?.skills) skills.push(...add.skills);
    }

    return { playbooks, skills, agents, mcps, lcps, blueprints, profiles, enterpriseSkills, enterprisePlaybooks, validations };
  }

  loadMarkdown(filePath: string): string {
    const abs = resolve(this.aeosRoot, filePath);
    if (!existsSync(abs)) {
      throw new ConfigLoadError(`File not found`, abs);
    }
    return readFileSync(abs, "utf-8");
  }

  loadYaml<T>(relativePath: string): T {
    const abs = resolve(this.aeosRoot, relativePath);
    if (!existsSync(abs)) {
      throw new ConfigLoadError(`File not found`, abs);
    }
    let raw = readFileSync(abs, "utf-8");
    if (raw.charCodeAt(0) === 0xFEFF || (raw.charCodeAt(0) === 0xEF && raw.charCodeAt(1) === 0xBB && raw.charCodeAt(2) === 0xBF)) {
      raw = raw.replace(/^\uFEFF/, "").replace(/^\uEF\uBB\uBF/, "");
    }
    try {
      const parsed = yaml.load(raw) as T;
      if (!parsed) {
        throw new ConfigLoadError("Empty or invalid YAML", abs);
      }
      return parsed;
    } catch (err) {
      if (err instanceof ConfigLoadError) throw err;
      throw new ConfigLoadError(
        `YAML parse error: ${err instanceof Error ? err.message : String(err)}`,
        abs
      );
    }
  }

  fileExists(relativePath: string): boolean {
    return existsSync(resolve(this.aeosRoot, relativePath));
  }

  private reportValidation(file: string, result: ValidationResult): void {
    if (result.errors.length > 0 || result.warnings.length > 0) {
      const lines = [`Validation [${file}]:`];
      for (const e of result.errors) lines.push(`  ERROR: ${e}`);
      for (const w of result.warnings) lines.push(`  WARN:  ${w}`);
    }
  }
}