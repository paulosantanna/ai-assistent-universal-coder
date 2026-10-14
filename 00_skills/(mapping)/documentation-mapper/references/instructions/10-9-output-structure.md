<!-- Package: 00_skills/(mapping)/documentation-mapper; relative command/resource examples resolve from that package or workspace root. -->

## 9. Output Structure

All output saved to `Desktop/documentação_v1/`:

```
Desktop/documentação_v1/
├── html/
│   └── documentacao.html              ← Interactive HTML (self-contained)
├── pdf/
│   ├── documentacao_completa.pdf       ← Full documentation
│   └── plano_de_melhorias.pdf          ← Improvement plan only
├── diagrams/
│   ├── src/                            ← Mermaid .mmd source files
│   ├── svg/                            ← SVG exports
│   └── png/                            ← PNG exports
├── data/
│   ├── dicionario_de_dados.yaml         ← Data dictionary
│   ├── analise_camadas.yaml            ← 10-layer analysis
│   └── metricas.yaml                   ← Project metrics
├── views/
│   ├── visao_negocio.md
│   ├── visao_desenvolvedor.md
│   └── visao_diretoria.md
├── evidence/
│   ├── file_index.json                 ← All files referenced
│   └── evidence_log.jsonl              ← Evidence trace for each claim
├── improvement/
│   ├── plano_de_melhorias.md
│   └── roadmap.mmd
├── MANIFEST.json                       ← Integrity manifest
└── evaluation/
    ├── rubric.md
    ├── evaluation_iterations.md         ← All judge iterations
    └── verdict_final.md                ← Final 10/10 verdict
```

---
