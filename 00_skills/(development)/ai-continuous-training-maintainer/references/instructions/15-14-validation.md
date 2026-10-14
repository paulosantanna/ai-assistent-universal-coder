<!-- Package: 00_skills/(development)/ai-continuous-training-maintainer; relative command/resource examples resolve from that package or workspace root. -->

## 14. Validation

### Pre-execution
- Todos os arquivos alvo existem?
- Git disponível?
- Ambiente Python ativo?
- Ferramentas de análise disponíveis?

### During Execution
- Cada alteração compila (ruff + mypy)?
- Testes focados passam?
- Nenhuma regressão introduzida?

### Post-execution
- Bateria completa de testes passa?
- CVEs do baseline foram resolvidas?
- Nenhum novo achado SAST crítico/alto?
- Diff está dentro do escopo autorizado?

---
