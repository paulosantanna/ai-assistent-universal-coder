# Skills canônicas

Updated: 2026-11-09
Entry point: [contrato](STANDARD.md), [catálogo](catalog.json), [esteira](../quality/README.md).

324 pacotes canônicos. Adaptações herdam AGENTS.md; disponibilidade externa deve ser comprovada ao executar.

## architecture

- [ai-architecture-expert]((architecture)/ai-architecture-expert/SKILL.md) — Design or reconstruct production AI architecture with evidence and trade-offs. Use for AI architecture. Do NOT use for deployment.
- [angular-8-to-20-migration]((architecture)/angular-8-to-20-migration/SKILL.md) — Migrate Angular 8 to 20 one major per step, keeping UI and async behavior. Use for upgrades. Do NOT use for single-version code (angular-20-expert).
- [architecture-decision-log]((architecture)/architecture-decision-log/SKILL.md) — Maintain the ADR log: next number, index, statuses, integrity. Use for ADR index work. Do NOT use to write one ADR (architecture-decision-record).
- [architecture-decision-record]((architecture)/architecture-decision-record/SKILL.md) — Write, supersede or review one ADR (MADR, Nygard, Y-statement) and lint it. Use when asked to record a decision. Do NOT use for the ADR index.
- [architecture-knowledge-management]((architecture)/architecture-knowledge-management/SKILL.md) — Govern architecture knowledge: audit missing or stale decisions, recover legacy ones. Use for AKM gaps. Do NOT use for single ADRs or the log index.
- [architecture-mapper]((architecture)/architecture-mapper/SKILL.md) — Map architecture from detected files and explicit evidence. Use when asked to map architecture. Do NOT use for implementation or deployment.
- [blueprint-generator]((architecture)/blueprint-generator/SKILL.md) — Generate an evidence-based project blueprint: boundaries, components, data, gates. Use for blueprints. Do NOT use for implementation or deployment.
- [component-common-domain-detection]((architecture)/component-common-domain-detection/SKILL.md) — Find duplicated business logic across components. Use for overlap before refactoring. Do NOT use for dependencies (coupling-analysis).
- [component-flattening-analysis]((architecture)/component-flattening-analysis/SKILL.md) — Find misplaced classes and fix component hierarchy. Use for orphaned classes or flattening nested components. Do NOT use for domain grouping.
- [component-identification-sizing]((architecture)/component-identification-sizing/SKILL.md) — Map components and measure their size to pick what to extract first. Use for module sizing. Do NOT use for runtime performance or capacity planning.
- [coupling-analysis]((architecture)/coupling-analysis/SKILL.md) — Analyze module coupling (strength, distance, volatility). Use for coupling reports. Do NOT use for domain boundaries (domain-analysis).
- [database-architecture-planner]((architecture)/database-architecture-planner/SKILL.md) — Plan database architecture: schema governance, migrations, backup, restore. Use for DB planning. Do NOT use for implementation or deployment.
- [decomposition-planning-roadmap]((architecture)/decomposition-planning-roadmap/SKILL.md) — Create decomposition plans and migration roadmaps for splitting monoliths. Use for extraction order. Do NOT use for domain analysis (domain-analysis).
- [domain-analysis]((architecture)/domain-analysis/SKILL.md) — Map business domains and service boundaries with DDD strategy. Use for bounded contexts. Do NOT use to group existing components.
- [domain-identification-grouping]((architecture)/domain-identification-grouping/SKILL.md) — Group existing components into domains for service planning. Use for component-to-domain mapping. Do NOT use for new domains (domain-analysis).
- [evolutionary-modular-architecture]((architecture)/evolutionary-modular-architecture/SKILL.md) — Design modular monoliths: DDD contexts, ports and adapters, resilience. Use for platform design. Do NOT use for simple CRUD or tactical-ddd review.
- [frontend-blueprint]((architecture)/frontend-blueprint/SKILL.md) — Discovery-first frontend design: references, tokens and brand before UI code. Use for building or redesigning UI. Do NOT use for backend or APIs.
- [kinghost-database-expert]((architecture)/kinghost-database-expert/SKILL.md) — Governed KingHost MySQL work: access, backup, query analysis, migration, recovery. Use for KingHost databases. Do NOT use for unrelated changes.
- [legacy-migration-planner]((architecture)/legacy-migration-planner/SKILL.md) — Plan legacy migrations, strangler-fig rewrites and framework upgrades. Use for migration strategy. Do NOT use for domain analysis (domain-analysis).
- [legacy-risk-mapper]((architecture)/legacy-risk-mapper/SKILL.md) — Map legacy risks, modernization blockers and migration strategy. Use for legacy risk mapping. Do NOT use for unrelated implementation or deployment.
- [modular-decomposition]((architecture)/modular-decomposition/SKILL.md) — Monolith-to-modular pipeline: sizing, duplication, hierarchy, coupling. Use for splitting monoliths. Do NOT use for roadmaps.
- [modular-design-principles]((architecture)/modular-design-principles/SKILL.md) — Modular design principles: bounded contexts, boundaries, contracts, splits. Use for module structure reviews. Do NOT use for decomposition pipelines.
- [react-composition-patterns]((architecture)/react-composition-patterns/SKILL.md) — React composition: compound components, render props, React 19. Use for component API refactors. Do NOT use for performance (react-best-practices).
- [staff-iii-architecture-governor]((architecture)/staff-iii-architecture-governor/SKILL.md) — Plan and select architecture for new projects or changes. Use for architecture selection. Do NOT use for implementation or deployment.
- [tactical-ddd]((architecture)/tactical-ddd/SKILL.md) — Detect anemic domain models and refactor to rich DDD models. Use for DDD model reviews. Do NOT use for service boundaries or DTOs.

## cloud

- [aws-advisor]((cloud)/aws-advisor/SKILL.md) — AWS architecture, security, service choice and troubleshooting. Use for AWS or AWS services (Lambda, S3, IAM, CDK). Do NOT use for other clouds.
- [cloudflare-deploy]((cloud)/cloudflare-deploy/SKILL.md) — Deploy apps and infrastructure to Cloudflare (Workers, Pages). Use to deploy or host on Cloudflare. Do NOT use for Vercel, Netlify or Render.
- [deployment-pipeline-expert]((cloud)/deployment-pipeline-expert/SKILL.md) — Map, diagnose and improve CI/CD and deployment pipelines safely. Use for pipeline diagnosis. Do NOT use for app features or unapproved prod changes.
- [devops-pipeline-engineering]((cloud)/devops-pipeline-engineering/SKILL.md) — Governed DevOps, Git and Actions lifecycle: CI recovery, merge readiness. Use for DevOps or Actions work. Do NOT use for unapproved prod changes.
- [docker-devcontainer-engineer]((cloud)/docker-devcontainer-engineer/SKILL.md) — Generate devcontainer and Docker artifacts in a sandbox. Use for devcontainer or Dockerfile work. Do NOT use for unapproved prod changes.
- [kinghost-backup-recovery-expert]((cloud)/kinghost-backup-recovery-expert/SKILL.md) — Governed KingHost backup and rollback-safe restore: sites, databases, email. Use for KingHost backups. Do NOT use for unapproved prod changes.
- [kinghost-clone-site-expert]((cloud)/kinghost-clone-site-expert/SKILL.md) — Governed KingHost site clone via verified FTP copy, never mutating the origin. Use for KingHost clones. Do NOT use for unapproved production changes.
- [kinghost-domain-dns-ssl-expert]((cloud)/kinghost-domain-dns-ssl-expert/SKILL.md) — Governed KingHost domain, DNS and SSL changes with snapshot and rollback. Use for KingHost DNS or SSL. Do NOT use for unapproved production changes.
- [kinghost-email-expert]((cloud)/kinghost-email-expert/SKILL.md) — Governed KingHost email: mailboxes, DNS/MX, webmail, recovery, no secret exposure. Use for KingHost email. Do NOT use for unapproved prod changes.
- [kinghost-expert]((cloud)/kinghost-expert/SKILL.md) — KingHost hosting super-skill: domains, FTP/SSH publish, WordPress, MySQL, backups. Use for KingHost work. Do NOT use for unapproved prod changes.
- [kinghost-performance-expert]((cloud)/kinghost-performance-expert/SKILL.md) — Measured KingHost performance: resources, cache, PHP runtime, PageSpeed. Use for KingHost performance. Do NOT use for unapproved prod changes.
- [kinghost-site-publish-ftp-expert]((cloud)/kinghost-site-publish-ftp-expert/SKILL.md) — Governed KingHost WordPress/PHP FTP publish with backup and rollback. Use for KingHost publishing. Do NOT use for unapproved production changes.
- [kubernetes-code-context-mapper]((cloud)/kubernetes-code-context-mapper/SKILL.md) — Map Kubernetes workloads, services and logs back to repo code and owners. Use for K8s-to-code mapping. Do NOT use for unapproved prod changes.
- [netlify-deploy]((cloud)/netlify-deploy/SKILL.md) — Deploy web projects to Netlify via the CLI, including previews. Use for Netlify deploys or links. Do NOT use for Vercel, Cloudflare or Render.
- [production-deployment-planner]((cloud)/production-deployment-planner/SKILL.md) — Plan production packaging, CI/CD, deployment, observability and rollback. Use for deployment plans. Do NOT use for unapproved prod changes.
- [render-deploy]((cloud)/render-deploy/SKILL.md) — Deploy apps to Render: analyze code, generate render.yaml Blueprints. Use for Render deploys. Do NOT use for Vercel, Netlify or Cloudflare.
- [rollback-planner]((cloud)/rollback-planner/SKILL.md) — Generate rollback plans that define how to undo every operation safely. Use for rollback planning. Do NOT use for unapproved production changes.
- [vercel-deploy]((cloud)/vercel-deploy/SKILL.md) — Deploy apps and websites to Vercel, including previews. Use for Vercel deploys or live links. Do NOT use for Netlify, Cloudflare or Render.

## creation

- [ai-project-bootstrapper]((creation)/ai-project-bootstrapper/SKILL.md) — Bootstrap a real AI project from zero or rebuild one step by step. Use to bootstrap an AI project. Do NOT use for one-off coding.
- [create-adr]((creation)/create-adr/SKILL.md) — Create an ADR recording a made architectural decision and its rationale. Use for 'write an ADR'. Do NOT use for undecided choices (create-rfc).
- [create-rfc]((creation)/create-rfc/SKILL.md) — Create RFCs to propose and decide significant changes with stakeholders. Use for 'write an RFC'. Do NOT use for TDDs (technical-design-doc-creator).
- [create-technical-design-doc]((creation)/create-technical-design-doc/SKILL.md) — Create architecture-level technical design docs via discovery. Use for 'write a design doc' or 'criar um TDD'. Do NOT use for README or API docs.
- [cursor-subagent-creator]((creation)/cursor-subagent-creator/SKILL.md) — Design Cursor work units: isolated workflows, verifiers, auditors. Use for isolated work units. Do NOT use for one-off skills or agent identities.
- [playbook-factory-generator]((creation)/playbook-factory-generator/SKILL.md) — Generate a reviewable playbook with step contracts, dependencies and verification gates. Use for playbook generation. Do NOT use for one-off coding.
- [playbook-optimizer]((creation)/playbook-optimizer/SKILL.md) — Optimize playbooks for execution time, safety and evidence quality. Use for playbook optimization. Do NOT use for one-off coding.
- [skill-architect]((creation)/skill-architect/SKILL.md) — Build, score and improve reusable skills with minimal evidence-based edits. Use for creating or reviewing skills. Do NOT use for agent identities.
- [skill-factory]((creation)/skill-factory/SKILL.md) — Create, refactor and validate workspace skills with precise routing. Use for criar or refatorar skills. Do NOT use for agent identities.
- [skill-factory-generator]((creation)/skill-factory-generator/SKILL.md) — Generate a bounded reusable skill package with routing and verifiable gates. Use for skill generation. Do NOT use for unrelated coding.
- [skill-hardener]((creation)/skill-hardener/SKILL.md) — Harden skills with contracts, forbidden actions and quality gates. Use for skill hardening. Do NOT use for unrelated coding.
- [subagent-creator]((creation)/subagent-creator/SKILL.md) — Design bounded lenses of codenavi-agent with one deliverable and a verdict. Use for verifier or audit units. Do NOT use to create agent identities.
- [universal-project-factory]((creation)/universal-project-factory/SKILL.md) — Plan and generate sandbox-first projects from zero to production for any stack. Use for project generation. Do NOT use for ordinary one-off coding.

## decision-making

- [the-fool]((decision-making)/the-fool/SKILL.md) — Stress-test a pending decision: threats, fragile assumptions, blind spots. Use for devil's advocate or pre-mortem. Do NOT use to decide for the owner.
- [the-jury]((decision-making)/the-jury/SKILL.md) — Tally a verdict on a decidable question through 3 or 5 orthogonal lenses. Use for decision panels. Do NOT use to spawn agents or implement.

## design

- [figma]((design)/figma/SKILL.md) — Fetch Figma context, screenshots and assets via MCP. Use for Figma URLs or node IDs. Do NOT use for pixel-perfect builds (figma-implement-design).
- [figma-implement-design]((design)/figma-implement-design/SKILL.md) — Translate Figma nodes into production code with 1:1 fidelity via Figma MCP. Use for Figma URLs to implement. Do NOT use for data fetching (figma).
- [frontend-design]((design)/frontend-design/SKILL.md) — Create distinctive production UIs, avoiding generic AI looks. Use for pages or components. Do NOT use for design audits (web-design-guidelines).
- [impeccable]((design)/impeccable/SKILL.md) — Use when the user wants to design, redesign, shape, critique, audit, polish, clarify, distill, harden, optimize, adapt, animate, colorize, extract, or otherwise improve a frontend interface. Covers websites, landing pages, dashboards, product UI, app shells, components, forms, settings, onboarding, and empty states. Handles UX review, visual hierarchy, information architecture, cognitive load, accessibility, performance, responsive behavior, theming, anti-patterns, typography, fonts, spacing, layout, alignment, color, motion, micro-interactions, UX copy, error states, edge cases, i18n, and reusable design systems or tokens. Also use for bland designs that need to become bolder or more delightful, loud designs that should become quieter, live browser iteration on UI elements, or ambitious visual effects that should feel technically extraordinary. Not for backend-only or non-UI tasks.
- [report-design]((design)/report-design/SKILL.md) — Apply the offline report layout: tokens, grids, filters, export, drill-down. Use for HTML report fixes. Do NOT use for data collection.
- [web-design-guidelines]((design)/web-design-guidelines/SKILL.md) — Review UI code against Web Interface Guidelines: visual and interaction patterns. Use for 'review my UI'. Do NOT use for performance or SEO audits.

## development

- [adr-decision-writer]((development)/adr-decision-writer/SKILL.md) — Write ADRs from inspected evidence only. Use when asked for an ADR or decision record. Do NOT use for deployment or unrelated domains.
- [ai-continuous-training-maintainer]((development)/ai-continuous-training-maintainer/SKILL.md) — Maintain the aidiabetic-research training pipeline (ML practices, CVE-free deps, SAST). Use for it. Do NOT use for other projects or deployment.
- [ai-engineering-expert]((development)/ai-engineering-expert/SKILL.md) — Build or refactor production AI systems from requirements to monitored deployment. Use for AI engineering. Do NOT use for unrelated domains.
- [angular-20-expert]((development)/angular-20-expert/SKILL.md) — Implement, diagnose or modernize Angular 20 apps without other-major behavior. Use for Angular 20 work. Do NOT use for other stacks.
- [architecturally-significant-requirement]((development)/architecturally-significant-requirement/SKILL.md) — Judge if a requirement is architecturally significant (ASR). Use for ASR triage. Do NOT use to write ADRs (architecture-decision-record).
- [atualizar-dependencias]((development)/atualizar-dependencias/SKILL.md) — Update dependencies with manifest/lockfile compatibility and regression evidence. Use for atualizar dependências. Do NOT use for deployment.
- [bm25-expert]((development)/bm25-expert/SKILL.md) — Design, tune and evaluate BM25 and hybrid lexical retrieval. Use for BM25 or hybrid search work. Do NOT use for unrelated domains or deployment.
- [camel-banking-expert]((development)/camel-banking-expert/SKILL.md) — Analyze and implement Apache Camel flows with banking-grade reliability and idempotency. Use for Camel banking flows. Do NOT use for other stacks.
- [ci-quality-gate-engineer]((development)/ci-quality-gate-engineer/SKILL.md) — Create CI/CD quality gates for AEOS and target projects. Use when asked for CI quality gates. Do NOT use for production deployment.
- [codenavi]((development)/codenavi/SKILL.md) — Investigate unknown codebases and change them surgically. Use for bugs, features or unfamiliar flows. Do NOT use for greenfield, CI/CD or infra.
- [coding-guidelines]((development)/coding-guidelines/SKILL.md) — Apply target repo coding conventions, with source evidence, before editing. Use for coding guidelines or style matching. Do NOT use for deployment.
- [compatibility-analyzer]((development)/compatibility-analyzer/SKILL.md) — Analyze dependency compatibility: version conflicts, peer deps, platform limits, breaking changes. Use for compat checks. Do NOT use for deployment.
- [confluence-assistant]((development)/confluence-assistant/SKILL.md) — Confluence operations via Atlassian MCP: search, create, update pages and comments. Use for Confluence requests. Do NOT use for Jira or local files.
- [critical-thinking-governor]((development)/critical-thinking-governor/SKILL.md) — Governs AEOS runs with 20 internal critical-thinking lenses, never agent identities. Use for critical review. Do NOT use for unrelated domains.
- [csharp-expert]((development)/csharp-expert/SKILL.md) — Write and review production C# on current .NET (C# 14, .NET 10). Use for C#, .NET, csproj or .cs work. Do NOT use for F#, VB or non-.NET code.
- [dark-videos-knowledge-base]((development)/dark-videos-knowledge-base/SKILL.md) — Navigate the dark-videos repo map; reconcile old paths with evidence. Use for 'mapa do dark-videos'. Do NOT use to claim inventory or publish.
- [dark-videos-pipeline-expert]((development)/dark-videos-pipeline-expert/SKILL.md) — Run the dark-videos pipeline: mine, rank, frame, publish via dispatch. Use for shorts posting. Do NOT use for a second publisher or cookie export.
- [dependency-analyzer]((development)/dependency-analyzer/SKILL.md) — Analyze dependencies, upgrade candidates, compatibility and risks. Use for dependency analysis or upgrade planning. Do NOT use for deployment.
- [dependency-updater]((development)/dependency-updater/SKILL.md) — Update dependencies with minimal blast radius and evidence-backed compatibility. Use for dependency updates. Do NOT use for deployment.
- [deploy-expert-unique]((development)/deploy-expert-unique/SKILL.md) — AIHealthResearch AWS deploy contract: branch promotion, OSV, CodeQL, validators. Use for AIHealthResearch deploys. Do NOT use for other projects.
- [docs-writer]((development)/docs-writer/SKILL.md) — Write, review and edit docs for structure, tone and accuracy. Use for docs or READMEs. Do NOT use for code comments or API reference generation.
- [documentation]((development)/documentation/SKILL.md) — Generate evidence-based documentation in a sandbox. Use for documentation requests. Do NOT use for production deployment or unrelated stacks.
- [evidence-cache-auditor]((development)/evidence-cache-auditor/SKILL.md) — Audit evidence cache keys, invalidation and stale-cache risks. Use for evidence cache audits. Do NOT use for unrelated stacks or deployment.
- [evidence-integrity-engineer]((development)/evidence-integrity-engineer/SKILL.md) — Validate manifests, hash chains and tamper resistance. Use for evidence integrity checks. Do NOT use for unrelated stacks or deployment.
- [fable]((development)/fable/SKILL.md) — Standard problem-solving loop: classify, gather evidence, act surgically, verify. Use for non-trivial tasks. Do NOT use for trivial one-step answers.
- [fable-aeos-harness]((development)/fable-aeos-harness/SKILL.md) — Execution harness wrapping all AEOS skills with the Fable problem-solving loop. Use to run AEOS skills under Fable. Do NOT use for unrelated stacks.
- [fable-domain]((development)/fable-domain/SKILL.md) — Research a domain and build a Fable adapter, flowchart, trap fixture and smoke eval. Use for new sector adapters. Do NOT use for unrelated stacks.
- [fable-loop]((development)/fable-loop/SKILL.md) — Multi-stage workflow: evidence lenses, one plan, surgical execution, verification. Use for complex multi-stage work. Do NOT use for trivial tasks.
- [fine-tuning-expert]((development)/fine-tuning-expert/SKILL.md) — Decide if fine-tuning is justified; build a governed training pipeline. Use for fine-tuning decisions. Do NOT use for unrelated stacks.
- [gh-address-comments]((development)/gh-address-comments/SKILL.md) — Address review comments on the open GitHub PR of this branch via gh CLI. Use for 'address PR comments'. Do NOT use for CI debugging (gh-fix-ci).
- [harness-eval]((development)/harness-eval/SKILL.md) — Audit an agent harness (AGENTS.md, rules, skills) for broken paths and redundancy. Use for harness audits. Do NOT use for harness setup.
- [java-11-expert]((development)/java-11-expert/SKILL.md) — Build and modernize Java 11 systems with Java 8-to-11 compatibility analysis. Use for Java 11 work. Do NOT use for other languages or deployment.
- [java-17-expert]((development)/java-17-expert/SKILL.md) — Implement and migrate LTS Java 17 applications safely. Use for Java 17 work. Do NOT use for other languages or deployment.
- [java-21-expert]((development)/java-21-expert/SKILL.md) — Design and implement Java 21 systems and migrations with LTS-aware verification. Use for Java 21 work. Do NOT use for other languages or deployment.
- [java-25-expert]((development)/java-25-expert/SKILL.md) — Build or migrate Java 25 projects using only APIs verified for toolchain and runtime. Use for Java 25 work. Do NOT use for other languages.
- [java-26-expert]((development)/java-26-expert/SKILL.md) — Build or migrate Java 26 projects; handle preview status and verify runtime compatibility. Use for Java 26 work. Do NOT use for other languages.
- [java-8-expert]((development)/java-8-expert/SKILL.md) — Implement, diagnose and modernize Java 8 systems without later-version APIs. Use for Java 8 work. Do NOT use for other languages or deployment.
- [java-bug-solver]((development)/java-bug-solver/SKILL.md) — Analyze Java stack traces, find root causes, validate fixes, keep lessons. Use for Java stack traces. Do NOT use for other languages or deployment.
- [java-bug-solver-skill]((development)/java-bug-solver-skill/SKILL.md) — Create a Java bug-solver skill that analyzes stack traces and validates fixes. Use for creating a Java bug solver. Do NOT use for other languages.
- [java-enterprise-modernizer]((development)/java-enterprise-modernizer/SKILL.md) — Analyze Java/Spring enterprise modernization opportunities safely. Use for Java/Spring modernization. Do NOT use for other languages or deployment.
- [java-expert]((development)/java-expert/SKILL.md) — Implement, diagnose and migrate Java projects with version-correct APIs and evidence. Use for Java work. Do NOT use for other languages.
- [java-migration]((development)/java-migration/SKILL.md) — Analyze Java projects and perform version migrations, API replacements and build updates. Use for Java migrations. Do NOT use for other languages.
- [java-version-expert]((development)/java-version-expert/SKILL.md) — Route Java work to the exact verified JDK profile, loading only needed knowledge. Use for JDK version routing. Do NOT use for other languages.
- [javascript-expert]((development)/javascript-expert/SKILL.md) — Implement, diagnose and modernize JavaScript with exact runtime and module compatibility. Use for JavaScript work. Do NOT use for other languages.
- [jev-call-expert]((development)/jev-call-expert/SKILL.md) — Design and review TypeSafe Jev function calling with typed signatures. Use for Jev calls. Do NOT use for generic tool calling or unapproved actions.
- [jira-assistant]((development)/jira-assistant/SKILL.md) — Manage Jira issues via Atlassian MCP: search, create, update, transition. Use for Jira tickets. Do NOT use for Confluence (confluence-assistant).
- [jira-confluence-assistant]((development)/jira-confluence-assistant/SKILL.md) — Prepare governed Jira/Confluence work with traceability to code and evidence. Use for Jira/Confluence tracing. Do NOT use for unrelated stacks.
- [jira-time-entry-assistant]((development)/jira-time-entry-assistant/SKILL.md) — Prepare auditable Jira worklog proposals from actual task evidence. Use for Jira time entries. Do NOT use for unrelated stacks or deployment.
- [kotlin-expert]((development)/kotlin-expert/SKILL.md) — Design and implement Kotlin systems on the current stable release. Use for Kotlin work. Do NOT use for other languages.
- [laya-expert]((development)/laya-expert/SKILL.md) — Implement calibrated typed decisions with the Laya SDK. Use for Laya decisions or RLCD training. Do NOT use for open-ended text or GraphRAG.
- [llm-calibration-temperature-expert]((development)/llm-calibration-temperature-expert/SKILL.md) — Engineer LLM decoding and calibration behavior instead of tuning temperature blindly. Use for LLM calibration. Do NOT use for unrelated stacks.
- [llm-model-selection-expert]((development)/llm-model-selection-expert/SKILL.md) — Select the best current model for a workload, using live capability data and evals. Use for model selection. Do NOT use for unrelated stacks.
- [lora-qlora-dora-expert]((development)/lora-qlora-dora-expert/SKILL.md) — Implement LoRA, QLoRA or DoRA fine-tuning with reproducible experiments. Use for PEFT work. Do NOT use for unrelated stacks.
- [nestjs-modular-monolith]((development)/nestjs-modular-monolith/SKILL.md) — Design NestJS modular monoliths with DDD, CQRS and clean architecture. Use for NestJS bounded contexts. Do NOT use for simple CRUD.
- [not-your-babysitter]((development)/not-your-babysitter/SKILL.md) — Autonomous operator: drive tasks to verified results, evidence-or-stop. Use for autonomous runs. Do NOT use for tutorials or brainstorms.
- [patch-planner]((development)/patch-planner/SKILL.md) — Generate patch proposals and rollback plans without applying them. Use for patch planning. Do NOT use for unrelated stacks or deployment.
- [pr-comment-resolver]((development)/pr-comment-resolver/SKILL.md) — Resolve PR review comments systematically, without blindly obeying incorrect feedback. Use for PR comment resolution. Do NOT use for deployment.
- [pr-reviewer]((development)/pr-reviewer/SKILL.md) — Review pull requests as an independent, evidence-based reviewer. Use for PR reviews. Do NOT use for deployment or unrelated stacks.
- [pr-reviewer-advanced]((development)/pr-reviewer-advanced/SKILL.md) — Perform severity-ranked, evidence-backed PR reviews. Use for deep PR reviews. Do NOT use for deployment or unrelated stacks.
- [python-ai-productionizer]((development)/python-ai-productionizer/SKILL.md) — Analyze Python AI/RAG systems for production readiness. Use for Python AI productionization. Do NOT use for unrelated stacks or deployment.
- [python-bug-solver-skill]((development)/python-bug-solver-skill/SKILL.md) — Create a Python bug-solver skill for stack traces and root-cause fixes. Use for creating a Python bug solver. Do NOT use for other languages.
- [python-expert]((development)/python-expert/SKILL.md) — Implement, diagnose, test and modernize Python projects with version-correct APIs. Use for Python work. Do NOT use for other languages.
- [python-rag-audit]((development)/python-rag-audit/SKILL.md) — Audit Python RAG pipelines for security, data leakage and prompt injection. Use for Python RAG audits. Do NOT use for unrelated stacks.
- [rag-expert]((development)/rag-expert/SKILL.md) — Implement and evaluate grounded retrieval: hybrid search, reranking, citations. Use for RAG work. Do NOT use for standalone Laya training.
- [rag-laya-expert]((development)/rag-laya-expert/SKILL.md) — Orchestrate evaluated RAG and GraphRAG with Laya decisions. Use for RAG or GraphRAG with Laya. Do NOT use for standalone graph drawing.
- [ragraph-expert]((development)/ragraph-expert/SKILL.md) — Build and evaluate source-backed knowledge-graph retrieval (GraphRAG). Use for GraphRAG or entity resolution. Do NOT use for generic diagrams.
- [rails-dev]((development)/rails-dev/SKILL.md) — Rails conventions (rich models, concerns, Minitest). Use for any Rails model, schema or code topic. Do NOT use for non-Rails backends.
- [react-expert]((development)/react-expert/SKILL.md) — Implement and refactor React apps on the repo's exact React version and conventions. Use for React work. Do NOT use for other stacks or deployment.
- [react-native-expert]((development)/react-native-expert/SKILL.md) — Build production React Native and Expo apps: navigation, lists, native modules. Use for mobile app work. Do NOT use for Flutter or web-only React.
- [resolver-comentarios]((development)/resolver-comentarios/SKILL.md) — Resolve concrete PR review comments after inspecting code and verifying fixes. Use for PR comment fixes. Do NOT use for deployment.
- [revisar-pr]((development)/revisar-pr/SKILL.md) — Review a PR diff against requirements and conventions, ranked findings. Use for revisar PR. Do NOT use for security review (revisar-seguranca-pr).
- [runtime-troubleshooting]((development)/runtime-troubleshooting/SKILL.md) — Diagnose apps from read-only logs. Use for runtime failures. Do NOT use to restart, scale, deploy, redesign or invent inaccessible broker state.
- [rust-expert]((development)/rust-expert/SKILL.md) — Implement, diagnose, modernize and migrate Rust projects with version-correct APIs. Use for Rust work. Do NOT use for other languages or deployment.
- [shopify-developer]((development)/shopify-developer/SKILL.md) — Shopify reference: Liquid, themes, GraphQL, Hydrogen, Functions. Use for .liquid files or Shopify apps. Do NOT use for other e-commerce platforms.
- [simulator-ai]((development)/simulator-ai/SKILL.md) — Build a governed AI medical simulator. Use for simulator construction. Never hallucinates or invents results; do NOT use for unrelated stacks.
- [solve-problems]((development)/solve-problems/SKILL.md) — Fix defects across any language without changing project architecture. Use for defect fixes. Do NOT use for unrelated stacks or deployment.
- [spec-driven]((development)/spec-driven/SKILL.md) — Spec-driven 4.0.0 (TLC): specify, design, tasks, execute with EARS and mutation checks. Use for feature specs. Do NOT use for pure architecture.
- [spec-driven-eval]((development)/spec-driven-eval/SKILL.md) — Grade how fully an implementation fulfills a PRD, with one comparable score. Use when explicitly named. Do NOT use to build (tlc-spec-driven).
- [spec-driven-lean]((development)/spec-driven-lean/SKILL.md) — Tech Lead Club spec-lean 2.0.0: freeze obligations in proof-backed checks, then build. Use for spec-driven-lean work. Do NOT use for design docs.
- [specs]((development)/specs/SKILL.md) — Require a spec before implementation: scope, checks, risks. Use for pre-implementation contracts. Do NOT use to override approved requirements.
- [staff-tdd-code-builder]((development)/staff-tdd-code-builder/SKILL.md) — Create or change code from an architecture plan using TDD by default. Use for TDD builds from a plan. Do NOT use for unrelated stacks or deployment.
- [tlc-discover]((development)/tlc-discover/SKILL.md) — Interview an unshaped idea into a verdict and design doc. Use for 'should we build this' or discovery. Do NOT use to cut tasks or implement.
- [tlc-implement]((development)/tlc-implement/SKILL.md) — Implement planned work: extract a checklist, build it, prove each check. Use for 'build this ticket'. Do NOT use to design the work.
- [tlc-plan]((development)/tlc-plan/SKILL.md) — Turn a decided PRD or design doc into tasks with observable criteria. Use for task cutting. Do NOT use for discovery or implementation.
- [tlc-prd]((development)/tlc-prd/SKILL.md) — Interview an idea into a PRD: problem, success, boundaries, journeys. Use for 'write the PRD'. Do NOT use to design solutions or cut tasks.
- [tlc-spec-driven]((development)/tlc-spec-driven/SKILL.md) — TLC spec-driven 4.0.0: specify, design, tasks, execute with EARS and proof checks. Use for feature specs. Do NOT use for pure architecture.
- [tlc-spec-lean]((development)/tlc-spec-lean/SKILL.md) — TLC spec-lean 2.0.0: freeze obligations in proof-backed checks, then build. Use for plan feature or write checks. Do NOT use for design docs.
- [typesafe-ai]((development)/typesafe-ai/SKILL.md) — Build AI features with TypeSafe models (Jev): typed judgments as code primitives. Use for programmable AI decisions. Do NOT use for unrelated stacks.
- [unique-environment-auditor]((development)/unique-environment-auditor/SKILL.md) — Audit an environment inventory for conflicting versions and unmet runtime needs. Use for environment audits. Do NOT use for unrelated stacks.
- [wordpress-expert]((development)/wordpress-expert/SKILL.md) — Staff-level WordPress super-skill: site mapping, clean-code changes, plugins, themes. Use for WordPress work. Do NOT use for unrelated stacks.

## gtm

- [ai-cold-outreach]((gtm)/ai-cold-outreach/SKILL.md) — AI cold outreach: emails, deliverability, personalization. Use for cold email or Instantly/Smartlead/Clay stacks. Do NOT use for code work.
- [ai-pricing]((gtm)/ai-pricing/SKILL.md) — Price AI products: charge metric, tiers, packaging, margins. Use for AI pricing or BYOK. Do NOT use for code or architecture work.
- [ai-sdr]((gtm)/ai-sdr/SKILL.md) — AI SDR deployment: qualification automation, signal routing, sales agents. Use for AI SDR/BDR or autonomous sales. Do NOT use for code work.
- [ai-seo]((gtm)/ai-seo/SKILL.md) — Programmatic SEO, competitor pages, AI Overviews/GEO, keyword strategy. Use for SEO or organic traffic. Do NOT use for code review or architecture.
- [ai-ugc-ads]((gtm)/ai-ugc-ads/SKILL.md) — UGC ad campaigns: creator recruitment, AI UGC content, scaling. Use for UGC or creator ads (Spark, Arcads). Do NOT use for code work.
- [content-to-pipeline]((gtm)/content-to-pipeline/SKILL.md) — Turn content into pipeline: content-led GTM, distribution, repurposing. Use for content marketing or content-led growth. Do NOT use for code work.
- [expansion-retention]((gtm)/expansion-retention/SKILL.md) — Reduce churn and grow expansion revenue: NRR, upsell, customer success, renewals. Use for retention systems. Do NOT use for code work.
- [gtm-engineering]((gtm)/gtm-engineering/SKILL.md) — Build GTM automation: workflow architecture, AI agents, n8n/Make/Zapier. Use for GTM engineering. Do NOT use for code review or architecture.
- [gtm-metrics]((gtm)/gtm-metrics/SKILL.md) — Define GTM metrics and dashboards: pipeline velocity, CAC, LTV, NRR, attribution. Use for GTM measurement. Do NOT use for code work.
- [lead-enrichment]((gtm)/lead-enrichment/SKILL.md) — Lead enrichment waterfalls, ICP scoring and contact verification (Clay, Apollo). Use for enrichment or lead scoring. Do NOT use for code work.
- [multi-platform-launch]((gtm)/multi-platform-launch/SKILL.md) — Plan and run multi-platform product launches: Product Hunt, waitlists, launch day. Use for launch strategy. Do NOT use for code work.
- [paid-creative-ai]((gtm)/paid-creative-ai/SKILL.md) — AI paid ad creative: generation, testing, fatigue, ROAS. Use for ad creative or Meta/Google/TikTok ads. Do NOT use for code work.
- [partner-affiliate]((gtm)/partner-affiliate/SKILL.md) — Design partner and affiliate programs: recruitment, revenue share, co-marketing. Use for partner programs. Do NOT use for code work.
- [positioning-icp]((gtm)/positioning-icp/SKILL.md) — ICP definition, market positioning, messaging and PMF validation for AI-native products. Use for ICP or positioning work. Do NOT use for code work.
- [sales-motion-design]((gtm)/sales-motion-design/SKILL.md) — Choose PLG vs sales-led, design the sales motion and time-to-first-value. Use for sales motion or free-trial design. Do NOT use for code work.
- [social-selling]((gtm)/social-selling/SKILL.md) — LinkedIn social selling: profile optimization, DM sequences, DM-to-deal conversion. Use for LinkedIn selling. Do NOT use for code work.
- [solo-founder-gtm]((gtm)/solo-founder-gtm/SKILL.md) — GTM playbook for solo founders: stack, AI agent team, revenue stages, hiring. Use for solo-founder GTM. Do NOT use for code work.
- [video-outreach]((gtm)/video-outreach/SKILL.md) — Video-first cold outreach: personalized video at scale, async selling, AI demos. Use for video prospecting. Do NOT use for code work.

## learning

- [chromatic-mega-brain]((learning)/chromatic-mega-brain/SKILL.md) — Maintain hierarchical memory and continuity files. Use to resume a project or update handoff. Do NOT use for fleet mapping.
- [context-router]((learning)/context-router/SKILL.md) — Resolve minimal context packets from task, LCPs and memory rules. Use for context packets. Do NOT use to promote unverified claims into memory.
- [continuity-bootstrapper]((learning)/continuity-bootstrapper/SKILL.md) — Bootstrap and validate the CodENavi quartet without inventing project state. Use for continuity setup. Do NOT use to promote unverified claims.
- [cost-token-optimizer]((learning)/cost-token-optimizer/SKILL.md) — Optimize LLM and tool costs via context minimization and cache policy. Use for token cost reduction. Do NOT use to drop required evidence or checks.
- [handoff-manager]((learning)/handoff-manager/SKILL.md) — Maintain a concise .notebook/HANDOFF.md of the last verified state. Use for handoff updates. Do NOT use to promote unverified claims.
- [learning-curator]((learning)/learning-curator/SKILL.md) — Promote verified, reusable engineering lessons into .notebook/LEARNING.md. Use for learning promotion. Do NOT use to promote unverified claims.
- [learning-opportunities]((learning)/learning-opportunities/SKILL.md) — Identify reusable lessons and promotion candidates from finished work. Use for session reviews. Do NOT use to write continuity files.
- [memory-curator]((learning)/memory-curator/SKILL.md) — Curate durable, evidence-backed memory in .notebook/MEMORY.md. Use for memory curation. Do NOT use to promote unverified claims or transient status.
- [memory-governance-auditor]((learning)/memory-governance-auditor/SKILL.md) — Audit memory reads and writes for evidence, scope and secret safety. Use for memory audits. Do NOT use to promote unverified claims into memory.
- [notebook-intelligence]((learning)/notebook-intelligence/SKILL.md) — Maintain compact, fresh project intelligence in .notebook/. Use for notebook maintenance. Do NOT use to promote unverified claims.
- [progress-tracker]((learning)/progress-tracker/SKILL.md) — Keep .notebook/PROGRESS.md as the live, evidence-backed mission checklist. Use for progress tracking. Do NOT use to promote unverified claims.
- [token-budget-governor]((learning)/token-budget-governor/SKILL.md) — Prevent token waste with scoped prompts, compact context and narrow lenses. Use for token budget governance. Do NOT use to promote unverified claims.

## mapping

- [code-analyzer]((mapping)/code-analyzer/SKILL.md) — Analyze change impact and risks in code. Use for proposed changes. Do NOT use to mutate production or invent architecture without source evidence.
- [documentation-11-layer-mapper]((mapping)/documentation-11-layer-mapper/SKILL.md) — 11-layer docs from source: purpose, flows, endpoints. Use for docs. Do NOT use to mutate production or invent architecture without source evidence.
- [documentation-mapper]((mapping)/documentation-mapper/SKILL.md) — Verified enterprise docs from a repo. Use for repo doc mapping. Do NOT use to mutate production or invent architecture without source evidence.
- [enterprise-repo-intelligence]((mapping)/enterprise-repo-intelligence/SKILL.md) — Map enterprise repos with budgets and evidence. Use for repo mapping. Do NOT use to mutate production or invent architecture without source evidence.
- [fleet-mapping]((mapping)/fleet-mapping/SKILL.md) — Map sigla fleet dependencies. Use for mapear a sigla. Do NOT use to fix bugs, provision infra, mutate production or invent business rules.
- [multirepo-ecosystem-mapper]((mapping)/multirepo-ecosystem-mapper/SKILL.md) — Map multi-repo ecosystems and owners. Use for multi-repo mapping. Do NOT use to mutate production or invent architecture without source evidence.
- [repo-scanner]((mapping)/repo-scanner/SKILL.md) — Map repositories into factual ecosystems. Use for repo scans. Do NOT use to mutate production or invent architecture without source evidence.

## monitoring

- [dynatrace-observability-staff]((monitoring)/dynatrace-observability-staff/SKILL.md) — Dynatrace analysis: metrics, logs, traces, Davis problems. Use for Dynatrace investigations. Do NOT use to mutate live systems unless authorized.
- [grafana-observability-staff]((monitoring)/grafana-observability-staff/SKILL.md) — Grafana analysis: dashboards, Prometheus, Loki, Tempo, alerts. Use for Grafana investigations. Do NOT use to mutate live systems unless authorized.
- [incident-commander]((monitoring)/incident-commander/SKILL.md) — Generate incident triage, rollback and postmortem artifacts. Use for incident artifacts. Do NOT use to mutate live systems unless authorized.
- [incident-response-assistant]((monitoring)/incident-response-assistant/SKILL.md) — Support human-led incident triage, RCA and recovery. Use for incident support. Do NOT use to mutate live systems unless authorized.
- [kubernetes-observability-staff]((monitoring)/kubernetes-observability-staff/SKILL.md) — Kubernetes observability: health, workloads, events, probes. Use for K8s investigations. Do NOT use to mutate live systems unless authorized.
- [observability-architect]((monitoring)/observability-architect/SKILL.md) — Design logs, traces, metrics, dashboards, alerting. Use for observability design. Do NOT use to mutate live systems unless authorized.
- [observability-reporter]((monitoring)/observability-reporter/SKILL.md) — Generate timelines, metrics, trace summaries and failure analysis. Use for observability reports. Do NOT use to mutate live systems unless authorized.
- [observability-root-cause-integrator]((monitoring)/observability-root-cause-integrator/SKILL.md) — Merge observability and code evidence into a root-cause plan. Use for root-cause integration. Do NOT use to mutate live systems unless authorized.
- [openshift-observability-staff]((monitoring)/openshift-observability-staff/SKILL.md) — OpenShift observability: monitoring, alerts, logging, operators. Use for OpenShift work. Do NOT use to mutate live systems unless authorized.
- [sentry]((monitoring)/sentry/SKILL.md) — Inspect Sentry issues and production errors via the read-only API. Use for 'check Sentry' reports. Do NOT use for SDK setup or alerts.
- [servicenow-incident-assistant]((monitoring)/servicenow-incident-assistant/SKILL.md) — Turn incident evidence into ServiceNow triage, updates and RCA. Use for ServiceNow incident work. Do NOT use to mutate live systems unless authorized.
- [splunk-observability-staff]((monitoring)/splunk-observability-staff/SKILL.md) — Splunk analysis: searches, metrics, logs, traces, notable events. Use for Splunk work. Do NOT use to mutate live systems unless authorized.
- [telemetry-bug-root-cause-solver]((monitoring)/telemetry-bug-root-cause-solver/SKILL.md) — Resolve bugs from logs, metrics and traces via runtime evidence and code. Use for telemetry RCA. Do NOT use to mutate live systems unless authorized.

## performance

- [core-web-vitals]((performance)/core-web-vitals/SKILL.md) — Fix LCP, INP and CLS to current Google thresholds. Use for Core Web Vitals or layout shifts. Do NOT use for bundles (perf-web-optimization).
- [perf-astro]((performance)/perf-astro/SKILL.md) — Optimize Astro sites for Lighthouse: critical CSS, fonts, LCP. Use for Astro performance. Do NOT use for non-Astro sites or Lighthouse-only audits.
- [perf-lighthouse]((performance)/perf-lighthouse/SKILL.md) — Run Lighthouse via CLI or Node, parse reports, set budgets. Use for Lighthouse audits. Do NOT use for CWV fixes (core-web-vitals).
- [perf-web-optimization]((performance)/perf-web-optimization/SKILL.md) — Measure, then cut bundle size, images, caching and page speed. Use for web performance work. Do NOT use for CWV-only work (core-web-vitals).
- [performance-optimizer]((performance)/performance-optimizer/SKILL.md) — Measure and improve AEOS hot paths: registry, skill runs, evidence. Use for measured optimization. Do NOT use for speculative tuning.
- [performance-profiler]((performance)/performance-profiler/SKILL.md) — Profile AEOS runs: repo scans, hashing, package verification, Judge runtime. Use for AEOS profiling. Do NOT use for speculative tuning.
- [slo-risk-analyzer]((performance)/slo-risk-analyzer/SKILL.md) — Map engineering operations to SLO/SLA risks and error budgets. Use for SLO risk analysis. Do NOT use for unmeasured speculative tuning.

## quality

- [agent-trace-validator]((quality)/agent-trace-validator/SKILL.md) — Validate agent trace completeness and integrity. Use for trace validation. Do NOT use as deployment approval or proof of unexecuted checks.
- [ai-evals-expert]((quality)/ai-evals-expert/SKILL.md) — Turn AI quality claims into reproducible eval evidence. Use for AI quality evaluation. Do NOT use as deployment approval or for unexecuted checks.
- [anti-hallucination-evaluator]((quality)/anti-hallucination-evaluator/SKILL.md) — Anti-hallucination check of claims against inspected sources. Use for hallucination audits. Do NOT use as deployment approval.
- [change-trace-auditor]((quality)/change-trace-auditor/SKILL.md) — Audit change manifests and rollback plans so changes can be reviewed and reverted. Use for change-trace audits. Do NOT use as deployment approval.
- [compliance-audit-exporter]((quality)/compliance-audit-exporter/SKILL.md) — Export a redacted audit package mapping controls to verified evidence and gaps. Use for compliance audit exports. Do NOT use as deployment approval.
- [compliance-evidence-exporter]((quality)/compliance-evidence-exporter/SKILL.md) — Export compliance evidence without leaking secrets. Use for compliance evidence exports. Do NOT use as deployment approval or for unexecuted checks.
- [diff-reviewer]((quality)/diff-reviewer/SKILL.md) — Review generated diffs and patches for correctness, safety and evidence. Use for diff review. Do NOT use as deployment approval.
- [evaluation-runner]((quality)/evaluation-runner/SKILL.md) — Run a supplied evaluation suite; report reproducible results and gaps. Use for running a named eval suite. Do NOT use as deployment approval.
- [fable-judge]((quality)/fable-judge/SKILL.md) — Adversarial verification of finished work: reruns checks, catches false claims. Use for finished-work verification. Do NOT use as deployment approval.
- [fixture-corpus-validator]((quality)/fixture-corpus-validator/SKILL.md) — Validate fixture corpus structure, provenance and expected-output contracts. Use for fixture checks. Do NOT use as deployment approval.
- [judge-benchmark-runner]((quality)/judge-benchmark-runner/SKILL.md) — Benchmark a deterministic Judge gate against a supplied corpus and thresholds. Use for Judge benchmarks. Do NOT use as deployment approval.
- [react-best-practices]((quality)/react-best-practices/SKILL.md) — React/Next.js performance: data fetching, bundles, rendering. Use for React perf work. Do NOT use for component APIs (react-composition-patterns).
- [release-readiness-judge]((quality)/release-readiness-judge/SKILL.md) — Validate release readiness with deterministic gates. Use for release readiness checks. Do NOT use as deployment approval or for unexecuted checks.
- [seo]((quality)/seo/SKILL.md) — Optimize search visibility: meta tags, structured data, sitemaps. Use for 'improve SEO' requests. Do NOT use for accessibility or full site audits.
- [test-gap-analyzer]((quality)/test-gap-analyzer/SKILL.md) — Analyze test coverage gaps: untested modules and edge cases. Use for test gap analysis. Do NOT use as deployment approval or for unexecuted checks.
- [test-generation]((quality)/test-generation/SKILL.md) — Detect test gaps and generate proposed tests in a sandbox. Use for test generation. Do NOT use as deployment approval or for unexecuted checks.
- [test-strategy-architect]((quality)/test-strategy-architect/SKILL.md) — Build test strategy: unit, contract, e2e, security, performance. Use for test planning. Do NOT use as deployment approval or for unexecuted checks.
- [test-writer]((quality)/test-writer/SKILL.md) — Generate proposed tests in a sandbox from evidence; never real test dirs. Use for test proposals. Do NOT use as approval or for unexecuted checks.
- [tests-expert]((quality)/tests-expert/SKILL.md) — Run real functional and e2e checks after a fix or new behavior. Use for fixes, new features or e2e tests. Do NOT use for unit tests or coverage.
- [the-judge]((quality)/the-judge/SKILL.md) — Evidence-first PR judge: repo checks, correctness, security, one GitHub review. Use for 'review this PR' or 'julgue esse PR'. Do NOT use for CI fixes.
- [tlc-generative-engine-optimization]((quality)/tlc-generative-engine-optimization/SKILL.md) — Make pages citable by AI answer engines (GEO): schema, llms.txt, structure. Use for GEO or AI citability. Do NOT use for AI SEO strategy (ai-seo).
- [v1-readiness-auditor]((quality)/v1-readiness-auditor/SKILL.md) — Validate AEOS against v1.0 release gates and generate a blocking report. Use for v1 readiness checks. Do NOT use as deployment approval.
- [web-accessibility]((quality)/web-accessibility/SKILL.md) — Audit and improve web accessibility to WCAG 2.1. Use for a11y audits. Do NOT use for SEO or performance work.
- [web-best-practices]((quality)/web-best-practices/SKILL.md) — Apply modern web security, compatibility and code-quality checks. Use for web best-practice reviews. Do NOT use for accessibility, SEO or full audits.
- [web-quality-audit]((quality)/web-quality-audit/SKILL.md) — Multi-area web audit: performance, accessibility, SEO, best practices. Use for 'audit my site'. Do NOT use for single-area work.

## security

- [approval-governance-auditor]((security)/approval-governance-auditor/SKILL.md) — Validate approval scope, expiry, audit trail. Use when asked to audit approvals. Do NOT use outside authorized scope or to expose secrets.
- [approval-requester]((security)/approval-requester/SKILL.md) — Determine approvals, create requests, track status. Use when asked to request approval. Do NOT use outside authorized scope or to expose secrets.
- [cve-advisory-sync]((security)/cve-advisory-sync/SKILL.md) — Refresh an advisory dataset from authorized OSV/GHSA/NVD. Use for CVE base sync. Do NOT use for assessments (vuln-obsol-recon) or patching.
- [cve-remediation]((security)/cve-remediation/SKILL.md) — Fix a known dependency CVE/GHSA with the smallest compatible change. Use for 'corrigir esta CVE'. Do NOT use for discovery (vuln-obsol-recon).
- [enterprise-security-auditor]((security)/enterprise-security-auditor/SKILL.md) — Audit repo and integration security from trust boundaries. Use for security audits. Do NOT use outside authorized scope or to expose secrets.
- [eol-advisory-sync]((security)/eol-advisory-sync/SKILL.md) — Refresh end-of-life metadata from endoflife.date and maintainers. Use for EOL base sync. Do NOT use for CVE sync or patching.
- [kinghost-security-expert]((security)/kinghost-security-expert/SKILL.md) — KingHost security: malware scans, quarantine, WAF, SSL. Use for KingHost security. Do NOT use outside authorized scope or to expose secrets.
- [local-secret-vault]((security)/local-secret-vault/SKILL.md) — Read authorized local credential vaults, exposing only masked metadata. Use for local vault access. Do NOT use outside scope or to expose secrets.
- [mantis-architecture]((security)/mantis-architecture/SKILL.md) — Build the Mantis knowledge base (architecture, entities, vulnerabilities). Use at the start of a review loop. Do NOT use for threat models or plans.
- [mantis-calibrate]((security)/mantis-calibrate/SKILL.md) — Calculate final risk scores from evidence and architectural impact. Use when findings are processed. Do NOT use to find vulnerabilities or patch.
- [mantis-chain]((security)/mantis-chain/SKILL.md) — Combine validated findings into exploit chains that raise impact. Use after validation. Do NOT use for initial audits or patch code.
- [mantis-critic]((security)/mantis-critic/SKILL.md) — Assess production viability of validated findings, filtering debug-only paths. Use for release-build triggerability. Do NOT use for patches.
- [mantis-dedupe]((security)/mantis-dedupe/SKILL.md) — Consolidate raw security findings to remove redundant reports. Use before review of raw findings. Do NOT use for auditing code or patch generation.
- [mantis-history]((security)/mantis-history/SKILL.md) — Mine VCS history for past vulnerabilities and fixes. Use as first Mantis pre-processing step. Do NOT use for code review or patches.
- [mantis-meta-agent]((security)/mantis-meta-agent/SKILL.md) — Supervise a long-running automated security review campaign. Use for autonomous campaigns. Do NOT use to run single review stages.
- [mantis-patch]((security)/mantis-patch/SKILL.md) — Generate minimal security fixes in isolated copies, then apply and verify. Use for reproduced findings. Do NOT use for research or payloads.
- [mantis-pipeline-adapter]((security)/mantis-pipeline-adapter/SKILL.md) — Design custom deterministic harnesses that wrap Mantis skills. Use for building your own pipeline. Do NOT use to run the default pipeline.
- [mantis-plan]((security)/mantis-plan/SKILL.md) — Formulate a targeted defensive review plan from the threat model and learnings. Use when starting a campaign. Do NOT use for reviews or patches.
- [mantis-reflect]((security)/mantis-reflect/SKILL.md) — Extract learnings from finished review runs: successes, failures, false assumptions. Use for Mantis reflection. Do NOT use for source or patches.
- [mantis-report]((security)/mantis-report/SKILL.md) — Generate a stakeholder security review packet from confirmed findings. Use at the end of a review cycle. Do NOT use for audits or patch checks.
- [mantis-reproduce]((security)/mantis-reproduce/SKILL.md) — Write and run crash reproducers to verify security flaws. Use when viable findings exist. Do NOT use for code auditing or patching.
- [mantis-researcher]((security)/mantis-researcher/SKILL.md) — Audit production source files per the review plan with static analysis and deep dives. Use when a plan exists. Do NOT use for planning or patches.
- [mantis-review]((security)/mantis-review/SKILL.md) — Independently review findings and filter false positives against source. Use for source validation of findings. Do NOT use for repro or patches.
- [mantis-structural-index]((security)/mantis-structural-index/SKILL.md) — Build a content-addressed semantic index of source units. Use when a pinned codebase is available. Do NOT use for findings or patches.
- [mantis-summarize]((security)/mantis-summarize/SKILL.md) — Generate security summaries per directory before planning. Use at the start of a review campaign. Do NOT use for reviews or patches.
- [mantis-threat-model]((security)/mantis-threat-model/SKILL.md) — Synthesize trust boundaries, attack surfaces and attackers into a living threat model. Use for KB stage B. Do NOT use for source analysis.
- [mcp-poisoning-evaluator]((security)/mcp-poisoning-evaluator/SKILL.md) — Evaluate MCP descriptions and responses for injection and poisoning. Use for MCP reviews. Do NOT use outside authorized scope or to expose secrets.
- [package-trust-engineer]((security)/package-trust-engineer/SKILL.md) — Verify packages, manifests, quarantine and promotion. Use for package trust checks. Do NOT use outside authorized scope or to expose secrets.
- [policy-bypass-evaluator]((security)/policy-bypass-evaluator/SKILL.md) — Check policy boundaries reject bypass attempts. Use for bypass evaluations. Do NOT use outside authorized scope or to expose secrets.
- [policy-hardening-auditor]((security)/policy-hardening-auditor/SKILL.md) — Audit policies for unsafe paths and fail-closed behavior. Use for policy hardening. Do NOT use outside authorized scope or to expose secrets.
- [redaction-evaluator]((security)/redaction-evaluator/SKILL.md) — Evaluate redaction in authorized outputs for leakage and over-redaction. Use for redaction reviews. Do NOT use outside scope or to expose secrets.
- [revisar-seguranca-pr]((security)/revisar-seguranca-pr/SKILL.md) — Review a PR diff for authorization, sensitive data and security failures. Use for PR security review. Do NOT use for general review (revisar-pr).
- [risk-classifier]((security)/risk-classifier/SKILL.md) — Classify change risk: scope, impact, reversibility, coverage. Use for risk classification. Do NOT use outside authorized scope or to expose secrets.
- [secret-redaction-specialist]((security)/secret-redaction-specialist/SKILL.md) — Detect and redact sensitive data without exposing raw values. Use for secret redaction. Do NOT use outside authorized scope or to expose secrets.
- [security-audit]((security)/security-audit/SKILL.md) — Detect security risks and possible secrets without exposing values. Use for security audits. Do NOT use outside authorized scope or to expose secrets.
- [security-best-practices]((security)/security-best-practices/SKILL.md) — Review secure-by-default code (Java, Spring, Angular, Python, JS, Go). Use for secure coding. Do NOT use for PR diffs (revisar-seguranca-pr).
- [security-ownership-map]((security)/security-ownership-map/SKILL.md) — Map git ownership: people-to-file, bus factor, orphaned sensitive code. Use for bus-factor checks. Do NOT use for threat models.
- [security-threat-model]((security)/security-threat-model/SKILL.md) — Repo-grounded threat model: trust boundaries, assets, attackers, abuse paths. Use for threat modeling. Do NOT use for architecture summaries.
- [supply-chain-auditor]((security)/supply-chain-auditor/SKILL.md) — Audit dependency provenance and release integrity. Use for supply-chain audits. Do NOT use outside authorized scope or to expose secrets.
- [threat-modeler]((security)/threat-modeler/SKILL.md) — Produce AEOS threat models for prompt injection, tool poisoning and secret leakage. Use for AEOS threat models. Do NOT use outside authorized scope.
- [vuln-obsol-recon]((security)/vuln-obsol-recon/SKILL.md) — Assess CVE and EOL risk. Use for CVE checks. Do NOT use for base sync, patching or invented versions without manifests/runtime evidence.

## tooling

- [acta-aurea]((tooling)/acta-aurea/SKILL.md) — Authorized meeting video to offline pack: transcript, speakers, minutes. Use for an ata or call transcript. Do NOT use for bare audio (vox-aurum).
- [automation-orchestrator]((tooling)/automation-orchestrator/SKILL.md) — Design idempotent multi-step automations from existing skills. Use for automation orchestration. Do NOT use for unapproved remote writes.
- [chrome-devtools]((tooling)/chrome-devtools/SKILL.md) — Debug and profile pages via Chrome DevTools MCP: console, network, performance. Use for 'debug this page'. Do NOT use for E2E (playwright-skill).
- [conflict-detector]((tooling)/conflict-detector/SKILL.md) — Detect read/write, tool, approval and resource conflicts before parallel runs. Use before parallel work. Do NOT use for unapproved remote writes.
- [delegation-auditor]((tooling)/delegation-auditor/SKILL.md) — Validate delegation against policy, scope, capabilities and risk. Use for delegation audits. Do NOT use for unapproved remote writes.
- [documentary-adversarial-judge]((tooling)/documentary-adversarial-judge/SKILL.md) — Adversarial judge of documentary packages: evidence scores, minimum 9.5. Use for julgar o vídeo. Do NOT use to write, mix or approve finally.
- [documentary-audio-engineer]((tooling)/documentary-audio-engineer/SKILL.md) — Mix documentary audio: narration and music ducking, -16 LUFS, -1.5 dBFS peak. Use to mix narration or fix loudness. Do NOT use for music choice.
- [documentary-factory]((tooling)/documentary-factory/SKILL.md) — Runs the documentary factory: six gated roles and a reject-restart loop. Use for full documentary production. Do NOT use for one role or publishing.
- [documentary-music-curator]((tooling)/documentary-music-curator/SKILL.md) — Select calm documentary music with verified license, no Content ID risk. Use for track licensing. Do NOT use for final mix or unlicensed downloads.
- [documentary-social-video-expert]((tooling)/documentary-social-video-expert/SKILL.md) — Publication pack: titles, chapters, thumbnails, vertical cuts. Use for YouTube/Reels metadata. Do NOT use to publish (dark-videos-pipeline-expert).
- [documentary-subject-expert]((tooling)/documentary-subject-expert/SKILL.md) — Subject expert for documentaries: sourced facts, chapter arc, narration. Use for enredo, roteiro or chapters. Do NOT use to judge or acquire assets.
- [documentary-visual-curator]((tooling)/documentary-visual-curator/SKILL.md) — Source on-topic, watermark-free images and GIFs with verified licenses. Use for video visuals. Do NOT use to remove third-party watermarks (policy).
- [excalidraw-studio]((tooling)/excalidraw-studio/SKILL.md) — Generate .excalidraw diagrams from text: flowcharts, architecture, ER, sequence. Use for 'create a diagram'. Do NOT use for Mermaid (mermaid-studio).
- [gh-fix-ci]((tooling)/gh-fix-ci/SKILL.md) — Debug failing GitHub Actions PR checks; apply fixes only after approval. Use for failing checks. Do NOT use for review comments (gh-address-comments).
- [girl-voice-composer-simulation-expert]((tooling)/girl-voice-composer-simulation-expert/SKILL.md) — Direct TTS to synthesize a generic fictional child voice (6-8), pt-BR and en-US. Use for synthetic voice profiles. Do NOT use to clone a real child.
- [github-operations]((tooling)/github-operations/SKILL.md) — Governed Git and GitHub operations: branches, PRs, workflows. Use for Git or GitHub actions. Do NOT use for unapproved remote writes.
- [marketplace-curator]((tooling)/marketplace-curator/SKILL.md) — Curate capability listings by provenance, licensing, scope and compatibility. Use for marketplace curation. Do NOT use for unapproved remote writes.
- [mcp-discovery]((tooling)/mcp-discovery/SKILL.md) — Discover and validate MCP tools and capabilities against AEOS policies. Use for MCP discovery. Do NOT use for unapproved remote writes.
- [mcp-health-check]((tooling)/mcp-health-check/SKILL.md) — Validate MCP runtime health, tools, capabilities and security posture. Use for MCP health checks. Do NOT use for unapproved remote writes.
- [mcp-risk-controller]((tooling)/mcp-risk-controller/SKILL.md) — Audit MCPs, tool descriptions, capabilities and poisoning risks. Use for MCP risk audits. Do NOT use for unapproved remote writes.
- [mermaid-studio]((tooling)/mermaid-studio/SKILL.md) — Create, validate and render Mermaid diagrams (SVG, PNG, ASCII). Use for diagrams or mermaid files. Do NOT use for chart plotting or image generation.
- [motion-comic-animation-expert]((tooling)/motion-comic-animation-expert/SKILL.md) — Motion Comic animation in Python and FFmpeg: camera, layers, parallax. Use for animar camadas or timeline HQ. Do NOT use to promise unrendered output.
- [motion-comic-art-expert]((tooling)/motion-comic-art-expert/SKILL.md) — Arte HQ científica em camadas. Use for storyboards ou bíblia visual. Do NOT use para chamar imagem única de animação ou inventar referência anexada.
- [nx-ci-monitor]((tooling)/nx-ci-monitor/SKILL.md) — Monitor Nx Cloud CI status and handle self-healing fixes. Use for 'watch CI' on Nx. Do NOT use for local task runs (nx-run-tasks).
- [nx-generate]((tooling)/nx-generate/SKILL.md) — Scaffold code with Nx generators: projects, libraries, features. Use for 'nx generate' tasks. Do NOT use for running tasks (nx-run-tasks).
- [nx-run-tasks]((tooling)/nx-run-tasks/SKILL.md) — Run Nx build, test, lint, serve and affected tasks in a workspace. Use for 'run tests' or 'nx affected'. Do NOT use for code generation (nx-generate).
- [nx-workspace]((tooling)/nx-workspace/SKILL.md) — Configure and optimize Nx monorepos: boundaries, affected analysis, caching, CI. Use for Nx workspace setup. Do NOT use to run tasks or generate code.
- [pack-marketplace-auditor]((tooling)/pack-marketplace-auditor/SKILL.md) — Audit pack marketplace quarantine, staging, active packs and trust policy. Use for pack marketplace audits. Do NOT use for unapproved remote writes.
- [packaging]((tooling)/packaging/SKILL.md) — Create, inspect and verify AEOS packages with manifests and checksums. Use for packaging work. Do NOT use for unapproved remote writes.
- [parallel-scheduler]((tooling)/parallel-scheduler/SKILL.md) — Create deterministic safe schedules for playbook tasks from dependency sets. Use for parallel scheduling. Do NOT use for unapproved remote writes.
- [prompt-optimizer]((tooling)/prompt-optimizer/SKILL.md) — Convert vague prompts into bounded, evidence-based task prompts. Use for prompt optimization. Do NOT use for unapproved remote writes.
- [ptbr-documentary-voice-expert]((tooling)/ptbr-documentary-voice-expert/SKILL.md) — Deep male PT-BR documentary narration, scientific pronunciation. Use for narrador de documentário. Do NOT use to clone voices without authorization.
- [science-research-expert]((tooling)/science-research-expert/SKILL.md) — Revisar fontes de ciência. Use for checar afirmações científicas. Do NOT use para inventar referências, certificar medicina ou renderizar vídeo.
- [science-script-expert]((tooling)/science-script-expert/SKILL.md) — Escrever roteiros científicos PT-BR sincronizados com storyboard. Use for roteiro de ciência. Do NOT use for pesquisa sem fontes ou arte final.
- [science-studio-expert]((tooling)/science-studio-expert/SKILL.md) — Orquestrar Science Studio AI do tema ao Motion Comic revisável. Use for criar vídeo de ciência. Do NOT use to publish without review.
- [science-vfx-expert]((tooling)/science-vfx-expert/SKILL.md) — Plan controlled science VFX: gravitational lens, particles, glow. Use for VFX científicos em Motion Comic. Do NOT use to claim validated physics.
- [science-video-review-expert]((tooling)/science-video-review-expert/SKILL.md) — Review and package science Motion Comic videos before export. Use for QA de vídeo de ciência. Do NOT use to self-approve or publish without request.
- [social-media-operator]((tooling)/social-media-operator/SKILL.md) — Governed TikTok/Instagram operations via cookie or browser sessions. Use for social profile reads. Do NOT use for OAuth keys or developer accounts.
- [studio-creation-tlc]((tooling)/studio-creation-tlc/SKILL.md) — TLC rule for Dark Videos media (spec-driven, Spotify). Use for media creation with a role skill. Do NOT use as substitute or to upload mined files.
- [task-graph-builder]((tooling)/task-graph-builder/SKILL.md) — Build a deterministic task graph from a playbook and objective. Use for task graphs. Do NOT use for unapproved remote writes.
- [tool-router-audit]((tooling)/tool-router-audit/SKILL.md) — Audit whether AEOS code and playbooks enforce Tool Router for external actions. Use for Tool Router audits. Do NOT use for unapproved remote writes.
- [voiceai]((tooling)/voiceai/SKILL.md) — Voice interface for AEOS; activation is consent for authorized audio only. Use for voice input or transcription. Do NOT use for remote writes.
- [vox-aurum]((tooling)/vox-aurum/SKILL.md) — Transcribe authorized bare audio offline with local Whisper. Use for offline transcription. Do NOT use for meeting video (acta-aurea).
- [whatsapp-simulator]((tooling)/whatsapp-simulator/SKILL.md) — Generate synthetic WhatsApp-style conversation fixtures for testing. Use for chat fixtures. Do NOT use for unapproved remote writes.
- [workbench-profile-resolver]((tooling)/workbench-profile-resolver/SKILL.md) — Resolve the smallest compatible workbench profile from scope and constraints. Use for profile selection. Do NOT use for unapproved remote writes.

## web-automation

- [demo]((web-automation)/demo/SKILL.md) — Record a web app demo video (mp4 and telemetry) on a real desktop. Use for 'record a demo' or screencasts. Do NOT use for tests (playwright-skill).
- [playwright-skill]((web-automation)/playwright-skill/SKILL.md) — Browser automation and E2E tests with Playwright: forms, flows, responsive checks. Use for web tests. Do NOT use for debugging (chrome-devtools).
