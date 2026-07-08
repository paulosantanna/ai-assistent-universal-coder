import type {
  PlaybooksRegistry,
  SkillsRegistry,
  MCPsRegistry,
  LCPsRegistry,
  AgentsRegistry,
  PlaybookRegistryEntry,
  SkillRegistryEntry,
  MCPRegistryEntry,
  LCPRegistryEntry,
  AgentRegistryEntry
} from "./types.js";
import { ConfigLoader } from "./config-loader.js";

export class RegistryLoader {
  private loader: ConfigLoader;

  constructor(aeosRoot: string) {
    this.loader = new ConfigLoader(aeosRoot);
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
