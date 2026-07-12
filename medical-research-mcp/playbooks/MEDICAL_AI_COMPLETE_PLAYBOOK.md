# MEDICAL_AI_COMPLETE_PLAYBOOK.md
# AEOS Disease-Focused Medical AI — Complete Repository-to-Beta Playbook

## 1. Purpose

Transform an existing disease-focused AI repository into a reproducible, secure, observable, documented, and governed **research-only Beta**.

The target system may:

- discover and normalize biomedical evidence;
- model disease, subgroups, and comorbidities;
- train and evaluate retrieval and machine-learning components;
- generate computational hypotheses;
- compare hypotheses with external literature and trial registries;
- create evidence packages for qualified scientific review.

The target system may not autonomously authorize wet-lab, animal, or human experimentation and may not claim a cure, safety, efficacy, or clinical validity from software or simulation results alone.

## 2. Governing principles

1. Evidence before claims.
2. Repository truth before redesign.
3. Characterization tests before refactor.
4. Modular-monolith-first while boundaries are unstable.
5. Deterministic validation before model judgment.
6. Independent review before completion.
7. Provenance before training.
8. External validation separated from internal evaluation.
9. Simulation treated as hypothesis generation.
10. Human and regulatory authority over laboratory and clinical transitions.
11. Token economy through scope isolation, not through evidence removal.
12. Score 10.0 only when every mandatory criterion passes with direct evidence.

## 3. Agent organization

```text
Human Authority
      ↓
ROOT Medical AI Architect
      ↓
Planning Orchestrator
      ├── Repository Cartographer
      ├── Architecture Governor
      ├── Medical Evidence Researcher
      ├── Qualified Source Curator
      ├── Data Governance Specialist
      ├── Training Pipeline Specialist
      ├── RAG Specialist
      ├── BM25 Specialist
      ├── Adapter Specialist
      ├── Continuous Learning Specialist
      ├── Simulation Scientist
      ├── OWASP AI Security Specialist
      ├── Vulnerability Intelligence Specialist
      ├── Python Staff Engineer
      ├── Test and Evaluation Engineer
      ├── Documentation Engineer
      └── Token and Context Governor
      ↓
Independent Expert Judge
```

## 4. Token-efficient execution

Before reading source:

1. hash the repository state;
2. scan manifests and top-level structure;
3. build a symbol and module inventory;
4. cache repository and evidence indexes;
5. select only the agents required by the current phase;
6. create bounded handovers;
7. stop duplicate investigations;
8. send the Judge only scope, claims, evidence, contradictions, failures, and risk.

Recommended budget:

```yaml
root: 14%
evidence: 22%
specialists: 44%
synthesis: 8%
judge: 12%
```

Critical tasks may receive a risk multiplier, but all budgets remain bounded.

---

# Phase 0 — Authority, scope, and immutable baseline

## Owner

ROOT Medical AI Architect + Repository Cartographer.

## Actions

- identify the repository root;
- record branch, commit, dirty state, and file hashes;
- create an isolated work branch;
- create a backup or validated restore point;
- record operating system, Python, Java, Node, CUDA, GPU, containers, and external services;
- load `config/disease-profile.yaml`;
- declare the intended research-only use;
- define allowed and forbidden paths;
- identify data that may contain personal or clinical information;
- identify credentials and external systems;
- create the first execution ID and handovers.

## Evidence

- Git status and commit hash;
- environment inventory;
- repository manifest;
- backup verification;
- approved scope;
- disease profile hash.

## Gate

`PASS` only when baseline and rollback are reproducible.

---

# Phase 1 — Repository cartography and current-state truth

## Owner

Repository Cartographer.

## Actions

- inventory languages, frameworks, libraries, manifests, lockfiles, services, scripts, tests, and docs;
- map entry points and runtime flows;
- map ingestion, data curation, knowledge, RAG, training, evaluation, simulation, API, security, and observability;
- identify duplicated and orphaned modules;
- identify hidden side effects, direct file writes, global state, and cyclic dependencies;
- map data stores, vector stores, model artifacts, caches, queues, and external APIs;
- identify current deployment and execution procedures;
- identify documentation drift.

## Deliverables

- repository inventory;
- module dependency graph;
- data-flow diagram;
- current training and simulation pipeline;
- runtime sequence;
- test inventory;
- documentation drift report;
- evidence index by file and symbol.

## Gate

No material component remains unmapped or explicitly marked unknown.

---

# Phase 2 — Scientific question and disease model

## Owner

Medical Evidence Researcher + Qualified Source Curator.

## Actions

- formalize disease, aliases, subgroups, and comorbidities;
- formalize biomarkers, mechanisms, interventions, outcomes, adverse events, contraindications, and exclusions;
- distinguish exploratory, diagnostic, prognostic, treatment-response, remission, prevention, and cure-related questions;
- define population, intervention, comparator, outcome, timing, and study-design fields where applicable;
- define what evidence would falsify a hypothesis;
- define prohibited unsupported claims.

## Deliverables

- versioned disease profile;
- research-question catalog;
- evidence inclusion and exclusion criteria;
- falsification criteria;
- terminology and ontology map.

## Gate

Every research question is bounded, testable, and mapped to evidence requirements.

---

# Phase 3 — Qualified source governance

## Owner

Qualified Source Curator.

## Source tiers

### Tier 1 — Primary and authoritative

- PubMed / NCBI;
- Europe PMC;
- ClinicalTrials.gov;
- WHO ICTRP and recognized primary registries;
- FDA, EMA, ANVISA, MHRA, Health Canada, TGA, and PMDA;
- official standards and guidance;
- primary peer-reviewed publications.

### Tier 2 — High-value secondary evidence

- systematic reviews;
- evidence-synthesis organizations;
- professional society guidelines;
- recognized biomedical repositories.

### Tier 3 — Discovery only

- preprints;
- conference abstracts;
- institutional pages;
- secondary indexes.

Tier 3 evidence cannot independently support high-impact conclusions.

## Actions

- define approved access methods;
- prefer official APIs and licensed exports;
- record query, date, source, source version, identifier, and retrieval method;
- preserve corrections, retractions, updates, negative findings, and contradictions;
- respect copyright, access controls, robots rules, terms, and rate limits;
- prohibit access-controlled or patient-identifiable scraping;
- define source authority and freshness rules.

## Gate

Every source has an access policy, authority tier, provenance requirements, and update strategy.

---

# Phase 4 — Evidence ingestion and normalization

## Owner

Medical Evidence Researcher + Data Governance Specialist.

## Actions

- execute versioned searches;
- ingest identifiers and metadata;
- retrieve licensed text only when permitted;
- normalize evidence into `schemas/evidence.schema.json`;
- deduplicate by stable identifiers, title, author, trial registration, and semantic similarity;
- link publications to trial registrations where possible;
- classify study type;
- extract population, subgroup, comorbidity, intervention, comparator, outcomes, adverse events, and limitations;
- record risk-of-bias fields;
- retain contradictory and failed interventions;
- detect retractions and corrections;
- separate raw, screened, extracted, validated, rejected, and superseded states.

## Gate

Evidence records are reproducible, schema-valid, deduplicated, and traceable.

---

# Phase 5 — Data governance, privacy, and leakage prevention

## Owner

Data Governance Specialist.

## Actions

- create immutable raw and versioned curated zones;
- document licenses and permitted uses;
- de-identify personal or clinical data;
- create dataset cards;
- record full lineage;
- enforce entity-aware deduplication;
- separate train, validation, internal test, temporal test, and external validation;
- detect patient, publication, institution, temporal, prompt, and benchmark leakage;
- evaluate representation of disease subgroups and comorbidities;
- define data-retention and deletion rules;
- validate access controls.

## Gate

Zero blocking provenance, privacy, license, or leakage finding.

---

# Phase 6 — Architecture decision

## Owner

Architecture Governor + Security + Delivery specialists.

## Options

- preserve the current architecture;
- modular monolith;
- hybrid architecture;
- microservices;
- batch and worker separation;
- event-driven extraction.

## Criteria

- bounded-context stability;
- coupling;
- independent scaling;
- independent deployment;
- failure isolation;
- data ownership;
- consistency;
- latency;
- compute requirements;
- local and cloud constraints;
- team size;
- observability and operational maturity;
- cost;
- migration and rollback risk.

## Default

Use a modular monolith while boundaries are evolving. Extract ingestion, training, simulation, or serving workers only when independently measured requirements justify it.

## Deliverables

- ADR;
- target architecture;
- module contracts;
- migration sequence;
- compatibility strategy;
- rollback strategy;
- security impact;
- scientific-validity impact.

## Gate

ADR accepted with direct repository evidence.

---

# Phase 7 — Characterization before code changes

## Owner

Test and Evaluation Engineer.

## Actions

- execute existing tests;
- capture current failures;
- add characterization tests around undocumented behavior;
- snapshot public APIs and schemas;
- capture current dataset, retrieval, training, model, and simulation metrics;
- identify non-determinism;
- create regression fixtures;
- classify each module as preserve, refactor, replace, or remove.

## Gate

Current behavior is characterized sufficiently to detect unintended change.

---

# Phase 8 — BM25 baseline

## Owner

BM25 Specialist.

## Actions

- define tokenizer and normalization;
- evaluate title, abstract, full-text, keyword, and metadata fields separately;
- establish BM25 parameters and corpus statistics;
- build relevance judgments;
- measure Recall@k, Precision@k, nDCG@k, and MRR;
- perform error analysis;
- preserve BM25 as a transparent baseline even when dense retrieval is added;
- create deterministic regression tests.

## Gate

BM25 baseline is reproducible and benchmarked.

---

# Phase 9 — RAG and grounded reasoning

## Owner

RAG Specialist.

## Actions

- audit chunking and document boundaries;
- version the embedding model;
- build sparse and dense indexes;
- measure each retriever independently;
- implement evidence-backed fusion;
- implement reranking;
- enforce metadata and authorization filtering;
- bind claims to identifiers and source spans;
- implement abstention;
- retrieve contradictions and retractions;
- detect unsupported claims;
- evaluate subgroup and comorbidity coverage;
- create adversarial retrieval tests.

## Metrics

- Recall@k;
- Precision@k;
- nDCG@k;
- MRR;
- citation correctness;
- source authority;
- unsupported-claim rate;
- abstention precision;
- contradiction recall;
- subgroup coverage.

## Gate

Predefined grounding thresholds pass with executed evidence.

---

# Phase 10 — Training pipeline and adapter selection

## Owner

Training Pipeline Specialist + Adapter Specialist.

## Actions

- define immutable dataset versions;
- protect validation and test sets;
- record seed, hardware, CUDA, libraries, model hash, configuration, and prompts;
- compare untuned, retrieval-only, LoRA, QLoRA, and DoRA baselines;
- use composed or double adapters only with explicit interference tests;
- track checkpoints and artifacts;
- produce model cards;
- evaluate general, disease-specific, subgroup, safety, calibration, and contradiction behavior;
- test catastrophic forgetting;
- test reproducibility.

## Gate

No candidate is promoted without outperforming the approved baseline on required criteria and without critical regression.

---

# Phase 11 — Continuous learning architecture

## Owner

Continuous Learning Specialist.

## Actions

- ingest new evidence as candidate data;
- re-run provenance, deduplication, quality, and leakage gates;
- version candidate datasets, indexes, adapters, models, prompts, and policies;
- maintain representative historical replay;
- monitor data, retrieval, calibration, subgroup, model, and security drift separately;
- evaluate candidates in shadow mode;
- require independent Judge review;
- require approval;
- provide rollback;
- supersede or deprecate knowledge instead of silently overwriting it.

## Prohibition

No autonomous online modification of clinical behavior.

## Gate

Replay, drift, shadow, approval, provenance, and rollback all pass.

---

# Phase 12 — Computational simulation

## Owner

Simulation Scientist.

## Permitted scope

- statistical simulation;
- causal sensitivity analysis;
- systems-biology hypothesis generation;
- validated external molecular or mechanistic workflows;
- counterfactual exploration;
- uncertainty analysis.

## Required controls

- assumptions;
- boundary conditions;
- calibration source;
- model validity domain;
- negative controls;
- sensitivity;
- uncertainty;
- external benchmarks;
- falsification criteria;
- reproducibility;
- independent scientific review.

## Prohibited interpretation

Simulation output must not be described as biological efficacy, safety, clinical validity, or cure.

## Gate

Simulation is explicitly hypothesis-generating and independently reviewable.

---

# Phase 13 — External evidence and trial validation

## Owner

Medical Evidence Researcher + Simulation Scientist.

## Actions

- search independent literature;
- search ClinicalTrials.gov and recognized registries;
- map population, intervention, comparator, outcomes, trial status, results, adverse events, and limitations;
- include negative, failed, terminated, withdrawn, and harmful interventions;
- assess subgroup applicability;
- build a contradiction matrix;
- separate retrospective, external, prospective, preclinical, and clinical evidence;
- define evidence gaps.

## Gate

Independent evidence synthesis exists with unresolved contradictions visible.

---

# Phase 14 — OWASP, agent security, and supply chain

## Owner

OWASP AI Security Specialist + Vulnerability Intelligence Specialist.

## Actions

- create application, API, GenAI, and agentic threat models;
- test prompt injection and indirect prompt injection;
- enforce instruction/data separation;
- implement least-privilege tools;
- validate model outputs before execution;
- isolate vector data and enforce authorization;
- detect data and model poisoning;
- set token, timeout, recursion, concurrency, and cost limits;
- scan secrets and rotate exposed credentials;
- generate SBOM;
- correlate OSV, GitHub advisories, NVD, CISA KEV, FIRST EPSS, and vendor advisories;
- assess reachability and exposure;
- scan containers, operating systems, and infrastructure as code;
- verify model and dataset provenance.

## Gate

No unaccepted known-exploited critical vulnerability and no unresolved critical excessive-agency path.

---

# Phase 15 — Controlled implementation and refactor

## Owner

Python Staff Engineer + relevant domain specialists.

## Per-change loop

```text
Approved handover
→ relevant context only
→ implementation
→ local deterministic validation
→ tests
→ evidence
→ domain review
→ integration
→ documentation update
```

## Rules

- no unrelated refactoring;
- no big-bang rewrite;
- no architecture boundary changes without ADR;
- no dependency upgrade without compatibility tests;
- no silent schema migration;
- no deletion without backup or rollback;
- no completion claim without direct evidence.

## Gate

Each bounded change passes its acceptance criteria.

---

# Phase 16 — Complete testing and evaluation

## Owner

Test and Evaluation Engineer.

## Required where applicable

- unit tests;
- integration tests;
- contract tests;
- end-to-end tests;
- schema and data-quality tests;
- provenance tests;
- leakage tests;
- BM25 tests;
- RAG and citation tests;
- contradiction tests;
- model regression;
- calibration and uncertainty;
- subgroup and comorbidity analysis;
- simulation reproducibility;
- security adversarial tests;
- load, resilience, timeout, and recovery tests;
- rollback tests;
- installation reproducibility.

## Gate

All mandatory tests execute successfully with stored outputs.

---

# Phase 17 — Documentation and Beta readiness

## Owner

Documentation Engineer + Independent Expert Judge.

## Required documents

- README;
- architecture;
- C4 or equivalent diagrams;
- ADRs;
- source policy;
- evidence schema;
- data lineage;
- dataset cards;
- model cards;
- retrieval evaluation;
- training evaluation;
- simulation limitations;
- MCP tool catalog;
- threat model;
- SBOM and vulnerability report;
- deployment guide;
- operations runbook;
- backup and rollback;
- limitations;
- scientific and regulatory boundaries;
- Beta readiness report.

## Strict Judge gate

Acceptance requires:

```text
score == 10.0
AND every mandatory criterion passed
AND every pass has evidence
AND no blocking finding remains
AND documentation matches implementation
AND research-only boundaries remain enforced
```

Possible final statuses:

- `BETA_READY_RESEARCH_ONLY`;
- `REWORK_REQUIRED`;
- `BLOCKED`;
- `WAITING_APPROVAL`.

---

# Phase 18 — Preclinical and human-research boundary

AEOS may assemble a research dossier and evidence traceability package.

Any transition beyond computational research requires qualified external institutions and applicable:

- scientific review;
- biosafety review;
- ethics committee or IRB;
- regulatory authorization;
- public trial registration before recruitment;
- informed consent;
- data safety monitoring;
- validated laboratory and manufacturing controls;
- qualified principal investigators.

AEOS never autonomously authorizes:

- wet-lab execution;
- animal experiments;
- participant recruitment;
- dosing or intervention;
- treatment decisions;
- a cure claim.

---

# Final Beta deliverable

```text
Research-only Beta
├── reproducible installation
├── versioned data, indexes, models, prompts, and policies
├── governed evidence ingestion
├── BM25 and RAG evaluation
├── training and adapter evaluation
├── continuous-learning safeguards
├── simulation boundaries
├── external evidence comparison
├── OWASP and supply-chain controls
├── observability
├── rollback
├── complete documentation
└── strict independent validation
```
