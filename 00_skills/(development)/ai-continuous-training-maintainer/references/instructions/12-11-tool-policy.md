<!-- Package: 00_skills/(development)/ai-continuous-training-maintainer; relative command/resource examples resolve from that package or workspace root. -->

## 11. Tool Policy

### Filesystem
- `filesystem-readonly` — leitura de arquivos no escopo
- `filesystem-write-sandbox` — escrita controlada

### Git
- `git-readonly` — diff, log, status, snapshot
- `git-controlled` — branch, commit (apenas no escopo)

### Test Runner
- `test-runner-controlled` — pytest com timeout e escopo

### Security Scanning
- `pip-audit` — CVE scanning (executado via shell)
- `bandit` — SAST Python (executado via shell)
- `trivy` — container/filesystem scan (se disponível)
- `ruff` — linter (executado via shell)

---
