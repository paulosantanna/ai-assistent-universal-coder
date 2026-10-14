<!-- Package: 00_skills/(development)/ai-continuous-training-maintainer; relative command/resource examples resolve from that package or workspace root. -->

## 21. Examples

### Exemplo 1: Verificar CVEs
```
Usuário: "verificar CVEs no continuous training"
→ Phase 0: Intent = cve
→ Phase 1: Baseline (pip-audit, trivy fs src/)
→ Phase 2: Subagent 1 (CVE-Resolver) dispatch
→ Phase 3: Consolidar achados
→ Phase 7: Persistir conhecimento
→ Handback: relatório de CVEs encontradas
```

### Exemplo 2: Atualização completa (score 10.0 na 1ª iteração)
```
Usuário: "atualizar o treino contínuo com melhores práticas"
→ Phase 0: Intent = update, recursion_count = 0
→ Phase 1: Baseline completo
→ Phase 2-3: Subagentes 1-5 em paralelo
→ Phase 4-5: Alterações graduais
→ Phase 6: Verificação pós
→ Phase 6.5: Quality-Judge
    → G1-G7: ALL PASS ✅
    → Score: 10.0/10.0 ✅
    → COMPLETED
→ Phase 7-8: Conhecimento e handback
```

### Exemplo 3: Atualização completa (recursão necessária)
```
Usuário: "atualizar o treino contínuo com melhores práticas"

Iteração 1:
→ Phase 0-6: Alterações aplicadas, testes passam
→ Phase 6.5: Quality-Judge → Score: 7.5/10.0
    → Gap 1: CVE crítica no torch não resolvida
    → Gap 2: Um arquivo não segue SRP (SOLID)
→ ROLLBACK iteração 1
→ recursion_count = 1

Iteração 2:
→ Phase 2-3: Subagentes focam apenas nos gaps
    → CVE-Resolver: torch atualizado
    → Code-Quality: refatora SRP no arquivo
→ Phase 4-6: Alterações graduais
→ Phase 6.5: Quality-Judge → Score: 9.0/10.0
    → Gap: mypy aponta 2 type-ignores desnecessários
→ ROLLBACK iteração 2
→ recursion_count = 2

Iteração 3:
→ Phase 2: Planejamento focado nos type-ignores
→ Phase 4-6: Correção
→ Phase 6.5: Quality-Judge → Score: 10.0/10.0 ✅
    → COMPLETED
→ Phase 7-8: Conhecimento e handback
```

### Exemplo 4: MAX_RECURSION_REACHED
```
Usuário: "corrigir CVEs no continuous training"
→ Phase 0-6: CVE-Resolver atua, 3 CVEs corrigidas
→ Phase 6.5: Quality-Judge → Score: 8.5/10.0
    → Gap: Uma CVE não tem patch disponível
→ Iteração 2-3: Mesmo gap permanece (sem patch upstream)
→ MAX_RECURSION_REACHED (3 iterações)
→ Status: MAX_RECURSION_REACHED
→ Handback: "3/4 CVEs resolvidas. CVE-2026-XXXX sem patch.
   Score final: 8.5. Risco aceito documentado."
```

### Exemplo 5: Rollback
```
Usuário: "reverter última alteração no continuous training"
→ Localizar snapshot em memory/EXECUTIONS.md
→ Restaurar arquivos do snapshot
→ Verificar integridade (SHA-256)
→ Testes de regressão
→ Relatório de rollback
```

---
