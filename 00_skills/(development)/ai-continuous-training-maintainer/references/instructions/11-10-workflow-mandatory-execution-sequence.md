<!-- Package: 00_skills/(development)/ai-continuous-training-maintainer; relative command/resource examples resolve from that package or workspace root. -->

## 10. Workflow — Mandatory Execution Sequence

### Phase 0: Intent Resolution
```
Receber comando do usuário
→ Classificar intenção (update | cve | sast | deps | rollback | health)
→ Determinar escopo
→ Verificar se ativa a skill
→ Registrar execução em memory/EXECUTIONS.md
```

### Phase 1: Baseline (sempre executado)
```
1. Fazer snapshot do estado atual dos arquivos no escopo
   - git diff HEAD~1 -- src/main.py src/continual/ (se em branch)
   - SHA-256 de cada arquivo alvo
   - Salvar em memory/EXECUTIONS.md
2. Executar análise atual:
   - pip-audit --format json > baseline_cves.json
   - bandit -r src/continual/ -f json > baseline_bandit.json
   - ruff check src/continual/ src/main.py --output-format json > baseline_ruff.json
   - mypy src/continual/ src/main.py > baseline_mypy.txt
   - pytest tests/ (focados em continual) > baseline_tests.txt
3. Consolidar relatório baseline
4. Armazenar em memory/FAILURES.md (achados existentes)
```

### Phase 2: Planning
```
1. Com base no baseline e no comando do usuário, criar plano:
   - Quais arquivos modificar
   - Qual a ordem das alterações
   - Quais subagentes engajar
   - Quais riscos existem
   - Plano de rollback
2. Se alteração destrutiva → WAITING_APPROVAL
3. Registrar plano em memory/EXECUTIONS.md
```

### Phase 3: Subagent Dispatch (quando aplicável)
```
DISPATCH paralelo de subagentes especializados:

┌──────────────────────────────────────────────────────────────┐
│                    PARENT (esta skill)                        │
│  Coordena, revisa evidências, persiste conhecimento,         │
│  decide próximo passo                                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  SUBAGENT 1: CVE-Resolver                                    │
│  ─────────────                                              │
│  Escopo: Analisar CVEs em dependências do pyproject.toml    │
│  Fontes: NVD, OSV.dev, GitHub Advisory, PyPA, Trivy DB      │
│  Ação: pip-audit, trivy fs, sugerir atualizações seguras    │
│  Output: cve_report.json (achados + correções propostas)    │
│                                                              │
│  SUBAGENT 2: SAST-Analyzer                                   │
│  ─────────────                                              │
│  Escopo: src/continual/ e src/main.py                        │
│  Ferramentas: bandit, ruff, mypy, semgrep                    │
│  Regras: OWASP Top 10, OWASP AI, SOLID, boas práticas Python│
│  Output: sast_report.json (achados + correções propostas)    │
│                                                              │
│  SUBAGENT 3: Lib-Updater                                     │
│  ─────────────                                              │
│  Escopo: pyproject.toml, requirements*.txt                   │
│  Ação: Verificar versões的最新, testar compatibilidade       │
│  Regra: Atualizar gradualmente, uma dep por vez              │
│  Output: lib_update_plan.json (deps a alterar, risco)        │
│                                                              │
│  SUBAGENT 4: Code-Quality                                    │
│  ─────────────                                              │
│  Escopo: src/main.py, src/continual/*.py                     │
│  Padrões: SOLID, OWASP AI, arquitetura atual, sem refactor   │
│  Ação: Sugerir melhorias focadas sem mudar arquitetura       │
│  Output: quality_report.json (sugestões + diff proposto)     │
│                                                              │
│  SUBAGENT 5: Rollback-Snapshot                               │
│  ─────────────                                              │
│  Escopo: Todo arquivo que será modificado                    │
│  Ação: snapshot SHA-256, git diff, backup em memory/        │
│  Output: rollback_snapshot.json (caminho + hash + conteúdo)  │
│                                                              │
│  SUBAGENT 6: Quality-Judge [INDEPENDENTE — NÃO IMPLEMENTA]   │
│  ─────────────                                              │
│  Escopo: Avaliar resultado final contra rubric 0.0-10.0     │
│  Regra: NUNCA modifica arquivos. NUNCA implementa.          │
│  Ação:                                                        │
│    1. Verificar deterministic gates (todos PASS/FAIL)       │
│    2. Aplicar rubric de scoring com evidência para cada item│
│    3. Produzir score final (0.0-10.0)                       │
│    4. Se score < 10.0: listar exatamente o que falta        │
│  Output: score_report.json (score + evidência + gaps)       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Phase 4: Review & Consolidation
```
1. Revisar outputs de cada subagente
2. Detectar conflitos entre subagentes
3. Priorizar alterações (CVEs críticas primeiro)
4. Consolidar em um plano de alteração unificado
5. Registrar em memory/EXECUTIONS.md
```

### Phase 5: Execution (alterações graduais)
```
PARA CADA alteração no plano (uma por vez):
  1. Aplicar mudança
  2. Rodar testes focados (pytest tests/ -m "not slow")
  3. Rodar ruff check no arquivo alterado
  4. Rodar mypy no arquivo alterado
  5. Se falhar → reverter a mudança, registrar falha, tentar abordagem alternativa
  6. Se passar → commit local, próximo passo
```

### Phase 6: Post-Execution Verification
```
1. Rodar bateria completa de testes:
   - pytest tests/ (todo o test suite)
   - pip-audit (verificar se CVEs foram resolvidas)
   - bandit -r src/continual/ src/main.py
   - ruff check src/continual/ src/main.py
   - mypy src/continual/ src/main.py
2. Comparar com baseline
3. Se regressão → ROLLBACK automático
```

### Phase 6.5: Recursive Evaluation Gate

```
┌──────────────────────────────────────────────────────────┐
│                 RECURSIVE EVALUATION GATE                 │
│                                                          │
│  Phase 6 done → Dispatch SUBAGENT 6 (Quality-Judge)     │
│       ↓                                                  │
│  Quality-Judge avalia (NUNCA implementa):                │
│   1. Deterministic Gates (PASS/FAIL obrigatório)         │
│   2. Score Rubric (0.0-10.0 com evidência)               │
│       ↓                                                  │
│  ┌───── RESULT ──────────────────────────────────┐      │
│  │                                               │      │
│  │  Score == 10.0  ──────────→ Phase 7 ✅       │      │
│  │                                               │      │
│  │  Score < 10.0                                 │      │
│  │    ├─ recursion_count < MAX_RECURSION (3)     │      │
│  │    │   → Registrar gaps no FAILURES.md        │      │
│  │    │   → ROLLBACK alterações desta iteração   │      │
│  │    │   → recursion_count++                    │      │
│  │    │   → Voltar ao Phase 2 (Planning)         │      │
│  │    │     com gaps como input prioritário      │      │
│  │    │                                          │      │
│  │    └─ recursion_count >= MAX_RECURSION         │      │
│  │        → MAX_RECURSION_REACHED                │      │
│  │        → Relatório do que falta para 10.0     │      │
│  │        → Phase 7 parcial                      │      │
│  └───────────────────────────────────────────────┘      │
└──────────────────────────────────────────────────────────┘
```

#### Deterministic Gates (PASS/FAIL — TODOS devem passar)
| Gate | Ferramenta | Critério |
|------|-----------|----------|
| G1 | pytest | Todos os testes passam (exit 0) |
| G2 | pip-audit | Nenhuma CVE critical/high não resolvida |
| G3 | bandit | Nenhum achado CRITICAL/HIGH |
| G4 | ruff | Nenhum erro de lint |
| G5 | mypy | Nenhum erro de tipo |
| G6 | SHA-256 | Snapshot de rollback existe e hashes conferem |
| G7 | Diff scope | Diff está dentro do escopo autorizado |

Se qualquer gate falhar → `FAILED_VERIFICATION` (não entra no scoring).

#### Score Rubric (0.0-10.0)
O Quality-Judge aplica CADA item com evidência obrigatória:

| # | Critério | Max | Evidência Exigida |
|---|----------|-----|-------------------|
| 1 | Test coverage mantido ou melhorado | 1.5 | pytest --cov-report= |
| 2 | CVEs critical/high resolvidas | 1.5 | pip-audit diff pré/pós |
| 3 | SAST findings critical/high resolvidos | 1.5 | bandit diff pré/pós |
| 4 | Código segue SOLID (SRP, OCP, DIP) | 1.0 | Análise estrutural + exemplos |
| 5 | Código segue OWASP AI (input validation, sanitização) | 1.0 | Revisão de segurança |
| 6 | Dependências atualizadas sem breaking changes | 1.0 | Diff pyproject.toml |
| 7 | Conhecimento persistido (memory/ + knowledge/) | 0.5 | Arquivos de memória atualizados |
| 8 | Código simples, sem complexidade desnecessária | 1.0 | Análise de complexidade ciclomática |
| 9 | Nenhum bug novo introduzido | 1.0 | Testes de regressão baseline vs final |
| **Total** | | **10.0** | |

**Regras do Score:**
- Score sem evidência = 0 (não pode ser inferido)
- Score de critério não aplicável = N/A (não conta no total)
- N/A máximo permitido: 2 itens (acima disso → REWORK_REQUIRED)
- Se deterministic gate falhar → score = 0.0 independente do rubric

#### Recursion Logic
```
MAX_RECURSION = 3 (default, configurável pelo usuário)
recursion_count = 0 (reset a cada nova execução)

if score >= 10.0:
    → COMPLETED
    → Phase 7 (Knowledge Persistence)
    → Phase 8 (Handback)

if score < 10.0 AND recursion_count < MAX_RECURSION:
    → Registrar gaps (o que falta para 10.0) em FAILURES.md
    → ROLLBACK alterações desta iteração (restaurar snapshot)
    → recursion_count++
    → Log em EXECUTIONS.md: "Iteração {n}: score {s}, gaps: {gaps}"
    → Voltar ao Phase 2 com gaps como input prioritário
    → Subagentes focam apenas nos gaps identificados

if score < 10.0 AND recursion_count >= MAX_RECURSION:
    → Status: MAX_RECURSION_REACHED
    → Relatório consolidado de todas as iterações
    → Scores parciais de cada iteração
    → Gaps restantes documentados
    → Phase 7 parcial (apenas conhecimento validado)
    → Handback com limitações explicitas
```

### Phase 7: Knowledge Persistence
```
1. Extrair lições de TODAS as iterações:
   - O que funcionou → POSITIVE_KNOWLEDGE.md
   - O que falhou → NEGATIVE_KNOWLEDGE.md
   - Padrões identificados → memory/PATTERNS.md
   - Gaps encontrados pelo Quality-Judge → FAILURES.md
2. Registrar execução completa (com todas iterações) em memory/EXECUTIONS.md
3. Se elegível, preparar candidato a conhecimento para promoção
```

### Phase 8: Final Handback
```
1. Relatório consolidado (multi-iteração):
   - Baseline vs Resultado Final
   - Iterações realizadas: N de MAX_RECURSION
   - Scores parciais: [s1, s2, s3, ...]
   - Score final: X.X / 10.0
   - CVEs encontradas/resolvidas
   - Achados SAST pré/pós (cada iteração)
   - Dependências atualizadas
   - Links para snapshots de rollback (cada iteração)
   - Diff completo (última iteração)
   - Testes passados/falhos
   - Gaps restantes (se MAX_RECURSION_REACHED)
   - Lições aprendidas
2. Status final: COMPLETED | MAX_RECURSION_REACHED | BLOCKED
3. Recomendação de próximo passo
```

---
