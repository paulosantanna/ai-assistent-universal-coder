# Redundancy Judge1
> run: 2026-11-13-full
> model: grok-4.7
> partitions: slice-01 .. slice-06

Counts: KEEP-CAVEAT=35 KEEP-COMPRESSED=58 KEEP-POLICY=459 KEEP-ROUTING=463 REDUNDANT-GENERAL=2 UNCLEAR=1

| ID | Cost | Class | Evidence | Confidence | Trim suggestion |
| C001 | 3 | KEEP-POLICY | Root listing has AGENTS.md only as the constitution; uniqueness and the mission lead-in are not manifest keys. | high | none |
| C002 | 3 | KEEP-POLICY | Root listing has AGENTS.md only as the constitution; uniqueness and the mission lead-in are not manifest keys. | high | none |
| C003 | 3 | KEEP-POLICY | docs/AGENT.md header scopes the same arrow to documentation work; the workspace-wide lifecycle is process, not a manifest. | medium | none |
| C004 | 3 | KEEP-ROUTING | .notebook/INDEX.md exists, but read-first-when-present is a load order, not a directory entry or manifest. | high | none |
| C005 | 3 | KEEP-POLICY | ls .notebook shows HANDOFF.md, MEMORY.md, PROGRESS.md and LEARNING.md; ensure-they-exist-for-material-work is policy. | high | none |
| C006 | 3 | KEEP-ROUTING | Quartet filenames are listed under .notebook; which files to read before planning, and when to skip LEARNING.md, is a load rule. | high | none |
| C007 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C008 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C009 | 3 | KEEP-ROUTING | Naming skills, playbooks, MCPs and LSPs as mandatory pre-work is routing policy; inventory manifests are empty. | high | none |
| C010 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C011 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C012 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C013 | 3 | KEEP-POLICY | The notebook-to-MCP-to-docs verification order is workspace policy and is not a config key or file header. | high | none |
| C014 | 3 | KEEP-CAVEAT | Stale continuity must be reconciled before trust. That failure rule is not in .notebook headers or a manifest. | high | none |
| C015 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C016 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C017 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C018 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C019 | 3 | KEEP-POLICY | Seeding PROGRESS.md with acceptance gates is a plan duty. The file exists; the duty is not in its header. | high | none |
| C020 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C021 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C022 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C023 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C024 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C025 | 3 | KEEP-POLICY | Check lockfiles and never add packages silently. No root manifest was discovered to echo this rule. | high | none |
| C026 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C027 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C028 | 3 | KEEP-POLICY | .notebook/PROGRESS.md uses [x], [~] and [ ] in its header without defining pending, active, done or [!] blocked. | high | none |
| C029 | 3 | KEEP-POLICY | Workspace secret and external cookie-jar rule. kinghost-control-mcp/AGENT.md only narrows cookie handling for that adapter. | high | none |
| C030 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C031 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C032 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C033 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C034 | 3 | KEEP-POLICY | Moving a PROGRESS.md item to [x] only after its acceptance gate is policy, not the checkbox syntax in the file header. | high | none |
| C035 | 3 | KEEP-CAVEAT | Do not invent tests outside the mission, and flag untested risk. That constraint is not a test manifest. | high | none |
| C036 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | high | none |
| C037 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | high | none |
| C038 | 3 | KEEP-POLICY | Refresh HANDOFF.md on pause or session boundary. .notebook/HANDOFF.md header is mission status, not this duty. | high | none |
| C039 | 3 | KEEP-POLICY | Promotion rules for MEMORY.md versus LEARNING.md versus PROGRESS.md are policy. File headers do not state them. | high | none |
| C040 | 3 | KEEP-POLICY | Promotion rules for MEMORY.md versus LEARNING.md versus PROGRESS.md are policy. File headers do not state them. | high | none |
| C041 | 3 | KEEP-CAVEAT | Stale notes are defects to fix immediately. .notebook/workspace-governance.md is itself on an older CodENavi v1 wording. | high | none |
| C042 | 3 | KEEP-POLICY | docs/AGENT.md header prefers pointers in documentation; the notebook rule against copying code into notes is separate policy. | medium | none |
| C043 | 3 | KEEP-ROUTING | No references/ directory at repo root, and no CODENAVI_CONTINUITY_STANDARD.md anywhere. The pointer is not rediscoverable by listing. | high | none |
| C044 | 3 | KEEP-COMPRESSED | Role contracts are not in the quartet file headers. The cited continuity standard file is absent, so these sentences are the compact protocol. | high | none |
| C045 | 3 | KEEP-COMPRESSED | Role contracts are not in the quartet file headers. The cited continuity standard file is absent, so these sentences are the compact protocol. | high | none |
| C046 | 3 | KEEP-COMPRESSED | Role contracts are not in the quartet file headers. The cited continuity standard file is absent, so these sentences are the compact protocol. | high | none |
| C047 | 3 | KEEP-COMPRESSED | Role contracts are not in the quartet file headers. The cited continuity standard file is absent, so these sentences are the compact protocol. | high | none |
| C048 | 3 | KEEP-POLICY | Non-duplication across the quartet is policy. INDEX blurbs are shorter and do not state the cross-link rule. | high | none |
| C049 | 3 | KEEP-POLICY | Ban on secrets, personal data and chain-of-thought in continuity files, with cookie paths by identifier only. Not a manifest. | high | none |
| C050 | 3 | KEEP-POLICY | .agents/skills lists continuity-bootstrapper, handoff-manager, memory-curator, progress-tracker and learning-curator; never-separate-agents is policy. | high | none |
| C051 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C052 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C053 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C054 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C055 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C056 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C057 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C058 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C059 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C060 | 3 | KEEP-POLICY | Process rule. Root inventory manifests are empty, and no single directory listing or file header states it. | medium | none |
| C061 | 1 | KEEP-ROUTING | .notebook/INDEX.md header says project intelligence, read before every material mission. Always-on load order is still routing, not a manifest. | medium | none |
| C062 | 3 | KEEP-POLICY | INDEX.md currently lists the quartet first; reserved-and-must-stay-first is not written in that header. | high | none |
| C063 | 3 | KEEP-POLICY | .notebook is still a flat directory past 15 notes. The flows/patterns/gotchas/domain/graph threshold is policy, not the listing. | high | none |
| C064 | 3 | KEEP-POLICY | INDEX.md shows slug, summary, category and tags. It does not state the ~100 character cap. | high | none |
| C065 | 3 | KEEP-POLICY | Tag count, sort order and note shape are authoring policy. INDEX.md demonstrates entries without stating these limits. | high | none |
| C066 | 3 | KEEP-POLICY | Tag count, sort order and note shape are authoring policy. INDEX.md demonstrates entries without stating these limits. | high | none |
| C067 | 3 | KEEP-POLICY | Tag count, sort order and note shape are authoring policy. INDEX.md demonstrates entries without stating these limits. | high | none |
| C068 | 3 | KEEP-POLICY | Tag count, sort order and note shape are authoring policy. INDEX.md demonstrates entries without stating these limits. | high | none |
| C069 | 3 | KEEP-POLICY | HANDOFF.md and PROGRESS.md headers include Updated and Entry point; the always-include rule is still policy. | medium | none |
| C070 | 3 | KEEP-POLICY | Pointer syntax, no-opinions, organic notes and progressive disclosure are notebook policy, not file headers. | high | none |
| C071 | 3 | KEEP-POLICY | Pointer syntax, no-opinions, organic notes and progressive disclosure are notebook policy, not file headers. | high | none |
| C072 | 3 | KEEP-POLICY | Pointer syntax, no-opinions, organic notes and progressive disclosure are notebook policy, not file headers. | high | none |
| C073 | 3 | KEEP-POLICY | Pointer syntax, no-opinions, organic notes and progressive disclosure are notebook policy, not file headers. | high | none |
| C074 | 3 | KEEP-POLICY | Single codenavi-agent identity, no extra agents, lenses and Judge-as-gate. MEMORY.md states identity only past its header; no manifest. | high | none |
| C075 | 3 | KEEP-POLICY | Single codenavi-agent identity, no extra agents, lenses and Judge-as-gate. MEMORY.md states identity only past its header; no manifest. | high | none |
| C076 | 3 | KEEP-POLICY | Single codenavi-agent identity, no extra agents, lenses and Judge-as-gate. MEMORY.md states identity only past its header; no manifest. | high | none |
| C077 | 3 | KEEP-POLICY | Single codenavi-agent identity, no extra agents, lenses and Judge-as-gate. MEMORY.md states identity only past its header; no manifest. | high | none |
| C078 | 3 | KEEP-POLICY | Single codenavi-agent identity, no extra agents, lenses and Judge-as-gate. MEMORY.md states identity only past its header; no manifest. | high | none |
| C079 | 3 | KEEP-POLICY | docs/AGENT.md repeats the v2 banner as a local inheritance label. The root governance name is process, not a manifest. | medium | none |
| C080 | 3 | KEEP-POLICY | Full-workspace scope plus the missing references/CODENAVI_FULL_WORKSPACE_STANDARD.md. Subtree files inherit it; they do not replace it. | high | none |
| C081 | 3 | KEEP-POLICY | Creation must-rules for new skills and governed artifacts. Not present in a manifest or one file header. | high | none |
| C082 | 3 | KEEP-POLICY | Creation must-rules for new skills and governed artifacts. Not present in a manifest or one file header. | high | none |
| C083 | 3 | KEEP-POLICY | Creation must-rules for new skills and governed artifacts. Not present in a manifest or one file header. | high | none |
| C084 | 3 | KEEP-POLICY | Creation must-rules for new skills and governed artifacts. Not present in a manifest or one file header. | high | none |
| C085 | 3 | KEEP-POLICY | Creation must-rules for new skills and governed artifacts. Not present in a manifest or one file header. | high | none |
| C086 | 3 | KEEP-POLICY | New artifacts must use runtime secret handling and external cookie-jar references. Same policy family as the secrets rule; not a config key. | high | none |
| C087 | 3 | KEEP-POLICY | Explicit scope and no new agent identities are creation standards, not directory facts. | high | none |
| C088 | 3 | KEEP-POLICY | Explicit scope and no new agent identities are creation standards, not directory facts. | high | none |
| C089 | 3 | KEEP-CAVEAT | Fail closed when evidence, permission or safety gates are missing. That is a safety posture, not a manifest. | high | none |
| C090 | 3 | KEEP-POLICY | AGENTS.md must stay canonical and byte-identical. A HANDOFF.md historical line reports a past check; it is not the rule. | high | none |
| C091 | 3 | KEEP-ROUTING | Trigger names WCAG tasks and excludes seo, core-web-vitals and web-quality-audit. The accessibility directory name does not carry those boundaries. | high | none |
| C092 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(quality)/web-accessibility/SKILL.md, which exists. Category is not shown by listing .agents/skills alone. Inventory manifests empty. Wrapper folder is accessibility, not web-accessibility. | high | none |
| C093 | 3 | KEEP-POLICY | One-agent Full Workspace v2 line. owner_agent sits in the same skill file; it is not a separate manifest. Inventory manifests empty. | high | none |
| C094 | 3 | KEEP-ROUTING | Routes meeting video and ata work, and excludes bare audio via vox-aurum. Not recoverable from the acta-aurea directory name. | high | none |
| C095 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(tooling)/acta-aurea/SKILL.md, which exists. Category is not shown by listing .agents/skills alone. Inventory manifests empty. | high | none |
| C096 | 3 | KEEP-POLICY | One-agent Full Workspace v2 line. owner_agent sits in the same skill file; it is not a separate manifest. Inventory manifests empty. | high | none |
| C097 | 3 | KEEP-ROUTING | Requires ADRs from inspected evidence only. The generic exclusion is extra routing, not a manifest. | high | none |
| C098 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/adr-decision-writer/SKILL.md, which exists. Category is not shown by listing .agents/skills alone. Inventory manifests empty. | high | none |
| C099 | 3 | KEEP-POLICY | One-agent Full Workspace v2 line. owner_agent sits in the same skill file; it is not a separate manifest. Inventory manifests empty. | high | none |
| C100 | 3 | KEEP-ROUTING | Forbids treating the trace skill as deployment authorization or as proof of checks that did not run. | high | none |
| C101 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(quality)/agent-trace-validator/SKILL.md, which exists. Category is not shown by listing .agents/skills alone. Inventory manifests empty. | high | none |
| C102 | 3 | KEEP-POLICY | One-agent Full Workspace v2 line. owner_agent sits in the same skill file; it is not a separate manifest. Inventory manifests empty. | high | none |
| C103 | 3 | KEEP-ROUTING | Trigger is the skill name plus a generic unrelated-implementation exclusion. Directory listing shows only ai-architecture-expert. | medium | none |
| C104 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(architecture)/ai-architecture-expert/SKILL.md, which exists. Category is not shown by listing .agents/skills alone. Inventory manifests empty. | high | none |
| C105 | 3 | KEEP-POLICY | One-agent Full Workspace v2 line. owner_agent sits in the same skill file; it is not a separate manifest. Inventory manifests empty. | high | none |
| C106 | 3 | KEEP-ROUTING | Cold-outreach trigger names Instantly, Smartlead, Clay and deliverability. Those tools are not a directory listing. | high | none |
| C107 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(gtm)/ai-cold-outreach/SKILL.md, which exists. Category is not shown by listing .agents/skills alone. Inventory manifests empty. | high | none |
| C108 | 3 | KEEP-POLICY | One-agent Full Workspace v2 line. owner_agent sits in the same skill file; it is not a separate manifest. Inventory manifests empty. | high | none |
| C109 | 3 | KEEP-ROUTING | Binds the skill to E:/GitHub/aidiabetic-research/src/ plus CVE, SAST and rollback duties. That absolute path is not a root manifest. | high | none |
| C110 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/ai-continuous-training-maintainer/SKILL.md, which exists. Category is not shown by listing .agents/skills alone. Inventory manifests empty. | high | none |
| C111 | 3 | KEEP-POLICY | One-agent Full Workspace v2 line. owner_agent sits in the same skill file; it is not a separate manifest. Inventory manifests empty. | high | none |
| C112 | 3 | KEEP-ROUTING | Trigger restates ai-engineering-expert and adds a generic do-not for unrelated languages and production deployment. | medium | none |
| C113 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/ai-engineering-expert/SKILL.md, which exists. Category is not shown by listing .agents/skills alone. Inventory manifests empty. | high | none |
| C114 | 3 | KEEP-POLICY | One-agent Full Workspace v2 line. owner_agent sits in the same skill file; it is not a separate manifest. Inventory manifests empty. | high | none |
| C115 | 3 | KEEP-ROUTING | Evals skill must not authorize deployment or stand in for checks that were not executed. | high | none |
| C116 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(quality)/ai-evals-expert/SKILL.md, which exists. Category is not shown by listing .agents/skills alone. Inventory manifests empty. | high | none |
| C117 | 3 | KEEP-POLICY | One-agent Full Workspace v2 line. owner_agent sits in the same skill file; it is not a separate manifest. Inventory manifests empty. | high | none |
| C118 | 3 | KEEP-ROUTING | Pricing trigger lists BYOK, tiers and margins, and excludes technical implementation. | high | none |
| C119 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(gtm)/ai-pricing/SKILL.md, which exists. Category is not shown by listing .agents/skills alone. Inventory manifests empty. | high | none |
| C120 | 3 | KEEP-POLICY | One-agent Full Workspace v2 line. owner_agent sits in the same skill file; it is not a separate manifest. Inventory manifests empty. | high | none |
| C121 | 3 | KEEP-ROUTING | Bootstrapper excludes ordinary one-off coding and human competency lists. | high | none |
| C122 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(creation)/ai-project-bootstrapper/SKILL.md, which exists. Category is not shown by listing .agents/skills alone. Inventory manifests empty. | high | none |
| C123 | 3 | KEEP-POLICY | One-agent Full Workspace v2 line. owner_agent sits in the same skill file; it is not a separate manifest. Inventory manifests empty. | high | none |
| C124 | 3 | KEEP-ROUTING | AI SDR trigger names 11x, Artisan and AiSDR and excludes technical implementation. | high | none |
| C125 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(gtm)/ai-sdr/SKILL.md, which exists. Category is not shown by listing .agents/skills alone. Inventory manifests empty. | high | none |
| C126 | 3 | KEEP-POLICY | One-agent Full Workspace v2 line. owner_agent sits in the same skill file; it is not a separate manifest. Inventory manifests empty. | high | none |
| C127 | 3 | KEEP-ROUTING | SEO trigger names programmatic SEO, AI Overviews and DataForSEO, and excludes application code review. | high | none |
| C128 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(gtm)/ai-seo/SKILL.md, which exists. Category is not shown by listing .agents/skills alone. Inventory manifests empty. | high | none |
| C129 | 3 | KEEP-POLICY | One-agent Full Workspace v2 line. owner_agent sits in the same skill file; it is not a separate manifest. Inventory manifests empty. | high | none |
| C130 | 3 | KEEP-ROUTING | UGC trigger names Spark Ads, Arcads and Creatify, and excludes technical implementation. | high | none |
| C131 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(gtm)/ai-ugc-ads/SKILL.md, which exists. Category is not shown by listing .agents/skills alone. Inventory manifests empty. | high | none |
| C132 | 3 | KEEP-POLICY | One-agent Full Workspace v2 line. owner_agent sits in the same skill file; it is not a separate manifest. Inventory manifests empty. | high | none |
| C133 | 3 | KEEP-ROUTING | Angular 20 work must not silently take behavior from another major. The directory name does not state that constraint. | high | none |
| C134 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/angular-20-expert/SKILL.md, which exists. Category is not shown by listing .agents/skills alone. Inventory manifests empty. | high | none |
| C135 | 3 | KEEP-POLICY | One-agent Full Workspace v2 line. owner_agent sits in the same skill file; it is not a separate manifest. Inventory manifests empty. | high | none |
| C136 | 3 | KEEP-ROUTING | Migration routing excludes angular-20-expert, legacy-migration-planner and deployment. | high | none |
| C137 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(architecture)/angular-8-to-20-migration/SKILL.md, which exists. Category is not shown by listing .agents/skills alone. Inventory manifests empty. | high | none |
| C138 | 3 | KEEP-POLICY | One-agent Full Workspace v2 line. owner_agent sits in the same skill file; it is not a separate manifest. Inventory manifests empty. | high | none |
| C139 | 3 | KEEP-ROUTING | Anti-hallucination use must not authorize deployment or replace checks that were not run. | high | none |
| C140 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(quality)/anti-hallucination-evaluator/SKILL.md, which exists. Category is not shown by listing .agents/skills alone. Inventory manifests empty. | high | none |
| C141 | 3 | KEEP-POLICY | One-agent Full Workspace v2 line. owner_agent sits in the same skill file; it is not a separate manifest. Inventory manifests empty. | high | none |
| C142 | 3 | KEEP-ROUTING | Approval audit is limited to authorized defensive scope and must not expose secret values. | high | none |
| C143 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(security)/approval-governance-auditor/SKILL.md, which exists. Category is not shown by listing .agents/skills alone. Inventory manifests empty. | high | none |
| C144 | 3 | KEEP-POLICY | One-agent Full Workspace v2 line. owner_agent sits in the same skill file; it is not a separate manifest. Inventory manifests empty. | high | none |
| C145 | 3 | KEEP-ROUTING | Approval requests stay inside authorized defensive scope and must not expose secrets. | high | none |
| C146 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(security)/approval-requester/SKILL.md, which exists. Category is not shown by listing .agents/skills alone. Inventory manifests empty. | high | none |
| C147 | 3 | KEEP-POLICY | One-agent Full Workspace v2 line. owner_agent sits in the same skill file; it is not a separate manifest. Inventory manifests empty. | high | none |
| C148 | 3 | KEEP-ROUTING | ASR routing names the seven-criteria test and ADR handoff, including Portuguese trigger phrases. | high | none |
| C149 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/architecturally-significant-requirement/SKILL.md, which exists. Category is not shown by listing .agents/skills alone. Inventory manifests empty. | high | none |
| C150 | 3 | KEEP-POLICY | One-agent Full Workspace v2 line. owner_agent sits in the same skill file; it is not a separate manifest. Inventory manifests empty. | high | none |
| C151 | 3 | KEEP-ROUTING | ADL routing covers numbering, supersession integrity and Portuguese trigger phrases. | high | none |
| C152 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(architecture)/architecture-decision-log/SKILL.md, which exists. Category is not shown by listing .agents/skills alone. Inventory manifests empty. | high | none |
| C153 | 3 | KEEP-POLICY | One-agent Full Workspace v2 line. owner_agent sits in the same skill file; it is not a separate manifest. Inventory manifests empty. | high | none |
| C154 | 3 | KEEP-ROUTING | ADR routing names MADR 4.0.0, Nygard and Y-statement, and excludes log indexing. | high | none |
| C155 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(architecture)/architecture-decision-record/SKILL.md, which exists. Category is not shown by listing .agents/skills alone. Inventory manifests empty. | high | none |
| C156 | 3 | KEEP-POLICY | One-agent Full Workspace v2 line. owner_agent sits in the same skill file; it is not a separate manifest. Inventory manifests empty. | high | none |
| C157 | 3 | KEEP-ROUTING | AKM routing covers ASR, ADR and the decision log, including the five-level adoption model. | high | none |
| C158 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(architecture)/architecture-knowledge-management/SKILL.md, which exists. Category is not shown by listing .agents/skills alone. Inventory manifests empty. | high | none |
| C159 | 3 | KEEP-POLICY | One-agent Full Workspace v2 line. owner_agent sits in the same skill file; it is not a separate manifest. Inventory manifests empty. | high | none |
| C160 | 3 | KEEP-ROUTING | Trigger restates architecture-mapper and a generic exclusion of unrelated implementation or deployment. | medium | none |
| C161 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(architecture)/architecture-mapper/SKILL.md, which exists. Category is not shown by listing .agents/skills alone. Inventory manifests empty. | high | none |
| C162 | 3 | KEEP-POLICY | One-agent Full Workspace v2 line. owner_agent sits in the same skill file; it is not a separate manifest. Inventory manifests empty. | high | none |
| C163 | 3 | KEEP-ROUTING | Dependency updates require manifest and lockfile compatibility plus regression evidence. | high | none |
| C164 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/atualizar-dependencias/SKILL.md, which exists. Category is not shown by listing .agents/skills alone. Inventory manifests empty. | high | none |
| C165 | 3 | KEEP-POLICY | One-agent Full Workspace v2 line. owner_agent sits in the same skill file; it is not a separate manifest. Inventory manifests empty. | high | none |
| C166 | 3 | KEEP-ROUTING | Orchestrator must stay deterministic and idempotent, and must not do unapproved remote writes. | high | none |
| C167 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(tooling)/automation-orchestrator/SKILL.md, which exists. Category is not shown by listing .agents/skills alone. Inventory manifests empty. | high | none |
| C168 | 3 | KEEP-POLICY | One-agent Full Workspace v2 line. owner_agent sits in the same skill file; it is not a separate manifest. Inventory manifests empty. | high | none |
| C169 | 3 | KEEP-ROUTING | AWS trigger lists service names and excludes non-AWS cloud providers. | high | none |
| C170 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(cloud)/aws-advisor/SKILL.md, which exists. Category is not shown by listing .agents/skills alone. Inventory manifests empty. | high | none |
| C171 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C172 | 3 | KEEP-ROUTING | sibling exclusions for accessibility, ai-seo, and full audit are not in inventory manifests or the folder name | high | none |
| C173 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C174 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C175 | 3 | KEEP-ROUTING | deployment-execution exclusion is a selection boundary; inventory manifests are empty | medium | none |
| C176 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C177 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C178 | 3 | KEEP-ROUTING | hybrid BM25 scope plus production-deployment ban is not a directory listing or manifest script | medium | none |
| C179 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C180 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C181 | 3 | KEEP-COMPRESSED | banking idempotency, traceability, and reliability bar is not in inventory manifests | medium | none |
| C182 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C183 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C184 | 3 | KEEP-CAVEAT | forbids treating the skill as deploy authorization or as proof of checks that did not run | high | none |
| C185 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C186 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C187 | 3 | KEEP-ROUTING | routes away from fleet-mapping, memory-curator, and multi-agent use; not a manifest string | high | none |
| C188 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C189 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C190 | 3 | KEEP-ROUTING | browser-debug triggers versus playwright-skill and non-browser work are not a folder listing | high | none |
| C191 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C192 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C193 | 3 | KEEP-ROUTING | AEOS quality-gate scope and the generic production ban are policy, not inventory manifests | medium | none |
| C194 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C195 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C196 | 3 | KEEP-ROUTING | names Workers and Pages and routes Vercel, Netlify, and Render to other skills | high | none |
| C197 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C198 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C199 | 3 | KEEP-CAVEAT | forbids production mutation and architecture invented without source evidence | high | none |
| C200 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C201 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C202 | 3 | KEEP-COMPRESSED | notebook continuity and no-assumption operating contract are not a skill-folder listing | high | none |
| C203 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C204 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C205 | 3 | KEEP-POLICY | requires source evidence before applying target conventions; not an inventory manifest | medium | none |
| C206 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C207 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C208 | 3 | KEEP-ROUTING | peer, platform, and breaking-change scope is a selector, not a discovered manifest command | medium | none |
| C209 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C210 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C211 | 3 | KEEP-CAVEAT | redacted audit export must not be used as deploy authorization or unrun-check evidence | high | none |
| C212 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C213 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C214 | 3 | KEEP-POLICY | secret non-leak plus no false evidence is process policy; manifests list is empty | medium | none |
| C215 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C216 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C217 | 3 | KEEP-ROUTING | sends code-level dupes to linters and dependency work to coupling-analysis | high | none |
| C218 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C219 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C220 | 3 | KEEP-ROUTING | excludes coupling-analysis and domain-identification-grouping; not visible from the folder name | high | none |
| C221 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C222 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C223 | 3 | KEEP-ROUTING | excludes runtime performance sizing and capacity planning; inventory manifests empty | high | none |
| C224 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C225 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C226 | 3 | KEEP-POLICY | blocks unapproved remote writes; that prohibition is not a manifest or directory name | medium | none |
| C227 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C228 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C229 | 3 | KEEP-ROUTING | limits the skill to Confluence MCP and away from Jira, web search, and local files | high | none |
| C230 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C231 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C232 | 3 | KEEP-ROUTING | content-to-revenue trigger list is a selector; quoted tail is truncated and not a manifest | medium | none |
| C233 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C234 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C235 | 3 | KEEP-POLICY | forbids promoting unverified claims or transient status into durable memory | high | none |
| C236 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C237 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C238 | 3 | KEEP-POLICY | forbids inventing project state and promoting unverified claims into memory | high | none |
| C239 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C240 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C241 | 3 | KEEP-ROUTING | assigns LCP, INP, and CLS away from perf-web-optimization, perf-lighthouse, and perf-astro | high | none |
| C242 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C243 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C244 | 3 | KEEP-POLICY | cache-policy purpose plus the durable-memory promotion ban is process policy | medium | none |
| C245 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C246 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C247 | 3 | KEEP-COMPRESSED | strength, distance, and volatility model is not implied by the folder name or manifests | medium | none |
| C248 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C249 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C250 | 3 | KEEP-ROUTING | sends undecided choices to create-rfc and implementation planning elsewhere | high | none |
| C251 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C252 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C253 | 3 | KEEP-ROUTING | separates RFC proposals from TDD and general docs via named sibling skills | high | none |
| C254 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C255 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C256 | 3 | KEEP-ROUTING | routes general docs to docs-writer and keeps this skill on design-doc discovery | high | none |
| C257 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C258 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C259 | 3 | KEEP-POLICY | states the 20 lenses are skill specializations and never agent identities | high | none |
| C260 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C261 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C262 | 3 | KEEP-COMPRESSED | pins C# 14 and .NET 10 and excludes F# and Visual Basic; no matching root manifest | high | none |
| C263 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C264 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C265 | 3 | KEEP-POLICY | forbids spawning or registering another AEOS agent identity | high | none |
| C266 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C267 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C268 | 3 | KEEP-ROUTING | routes CVE assessment, patching, and EOL dates to vuln-obsol-recon, cve-remediation, and eol-advisory-sync | high | none |
| C269 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C270 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C271 | 3 | KEEP-ROUTING | keeps discovery, ingestion, and PR publish or merge on other skills | high | none |
| C272 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C273 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C274 | 3 | KEEP-CAVEAT | warns not to claim a current inventory or publish without inspection and authorization | high | none |
| C275 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C276 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C277 | 3 | KEEP-COMPRESSED | 24h mine, top 20, LAYA, and red-team posting bar are not a directory listing | high | none |
| C278 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C279 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C280 | 3 | KEEP-ROUTING | schema and restore planning versus deployment execution is a selection boundary | medium | none |
| C281 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C282 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C283 | 3 | KEEP-ROUTING | excludes domain-analysis and component-identification-sizing for decomposition order | high | none |
| C284 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C285 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C286 | 3 | KEEP-POLICY | delegation check includes a ban on unapproved remote writes; manifests are empty | medium | none |
| C287 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C288 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C289 | 3 | KEEP-COMPRESSED | Docker, Xvfb, XFCE, mp4, and telemetry contract is not an inventory manifest | high | none |
| C290 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C291 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C292 | 3 | KEEP-ROUTING | upgrade-candidate scope plus the generic production ban is not a manifest script | medium | none |
| C293 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C294 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C295 | 3 | KEEP-ROUTING | minimal blast radius is a selection constraint; inventory manifests are empty | medium | none |
| C296 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C297 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C298 | 3 | KEEP-COMPRESSED | AIHealthResearch branch, OSV, CodeQL, and deploy-validator contract is not a root manifest | high | none |
| C299 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C300 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C301 | 3 | KEEP-POLICY | blocks unapproved production changes while diagnosing pipelines | medium | none |
| C302 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C303 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C304 | 3 | KEEP-COMPRESSED | recursive CI recovery, per-workflow guardians, and bundle handoff are not a folder listing | high | none |
| C305 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C306 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C307 | 3 | KEEP-CAVEAT | review output is not deploy authorization or evidence for checks that were not run | high | none |
| C308 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C309 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C310 | 3 | KEEP-POLICY | sandbox generation plus no unapproved production change is process policy | medium | none |
| C311 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C312 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C313 | 3 | KEEP-ROUTING | excludes code comments, inline JSDoc, and API reference generation | high | none |
| C314 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C315 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C316 | 3 | KEEP-POLICY | sandbox-only evidence-based docs plus the production ban are not a manifest string | medium | none |
| C317 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C318 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C319 | 3 | KEEP-COMPRESSED | 11-layer endpoint-to-operations package is a packed contract, not a directory name | medium | none |
| C320 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C321 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C322 | 3 | KEEP-CAVEAT | forbids production mutation and architecture invented without source evidence | high | none |
| C323 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C324 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C325 | 3 | KEEP-ROUTING | separates new DDD boundaries from domain-identification-grouping and coupling-analysis | high | none |
| C326 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C327 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C328 | 3 | KEEP-ROUTING | groups existing components and excludes domain-analysis and coupling-analysis | high | none |
| C329 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C330 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C331 | 3 | KEEP-POLICY | forbids restart, scale, or live mutation without an authorized operations task | high | none |
| C332 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C333 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C334 | 3 | KEEP-CAVEAT | forbids production mutation and architecture invented without source evidence | high | none |
| C335 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C336 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C337 | 3 | KEEP-POLICY | limits work to authorized defense and forbids exposing secret values | high | none |
| C338 | 2 | KEEP-ROUTING | 00_skills target exists, but category plus local-module load is not one listing or a manifest script | high | none |
| C339 | 3 | KEEP-POLICY | inventory manifests empty; single-identity ban is not a config key or directory name | high | none |
| C340 | 3 | KEEP-COMPRESSED | endoflife.date API v1, aliases, and the false public-EOL caveat are not a manifest | medium | none |
| C341 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C342 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C343 | 3 | KEEP-CAVEAT | unevaluated-check and deploy-authorization ban is process text; inventory manifests empty | medium | keep |
| C344 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C345 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C346 | 3 | KEEP-COMPRESSED | cache-key, invalidation, type, and stale-risk scope exceeds the directory name; inventory manifests empty | medium | keep |
| C347 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C348 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C349 | 3 | KEEP-COMPRESSED | manifest, hash-chain, and tamper-resistance scope exceeds the directory name; inventory manifests empty | medium | keep |
| C350 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C351 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C352 | 3 | KEEP-COMPRESSED | DDD, ACL, outbox, and resilience method is packed process text; inventory manifests empty | medium | keep |
| C353 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C354 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C355 | 3 | KEEP-ROUTING | diagram trigger list is selection text; inventory manifests empty | medium | keep |
| C356 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C357 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C358 | 3 | KEEP-ROUTING | churn and NRR triggers plus non-code boundary are selection text; inventory manifests empty | medium | keep |
| C359 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C360 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C361 | 3 | KEEP-COMPRESSED | classify-to-report loop is packed process text; inventory manifests empty | medium | keep |
| C362 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C363 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C364 | 3 | KEEP-ROUTING | wrapper-for-all-AEOS-skills route is not the directory name; inventory manifests empty | medium | keep |
| C365 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C366 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C367 | 3 | KEEP-COMPRESSED | adapter, flowchart, trap fixture, and smoke-eval list is packed process text; inventory manifests empty | medium | keep |
| C368 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C369 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C370 | 3 | KEEP-CAVEAT | do-not-treat-as-deploy-or-unrun-evidence caveat is process text; inventory manifests empty | medium | keep |
| C371 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C372 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C373 | 3 | KEEP-COMPRESSED | parallel lenses, one plan, surgical execute, adversarial verify is packed process text; inventory manifests empty | medium | keep |
| C374 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C375 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C376 | 3 | KEEP-ROUTING | pixel-perfect work is routed to figma-implement-design; listing both folders does not state that split; manifests empty | medium | keep |
| C377 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C378 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C379 | 3 | KEEP-ROUTING | general Figma fetch is routed to figma; listing both folders does not state that split; manifests empty | medium | keep |
| C380 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C381 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C382 | 3 | KEEP-POLICY | fine-tune-only-when-justified-and-provider-supported is an authorization gate; inventory manifests empty | medium | keep |
| C383 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C384 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C385 | 3 | KEEP-CAVEAT | do-not-treat-as-deploy-or-unrun-evidence caveat is process text; inventory manifests empty | medium | keep |
| C386 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C387 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C388 | 3 | KEEP-CAVEAT | ban on inventing business rules or mutating production is process text; inventory manifests empty | medium | keep |
| C389 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C390 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C391 | 3 | KEEP-COMPRESSED | discovery-before-code checklist is packed process text; inventory manifests empty | medium | keep |
| C392 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C393 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C394 | 3 | KEEP-ROUTING | design review is routed to web-design-guidelines or web-quality-audit; manifests empty | medium | keep |
| C395 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C396 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C397 | 3 | KEEP-ROUTING | CI comments route to gh-fix-ci and gh auth is required first; manifests empty | medium | keep |
| C398 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C399 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C400 | 3 | KEEP-ROUTING | review comments route to gh-address-comments; Buildkite and non-Actions CI are out of scope; manifests empty | medium | keep |
| C401 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C402 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C403 | 3 | KEEP-POLICY | ban on cloning an identifiable real child and on unapproved remote writes is policy; inventory manifests empty | medium | keep |
| C404 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C405 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C406 | 3 | KEEP-POLICY | runtime-only auth and immutable safety denials are policy; inventory manifests empty | medium | keep |
| C407 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C408 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C409 | 3 | KEEP-POLICY | no restart, scale, or live mutation without an authorized ops task; inventory manifests empty | medium | keep |
| C410 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C411 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C412 | 3 | KEEP-ROUTING | GTM-automation trigger vocabulary is selection text; inventory manifests empty | medium | keep |
| C413 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C414 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C415 | 3 | KEEP-COMPRESSED | GTM metric set is packed selection text beyond the directory name; inventory manifests empty | medium | keep |
| C416 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C417 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C418 | 3 | KEEP-CAVEAT | do not promote unverified or transient status into durable memory; inventory manifests empty | medium | keep |
| C419 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C420 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C421 | 3 | KEEP-COMPRESSED | Q1 Q2 Track A always and ADR exclusion are packed protocol text; inventory manifests empty | medium | keep |
| C422 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C423 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C424 | 3 | KEEP-ROUTING | interface-improvement trigger list is selection text; inventory manifests empty | medium | keep |
| C425 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C426 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C427 | 3 | KEEP-POLICY | no restart, scale, or live mutation without an authorized ops task; inventory manifests empty | medium | keep |
| C428 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C429 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C430 | 3 | KEEP-POLICY | does not replace production authority and bans unauthorized live mutation; inventory manifests empty | medium | keep |
| C431 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C432 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C433 | 3 | KEEP-COMPRESSED | Java 8 to 11 compatibility direction is not in the directory name; inventory manifests empty | medium | keep |
| C434 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C435 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C436 | 3 | KEEP-POLICY | stock ban on unrelated-domain production deployment is policy; name echo alone is not the claim; manifests empty | medium | keep |
| C437 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C438 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C439 | 3 | KEEP-COMPRESSED | LTS-aware verification constraint exceeds the directory name; inventory manifests empty | medium | keep |
| C440 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C441 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C442 | 3 | KEEP-POLICY | only toolchain- and runtime-verified Java 25 APIs may be used; inventory manifests empty | medium | keep |
| C443 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C444 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C445 | 3 | KEEP-CAVEAT | current versus preview versus incubator status must be handled explicitly; inventory manifests empty | medium | keep |
| C446 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C447 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C448 | 3 | KEEP-CAVEAT | do not silently use APIs introduced after Java 8; inventory manifests empty | medium | keep |
| C449 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C450 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C451 | 3 | KEEP-COMPRESSED | trace, cause, fix, validate, and retain-lessons sequence is packed process text; inventory manifests empty | medium | keep |
| C452 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C453 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C454 | 3 | KEEP-ROUTING | this row creates a solver skill rather than applying java-bug-solver; inventory manifests empty | medium | keep |
| C455 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C456 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C457 | 3 | KEEP-POLICY | stock ban on unrelated-domain production deployment is policy; manifests empty | medium | keep |
| C458 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C459 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C460 | 3 | KEEP-COMPRESSED | version-correct APIs, minimal diffs, and evidence-backed verification exceed the directory name; manifests empty | medium | keep |
| C461 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C462 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C463 | 3 | KEEP-COMPRESSED | API replacement and build-config update scope exceeds the directory name; inventory manifests empty | medium | keep |
| C464 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C465 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C466 | 3 | KEEP-ROUTING | route to one verified JDK profile and do not load other version skills; inventory manifests empty | medium | keep |
| C467 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C468 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C469 | 3 | KEEP-COMPRESSED | runtime, module-system, and browser compatibility constraints exceed the directory name; manifests empty | medium | keep |
| C470 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C471 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C472 | 3 | KEEP-POLICY | TypeSafe-only route and ban on executing unapproved actions are policy; inventory manifests empty | medium | keep |
| C473 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C474 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C475 | 3 | KEEP-ROUTING | Confluence pages route to confluence-assistant; listing both folders does not state that split; manifests empty | medium | keep |
| C476 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C477 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C478 | 3 | KEEP-COMPRESSED | requirement-code-evidence-doc traceability requirement exceeds the directory name; manifests empty | medium | keep |
| C479 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C480 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C481 | 3 | KEEP-CAVEAT | time entries must come from actual task evidence; inventory manifests empty | medium | keep |
| C482 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C483 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C484 | 3 | KEEP-POLICY | do not create a Judge agent and do not treat the run as deploy authorization; inventory manifests empty | medium | keep |
| C485 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C486 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C487 | 3 | KEEP-POLICY | rollback-safe restore and ban on unapproved production changes are policy; inventory manifests empty | medium | keep |
| C488 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C489 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C490 | 3 | KEEP-CAVEAT | clone must not mutate the remote origin or silently drop files; inventory manifests empty | medium | keep |
| C491 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C492 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C493 | 3 | KEEP-POLICY | ban on unrelated implementation or deployment execution is policy; inventory manifests empty | medium | keep |
| C494 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C495 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C496 | 3 | KEEP-POLICY | snapshot, rollback, and no unapproved production change are policy; inventory manifests empty | medium | keep |
| C497 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C498 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C499 | 3 | KEEP-POLICY | email ops must not expose secrets or ship unapproved production changes; inventory manifests empty | medium | keep |
| C500 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C501 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C502 | 3 | KEEP-COMPRESSED | super-skill scope across DNS, FTP, data, mail, and rollback is packed routing text; manifests empty | medium | keep |
| C503 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C504 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C505 | 3 | KEEP-COMPRESSED | Varnish, PHP, and PageSpeed measurement scope exceeds the directory name; inventory manifests empty | medium | keep |
| C506 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C507 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C508 | 3 | KEEP-POLICY | stay inside authorized defensive scope and do not expose secret values; inventory manifests empty | medium | keep |
| C509 | 2 | KEEP-ROUTING | stub dir lists SKILL.md only; category path needs a 00_skills walk; read-and-follow modules is not a root manifest string | high | keep |
| C510 | 3 | KEEP-POLICY | full no-extra-identity sentence is absent from catalog.json and skills.registry.yaml; inventory manifests empty | high | keep |
| C511 | 3 | KEEP-POLICY | Approval, backup, rollback, and the unapproved-production ban are only in the skill description, not a package field. | high | keep the approval and rollback ban |
| C512 | 2 | KEEP-ROUTING | Load target 00_skills/(cloud)/kinghost-site-publish-ftp-expert/SKILL.md is not on one listing of .agents/skills/kinghost-site-publish-ftp-expert; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C513 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C514 | 3 | KEEP-CAVEAT | Version-aware check against the current stable Kotlin release is a verification caveat; the directory name does not state it. | medium | keep the version-aware caveat |
| C515 | 2 | KEEP-ROUTING | Load target 00_skills/(development)/kotlin-expert/SKILL.md is not on one listing of .agents/skills/kotlin-expert; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C516 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C517 | 3 | KEEP-POLICY | Unapproved-production ban plus owner, test, and remediation mapping is only in the description. | medium | keep the no-unapproved-prod fence |
| C518 | 2 | KEEP-ROUTING | Load target 00_skills/(cloud)/kubernetes-code-context-mapper/SKILL.md is not on one listing of .agents/skills/kubernetes-code-context-mapper; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C519 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C520 | 3 | KEEP-POLICY | Ban on restart, scale, or mutate of live systems without an authorized ops task is process policy. | high | keep the no-mutate ban |
| C521 | 2 | KEEP-ROUTING | Load target 00_skills/(monitoring)/kubernetes-observability-staff/SKILL.md is not on one listing of .agents/skills/kubernetes-observability-staff; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C522 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C523 | 3 | KEEP-ROUTING | Trigger phrases and the ban on code review or software architecture are a skill-selection fence. | high | keep the GTM-versus-code fence |
| C524 | 2 | KEEP-ROUTING | Load target 00_skills/(gtm)/lead-enrichment/SKILL.md is not on one listing of .agents/skills/lead-enrichment; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C525 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C526 | 3 | KEEP-POLICY | Rule against promoting unverified claims or transient status into LEARNING.md is memory policy. | high | keep the promotion ban |
| C527 | 2 | KEEP-ROUTING | Load target 00_skills/(learning)/learning-curator/SKILL.md is not on one listing of .agents/skills/learning-curator; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C528 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C529 | 3 | KEEP-ROUTING | Negative routes name chromatic-mega-brain, skill-architect, create-adr, and the-fool. | high | keep the sibling-skill fence |
| C530 | 2 | KEEP-ROUTING | Load target 00_skills/(learning)/learning-opportunities/SKILL.md is not on one listing of .agents/skills/learning-opportunities; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C531 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C532 | 3 | KEEP-ROUTING | Negative routes name domain-analysis, component-identification-sizing, and decomposition-planning-roadmap. | high | keep the sibling-skill fence |
| C533 | 2 | KEEP-ROUTING | Load target 00_skills/(architecture)/legacy-migration-planner/SKILL.md is not on one listing of .agents/skills/legacy-migration-planner; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C534 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C535 | 3 | KEEP-ROUTING | Fence against implementation changes and deployment execution is a scope route, not a manifest string. | medium | keep the no-execute fence |
| C536 | 2 | KEEP-ROUTING | Load target 00_skills/(architecture)/legacy-risk-mapper/SKILL.md is not on one listing of .agents/skills/legacy-risk-mapper; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C537 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C538 | 3 | KEEP-CAVEAT | Warning that temperature is not a quality knob is a decoding caveat, not repo layout. | high | keep the temperature caveat |
| C539 | 2 | KEEP-ROUTING | Load target 00_skills/(development)/llm-calibration-temperature-expert/SKILL.md is not on one listing of .agents/skills/llm-calibration-temperature-expert; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C540 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C541 | 3 | KEEP-CAVEAT | Requires live authoritative capability data plus project evals before model choice. | high | keep the live-source caveat |
| C542 | 2 | KEEP-ROUTING | Load target 00_skills/(development)/llm-model-selection-expert/SKILL.md is not on one listing of .agents/skills/llm-model-selection-expert; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C543 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C544 | 3 | KEEP-POLICY | Masked metadata only, defensive scope, and no secret-value exposure are secret-handling policy. | high | keep the secret-exposure ban |
| C545 | 2 | KEEP-ROUTING | Load target 00_skills/(security)/local-secret-vault/SKILL.md is not on one listing of .agents/skills/local-secret-vault; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C546 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C547 | 3 | KEEP-POLICY | Ban on unrelated domains and production deployment is an authorization fence, not implied by the folder name. | medium | keep the no-deploy fence |
| C548 | 2 | KEEP-ROUTING | Load target 00_skills/(development)/lora-qlora-dora-expert/SKILL.md is not on one listing of .agents/skills/lora-qlora-dora-expert; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C549 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C550 | 3 | KEEP-ROUTING | Stage fence: build the KB, do not generate threat models or execution plans. | high | keep the stage fence |
| C551 | 2 | KEEP-ROUTING | Load target 00_skills/(security)/mantis-architecture/SKILL.md is not on one listing of .agents/skills/mantis-architecture; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C552 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C553 | 3 | KEEP-ROUTING | Runs only after prior stages and must not discover vulnerabilities or write patches. | high | keep the stage fence |
| C554 | 2 | KEEP-ROUTING | Load target 00_skills/(security)/mantis-calibrate/SKILL.md is not on one listing of .agents/skills/mantis-calibrate; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C555 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C556 | 3 | KEEP-ROUTING | Post-validation chain step; not initial auditing or patch writing. | high | keep the stage fence |
| C557 | 2 | KEEP-ROUTING | Load target 00_skills/(security)/mantis-chain/SKILL.md is not on one listing of .agents/skills/mantis-chain; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C558 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C559 | 3 | KEEP-CAVEAT | Production-viability filter calls out debug-only features and builds with assertions disabled. | high | keep the assertions-disabled caveat |
| C560 | 2 | KEEP-ROUTING | Load target 00_skills/(security)/mantis-critic/SKILL.md is not on one listing of .agents/skills/mantis-critic; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C561 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C562 | 3 | KEEP-ROUTING | Consolidation step before review; not initial auditing or patch generation. | high | keep the stage fence |
| C563 | 2 | KEEP-ROUTING | Load target 00_skills/(security)/mantis-dedupe/SKILL.md is not on one listing of .agents/skills/mantis-dedupe; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C564 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C565 | 3 | KEEP-COMPRESSED | Names the pre-process output workspace/historical_learnings.jsonl, which a directory listing does not. | high | keep the output-path contract |
| C566 | 2 | KEEP-ROUTING | Load target 00_skills/(security)/mantis-history/SKILL.md is not on one listing of .agents/skills/mantis-history; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C567 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C568 | 3 | KEEP-ROUTING | Supervisor role only; do not execute individual review stages. | high | keep the supervisor fence |
| C569 | 2 | KEEP-ROUTING | Load target 00_skills/(security)/mantis-meta-agent/SKILL.md is not on one listing of .agents/skills/mantis-meta-agent; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C570 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C571 | 3 | KEEP-POLICY | Requires transactional isolation via shadow directories or backups before patch apply. | high | keep the isolation rule |
| C572 | 2 | KEEP-ROUTING | Load target 00_skills/(security)/mantis-patch/SKILL.md is not on one listing of .agents/skills/mantis-patch; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C573 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C574 | 3 | KEEP-ROUTING | Designs a custom orchestrator and must not execute the default pipeline. | high | keep the adapter fence |
| C575 | 2 | KEEP-ROUTING | Load target 00_skills/(security)/mantis-pipeline-adapter/SKILL.md is not on one listing of .agents/skills/mantis-pipeline-adapter; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C576 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C577 | 3 | KEEP-COMPRESSED | Planning step writes workspace/plan.json and must not execute reviews or patches. | high | keep the plan.json contract |
| C578 | 2 | KEEP-ROUTING | Load target 00_skills/(security)/mantis-plan/SKILL.md is not on one listing of .agents/skills/mantis-plan; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C579 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C580 | 3 | KEEP-COMPRESSED | End-of-loop extract appends to workspace/learnings.jsonl rather than editing source. | high | keep the learnings.jsonl contract |
| C581 | 2 | KEEP-ROUTING | Load target 00_skills/(security)/mantis-reflect/SKILL.md is not on one listing of .agents/skills/mantis-reflect; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C582 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C583 | 3 | KEEP-ROUTING | End-of-cycle stakeholder packet; not code audit or patch verification. | high | keep the stage fence |
| C584 | 2 | KEEP-ROUTING | Load target 00_skills/(security)/mantis-report/SKILL.md is not on one listing of .agents/skills/mantis-report; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C585 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C586 | 3 | KEEP-ROUTING | Crash-reproducer step only; not auditing or patching. | high | keep the stage fence |
| C587 | 2 | KEEP-ROUTING | Load target 00_skills/(security)/mantis-reproduce/SKILL.md is not on one listing of .agents/skills/mantis-reproduce; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C588 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C589 | 3 | KEEP-ROUTING | Static review consumes workspace/plan.json and must not plan, dedupe, or patch. | high | keep the stage fence |
| C590 | 2 | KEEP-ROUTING | Load target 00_skills/(security)/mantis-researcher/SKILL.md is not on one listing of .agents/skills/mantis-researcher; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C591 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C592 | 3 | KEEP-ROUTING | False-positive review against source; not crash reproduction or patching. | high | keep the stage fence |
| C593 | 2 | KEEP-ROUTING | Load target 00_skills/(security)/mantis-review/SKILL.md is not on one listing of .agents/skills/mantis-review; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C594 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C595 | 3 | KEEP-COMPRESSED | Content-addressed semantic-unit index for a pinned or live tree is a method contract, not the folder name. | medium | keep the index contract |
| C596 | 2 | KEEP-ROUTING | Load target 00_skills/(security)/mantis-structural-index/SKILL.md is not on one listing of .agents/skills/mantis-structural-index; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C597 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C598 | 3 | KEEP-COMPRESSED | Requires a per-directory mantis-summary.md before threat modeling. | high | keep the summary-file contract |
| C599 | 2 | KEEP-ROUTING | Load target 00_skills/(security)/mantis-summarize/SKILL.md is not on one listing of .agents/skills/mantis-summarize; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C600 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C601 | 3 | KEEP-ROUTING | Stage B reads KB architecture and entities and must not mine source or JSONL learnings. | high | keep the stage fence |
| C602 | 2 | KEEP-ROUTING | Load target 00_skills/(security)/mantis-threat-model/SKILL.md is not on one listing of .agents/skills/mantis-threat-model; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C603 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C604 | 3 | KEEP-POLICY | Provenance curation plus a ban on unapproved remote writes is tool-write policy. | high | keep the no-remote-write ban |
| C605 | 2 | KEEP-ROUTING | Load target 00_skills/(tooling)/marketplace-curator/SKILL.md is not on one listing of .agents/skills/marketplace-curator; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C606 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C607 | 3 | KEEP-POLICY | MCP discovery is bound to AEOS policy and forbids unapproved remote writes. | high | keep the policy fence |
| C608 | 2 | KEEP-ROUTING | Load target 00_skills/(tooling)/mcp-discovery/SKILL.md is not on one listing of .agents/skills/mcp-discovery; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C609 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C610 | 3 | KEEP-POLICY | Health check forbids unapproved remote writes; that ban is not in a runtime manifest. | high | keep the no-remote-write ban |
| C611 | 2 | KEEP-ROUTING | Load target 00_skills/(tooling)/mcp-health-check/SKILL.md is not on one listing of .agents/skills/mcp-health-check; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C612 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C613 | 3 | KEEP-POLICY | Defensive-scope poisoning review that must not expose secret values. | high | keep the secret and scope ban |
| C614 | 2 | KEEP-ROUTING | Load target 00_skills/(security)/mcp-poisoning-evaluator/SKILL.md is not on one listing of .agents/skills/mcp-poisoning-evaluator; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C615 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C616 | 3 | KEEP-POLICY | MCP risk audit forbids unapproved remote writes. | high | keep the no-remote-write ban |
| C617 | 2 | KEEP-ROUTING | Load target 00_skills/(tooling)/mcp-risk-controller/SKILL.md is not on one listing of .agents/skills/mcp-risk-controller; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C618 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C619 | 3 | KEEP-POLICY | MEMORY.md curation must not store unverified claims or transient task status. | high | keep the promotion ban |
| C620 | 2 | KEEP-ROUTING | Load target 00_skills/(learning)/memory-curator/SKILL.md is not on one listing of .agents/skills/memory-curator; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C621 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C622 | 3 | KEEP-POLICY | Memory read and write audit covers evidence, scope, and secret safety. | high | keep the secret-safety rule |
| C623 | 2 | KEEP-ROUTING | Load target 00_skills/(learning)/memory-governance-auditor/SKILL.md is not on one listing of .agents/skills/memory-governance-auditor; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C624 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C625 | 3 | KEEP-COMPRESSED | Quoted capability list (dual-engine SVG/PNG/ASCII, 15+ themes, 20+ diagram types) is not a one-file header outside the skill. | medium | keep the capability contract |
| C626 | 2 | KEEP-ROUTING | Load target 00_skills/(tooling)/mermaid-studio/SKILL.md is not on one listing of .agents/skills/mermaid-studio; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C627 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C628 | 3 | KEEP-COMPRESSED | Quoted text is the ordered size, duplication, flattening, coupling, and grouping pipeline. | high | keep the pipeline order |
| C629 | 2 | KEEP-ROUTING | Load target 00_skills/(architecture)/modular-decomposition/SKILL.md is not on one listing of .agents/skills/modular-decomposition; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C630 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C631 | 3 | KEEP-ROUTING | Use-when triggers for split, boundary, and greenfield reviews are a selection fence; principles alone are not the claim. | medium | keep the selection fence |
| C632 | 2 | KEEP-ROUTING | Load target 00_skills/(architecture)/modular-design-principles/SKILL.md is not on one listing of .agents/skills/modular-design-principles; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C633 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C634 | 3 | KEEP-ROUTING | Launch triggers plus a ban on technical implementation, code review, and architecture. | high | keep the GTM-versus-code fence |
| C635 | 2 | KEEP-ROUTING | Load target 00_skills/(gtm)/multi-platform-launch/SKILL.md is not on one listing of .agents/skills/multi-platform-launch; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C636 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C637 | 3 | KEEP-POLICY | Forbids production mutation and architecture claims without source evidence. | high | keep the evidence and no-mutate rule |
| C638 | 2 | KEEP-ROUTING | Load target 00_skills/(mapping)/multirepo-ecosystem-mapper/SKILL.md is not on one listing of .agents/skills/multirepo-ecosystem-mapper; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C639 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C640 | 3 | KEEP-ROUTING | Quoted fence excludes simple CRUD and frontend work from this NestJS architecture skill. | high | keep the scope fence |
| C641 | 2 | KEEP-ROUTING | Load target 00_skills/(development)/nestjs-modular-monolith/SKILL.md is not on one listing of .agents/skills/nestjs-modular-monolith; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C642 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C643 | 3 | KEEP-ROUTING | Routes Netlify deploys away from Vercel, Cloudflare, and Render skills. | high | keep the provider fence |
| C644 | 2 | KEEP-ROUTING | Load target 00_skills/(cloud)/netlify-deploy/SKILL.md is not on one listing of .agents/skills/netlify-deploy; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C645 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C646 | 3 | KEEP-POLICY | Evidence-or-stop, three interrupt reasons, and short literal output are operator policy. | high | keep the operator rules |
| C647 | 2 | KEEP-ROUTING | Load target 00_skills/(development)/not-your-babysitter/SKILL.md is not on one listing of .agents/skills/not-your-babysitter; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C648 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C649 | 3 | KEEP-POLICY | Notebook progressive disclosure must not promote unverified or transient notes. | high | keep the promotion ban |
| C650 | 2 | KEEP-ROUTING | Load target 00_skills/(learning)/notebook-intelligence/SKILL.md is not on one listing of .agents/skills/notebook-intelligence; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C651 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C652 | 3 | KEEP-CAVEAT | Requires an Nx Cloud connection and excludes local task runs and non-Cloud CI. | medium | keep the Nx Cloud caveat |
| C653 | 2 | KEEP-ROUTING | Load target 00_skills/(tooling)/nx-ci-monitor/SKILL.md is not on one listing of .agents/skills/nx-ci-monitor; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C654 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C655 | 3 | KEEP-ROUTING | Generator path prefers local workspace plugins and names nx-run-tasks and nx-workspace as the other skills. | high | keep the sibling fence |
| C656 | 2 | KEEP-ROUTING | Load target 00_skills/(tooling)/nx-generate/SKILL.md is not on one listing of .agents/skills/nx-generate; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C657 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C658 | 3 | KEEP-ROUTING | Task execution is fenced from nx-generate and nx-workspace. | high | keep the sibling fence |
| C659 | 2 | KEEP-ROUTING | Load target 00_skills/(tooling)/nx-run-tasks/SKILL.md is not on one listing of .agents/skills/nx-run-tasks; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C660 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C661 | 3 | KEEP-ROUTING | Workspace config skill must not be the primary skill only to run a task or generate code. | high | keep the sibling fence |
| C662 | 2 | KEEP-ROUTING | Load target 00_skills/(tooling)/nx-workspace/SKILL.md is not on one listing of .agents/skills/nx-workspace; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C663 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C664 | 3 | KEEP-POLICY | Design skill still forbids restart, scale, or mutate without an authorized ops task. | high | keep the no-mutate ban |
| C665 | 2 | KEEP-ROUTING | Load target 00_skills/(monitoring)/observability-architect/SKILL.md is not on one listing of .agents/skills/observability-architect; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C666 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C667 | 3 | KEEP-POLICY | Reporting skill forbids restart, scale, or mutate without an authorized ops task. | high | keep the no-mutate ban |
| C668 | 2 | KEEP-ROUTING | Load target 00_skills/(monitoring)/observability-reporter/SKILL.md is not on one listing of .agents/skills/observability-reporter; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C669 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C670 | 3 | KEEP-POLICY | Root-cause integration forbids live mutation without an authorized ops task. | high | keep the no-mutate ban |
| C671 | 2 | KEEP-ROUTING | Load target 00_skills/(monitoring)/observability-root-cause-integrator/SKILL.md is not on one listing of .agents/skills/observability-root-cause-integrator; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C672 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C673 | 3 | KEEP-POLICY | OpenShift observability forbids live mutation without an authorized ops task. | high | keep the no-mutate ban |
| C674 | 2 | KEEP-ROUTING | Load target 00_skills/(monitoring)/openshift-observability-staff/SKILL.md is not on one listing of .agents/skills/openshift-observability-staff; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C675 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C676 | 3 | KEEP-POLICY | Quarantine, staging, active packs, and trust policy, with no unapproved remote writes. | high | keep the trust-policy fence |
| C677 | 2 | KEEP-ROUTING | Load target 00_skills/(tooling)/pack-marketplace-auditor/SKILL.md is not on one listing of .agents/skills/pack-marketplace-auditor; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C678 | 3 | KEEP-POLICY | Single-agent identity and Full Workspace v2 are process policy; the sentence is not an exact package or catalog header. | high | keep the governance line |
| C679 | 3 | KEEP-POLICY | Package verify, quarantine, and promotion stay inside defensive scope and must not expose secrets. | high | keep the secret and scope ban |
| C680 | 2 | KEEP-ROUTING | Load target 00_skills/(security)/package-trust-engineer/SKILL.md is not on one listing of .agents/skills/package-trust-engineer; category bucket plus local-modules rule are shim routing. | high | keep the canonical load line |
| C681 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C682 | 2 | KEEP-COMPRESSED | AEOS package manifest and checksum contract is absent from inventory manifests and from the packaging directory name. | medium | keep scope sentence |
| C683 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(tooling)/packaging/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C684 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C685 | 2 | KEEP-ROUTING | Channel triggers (Meta, Google, TikTok, Advantage+, Performance Max) and the technical-implementation exclusion are not in the directory name. | high | keep triggers and exclusions |
| C686 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(gtm)/paid-creative-ai/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C687 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C688 | 2 | KEEP-COMPRESSED | Dependency-graph and read/write-set scheduling is not recoverable from a single folder listing. | medium | keep scope sentence |
| C689 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(tooling)/parallel-scheduler/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C690 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C691 | 2 | KEEP-ROUTING | PartnerStack, reseller, and revenue-share triggers plus a technical-implementation exclusion. | high | keep triggers and exclusions |
| C692 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(gtm)/partner-affiliate/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C693 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C694 | 3 | KEEP-CAVEAT | Patch proposals must not be applied; production deployment is out of scope. | high | keep non-application rule |
| C695 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(development)/patch-planner/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C696 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C697 | 2 | KEEP-ROUTING | Astro-only scope and a ban on being the sole Lighthouse skill, including the astro-critters trigger. | high | keep triggers and exclusions |
| C698 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(performance)/perf-astro/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C699 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C700 | 2 | KEEP-ROUTING | Names core-web-vitals, perf-web-optimization, and perf-astro as out of scope. | high | keep sibling exclusions |
| C701 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(performance)/perf-lighthouse/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C702 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C703 | 2 | KEEP-ROUTING | Routes CWV-only, Lighthouse-only, and Astro-only work to other named skills. | high | keep sibling exclusions |
| C704 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(performance)/perf-web-optimization/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C705 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C706 | 2 | KEEP-COMPRESSED | Names AEOS hot paths (registry, skill execution, evidence, scan, LSP, TypeScript runtime) and forbids unmeasured optimization. | medium | keep hot-path list |
| C707 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(performance)/performance-optimizer/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C708 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C709 | 2 | KEEP-COMPRESSED | Profiles Judge runtime, hashing, and package verification; forbids unmeasured optimization. | medium | keep profiler scope |
| C710 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(performance)/performance-profiler/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C711 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C712 | 2 | KEEP-COMPRESSED | Requires step contracts, dependencies, resources, and verification gates; excludes one-off coding and human competency lists. | medium | keep contract scope |
| C713 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(creation)/playbook-factory-generator/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C714 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C715 | 2 | KEEP-COMPRESSED | Optimizes playbook time, safety, and evidence quality rather than general coding. | medium | keep optimization axes |
| C716 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(creation)/playbook-optimizer/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C717 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C718 | 2 | KEEP-ROUTING | Browser-task scope with an explicit handoff to chrome-devtools for page debugging and network inspection. | high | keep handoff |
| C719 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(web-automation)/playwright-skill/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C720 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C721 | 3 | KEEP-POLICY | Forbids weakening permissions or acceptance criteria and forbids secret exposure outside authorized defense. | high | keep policy fence |
| C722 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(security)/policy-bypass-evaluator/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C723 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C724 | 3 | KEEP-POLICY | Fail-closed policy audit with an authorized-scope and secret-exposure ban. | high | keep policy fence |
| C725 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(security)/policy-hardening-auditor/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C726 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C727 | 2 | KEEP-ROUTING | ICP, PMF, and messaging triggers with a technical-implementation exclusion. | high | keep triggers and exclusions |
| C728 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(gtm)/positioning-icp/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C729 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C730 | 3 | KEEP-CAVEAT | Forbids treating incorrect pull-request feedback as mandatory. | high | keep non-obedience caveat |
| C731 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(development)/pr-comment-resolver/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C732 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C733 | 2 | KEEP-COMPRESSED | Independent evidence-based review fence plus a production-deployment exclusion beyond the folder name. | medium | keep evidence-review fence |
| C734 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(development)/pr-reviewer/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C735 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C736 | 2 | KEEP-COMPRESSED | Severity-ranked evidence-backed review standard is narrower than the folder name. | medium | keep ranking rule |
| C737 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(development)/pr-reviewer-advanced/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C738 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C739 | 2 | KEEP-COMPRESSED | Plans CI/CD, observability, rollback, and readiness for any architecture; blocks unapproved production changes. | medium | keep planning scope |
| C740 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(cloud)/production-deployment-planner/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C741 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C742 | 3 | KEEP-POLICY | Binds live mission state to .notebook/PROGRESS.md and forbids promoting unverified claims into durable memory. | high | keep memory fence |
| C743 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(learning)/progress-tracker/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C744 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C745 | 2 | KEEP-COMPRESSED | Converts prompts into bounded evidence-based tasks and blocks unapproved remote writes. | medium | keep prompt bounds |
| C746 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(tooling)/prompt-optimizer/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C747 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C748 | 2 | KEEP-COMPRESSED | Production-readiness scope for Python AI/RAG systems, with language and deployment exclusions. | medium | keep readiness scope |
| C749 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(development)/python-ai-productionizer/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C750 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C751 | 2 | KEEP-COMPRESSED | Builds a Python bug-solver skill (traces, root cause, fix, stored lesson), which a folder listing does not specify. | medium | keep skill-build scope |
| C752 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(development)/python-bug-solver-skill/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C753 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C754 | 3 | KEEP-POLICY | Workspace rule: Python is allowed while AEOS kernel orchestration stays Node/TypeScript unless a later mission changes that surface. | high | keep language-surface rule |
| C755 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(development)/python-expert/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C756 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C757 | 2 | KEEP-COMPRESSED | RAG audit scope includes data leakage and prompt injection, not general Python work. | medium | keep audit scope |
| C758 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(development)/python-rag-audit/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C759 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C760 | 2 | KEEP-COMPRESSED | Requires measurable grounding quality for RAG work; production deployment stays out of scope. | medium | keep grounding bar |
| C761 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(development)/rag-expert/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C762 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C763 | 2 | KEEP-ROUTING | Requires loading Rails conventions before any code-level design discussion, not only before an edit. | medium | keep early-load rule |
| C764 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(development)/rails-dev/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C765 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C766 | 2 | KEEP-ROUTING | Performance guidelines with an explicit handoff to react-composition-patterns. | high | keep handoff |
| C767 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(quality)/react-best-practices/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C768 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C769 | 2 | KEEP-ROUTING | Composition-pattern scope with an explicit handoff to react-best-practices, including React 19 API changes. | high | keep handoff |
| C770 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(architecture)/react-composition-patterns/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C771 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C772 | 2 | KEEP-COMPRESSED | Requires the repository React/runtime version and existing component and data conventions. | medium | keep version-convention rule |
| C773 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(development)/react-expert/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C774 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C775 | 2 | KEEP-ROUTING | Expo Router, Reanimated, and list-virtualization triggers are not implied by the folder name. | high | keep triggers |
| C776 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(development)/react-native-expert/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C777 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C778 | 3 | KEEP-POLICY | Authorized redaction evaluation; forbids secret exposure and covers both leakage and over-removal. | high | keep secret fence |
| C779 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(security)/redaction-evaluator/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C780 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C781 | 3 | KEEP-CAVEAT | Must not be used as deployment authorization or as evidence for checks that were not executed. | high | keep non-authorization caveat |
| C782 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(quality)/release-readiness-judge/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C783 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C784 | 2 | KEEP-ROUTING | Render-only deploy path; excludes Vercel, Netlify, and Cloudflare in favor of their skills. | high | keep platform exclusions |
| C785 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(cloud)/render-deploy/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C786 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C787 | 3 | KEEP-CAVEAT | Forbids production mutation and architecture claims without source evidence. | high | keep non-mutation caveat |
| C788 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(mapping)/repo-scanner/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C789 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C790 | 2 | KEEP-ROUTING | Portuguese report-regression triggers; excludes fleet-mapping, schema edits, skill evaluation, and acta-aurea. | high | keep triggers and exclusions |
| C791 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(design)/report-design/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C792 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C793 | 3 | KEEP-CAVEAT | Requires inspecting the referenced code and verifying the correction before resolving comments. | high | keep verification caveat |
| C794 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(development)/resolver-comentarios/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C795 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C796 | 2 | KEEP-ROUTING | Local diff verdict only; excludes revisar-seguranca-pr, unsolicited remediation, posting a review, and merge. | high | keep sibling exclusions |
| C797 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(development)/revisar-pr/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C798 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C799 | 2 | KEEP-ROUTING | Security-diff review; excludes revisar-pr, fleet vulnerability inventory, and cve-remediation. | high | keep sibling exclusions |
| C800 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(security)/revisar-seguranca-pr/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C801 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C802 | 3 | KEEP-POLICY | Risk factors plus an authorized-scope and secret-exposure ban. | high | keep secret fence |
| C803 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(security)/risk-classifier/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C804 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C805 | 3 | KEEP-CAVEAT | Rollback text must say how to undo each operation; unapproved production changes are blocked. | high | keep undo caveat |
| C806 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(cloud)/rollback-planner/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C807 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C808 | 3 | KEEP-CAVEAT | Read-only runtime diagnosis; forbids restart, scale, deploy, and invented broker state. | high | keep read-only caveat |
| C809 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(development)/runtime-troubleshooting/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C810 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C811 | 2 | KEEP-COMPRESSED | Version-correct Rust APIs, minimal diffs, and evidence-backed verification. | medium | keep verification scope |
| C812 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(development)/rust-expert/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C813 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C814 | 2 | KEEP-ROUTING | PLG versus sales-led triggers (TTFV, freemium, demo-first) with a technical-implementation exclusion. | high | keep triggers and exclusions |
| C815 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(gtm)/sales-motion-design/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C816 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C817 | 3 | KEEP-POLICY | Redact without exposing raw secret values; authorized defensive scope only. | high | keep secret fence |
| C818 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(security)/secret-redaction-specialist/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C819 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C820 | 3 | KEEP-POLICY | Security audit must not print secret values and stays inside authorized defense. | high | keep secret fence |
| C821 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(security)/security-audit/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C822 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C823 | 2 | KEEP-ROUTING | Framework list (Java, Spring Boot 2/3, Camel, Angular, Python, JS/TS, Go) and exclusions for revisar-seguranca-pr, CVE/EOL, and threat modeling. | high | keep exclusions |
| C824 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(security)/security-best-practices/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C825 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C826 | 2 | KEEP-ROUTING | Git ownership, bus factor, and CODEOWNERS check; excludes maintainer lists and security-threat-model. | high | keep exclusions |
| C827 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(security)/security-ownership-map/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C828 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C829 | 2 | KEEP-ROUTING | Repo-grounded threat model; excludes architecture summaries, security-best-practices, and ownership maps. | high | keep exclusions |
| C830 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(security)/security-threat-model/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C831 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C832 | 3 | KEEP-CAVEAT | Read-only Sentry API use requires SENTRY_AUTH_TOKEN; excludes SDK setup and alert configuration. Environment prerequisite. | high | keep token and read-only caveat |
| C833 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(monitoring)/sentry/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C834 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C835 | 2 | KEEP-ROUTING | SEO scope excludes web-accessibility, core-web-vitals, and web-quality-audit. | high | keep exclusions |
| C836 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(quality)/seo/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C837 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C838 | 3 | KEEP-CAVEAT | ServiceNow triage text only; forbids restart, scale, or live mutation without an authorized operations task. | high | keep non-mutation caveat |
| C839 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(monitoring)/servicenow-incident-assistant/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C840 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C841 | 2 | KEEP-COMPRESSED | Shopify surface pin includes Liquid, Hydrogen, Functions, and API v2026-01. | medium | keep API surface pin |
| C842 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(development)/shopify-developer/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C843 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C844 | 3 | UNCLEAR | Quote demands four agents and a diabetes-cure simulator, conflicting with the same file single-agent governance line. Not in inventory manifests. | low | do not trim |
| C845 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(development)/simulator-ai/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C846 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C847 | 2 | KEEP-ROUTING | Skill-authoring route; excludes learning-opportunities, new agent identities, and technical design documents. | high | keep exclusions |
| C848 | 2 | KEEP-ROUTING | Load mandate for 00_skills/(creation)/skill-architect/SKILL.md and its local modules. The .agents skill folder listing does not name that category bucket. inventory.json manifests is empty. | high | keep delegation line |
| C849 | 3 | KEEP-POLICY | Single-agent Full Workspace v2 rule. inventory.json manifests is empty, so there is no cost-0 echo. A skill-directory listing does not state the rule. | high | keep |
| C850 | 2 | KEEP-COMPRESSED | Caps a skill entrypoint at 100 lines with local modules; excludes one-off fixes and new agent identities. | medium | keep 100-line rule |
| C851 | 2 | KEEP-ROUTING | skill-factory: canonical path 00_skills/(creation)/skill-factory/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C852 | 3 | KEEP-POLICY | skill-factory: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C853 | 3 | KEEP-ROUTING | skill-factory-generator: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C854 | 2 | KEEP-ROUTING | skill-factory-generator: canonical path 00_skills/(creation)/skill-factory-generator/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C855 | 3 | KEEP-POLICY | skill-factory-generator: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C856 | 3 | KEEP-ROUTING | skill-hardener: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C857 | 2 | KEEP-ROUTING | skill-hardener: canonical path 00_skills/(creation)/skill-hardener/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C858 | 3 | KEEP-POLICY | skill-hardener: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C859 | 3 | KEEP-ROUTING | slo-risk-analyzer: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C860 | 2 | KEEP-ROUTING | slo-risk-analyzer: canonical path 00_skills/(performance)/slo-risk-analyzer/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C861 | 3 | KEEP-POLICY | slo-risk-analyzer: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C862 | 3 | KEEP-ROUTING | social-media-operator: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C863 | 2 | KEEP-ROUTING | social-media-operator: canonical path 00_skills/(tooling)/social-media-operator/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C864 | 3 | KEEP-POLICY | social-media-operator: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C865 | 3 | KEEP-ROUTING | social-selling: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C866 | 2 | KEEP-ROUTING | social-selling: canonical path 00_skills/(gtm)/social-selling/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C867 | 3 | KEEP-POLICY | social-selling: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C868 | 3 | KEEP-ROUTING | solo-founder-gtm: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C869 | 2 | KEEP-ROUTING | solo-founder-gtm: canonical path 00_skills/(gtm)/solo-founder-gtm/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C870 | 3 | KEEP-POLICY | solo-founder-gtm: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C871 | 3 | KEEP-ROUTING | solve-problems: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C872 | 2 | KEEP-ROUTING | solve-problems: canonical path 00_skills/(development)/solve-problems/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C873 | 3 | KEEP-POLICY | solve-problems: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C874 | 3 | KEEP-ROUTING | spec-driven: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C875 | 2 | KEEP-ROUTING | spec-driven: canonical path 00_skills/(development)/spec-driven/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C876 | 3 | KEEP-POLICY | spec-driven: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C877 | 3 | KEEP-ROUTING | spec-driven-eval: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C878 | 2 | KEEP-ROUTING | spec-driven-eval: canonical path 00_skills/(development)/spec-driven-eval/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C879 | 3 | KEEP-POLICY | spec-driven-eval: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C880 | 3 | KEEP-ROUTING | spec-driven-lean: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C881 | 2 | KEEP-ROUTING | spec-driven-lean: canonical path 00_skills/(development)/spec-driven-lean/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C882 | 3 | KEEP-POLICY | spec-driven-lean: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C883 | 3 | KEEP-POLICY | Requires a specification before implementation and forbids overriding approved requirements; that gate is policy, not a directory listing | medium | keep |
| C884 | 2 | KEEP-ROUTING | specs: canonical path 00_skills/(development)/specs/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C885 | 3 | KEEP-POLICY | specs: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C886 | 3 | KEEP-POLICY | Forbids restart, scale, or live mutation without an authorized operations task; authorization is not a manifest key | high | keep |
| C887 | 2 | KEEP-ROUTING | splunk-observability-staff: canonical path 00_skills/(monitoring)/splunk-observability-staff/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C888 | 3 | KEEP-POLICY | splunk-observability-staff: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C889 | 3 | KEEP-ROUTING | staff-iii-architecture-governor: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C890 | 2 | KEEP-ROUTING | staff-iii-architecture-governor: canonical path 00_skills/(architecture)/staff-iii-architecture-governor/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C891 | 3 | KEEP-POLICY | staff-iii-architecture-governor: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C892 | 3 | KEEP-ROUTING | staff-tdd-code-builder: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C893 | 2 | KEEP-ROUTING | staff-tdd-code-builder: canonical path 00_skills/(development)/staff-tdd-code-builder/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C894 | 3 | KEEP-POLICY | staff-tdd-code-builder: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C895 | 3 | KEEP-ROUTING | subagent-creator: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C896 | 2 | KEEP-ROUTING | subagent-creator: canonical path 00_skills/(creation)/subagent-creator/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C897 | 3 | KEEP-POLICY | subagent-creator: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C898 | 3 | KEEP-POLICY | Limits the audit to authorized defensive scope and forbids exposing secret values | high | keep |
| C899 | 2 | KEEP-ROUTING | supply-chain-auditor: canonical path 00_skills/(security)/supply-chain-auditor/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C900 | 3 | KEEP-POLICY | supply-chain-auditor: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C901 | 3 | KEEP-ROUTING | tactical-ddd: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C902 | 2 | KEEP-ROUTING | tactical-ddd: canonical path 00_skills/(architecture)/tactical-ddd/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C903 | 3 | KEEP-POLICY | tactical-ddd: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C904 | 3 | KEEP-ROUTING | task-graph-builder: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C905 | 2 | KEEP-ROUTING | task-graph-builder: canonical path 00_skills/(tooling)/task-graph-builder/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C906 | 3 | KEEP-POLICY | task-graph-builder: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C907 | 3 | KEEP-ROUTING | technical-design-doc-creator: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C908 | 3 | KEEP-ROUTING | technical-design-doc-creator stub does not match canonical dir create-technical-design-doc; the alias and module-load rule are a route, not a listing | high | keep |
| C909 | 3 | KEEP-POLICY | technical-design-doc-creator: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C910 | 3 | KEEP-POLICY | Forbids restart, scale, or live mutation without an authorized operations task; authorization is not a manifest key | high | keep |
| C911 | 2 | KEEP-ROUTING | telemetry-bug-root-cause-solver: canonical path 00_skills/(monitoring)/telemetry-bug-root-cause-solver/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C912 | 3 | KEEP-POLICY | telemetry-bug-root-cause-solver: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C913 | 3 | KEEP-POLICY | Forbids treating the gap analysis as deployment authorization or as evidence for checks that were not run | high | keep |
| C914 | 2 | KEEP-ROUTING | test-gap-analyzer: canonical path 00_skills/(quality)/test-gap-analyzer/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C915 | 3 | KEEP-POLICY | test-gap-analyzer: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C916 | 3 | KEEP-POLICY | Constrains proposed tests to a sandbox and forbids using the result as deployment authorization | high | keep |
| C917 | 2 | KEEP-ROUTING | test-generation: canonical path 00_skills/(quality)/test-generation/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C918 | 3 | KEEP-POLICY | test-generation: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C919 | 3 | KEEP-POLICY | Forbids using the strategy as deployment authorization or as evidence for checks that were not executed | high | keep |
| C920 | 2 | KEEP-ROUTING | test-strategy-architect: canonical path 00_skills/(quality)/test-strategy-architect/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C921 | 3 | KEEP-POLICY | test-strategy-architect: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C922 | 3 | KEEP-POLICY | Forbids writing proposed tests into real test directories and forbids deployment-authorization use | high | keep |
| C923 | 2 | KEEP-ROUTING | test-writer: canonical path 00_skills/(quality)/test-writer/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C924 | 3 | KEEP-POLICY | test-writer: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C925 | 3 | KEEP-ROUTING | tests-expert: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C926 | 2 | KEEP-ROUTING | tests-expert: canonical path 00_skills/(quality)/tests-expert/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C927 | 3 | KEEP-POLICY | tests-expert: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C928 | 3 | KEEP-ROUTING | the-fool: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C929 | 2 | KEEP-ROUTING | the-fool: canonical path 00_skills/(decision-making)/the-fool/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C930 | 3 | KEEP-POLICY | the-fool: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C931 | 3 | KEEP-COMPRESSED | Compressed review contract covers gh review, official-doc checks, evidence, a noise gate, and verdict weights; none of that is a manifest string or one listing | medium | keep |
| C932 | 2 | KEEP-ROUTING | the-judge: canonical path 00_skills/(quality)/the-judge/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C933 | 3 | KEEP-POLICY | the-judge: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C934 | 3 | KEEP-ROUTING | the-jury: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C935 | 2 | KEEP-ROUTING | the-jury: canonical path 00_skills/(decision-making)/the-jury/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C936 | 3 | KEEP-POLICY | the-jury: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C937 | 3 | KEEP-POLICY | Limits threat modeling to authorized defensive scope and forbids exposing secret values | high | keep |
| C938 | 2 | KEEP-ROUTING | threat-modeler: canonical path 00_skills/(security)/threat-modeler/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C939 | 3 | KEEP-POLICY | threat-modeler: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C940 | 3 | KEEP-ROUTING | tlc-discover: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C941 | 2 | KEEP-ROUTING | tlc-discover: canonical path 00_skills/(development)/tlc-discover/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C942 | 3 | KEEP-POLICY | tlc-discover: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C943 | 3 | KEEP-ROUTING | tlc-generative-engine-optimization: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C944 | 2 | KEEP-ROUTING | tlc-generative-engine-optimization: canonical path 00_skills/(quality)/tlc-generative-engine-optimization/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C945 | 3 | KEEP-POLICY | tlc-generative-engine-optimization: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C946 | 3 | KEEP-ROUTING | tlc-implement: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C947 | 2 | KEEP-ROUTING | tlc-implement: canonical path 00_skills/(development)/tlc-implement/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C948 | 3 | KEEP-POLICY | tlc-implement: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C949 | 3 | KEEP-ROUTING | tlc-plan: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C950 | 2 | KEEP-ROUTING | tlc-plan: canonical path 00_skills/(development)/tlc-plan/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C951 | 3 | KEEP-POLICY | tlc-plan: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C952 | 3 | KEEP-ROUTING | tlc-prd: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C953 | 2 | KEEP-ROUTING | tlc-prd: canonical path 00_skills/(development)/tlc-prd/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C954 | 3 | KEEP-POLICY | tlc-prd: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C955 | 3 | KEEP-ROUTING | tlc-spec-driven: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C956 | 2 | KEEP-ROUTING | tlc-spec-driven: canonical path 00_skills/(development)/tlc-spec-driven/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C957 | 3 | KEEP-POLICY | tlc-spec-driven: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C958 | 3 | KEEP-ROUTING | tlc-spec-lean: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C959 | 2 | KEEP-ROUTING | tlc-spec-lean: canonical path 00_skills/(development)/tlc-spec-lean/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C960 | 3 | KEEP-POLICY | tlc-spec-lean: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C961 | 3 | KEEP-POLICY | Forbids promoting unverified claims or transient task status into durable memory | high | keep |
| C962 | 2 | KEEP-ROUTING | token-budget-governor: canonical path 00_skills/(learning)/token-budget-governor/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C963 | 3 | KEEP-POLICY | token-budget-governor: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C964 | 3 | KEEP-ROUTING | tool-router-audit: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C965 | 2 | KEEP-ROUTING | tool-router-audit: canonical path 00_skills/(tooling)/tool-router-audit/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C966 | 3 | KEEP-POLICY | tool-router-audit: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C967 | 3 | KEEP-ROUTING | typesafe-ai: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C968 | 2 | KEEP-ROUTING | typesafe-ai: canonical path 00_skills/(development)/typesafe-ai/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C969 | 3 | KEEP-POLICY | typesafe-ai: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C970 | 3 | KEEP-ROUTING | unique-environment-auditor: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C971 | 2 | KEEP-ROUTING | unique-environment-auditor: canonical path 00_skills/(development)/unique-environment-auditor/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C972 | 3 | KEEP-POLICY | unique-environment-auditor: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C973 | 3 | KEEP-ROUTING | universal-project-factory: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C974 | 2 | KEEP-ROUTING | universal-project-factory: canonical path 00_skills/(creation)/universal-project-factory/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C975 | 3 | KEEP-POLICY | universal-project-factory: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C976 | 3 | KEEP-POLICY | Forbids treating the readiness report as deployment authorization or as proof of checks not run | high | keep |
| C977 | 2 | KEEP-ROUTING | v1-readiness-auditor: canonical path 00_skills/(quality)/v1-readiness-auditor/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C978 | 3 | KEEP-POLICY | v1-readiness-auditor: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C979 | 3 | KEEP-ROUTING | vercel-deploy: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C980 | 2 | KEEP-ROUTING | vercel-deploy: canonical path 00_skills/(cloud)/vercel-deploy/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C981 | 3 | KEEP-POLICY | vercel-deploy: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C982 | 3 | KEEP-ROUTING | video-outreach: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C983 | 2 | KEEP-ROUTING | video-outreach: canonical path 00_skills/(gtm)/video-outreach/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C984 | 3 | KEEP-POLICY | video-outreach: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C985 | 3 | KEEP-POLICY | Treats skill activation as current-session consent to record or transcribe user audio; consent is policy | high | keep |
| C986 | 2 | KEEP-ROUTING | voiceai: canonical path 00_skills/(tooling)/voiceai/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C987 | 3 | KEEP-POLICY | voiceai: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C988 | 3 | KEEP-ROUTING | vox-aurum: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C989 | 2 | KEEP-ROUTING | vox-aurum: canonical path 00_skills/(tooling)/vox-aurum/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C990 | 3 | KEEP-POLICY | vox-aurum: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C991 | 3 | KEEP-ROUTING | vuln-obsol-recon: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C992 | 2 | KEEP-ROUTING | vuln-obsol-recon: canonical path 00_skills/(security)/vuln-obsol-recon/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C993 | 3 | KEEP-POLICY | vuln-obsol-recon: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C994 | 3 | KEEP-ROUTING | web-accessibility: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C995 | 2 | KEEP-ROUTING | web-accessibility: canonical path 00_skills/(quality)/web-accessibility/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C996 | 3 | KEEP-POLICY | web-accessibility: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C997 | 3 | KEEP-ROUTING | web-best-practices: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C998 | 2 | KEEP-ROUTING | web-best-practices: canonical path 00_skills/(quality)/web-best-practices/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C999 | 3 | KEEP-POLICY | web-best-practices: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C1000 | 3 | KEEP-ROUTING | web-design-guidelines: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C1001 | 2 | KEEP-ROUTING | web-design-guidelines: canonical path 00_skills/(design)/web-design-guidelines/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C1002 | 3 | KEEP-POLICY | web-design-guidelines: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C1003 | 3 | KEEP-ROUTING | web-quality-audit: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C1004 | 2 | KEEP-ROUTING | web-quality-audit: canonical path 00_skills/(quality)/web-quality-audit/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C1005 | 3 | KEEP-POLICY | web-quality-audit: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C1006 | 3 | KEEP-ROUTING | whatsapp-simulator: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C1007 | 2 | KEEP-ROUTING | whatsapp-simulator: canonical path 00_skills/(tooling)/whatsapp-simulator/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C1008 | 3 | KEEP-POLICY | whatsapp-simulator: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C1009 | 3 | KEEP-ROUTING | wordpress-expert: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C1010 | 2 | KEEP-ROUTING | wordpress-expert: canonical path 00_skills/(development)/wordpress-expert/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C1011 | 3 | KEEP-POLICY | wordpress-expert: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| C1012 | 3 | KEEP-ROUTING | workbench-profile-resolver: trigger phrases and Do NOT exclusions are invocation routing; the directory name and manifests do not state them | high | keep |
| C1013 | 2 | KEEP-ROUTING | workbench-profile-resolver: canonical path 00_skills/(tooling)/workbench-profile-resolver/SKILL.md and its sibling modules are outside the one-file stub; bucket lookup is a cross-tree read | high | keep |
| C1014 | 3 | KEEP-POLICY | workbench-profile-resolver: single-agent identity and Full Workspace v2 are process policy; the stub lists only SKILL.md and no manifest carries the rule | high | keep |
| P003 | 1 | REDUNDANT-GENERAL | workflow-tips is not in the tree; clear names and small functions are generic style with no repo fact | high | drop generic style line |
| P004 | 1 | REDUNDANT-GENERAL | workflow-tips is not in the tree; thin layers is generic architecture advice, not a manifest or file header | high | drop generic style line |
| P005 | 3 | KEEP-POLICY | Ban on committing secrets and the env-outside-version-control rule are process policy, not an exact manifest key | high | keep |
| P006 | 3 | KEEP-CAVEAT | Local success can still fail in CI when machine-local env or secrets are absent; that is an environment caveat | high | keep |
