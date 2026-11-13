# Harness Eval: Usefulness Agreement (Track C)

> Run dir: `/agent/repos/ai-assistent-universal-coder/.harness-eval/runs/2026-11-13-full`
> Trap gate: PASS (misses=0)
> Fan-in gate: PASS (slim-fanin-blocked=0)
> Judges: J1 model=`grok-4.7` · J2 model=`grok-4.7`
> Bands: Slim = dual SLIM/ROUTING + trap PASS + fan-in PASS; Keep-core = dual KEEP-CORE; Mixed = dual MIXED; Hold = disagree / unclear / missing / slim-fanin-blocked
> **Model-sensitive:** re-judge on a second model before large Slim deletes.
> **Fan-in:** another harness surface hard-loads this path as SoT → Hold, not Slim.
> **Mixed apply:** use `11-mixed-apply.md` only — do not re-judge from this table alone.

## What these words mean

| Word | Meaning | You should |
|------|---------|------------|
| **Keep-core** | Most of the file changes agent behavior | Do **not** slim |
| **Mixed** | Real rules + large theory/examples/overlap | Keep rules; cut bulk — follow `11-mixed-apply.md` |
| **Slim** | Mostly theory / repo-demo / overlap, **and** no other harness surface hard-loads it | Compress or delete body |
| **Hold** | Judges disagreed, unclear, or Slim blocked by fan-in | Do nothing yet (or update consumers first) |
| **Trap PASS** | Planted traps scored correctly | Necessary but not sufficient for Slim |
| **Fan-in blocked** | Another harness file mandates loading this path / treats it as SoT | Do **not** stub/delete until consumers are updated |

This track answers: *does deleting this change agent behavior?* Not the same as redundancy (`07-agreement.md`).

## Executive summary

- Real surfaces scored: 309
- Slim: **308**
- Keep-core: **1**
- Mixed: **0** → apply plan: `11-mixed-apply.md`
- Hold: **0** (fan-in blocked: 0)
- Trap misses: none

## Discrimination (plants)

| ID | Expected family | J2 family |
|----|-----------------|-----------|
| S901 | SLIM | SLIM |
| S902 | SLIM | SLIM |
| S903 | KEEP-CORE | KEEP-CORE |

Slim by tier: {'T1': 308}
Keep-core by tier: {'T0': 1}
Mixed by tier: {}
Hold by tier: {}

## Slim (compress / delete body candidates)

| ID | Tier | Name | Path | J1 | J2 |
|----|------|------|------|----|----|
| S002 | T1 | accessibility | `.agents/skills/accessibility/SKILL.md` | SLIM | ROUTING-ONLY |
| S003 | T1 | acta-aurea | `.agents/skills/acta-aurea/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S004 | T1 | adr-decision-writer | `.agents/skills/adr-decision-writer/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S005 | T1 | agent-trace-validator | `.agents/skills/agent-trace-validator/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S006 | T1 | ai-architecture-expert | `.agents/skills/ai-architecture-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S007 | T1 | ai-cold-outreach | `.agents/skills/ai-cold-outreach/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S008 | T1 | ai-continuous-training-maintainer | `.agents/skills/ai-continuous-training-maintainer/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S009 | T1 | ai-engineering-expert | `.agents/skills/ai-engineering-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S010 | T1 | ai-evals-expert | `.agents/skills/ai-evals-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S011 | T1 | ai-pricing | `.agents/skills/ai-pricing/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S012 | T1 | ai-project-bootstrapper | `.agents/skills/ai-project-bootstrapper/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S013 | T1 | ai-sdr | `.agents/skills/ai-sdr/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S014 | T1 | ai-seo | `.agents/skills/ai-seo/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S015 | T1 | ai-ugc-ads | `.agents/skills/ai-ugc-ads/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S016 | T1 | angular-20-expert | `.agents/skills/angular-20-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S017 | T1 | angular-8-to-20-migration | `.agents/skills/angular-8-to-20-migration/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S018 | T1 | anti-hallucination-evaluator | `.agents/skills/anti-hallucination-evaluator/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S019 | T1 | approval-governance-auditor | `.agents/skills/approval-governance-auditor/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S020 | T1 | approval-requester | `.agents/skills/approval-requester/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S021 | T1 | architecturally-significant-requirement | `.agents/skills/architecturally-significant-requirement/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S022 | T1 | architecture-decision-log | `.agents/skills/architecture-decision-log/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S023 | T1 | architecture-decision-record | `.agents/skills/architecture-decision-record/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S024 | T1 | architecture-knowledge-management | `.agents/skills/architecture-knowledge-management/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S025 | T1 | architecture-mapper | `.agents/skills/architecture-mapper/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S026 | T1 | atualizar-dependencias | `.agents/skills/atualizar-dependencias/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S027 | T1 | automation-orchestrator | `.agents/skills/automation-orchestrator/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S028 | T1 | aws-advisor | `.agents/skills/aws-advisor/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S029 | T1 | best-practices | `.agents/skills/best-practices/SKILL.md` | SLIM | ROUTING-ONLY |
| S030 | T1 | blueprint-generator | `.agents/skills/blueprint-generator/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S031 | T1 | bm25-expert | `.agents/skills/bm25-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S032 | T1 | camel-banking-expert | `.agents/skills/camel-banking-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S033 | T1 | change-trace-auditor | `.agents/skills/change-trace-auditor/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S034 | T1 | chromatic-mega-brain | `.agents/skills/chromatic-mega-brain/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S035 | T1 | chrome-devtools | `.agents/skills/chrome-devtools/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S036 | T1 | ci-quality-gate-engineer | `.agents/skills/ci-quality-gate-engineer/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S037 | T1 | cloudflare-deploy | `.agents/skills/cloudflare-deploy/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S038 | T1 | code-analyzer | `.agents/skills/code-analyzer/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S039 | T1 | codenavi | `.agents/skills/codenavi/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S040 | T1 | coding-guidelines | `.agents/skills/coding-guidelines/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S041 | T1 | compatibility-analyzer | `.agents/skills/compatibility-analyzer/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S042 | T1 | compliance-audit-exporter | `.agents/skills/compliance-audit-exporter/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S043 | T1 | compliance-evidence-exporter | `.agents/skills/compliance-evidence-exporter/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S044 | T1 | component-common-domain-detection | `.agents/skills/component-common-domain-detection/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S045 | T1 | component-flattening-analysis | `.agents/skills/component-flattening-analysis/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S046 | T1 | component-identification-sizing | `.agents/skills/component-identification-sizing/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S047 | T1 | conflict-detector | `.agents/skills/conflict-detector/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S048 | T1 | confluence-assistant | `.agents/skills/confluence-assistant/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S049 | T1 | content-to-pipeline | `.agents/skills/content-to-pipeline/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S050 | T1 | context-router | `.agents/skills/context-router/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S051 | T1 | continuity-bootstrapper | `.agents/skills/continuity-bootstrapper/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S052 | T1 | core-web-vitals | `.agents/skills/core-web-vitals/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S053 | T1 | cost-token-optimizer | `.agents/skills/cost-token-optimizer/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S054 | T1 | coupling-analysis | `.agents/skills/coupling-analysis/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S055 | T1 | create-adr | `.agents/skills/create-adr/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S056 | T1 | create-rfc | `.agents/skills/create-rfc/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S057 | T1 | create-technical-design-doc | `.agents/skills/create-technical-design-doc/SKILL.md` | SLIM | ROUTING-ONLY |
| S058 | T1 | critical-thinking-governor | `.agents/skills/critical-thinking-governor/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S059 | T1 | csharp-expert | `.agents/skills/csharp-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S060 | T1 | cursor-subagent-creator | `.agents/skills/cursor-subagent-creator/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S061 | T1 | cve-advisory-sync | `.agents/skills/cve-advisory-sync/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S062 | T1 | cve-remediation | `.agents/skills/cve-remediation/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S063 | T1 | dark-videos-knowledge-base | `.agents/skills/dark-videos-knowledge-base/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S064 | T1 | dark-videos-pipeline-expert | `.agents/skills/dark-videos-pipeline-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S065 | T1 | database-architecture-planner | `.agents/skills/database-architecture-planner/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S066 | T1 | decomposition-planning-roadmap | `.agents/skills/decomposition-planning-roadmap/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S067 | T1 | delegation-auditor | `.agents/skills/delegation-auditor/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S068 | T1 | demo | `.agents/skills/demo/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S069 | T1 | dependency-analyzer | `.agents/skills/dependency-analyzer/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S070 | T1 | dependency-updater | `.agents/skills/dependency-updater/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S071 | T1 | deploy-expert-unique | `.agents/skills/deploy-expert-unique/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S072 | T1 | deployment-pipeline-expert | `.agents/skills/deployment-pipeline-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S073 | T1 | devops-pipeline-engineering | `.agents/skills/devops-pipeline-engineering/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S074 | T1 | diff-reviewer | `.agents/skills/diff-reviewer/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S075 | T1 | docker-devcontainer-engineer | `.agents/skills/docker-devcontainer-engineer/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S076 | T1 | docs-writer | `.agents/skills/docs-writer/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S077 | T1 | documentation | `.agents/skills/documentation/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S078 | T1 | documentation-11-layer-mapper | `.agents/skills/documentation-11-layer-mapper/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S079 | T1 | documentation-mapper | `.agents/skills/documentation-mapper/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S080 | T1 | domain-analysis | `.agents/skills/domain-analysis/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S081 | T1 | domain-identification-grouping | `.agents/skills/domain-identification-grouping/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S082 | T1 | dynatrace-observability-staff | `.agents/skills/dynatrace-observability-staff/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S083 | T1 | enterprise-repo-intelligence | `.agents/skills/enterprise-repo-intelligence/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S084 | T1 | enterprise-security-auditor | `.agents/skills/enterprise-security-auditor/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S085 | T1 | eol-advisory-sync | `.agents/skills/eol-advisory-sync/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S086 | T1 | evaluation-runner | `.agents/skills/evaluation-runner/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S087 | T1 | evidence-cache-auditor | `.agents/skills/evidence-cache-auditor/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S088 | T1 | evidence-integrity-engineer | `.agents/skills/evidence-integrity-engineer/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S089 | T1 | evolutionary-modular-architecture | `.agents/skills/evolutionary-modular-architecture/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S090 | T1 | excalidraw-studio | `.agents/skills/excalidraw-studio/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S091 | T1 | expansion-retention | `.agents/skills/expansion-retention/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S092 | T1 | fable | `.agents/skills/fable/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S093 | T1 | fable-aeos-harness | `.agents/skills/fable-aeos-harness/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S094 | T1 | fable-domain | `.agents/skills/fable-domain/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S095 | T1 | fable-judge | `.agents/skills/fable-judge/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S096 | T1 | fable-loop | `.agents/skills/fable-loop/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S097 | T1 | figma | `.agents/skills/figma/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S098 | T1 | figma-implement-design | `.agents/skills/figma-implement-design/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S099 | T1 | fine-tuning-expert | `.agents/skills/fine-tuning-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S100 | T1 | fixture-corpus-validator | `.agents/skills/fixture-corpus-validator/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S101 | T1 | fleet-mapping | `.agents/skills/fleet-mapping/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S102 | T1 | frontend-blueprint | `.agents/skills/frontend-blueprint/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S103 | T1 | frontend-design | `.agents/skills/frontend-design/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S104 | T1 | gh-address-comments | `.agents/skills/gh-address-comments/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S105 | T1 | gh-fix-ci | `.agents/skills/gh-fix-ci/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S106 | T1 | girl-voice-composer-simulation-expert | `.agents/skills/girl-voice-composer-simulation-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S107 | T1 | github-operations | `.agents/skills/github-operations/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S108 | T1 | grafana-observability-staff | `.agents/skills/grafana-observability-staff/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S109 | T1 | gtm-engineering | `.agents/skills/gtm-engineering/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S110 | T1 | gtm-metrics | `.agents/skills/gtm-metrics/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S111 | T1 | handoff-manager | `.agents/skills/handoff-manager/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S112 | T1 | harness-eval | `.agents/skills/harness-eval/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S113 | T1 | impeccable | `.agents/skills/impeccable/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S114 | T1 | incident-commander | `.agents/skills/incident-commander/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S115 | T1 | incident-response-assistant | `.agents/skills/incident-response-assistant/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S116 | T1 | java-11-expert | `.agents/skills/java-11-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S117 | T1 | java-17-expert | `.agents/skills/java-17-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S118 | T1 | java-21-expert | `.agents/skills/java-21-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S119 | T1 | java-25-expert | `.agents/skills/java-25-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S120 | T1 | java-26-expert | `.agents/skills/java-26-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S121 | T1 | java-8-expert | `.agents/skills/java-8-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S122 | T1 | java-bug-solver | `.agents/skills/java-bug-solver/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S123 | T1 | java-bug-solver-skill | `.agents/skills/java-bug-solver-skill/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S124 | T1 | java-enterprise-modernizer | `.agents/skills/java-enterprise-modernizer/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S125 | T1 | java-expert | `.agents/skills/java-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S126 | T1 | java-migration | `.agents/skills/java-migration/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S127 | T1 | java-version-expert | `.agents/skills/java-version-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S128 | T1 | javascript-expert | `.agents/skills/javascript-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S129 | T1 | jev-call-expert | `.agents/skills/jev-call-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S130 | T1 | jira-assistant | `.agents/skills/jira-assistant/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S131 | T1 | jira-confluence-assistant | `.agents/skills/jira-confluence-assistant/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S132 | T1 | jira-time-entry-assistant | `.agents/skills/jira-time-entry-assistant/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S133 | T1 | judge-benchmark-runner | `.agents/skills/judge-benchmark-runner/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S134 | T1 | kinghost-backup-recovery-expert | `.agents/skills/kinghost-backup-recovery-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S135 | T1 | kinghost-clone-site-expert | `.agents/skills/kinghost-clone-site-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S136 | T1 | kinghost-database-expert | `.agents/skills/kinghost-database-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S137 | T1 | kinghost-domain-dns-ssl-expert | `.agents/skills/kinghost-domain-dns-ssl-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S138 | T1 | kinghost-email-expert | `.agents/skills/kinghost-email-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S139 | T1 | kinghost-expert | `.agents/skills/kinghost-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S140 | T1 | kinghost-performance-expert | `.agents/skills/kinghost-performance-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S141 | T1 | kinghost-security-expert | `.agents/skills/kinghost-security-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S142 | T1 | kinghost-site-publish-ftp-expert | `.agents/skills/kinghost-site-publish-ftp-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S143 | T1 | kotlin-expert | `.agents/skills/kotlin-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S144 | T1 | kubernetes-code-context-mapper | `.agents/skills/kubernetes-code-context-mapper/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S145 | T1 | kubernetes-observability-staff | `.agents/skills/kubernetes-observability-staff/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S146 | T1 | lead-enrichment | `.agents/skills/lead-enrichment/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S147 | T1 | learning-curator | `.agents/skills/learning-curator/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S148 | T1 | learning-opportunities | `.agents/skills/learning-opportunities/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S149 | T1 | legacy-migration-planner | `.agents/skills/legacy-migration-planner/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S150 | T1 | legacy-risk-mapper | `.agents/skills/legacy-risk-mapper/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S151 | T1 | llm-calibration-temperature-expert | `.agents/skills/llm-calibration-temperature-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S152 | T1 | llm-model-selection-expert | `.agents/skills/llm-model-selection-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S153 | T1 | local-secret-vault | `.agents/skills/local-secret-vault/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S154 | T1 | lora-qlora-dora-expert | `.agents/skills/lora-qlora-dora-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S155 | T1 | mantis-architecture | `.agents/skills/mantis-architecture/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S156 | T1 | mantis-calibrate | `.agents/skills/mantis-calibrate/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S157 | T1 | mantis-chain | `.agents/skills/mantis-chain/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S158 | T1 | mantis-critic | `.agents/skills/mantis-critic/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S159 | T1 | mantis-dedupe | `.agents/skills/mantis-dedupe/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S160 | T1 | mantis-history | `.agents/skills/mantis-history/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S161 | T1 | mantis-meta-agent | `.agents/skills/mantis-meta-agent/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S162 | T1 | mantis-patch | `.agents/skills/mantis-patch/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S163 | T1 | mantis-pipeline-adapter | `.agents/skills/mantis-pipeline-adapter/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S164 | T1 | mantis-plan | `.agents/skills/mantis-plan/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S165 | T1 | mantis-reflect | `.agents/skills/mantis-reflect/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S166 | T1 | mantis-report | `.agents/skills/mantis-report/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S167 | T1 | mantis-reproduce | `.agents/skills/mantis-reproduce/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S168 | T1 | mantis-researcher | `.agents/skills/mantis-researcher/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S169 | T1 | mantis-review | `.agents/skills/mantis-review/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S170 | T1 | mantis-structural-index | `.agents/skills/mantis-structural-index/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S171 | T1 | mantis-summarize | `.agents/skills/mantis-summarize/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S172 | T1 | mantis-threat-model | `.agents/skills/mantis-threat-model/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S173 | T1 | marketplace-curator | `.agents/skills/marketplace-curator/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S174 | T1 | mcp-discovery | `.agents/skills/mcp-discovery/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S175 | T1 | mcp-health-check | `.agents/skills/mcp-health-check/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S176 | T1 | mcp-poisoning-evaluator | `.agents/skills/mcp-poisoning-evaluator/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S177 | T1 | mcp-risk-controller | `.agents/skills/mcp-risk-controller/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S178 | T1 | memory-curator | `.agents/skills/memory-curator/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S179 | T1 | memory-governance-auditor | `.agents/skills/memory-governance-auditor/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S180 | T1 | mermaid-studio | `.agents/skills/mermaid-studio/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S181 | T1 | modular-decomposition | `.agents/skills/modular-decomposition/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S182 | T1 | modular-design-principles | `.agents/skills/modular-design-principles/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S183 | T1 | multi-platform-launch | `.agents/skills/multi-platform-launch/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S184 | T1 | multirepo-ecosystem-mapper | `.agents/skills/multirepo-ecosystem-mapper/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S185 | T1 | nestjs-modular-monolith | `.agents/skills/nestjs-modular-monolith/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S186 | T1 | netlify-deploy | `.agents/skills/netlify-deploy/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S187 | T1 | not-your-babysitter | `.agents/skills/not-your-babysitter/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S188 | T1 | notebook-intelligence | `.agents/skills/notebook-intelligence/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S189 | T1 | nx-ci-monitor | `.agents/skills/nx-ci-monitor/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S190 | T1 | nx-generate | `.agents/skills/nx-generate/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S191 | T1 | nx-run-tasks | `.agents/skills/nx-run-tasks/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S192 | T1 | nx-workspace | `.agents/skills/nx-workspace/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S193 | T1 | observability-architect | `.agents/skills/observability-architect/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S194 | T1 | observability-reporter | `.agents/skills/observability-reporter/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S195 | T1 | observability-root-cause-integrator | `.agents/skills/observability-root-cause-integrator/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S196 | T1 | openshift-observability-staff | `.agents/skills/openshift-observability-staff/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S197 | T1 | pack-marketplace-auditor | `.agents/skills/pack-marketplace-auditor/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S198 | T1 | package-trust-engineer | `.agents/skills/package-trust-engineer/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S199 | T1 | packaging | `.agents/skills/packaging/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S200 | T1 | paid-creative-ai | `.agents/skills/paid-creative-ai/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S201 | T1 | parallel-scheduler | `.agents/skills/parallel-scheduler/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S202 | T1 | partner-affiliate | `.agents/skills/partner-affiliate/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S203 | T1 | patch-planner | `.agents/skills/patch-planner/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S204 | T1 | perf-astro | `.agents/skills/perf-astro/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S205 | T1 | perf-lighthouse | `.agents/skills/perf-lighthouse/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S206 | T1 | perf-web-optimization | `.agents/skills/perf-web-optimization/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S207 | T1 | performance-optimizer | `.agents/skills/performance-optimizer/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S208 | T1 | performance-profiler | `.agents/skills/performance-profiler/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S209 | T1 | playbook-factory-generator | `.agents/skills/playbook-factory-generator/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S210 | T1 | playbook-optimizer | `.agents/skills/playbook-optimizer/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S211 | T1 | playwright-skill | `.agents/skills/playwright-skill/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S212 | T1 | policy-bypass-evaluator | `.agents/skills/policy-bypass-evaluator/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S213 | T1 | policy-hardening-auditor | `.agents/skills/policy-hardening-auditor/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S214 | T1 | positioning-icp | `.agents/skills/positioning-icp/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S215 | T1 | pr-comment-resolver | `.agents/skills/pr-comment-resolver/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S216 | T1 | pr-reviewer | `.agents/skills/pr-reviewer/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S217 | T1 | pr-reviewer-advanced | `.agents/skills/pr-reviewer-advanced/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S218 | T1 | production-deployment-planner | `.agents/skills/production-deployment-planner/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S219 | T1 | progress-tracker | `.agents/skills/progress-tracker/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S220 | T1 | prompt-optimizer | `.agents/skills/prompt-optimizer/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S221 | T1 | python-ai-productionizer | `.agents/skills/python-ai-productionizer/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S222 | T1 | python-bug-solver-skill | `.agents/skills/python-bug-solver-skill/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S223 | T1 | python-expert | `.agents/skills/python-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S224 | T1 | python-rag-audit | `.agents/skills/python-rag-audit/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S225 | T1 | rag-expert | `.agents/skills/rag-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S226 | T1 | rails-dev | `.agents/skills/rails-dev/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S227 | T1 | react-best-practices | `.agents/skills/react-best-practices/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S228 | T1 | react-composition-patterns | `.agents/skills/react-composition-patterns/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S229 | T1 | react-expert | `.agents/skills/react-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S230 | T1 | react-native-expert | `.agents/skills/react-native-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S231 | T1 | redaction-evaluator | `.agents/skills/redaction-evaluator/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S232 | T1 | release-readiness-judge | `.agents/skills/release-readiness-judge/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S233 | T1 | render-deploy | `.agents/skills/render-deploy/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S234 | T1 | repo-scanner | `.agents/skills/repo-scanner/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S235 | T1 | report-design | `.agents/skills/report-design/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S236 | T1 | resolver-comentarios | `.agents/skills/resolver-comentarios/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S237 | T1 | revisar-pr | `.agents/skills/revisar-pr/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S238 | T1 | revisar-seguranca-pr | `.agents/skills/revisar-seguranca-pr/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S239 | T1 | risk-classifier | `.agents/skills/risk-classifier/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S240 | T1 | rollback-planner | `.agents/skills/rollback-planner/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S241 | T1 | runtime-troubleshooting | `.agents/skills/runtime-troubleshooting/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S242 | T1 | rust-expert | `.agents/skills/rust-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S243 | T1 | sales-motion-design | `.agents/skills/sales-motion-design/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S244 | T1 | secret-redaction-specialist | `.agents/skills/secret-redaction-specialist/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S245 | T1 | security-audit | `.agents/skills/security-audit/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S246 | T1 | security-best-practices | `.agents/skills/security-best-practices/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S247 | T1 | security-ownership-map | `.agents/skills/security-ownership-map/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S248 | T1 | security-threat-model | `.agents/skills/security-threat-model/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S249 | T1 | sentry | `.agents/skills/sentry/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S250 | T1 | seo | `.agents/skills/seo/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S251 | T1 | servicenow-incident-assistant | `.agents/skills/servicenow-incident-assistant/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S252 | T1 | shopify-developer | `.agents/skills/shopify-developer/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S253 | T1 | simulator-ai | `.agents/skills/simulator-ai/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S254 | T1 | skill-architect | `.agents/skills/skill-architect/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S255 | T1 | skill-factory | `.agents/skills/skill-factory/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S256 | T1 | skill-factory-generator | `.agents/skills/skill-factory-generator/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S257 | T1 | skill-hardener | `.agents/skills/skill-hardener/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S258 | T1 | slo-risk-analyzer | `.agents/skills/slo-risk-analyzer/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S259 | T1 | social-media-operator | `.agents/skills/social-media-operator/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S260 | T1 | social-selling | `.agents/skills/social-selling/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S261 | T1 | solo-founder-gtm | `.agents/skills/solo-founder-gtm/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S262 | T1 | solve-problems | `.agents/skills/solve-problems/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S263 | T1 | spec-driven | `.agents/skills/spec-driven/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S264 | T1 | spec-driven-eval | `.agents/skills/spec-driven-eval/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S265 | T1 | spec-driven-lean | `.agents/skills/spec-driven-lean/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S266 | T1 | specs | `.agents/skills/specs/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S267 | T1 | splunk-observability-staff | `.agents/skills/splunk-observability-staff/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S268 | T1 | staff-iii-architecture-governor | `.agents/skills/staff-iii-architecture-governor/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S269 | T1 | staff-tdd-code-builder | `.agents/skills/staff-tdd-code-builder/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S270 | T1 | subagent-creator | `.agents/skills/subagent-creator/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S271 | T1 | supply-chain-auditor | `.agents/skills/supply-chain-auditor/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S272 | T1 | tactical-ddd | `.agents/skills/tactical-ddd/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S273 | T1 | task-graph-builder | `.agents/skills/task-graph-builder/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S274 | T1 | technical-design-doc-creator | `.agents/skills/technical-design-doc-creator/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S275 | T1 | telemetry-bug-root-cause-solver | `.agents/skills/telemetry-bug-root-cause-solver/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S276 | T1 | test-gap-analyzer | `.agents/skills/test-gap-analyzer/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S277 | T1 | test-generation | `.agents/skills/test-generation/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S278 | T1 | test-strategy-architect | `.agents/skills/test-strategy-architect/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S279 | T1 | test-writer | `.agents/skills/test-writer/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S280 | T1 | tests-expert | `.agents/skills/tests-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S281 | T1 | the-fool | `.agents/skills/the-fool/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S282 | T1 | the-judge | `.agents/skills/the-judge/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S283 | T1 | the-jury | `.agents/skills/the-jury/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S284 | T1 | threat-modeler | `.agents/skills/threat-modeler/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S285 | T1 | tlc-discover | `.agents/skills/tlc-discover/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S286 | T1 | tlc-generative-engine-optimization | `.agents/skills/tlc-generative-engine-optimization/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S287 | T1 | tlc-implement | `.agents/skills/tlc-implement/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S288 | T1 | tlc-plan | `.agents/skills/tlc-plan/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S289 | T1 | tlc-prd | `.agents/skills/tlc-prd/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S290 | T1 | tlc-spec-driven | `.agents/skills/tlc-spec-driven/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S291 | T1 | tlc-spec-lean | `.agents/skills/tlc-spec-lean/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S292 | T1 | token-budget-governor | `.agents/skills/token-budget-governor/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S293 | T1 | tool-router-audit | `.agents/skills/tool-router-audit/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S294 | T1 | typesafe-ai | `.agents/skills/typesafe-ai/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S295 | T1 | unique-environment-auditor | `.agents/skills/unique-environment-auditor/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S296 | T1 | universal-project-factory | `.agents/skills/universal-project-factory/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S297 | T1 | v1-readiness-auditor | `.agents/skills/v1-readiness-auditor/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S298 | T1 | vercel-deploy | `.agents/skills/vercel-deploy/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S299 | T1 | video-outreach | `.agents/skills/video-outreach/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S300 | T1 | voiceai | `.agents/skills/voiceai/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S301 | T1 | vox-aurum | `.agents/skills/vox-aurum/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S302 | T1 | vuln-obsol-recon | `.agents/skills/vuln-obsol-recon/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S303 | T1 | web-accessibility | `.agents/skills/web-accessibility/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S304 | T1 | web-best-practices | `.agents/skills/web-best-practices/SKILL.md` | ROUTING-ONLY | SLIM |
| S305 | T1 | web-design-guidelines | `.agents/skills/web-design-guidelines/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S306 | T1 | web-quality-audit | `.agents/skills/web-quality-audit/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S307 | T1 | whatsapp-simulator | `.agents/skills/whatsapp-simulator/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S308 | T1 | wordpress-expert | `.agents/skills/wordpress-expert/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S309 | T1 | workbench-profile-resolver | `.agents/skills/workbench-profile-resolver/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |

## Slim fan-in blocked (do not stub/delete)

Dual SLIM/ROUTING-ONLY, but another harness surface hard-loads the path (load/SoT/extract mandate). Update or drop those consumers before Slim apply.

| ID | Path | Citers |
|----|------|--------|
| — | — | none |

## Keep-core

| ID | Tier | Name | Path | J1 | J2 |
|----|------|------|------|----|----|
| S001 | T0 | AGENTS.md | `AGENTS.md` | KEEP-CORE | KEEP-CORE |

## Mixed (keep core, slim examples/theory)

Path list only. **Apply instructions:** `11-mixed-apply.md` (KEEP/CUT per ID).

| ID | Tier | Name | Path | J1 | J2 |
|----|------|------|------|----|----|

## Hold

| ID | Tier | Reason | J1 | J2 | Path |
|----|------|--------|----|----|------|

## Action guidance

- **Slim:** compress only after trap PASS **and** fan-in PASS; still human-approve; prefer re-judge on a second model if deleting >30% of a skill.
- **Slim fan-in blocked:** do **not** stub/delete; either keep the checklist body or update every citing harness surface in the same change, then re-merge.
- **Mixed:** open `11-mixed-apply.md` and execute KEEP/CUT per ID only. Do **not** re-judge. Do **not** replace KEEP snippets with `See app/...` or defer KEEP contracts to AGENTS.md. Empty Keep-core/Slim cells → skip that path.
- **Keep-core:** do not slim for usefulness reasons.
- **Hold:** no usefulness trim.
- See `08-usefulness-j1.md` / `09-usefulness-j2.md` for raw score rows.
- Fan-in detail JSON: `slim-fanin.json`.

