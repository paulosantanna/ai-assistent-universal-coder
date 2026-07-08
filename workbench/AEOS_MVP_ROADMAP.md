# AEOS MVP Roadmap — v1.0.0

## Fase 0: Fundação (MVP Atual)

**Status:** ✅ CONCLUÍDO

### Entregas
- [x] AEOS_CONSTITUTION.md
- [x] AEOS_KERNEL.md
- [x] AEOS_AGENT_CONTRACT.md
- [x] AEOS_SKILL_CONTRACT.md
- [x] AEOS_PLAYBOOK_CONTRACT.md
- [x] AEOS_POLICY_ENGINE.md
- [x] AEOS_PERMISSION_MODEL.md
- [x] AEOS_MEMORY_MODEL.md
- [x] AEOS_JUDGE_LAYER.md
- [x] AEOS_SECURITY_MODEL.md
- [x] AEOS_ECOSYSTEM_SCHEMA.md
- [x] AEOS_MVP_ROADMAP.md
- [x] aeos.ecosystem.yaml
- [x] Module directory structure
- [x] MVP Scanner (Python)
- [x] Stack Detector
- [x] Ecosystem Map Generator
- [x] Risk Report Generator
- [x] Playbook Recommender
- [x] Skill Generator
- [x] Judge Report Generator
- [x] Evidence Ledger
- [x] Finalization Blocking

## Fase 1: Scanner e Stack Detection

**Status:** ⬜ NÃO INICIADO

### Objetivos
- [ ] Scanner recursivo de projeto/repositório.
- [ ] Detecção de linguagens (Java, Python, TypeScript, Go, Rust).
- [ ] Detecção de frameworks (Spring, FastAPI, React, Next.js).
- [ ] Detecção de build tools (Maven, Gradle, npm, pip, poetry).
- [ ] Detecção de Docker/Compose/Kubernetes.
- [ ] Mapa de dependências externas.
- [ ] Arquivo ecosystem-map.md.

### Critérios de Aceite
- Scanner roda em qualquer diretório.
- Detecta stacks com confidence score.
- Gera ecosystem-map.md.
- Exporta em YAML e JSON.

## Fase 2: Risk Mapping

**Status:** ⬜ NÃO INICIADO

### Objetivos
- [ ] Análise de dependências obsoletas.
- [ ] Detecção de CVEs (via API pública).
- [ ] Análise de débito técnico.
- [ ] Análise de cobertura de testes.
- [ ] Análise de segurança de código.
- [ ] Risk report em markdown.

### Critérios de Aceite
- Riscos classificados por severidade.
- Recomendações acionáveis.
- Risk-report.md gerado.

## Fase 3: Skill Generation

**Status:** ⬜ NÃO INICIADO

### Objetivos
- [ ] Skill Factory com templates por stack.
- [ ] Geração automática de skills.
- [ ] Registro no Skill Registry.
- [ ] Avaliação de skills (skill evaluator).
- [ ] Skills para Java/Spring, Python/FastAPI, React/TypeScript.

### Critérios de Aceite
- Skills geradas baseadas no stack detectado.
- Skills registradas e disponíveis.
- Skills passam por avaliação automática.

## Fase 4: Playbook Engine

**Status:** ⬜ NÃO INICIADO

### Objetivos
- [ ] Playbook Registry.
- [ ] Recomendação automática de playbooks.
- [ ] Executor de playbooks.
- [ ] Rollback automático.
- [ ] Relatórios de execução.

### Critérios de Aceite
- Playbooks recomendados baseados no scan.
- Playbooks executáveis com aprovação.
- Rollback funcional.

## Fase 5: Judge Layer

**Status:** ⬜ NÃO INICIADO

### Objetivos
- [ ] Judge Engine com scoring.
- [ ] Condições de bloqueio.
- [ ] Judge Report em markdown.
- [ ] Recurso e reavaliação.
- [ ] Integração com Evidence Ledger.

### Critérios de Aceite
- Judge aprova/rejeita/bloqueia.
- Score mínimo exigido (7.0).
- Bloqueio sem evidências.
- Judge ≠ implementador.

## Fase 6: Observabilidade

**Status:** ⬜ NÃO INICIADO

### Objetivos
- [ ] Logs estruturados (JSON).
- [ ] Tracing distribuído.
- [ ] Métricas (token usage, tool calls).
- [ ] Execution reports.
- [ ] Dashboard CLI.

### Critérios de Aceite
- Logs imutáveis.
- Métricas coletadas.
- Relatórios de execução.

## Fase 7: Portabilidade

**Status:** ⬜ NÃO INICIADO

### Objetivos
- [ ] Docker image.
- [ ] Devcontainer spec.
- [ ] CI templates (GitHub Actions, GitLab CI).
- [ ] Windows/Linux/macOS test matrix.
- [ ] WSL support.

### Critérios de Aceite
- Roda em 3+ ambientes.
- Docker compose up funcional.
- Devcontainer one-click setup.

## Fase 8: Multi-Ecossistema

**Status:** ⬜ NÃO INICIADO

### Objetivos
- [ ] Java/Spring Boot enterprise.
- [ ] Python/FastAPI + AI/RAG.
- [ ] Fullstack TypeScript/Next.js.
- [ ] Mobile (React Native).
- [ ] Infra (Terraform, Kubernetes).

### Critérios de Aceite
- Scan completo de cada ecossistema.
- Skills específicas por ecossistema.
- Playbooks específicos por ecossistema.

## Fase 9: Production Readiness

**Status:** ⬜ NÃO INICIADO

### Objetivos
- [ ] Performance optimization.
- [ ] Security hardening.
- [ ] Documentation complete.
- [ ] Community guidelines.
- [ ] Release automation.

### Critérios de Aceite
- Testes de performance.
- Audit report limpo.
- Documentação completa.
- CI/CD pipeline.
