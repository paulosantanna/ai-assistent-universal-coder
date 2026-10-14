<!-- Package: 00_skills/(development)/ai-continuous-training-maintainer; relative command/resource examples resolve from that package or workspace root. -->

## 13. Subagent Policy

### Criação de Subagentes

Cada subagente deve receber:
- Escopo exato (arquivos, diretórios)
- Handoff com allowed/forbidden paths
- Ferramentas permitidas
- Output schema esperado
- Stop conditions

### Handoff to Subagent
```yaml
handoff_id: <uuid>
source_role: PARENT (ai-continuous-training-maintainer)
target_role: CHILD
objective: <descrição>
allowed_paths: <caminhos>
forbidden_paths: <caminhos>
required_evidence: <evidências esperadas>
completion_criteria: <critérios>
stop_conditions: <condições de parada>
```

### Handback from Subagent
```yaml
handoff_id: <uuid>
status: completed | blocked | failed | scope_change_required
findings: <achados>
evidence_refs: <referências>
risks: <riscos>
recommendations: <recomendações>
```

---
