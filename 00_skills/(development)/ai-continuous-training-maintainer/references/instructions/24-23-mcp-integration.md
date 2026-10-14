<!-- Package: 00_skills/(development)/ai-continuous-training-maintainer; relative command/resource examples resolve from that package or workspace root. -->

## 23. MCP Integration

Esta skill se conecta ao MCP para:

- **knowledge-update** — atualizar base de conhecimento com melhores práticas de treino contínuo
- **cve-resolver** — resolver CVEs no ecossistema Python de ML
- **code-snapshot** — criar snapshots para rollback
- **subagent-orchestrator** — coordenar subagentes especializados

```yaml
mcp_connections:
  - mcp_id: filesystem-readonly
    purpose: Leitura de arquivos do repositório
  - mcp_id: filesystem-write-sandbox
    purpose: Escrita de diffs e snapshots
  - mcp_id: git-controlled
    purpose: Branch, diff, commit controlado
  - mcp_id: test-runner-controlled
    purpose: Execução de testes com escopo e timeout
