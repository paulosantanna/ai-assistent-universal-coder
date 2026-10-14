<!-- Package: 00_skills/(development)/ai-continuous-training-maintainer; relative command/resource examples resolve from that package or workspace root. -->

## 18. Memory Behavior

### Estrutura
```
memory/
├── EXECUTIONS.md    — registro de cada execução (data, comando, resultados)
├── LESSONS.md       — lições extraídas (positivas e negativas)
├── FAILURES.md      — falhas e incidentes (causa, impacto, correção)
└── PATTERNS.md      — padrões identificados (arquitetura, código, segurança)
```

### Regras
- Toda execução é registrada em EXECUTIONS.md
- Toda falha é registrada em FAILURES.md com causa raiz
- Padrões são extraídos apenas após 2+ ocorrências
- Lições são candidatas até revisão

### Snapshot de Rollback
Antes de qualquer alteração:
- SHA-256 do conteúdo original de cada arquivo
- Cópia do estado atual em `memory/rollback/<execution_id>/<file>.bak`
- Referência no EXECUTIONS.md

---
