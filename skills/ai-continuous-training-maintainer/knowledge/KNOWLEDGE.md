# KNOWLEDGE.md — AI Continuous Training Knowledge Base

## Propósito

Base de conhecimento validado sobre manutenção de pipeline de treino contínuo de IA.

## Conhecimentos

<!-- Adicionado e validado pela skill a cada execução -->

### 2026-07-11

- **Snapshot antes de alterar**: Sempre criar snapshot SHA-256 antes de modificar arquivos. Rollback depende disso.
- **Alterações graduais**: Uma mudança por vez. Aplicar, testar, verificar. Se falhar, reverter.
- **CVEs multi-fonte**: pip-audit captura PyPA. Trivy captura OS + filesystem. GitHub Advisory captura GHSA IDs.
- **SOLID no treino contínuo**: Single Responsibility em cada módulo (daemon, builder, scorer, etc). Open/Closed via estratégias de replay injetadas.
- **OWASP AI**: Validar input de dados de treino contra injection. Sanitizar antes de concatenar em prompts/instructions.

## Estado

<!-- Atualizado automaticamente -->
- **Última revisão**: 2026-07-11
- **Entradas validadas**: 4
- **Entradas candidatas**: 0
