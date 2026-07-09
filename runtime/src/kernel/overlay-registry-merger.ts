import type {
  AgentRegistryEntry,
  SubAgentRegistryEntry,
  SkillRegistryEntry,
  PlaybookRegistryEntry,
  MergeConflict,
  MergeResult,
  OverlayRegistryIndex
} from "./types.js";
import { ConfigLoader } from "./config-loader.js";

export class OverlayRegistryMerger {
  private loader: ConfigLoader;

  constructor(aeosRoot: string) {
    this.loader = new ConfigLoader(aeosRoot);
  }

  loadAndMergeAll(): MergeResult {
    const conflicts: MergeConflict[] = [];
    const warnings: string[] = [];

    const index = this.loader.loadOverlayRegistryIndex();
    const fragments = index.registry_fragments.map(f => f.path);

    const allAgents: AgentRegistryEntry[] = [];
    const allSubAgents: SubAgentRegistryEntry[] = [];
    const allSkills: SkillRegistryEntry[] = [];
    const allPlaybooks: PlaybookRegistryEntry[] = [];

    const agentIds = new Set<string>();
    const skillIds = new Set<string>();
    const playbookIds = new Set<string>();

    for (const fragmentPath of fragments) {
      if (!this.loader.fileExists(fragmentPath)) {
        warnings.push(`Fragment not found, skipping: ${fragmentPath}`);
        continue;
      }

      const data = this.loader.loadYaml<any>(fragmentPath);

      if (!data || typeof data !== "object") {
        warnings.push(`Empty or invalid fragment: ${fragmentPath}`);
        continue;
      }

      if (Array.isArray(data.agents)) {
        for (const agent of data.agents as AgentRegistryEntry[]) {
          if (agentIds.has(agent.id)) {
            conflicts.push({
              registry: fragmentPath,
              existing_id: agent.id,
              source: "agents",
              reason: `Duplicate agent id "${agent.id}" in ${fragmentPath}`
            });
          } else {
            agentIds.add(agent.id);
            allAgents.push(agent);
          }
        }
      }

      if (Array.isArray(data.subagents)) {
        for (const subagent of data.subagents as SubAgentRegistryEntry[]) {
          allSubAgents.push(subagent);
        }
      }

      if (Array.isArray(data.skills)) {
        for (const skill of data.skills as SkillRegistryEntry[]) {
          if (skillIds.has(skill.id)) {
            conflicts.push({
              registry: fragmentPath,
              existing_id: skill.id,
              source: "skills",
              reason: `Duplicate skill id "${skill.id}" in ${fragmentPath}`
            });
          } else {
            skillIds.add(skill.id);
            allSkills.push(skill);
          }
        }
      }

      if (Array.isArray(data.playbooks)) {
        for (const pb of data.playbooks as PlaybookRegistryEntry[]) {
          if (playbookIds.has(pb.id)) {
            conflicts.push({
              registry: fragmentPath,
              existing_id: pb.id,
              source: "playbooks",
              reason: `Duplicate playbook id "${pb.id}" in ${fragmentPath}`
            });
          } else {
            playbookIds.add(pb.id);
            allPlaybooks.push(pb);
          }
        }
      }
    }

    if (conflicts.length > 0) {
      return {
        merged: false,
        conflicts,
        warnings,
        agents: allAgents,
        subagents: allSubAgents,
        skills: allSkills,
        playbooks: allPlaybooks
      };
    }

    return {
      merged: true,
      conflicts: [],
      warnings,
      agents: allAgents,
      subagents: allSubAgents,
      skills: allSkills,
      playbooks: allPlaybooks
    };
  }

  loadAndMergeWithStrategy(strategy: "replace-duplicates" | "skip-duplicates" | "fail-on-duplicates"): MergeResult {
    const result = this.loadAndMergeAll();

    if (result.conflicts.length === 0) return result;

    if (strategy === "fail-on-duplicates") {
      return result;
    }

    const warnings = [...result.warnings];

    if (strategy === "skip-duplicates") {
      warnings.push(`Skipped ${result.conflicts.length} duplicates`);
      return { ...result, merged: true, warnings };
    }

    if (strategy === "replace-duplicates") {
      const agentIds = new Set<string>();
      const skillIds = new Set<string>();
      const playbookIds = new Set<string>();

      const dedupedAgents: AgentRegistryEntry[] = [];
      const dedupedSkills: SkillRegistryEntry[] = [];
      const dedupedPlaybooks: PlaybookRegistryEntry[] = [];

      for (const agent of result.agents) {
        if (agentIds.has(agent.id)) {
          const idx = dedupedAgents.findIndex(a => a.id === agent.id);
          if (idx >= 0) dedupedAgents[idx] = agent;
        } else {
          agentIds.add(agent.id);
          dedupedAgents.push(agent);
        }
      }

      for (const skill of result.skills) {
        if (skillIds.has(skill.id)) {
          const idx = dedupedSkills.findIndex(s => s.id === skill.id);
          if (idx >= 0) dedupedSkills[idx] = skill;
        } else {
          skillIds.add(skill.id);
          dedupedSkills.push(skill);
        }
      }

      for (const pb of result.playbooks) {
        if (playbookIds.has(pb.id)) {
          const idx = dedupedPlaybooks.findIndex(p => p.id === pb.id);
          if (idx >= 0) dedupedPlaybooks[idx] = pb;
        } else {
          playbookIds.add(pb.id);
          dedupedPlaybooks.push(pb);
        }
      }

      warnings.push(`Replaced ${result.conflicts.length} duplicates with latest fragment version`);
      return {
        merged: true,
        conflicts: result.conflicts,
        warnings,
        agents: dedupedAgents,
        subagents: result.subagents,
        skills: dedupedSkills,
        playbooks: dedupedPlaybooks
      };
    }

    return { ...result, merged: false };
  }
}