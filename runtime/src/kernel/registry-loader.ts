import type {
  PlaybooksRegistry,
  SkillsRegistry,
  MCPsRegistry,
  LCPsRegistry,
  AgentsRegistry,
  BlueprintsRegistry,
  WorkbenchProfilesRegistry,
  EnterpriseSkillsRegistry,
  EnterprisePlaybooksRegistry,
  PlaybookRegistryEntry,
  SkillRegistryEntry,
  MCPRegistryEntry,
  LCPRegistryEntry,
  AgentRegistryEntry,
  BlueprintRegistryEntry,
  WorkbenchProfileRegistryEntry,
  EnterpriseSkillRegistryEntry,
  EnterprisePlaybookRegistryEntry,
  MergeResult,
  SubAgentRegistryEntry,
  CrossReferenceValidation,
  OverlayRegistryIndex
} from "./types.js";
import { ConfigLoader } from "./config-loader.js";
import { OverlayRegistryMerger } from "./overlay-registry-merger.js";

export class RegistryLoader {
  private loader: ConfigLoader;
  private merger: OverlayRegistryMerger;
  private readonly indexes = new WeakMap<readonly { id: string }[], Map<string, { id: string }>>();

  constructor(aeosRoot: string) {
    this.loader = new ConfigLoader(aeosRoot);
    this.merger = new OverlayRegistryMerger(aeosRoot);
  }

  loadPlaybooks(): PlaybooksRegistry {
    return this.loader.loadYaml<PlaybooksRegistry>("aeos/registries/playbooks.registry.yaml");
  }

  loadSkills(): SkillsRegistry {
    return this.loader.loadYaml<SkillsRegistry>("aeos/registries/skills.registry.yaml");
  }

  loadMCPs(): MCPsRegistry {
    return this.loader.loadYaml<MCPsRegistry>("aeos/registries/mcps.registry.yaml");
  }

  loadLCPs(): LCPsRegistry {
    return this.loader.loadYaml<LCPsRegistry>("aeos/registries/lcps.registry.yaml");
  }

  loadAgents(): AgentsRegistry {
    return this.loader.loadYaml<AgentsRegistry>("aeos/registries/agents.registry.yaml");
  }

  loadBlueprints(): BlueprintsRegistry {
    return this.loader.loadYaml<BlueprintsRegistry>("aeos/registries/blueprints.registry.yaml");
  }

  loadWorkbenchProfiles(): WorkbenchProfilesRegistry {
    return this.loader.loadYaml<WorkbenchProfilesRegistry>("aeos/registries/workbench-profiles.registry.yaml");
  }

  loadOverlayIndex(): OverlayRegistryIndex {
    return this.loader.loadYaml<OverlayRegistryIndex>("aeos/registries/overlay.registry.index.yaml");
  }

  loadMergedFromOverlay(): MergeResult {
    return this.merger.loadAndMergeWithStrategy("replace-duplicates");
  }

  loadAllResolved(): {
    agents: AgentRegistryEntry[];
    subagents: SubAgentRegistryEntry[];
    skills: SkillRegistryEntry[];
    playbooks: PlaybookRegistryEntry[];
    mcps: MCPRegistryEntry[];
    lcps: LCPRegistryEntry[];
    blueprints: BlueprintRegistryEntry[];
    profiles: WorkbenchProfileRegistryEntry[];
    mergeResult: MergeResult;
  } {
    const mergeResult = this.loadMergedFromOverlay();
    const mcps = this.loadMCPs().mcps;
    const lcps = this.loadLCPs().lcps;
    const blueprints = this.loadBlueprints().blueprints;
    const profiles = this.loadWorkbenchProfiles().profiles;

    return {
      agents: mergeResult.agents,
      subagents: mergeResult.subagents,
      skills: mergeResult.skills,
      playbooks: mergeResult.playbooks,
      mcps,
      lcps,
      blueprints,
      profiles,
      mergeResult
    };
  }

  resolvePlaybook(playbooks: PlaybookRegistryEntry[], id: string): PlaybookRegistryEntry | null {
    return (this.indexById(playbooks).get(id) as PlaybookRegistryEntry | undefined) ?? null;
  }

  resolveSkills(skills: SkillRegistryEntry[], ids: string[]): SkillRegistryEntry[] {
    return this.resolveMany(skills, ids) as SkillRegistryEntry[];
  }

  resolveMCPs(mcps: MCPRegistryEntry[], ids: string[]): MCPRegistryEntry[] {
    return this.resolveMany(mcps, ids) as MCPRegistryEntry[];
  }

  resolveLCPs(lcps: LCPRegistryEntry[], ids: string[]): LCPRegistryEntry[] {
    return this.resolveMany(lcps, ids) as LCPRegistryEntry[];
  }

  resolveAgent(agents: AgentRegistryEntry[], id: string): AgentRegistryEntry | null {
    return (this.indexById(agents).get(id) as AgentRegistryEntry | undefined) ?? null;
  }

  private resolveMany<T extends { id: string }>(entries: T[], ids: string[]): T[] {
    const index = this.indexById(entries);
    const resolved: T[] = [];
    const seen = new Set<string>();
    for (const id of ids) {
      if (seen.has(id)) continue;
      seen.add(id);
      const entry = index.get(id) as T | undefined;
      if (entry) resolved.push(entry);
    }
    return resolved;
  }

  private indexById<T extends { id: string }>(entries: T[]): Map<string, T> {
    const cached = this.indexes.get(entries);
    if (cached) {
      return cached as Map<string, T>;
    }
    const index = new Map<string, T>();
    for (const entry of entries) {
      index.set(entry.id, entry);
    }
    this.indexes.set(entries, index as Map<string, { id: string }>);
    return index;
  }
}
