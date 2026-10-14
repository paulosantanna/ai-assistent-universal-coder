---
name: "fleet-mapping"
description: "Map authorized repository fleets by sigla with corporate, domain and repository knowledge, scoped glossaries, evidenced dependencies and an offline consolidated report. Use for mapear os repositorios da sigla, jornada do sistema, glossário do fleet or visão sistêmica. Do NOT use to fix one bug, provision infrastructure, mutate production or invent business rules."
license: "CC-BY-4.0"
metadata:
  author: "AEOS; photographic reference supplied by user"
  version: "1.1.0"
  owner_agent: "codenavi-agent"
---

# fleet-mapping

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.

## Workflow

1. Intake the complete authorized repository list, access, existing maps, output and coverage gates. Read human/domain inputs before interpreting code; unknown sigla meaning remains unknown.
2. Resolve terminology from most specific to broadest: repository → sigla → corporate. Read [knowledge layers](references/knowledge-layers.md) before creating notes or directories.
3. Map one repository at a time with codenavi; use [mapping playbook](references/mapping-playbook.md) and preserve the established [ten dimensions](references/dimensions.md). Record full path/line pointers, exact versions and observed/inferred/unknown distinctions.
4. For external owners, read [cross-sigla](references/cross-sigla.md). Discover candidates in bounded batches, map only consumed repositories, checkpoint depth work, reconcile both ends and keep unresolved/failed clones visible.
5. Record journeys from business trigger through entrypoint, layers, integration, data and result/error. Build bidirectional consumes/consumed-by graph pointers from verified interfaces, not names.
6. Distinguish repository default-branch snapshot from deployed runtime using [runtime evidence](references/runtime-evidence.md). Keep active slots/image tags in timestamped read-only reports; do not bake volatile values into canonical knowledge.
7. Fill the local [sigla templates](templates/sigla) and [notebook templates](templates/notebook) only with evidence. Use [report contract](references/relatorio.md) and report-design for consolidation, with exact complete totals and visible gaps.
8. Validate schema, cited values, coverage, redaction, local/offline report behavior and no unauthorized changes. Merge only inspected fields; never erase richer existing values with null.

## Inputs, outputs and stop

Inputs: authorized fleet, scoped human knowledge and accessible source. Outputs: per-repo maps, layered glossary, graph, offline report and unresolved evidence/access/asset gaps.
Root: 01_siglas/_comum, 01_siglas/SIGLA, 02_repositorios/SIGLA/REPO/.notebook, 04_visao_sistemica. Repositories are read-only mirrors unless the task authorizes edits.
Never spawn another identity. A sequential lens is not independent blind review. No assumptions about corporate org, deployment region or credentials from the sample photos.
Source: IMG_2732–IMG_2738; photographed version 1.1.0.

## Examples and failure handling

Example: “mapear a sigla X” → read supplied perfil/glossário, map authorized repos, reconcile interfaces and produce complete-coverage report; an external dependency maps only the consumed repository. Failure: inaccessible repo/runtime → visible gap, never invented content or production state.

## Retained resources

- Read [retained provenance](references/provenance.md) only for its matching mode; this entry and root governance take precedence.
- Read [retained usage-and-verification](references/usage-and-verification.md) only for its matching mode; this entry and root governance take precedence.
