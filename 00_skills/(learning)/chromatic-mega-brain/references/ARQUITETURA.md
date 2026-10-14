# Hierarquia de memória do workspace

Updated: 2026-10-12
Fonte: IMG_2156–IMG_2157 e IMG_2301–IMG_2316; adaptada ao protocolo `.notebook/` vigente.

Memória hierárquica organiza conhecimento, não identidades de agentes. O único agente é `codenavi-agent`.

1. **Workspace:** `.notebook/MEMORY.md` e `LEARNING.md` guardam fatos/decisões e lições válidos para o workspace. INDEX aponta para o conhecimento relevante.
2. **Categoria/domínio:** quando houver trabalho real que justifique esse nível, suas notas guardam apenas conhecimento daquele domínio; deferem às regras e fatos comuns do pai.
3. **Projeto/tarefa:** seu `.notebook/` guarda o quarteto completo. PROGRESS é estado transitório verificável; HANDOFF é transferência operacional, com último estado verificado e próximo passo exato.

Leia do geral ao específico, somente o contexto aplicável. Não copie no filho o que já vive no pai. Um pai não guarda um fato específico de um único filho.

Promova uma decisão/lição somente depois de verificar sua generalidade e evidência. Mova o conhecimento para o escopo superior adequado, deixando ponteiro no filho; evite duplicação. Observações transitórias permanecem em PROGRESS; hipóteses não viram MEMORY ou LEARNING.

Nomes canônicos: HANDOFF.md, MEMORY.md, PROGRESS.md e LEARNING.md. Não crie variações por caixa/sufixo. Não bootstrap categorias inteiras sem descoberta real. Nunca armazene segredos, cookies, dados pessoais ou raciocínio privado.

No início confira a existência e coerência do quarteto da tarefa; ao fechar uma fase atualize PROGRESS. Na pausa/fronteira de sessão, HANDOFF aponta para a próxima ação executável e validação pendente. O protocolo normativo é `references/CODENAVI_CONTINUITY_STANDARD.md` no workspace.
