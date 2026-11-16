# Blind scores Judge2
> run: 2026-11-13-full
> model: grok-4.7
> partitions: slice-01 .. slice-06

Counts: KEEP-CAVEAT=58 KEEP-COMPRESSED=65 KEEP-POLICY=450 KEEP-ROUTING=438 REDUNDANT-GENERAL=6 UNCLEAR=1

| ID | Cost | Class | Evidence | Confidence | Trim suggestion |
| C001 | 3 | KEEP-POLICY | Constitutional uniqueness is process; inventory manifests empty; 00_skills/STANDARD.md defers to AGENTS.md and does not state this sentence. | high | keep |
| C002 | 3 | KEEP-POLICY | Mission-scope mandate is process; not a manifest string or a directory listing. | high | keep |
| C003 | 3 | KEEP-POLICY | Six-phase lifecycle is process. 00_skills/STANDARD.md echoes the arrow later in the file and still names AGENTS.md as the contract. | high | keep |
| C004 | 3 | KEEP-ROUTING | Read-first routing. .notebook/INDEX.md header repeats the read mandate only after the file is opened; listing .notebook does not state order. | high | keep |
| C005 | 3 | KEEP-POLICY | .notebook listing shows HANDOFF.md, MEMORY.md, PROGRESS.md, LEARNING.md; the ensure-they-exist mandate is not in that listing. | high | keep |
| C006 | 3 | KEEP-POLICY | Which quartet files to load before planning, and when to skip LEARNING.md, is process; INDEX one-liners do not state that order. | high | keep |
| C007 | 3 | KEEP-POLICY | Required briefing fields are a workspace checklist, not a manifest or file header. | high | keep |
| C008 | 3 | KEEP-POLICY | Goal-shaping rule is process. No manifest or single header restates it. | medium | keep |
| C009 | 3 | KEEP-ROUTING | Routes the agent to skills, playbooks, MCPs, LSPs, and current docs before action; not shown by one listing. | high | keep |
| C010 | 3 | KEEP-POLICY | Recon rule is process. A tree listing does not state inspect-before-edit. | medium | keep |
| C011 | 3 | KEEP-POLICY | Convention preference is process, not a discovered config value. | medium | keep |
| C012 | 3 | KEEP-POLICY | Requires project evidence plus current official docs for APIs and versions; not in inventory manifests. | high | keep |
| C013 | 3 | KEEP-COMPRESSED | Ordered verification chain from .notebook through web research is a compressed procedure, not one header. | high | keep format rule |
| C014 | 3 | KEEP-CAVEAT | Treats stale continuity as a defect that must be reconciled; not visible from .notebook filenames. | high | keep constraint |
| C015 | 3 | KEEP-POLICY | Simplicity rule is process. No manifest echo. | medium | keep |
| C016 | 3 | KEEP-POLICY | Trade-off disclosure is process, not a code or config fact. | medium | keep |
| C017 | 3 | KEEP-POLICY | Pre-execution checkpoints are a required planning gate. | high | keep |
| C018 | 3 | KEEP-POLICY | Surgical-change rule binds every line to the mission; not rediscovered from a listing. | high | keep |
| C019 | 3 | KEEP-POLICY | Write mandate for PROGRESS.md checklist and acceptance gates; the file exists but does not state this duty. | high | keep |
| C020 | 3 | KEEP-POLICY | Think-before-coding is process. Cost 3 blocks a general-redundancy class. | medium | keep |
| C021 | 3 | KEEP-POLICY | Minimum-code rule is process, not a manifest or header. | medium | keep |
| C022 | 3 | KEEP-POLICY | Specific ban on extra features, abstractions, config, speculative optimization, and unrelated refactors. | high | keep |
| C023 | 3 | KEEP-POLICY | Match-local-style rule is process; conventions are not one file header. | medium | keep |
| C024 | 3 | KEEP-POLICY | Non-deprecated API rule is process, not a discovered dependency manifest. | medium | keep |
| C025 | 3 | KEEP-POLICY | Lockfile check and silent-package ban are process. Root inventory manifests are empty. | high | keep |
| C026 | 3 | KEEP-CAVEAT | Silent error swallowing is a failure caveat, not shown by a listing. | high | keep constraint |
| C027 | 3 | KEEP-POLICY | Comment-why rule is process; source files do not carry this legend in a header. | medium | keep |
| C028 | 3 | KEEP-COMPRESSED | .notebook/PROGRESS.md uses [x] [~] [ ] but does not define the [ ] [~] [x] [!] legend. | high | keep format rule |
| C029 | 3 | KEEP-CAVEAT | Cookie-jar, redaction, and compromise rule is environment policy; absent from manifests. | high | keep constraint |
| C030 | 3 | KEEP-POLICY | Verify contracts rather than implementation details is a test-policy gate. | high | keep |
| C031 | 3 | KEEP-POLICY | Baseline-first when tests are in scope is process, not a test-runner config. | high | keep |
| C032 | 3 | KEEP-POLICY | Reproduce-then-root-cause order is process, not a code header. | high | keep |
| C033 | 3 | KEEP-POLICY | Smallest-check-first order is a verification policy. | high | keep |
| C034 | 3 | KEEP-POLICY | PROGRESS [x] only after the stated gate is a status policy, not the checkbox characters in the log. | high | keep |
| C035 | 3 | KEEP-CAVEAT | Do not invent out-of-scope tests, and flag untested risk; not a test manifest. | high | keep constraint |
| C036 | 3 | KEEP-POLICY | Debrief contents (change, verification, risk, uncertainty) are process. | high | keep |
| C037 | 3 | KEEP-POLICY | Notebook writes limited to durable findings are process; notes do not state the filter. | high | keep |
| C038 | 3 | KEEP-POLICY | HANDOFF refresh triggers (pause, session boundary, remaining work) are process. | high | keep |
| C039 | 3 | KEEP-POLICY | MEMORY admission rule (verified durable facts only) is process; MEMORY.md header does not state it. | high | keep |
| C040 | 3 | KEEP-POLICY | LEARNING versus PROGRESS split is process; both files exist without this rule in their headers. | high | keep |
| C041 | 3 | KEEP-CAVEAT | Stale-note defect rule is a caveat, not implied by note filenames. | high | keep constraint |
| C042 | 3 | KEEP-POLICY | Pointer-not-paste rule for notes is process. | high | keep |
| C043 | 3 | KEEP-ROUTING | Routes to references/CODENAVI_CONTINUITY_STANDARD.md, which is not in the repo and not a manifest. | high | keep |
| C044 | 3 | KEEP-POLICY | HANDOFF role (working set, blockers, not a diary) exceeds the INDEX one-liner. | high | keep |
| C045 | 3 | KEEP-POLICY | MEMORY role including no secrets and no transient status is process; INDEX line is shorter. | high | keep |
| C046 | 3 | KEEP-POLICY | PROGRESS as mission-state source of truth is process; the log does not declare that. | high | keep |
| C047 | 3 | KEEP-POLICY | LEARNING field contract (trigger, cause, fix, reuse, evidence) is process; the file demonstrates entries without defining the schema. | high | keep |
| C048 | 3 | KEEP-POLICY | Non-duplication and cross-link rule across the four files is process. | high | keep |
| C049 | 3 | KEEP-CAVEAT | Secret and cookie-content ban in continuity artifacts is environment policy. | high | keep constraint |
| C050 | 3 | KEEP-POLICY | Names five skills as skills of codenavi-agent and forbids separate agents; a skill-dir listing does not state that. | high | keep |
| C051 | 3 | KEEP-POLICY | Think-before-coding principle is process, including when to ask and when to challenge. | medium | keep |
| C052 | 3 | KEEP-POLICY | Simplicity-first principle is process. | medium | keep |
| C053 | 3 | KEEP-POLICY | No adjacent cleanup unless the mission caused it is a specific change policy. | high | keep |
| C054 | 3 | KEEP-POLICY | Measurable completion criteria are a process gate. | high | keep |
| C055 | 3 | KEEP-POLICY | Local conventions as default unless unsafe or obsolete is process. | medium | keep |
| C056 | 3 | KEEP-CAVEAT | Do not trust model memory for API signatures is a caveat; not in a manifest. | high | keep constraint |
| C057 | 3 | KEEP-POLICY | Reuse-before-add with rationale is dependency policy. No root manifest was discovered. | high | keep |
| C058 | 3 | KEEP-CAVEAT | No silent error swallowing is a failure caveat. | high | keep constraint |
| C059 | 3 | KEEP-POLICY | Test contracts and reproduce bugs first is process, not a test config. | high | keep |
| C060 | 3 | KEEP-POLICY | Comment-why principle is process. | medium | keep |
| C061 | 1 | KEEP-ROUTING | .notebook/INDEX.md header says project intelligence, read before every material mission. That is one file header, not a manifest, so the read mandate stays. | medium | keep |
| C062 | 3 | KEEP-POLICY | INDEX lists the four files first but does not say they are reserved and must stay first. | high | keep |
| C063 | 3 | KEEP-COMPRESSED | .notebook is flat today; flows, patterns, gotchas, domain, graph, and archive rules are not in the listing. | high | keep format rule |
| C064 | 3 | KEEP-COMPRESSED | INDEX rows match slug, summary, category, tags, but the max-100-char template is not stated in the file. | high | keep format rule |
| C065 | 3 | KEEP-COMPRESSED | Example tags are lowercase; the 2-4 count and domain-plus-technology-plus-action span are not in the header. | high | keep format rule |
| C066 | 3 | KEEP-POLICY | Recency sort plus pinned quartet is a format policy; INDEX does not state the sort key. | high | keep |
| C067 | 3 | KEEP-POLICY | Telegraphic notes, not duplicated docs, is process. | high | keep |
| C068 | 3 | KEEP-POLICY | One concept per note is a writing policy, not a file header. | medium | keep |
| C069 | 3 | KEEP-COMPRESSED | Some notes show Updated and an entry point; the always-required template is not defined there. | high | keep format rule |
| C070 | 3 | KEEP-COMPRESSED | Pointer shapes path/file.ts:function(), line ranges, and Class.method() are a compressed citation spec. | high | keep format rule |
| C071 | 3 | KEEP-POLICY | Observations and measurable impacts, not opinions, is process. | medium | keep |
| C072 | 3 | KEEP-CAVEAT | Ban on inventing a full notebook analysis is a caveat. | high | keep constraint |
| C073 | 3 | KEEP-POLICY | Progressive disclosure is mandatory. STANDARD.md mentions it only inside a longer standard that defers to AGENTS.md. | high | keep |
| C074 | 3 | KEEP-POLICY | Single identity codenavi-agent is process. STANDARD.md states one identity and points back at AGENTS.md. | high | keep |
| C075 | 3 | KEEP-POLICY | Ban on personas, specialist agents, subagents, and overlays is process, not a directory fact. | high | keep |
| C076 | 3 | KEEP-POLICY | Specialization list (skills, super-skills, playbooks, MCPs, LSPs, lenses, tools) is policy. | high | keep |
| C077 | 3 | KEEP-POLICY | Critical-thinking lenses are not agents. STANDARD.md is a partial echo, not the full rule. | high | keep |
| C078 | 3 | KEEP-POLICY | Judge as a deterministic gate, never a persona, is process. | high | keep |
| C079 | 3 | KEEP-POLICY | CodENavi Full Workspace v2 banner is the governance label; not an inventory manifest. | high | keep |
| C080 | 3 | KEEP-POLICY | references/CODENAVI_FULL_WORKSPACE_STANDARD.md is absent; the subtree non-weakening contract is process. | high | keep |
| C081 | 3 | KEEP-POLICY | Creation-standard lead-in for new governed artifacts is process. | high | keep |
| C082 | 3 | KEEP-POLICY | New artifacts must inherit this agent standard; not a config key. | high | keep |
| C083 | 3 | KEEP-POLICY | Six-phase lifecycle requirement for new artifacts is process. | high | keep |
| C084 | 3 | KEEP-POLICY | Must use the coding principles above is an internal process cross-reference. | medium | keep |
| C085 | 3 | KEEP-POLICY | New artifacts must respect notebook disclosure and the quartet. | high | keep |
| C086 | 3 | KEEP-CAVEAT | Governed secret handling and external cookie-jar references are environment policy. | high | keep constraint |
| C087 | 3 | KEEP-POLICY | Required scope, inputs, outputs, risks, and verification for new artifacts. | high | keep |
| C088 | 3 | KEEP-POLICY | Ban on new agent identities for future artifacts is process. | high | keep |
| C089 | 3 | KEEP-CAVEAT | Fail closed on missing evidence, permissions, or safety gates. | high | keep constraint |
| C090 | 3 | KEEP-POLICY | Byte-identical canonical AGENTS.md and no legacy constitution precedence is process; STANDARD.md does not say byte-identical. | high | keep |
| C091 | 2 | KEEP-ROUTING | Trigger and exclusion text for accessibility is not in inventory manifests. Recovering it means reading 00_skills/(quality)/web-accessibility/SKILL.md or the long catalog, not one directory listing. Stub name accessibility does not match folder web-accessibility. | medium | keep triggers and exclusions |
| C092 | 2 | KEEP-ROUTING | 00_skills/(quality)/web-accessibility/SKILL.md exists. The category path is not obvious from one listing of .agents/skills/accessibility. Stub name accessibility does not match folder web-accessibility. | high | keep path pointer |
| C093 | 3 | KEEP-POLICY | Governance line on accessibility is process. Canonical 00_skills headers say inherit AGENTS.md, not this no-additional-identity sentence, and it is not a discovered manifest. | high | keep identity sentence |
| C094 | 2 | KEEP-ROUTING | Trigger and exclusion text for acta-aurea is not in inventory manifests. Recovering it means reading 00_skills/(tooling)/acta-aurea/SKILL.md or the long catalog, not one directory listing. | medium | keep triggers and exclusions |
| C095 | 2 | KEEP-ROUTING | 00_skills/(tooling)/acta-aurea/SKILL.md exists. The category path is not obvious from one listing of .agents/skills/acta-aurea. | high | keep path pointer |
| C096 | 3 | KEEP-POLICY | Governance line on acta-aurea is process. Canonical 00_skills headers say inherit AGENTS.md, not this no-additional-identity sentence, and it is not a discovered manifest. | high | keep identity sentence |
| C097 | 2 | KEEP-ROUTING | Trigger and exclusion text for adr-decision-writer is not in inventory manifests. Recovering it means reading 00_skills/(development)/adr-decision-writer/SKILL.md or the long catalog, not one directory listing. | medium | keep triggers and exclusions |
| C098 | 2 | KEEP-ROUTING | 00_skills/(development)/adr-decision-writer/SKILL.md exists. The category path is not obvious from one listing of .agents/skills/adr-decision-writer. | high | keep path pointer |
| C099 | 3 | KEEP-POLICY | Governance line on adr-decision-writer is process. Canonical 00_skills headers say inherit AGENTS.md, not this no-additional-identity sentence, and it is not a discovered manifest. | high | keep identity sentence |
| C100 | 2 | KEEP-ROUTING | Trigger and exclusion text for agent-trace-validator is not in inventory manifests. Recovering it means reading 00_skills/(quality)/agent-trace-validator/SKILL.md or the long catalog, not one directory listing. | medium | keep triggers and exclusions |
| C101 | 2 | KEEP-ROUTING | 00_skills/(quality)/agent-trace-validator/SKILL.md exists. The category path is not obvious from one listing of .agents/skills/agent-trace-validator. | high | keep path pointer |
| C102 | 3 | KEEP-POLICY | Governance line on agent-trace-validator is process. Canonical 00_skills headers say inherit AGENTS.md, not this no-additional-identity sentence, and it is not a discovered manifest. | high | keep identity sentence |
| C103 | 2 | KEEP-ROUTING | Trigger and exclusion text for ai-architecture-expert is not in inventory manifests. Recovering it means reading 00_skills/(architecture)/ai-architecture-expert/SKILL.md or the long catalog, not one directory listing. | medium | keep triggers and exclusions |
| C104 | 2 | KEEP-ROUTING | 00_skills/(architecture)/ai-architecture-expert/SKILL.md exists. The category path is not obvious from one listing of .agents/skills/ai-architecture-expert. | high | keep path pointer |
| C105 | 3 | KEEP-POLICY | Governance line on ai-architecture-expert is process. Canonical 00_skills headers say inherit AGENTS.md, not this no-additional-identity sentence, and it is not a discovered manifest. | high | keep identity sentence |
| C106 | 2 | KEEP-ROUTING | Trigger and exclusion text for ai-cold-outreach is not in inventory manifests. Recovering it means reading 00_skills/(gtm)/ai-cold-outreach/SKILL.md or the long catalog, not one directory listing. | medium | keep triggers and exclusions |
| C107 | 2 | KEEP-ROUTING | 00_skills/(gtm)/ai-cold-outreach/SKILL.md exists. The category path is not obvious from one listing of .agents/skills/ai-cold-outreach. | high | keep path pointer |
| C108 | 3 | KEEP-POLICY | Governance line on ai-cold-outreach is process. Canonical 00_skills headers say inherit AGENTS.md, not this no-additional-identity sentence, and it is not a discovered manifest. | high | keep identity sentence |
| C109 | 2 | KEEP-ROUTING | Trigger and exclusion text for ai-continuous-training-maintainer is not in inventory manifests. Recovering it means reading 00_skills/(development)/ai-continuous-training-maintainer/SKILL.md or the long catalog, not one directory listing. | medium | keep triggers and exclusions |
| C110 | 2 | KEEP-ROUTING | 00_skills/(development)/ai-continuous-training-maintainer/SKILL.md exists. The category path is not obvious from one listing of .agents/skills/ai-continuous-training-maintainer. | high | keep path pointer |
| C111 | 3 | KEEP-POLICY | Governance line on ai-continuous-training-maintainer is process. Canonical 00_skills headers say inherit AGENTS.md, not this no-additional-identity sentence, and it is not a discovered manifest. | high | keep identity sentence |
| C112 | 2 | KEEP-ROUTING | Trigger and exclusion text for ai-engineering-expert is not in inventory manifests. Recovering it means reading 00_skills/(development)/ai-engineering-expert/SKILL.md or the long catalog, not one directory listing. | medium | keep triggers and exclusions |
| C113 | 2 | KEEP-ROUTING | 00_skills/(development)/ai-engineering-expert/SKILL.md exists. The category path is not obvious from one listing of .agents/skills/ai-engineering-expert. | high | keep path pointer |
| C114 | 3 | KEEP-POLICY | Governance line on ai-engineering-expert is process. Canonical 00_skills headers say inherit AGENTS.md, not this no-additional-identity sentence, and it is not a discovered manifest. | high | keep identity sentence |
| C115 | 2 | KEEP-ROUTING | Trigger and exclusion text for ai-evals-expert is not in inventory manifests. Recovering it means reading 00_skills/(quality)/ai-evals-expert/SKILL.md or the long catalog, not one directory listing. | medium | keep triggers and exclusions |
| C116 | 2 | KEEP-ROUTING | 00_skills/(quality)/ai-evals-expert/SKILL.md exists. The category path is not obvious from one listing of .agents/skills/ai-evals-expert. | high | keep path pointer |
| C117 | 3 | KEEP-POLICY | Governance line on ai-evals-expert is process. Canonical 00_skills headers say inherit AGENTS.md, not this no-additional-identity sentence, and it is not a discovered manifest. | high | keep identity sentence |
| C118 | 2 | KEEP-ROUTING | Trigger and exclusion text for ai-pricing is not in inventory manifests. Recovering it means reading 00_skills/(gtm)/ai-pricing/SKILL.md or the long catalog, not one directory listing. | medium | keep triggers and exclusions |
| C119 | 2 | KEEP-ROUTING | 00_skills/(gtm)/ai-pricing/SKILL.md exists. The category path is not obvious from one listing of .agents/skills/ai-pricing. | high | keep path pointer |
| C120 | 3 | KEEP-POLICY | Governance line on ai-pricing is process. Canonical 00_skills headers say inherit AGENTS.md, not this no-additional-identity sentence, and it is not a discovered manifest. | high | keep identity sentence |
| C121 | 2 | KEEP-ROUTING | Trigger and exclusion text for ai-project-bootstrapper is not in inventory manifests. Recovering it means reading 00_skills/(creation)/ai-project-bootstrapper/SKILL.md or the long catalog, not one directory listing. | medium | keep triggers and exclusions |
| C122 | 2 | KEEP-ROUTING | 00_skills/(creation)/ai-project-bootstrapper/SKILL.md exists. The category path is not obvious from one listing of .agents/skills/ai-project-bootstrapper. | high | keep path pointer |
| C123 | 3 | KEEP-POLICY | Governance line on ai-project-bootstrapper is process. Canonical 00_skills headers say inherit AGENTS.md, not this no-additional-identity sentence, and it is not a discovered manifest. | high | keep identity sentence |
| C124 | 2 | KEEP-ROUTING | Trigger and exclusion text for ai-sdr is not in inventory manifests. Recovering it means reading 00_skills/(gtm)/ai-sdr/SKILL.md or the long catalog, not one directory listing. | medium | keep triggers and exclusions |
| C125 | 2 | KEEP-ROUTING | 00_skills/(gtm)/ai-sdr/SKILL.md exists. The category path is not obvious from one listing of .agents/skills/ai-sdr. | high | keep path pointer |
| C126 | 3 | KEEP-POLICY | Governance line on ai-sdr is process. Canonical 00_skills headers say inherit AGENTS.md, not this no-additional-identity sentence, and it is not a discovered manifest. | high | keep identity sentence |
| C127 | 2 | KEEP-ROUTING | Trigger and exclusion text for ai-seo is not in inventory manifests. Recovering it means reading 00_skills/(gtm)/ai-seo/SKILL.md or the long catalog, not one directory listing. | medium | keep triggers and exclusions |
| C128 | 2 | KEEP-ROUTING | 00_skills/(gtm)/ai-seo/SKILL.md exists. The category path is not obvious from one listing of .agents/skills/ai-seo. | high | keep path pointer |
| C129 | 3 | KEEP-POLICY | Governance line on ai-seo is process. Canonical 00_skills headers say inherit AGENTS.md, not this no-additional-identity sentence, and it is not a discovered manifest. | high | keep identity sentence |
| C130 | 2 | KEEP-ROUTING | Trigger and exclusion text for ai-ugc-ads is not in inventory manifests. Recovering it means reading 00_skills/(gtm)/ai-ugc-ads/SKILL.md or the long catalog, not one directory listing. | medium | keep triggers and exclusions |
| C131 | 2 | KEEP-ROUTING | 00_skills/(gtm)/ai-ugc-ads/SKILL.md exists. The category path is not obvious from one listing of .agents/skills/ai-ugc-ads. | high | keep path pointer |
| C132 | 3 | KEEP-POLICY | Governance line on ai-ugc-ads is process. Canonical 00_skills headers say inherit AGENTS.md, not this no-additional-identity sentence, and it is not a discovered manifest. | high | keep identity sentence |
| C133 | 2 | KEEP-ROUTING | Trigger and exclusion text for angular-20-expert is not in inventory manifests. Recovering it means reading 00_skills/(development)/angular-20-expert/SKILL.md or the long catalog, not one directory listing. | medium | keep triggers and exclusions |
| C134 | 2 | KEEP-ROUTING | 00_skills/(development)/angular-20-expert/SKILL.md exists. The category path is not obvious from one listing of .agents/skills/angular-20-expert. | high | keep path pointer |
| C135 | 3 | KEEP-POLICY | Governance line on angular-20-expert is process. Canonical 00_skills headers say inherit AGENTS.md, not this no-additional-identity sentence, and it is not a discovered manifest. | high | keep identity sentence |
| C136 | 2 | KEEP-ROUTING | Trigger and exclusion text for angular-8-to-20-migration is not in inventory manifests. Recovering it means reading 00_skills/(architecture)/angular-8-to-20-migration/SKILL.md or the long catalog, not one directory listing. | medium | keep triggers and exclusions |
| C137 | 2 | KEEP-ROUTING | 00_skills/(architecture)/angular-8-to-20-migration/SKILL.md exists. The category path is not obvious from one listing of .agents/skills/angular-8-to-20-migration. | high | keep path pointer |
| C138 | 3 | KEEP-POLICY | Governance line on angular-8-to-20-migration is process. Canonical 00_skills headers say inherit AGENTS.md, not this no-additional-identity sentence, and it is not a discovered manifest. | high | keep identity sentence |
| C139 | 2 | KEEP-ROUTING | Trigger and exclusion text for anti-hallucination-evaluator is not in inventory manifests. Recovering it means reading 00_skills/(quality)/anti-hallucination-evaluator/SKILL.md or the long catalog, not one directory listing. | medium | keep triggers and exclusions |
| C140 | 2 | KEEP-ROUTING | 00_skills/(quality)/anti-hallucination-evaluator/SKILL.md exists. The category path is not obvious from one listing of .agents/skills/anti-hallucination-evaluator. | high | keep path pointer |
| C141 | 3 | KEEP-POLICY | Governance line on anti-hallucination-evaluator is process. Canonical 00_skills headers say inherit AGENTS.md, not this no-additional-identity sentence, and it is not a discovered manifest. | high | keep identity sentence |
| C142 | 2 | KEEP-ROUTING | Trigger and exclusion text for approval-governance-auditor is not in inventory manifests. Recovering it means reading 00_skills/(security)/approval-governance-auditor/SKILL.md or the long catalog, not one directory listing. | medium | keep triggers and exclusions |
| C143 | 2 | KEEP-ROUTING | 00_skills/(security)/approval-governance-auditor/SKILL.md exists. The category path is not obvious from one listing of .agents/skills/approval-governance-auditor. | high | keep path pointer |
| C144 | 3 | KEEP-POLICY | Governance line on approval-governance-auditor is process. Canonical 00_skills headers say inherit AGENTS.md, not this no-additional-identity sentence, and it is not a discovered manifest. | high | keep identity sentence |
| C145 | 2 | KEEP-ROUTING | Trigger and exclusion text for approval-requester is not in inventory manifests. Recovering it means reading 00_skills/(security)/approval-requester/SKILL.md or the long catalog, not one directory listing. | medium | keep triggers and exclusions |
| C146 | 2 | KEEP-ROUTING | 00_skills/(security)/approval-requester/SKILL.md exists. The category path is not obvious from one listing of .agents/skills/approval-requester. | high | keep path pointer |
| C147 | 3 | KEEP-POLICY | Governance line on approval-requester is process. Canonical 00_skills headers say inherit AGENTS.md, not this no-additional-identity sentence, and it is not a discovered manifest. | high | keep identity sentence |
| C148 | 2 | KEEP-ROUTING | Trigger and exclusion text for architecturally-significant-requirement is not in inventory manifests. Recovering it means reading 00_skills/(development)/architecturally-significant-requirement/SKILL.md or the long catalog, not one directory listing. | medium | keep triggers and exclusions |
| C149 | 2 | KEEP-ROUTING | 00_skills/(development)/architecturally-significant-requirement/SKILL.md exists. The category path is not obvious from one listing of .agents/skills/architecturally-significant-requirement. | high | keep path pointer |
| C150 | 3 | KEEP-POLICY | Governance line on architecturally-significant-requirement is process. Canonical 00_skills headers say inherit AGENTS.md, not this no-additional-identity sentence, and it is not a discovered manifest. | high | keep identity sentence |
| C151 | 2 | KEEP-ROUTING | Trigger and exclusion text for architecture-decision-log is not in inventory manifests. Recovering it means reading 00_skills/(architecture)/architecture-decision-log/SKILL.md or the long catalog, not one directory listing. | medium | keep triggers and exclusions |
| C152 | 2 | KEEP-ROUTING | 00_skills/(architecture)/architecture-decision-log/SKILL.md exists. The category path is not obvious from one listing of .agents/skills/architecture-decision-log. | high | keep path pointer |
| C153 | 3 | KEEP-POLICY | Governance line on architecture-decision-log is process. Canonical 00_skills headers say inherit AGENTS.md, not this no-additional-identity sentence, and it is not a discovered manifest. | high | keep identity sentence |
| C154 | 2 | KEEP-ROUTING | Trigger and exclusion text for architecture-decision-record is not in inventory manifests. Recovering it means reading 00_skills/(architecture)/architecture-decision-record/SKILL.md or the long catalog, not one directory listing. | medium | keep triggers and exclusions |
| C155 | 2 | KEEP-ROUTING | 00_skills/(architecture)/architecture-decision-record/SKILL.md exists. The category path is not obvious from one listing of .agents/skills/architecture-decision-record. | high | keep path pointer |
| C156 | 3 | KEEP-POLICY | Governance line on architecture-decision-record is process. Canonical 00_skills headers say inherit AGENTS.md, not this no-additional-identity sentence, and it is not a discovered manifest. | high | keep identity sentence |
| C157 | 2 | KEEP-ROUTING | Trigger and exclusion text for architecture-knowledge-management is not in inventory manifests. Recovering it means reading 00_skills/(architecture)/architecture-knowledge-management/SKILL.md or the long catalog, not one directory listing. | medium | keep triggers and exclusions |
| C158 | 2 | KEEP-ROUTING | 00_skills/(architecture)/architecture-knowledge-management/SKILL.md exists. The category path is not obvious from one listing of .agents/skills/architecture-knowledge-management. | high | keep path pointer |
| C159 | 3 | KEEP-POLICY | Governance line on architecture-knowledge-management is process. Canonical 00_skills headers say inherit AGENTS.md, not this no-additional-identity sentence, and it is not a discovered manifest. | high | keep identity sentence |
| C160 | 2 | KEEP-ROUTING | Trigger and exclusion text for architecture-mapper is not in inventory manifests. Recovering it means reading 00_skills/(architecture)/architecture-mapper/SKILL.md or the long catalog, not one directory listing. | medium | keep triggers and exclusions |
| C161 | 2 | KEEP-ROUTING | 00_skills/(architecture)/architecture-mapper/SKILL.md exists. The category path is not obvious from one listing of .agents/skills/architecture-mapper. | high | keep path pointer |
| C162 | 3 | KEEP-POLICY | Governance line on architecture-mapper is process. Canonical 00_skills headers say inherit AGENTS.md, not this no-additional-identity sentence, and it is not a discovered manifest. | high | keep identity sentence |
| C163 | 2 | KEEP-ROUTING | Trigger and exclusion text for atualizar-dependencias is not in inventory manifests. Recovering it means reading 00_skills/(development)/atualizar-dependencias/SKILL.md or the long catalog, not one directory listing. | medium | keep triggers and exclusions |
| C164 | 2 | KEEP-ROUTING | 00_skills/(development)/atualizar-dependencias/SKILL.md exists. The category path is not obvious from one listing of .agents/skills/atualizar-dependencias. | high | keep path pointer |
| C165 | 3 | KEEP-POLICY | Governance line on atualizar-dependencias is process. Canonical 00_skills headers say inherit AGENTS.md, not this no-additional-identity sentence, and it is not a discovered manifest. | high | keep identity sentence |
| C166 | 2 | KEEP-ROUTING | Trigger and exclusion text for automation-orchestrator is not in inventory manifests. Recovering it means reading 00_skills/(tooling)/automation-orchestrator/SKILL.md or the long catalog, not one directory listing. | medium | keep triggers and exclusions |
| C167 | 2 | KEEP-ROUTING | 00_skills/(tooling)/automation-orchestrator/SKILL.md exists. The category path is not obvious from one listing of .agents/skills/automation-orchestrator. | high | keep path pointer |
| C168 | 3 | KEEP-POLICY | Governance line on automation-orchestrator is process. Canonical 00_skills headers say inherit AGENTS.md, not this no-additional-identity sentence, and it is not a discovered manifest. | high | keep identity sentence |
| C169 | 2 | KEEP-ROUTING | Trigger and exclusion text for aws-advisor is not in inventory manifests. Recovering it means reading 00_skills/(cloud)/aws-advisor/SKILL.md or the long catalog, not one directory listing. | medium | keep triggers and exclusions |
| C170 | 2 | KEEP-ROUTING | 00_skills/(cloud)/aws-advisor/SKILL.md exists. The category path is not obvious from one listing of .agents/skills/aws-advisor. | high | keep path pointer |
| C171 | 3 | KEEP-POLICY | aws-advisor governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C172 | 3 | KEEP-ROUTING | Trigger excludes accessibility, ai-seo, and a full multi-area audit. A directory listing does not state that boundary. | high | none |
| C173 | 2 | KEEP-ROUTING | best-practices listing does not show 00_skills/(quality)/web-best-practices/SKILL.md; leaf name is web-best-practices. Category bucket needs a second tree, so cost 2. | high | none |
| C174 | 3 | KEEP-POLICY | best-practices governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C175 | 3 | KEEP-ROUTING | Selection rule blocks unrelated implementation and deployment execution. Not a manifest string; manifests list is empty. | high | none |
| C176 | 2 | KEEP-ROUTING | blueprint-generator listing does not show category path 00_skills/(architecture)/blueprint-generator/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C177 | 3 | KEEP-POLICY | blueprint-generator governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C178 | 3 | KEEP-ROUTING | Lexical and hybrid BM25 purpose plus the invoke trigger are not in the empty manifest set. | high | Drop only the stock unrelated-languages sentence; keep the BM25 purpose and invoke line. |
| C179 | 2 | KEEP-ROUTING | bm25-expert listing does not show category path 00_skills/(development)/bm25-expert/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C180 | 3 | KEEP-POLICY | bm25-expert governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C181 | 3 | KEEP-ROUTING | Camel banking selection names reliability, security, traceability, and idempotency. Those bars are not config keys. | high | Drop only the stock unrelated-languages sentence; keep the banking quality bar. |
| C182 | 2 | KEEP-ROUTING | camel-banking-expert listing does not show category path 00_skills/(development)/camel-banking-expert/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C183 | 3 | KEEP-POLICY | camel-banking-expert governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C184 | 3 | KEEP-POLICY | Forbids treating the audit as deployment authorization or as evidence for checks that did not run. | high | none |
| C185 | 2 | KEEP-ROUTING | change-trace-auditor listing does not show category path 00_skills/(quality)/change-trace-auditor/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C186 | 3 | KEEP-POLICY | change-trace-auditor governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C187 | 3 | KEEP-ROUTING | Routes memory work away from fleet-mapping, memory-curator, learning-curator, and multi-agent reasoning. | high | none |
| C188 | 2 | KEEP-ROUTING | chromatic-mega-brain listing does not show category path 00_skills/(learning)/chromatic-mega-brain/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C189 | 3 | KEEP-POLICY | chromatic-mega-brain governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C190 | 3 | KEEP-ROUTING | Browser debug triggers split full E2E suites to playwright-skill and exclude non-browser debugging. | high | none |
| C191 | 2 | KEEP-ROUTING | chrome-devtools listing does not show category path 00_skills/(tooling)/chrome-devtools/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C192 | 3 | KEEP-POLICY | chrome-devtools governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C193 | 3 | KEEP-ROUTING | CI quality-gate selection is process text. Inventory manifest commands are empty. | high | Drop only the stock unrelated-languages sentence; keep the quality-gate purpose. |
| C194 | 2 | KEEP-ROUTING | ci-quality-gate-engineer listing does not show category path 00_skills/(development)/ci-quality-gate-engineer/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C195 | 3 | KEEP-POLICY | ci-quality-gate-engineer governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C196 | 3 | KEEP-ROUTING | Cloudflare deploy trigger explicitly excludes Vercel, Netlify, and Render skills. | high | none |
| C197 | 2 | KEEP-ROUTING | cloudflare-deploy listing does not show category path 00_skills/(cloud)/cloudflare-deploy/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C198 | 3 | KEEP-POLICY | cloudflare-deploy governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C199 | 3 | KEEP-POLICY | Bans production mutation and architecture claims that lack source evidence. | high | none |
| C200 | 2 | KEEP-ROUTING | code-analyzer listing does not show category path 00_skills/(mapping)/code-analyzer/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C201 | 3 | KEEP-POLICY | code-analyzer governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C202 | 3 | KEEP-COMPRESSED | Packs no-assumption behavior, .notebook continuity, and when to summon skills. The folder name does not state that contract. | high | none |
| C203 | 2 | KEEP-ROUTING | codenavi listing does not show category path 00_skills/(development)/codenavi/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C204 | 3 | KEEP-POLICY | codenavi governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C205 | 3 | KEEP-POLICY | Requires source evidence of the target repo conventions before code changes. | medium | Drop only the stock unrelated-languages sentence; keep the evidence-before-edit rule. |
| C206 | 2 | KEEP-ROUTING | coding-guidelines listing does not show category path 00_skills/(development)/coding-guidelines/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C207 | 3 | KEEP-POLICY | coding-guidelines governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C208 | 3 | KEEP-ROUTING | Compatibility trigger covers version conflicts, peers, platform constraints, and breaking-change risk. Not a manifest echo. | high | Drop only the stock unrelated-languages sentence; keep the compatibility checks. |
| C209 | 2 | KEEP-ROUTING | compatibility-analyzer listing does not show category path 00_skills/(development)/compatibility-analyzer/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C210 | 3 | KEEP-POLICY | compatibility-analyzer governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C211 | 3 | KEEP-POLICY | Forbids using the export as deployment authorization or as evidence of checks that did not run. | high | none |
| C212 | 2 | KEEP-ROUTING | compliance-audit-exporter listing does not show category path 00_skills/(quality)/compliance-audit-exporter/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C213 | 3 | KEEP-POLICY | compliance-audit-exporter governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C214 | 3 | KEEP-POLICY | Requires secret-safe export and forbids deployment authorization or credit for unexecuted checks. | high | none |
| C215 | 2 | KEEP-ROUTING | compliance-evidence-exporter listing does not show category path 00_skills/(quality)/compliance-evidence-exporter/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C216 | 3 | KEEP-POLICY | compliance-evidence-exporter governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C217 | 3 | KEEP-ROUTING | Sends code-level duplication to linters and dependency work to coupling-analysis. | high | none |
| C218 | 2 | KEEP-ROUTING | component-common-domain-detection listing does not show category path 00_skills/(architecture)/component-common-domain-detection/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C219 | 3 | KEEP-POLICY | component-common-domain-detection governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C220 | 3 | KEEP-ROUTING | Sends dependency analysis to coupling-analysis and domain grouping to domain-identification-grouping. | high | none |
| C221 | 2 | KEEP-ROUTING | component-flattening-analysis listing does not show category path 00_skills/(architecture)/component-flattening-analysis/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C222 | 3 | KEEP-POLICY | component-flattening-analysis governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C223 | 3 | KEEP-CAVEAT | Warns that component size is not runtime performance sizing or infrastructure capacity planning. | high | none |
| C224 | 2 | KEEP-ROUTING | component-identification-sizing listing does not show category path 00_skills/(architecture)/component-identification-sizing/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C225 | 3 | KEEP-POLICY | component-identification-sizing governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C226 | 3 | KEEP-POLICY | Blocks unapproved remote writes. The conflict-detector directory name does not state that ban. | high | Drop only the unrelated-tools phrase; keep the remote-write ban. |
| C227 | 2 | KEEP-ROUTING | conflict-detector listing does not show category path 00_skills/(tooling)/conflict-detector/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C228 | 3 | KEEP-POLICY | conflict-detector governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C229 | 3 | KEEP-ROUTING | Confluence trigger excludes Jira, general web search, and local file creation. | high | none |
| C230 | 2 | KEEP-ROUTING | confluence-assistant listing does not show category path 00_skills/(development)/confluence-assistant/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C231 | 3 | KEEP-POLICY | confluence-assistant governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C232 | 3 | KEEP-ROUTING | Content-to-revenue trigger list is selection policy. The quoted tail already leaves technical implementation. | high | none |
| C233 | 2 | KEEP-ROUTING | content-to-pipeline listing does not show category path 00_skills/(gtm)/content-to-pipeline/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C234 | 3 | KEEP-POLICY | content-to-pipeline governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C235 | 3 | KEEP-POLICY | Bans promoting unverified claims or transient task status into durable memory. | high | none |
| C236 | 2 | KEEP-ROUTING | context-router listing does not show category path 00_skills/(learning)/context-router/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C237 | 3 | KEEP-POLICY | context-router governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C238 | 3 | KEEP-POLICY | Bans inventing project state and promoting unverified claims into durable memory. | high | none |
| C239 | 2 | KEEP-ROUTING | continuity-bootstrapper listing does not show category path 00_skills/(learning)/continuity-bootstrapper/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C240 | 3 | KEEP-POLICY | continuity-bootstrapper governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C241 | 3 | KEEP-ROUTING | Routes LCP, INP, and CLS work away from perf-web-optimization, perf-lighthouse, and perf-astro. | high | none |
| C242 | 2 | KEEP-ROUTING | core-web-vitals listing does not show category path 00_skills/(performance)/core-web-vitals/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C243 | 3 | KEEP-POLICY | core-web-vitals governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C244 | 3 | KEEP-POLICY | Bans promoting unverified claims or transient status into durable memory. The cost-token folder name does not say that. | high | none |
| C245 | 2 | KEEP-ROUTING | cost-token-optimizer listing does not show category path 00_skills/(learning)/cost-token-optimizer/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C246 | 3 | KEEP-POLICY | cost-token-optimizer governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C247 | 3 | KEEP-ROUTING | Coupling trigger excludes domain-analysis and component-identification-sizing. | high | none |
| C248 | 2 | KEEP-ROUTING | coupling-analysis listing does not show category path 00_skills/(architecture)/coupling-analysis/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C249 | 3 | KEEP-POLICY | coupling-analysis governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C250 | 3 | KEEP-ROUTING | ADR trigger sends undecided choices to create-rfc and implementation planning to a design-doc skill. | high | none |
| C251 | 2 | KEEP-ROUTING | create-adr listing does not show category path 00_skills/(creation)/create-adr/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C252 | 3 | KEEP-POLICY | create-adr governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C253 | 3 | KEEP-ROUTING | RFC trigger excludes TDD or implementation docs and general documentation. | high | none |
| C254 | 2 | KEEP-ROUTING | create-rfc listing does not show category path 00_skills/(creation)/create-rfc/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C255 | 3 | KEEP-POLICY | create-rfc governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C256 | 3 | KEEP-ROUTING | TDD trigger excludes API docs and general docs under docs-writer. | high | none |
| C257 | 2 | KEEP-ROUTING | create-technical-design-doc listing does not show category path 00_skills/(creation)/create-technical-design-doc/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C258 | 3 | KEEP-POLICY | create-technical-design-doc governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C259 | 3 | KEEP-POLICY | States that the 20 critical-thinking lenses are skill specializations, not agent identities. | high | Drop only the stock unrelated-languages sentence; keep the no-agent-identity rule. |
| C260 | 2 | KEEP-ROUTING | critical-thinking-governor listing does not show category path 00_skills/(development)/critical-thinking-governor/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C261 | 3 | KEEP-POLICY | critical-thinking-governor governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C262 | 3 | KEEP-COMPRESSED | Pins C# 14 and .NET 10 and excludes F# and Visual Basic. No discovered manifest carries that pin. | high | none |
| C263 | 2 | KEEP-ROUTING | csharp-expert listing does not show category path 00_skills/(development)/csharp-expert/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C264 | 3 | KEEP-POLICY | csharp-expert governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C265 | 3 | KEEP-POLICY | Forbids spawning or registering another AEOS agent identity. | high | none |
| C266 | 2 | KEEP-ROUTING | cursor-subagent-creator listing does not show category path 00_skills/(creation)/cursor-subagent-creator/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C267 | 3 | KEEP-POLICY | cursor-subagent-creator governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C268 | 3 | KEEP-ROUTING | Advisory sync is not vuln-obsol-recon, cve-remediation, or eol-advisory-sync. | high | none |
| C269 | 2 | KEEP-ROUTING | cve-advisory-sync listing does not show category path 00_skills/(security)/cve-advisory-sync/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C270 | 3 | KEEP-POLICY | cve-advisory-sync governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C271 | 3 | KEEP-POLICY | Remediation must not publish or merge the resulting PR, and is not broad discovery or advisory ingestion. | medium | none |
| C272 | 2 | KEEP-ROUTING | cve-remediation listing does not show category path 00_skills/(security)/cve-remediation/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C273 | 3 | KEEP-POLICY | cve-remediation governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C274 | 3 | KEEP-CAVEAT | Warns that the retained dark-videos map is not a current inventory and does not authorize a run or a publish. | high | none |
| C275 | 2 | KEEP-ROUTING | dark-videos-knowledge-base listing does not show category path 00_skills/(development)/dark-videos-knowledge-base/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C276 | 3 | KEEP-POLICY | dark-videos-knowledge-base governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C277 | 3 | KEEP-COMPRESSED | Fixes a 24h mine, top-20 LAYA rank, template dispatch, and a red-team posting limit. Not a listing fact. | high | none |
| C278 | 2 | KEEP-ROUTING | dark-videos-pipeline-expert listing does not show category path 00_skills/(development)/dark-videos-pipeline-expert/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C279 | 3 | KEEP-POLICY | dark-videos-pipeline-expert governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C280 | 3 | KEEP-ROUTING | Database-planning trigger excludes unrelated implementation and deployment execution. | high | none |
| C281 | 2 | KEEP-ROUTING | database-architecture-planner listing does not show category path 00_skills/(architecture)/database-architecture-planner/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C282 | 3 | KEEP-POLICY | database-architecture-planner governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C283 | 3 | KEEP-ROUTING | Decomposition roadmap excludes domain-analysis and component-identification-sizing. | high | none |
| C284 | 2 | KEEP-ROUTING | decomposition-planning-roadmap listing does not show category path 00_skills/(architecture)/decomposition-planning-roadmap/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C285 | 3 | KEEP-POLICY | decomposition-planning-roadmap governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C286 | 3 | KEEP-POLICY | Blocks unapproved remote writes during delegation checks. | high | Drop only the unrelated-tools phrase; keep the remote-write ban. |
| C287 | 2 | KEEP-ROUTING | delegation-auditor listing does not show category path 00_skills/(tooling)/delegation-auditor/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C288 | 3 | KEEP-POLICY | delegation-auditor governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C289 | 3 | KEEP-COMPRESSED | Environment-specific demo contract names Docker, Xvfb, XFCE, an mp4, and click telemetry. | high | none |
| C290 | 2 | KEEP-ROUTING | demo listing does not show category path 00_skills/(web-automation)/demo/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C291 | 3 | KEEP-POLICY | demo governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C292 | 3 | KEEP-ROUTING | Dependency-analysis trigger is absent from the empty manifest command list. | high | Drop only the stock unrelated-languages sentence; keep the analysis purpose. |
| C293 | 2 | KEEP-ROUTING | dependency-analyzer listing does not show category path 00_skills/(development)/dependency-analyzer/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C294 | 3 | KEEP-POLICY | dependency-analyzer governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C295 | 3 | KEEP-ROUTING | Updater trigger requires minimal blast radius and evidence-backed compatibility, not a package script name. | high | Drop only the stock unrelated-languages sentence; keep the blast-radius rule. |
| C296 | 2 | KEEP-ROUTING | dependency-updater listing does not show category path 00_skills/(development)/dependency-updater/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C297 | 3 | KEEP-POLICY | dependency-updater governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C298 | 3 | KEEP-COMPRESSED | Names AIHealthResearch gates: branch promotion, Google OSV, CodeQL, Python security, and deploy validators. | high | Drop only the stock unrelated-languages sentence; keep the named gates. |
| C299 | 2 | KEEP-ROUTING | deploy-expert-unique listing does not show category path 00_skills/(development)/deploy-expert-unique/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C300 | 3 | KEEP-POLICY | deploy-expert-unique governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C301 | 3 | KEEP-ROUTING | Pipeline diagnosis trigger excludes unrelated features and unapproved production changes. | high | none |
| C302 | 2 | KEEP-ROUTING | deployment-pipeline-expert listing does not show category path 00_skills/(cloud)/deployment-pipeline-expert/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C303 | 3 | KEEP-POLICY | deployment-pipeline-expert governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C304 | 3 | KEEP-COMPRESSED | Packs recursive CI recovery, per-workflow guardians, merge readiness, and bundle handoff. | high | none |
| C305 | 2 | KEEP-ROUTING | devops-pipeline-engineering listing does not show category path 00_skills/(cloud)/devops-pipeline-engineering/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C306 | 3 | KEEP-POLICY | devops-pipeline-engineering governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C307 | 3 | KEEP-POLICY | Diff review is not deployment authorization and is not evidence for checks that did not run. | high | none |
| C308 | 2 | KEEP-ROUTING | diff-reviewer listing does not show category path 00_skills/(quality)/diff-reviewer/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C309 | 3 | KEEP-POLICY | diff-reviewer governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C310 | 3 | KEEP-POLICY | Devcontainer generation stays in a sandbox and is not an unapproved production change. | high | none |
| C311 | 2 | KEEP-ROUTING | docker-devcontainer-engineer listing does not show category path 00_skills/(cloud)/docker-devcontainer-engineer/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C312 | 3 | KEEP-POLICY | docker-devcontainer-engineer governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C313 | 3 | KEEP-ROUTING | Docs-writer trigger excludes code comments, inline JSDoc, and API reference generation. | high | none |
| C314 | 2 | KEEP-ROUTING | docs-writer listing does not show category path 00_skills/(development)/docs-writer/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C315 | 3 | KEEP-POLICY | docs-writer governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C316 | 3 | KEEP-POLICY | Documentation output is evidence-based and sandbox-scoped. The directory name does not state either limit. | high | Drop only the stock unrelated-languages sentence; keep the sandbox and evidence limits. |
| C317 | 2 | KEEP-ROUTING | documentation listing does not show category path 00_skills/(development)/documentation/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C318 | 3 | KEEP-POLICY | documentation governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C319 | 3 | KEEP-POLICY | 11-layer mapping must not mutate production or invent architecture without source evidence. | high | none |
| C320 | 2 | KEEP-ROUTING | documentation-11-layer-mapper listing does not show category path 00_skills/(mapping)/documentation-11-layer-mapper/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C321 | 3 | KEEP-POLICY | documentation-11-layer-mapper governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C322 | 3 | KEEP-POLICY | Documentation mapping must not mutate production or invent architecture without source evidence. | high | none |
| C323 | 2 | KEEP-ROUTING | documentation-mapper listing does not show category path 00_skills/(mapping)/documentation-mapper/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C324 | 3 | KEEP-POLICY | documentation-mapper governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C325 | 3 | KEEP-ROUTING | Domain-analysis trigger excludes domain-identification-grouping and coupling-analysis. | high | none |
| C326 | 2 | KEEP-ROUTING | domain-analysis listing does not show category path 00_skills/(architecture)/domain-analysis/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C327 | 3 | KEEP-POLICY | domain-analysis governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C328 | 3 | KEEP-ROUTING | Component-to-domain grouping excludes domain-analysis and coupling-analysis. | high | none |
| C329 | 2 | KEEP-ROUTING | domain-identification-grouping listing does not show category path 00_skills/(architecture)/domain-identification-grouping/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C330 | 3 | KEEP-POLICY | domain-identification-grouping governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C331 | 3 | KEEP-POLICY | Forbids restart, scale, or live mutation without an authorized operations task. | high | none |
| C332 | 2 | KEEP-ROUTING | dynatrace-observability-staff listing does not show category path 00_skills/(monitoring)/dynatrace-observability-staff/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C333 | 3 | KEEP-POLICY | dynatrace-observability-staff governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C334 | 3 | KEEP-POLICY | Repo intelligence must not mutate production or invent architecture without source evidence. | high | none |
| C335 | 2 | KEEP-ROUTING | enterprise-repo-intelligence listing does not show category path 00_skills/(mapping)/enterprise-repo-intelligence/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C336 | 3 | KEEP-POLICY | enterprise-repo-intelligence governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C337 | 3 | KEEP-POLICY | Limits the audit to authorized defensive scope and forbids exposing secret values. | high | none |
| C338 | 2 | KEEP-ROUTING | enterprise-security-auditor listing does not show category path 00_skills/(security)/enterprise-security-auditor/SKILL.md. Finding that bucket is a cross-tree read, so cost 2. | high | none |
| C339 | 3 | KEEP-POLICY | enterprise-security-auditor governance line is the single-agent identity rule. Inventory manifests are empty, so it is not a config echo. | high | none |
| C340 | 3 | KEEP-CAVEAT | Warns not to treat missing public EOL dates as support facts for internal libraries. Also not CVE sync or patching. | high | none |
| C341 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(security)/eol-advisory-sync/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C342 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C343 | 3 | KEEP-CAVEAT | Forbids using an unrun suite as deployment authorization or as evidence | medium | none |
| C344 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(quality)/evaluation-runner/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C345 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C346 | 3 | KEEP-COMPRESSED | Cache-key, invalidation, allowed-type and stale-risk checklist is not a directory listing | medium | none |
| C347 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/evidence-cache-auditor/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C348 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C349 | 3 | KEEP-COMPRESSED | Hash-chain and tamper-resistance contract is absent from inventory manifests | medium | none |
| C350 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/evidence-integrity-engineer/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C351 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C352 | 3 | KEEP-ROUTING | Full description redirects NestJS-only work to nestjs-modular-monolith and domain review to tactical-ddd | high | none |
| C353 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(architecture)/evolutionary-modular-architecture/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C354 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C355 | 3 | KEEP-ROUTING | Full description sends Mermaid to mermaid-studio and non-visual docs to docs-writer | high | none |
| C356 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(tooling)/excalidraw-studio/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C357 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C358 | 3 | KEEP-CAVEAT | Forbids using this GTM skill for implementation, code review, or software architecture | high | none |
| C359 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(gtm)/expansion-retention/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C360 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C361 | 3 | KEEP-COMPRESSED | Classify, done, evidence, decide, act, verify, report loop is process text | high | none |
| C362 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/fable/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C363 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C364 | 3 | KEEP-COMPRESSED | Wrapper-over-all-AEOS-skills scope is invocation policy, not a folder header | medium | none |
| C365 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/fable-aeos-harness/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C366 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C367 | 3 | KEEP-COMPRESSED | Adapter, flowchart, trap fixture and smoke eval outputs are not a listing | medium | none |
| C368 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/fable-domain/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C369 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C370 | 3 | KEEP-CAVEAT | Forbids treating verdicts as deployment authorization or as checks that were not run | medium | none |
| C371 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(quality)/fable-judge/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C372 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C373 | 3 | KEEP-COMPRESSED | Parallel lenses, one committed plan, then adversarial verification is process text | medium | none |
| C374 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/fable-loop/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C375 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C376 | 3 | KEEP-ROUTING | Pixel-perfect Figma implementation is redirected to figma-implement-design | high | none |
| C377 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(design)/figma/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C378 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C379 | 3 | KEEP-ROUTING | General Figma fetch and MCP troubleshooting are redirected to figma | high | none |
| C380 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(design)/figma-implement-design/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C381 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C382 | 3 | KEEP-COMPRESSED | Fine-tune only when justified, then a governed pipeline; not a manifest string | medium | none |
| C383 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/fine-tuning-expert/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C384 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C385 | 3 | KEEP-CAVEAT | Forbids using the validator as deployment authorization or as unrun checks | medium | none |
| C386 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(quality)/fixture-corpus-validator/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C387 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C388 | 3 | KEEP-CAVEAT | Forbids one-bug fixes, infra provision, production mutation, and invented business rules | high | none |
| C389 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(mapping)/fleet-mapping/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C390 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C391 | 3 | KEEP-CAVEAT | Full text forbids backend, API, database, and non-visual tasks | medium | none |
| C392 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(architecture)/frontend-blueprint/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C393 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C394 | 3 | KEEP-ROUTING | Design review and audit are redirected to web-design-guidelines or web-quality-audit | high | none |
| C395 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(design)/frontend-design/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C396 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C397 | 3 | KEEP-ROUTING | Fences PR creation and CI debugging off to gh-fix-ci; auth prompt is not a listing | high | none |
| C398 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/gh-address-comments/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C399 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C400 | 3 | KEEP-ROUTING | Review comments go to gh-address-comments; non-Actions providers such as Buildkite stay out of scope | high | none |
| C401 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(tooling)/gh-fix-ci/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C402 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C403 | 3 | KEEP-CAVEAT | Forbids cloning or replicating any identifiable real child | high | none |
| C404 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(tooling)/girl-voice-composer-simulation-expert/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C405 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C406 | 3 | KEEP-COMPRESSED | Runtime-only auth, immutable safety denials, and Work Bundle scope are policy text | medium | none |
| C407 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(tooling)/github-operations/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C408 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C409 | 3 | KEEP-CAVEAT | Forbids restart, scale, or live mutation without an authorized operations task | high | none |
| C410 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(monitoring)/grafana-observability-staff/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C411 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C412 | 3 | KEEP-CAVEAT | Full text forbids technical implementation, code review, and software architecture | high | none |
| C413 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(gtm)/gtm-engineering/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C414 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C415 | 3 | KEEP-CAVEAT | Full text forbids technical implementation, code review, and software architecture | high | none |
| C416 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(gtm)/gtm-metrics/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C417 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C418 | 3 | KEEP-CAVEAT | Forbids promoting unverified claims or transient status into durable memory | high | none |
| C419 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(learning)/handoff-manager/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C420 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C421 | 3 | KEEP-COMPRESSED | Q1, Q2-before-A, ADR exclusion from T2, and 11-mixed-apply.md are protocol, not a listing | high | none |
| C422 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/harness-eval/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C423 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C424 | 3 | KEEP-COMPRESSED | UI coverage list plus non-UI exclusion is not rediscoverable from the directory name | medium | none |
| C425 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(design)/impeccable/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C426 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C427 | 3 | KEEP-CAVEAT | Forbids restart, scale, or live mutation without an authorized operations task | high | none |
| C428 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(monitoring)/incident-commander/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C429 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C430 | 3 | KEEP-CAVEAT | Forbids restart, scale, or live mutation without an authorized operations task | high | none |
| C431 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(monitoring)/incident-response-assistant/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C432 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C433 | 3 | KEEP-COMPRESSED | Requires explicit Java 8-to-11 compatibility analysis, which the directory name does not state | medium | none |
| C434 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/java-11-expert/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C435 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C436 | 3 | KEEP-COMPRESSED | LTS migration-safety scope plus a production-deployment ban is not a manifest string | medium | none |
| C437 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/java-17-expert/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C438 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C439 | 3 | KEEP-COMPRESSED | LTS-aware verification requirement is process text; inventory manifests are empty | medium | none |
| C440 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/java-21-expert/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C441 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C442 | 3 | KEEP-COMPRESSED | Java 25 features must be verified for this repo toolchain and deployment runtime | high | none |
| C443 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/java-25-expert/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C444 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C445 | 3 | KEEP-COMPRESSED | Requires explicit current, preview, and incubator handling for Java 26 | high | none |
| C446 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/java-26-expert/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C447 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C448 | 3 | KEEP-CAVEAT | Forbids silently using APIs or language features introduced after Java 8 | high | none |
| C449 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/java-8-expert/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C450 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C451 | 3 | KEEP-COMPRESSED | Trace, root cause, fix, validate, and retain lessons is a workflow, not a header | medium | none |
| C452 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/java-bug-solver/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C453 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C454 | 3 | KEEP-COMPRESSED | Creates a Java bug-solver skill rather than only repairing one stack trace | medium | none |
| C455 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/java-bug-solver-skill/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C456 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C457 | 3 | KEEP-COMPRESSED | Java/Spring modernization analysis is scoped process text, not a layout echo | medium | none |
| C458 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/java-enterprise-modernizer/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C459 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C460 | 3 | KEEP-COMPRESSED | Version-correct APIs, minimal diffs, and evidence-backed verification are not a listing | medium | none |
| C461 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/java-expert/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C462 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C463 | 3 | KEEP-COMPRESSED | Migration scope includes API replacement and build-configuration updates | medium | none |
| C464 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/java-migration/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C465 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C466 | 3 | KEEP-ROUTING | Routes Java work to one verified JDK profile and skips unrelated version knowledge | high | none |
| C467 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/java-version-expert/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C468 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C469 | 3 | KEEP-COMPRESSED | Requires exact runtime, module-system, and browser compatibility | medium | none |
| C470 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/javascript-expert/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C471 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C472 | 3 | KEEP-CAVEAT | Forbids generic tool calling and direct execution of untrusted or unapproved actions | high | none |
| C473 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/jev-call-expert/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C474 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C475 | 3 | KEEP-ROUTING | Confluence page work is redirected to confluence-assistant | high | none |
| C476 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/jira-assistant/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C477 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C478 | 3 | KEEP-COMPRESSED | Requires traceability across requirement, code, evidence, and documentation | medium | none |
| C479 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/jira-confluence-assistant/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C480 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C481 | 3 | KEEP-CAVEAT | Time-entry proposals must come from actual task evidence | medium | none |
| C482 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(development)/jira-time-entry-assistant/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C483 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C484 | 3 | KEEP-CAVEAT | Forbids creating a Judge agent and forbids use as deployment authorization | high | none |
| C485 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(quality)/judge-benchmark-runner/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C486 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C487 | 3 | KEEP-COMPRESSED | Rollback-safe restore verification is the contract; not an inventory manifest string | medium | none |
| C488 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(cloud)/kinghost-backup-recovery-expert/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C489 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C490 | 3 | KEEP-CAVEAT | Forbids mutating the remote origin and forbids silently losing files | high | none |
| C491 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(cloud)/kinghost-clone-site-expert/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C492 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C493 | 3 | KEEP-COMPRESSED | Covers KingHost database create, access, backup, query, migration, and recovery | medium | none |
| C494 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(architecture)/kinghost-database-expert/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C495 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C496 | 3 | KEEP-COMPRESSED | Requires snapshot, rollback, and DNS or SSL propagation verification | medium | none |
| C497 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(cloud)/kinghost-domain-dns-ssl-expert/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C498 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C499 | 3 | KEEP-CAVEAT | Email, DNS, and MX work must not expose secrets | high | none |
| C500 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(cloud)/kinghost-email-expert/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C501 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C502 | 3 | KEEP-COMPRESSED | Super-skill map of panel, DNS, FTP clone, publish, data, and rollback-safe change | medium | none |
| C503 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(cloud)/kinghost-expert/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C504 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C505 | 3 | KEEP-COMPRESSED | Measurement-driven Varnish, PHP runtime, and PageSpeed scope is not a folder header | medium | none |
| C506 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(cloud)/kinghost-performance-expert/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C507 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C508 | 3 | KEEP-CAVEAT | Defensive scope only; forbids exposing secret values | high | none |
| C509 | 3 | KEEP-ROUTING | Load mandate for 00_skills/(security)/kinghost-security-expert/SKILL.md; category bucket is not in the .agents skill directory listing | high | none |
| C510 | 3 | KEEP-POLICY | Identity rule (codenavi-agent, no extra agent) is process policy; inventory manifests empty | high | none |
| C511 | 3 | KEEP-POLICY | Publish steps include approval and a ban on unapproved production changes; neither is in inventory manifests or the skill directory listing | medium | none |
| C512 | 2 | KEEP-ROUTING | Canonical 00_skills/(cloud)/kinghost-site-publish-ftp-expert/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/kinghost-site-publish-ftp-expert | high | none |
| C513 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/kinghost-site-publish-ftp-expert; it is process policy | high | none |
| C514 | 3 | KEEP-CAVEAT | Current-stable Kotlin and version-aware verification are not in any manifest; the slug does not state the deployment exclusion | high | none |
| C515 | 2 | KEEP-ROUTING | Canonical 00_skills/(development)/kotlin-expert/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/kotlin-expert | high | none |
| C516 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/kotlin-expert; it is process policy | high | none |
| C517 | 3 | KEEP-POLICY | Cluster-to-code mapping plus the unapproved-production ban is not a manifest string or a one-listing fact | medium | none |
| C518 | 2 | KEEP-ROUTING | Canonical 00_skills/(cloud)/kubernetes-code-context-mapper/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/kubernetes-code-context-mapper | high | none |
| C519 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/kubernetes-code-context-mapper; it is process policy | high | none |
| C520 | 3 | KEEP-POLICY | Ban on restart, scale, or live mutation is operations policy; no cluster manifest states it | high | none |
| C521 | 2 | KEEP-ROUTING | Canonical 00_skills/(monitoring)/kubernetes-observability-staff/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/kubernetes-observability-staff | high | none |
| C522 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/kubernetes-observability-staff; it is process policy | high | none |
| C523 | 3 | KEEP-CAVEAT | Enrichment trigger list and the exclusion of code review or architecture are absent from manifests and from the slug | high | none |
| C524 | 2 | KEEP-ROUTING | Canonical 00_skills/(gtm)/lead-enrichment/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/lead-enrichment | high | none |
| C525 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/lead-enrichment; it is process policy | high | none |
| C526 | 3 | KEEP-POLICY | Ban on promoting unverified or transient notes into .notebook/LEARNING.md is memory policy, not a file header | high | none |
| C527 | 2 | KEEP-ROUTING | Canonical 00_skills/(learning)/learning-curator/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/learning-curator | high | none |
| C528 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/learning-curator; it is process policy | high | none |
| C529 | 3 | KEEP-ROUTING | Handoff away from chromatic-mega-brain, skill-architect, create-adr, and the-fool is not in a directory listing | high | none |
| C530 | 2 | KEEP-ROUTING | Canonical 00_skills/(learning)/learning-opportunities/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/learning-opportunities | high | none |
| C531 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/learning-opportunities; it is process policy | high | none |
| C532 | 3 | KEEP-ROUTING | Handoff to domain-analysis, component-identification-sizing, and decomposition-planning-roadmap is cross-skill routing | high | none |
| C533 | 2 | KEEP-ROUTING | Canonical 00_skills/(architecture)/legacy-migration-planner/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/legacy-migration-planner | high | none |
| C534 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/legacy-migration-planner; it is process policy | high | none |
| C535 | 3 | KEEP-CAVEAT | Exclusion of implementation changes and deployment execution is not stated by the legacy-risk-mapper slug | medium | none |
| C536 | 2 | KEEP-ROUTING | Canonical 00_skills/(architecture)/legacy-risk-mapper/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/legacy-risk-mapper | high | none |
| C537 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/legacy-risk-mapper; it is process policy | high | none |
| C538 | 3 | KEEP-CAVEAT | Warning that temperature is not a quality knob is not in manifests or a file header | high | none |
| C539 | 2 | KEEP-ROUTING | Canonical 00_skills/(development)/llm-calibration-temperature-expert/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/llm-calibration-temperature-expert | high | none |
| C540 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/llm-calibration-temperature-expert; it is process policy | high | none |
| C541 | 3 | KEEP-CAVEAT | Requirement to use live capability sources plus project evals is process, not a manifest string | high | none |
| C542 | 2 | KEEP-ROUTING | Canonical 00_skills/(development)/llm-model-selection-expert/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/llm-model-selection-expert | high | none |
| C543 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/llm-model-selection-expert; it is process policy | high | none |
| C544 | 3 | KEEP-POLICY | Masked-only vault reads and the secret-exposure ban are absent from manifests | high | none |
| C545 | 2 | KEEP-ROUTING | Canonical 00_skills/(security)/local-secret-vault/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/local-secret-vault | high | none |
| C546 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/local-secret-vault; it is process policy | high | none |
| C547 | 3 | KEEP-CAVEAT | Open-weight fine-tune scope and the production-deployment exclusion are not in a toolchain manifest | medium | none |
| C548 | 2 | KEEP-ROUTING | Canonical 00_skills/(development)/lora-qlora-dora-expert/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/lora-qlora-dora-expert | high | none |
| C549 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/lora-qlora-dora-expert; it is process policy | high | none |
| C550 | 3 | KEEP-COMPRESSED | KB outputs architecture.md, entities, and vulnerabilities are process names, not repo files a listing shows | medium | none |
| C551 | 2 | KEEP-ROUTING | Canonical 00_skills/(security)/mantis-architecture/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/mantis-architecture | high | none |
| C552 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/mantis-architecture; it is process policy | high | none |
| C553 | 3 | KEEP-COMPRESSED | Appending final risk scores onto finding files is a stage method, not a manifest or listing | medium | none |
| C554 | 2 | KEEP-ROUTING | Canonical 00_skills/(security)/mantis-calibrate/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/mantis-calibrate | high | none |
| C555 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/mantis-calibrate; it is process policy | high | none |
| C556 | 3 | KEEP-COMPRESSED | Combining low-severity bugs into a higher-impact chain is a stage method, not recoverable from one listing | medium | none |
| C557 | 2 | KEEP-ROUTING | Canonical 00_skills/(security)/mantis-chain/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/mantis-chain | high | none |
| C558 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/mantis-chain; it is process policy | high | none |
| C559 | 3 | KEEP-CAVEAT | Production-viability filter with assertions disabled is an environment caveat, not a build-file header | high | none |
| C560 | 2 | KEEP-ROUTING | Canonical 00_skills/(security)/mantis-critic/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/mantis-critic | high | none |
| C561 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/mantis-critic; it is process policy | high | none |
| C562 | 3 | KEEP-ROUTING | Researcher-then-review consolidation order is a stage handoff, not a directory listing | medium | none |
| C563 | 2 | KEEP-ROUTING | Canonical 00_skills/(security)/mantis-dedupe/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/mantis-dedupe | high | none |
| C564 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/mantis-dedupe; it is process policy | high | none |
| C565 | 3 | KEEP-COMPRESSED | workspace/historical_learnings.jsonl is not a checked-in file; the VCS pre-step is process | high | none |
| C566 | 2 | KEEP-ROUTING | Canonical 00_skills/(security)/mantis-history/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/mantis-history | high | none |
| C567 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/mantis-history; it is process policy | high | none |
| C568 | 3 | KEEP-CAVEAT | Supervisor-only role versus running individual stages is a boundary, not a manifest | high | none |
| C569 | 2 | KEEP-ROUTING | Canonical 00_skills/(security)/mantis-meta-agent/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/mantis-meta-agent | high | none |
| C570 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/mantis-meta-agent; it is process policy | high | none |
| C571 | 3 | KEEP-COMPRESSED | Shadow-directory or file-backup patch isolation is not described by a listing | high | none |
| C572 | 2 | KEEP-ROUTING | Canonical 00_skills/(security)/mantis-patch/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/mantis-patch | high | none |
| C573 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/mantis-patch; it is process policy | high | none |
| C574 | 3 | KEEP-ROUTING | Custom orchestrator versus the default pipeline is a routing boundary, not a config string | medium | none |
| C575 | 2 | KEEP-ROUTING | Canonical 00_skills/(security)/mantis-pipeline-adapter/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/mantis-pipeline-adapter | high | none |
| C576 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/mantis-pipeline-adapter; it is process policy | high | none |
| C577 | 3 | KEEP-COMPRESSED | workspace/plan.json roadmap is not checked in; the planning boundary is process | high | none |
| C578 | 2 | KEEP-ROUTING | Canonical 00_skills/(security)/mantis-plan/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/mantis-plan | high | none |
| C579 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/mantis-plan; it is process policy | high | none |
| C580 | 3 | KEEP-COMPRESSED | workspace/learnings.jsonl extraction from trajectories is process, not a repo artifact | high | none |
| C581 | 2 | KEEP-ROUTING | Canonical 00_skills/(security)/mantis-reflect/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/mantis-reflect | high | none |
| C582 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/mantis-reflect; it is process policy | high | none |
| C583 | 3 | KEEP-ROUTING | End-of-cycle review packet versus auditing code is a stage handoff | medium | none |
| C584 | 2 | KEEP-ROUTING | Canonical 00_skills/(security)/mantis-report/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/mantis-report | high | none |
| C585 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/mantis-report; it is process policy | high | none |
| C586 | 3 | KEEP-CAVEAT | Crash-reproducer boundary versus auditing or patching is a stage caveat | high | none |
| C587 | 2 | KEEP-ROUTING | Canonical 00_skills/(security)/mantis-reproduce/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/mantis-reproduce | high | none |
| C588 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/mantis-reproduce; it is process policy | high | none |
| C589 | 3 | KEEP-COMPRESSED | Static review keyed off workspace/plan.json is process; that file is not in the repo | high | none |
| C590 | 2 | KEEP-ROUTING | Canonical 00_skills/(security)/mantis-researcher/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/mantis-researcher | high | none |
| C591 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/mantis-researcher; it is process policy | high | none |
| C592 | 3 | KEEP-CAVEAT | False-positive filter against source, distinct from reproduce or patch, is a stage caveat | high | none |
| C593 | 2 | KEEP-ROUTING | Canonical 00_skills/(security)/mantis-review/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/mantis-review | high | none |
| C594 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/mantis-review; it is process policy | high | none |
| C595 | 3 | KEEP-COMPRESSED | Content-addressed semantic-unit index is a named build step, not a listing | medium | none |
| C596 | 2 | KEEP-ROUTING | Canonical 00_skills/(security)/mantis-structural-index/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/mantis-structural-index | high | none |
| C597 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/mantis-structural-index; it is process policy | high | none |
| C598 | 3 | KEEP-COMPRESSED | Per-directory mantis-summary.md pre-pass is process; no such tree is checked in | high | none |
| C599 | 2 | KEEP-ROUTING | Canonical 00_skills/(security)/mantis-summarize/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/mantis-summarize | high | none |
| C600 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/mantis-summarize; it is process policy | high | none |
| C601 | 3 | KEEP-COMPRESSED | Stage B threat model from the KB, excluding source analysis and JSONL extraction, is a stage contract | medium | none |
| C602 | 2 | KEEP-ROUTING | Canonical 00_skills/(security)/mantis-threat-model/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/mantis-threat-model | high | none |
| C603 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/mantis-threat-model; it is process policy | high | none |
| C604 | 3 | KEEP-POLICY | Provenance and license curation plus the remote-write ban are policy, not a marketplace manifest | medium | none |
| C605 | 2 | KEEP-ROUTING | Canonical 00_skills/(tooling)/marketplace-curator/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/marketplace-curator | high | none |
| C606 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/marketplace-curator; it is process policy | high | none |
| C607 | 3 | KEEP-POLICY | Validate MCP tools against AEOS policies; inventory manifests do not state that gate | high | none |
| C608 | 2 | KEEP-ROUTING | Canonical 00_skills/(tooling)/mcp-discovery/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/mcp-discovery | high | none |
| C609 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/mcp-discovery; it is process policy | high | none |
| C610 | 3 | KEEP-POLICY | MCP runtime health check plus the remote-write ban is operational policy | medium | none |
| C611 | 2 | KEEP-ROUTING | Canonical 00_skills/(tooling)/mcp-health-check/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/mcp-health-check | high | none |
| C612 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/mcp-health-check; it is process policy | high | none |
| C613 | 3 | KEEP-POLICY | Injection and poisoning review stays inside defensive scope and must not expose secrets | high | none |
| C614 | 2 | KEEP-ROUTING | Canonical 00_skills/(security)/mcp-poisoning-evaluator/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/mcp-poisoning-evaluator | high | none |
| C615 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/mcp-poisoning-evaluator; it is process policy | high | none |
| C616 | 3 | KEEP-POLICY | MCP poisoning audit and the remote-write ban are policy, not a tool manifest | medium | none |
| C617 | 2 | KEEP-ROUTING | Canonical 00_skills/(tooling)/mcp-risk-controller/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/mcp-risk-controller | high | none |
| C618 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/mcp-risk-controller; it is process policy | high | none |
| C619 | 3 | KEEP-POLICY | .notebook/MEMORY.md curation forbids unverified or transient promotion; that is policy, not a file header | high | none |
| C620 | 2 | KEEP-ROUTING | Canonical 00_skills/(learning)/memory-curator/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/memory-curator | high | none |
| C621 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/memory-curator; it is process policy | high | none |
| C622 | 3 | KEEP-POLICY | Memory read and write audit for evidence, scope, and secret safety is policy | high | none |
| C623 | 2 | KEEP-ROUTING | Canonical 00_skills/(learning)/memory-governance-auditor/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/memory-governance-auditor | high | none |
| C624 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/memory-governance-auditor; it is process policy | high | none |
| C625 | 3 | KEEP-COMPRESSED | Dual-engine SVG, PNG, and ASCII plus the diagram-type set are not in a renderer manifest | medium | none |
| C626 | 2 | KEEP-ROUTING | Canonical 00_skills/(tooling)/mermaid-studio/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/mermaid-studio | high | none |
| C627 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/mermaid-studio; it is process policy | high | none |
| C628 | 3 | KEEP-COMPRESSED | Sequenced monolith pipeline steps are not stated by the skill directory name | high | none |
| C629 | 2 | KEEP-ROUTING | Canonical 00_skills/(architecture)/modular-decomposition/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/modular-decomposition | high | none |
| C630 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/modular-decomposition; it is process policy | high | none |
| C631 | 3 | KEEP-COMPRESSED | Bounded-context and contract checklist is guidance, not a module header in the repo | medium | none |
| C632 | 2 | KEEP-ROUTING | Canonical 00_skills/(architecture)/modular-design-principles/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/modular-design-principles | high | none |
| C633 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/modular-design-principles; it is process policy | high | none |
| C634 | 3 | KEEP-CAVEAT | Launch-channel triggers and the non-engineering exclusion are absent from manifests | medium | none |
| C635 | 2 | KEEP-ROUTING | Canonical 00_skills/(gtm)/multi-platform-launch/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/multi-platform-launch | high | none |
| C636 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/multi-platform-launch; it is process policy | high | none |
| C637 | 3 | KEEP-POLICY | Multi-repo mapping forbids production mutation and evidence-free architecture | high | none |
| C638 | 2 | KEEP-ROUTING | Canonical 00_skills/(mapping)/multirepo-ecosystem-mapper/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/multirepo-ecosystem-mapper | high | none |
| C639 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/multirepo-ecosystem-mapper; it is process policy | high | none |
| C640 | 3 | KEEP-CAVEAT | NestJS modular-monolith fence versus CRUD, frontend, and the sibling architecture skill is a scope caveat | medium | none |
| C641 | 2 | KEEP-ROUTING | Canonical 00_skills/(development)/nestjs-modular-monolith/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/nestjs-modular-monolith | high | none |
| C642 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/nestjs-modular-monolith; it is process policy | high | none |
| C643 | 3 | KEEP-ROUTING | Netlify CLI versus Vercel, Cloudflare, and Render skills is a host handoff; no netlify config contains the quote | high | none |
| C644 | 2 | KEEP-ROUTING | Canonical 00_skills/(cloud)/netlify-deploy/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/netlify-deploy | high | none |
| C645 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/netlify-deploy; it is process policy | high | none |
| C646 | 3 | KEEP-COMPRESSED | evidence-or-stop with only three interrupt reasons is an operator contract, not a listing | high | none |
| C647 | 2 | KEEP-ROUTING | Canonical 00_skills/(development)/not-your-babysitter/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/not-your-babysitter | high | none |
| C648 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/not-your-babysitter; it is process policy | high | none |
| C649 | 3 | KEEP-POLICY | Progressive .notebook notes forbid unverified promotion; that is policy | high | none |
| C650 | 2 | KEEP-ROUTING | Canonical 00_skills/(learning)/notebook-intelligence/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/notebook-intelligence | high | none |
| C651 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/notebook-intelligence; it is process policy | high | none |
| C652 | 3 | KEEP-CAVEAT | Nx Cloud prerequisite and the local-task exclusion are environment limits; no nx.json is in the repo | high | none |
| C653 | 2 | KEEP-ROUTING | Canonical 00_skills/(tooling)/nx-ci-monitor/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/nx-ci-monitor | high | none |
| C654 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/nx-ci-monitor; it is process policy | high | none |
| C655 | 3 | KEEP-ROUTING | Generator path prefers local plugins and defers tasks and workspace config to sibling skills | high | none |
| C656 | 2 | KEEP-ROUTING | Canonical 00_skills/(tooling)/nx-generate/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/nx-generate | high | none |
| C657 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/nx-generate; it is process policy | high | none |
| C658 | 3 | KEEP-ROUTING | run-many and affected execution defers generation and workspace config to sibling skills | high | none |
| C659 | 2 | KEEP-ROUTING | Canonical 00_skills/(tooling)/nx-run-tasks/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/nx-run-tasks | high | none |
| C660 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/nx-run-tasks; it is process policy | high | none |
| C661 | 3 | KEEP-ROUTING | Workspace configuration defers pure task runs and pure generation to sibling skills | high | none |
| C662 | 2 | KEEP-ROUTING | Canonical 00_skills/(tooling)/nx-workspace/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/nx-workspace | high | none |
| C663 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/nx-workspace; it is process policy | high | none |
| C664 | 3 | KEEP-POLICY | Observability design forbids unsupervised live restart, scale, or mutate | high | none |
| C665 | 2 | KEEP-ROUTING | Canonical 00_skills/(monitoring)/observability-architect/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/observability-architect | high | none |
| C666 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/observability-architect; it is process policy | high | none |
| C667 | 3 | KEEP-POLICY | Timeline and failure reporting forbids unsupervised live mutation | high | none |
| C668 | 2 | KEEP-ROUTING | Canonical 00_skills/(monitoring)/observability-reporter/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/observability-reporter | high | none |
| C669 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/observability-reporter; it is process policy | high | none |
| C670 | 3 | KEEP-POLICY | Root-cause integration forbids unsupervised live mutation | high | none |
| C671 | 2 | KEEP-ROUTING | Canonical 00_skills/(monitoring)/observability-root-cause-integrator/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/observability-root-cause-integrator | high | none |
| C672 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/observability-root-cause-integrator; it is process policy | high | none |
| C673 | 3 | KEEP-POLICY | OpenShift observability forbids unsupervised live mutation; no cluster config states it | high | none |
| C674 | 2 | KEEP-ROUTING | Canonical 00_skills/(monitoring)/openshift-observability-staff/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/openshift-observability-staff | high | none |
| C675 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/openshift-observability-staff; it is process policy | high | none |
| C676 | 3 | KEEP-POLICY | Pack quarantine, staging, and active trust audit plus the remote-write ban is policy | medium | none |
| C677 | 2 | KEEP-ROUTING | Canonical 00_skills/(tooling)/pack-marketplace-auditor/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/pack-marketplace-auditor | high | none |
| C678 | 3 | KEEP-POLICY | Single-agent identity codenavi-agent is not in inventory manifests or a listing of .agents/skills/pack-marketplace-auditor; it is process policy | high | none |
| C679 | 3 | KEEP-POLICY | Package quarantine and promotion checks forbid secret exposure; not a manifest string | high | none |
| C680 | 2 | KEEP-ROUTING | Canonical 00_skills/(security)/package-trust-engineer/SKILL.md is on disk, but its category bucket is not in a listing of .agents/skills/package-trust-engineer | high | none |
| C681 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/package-trust-engineer/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C682 | 3 | KEEP-POLICY | packaging directory name does not state the unapproved-remote-write ban; inventory manifests empty | medium | keep the remote-write ban |
| C683 | 2 | KEEP-ROUTING | 00_skills/(tooling)/packaging/SKILL.md is outside .agents/skills/packaging/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C684 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/packaging/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C685 | 3 | KEEP-ROUTING | paid-creative-ai listing does not include the ad-platform trigger list or the exclusion of code review and architecture | high | keep the trigger phrases and the non-code exclusion |
| C686 | 2 | KEEP-ROUTING | 00_skills/(gtm)/paid-creative-ai/SKILL.md is outside .agents/skills/paid-creative-ai/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C687 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/paid-creative-ai/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C688 | 3 | KEEP-POLICY | parallel-scheduler listing does not state dependency-graph scheduling, read/write sets, or the remote-write ban | medium | keep the read/write-set contract and the remote-write ban |
| C689 | 2 | KEEP-ROUTING | 00_skills/(tooling)/parallel-scheduler/SKILL.md is outside .agents/skills/parallel-scheduler/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C690 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/parallel-scheduler/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C691 | 3 | KEEP-ROUTING | partner-affiliate listing does not include PartnerStack, reseller, or revenue-share triggers, nor the non-code exclusion | high | keep the keyword triggers and the non-code exclusion |
| C692 | 2 | KEEP-ROUTING | 00_skills/(gtm)/partner-affiliate/SKILL.md is outside .agents/skills/partner-affiliate/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C693 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/partner-affiliate/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C694 | 3 | KEEP-CAVEAT | patch-planner listing does not state that proposals and rollback plans must not be applied | high | keep the do-not-apply boundary |
| C695 | 2 | KEEP-ROUTING | 00_skills/(development)/patch-planner/SKILL.md is outside .agents/skills/patch-planner/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C696 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/patch-planner/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C697 | 3 | KEEP-ROUTING | perf-astro listing does not state the non-Astro exclusion or that it must not be the only Lighthouse skill | high | keep the Astro-only and not-sole-Lighthouse boundaries |
| C698 | 2 | KEEP-ROUTING | 00_skills/(performance)/perf-astro/SKILL.md is outside .agents/skills/perf-astro/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C699 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/perf-astro/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C700 | 3 | KEEP-ROUTING | perf-lighthouse listing does not name the sibling exclusions core-web-vitals, perf-web-optimization, and perf-astro | high | keep the sibling-skill exclusions |
| C701 | 2 | KEEP-ROUTING | 00_skills/(performance)/perf-lighthouse/SKILL.md is outside .agents/skills/perf-lighthouse/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C702 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/perf-lighthouse/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C703 | 3 | KEEP-ROUTING | perf-web-optimization listing does not name the sibling exclusions core-web-vitals, perf-lighthouse, and perf-astro | high | keep the sibling-skill exclusions |
| C704 | 2 | KEEP-ROUTING | 00_skills/(performance)/perf-web-optimization/SKILL.md is outside .agents/skills/perf-web-optimization/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C705 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/perf-web-optimization/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C706 | 3 | KEEP-COMPRESSED | performance-optimizer hot-path list covering registry, evidence, LSP, and TypeScript runtime is not in inventory manifests or a single directory header | medium | keep the AEOS hot-path list and the no-unmeasured-optimization ban |
| C707 | 2 | KEEP-ROUTING | 00_skills/(performance)/performance-optimizer/SKILL.md is outside .agents/skills/performance-optimizer/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C708 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/performance-optimizer/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C709 | 3 | KEEP-COMPRESSED | performance-profiler targets covering hashing, package verification, and Judge runtime are not in inventory manifests or the skill directory name | medium | keep the Judge-runtime and package-verification scope |
| C710 | 2 | KEEP-ROUTING | 00_skills/(performance)/performance-profiler/SKILL.md is outside .agents/skills/performance-profiler/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C711 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/performance-profiler/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C712 | 3 | KEEP-ROUTING | playbook-factory-generator listing does not state the exclusion of one-off coding and human competency lists | medium | keep the competency-list and one-off-coding exclusions |
| C713 | 2 | KEEP-ROUTING | 00_skills/(creation)/playbook-factory-generator/SKILL.md is outside .agents/skills/playbook-factory-generator/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C714 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/playbook-factory-generator/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C715 | 3 | KEEP-POLICY | playbook-optimizer listing does not state safety and evidence-quality goals or the competency-list exclusion | medium | keep the safety and evidence-quality goals |
| C716 | 2 | KEEP-ROUTING | 00_skills/(creation)/playbook-optimizer/SKILL.md is outside .agents/skills/playbook-optimizer/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C717 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/playbook-optimizer/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C718 | 3 | KEEP-ROUTING | playwright-skill listing does not state script output under /tmp or the chrome-devtools exclusion | high | keep the chrome-devtools exclusion |
| C719 | 2 | KEEP-ROUTING | 00_skills/(web-automation)/playwright-skill/SKILL.md is outside .agents/skills/playwright-skill/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C720 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/playwright-skill/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C721 | 3 | KEEP-POLICY | policy-bypass-evaluator listing does not state the no-weaken-permissions rule or the secret-exposure ban | high | keep the no-weaken and no-secret-exposure limits |
| C722 | 2 | KEEP-ROUTING | 00_skills/(security)/policy-bypass-evaluator/SKILL.md is outside .agents/skills/policy-bypass-evaluator/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C723 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/policy-bypass-evaluator/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C724 | 3 | KEEP-POLICY | policy-hardening-auditor listing does not state fail-closed coverage or the secret-exposure ban | high | keep the fail-closed and secret-exposure limits |
| C725 | 2 | KEEP-ROUTING | 00_skills/(security)/policy-hardening-auditor/SKILL.md is outside .agents/skills/policy-hardening-auditor/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C726 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/policy-hardening-auditor/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C727 | 3 | KEEP-ROUTING | positioning-icp listing does not include ICP, PMF, or buyer-persona triggers, nor the non-code exclusion | high | keep the keyword triggers and the non-code exclusion |
| C728 | 2 | KEEP-ROUTING | 00_skills/(gtm)/positioning-icp/SKILL.md is outside .agents/skills/positioning-icp/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C729 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/positioning-icp/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C730 | 3 | KEEP-CAVEAT | pr-comment-resolver listing does not state that incorrect review feedback must not be obeyed blindly | high | keep the do-not-blindly-obey clause |
| C731 | 2 | KEEP-ROUTING | 00_skills/(development)/pr-comment-resolver/SKILL.md is outside .agents/skills/pr-comment-resolver/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C732 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/pr-comment-resolver/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C733 | 1 | REDUNDANT-GENERAL | .agents/skills/pr-reviewer/ listing already supplies the trigger; the quote is generic evidence-based review advice and inventory manifests is empty | medium | drop the description gloss |
| C734 | 2 | KEEP-ROUTING | 00_skills/(development)/pr-reviewer/SKILL.md is outside .agents/skills/pr-reviewer/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C735 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/pr-reviewer/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C736 | 1 | REDUNDANT-GENERAL | .agents/skills/pr-reviewer-advanced/ listing already supplies the trigger; severity-ranked review is generic advice, not a manifest string | medium | drop the description gloss |
| C737 | 2 | KEEP-ROUTING | 00_skills/(development)/pr-reviewer-advanced/SKILL.md is outside .agents/skills/pr-reviewer-advanced/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C738 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/pr-reviewer-advanced/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C739 | 3 | KEEP-POLICY | production-deployment-planner listing does not state the ban on unapproved production changes | medium | keep the unapproved-production-changes ban |
| C740 | 2 | KEEP-ROUTING | 00_skills/(cloud)/production-deployment-planner/SKILL.md is outside .agents/skills/production-deployment-planner/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C741 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/production-deployment-planner/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C742 | 3 | KEEP-POLICY | progress-tracker quote binds .notebook/PROGRESS.md and forbids promoting unverified claims into durable memory; that ban is not a directory name or inventory manifest | high | keep the PROGRESS.md role and the no-unverified-promotion ban |
| C743 | 2 | KEEP-ROUTING | 00_skills/(learning)/progress-tracker/SKILL.md is outside .agents/skills/progress-tracker/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C744 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/progress-tracker/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C745 | 3 | KEEP-POLICY | prompt-optimizer listing does not state the unapproved-remote-write ban | medium | keep the remote-write ban |
| C746 | 2 | KEEP-ROUTING | 00_skills/(tooling)/prompt-optimizer/SKILL.md is outside .agents/skills/prompt-optimizer/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C747 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/prompt-optimizer/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C748 | 1 | REDUNDANT-GENERAL | .agents/skills/python-ai-productionizer/ listing already matches the production-readiness gloss; no manifest carries this sentence | medium | drop the description gloss |
| C749 | 2 | KEEP-ROUTING | 00_skills/(development)/python-ai-productionizer/SKILL.md is outside .agents/skills/python-ai-productionizer/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C750 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/python-ai-productionizer/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C751 | 3 | KEEP-COMPRESSED | python-bug-solver-skill listing does not state the validate-fixes and store-lessons steps | medium | keep the validate-and-store-lessons contract |
| C752 | 2 | KEEP-ROUTING | 00_skills/(development)/python-bug-solver-skill/SKILL.md is outside .agents/skills/python-bug-solver-skill/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C753 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/python-bug-solver-skill/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C754 | 3 | KEEP-POLICY | python-expert quote allows Python but keeps AEOS kernel orchestration on Node/TypeScript; that split is not in inventory manifests | high | keep the Python-allowed and kernel-stays-Node constraint |
| C755 | 2 | KEEP-ROUTING | 00_skills/(development)/python-expert/SKILL.md is outside .agents/skills/python-expert/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C756 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/python-expert/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C757 | 3 | KEEP-POLICY | python-rag-audit listing does not state data-leakage or prompt-injection scope | medium | keep the leakage and prompt-injection scope |
| C758 | 2 | KEEP-ROUTING | 00_skills/(development)/python-rag-audit/SKILL.md is outside .agents/skills/python-rag-audit/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C759 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/python-rag-audit/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C760 | 3 | KEEP-CAVEAT | rag-expert listing does not state the measurable-grounding-quality bar | medium | keep the measurable-grounding bar |
| C761 | 2 | KEEP-ROUTING | 00_skills/(development)/rag-expert/SKILL.md is outside .agents/skills/rag-expert/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C762 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/rag-expert/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C763 | 3 | KEEP-ROUTING | rails-dev quote requires loading the skill before any Rails naming or design talk; that early-load rule is not the directory name | high | keep the load-before-any-Rails-thinking rule |
| C764 | 2 | KEEP-ROUTING | 00_skills/(development)/rails-dev/SKILL.md is outside .agents/skills/rails-dev/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C765 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/rails-dev/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C766 | 3 | KEEP-ROUTING | react-best-practices listing does not point performance work away from react-composition-patterns | high | keep the composition-patterns exclusion |
| C767 | 2 | KEEP-ROUTING | 00_skills/(quality)/react-best-practices/SKILL.md is outside .agents/skills/react-best-practices/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C768 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/react-best-practices/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C769 | 3 | KEEP-ROUTING | react-composition-patterns listing does not point API design away from react-best-practices | high | keep the performance-skill exclusion |
| C770 | 2 | KEEP-ROUTING | 00_skills/(architecture)/react-composition-patterns/SKILL.md is outside .agents/skills/react-composition-patterns/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C771 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/react-composition-patterns/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C772 | 3 | KEEP-CAVEAT | react-expert listing does not state that the repository React version and existing data-fetching conventions must be followed | medium | keep the use-the-repo-React-version constraint |
| C773 | 2 | KEEP-ROUTING | 00_skills/(development)/react-expert/SKILL.md is outside .agents/skills/react-expert/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C774 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/react-expert/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C775 | 3 | KEEP-ROUTING | react-native-expert listing does not state the Flutter, web-only React, and backend Node exclusions | high | keep the Flutter and web-React exclusions |
| C776 | 2 | KEEP-ROUTING | 00_skills/(development)/react-native-expert/SKILL.md is outside .agents/skills/react-native-expert/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C777 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/react-native-expert/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C778 | 3 | KEEP-POLICY | redaction-evaluator listing does not state the secret-leakage check or the defensive-scope limit | high | keep the leakage check and secret-exposure ban |
| C779 | 2 | KEEP-ROUTING | 00_skills/(security)/redaction-evaluator/SKILL.md is outside .agents/skills/redaction-evaluator/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C780 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/redaction-evaluator/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C781 | 3 | KEEP-CAVEAT | release-readiness-judge listing does not state that the skill is not deployment authorization and not evidence for checks that were not run | high | keep the not-authorization and not-unrun-evidence limits |
| C782 | 2 | KEEP-ROUTING | 00_skills/(quality)/release-readiness-judge/SKILL.md is outside .agents/skills/release-readiness-judge/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C783 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/release-readiness-judge/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C784 | 3 | KEEP-ROUTING | render-deploy listing does not state render.yaml blueprints or the Vercel, Netlify, and Cloudflare exclusions | high | keep the other-host exclusions |
| C785 | 2 | KEEP-ROUTING | 00_skills/(cloud)/render-deploy/SKILL.md is outside .agents/skills/render-deploy/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C786 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/render-deploy/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C787 | 3 | KEEP-POLICY | repo-scanner listing does not state the ban on production mutation or on inventing architecture without evidence | high | keep the no-mutate and no-invented-architecture limits |
| C788 | 2 | KEEP-ROUTING | 00_skills/(mapping)/repo-scanner/SKILL.md is outside .agents/skills/repo-scanner/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C789 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/repo-scanner/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C790 | 3 | KEEP-ROUTING | report-design quote uses Portuguese report phrases and excludes fleet-mapping and acta-aurea; those routes are not the directory name | high | keep the Portuguese triggers and the sibling exclusions |
| C791 | 2 | KEEP-ROUTING | 00_skills/(design)/report-design/SKILL.md is outside .agents/skills/report-design/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C792 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/report-design/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C793 | 3 | KEEP-CAVEAT | resolver-comentarios listing does not state that referenced code must be inspected and the correction verified | medium | keep the inspect-and-verify constraint |
| C794 | 2 | KEEP-ROUTING | 00_skills/(development)/resolver-comentarios/SKILL.md is outside .agents/skills/resolver-comentarios/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C795 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/resolver-comentarios/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C796 | 3 | KEEP-ROUTING | revisar-pr quote uses Portuguese review phrases and excludes revisar-seguranca-pr, unrequested remediation, posting a review, and merge | high | keep the security-review split and the no-merge limit |
| C797 | 2 | KEEP-ROUTING | 00_skills/(development)/revisar-pr/SKILL.md is outside .agents/skills/revisar-pr/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C798 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/revisar-pr/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C799 | 3 | KEEP-ROUTING | revisar-seguranca-pr quote uses Portuguese security-review phrases and excludes revisar-pr and cve-remediation | high | keep the general-review and CVE-remediation exclusions |
| C800 | 2 | KEEP-ROUTING | 00_skills/(security)/revisar-seguranca-pr/SKILL.md is outside .agents/skills/revisar-seguranca-pr/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C801 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/revisar-seguranca-pr/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C802 | 3 | KEEP-POLICY | risk-classifier listing does not state the secret-exposure ban | high | keep the secret-exposure ban |
| C803 | 2 | KEEP-ROUTING | 00_skills/(security)/risk-classifier/SKILL.md is outside .agents/skills/risk-classifier/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C804 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/risk-classifier/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C805 | 3 | KEEP-POLICY | rollback-planner listing does not state the ban on unapproved production changes | medium | keep the unapproved-production-changes ban |
| C806 | 2 | KEEP-ROUTING | 00_skills/(cloud)/rollback-planner/SKILL.md is outside .agents/skills/rollback-planner/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C807 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/rollback-planner/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C808 | 3 | KEEP-POLICY | runtime-troubleshooting quote requires read-only diagnosis and forbids restart, scale, deploy, and invented broker state | high | keep the read-only and no-live-mutation limits |
| C809 | 2 | KEEP-ROUTING | 00_skills/(development)/runtime-troubleshooting/SKILL.md is outside .agents/skills/runtime-troubleshooting/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C810 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/runtime-troubleshooting/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C811 | 1 | REDUNDANT-GENERAL | .agents/skills/rust-expert/ listing already supplies the trigger; version-correct APIs and minimal diffs are generic practice, not a manifest string | medium | drop the description gloss |
| C812 | 2 | KEEP-ROUTING | 00_skills/(development)/rust-expert/SKILL.md is outside .agents/skills/rust-expert/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C813 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/rust-expert/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C814 | 3 | KEEP-ROUTING | sales-motion-design listing does not include PLG, TTFV, or freemium triggers, nor the non-code exclusion | high | keep the keyword triggers and the non-code exclusion |
| C815 | 2 | KEEP-ROUTING | 00_skills/(gtm)/sales-motion-design/SKILL.md is outside .agents/skills/sales-motion-design/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C816 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/sales-motion-design/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C817 | 3 | KEEP-POLICY | secret-redaction-specialist listing does not state the raw-value exposure ban | high | keep the no-raw-value-exposure limit |
| C818 | 2 | KEEP-ROUTING | 00_skills/(security)/secret-redaction-specialist/SKILL.md is outside .agents/skills/secret-redaction-specialist/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C819 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/secret-redaction-specialist/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C820 | 3 | KEEP-POLICY | security-audit listing does not state the secret-value exposure ban | high | keep the no-secret-exposure limit |
| C821 | 2 | KEEP-ROUTING | 00_skills/(security)/security-audit/SKILL.md is outside .agents/skills/security-audit/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C822 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/security-audit/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C823 | 3 | KEEP-ROUTING | security-best-practices quote names the inspected language set and excludes revisar-seguranca-pr, CVE/EOL recon, and threat modeling | high | keep the sibling exclusions |
| C824 | 2 | KEEP-ROUTING | 00_skills/(security)/security-best-practices/SKILL.md is outside .agents/skills/security-best-practices/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C825 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/security-best-practices/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C826 | 3 | KEEP-ROUTING | security-ownership-map listing does not exclude threat modeling via security-threat-model | high | keep the threat-model exclusion |
| C827 | 2 | KEEP-ROUTING | 00_skills/(security)/security-ownership-map/SKILL.md is outside .agents/skills/security-ownership-map/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C828 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/security-ownership-map/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C829 | 3 | KEEP-ROUTING | security-threat-model listing does not exclude architecture summaries, security-best-practices reviews, or ownership maps | high | keep the sibling exclusions |
| C830 | 2 | KEEP-ROUTING | 00_skills/(security)/security-threat-model/SKILL.md is outside .agents/skills/security-threat-model/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C831 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/security-threat-model/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C832 | 3 | KEEP-CAVEAT | sentry quote requires env var SENTRY_AUTH_TOKEN and read-only API use; that requirement is not a directory listing or inventory manifest | high | keep the token requirement and the non-SDK exclusion |
| C833 | 2 | KEEP-ROUTING | 00_skills/(monitoring)/sentry/SKILL.md is outside .agents/skills/sentry/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C834 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/sentry/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C835 | 3 | KEEP-ROUTING | seo listing does not name web-accessibility, core-web-vitals, or web-quality-audit as the other skills | high | keep the sibling-skill exclusions |
| C836 | 2 | KEEP-ROUTING | 00_skills/(quality)/seo/SKILL.md is outside .agents/skills/seo/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C837 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/seo/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C838 | 3 | KEEP-POLICY | servicenow-incident-assistant listing does not state the ban on restarting, scaling, or mutating live systems | high | keep the no-live-mutation limit |
| C839 | 2 | KEEP-ROUTING | 00_skills/(monitoring)/servicenow-incident-assistant/SKILL.md is outside .agents/skills/servicenow-incident-assistant/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C840 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/servicenow-incident-assistant/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C841 | 3 | KEEP-ROUTING | shopify-developer quote pins API v2026-01 and excludes non-Shopify platforms; neither is the directory name | high | keep the API version pin and the non-Shopify exclusion |
| C842 | 2 | KEEP-ROUTING | 00_skills/(development)/shopify-developer/SKILL.md is outside .agents/skills/shopify-developer/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C843 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/shopify-developer/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C844 | 3 | UNCLEAR | simulator-ai quote demands 4 agents and a diabetes-cure search, which no listing or inventory manifest states, but the sentence is garbled | low | do not drop as redundant; review the 4-agent wording separately |
| C845 | 2 | KEEP-ROUTING | 00_skills/(development)/simulator-ai/SKILL.md is outside .agents/skills/simulator-ai/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C846 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/simulator-ai/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C847 | 3 | KEEP-ROUTING | skill-architect quote routes finished-work skill decisions to learning-opportunities and forbids new agent identities | high | keep the learning-opportunities split and the no-new-agent-identity ban |
| C848 | 2 | KEEP-ROUTING | 00_skills/(creation)/skill-architect/SKILL.md is outside .agents/skills/skill-architect/ and inventory manifests is empty, so the follow line is not a one-listing echo | medium | keep the one-line follow pointer |
| C849 | 3 | KEEP-POLICY | inventory manifests empty; listing .agents/skills/skill-architect/ does not state the single-agent prohibition | high | keep the one-line identity bind |
| C850 | 3 | KEEP-POLICY | skill-factory quote caps the entrypoint at 100 lines and forbids new agent identities; neither is a directory name or inventory manifest | high | keep the 100-line cap and the no-new-agent-identity ban |
| C851 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(creation)/skill-factory/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C852 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C853 | 3 | KEEP-ROUTING | Purpose plus exclusions (one-off coding, human competency lists) are routing text, not a manifest or directory-header fact. | high | keep |
| C854 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(creation)/skill-factory-generator/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C855 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C856 | 3 | KEEP-ROUTING | Hardening via contracts, forbidden actions, and quality gates is a routing contract, not recoverable from a listing. | high | keep |
| C857 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(creation)/skill-hardener/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C858 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C859 | 3 | KEEP-ROUTING | SLO/error-budget use and the ban on unmeasured optimization are routing scope, absent from manifests and source headers. | high | keep |
| C860 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(performance)/slo-risk-analyzer/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C861 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C862 | 3 | KEEP-CAVEAT | Browser-session auth versus OAuth or developer keys is a misroute caveat, not stated by a manifest or one file header. | high | keep |
| C863 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(tooling)/social-media-operator/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C864 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C865 | 3 | KEEP-ROUTING | Social-selling trigger lexicon and the technical-implementation exclusion are not in manifests, listings, or non-harness headers. | high | keep |
| C866 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(gtm)/social-selling/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C867 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C868 | 3 | KEEP-ROUTING | Solo-founder GTM triggers, including agent-team design, are routing lexicon with no manifest or listing echo. | high | keep |
| C869 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(gtm)/solo-founder-gtm/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C870 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C871 | 3 | KEEP-POLICY | Fix-without-architecture-change and the production-deployment exclusion are process limits, not a code or config string. | medium | keep |
| C872 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(development)/solve-problems/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C873 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C874 | 3 | KEEP-COMPRESSED | spec-driven 4.0.0 phases, EARS, proof commands, mutation checks, and screen capture are a compressed method, not a manifest. | high | keep |
| C875 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(development)/spec-driven/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C876 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C877 | 3 | KEEP-ROUTING | Explicit-name-only invoke and the no-auto-trigger gate are routing policy, not implied by the directory name. | high | keep |
| C878 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(development)/spec-driven-eval/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C879 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C880 | 3 | KEEP-COMPRESSED | spec-lean 2.0.0 obligation freeze plus mutation and screen proof is a compressed method, not a listing or config string. | high | keep |
| C881 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(development)/spec-driven-lean/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C882 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C883 | 3 | KEEP-POLICY | Spec-before-implementation and do-not-override-approved-requirements are process policy, not in manifests or source. | high | keep |
| C884 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(development)/specs/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C885 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C886 | 3 | KEEP-POLICY | Ban on restarting, scaling, or mutating live Splunk systems without an authorized ops task is operational policy. | high | keep |
| C887 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(monitoring)/splunk-observability-staff/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C888 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C889 | 3 | KEEP-ROUTING | Architecture selection versus implementation or deployment execution is a routing boundary, not a file-header fact. | high | keep |
| C890 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(architecture)/staff-iii-architecture-governor/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C891 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C892 | 3 | KEEP-ROUTING | TDD-by-default against an architecture plan, and the deployment exclusion, are routing scope absent from manifests. | high | keep |
| C893 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(development)/staff-tdd-code-builder/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C894 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C895 | 3 | KEEP-ROUTING | Disambiguates this lens designer from skill-architect, cursor-subagent-creator, and spawning agent identities. | high | keep |
| C896 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(creation)/subagent-creator/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C897 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C898 | 3 | KEEP-POLICY | Defensive-scope limit and the ban on exposing secret values are security policy, not a manifest string. | high | keep |
| C899 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(security)/supply-chain-auditor/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C900 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C901 | 3 | KEEP-ROUTING | DDD trigger lexicon (anemic model, aggregate, value object, domain event) is not recoverable from one listing or header. | high | keep |
| C902 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(architecture)/tactical-ddd/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C903 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C904 | 3 | KEEP-ROUTING | Playbook-to-task-graph use and the unapproved-remote-write exclusion are routing rules, not config or layout. | high | keep |
| C905 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(tooling)/task-graph-builder/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C906 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C907 | 3 | KEEP-ROUTING | Design-doc triggers and the handoff of README/API/general docs to docs-writer are routing, not a manifest echo. | high | keep |
| C908 | 3 | KEEP-ROUTING | Stub name technical-design-doc-creator does not match canonical create-technical-design-doc. Follow-mandate is routing, not a same-name listing. | high | keep |
| C909 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C910 | 3 | KEEP-POLICY | Telemetry root-cause work must not restart, scale, or mutate live systems without authorization; that is operational policy. | high | keep |
| C911 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(monitoring)/telemetry-bug-root-cause-solver/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C912 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C913 | 3 | KEEP-POLICY | Test-gap output is not deployment authorization or evidence of checks that were not executed; that gate is policy. | high | keep |
| C914 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(quality)/test-gap-analyzer/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C915 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C916 | 3 | KEEP-POLICY | Sandbox test proposals are not deployment authorization or proof of unrun checks; that limit is process policy. | high | keep |
| C917 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(quality)/test-generation/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C918 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C919 | 3 | KEEP-POLICY | A test-strategy document is not deploy authorization or proof of unexecuted checks; that limit is process policy. | high | keep |
| C920 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(quality)/test-strategy-architect/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C921 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C922 | 3 | KEEP-POLICY | Never writing real test directories, and not standing in for unrun checks or deploy approval, is a write/authority policy. | high | keep |
| C923 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(quality)/test-writer/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C924 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C925 | 3 | KEEP-ROUTING | Functional and e2e triggers, including Portuguese phrases, plus the unit-test exclusion, are routing not shown by a listing. | high | keep |
| C926 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(quality)/tests-expert/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C927 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C928 | 3 | KEEP-ROUTING | Pre-mortem use versus deciding, implementing, or harvesting lessons (learning-opportunities) is a routing boundary. | high | keep |
| C929 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(decision-making)/the-fool/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C930 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C931 | 3 | KEEP-COMPRESSED | PR-judge sequence (repo checks, current official docs, noise gate, one gh review) is compressed procedure, not a manifest. | high | keep |
| C932 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(quality)/the-judge/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C933 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C934 | 3 | KEEP-COMPRESSED | Three-or-five lens tally with dissent, plus the no-spawn and not-the-fool limits, is a compressed decision protocol. | medium | keep |
| C935 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(decision-making)/the-jury/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C936 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C937 | 3 | KEEP-POLICY | Threat modeling stays in defensive scope and must not expose secrets; that constraint is security policy. | high | keep |
| C938 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(security)/threat-modeler/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C939 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C940 | 3 | KEEP-ROUTING | Discovery-to-design-doc use, and the ban on cutting tasks or implementing, is routing absent from manifests. | high | keep |
| C941 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(development)/tlc-discover/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C942 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C943 | 3 | KEEP-ROUTING | GEO/answer-engine triggers (citability, llms.txt, AI Overviews) are routing lexicon, not a repo manifest or header. | high | keep |
| C944 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(quality)/tlc-generative-engine-optimization/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C945 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C946 | 3 | KEEP-ROUTING | Implement-an-already-planned-checklist versus designing the work is a routing boundary, not a listing fact. | high | keep |
| C947 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(development)/tlc-implement/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C948 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C949 | 3 | KEEP-ROUTING | tlc-plan turns a decided PRD into tasks and excludes discovery and implementation; that split is routing. | high | keep |
| C950 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(development)/tlc-plan/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C951 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C952 | 3 | KEEP-ROUTING | PRD interview that stops before technical design is a routing boundary, not stated by config or a file header. | high | keep |
| C953 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(development)/tlc-prd/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C954 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C955 | 3 | KEEP-COMPRESSED | tlc-spec-driven 4.0.0 Specify/Design/Tasks/Execute contract with EARS and screen checks is compressed method. | high | keep |
| C956 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(development)/tlc-spec-driven/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C957 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C958 | 3 | KEEP-COMPRESSED | tlc-spec-lean 2.0.0 obligation-and-proof contract is compressed method, not a manifest or directory listing. | high | keep |
| C959 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(development)/tlc-spec-lean/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C960 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C961 | 3 | KEEP-POLICY | Ban on promoting unverified claims or transient status into durable memory is memory policy, not a config string. | high | keep |
| C962 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(learning)/token-budget-governor/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C963 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C964 | 3 | KEEP-ROUTING | Audit that Tool Router covers every external action is a routing/policy trigger, not echoed by a manifest. | high | keep |
| C965 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(tooling)/tool-router-audit/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C966 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C967 | 3 | KEEP-COMPRESSED | TypeSafe System One / Jev typed-judgment model is compressed product procedure, not a manifest or listing. | medium | keep |
| C968 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(development)/typesafe-ai/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C969 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C970 | 3 | KEEP-ROUTING | Environment-inventory conflict audit versus language or deployment work is routing scope, not a header fact. | high | keep |
| C971 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(development)/unique-environment-auditor/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C972 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C973 | 3 | KEEP-ROUTING | Sandbox-first multi-stack project generation, excluding one-off coding and competency lists, is routing. | high | keep |
| C974 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(creation)/universal-project-factory/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C975 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C976 | 3 | KEEP-POLICY | v1 readiness output is not deployment authorization or evidence of checks that were not executed; that gate is policy. | high | keep |
| C977 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(quality)/v1-readiness-auditor/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C978 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C979 | 3 | KEEP-ROUTING | Vercel deploy triggers and the negative route to Netlify, Cloudflare, and Render skills are not in manifests. | high | keep |
| C980 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(cloud)/vercel-deploy/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C981 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C982 | 3 | KEEP-ROUTING | Video-outreach trigger lexicon (Tavus, Sendspark, HeyGen) and the non-technical exclusion are not listing facts. | high | keep |
| C983 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(gtm)/video-outreach/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C984 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C985 | 3 | KEEP-POLICY | Activating voiceai as current-session consent to record or transcribe authorized audio is consent policy, not config. | high | keep |
| C986 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(tooling)/voiceai/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C987 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C988 | 3 | KEEP-CAVEAT | Bare-audio Whisper versus meeting video (acta-aurea), diarization, dictation, or cloning is a misroute caveat. | high | keep |
| C989 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(tooling)/vox-aurum/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C990 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C991 | 3 | KEEP-CAVEAT | Do not invent versions or substitute this recon for patching, base sync, or deep PR review; that is a scope caveat. | high | keep |
| C992 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(security)/vuln-obsol-recon/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C993 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C994 | 3 | KEEP-ROUTING | WCAG audit triggers and the negative route to seo, core-web-vitals, and web-quality-audit are routing, not manifests. | high | keep |
| C995 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(quality)/web-accessibility/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C996 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C997 | 3 | KEEP-ROUTING | Security, compatibility, and code-quality checks, excluding primary a11y/SEO/full-audit ownership, are routing. | high | keep |
| C998 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(quality)/web-best-practices/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C999 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C1000 | 3 | KEEP-ROUTING | Visual and interaction review, with negative routes to core-web-vitals, seo, and web-quality-audit, is routing. | high | keep |
| C1001 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(design)/web-design-guidelines/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C1002 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C1003 | 3 | KEEP-ROUTING | Multi-area web audit versus single-area skills (core-web-vitals, ai-seo, best-practices, perf-lighthouse) is routing. | high | keep |
| C1004 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(quality)/web-quality-audit/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C1005 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C1006 | 3 | KEEP-ROUTING | Synthetic WhatsApp fixtures versus live or unapproved remote writes is a routing boundary, not a manifest string. | high | keep |
| C1007 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(tooling)/whatsapp-simulator/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C1008 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C1009 | 3 | KEEP-ROUTING | WordPress scope (plugins, governed wp-admin, production-safe edits) is routing, not a package manifest or listing. | high | keep |
| C1010 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(development)/wordpress-expert/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C1011 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| C1012 | 3 | KEEP-ROUTING | Smallest workbench profile from scope, capabilities, and constraints is routing, not a config or header echo. | high | keep |
| C1013 | 3 | KEEP-ROUTING | Follow-mandate for 00_skills/(tooling)/workbench-profile-resolver/SKILL.md is routing policy. The file is on disk; no manifest or non-harness source states it. | high | keep |
| C1014 | 3 | KEEP-POLICY | Single-identity rule for codenavi-agent is process policy. Not an exact string in package manifests or non-harness source. | high | keep |
| P003 | 1 | REDUNDANT-GENERAL | Generic naming advice. Exact sentence is not a manifest, config, or file header; workflow-tips is not on disk. | high | cut; generic advice with no repo signal |
| P004 | 1 | REDUNDANT-GENERAL | Generic layering slogan. Not an exact manifest string and not shown by one listing or file header. | high | cut; generic advice with no repo signal |
| P005 | 3 | KEEP-POLICY | Secrets policy. Exact sentence is absent from manifests and from live AGENTS.md; shorter deploy notes are still harness text. | high | keep |
| P006 | 3 | KEEP-CAVEAT | Local-pass versus missing CI secrets is an environment caveat, not an exact workflow or script string. | high | keep |
