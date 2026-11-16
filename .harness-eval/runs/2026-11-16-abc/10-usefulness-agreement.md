# Harness Eval: Usefulness Agreement (Track C)

> Run dir: `E:\Github\ai-assistent-universal-coder\.harness-eval\runs\2026-11-16-abc`
> Trap gate: PASS (misses=0)
> Fan-in gate: PASS (slim-fanin-blocked=0)
> Judges: J1 model=`gpt-5.6-sol-medium` · J2 model=`gpt-5.6-sol-medium`
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

- Real surfaces scored: 328
- Slim: **8**
- Keep-core: **166**
- Mixed: **4** → apply plan: `11-mixed-apply.md`
- Hold: **150** (fan-in blocked: 0)
- Trap misses: none

## Discrimination (plants)

| ID | Expected family | J2 family |
|----|-----------------|-----------|
| S901 | SLIM | SLIM |
| S902 | SLIM | SLIM |
| S903 | KEEP-CORE | KEEP-CORE |

Slim by tier: {'T1': 8}
Keep-core by tier: {'T0': 1, 'T1': 165}
Mixed by tier: {'T1': 4}
Hold by tier: {'T1': 150}

## Slim (compress / delete body candidates)

| ID | Tier | Name | Path | J1 | J2 |
|----|------|------|------|----|----|
| S002 | T1 | accessibility | `.agents/skills/accessibility/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S026 | T1 | atualizar-dependencias | `.agents/skills/atualizar-dependencias/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S040 | T1 | coding-guidelines | `.agents/skills/coding-guidelines/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S063 | T1 | dark-videos-knowledge-base | `.agents/skills/dark-videos-knowledge-base/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S068 | T1 | demo | `.agents/skills/demo/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S099 | T1 | fable | `.agents/skills/fable/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S100 | T1 | fable-aeos-harness | `.agents/skills/fable-aeos-harness/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |
| S249 | T1 | resolver-comentarios | `.agents/skills/resolver-comentarios/SKILL.md` | ROUTING-ONLY | ROUTING-ONLY |

## Slim fan-in blocked (do not stub/delete)

Dual SLIM/ROUTING-ONLY, but another harness surface hard-loads the path (load/SoT/extract mandate). Update or drop those consumers before Slim apply.

| ID | Path | Citers |
|----|------|--------|
| — | — | none |

## Keep-core

| ID | Tier | Name | Path | J1 | J2 |
|----|------|------|------|----|----|
| S001 | T0 | AGENTS.md | `AGENTS.md` | KEEP-CORE | KEEP-CORE |
| S003 | T1 | acta-aurea | `.agents/skills/acta-aurea/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S005 | T1 | agent-trace-validator | `.agents/skills/agent-trace-validator/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S006 | T1 | ai-architecture-expert | `.agents/skills/ai-architecture-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S009 | T1 | ai-engineering-expert | `.agents/skills/ai-engineering-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S010 | T1 | ai-evals-expert | `.agents/skills/ai-evals-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S012 | T1 | ai-project-bootstrapper | `.agents/skills/ai-project-bootstrapper/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S016 | T1 | angular-20-expert | `.agents/skills/angular-20-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S017 | T1 | angular-8-to-20-migration | `.agents/skills/angular-8-to-20-migration/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S019 | T1 | approval-governance-auditor | `.agents/skills/approval-governance-auditor/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S020 | T1 | approval-requester | `.agents/skills/approval-requester/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S022 | T1 | architecture-decision-log | `.agents/skills/architecture-decision-log/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S024 | T1 | architecture-knowledge-management | `.agents/skills/architecture-knowledge-management/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S025 | T1 | architecture-mapper | `.agents/skills/architecture-mapper/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S027 | T1 | automation-orchestrator | `.agents/skills/automation-orchestrator/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S031 | T1 | bm25-expert | `.agents/skills/bm25-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S032 | T1 | camel-banking-expert | `.agents/skills/camel-banking-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S033 | T1 | change-trace-auditor | `.agents/skills/change-trace-auditor/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S041 | T1 | compatibility-analyzer | `.agents/skills/compatibility-analyzer/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S042 | T1 | compliance-audit-exporter | `.agents/skills/compliance-audit-exporter/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S048 | T1 | confluence-assistant | `.agents/skills/confluence-assistant/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S050 | T1 | context-router | `.agents/skills/context-router/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S051 | T1 | continuity-bootstrapper | `.agents/skills/continuity-bootstrapper/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S052 | T1 | core-web-vitals | `.agents/skills/core-web-vitals/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S059 | T1 | csharp-expert | `.agents/skills/csharp-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S060 | T1 | cursor-subagent-creator | `.agents/skills/cursor-subagent-creator/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S061 | T1 | cve-advisory-sync | `.agents/skills/cve-advisory-sync/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S062 | T1 | cve-remediation | `.agents/skills/cve-remediation/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S064 | T1 | dark-videos-pipeline-expert | `.agents/skills/dark-videos-pipeline-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S065 | T1 | database-architecture-planner | `.agents/skills/database-architecture-planner/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S066 | T1 | decomposition-planning-roadmap | `.agents/skills/decomposition-planning-roadmap/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S070 | T1 | dependency-updater | `.agents/skills/dependency-updater/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S071 | T1 | deploy-expert-unique | `.agents/skills/deploy-expert-unique/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S072 | T1 | deployment-pipeline-expert | `.agents/skills/deployment-pipeline-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S073 | T1 | devops-pipeline-engineering | `.agents/skills/devops-pipeline-engineering/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S074 | T1 | diff-reviewer | `.agents/skills/diff-reviewer/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S076 | T1 | docs-writer | `.agents/skills/docs-writer/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S077 | T1 | documentary-adversarial-judge | `.agents/skills/documentary-adversarial-judge/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S078 | T1 | documentary-audio-engineer | `.agents/skills/documentary-audio-engineer/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S079 | T1 | documentary-factory | `.agents/skills/documentary-factory/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S080 | T1 | documentary-music-curator | `.agents/skills/documentary-music-curator/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S081 | T1 | documentary-social-video-expert | `.agents/skills/documentary-social-video-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S082 | T1 | documentary-subject-expert | `.agents/skills/documentary-subject-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S083 | T1 | documentary-visual-curator | `.agents/skills/documentary-visual-curator/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S092 | T1 | eol-advisory-sync | `.agents/skills/eol-advisory-sync/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S094 | T1 | evidence-cache-auditor | `.agents/skills/evidence-cache-auditor/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S101 | T1 | fable-domain | `.agents/skills/fable-domain/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S102 | T1 | fable-judge | `.agents/skills/fable-judge/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S104 | T1 | figma | `.agents/skills/figma/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S106 | T1 | fine-tuning-expert | `.agents/skills/fine-tuning-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S108 | T1 | fleet-mapping | `.agents/skills/fleet-mapping/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S111 | T1 | gh-address-comments | `.agents/skills/gh-address-comments/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S112 | T1 | gh-fix-ci | `.agents/skills/gh-fix-ci/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S116 | T1 | gtm-engineering | `.agents/skills/gtm-engineering/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S118 | T1 | handoff-manager | `.agents/skills/handoff-manager/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S119 | T1 | harness-eval | `.agents/skills/harness-eval/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S120 | T1 | impeccable | `.agents/skills/impeccable/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S122 | T1 | incident-response-assistant | `.agents/skills/incident-response-assistant/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S123 | T1 | java-11-expert | `.agents/skills/java-11-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S124 | T1 | java-17-expert | `.agents/skills/java-17-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S125 | T1 | java-21-expert | `.agents/skills/java-21-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S126 | T1 | java-25-expert | `.agents/skills/java-25-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S127 | T1 | java-26-expert | `.agents/skills/java-26-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S128 | T1 | java-8-expert | `.agents/skills/java-8-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S132 | T1 | java-expert | `.agents/skills/java-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S133 | T1 | java-migration | `.agents/skills/java-migration/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S135 | T1 | javascript-expert | `.agents/skills/javascript-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S137 | T1 | jira-assistant | `.agents/skills/jira-assistant/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S138 | T1 | jira-confluence-assistant | `.agents/skills/jira-confluence-assistant/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S139 | T1 | jira-time-entry-assistant | `.agents/skills/jira-time-entry-assistant/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S141 | T1 | kinghost-backup-recovery-expert | `.agents/skills/kinghost-backup-recovery-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S143 | T1 | kinghost-database-expert | `.agents/skills/kinghost-database-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S144 | T1 | kinghost-domain-dns-ssl-expert | `.agents/skills/kinghost-domain-dns-ssl-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S145 | T1 | kinghost-email-expert | `.agents/skills/kinghost-email-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S147 | T1 | kinghost-performance-expert | `.agents/skills/kinghost-performance-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S148 | T1 | kinghost-security-expert | `.agents/skills/kinghost-security-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S150 | T1 | kotlin-expert | `.agents/skills/kotlin-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S153 | T1 | laya-expert | `.agents/skills/laya-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S155 | T1 | learning-curator | `.agents/skills/learning-curator/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S156 | T1 | learning-opportunities | `.agents/skills/learning-opportunities/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S157 | T1 | legacy-migration-planner | `.agents/skills/legacy-migration-planner/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S159 | T1 | llm-calibration-temperature-expert | `.agents/skills/llm-calibration-temperature-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S160 | T1 | llm-model-selection-expert | `.agents/skills/llm-model-selection-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S161 | T1 | local-secret-vault | `.agents/skills/local-secret-vault/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S162 | T1 | lora-qlora-dora-expert | `.agents/skills/lora-qlora-dora-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S163 | T1 | mantis-architecture | `.agents/skills/mantis-architecture/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S168 | T1 | mantis-history | `.agents/skills/mantis-history/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S174 | T1 | mantis-report | `.agents/skills/mantis-report/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S175 | T1 | mantis-reproduce | `.agents/skills/mantis-reproduce/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S177 | T1 | mantis-review | `.agents/skills/mantis-review/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S180 | T1 | mantis-threat-model | `.agents/skills/mantis-threat-model/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S183 | T1 | mcp-health-check | `.agents/skills/mcp-health-check/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S186 | T1 | memory-curator | `.agents/skills/memory-curator/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S191 | T1 | motion-comic-animation-expert | `.agents/skills/motion-comic-animation-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S192 | T1 | motion-comic-art-expert | `.agents/skills/motion-comic-art-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S196 | T1 | netlify-deploy | `.agents/skills/netlify-deploy/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S198 | T1 | notebook-intelligence | `.agents/skills/notebook-intelligence/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S201 | T1 | nx-run-tasks | `.agents/skills/nx-run-tasks/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S202 | T1 | nx-workspace | `.agents/skills/nx-workspace/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S203 | T1 | observability-architect | `.agents/skills/observability-architect/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S208 | T1 | package-trust-engineer | `.agents/skills/package-trust-engineer/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S211 | T1 | parallel-scheduler | `.agents/skills/parallel-scheduler/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S213 | T1 | patch-planner | `.agents/skills/patch-planner/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S214 | T1 | perf-astro | `.agents/skills/perf-astro/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S215 | T1 | perf-lighthouse | `.agents/skills/perf-lighthouse/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S216 | T1 | perf-web-optimization | `.agents/skills/perf-web-optimization/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S217 | T1 | performance-optimizer | `.agents/skills/performance-optimizer/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S225 | T1 | pr-comment-resolver | `.agents/skills/pr-comment-resolver/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S226 | T1 | pr-reviewer | `.agents/skills/pr-reviewer/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S228 | T1 | production-deployment-planner | `.agents/skills/production-deployment-planner/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S229 | T1 | progress-tracker | `.agents/skills/progress-tracker/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S231 | T1 | ptbr-documentary-voice-expert | `.agents/skills/ptbr-documentary-voice-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S234 | T1 | python-expert | `.agents/skills/python-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S235 | T1 | python-rag-audit | `.agents/skills/python-rag-audit/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S236 | T1 | rag-expert | `.agents/skills/rag-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S237 | T1 | rag-laya-expert | `.agents/skills/rag-laya-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S238 | T1 | ragraph-expert | `.agents/skills/ragraph-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S239 | T1 | rails-dev | `.agents/skills/rails-dev/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S242 | T1 | react-expert | `.agents/skills/react-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S243 | T1 | react-native-expert | `.agents/skills/react-native-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S245 | T1 | release-readiness-judge | `.agents/skills/release-readiness-judge/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S248 | T1 | report-design | `.agents/skills/report-design/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S250 | T1 | revisar-pr | `.agents/skills/revisar-pr/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S251 | T1 | revisar-seguranca-pr | `.agents/skills/revisar-seguranca-pr/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S254 | T1 | runtime-troubleshooting | `.agents/skills/runtime-troubleshooting/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S255 | T1 | rust-expert | `.agents/skills/rust-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S257 | T1 | science-research-expert | `.agents/skills/science-research-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S258 | T1 | science-script-expert | `.agents/skills/science-script-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S259 | T1 | science-studio-expert | `.agents/skills/science-studio-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S260 | T1 | science-vfx-expert | `.agents/skills/science-vfx-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S261 | T1 | science-video-review-expert | `.agents/skills/science-video-review-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S264 | T1 | security-best-practices | `.agents/skills/security-best-practices/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S265 | T1 | security-ownership-map | `.agents/skills/security-ownership-map/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S266 | T1 | security-threat-model | `.agents/skills/security-threat-model/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S269 | T1 | servicenow-incident-assistant | `.agents/skills/servicenow-incident-assistant/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S270 | T1 | shopify-developer | `.agents/skills/shopify-developer/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S272 | T1 | skill-architect | `.agents/skills/skill-architect/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S273 | T1 | skill-factory | `.agents/skills/skill-factory/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S274 | T1 | skill-factory-generator | `.agents/skills/skill-factory-generator/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S281 | T1 | spec-driven | `.agents/skills/spec-driven/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S282 | T1 | spec-driven-eval | `.agents/skills/spec-driven-eval/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S283 | T1 | spec-driven-lean | `.agents/skills/spec-driven-lean/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S288 | T1 | studio-creation-tlc | `.agents/skills/studio-creation-tlc/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S289 | T1 | subagent-creator | `.agents/skills/subagent-creator/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S290 | T1 | supply-chain-auditor | `.agents/skills/supply-chain-auditor/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S291 | T1 | tactical-ddd | `.agents/skills/tactical-ddd/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S292 | T1 | task-graph-builder | `.agents/skills/task-graph-builder/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S297 | T1 | test-strategy-architect | `.agents/skills/test-strategy-architect/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S298 | T1 | test-writer | `.agents/skills/test-writer/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S299 | T1 | tests-expert | `.agents/skills/tests-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S300 | T1 | the-fool | `.agents/skills/the-fool/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S302 | T1 | the-jury | `.agents/skills/the-jury/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S304 | T1 | tlc-discover | `.agents/skills/tlc-discover/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S306 | T1 | tlc-implement | `.agents/skills/tlc-implement/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S307 | T1 | tlc-plan | `.agents/skills/tlc-plan/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S308 | T1 | tlc-prd | `.agents/skills/tlc-prd/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S309 | T1 | tlc-spec-driven | `.agents/skills/tlc-spec-driven/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S310 | T1 | tlc-spec-lean | `.agents/skills/tlc-spec-lean/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S312 | T1 | tool-router-audit | `.agents/skills/tool-router-audit/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S317 | T1 | vercel-deploy | `.agents/skills/vercel-deploy/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S320 | T1 | vox-aurum | `.agents/skills/vox-aurum/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S321 | T1 | vuln-obsol-recon | `.agents/skills/vuln-obsol-recon/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S324 | T1 | web-design-guidelines | `.agents/skills/web-design-guidelines/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S325 | T1 | web-quality-audit | `.agents/skills/web-quality-audit/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S326 | T1 | whatsapp-simulator | `.agents/skills/whatsapp-simulator/SKILL.md` | KEEP-CORE | KEEP-CORE |
| S327 | T1 | wordpress-expert | `.agents/skills/wordpress-expert/SKILL.md` | KEEP-CORE | KEEP-CORE |

## Mixed (keep core, slim examples/theory)

Path list only. **Apply instructions:** `11-mixed-apply.md` (KEEP/CUT per ID).

| ID | Tier | Name | Path | J1 | J2 |
|----|------|------|------|----|----|
| S058 | T1 | critical-thinking-governor | `.agents/skills/critical-thinking-governor/SKILL.md` | MIXED | MIXED |
| S209 | T1 | packaging | `.agents/skills/packaging/SKILL.md` | MIXED | MIXED |
| S263 | T1 | security-audit | `.agents/skills/security-audit/SKILL.md` | MIXED | MIXED |
| S303 | T1 | threat-modeler | `.agents/skills/threat-modeler/SKILL.md` | MIXED | MIXED |

## Hold

| ID | Tier | Reason | J1 | J2 | Path |
|----|------|--------|----|----|------|
| S004 | T1 | disagree | MIXED | ROUTING-ONLY | `.agents/skills/adr-decision-writer/SKILL.md` |
| S007 | T1 | disagree | KEEP-CORE | SLIM | `.agents/skills/ai-cold-outreach/SKILL.md` |
| S008 | T1 | disagree | KEEP-CORE | ROUTING-ONLY | `.agents/skills/ai-continuous-training-maintainer/SKILL.md` |
| S011 | T1 | disagree | ROUTING-ONLY | MIXED | `.agents/skills/ai-pricing/SKILL.md` |
| S013 | T1 | disagree | MIXED | ROUTING-ONLY | `.agents/skills/ai-sdr/SKILL.md` |
| S014 | T1 | disagree | KEEP-CORE | MIXED | `.agents/skills/ai-seo/SKILL.md` |
| S015 | T1 | disagree | ROUTING-ONLY | MIXED | `.agents/skills/ai-ugc-ads/SKILL.md` |
| S018 | T1 | disagree | MIXED | KEEP-CORE | `.agents/skills/anti-hallucination-evaluator/SKILL.md` |
| S021 | T1 | disagree | KEEP-CORE | ROUTING-ONLY | `.agents/skills/architecturally-significant-requirement/SKILL.md` |
| S023 | T1 | disagree | KEEP-CORE | ROUTING-ONLY | `.agents/skills/architecture-decision-record/SKILL.md` |
| S028 | T1 | disagree | KEEP-CORE | ROUTING-ONLY | `.agents/skills/aws-advisor/SKILL.md` |
| S029 | T1 | disagree | KEEP-CORE | ROUTING-ONLY | `.agents/skills/best-practices/SKILL.md` |
| S030 | T1 | disagree | MIXED | KEEP-CORE | `.agents/skills/blueprint-generator/SKILL.md` |
| S034 | T1 | disagree | MIXED | KEEP-CORE | `.agents/skills/chromatic-mega-brain/SKILL.md` |
| S035 | T1 | disagree | ROUTING-ONLY | MIXED | `.agents/skills/chrome-devtools/SKILL.md` |
| S036 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/ci-quality-gate-engineer/SKILL.md` |
| S037 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/cloudflare-deploy/SKILL.md` |
| S038 | T1 | disagree | KEEP-CORE | MIXED | `.agents/skills/code-analyzer/SKILL.md` |
| S039 | T1 | disagree | MIXED | KEEP-CORE | `.agents/skills/codenavi/SKILL.md` |
| S043 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/compliance-evidence-exporter/SKILL.md` |
| S044 | T1 | disagree | ROUTING-ONLY | MIXED | `.agents/skills/component-common-domain-detection/SKILL.md` |
| S045 | T1 | disagree | MIXED | ROUTING-ONLY | `.agents/skills/component-flattening-analysis/SKILL.md` |
| S046 | T1 | disagree | MIXED | ROUTING-ONLY | `.agents/skills/component-identification-sizing/SKILL.md` |
| S047 | T1 | disagree | KEEP-CORE | MIXED | `.agents/skills/conflict-detector/SKILL.md` |
| S049 | T1 | disagree | ROUTING-ONLY | MIXED | `.agents/skills/content-to-pipeline/SKILL.md` |
| S053 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/cost-token-optimizer/SKILL.md` |
| S054 | T1 | disagree | ROUTING-ONLY | MIXED | `.agents/skills/coupling-analysis/SKILL.md` |
| S055 | T1 | disagree | MIXED | SLIM | `.agents/skills/create-adr/SKILL.md` |
| S056 | T1 | disagree | ROUTING-ONLY | MIXED | `.agents/skills/create-rfc/SKILL.md` |
| S057 | T1 | disagree | MIXED | ROUTING-ONLY | `.agents/skills/create-technical-design-doc/SKILL.md` |
| S067 | T1 | disagree | KEEP-CORE | MIXED | `.agents/skills/delegation-auditor/SKILL.md` |
| S069 | T1 | disagree | MIXED | SLIM | `.agents/skills/dependency-analyzer/SKILL.md` |
| S075 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/docker-devcontainer-engineer/SKILL.md` |
| S084 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/documentation/SKILL.md` |
| S085 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/documentation-11-layer-mapper/SKILL.md` |
| S086 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/documentation-mapper/SKILL.md` |
| S087 | T1 | disagree | ROUTING-ONLY | MIXED | `.agents/skills/domain-analysis/SKILL.md` |
| S088 | T1 | disagree | MIXED | ROUTING-ONLY | `.agents/skills/domain-identification-grouping/SKILL.md` |
| S089 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/dynatrace-observability-staff/SKILL.md` |
| S090 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/enterprise-repo-intelligence/SKILL.md` |
| S091 | T1 | disagree | KEEP-CORE | MIXED | `.agents/skills/enterprise-security-auditor/SKILL.md` |
| S093 | T1 | disagree | KEEP-CORE | MIXED | `.agents/skills/evaluation-runner/SKILL.md` |
| S095 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/evidence-integrity-engineer/SKILL.md` |
| S096 | T1 | disagree | ROUTING-ONLY | MIXED | `.agents/skills/evolutionary-modular-architecture/SKILL.md` |
| S097 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/excalidraw-studio/SKILL.md` |
| S098 | T1 | disagree | KEEP-CORE | SLIM | `.agents/skills/expansion-retention/SKILL.md` |
| S103 | T1 | disagree | KEEP-CORE | SLIM | `.agents/skills/fable-loop/SKILL.md` |
| S105 | T1 | disagree | KEEP-CORE | ROUTING-ONLY | `.agents/skills/figma-implement-design/SKILL.md` |
| S107 | T1 | disagree | KEEP-CORE | MIXED | `.agents/skills/fixture-corpus-validator/SKILL.md` |
| S109 | T1 | disagree | KEEP-CORE | MIXED | `.agents/skills/frontend-blueprint/SKILL.md` |
| S110 | T1 | disagree | KEEP-CORE | ROUTING-ONLY | `.agents/skills/frontend-design/SKILL.md` |
| S113 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/girl-voice-composer-simulation-expert/SKILL.md` |
| S114 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/github-operations/SKILL.md` |
| S115 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/grafana-observability-staff/SKILL.md` |
| S117 | T1 | disagree | ROUTING-ONLY | MIXED | `.agents/skills/gtm-metrics/SKILL.md` |
| S121 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/incident-commander/SKILL.md` |
| S129 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/java-bug-solver/SKILL.md` |
| S130 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/java-bug-solver-skill/SKILL.md` |
| S131 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/java-enterprise-modernizer/SKILL.md` |
| S134 | T1 | disagree | KEEP-CORE | ROUTING-ONLY | `.agents/skills/java-version-expert/SKILL.md` |
| S136 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/jev-call-expert/SKILL.md` |
| S140 | T1 | disagree | KEEP-CORE | MIXED | `.agents/skills/judge-benchmark-runner/SKILL.md` |
| S142 | T1 | disagree | KEEP-CORE | ROUTING-ONLY | `.agents/skills/kinghost-clone-site-expert/SKILL.md` |
| S146 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/kinghost-expert/SKILL.md` |
| S149 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/kinghost-site-publish-ftp-expert/SKILL.md` |
| S151 | T1 | disagree | KEEP-CORE | ROUTING-ONLY | `.agents/skills/kubernetes-code-context-mapper/SKILL.md` |
| S152 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/kubernetes-observability-staff/SKILL.md` |
| S154 | T1 | disagree | MIXED | ROUTING-ONLY | `.agents/skills/lead-enrichment/SKILL.md` |
| S158 | T1 | disagree | MIXED | ROUTING-ONLY | `.agents/skills/legacy-risk-mapper/SKILL.md` |
| S164 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/mantis-calibrate/SKILL.md` |
| S165 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/mantis-chain/SKILL.md` |
| S166 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/mantis-critic/SKILL.md` |
| S167 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/mantis-dedupe/SKILL.md` |
| S169 | T1 | disagree | KEEP-CORE | ROUTING-ONLY | `.agents/skills/mantis-meta-agent/SKILL.md` |
| S170 | T1 | disagree | KEEP-CORE | ROUTING-ONLY | `.agents/skills/mantis-patch/SKILL.md` |
| S171 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/mantis-pipeline-adapter/SKILL.md` |
| S172 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/mantis-plan/SKILL.md` |
| S173 | T1 | disagree | KEEP-CORE | ROUTING-ONLY | `.agents/skills/mantis-reflect/SKILL.md` |
| S176 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/mantis-researcher/SKILL.md` |
| S178 | T1 | disagree | KEEP-CORE | ROUTING-ONLY | `.agents/skills/mantis-structural-index/SKILL.md` |
| S179 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/mantis-summarize/SKILL.md` |
| S181 | T1 | disagree | KEEP-CORE | MIXED | `.agents/skills/marketplace-curator/SKILL.md` |
| S182 | T1 | disagree | MIXED | KEEP-CORE | `.agents/skills/mcp-discovery/SKILL.md` |
| S184 | T1 | disagree | MIXED | KEEP-CORE | `.agents/skills/mcp-poisoning-evaluator/SKILL.md` |
| S185 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/mcp-risk-controller/SKILL.md` |
| S187 | T1 | disagree | KEEP-CORE | MIXED | `.agents/skills/memory-governance-auditor/SKILL.md` |
| S188 | T1 | disagree | KEEP-CORE | ROUTING-ONLY | `.agents/skills/mermaid-studio/SKILL.md` |
| S189 | T1 | disagree | MIXED | KEEP-CORE | `.agents/skills/modular-decomposition/SKILL.md` |
| S190 | T1 | disagree | KEEP-CORE | ROUTING-ONLY | `.agents/skills/modular-design-principles/SKILL.md` |
| S193 | T1 | disagree | ROUTING-ONLY | MIXED | `.agents/skills/multi-platform-launch/SKILL.md` |
| S194 | T1 | disagree | KEEP-CORE | ROUTING-ONLY | `.agents/skills/multirepo-ecosystem-mapper/SKILL.md` |
| S195 | T1 | disagree | ROUTING-ONLY | MIXED | `.agents/skills/nestjs-modular-monolith/SKILL.md` |
| S197 | T1 | disagree | MIXED | KEEP-CORE | `.agents/skills/not-your-babysitter/SKILL.md` |
| S199 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/nx-ci-monitor/SKILL.md` |
| S200 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/nx-generate/SKILL.md` |
| S204 | T1 | disagree | KEEP-CORE | MIXED | `.agents/skills/observability-reporter/SKILL.md` |
| S205 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/observability-root-cause-integrator/SKILL.md` |
| S206 | T1 | disagree | KEEP-CORE | ROUTING-ONLY | `.agents/skills/openshift-observability-staff/SKILL.md` |
| S207 | T1 | disagree | KEEP-CORE | MIXED | `.agents/skills/pack-marketplace-auditor/SKILL.md` |
| S210 | T1 | disagree | ROUTING-ONLY | MIXED | `.agents/skills/paid-creative-ai/SKILL.md` |
| S212 | T1 | disagree | KEEP-CORE | SLIM | `.agents/skills/partner-affiliate/SKILL.md` |
| S218 | T1 | disagree | KEEP-CORE | ROUTING-ONLY | `.agents/skills/performance-profiler/SKILL.md` |
| S219 | T1 | disagree | KEEP-CORE | MIXED | `.agents/skills/playbook-factory-generator/SKILL.md` |
| S220 | T1 | disagree | KEEP-CORE | ROUTING-ONLY | `.agents/skills/playbook-optimizer/SKILL.md` |
| S221 | T1 | disagree | ROUTING-ONLY | MIXED | `.agents/skills/playwright-skill/SKILL.md` |
| S222 | T1 | disagree | KEEP-CORE | MIXED | `.agents/skills/policy-bypass-evaluator/SKILL.md` |
| S223 | T1 | disagree | MIXED | KEEP-CORE | `.agents/skills/policy-hardening-auditor/SKILL.md` |
| S224 | T1 | disagree | ROUTING-ONLY | MIXED | `.agents/skills/positioning-icp/SKILL.md` |
| S227 | T1 | disagree | KEEP-CORE | SLIM | `.agents/skills/pr-reviewer-advanced/SKILL.md` |
| S230 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/prompt-optimizer/SKILL.md` |
| S232 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/python-ai-productionizer/SKILL.md` |
| S233 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/python-bug-solver-skill/SKILL.md` |
| S240 | T1 | disagree | KEEP-CORE | ROUTING-ONLY | `.agents/skills/react-best-practices/SKILL.md` |
| S241 | T1 | disagree | MIXED | SLIM | `.agents/skills/react-composition-patterns/SKILL.md` |
| S244 | T1 | disagree | KEEP-CORE | MIXED | `.agents/skills/redaction-evaluator/SKILL.md` |
| S246 | T1 | disagree | KEEP-CORE | ROUTING-ONLY | `.agents/skills/render-deploy/SKILL.md` |
| S247 | T1 | disagree | MIXED | KEEP-CORE | `.agents/skills/repo-scanner/SKILL.md` |
| S252 | T1 | disagree | MIXED | KEEP-CORE | `.agents/skills/risk-classifier/SKILL.md` |
| S253 | T1 | disagree | MIXED | KEEP-CORE | `.agents/skills/rollback-planner/SKILL.md` |
| S256 | T1 | disagree | MIXED | ROUTING-ONLY | `.agents/skills/sales-motion-design/SKILL.md` |
| S262 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/secret-redaction-specialist/SKILL.md` |
| S267 | T1 | disagree | KEEP-CORE | ROUTING-ONLY | `.agents/skills/sentry/SKILL.md` |
| S268 | T1 | disagree | ROUTING-ONLY | MIXED | `.agents/skills/seo/SKILL.md` |
| S271 | T1 | both-unclear | UNCLEAR | UNCLEAR | `.agents/skills/simulator-ai/SKILL.md` |
| S275 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/skill-hardener/SKILL.md` |
| S276 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/slo-risk-analyzer/SKILL.md` |
| S277 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/social-media-operator/SKILL.md` |
| S278 | T1 | disagree | ROUTING-ONLY | MIXED | `.agents/skills/social-selling/SKILL.md` |
| S279 | T1 | disagree | KEEP-CORE | SLIM | `.agents/skills/solo-founder-gtm/SKILL.md` |
| S280 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/solve-problems/SKILL.md` |
| S284 | T1 | disagree | MIXED | ROUTING-ONLY | `.agents/skills/specs/SKILL.md` |
| S285 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/splunk-observability-staff/SKILL.md` |
| S286 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/staff-iii-architecture-governor/SKILL.md` |
| S287 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/staff-tdd-code-builder/SKILL.md` |
| S293 | T1 | disagree | KEEP-CORE | ROUTING-ONLY | `.agents/skills/technical-design-doc-creator/SKILL.md` |
| S294 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/telemetry-bug-root-cause-solver/SKILL.md` |
| S295 | T1 | disagree | MIXED | KEEP-CORE | `.agents/skills/test-gap-analyzer/SKILL.md` |
| S296 | T1 | disagree | MIXED | SLIM | `.agents/skills/test-generation/SKILL.md` |
| S301 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/the-judge/SKILL.md` |
| S305 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/tlc-generative-engine-optimization/SKILL.md` |
| S311 | T1 | disagree | MIXED | KEEP-CORE | `.agents/skills/token-budget-governor/SKILL.md` |
| S313 | T1 | disagree | KEEP-CORE | ROUTING-ONLY | `.agents/skills/typesafe-ai/SKILL.md` |
| S314 | T1 | disagree | KEEP-CORE | MIXED | `.agents/skills/unique-environment-auditor/SKILL.md` |
| S315 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/universal-project-factory/SKILL.md` |
| S316 | T1 | disagree | KEEP-CORE | MIXED | `.agents/skills/v1-readiness-auditor/SKILL.md` |
| S318 | T1 | disagree | ROUTING-ONLY | MIXED | `.agents/skills/video-outreach/SKILL.md` |
| S319 | T1 | disagree | ROUTING-ONLY | KEEP-CORE | `.agents/skills/voiceai/SKILL.md` |
| S322 | T1 | disagree | ROUTING-ONLY | MIXED | `.agents/skills/web-accessibility/SKILL.md` |
| S323 | T1 | disagree | KEEP-CORE | MIXED | `.agents/skills/web-best-practices/SKILL.md` |
| S328 | T1 | disagree | KEEP-CORE | MIXED | `.agents/skills/workbench-profile-resolver/SKILL.md` |

## Action guidance

- **Slim:** compress only after trap PASS **and** fan-in PASS; still human-approve; prefer re-judge on a second model if deleting >30% of a skill.
- **Slim fan-in blocked:** do **not** stub/delete; either keep the checklist body or update every citing harness surface in the same change, then re-merge.
- **Mixed:** open `11-mixed-apply.md` and execute KEEP/CUT per ID only. Do **not** re-judge. Do **not** replace KEEP snippets with `See app/...` or defer KEEP contracts to AGENTS.md. Empty Keep-core/Slim cells → skip that path.
- **Keep-core:** do not slim for usefulness reasons.
- **Hold:** no usefulness trim.
- See `08-usefulness-j1.md` / `09-usefulness-j2.md` for raw score rows.
- Fan-in detail JSON: `slim-fanin.json`.

