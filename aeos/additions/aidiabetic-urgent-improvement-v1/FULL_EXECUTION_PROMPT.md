# Comando operacional único — AIDiabetic Urgent Improvement

Execute o playbook `aidiabetic-urgent-improvement-v1` contra
`E:\GitHub\aidiabetic-research`.

## Contrato de execução

1. Leia `playbooks/AIDIABETIC_URGENT_IMPROVEMENT_FULL.md`,
   `config/execution-policy.yaml`, `config/quality-gates.yaml`,
   `config/clinical-safety-policy.yaml` e `config/token-budget.yaml`.
2. Faça baseline somente leitura antes de qualquer mutação.
3. Confirme ou rejeite cada alegação do plano original com evidência de arquivo,
   comando, teste, telemetria ou documentação versionada.
4. Gere o mapa de jornadas críticas. Não invente login, chat, pagamento ou
   qualquer fluxo não observado.
5. Crie branch de trabalho ou snapshot de rollback antes da primeira mudança.
6. Execute as waves na ordem definida. Paralelize somente steps sem conflito de
   arquivo, contrato ou migração.
7. Cada skill deve operar em escopo único e entregar handoff estruturado.
8. Cada implementação deve passar pelo revisor Staff/Chief correspondente.
9. Use ferramentas determinísticas antes de usar LLM. Obedeça ao Token Context
   Governor e aos checkpoints de 40%, 70% e 85%.
10. Não exponha PHI, secrets, tokens, cookies ou dados clínicos em prompts,
    logs, caches, traces ou artefatos.
11. Não habilite auto-merge, auto-deploy, shell irrestrito ou bypass do Tool
    Router.
12. Para mudanças de alto risco, pare em `WAITING_APPROVAL` antes da mutação.
13. Rode testes focados após cada patch e suíte ampliada no fim de cada wave.
14. Gere ADR para decisões arquiteturais significativas.
15. Gere evidências com SHA-256, comandos, exit code, timestamps, diff stat,
    testes, riscos e rollback.
16. O Judge determinístico tem precedência. O Judge LLM pode explicar, mas não
    substituir um gate falho.
17. Máximo de três ciclos de retrabalho por gate. Depois disso, marque `BLOCKED`
    com causa raiz e ação humana necessária.
18. Finalize apenas com `PASS`, `REWORK_REQUIRED` ou `BLOCKED`, acompanhado do
    relatório integral de evidências.

## Saídas obrigatórias

- baseline do repositório;
- matriz de alegações confirmadas/rejeitadas;
- matriz de jornadas e riscos;
- plano final reestimado;
- árvore de arquivos alterados;
- ADRs;
- testes e resultados;
- benchmarks antes/depois;
- relatório de segurança e privacidade;
- relatório de observabilidade;
- relatório de rollback;
- scorecard por gate;
- verdict final do Judge.
