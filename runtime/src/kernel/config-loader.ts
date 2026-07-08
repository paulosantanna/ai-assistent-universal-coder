import { existsSync, readFileSync } from "node:fs";
import { join, resolve } from "node:path";
import * as yaml from "js-yaml";
import type {
  AeosConfig,
  CapabilitiesConfig,
  PermissionsConfig,
  PoliciesConfig
} from "./types.js";

export class ConfigLoadError extends Error {
  constructor(message: string, public filePath: string) {
    super(`ConfigLoadError [${filePath}]: ${message}`);
    this.name = "ConfigLoadError";
  }
}

export class ConfigLoader {
  private readonly aeosRoot: string;

  constructor(aeosRoot: string) {
    this.aeosRoot = resolve(aeosRoot);
  }

  loadAeosConfig(): AeosConfig {
    return this.loadYaml<AeosConfig>("aeos/config/aeos.config.yaml");
  }

  loadCapabilities(): CapabilitiesConfig {
    return this.loadYaml<CapabilitiesConfig>("aeos/config/capabilities.yaml");
  }

  loadPermissions(): PermissionsConfig {
    return this.loadYaml<PermissionsConfig>("aeos/config/permissions.yaml");
  }

  loadPolicies(): PoliciesConfig {
    return this.loadYaml<PoliciesConfig>("aeos/config/policies.yaml");
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
    const raw = readFileSync(abs, "utf-8");
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
}
