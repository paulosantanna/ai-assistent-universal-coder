# AEOS Documentation Mapper

## Overview

Complete enterprise-grade project documentation generator. Maps all 10 architectural layers of any repository, generates interactive HTML with clickable Mermaid diagrams, PDF documentation, data dictionaries, stakeholder-specific views, and actionable improvement plans.

## Features

- **10-Layer Analysis** — Infrastructure, Data, Backend, Frontend, Business Logic, Integrations, Security, DevOps, Observability, Governance
- **Data Dictionary** — MongoDB collections, ChromaDB collections, SQL tables fully documented
- **Stakeholder Views** — Business (non-technical), Developer (technical), Director (executive)
- **14+ Mermaid Diagrams** — Architecture, ERD, Data Flow, Deployment, Sequence, Security, etc.
- **Interactive HTML** — Clickable entities that expand to show connections, full-text search
- **PDF Generation** — Full documentation + improvement plan
- **CHIEF STAFF Evaluation** — Independent JUDGE subagent with 10-criterion rubric, only 10.0/10 passes
- **Recursive Improvement** — Sub-10.0/10 scores trigger full recursion (max 10 iterations)

## Usage

```bash
# From AEOS:
# "Mapeie o projeto <path>"
# "Documentar sistema completo"
# "Generate full documentation for <repo>"

# Or directly with scripts:
python scripts/analyze_layers.py /path/to/repo ./output
python scripts/generate_dictionary.py ./output/data ./output/data
node scripts/generate_diagrams.js ./output/diagrams
node scripts/generate_html.js ./output/html ./output/diagrams
python scripts/generate_pdf.py ./output/pdf ./output/html
```

## Output Structure

```
Desktop/documentação_v1/
├── html/documentacao.html
├── pdf/
│   ├── documentacao_completa.pdf
│   └── plano_de_melhorias.pdf
├── diagrams/{src,svg,png}/
├── data/
├── views/
├── evidence/
├── improvement/
├── MANIFEST.json
└── evaluation/
```

## Architecture

- **ROOT Agent**: Orchestrates analysis, consolidates output
- **PARENT Agents** (10×): One per layer, parallel analysis
- **CHILD Agents**: Atomic analysis tasks
- **JUDGE Agent** (CHIEF STAFF): Independent evaluation, 10-criterion rubric

## Requirements

- Node.js 18+
- Python 3.10+
- `@mermaid-js/mermaid-cli` (for diagram export)
- Playwright / WeasyPrint / pdfkit (for PDF generation)
