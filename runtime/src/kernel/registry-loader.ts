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
  CrossReferenceValidation,
  OverlayRegistryIndex
} from "./types.js";
import { ConfigLoader } from "./config-loader.js";
import { OverlayRegistryMerger } from "./overlay-registry-merger.js";
import {
  governEntries,
  governEntry,
  governPlaybookEntries,
  governSkillEntries
} from "./codenavi-governance.js";

export class RegistryLoader {
  private loader: ConfigLoader;
  private merger: OverlayRegistryMerger;
  private readonly indexes = new WeakMap<readonly { id: string }[], Map<string, { id: string }>>();

  constructor(aeosRoot: string) {
    this.loader = new ConfigLoader(aeosRoot);
    this.merger = new OverlayRegistryMerger(aeosRoot);
  }

  loadPlaybooks(): PlaybooksRegistry {
    const registry = this.loader.loadYaml<PlaybooksRegistry>("aeos/registries/playbooks.registry.yaml");
    return { ...registry, playbooks: governPlaybookEntries(registry.playbooks) };
  }

  loadSkills(): SkillsRegistry {
    const registry = this.loader.loadYaml<SkillsRegistry>("aeos/registries/skills.registry.yaml");
    return { ...registry, skills: governSkillEntries(registry.skills) };
  }

  loadMCPs(): MCPsRegistry {
    const registry = this.loader.loadYaml<MCPsRegistry>("aeos/registries/mcps.registry.yaml");
    return { ...registry, mcps: governEntries(registry.mcps) };
  }

  loadLCPs(): LCPsRegistry {
    const registry = this.loader.loadYaml<LCPsRegistry>("aeos/registries/lcps.registry.yaml");
    return { ...registry, lcps: governEntries(registry.lcps) };
  }

  loadAgents(): AgentsRegistry {
    const registry = this.loader.loadYaml<AgentsRegistry>("aeos/registries/agents.registry.yaml");
    return { ...registry, agents: governEntries(registry.agents) };
  }

  loadBlueprints(): BlueprintsRegistry {
    const registry = this.loader.loadYaml<BlueprintsRegistry>("aeos/registries/blueprints.registry.yaml");
    return { ...registry, blueprints: governEntries(registry.blueprints) };
  }

  loadWorkbenchProfiles(): WorkbenchProfilesRegistry {
    const registry = this.loader.loadYaml<WorkbenchProfilesRegistry>("aeos/registries/workbench-profiles.registry.yaml");
    return { ...registry, profiles: governEntries(registry.profiles) };
  }

  loadOverlayIndex(): OverlayRegistryIndex {
    return this.loader.loadYaml<OverlayRegistryIndex>("aeos/registries/overlay.registry.index.yaml");
  }

  loadMergedFromOverlay(): MergeResult {
    const merged = this.merger.loadAndMergeWithStrategy("replace-duplicates");
    return {
      ...merged,
      agents: governEntries(merged.agents),
      skills: governSkillEntries(merged.skills),
      playbooks: governPlaybookEntries(merged.playbooks)
    };
  }

  loadAllResolved(): {
    agents: AgentRegistryEntry[];
    subagents: [];
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
      // Compatibility field for legacy consumers. The single-agent model forbids runtime subagents.
      subagents: [],
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
    const entry = this.indexById(playbooks).get(id) as PlaybookRegistryEntry | undefined;
    return entry ? governPlaybookEntries([entry])[0] ?? null : null;
  }

  resolveSkills(skills: SkillRegistryEntry[], ids: string[]): SkillRegistryEntry[] {
    return governSkillEntries(this.resolveMany(skills, ids) as SkillRegistryEntry[]);
  }

  resolveMCPs(mcps: MCPRegistryEntry[], ids: string[]): MCPRegistryEntry[] {
    return governEntries(this.resolveMany(mcps, ids) as MCPRegistryEntry[]);
  }

  resolveLCPs(lcps: LCPRegistryEntry[], ids: string[]): LCPRegistryEntry[] {
    return governEntries(this.resolveMany(lcps, ids) as LCPRegistryEntry[]);
  }

  resolveAgent(agents: AgentRegistryEntry[], id: string): AgentRegistryEntry | null {
    const entry = this.indexById(agents).get(id) as AgentRegistryEntry | undefined;
    return entry ? governEntry(entry) : null;
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
