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
    return playbooks.find((pb) => pb.id === id) ?? null;
  }

  resolveSkills(skills: SkillRegistryEntry[], ids: string[]): SkillRegistryEntry[] {
    return skills.filter((sk) => ids.includes(sk.id));
  }

  resolveMCPs(mcps: MCPRegistryEntry[], ids: string[]): MCPRegistryEntry[] {
    return mcps.filter((mcp) => ids.includes(mcp.id));
  }

  resolveLCPs(lcps: LCPRegistryEntry[], ids: string[]): LCPRegistryEntry[] {
    return lcps.filter((lcp) => ids.includes(lcp.id));
  }

  resolveAgent(agents: AgentRegistryEntry[], id: string): AgentRegistryEntry | null {
    return agents.find((a) => a.id === id) ?? null;
  }
}