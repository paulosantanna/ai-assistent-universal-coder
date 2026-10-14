<!-- Package: 00_skills/(mapping)/documentation-mapper; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# AEOS Documentation Mapper

> **Complete project mapping, 10-layer analysis, data dictionary, business/developer/director views, interactive HTML diagrams, and PDF documentation with improvement plans.**

---

```yaml
skill:
  name: AEOS Documentation Mapper
  slug: documentation-mapper
  version: 1.0.0
  description: >
    Mapeia todas as camadas de um projeto de T.I — infraestrutura, dados,
    backend, frontend, integrações, segurança, DevOps, observabilidade e
    governança. Gera dicionário de dados, visões de negócio/desenvolvedor/
    diretoria, diagramas Mermaid interativos em HTML, PDFs completos e
    plano de melhorias. Avaliado por subagent CHIEF STAFF com nota >= 10/10.
  category: DOCUMENTATION
  architecture_level: 3
  risk_level: HIGH
  activation:
    - requests to map, document, diagram or analyze a full project
    - "mapear projeto"
    - "documentar sistema"
    - "criar diagramas do projeto"
    - "análise completa de camadas"
    - "documentação técnica"
    - "mapeamento de arquitetura"
    - "project documentation"
    - "system mapping"
    - "architecture diagram"
    - "documentar tudo"
  exclusions:
    - single-file documentation requests
    - simple README generation
    - unrelated code generation
  inputs:
    - target repository path or URL
    - optional project metadata
    - optional MCP connection config for diagram research
  outputs:
    - interactive HTML documentation with clickable diagrams
    - PDF full documentation
    - PDF improvement plan
    - data dictionary
    - 10-layer architecture analysis
    - business/developer/director views
    - all Mermaid diagram source files
    - evaluation report with CHIEF STAFF verdict
  tools:
    - Node.js
    - Python
    - filesystem
    - MCP client (for diagram research)
    - mermaid-cli (mmdc) or @mermaid-js/mermaid-cli
  memory: true
  human_approval: conditional
  maintainer: AEOS
```

---
