# Prompt — Implement AEOS Major Pack v0.8 → v1.0

Leia todos os arquivos deste pacote e implemente o AEOS v0.8 a v1.0 como overlay incremental.

Objetivo:
Evoluir o AEOS para um Workbench AI-First governado com execução paralela segura, cache de evidência, approval avançado, observabilidade, marketplace local de packs, hardening de segurança e readiness v1.0.

Prioridade de implementação:

1. v0.8 Parallel Execution
- Task DAG
- read_set/write_set
- ConflictDetector
- DeterministicParallelScheduler
- parallel-execution-smoke-test
- Judge rules para conflitos

2. v0.9 Evidence Cache + Observability + Approval
- EvidenceCacheKeyBuilder
- EvidenceCacheStore
- cache invalidation
- AdvancedApproval
- approval expiration
- observability logs/traces/metrics/timeline
- observability-report playbook

3. v0.95 Security + Marketplace
- threat model
- security-hardening-audit
- pack marketplace quarantine/staging/active
- pack verify/promote/activate
- package quarantine report
- trust policy

4. v1.0 Readiness
- v1-readiness-audit
- v1 release gates
- stable CLI surface
- docs/runbooks completeness
- negative tests for all critical blocking rules

Regras obrigatórias:
- Não implementar auto-merge.
- Não implementar auto-deploy.
- Não habilitar critical MCPs por padrão.
- Não persistir secrets.
- Não permitir shell irrestrito.
- Não permitir wildcard approval.
- Não aceitar evidência cacheada sem chave forte.
- Não executar paralelo sem read/write sets.
- Não importar pack diretamente para active.
- Não permitir Judge LLM sobrescrever falha determinística.

Ao final, gere:
1. árvore de arquivos alterada;
2. comandos implementados;
3. exemplos de execução;
4. relatórios gerados;
5. testes criados;
6. riscos restantes;
7. readiness score;
8. Judge final.
