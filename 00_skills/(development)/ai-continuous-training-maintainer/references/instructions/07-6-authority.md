<!-- Package: 00_skills/(development)/ai-continuous-training-maintainer; relative command/resource examples resolve from that package or workspace root. -->

## 6. Authority

### Allowed
- Ler qualquer arquivo no escopo
- Executar comandos de análise (pip-audit, trivy, bandit, mypy, ruff, pytest)
- Criar branches para alterações (git-controlled)
- Modificar arquivos dentro do escopo
- Executar testes do pipeline de treino contínuo
- Criar snapshots de rollback
- Persistir conhecimento em `memory/` e `knowledge/`

### Forbidden
- Modificar arquivos fora do escopo
- Deploy em produção
- Acessar ou persistir secrets
- Alterar arquitetura global sem ROOT
- Promover conhecimento sem validação
- Executar alterações destrutivas sem aprovação humana

---
