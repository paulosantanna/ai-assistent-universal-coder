# Preparação para treinamento

Updated: 2026-11-01. Entry point: [README](README.md).

O objetivo provável é responder perguntas e executar tarefas futuras com evidências sobre Reversa. Conhecimento mutável e citações devem primeiro vir de recuperação atualizada. Fine-tuning pode ser útil para comportamento estável somente depois de um baseline e uma taxonomia de falhas demonstrar necessidade; memorizar o repositório não garante atualização nem citações corretas.

Os exemplos em `candidatos.jsonl` são rascunhos de instrução/resposta, produzidos a partir do código, com origem e `review.approved=false`. O usuário delegou a revisão ao assistente; veja [REVISAO-ASSISTENTE.md](REVISAO-ASSISTENTE.md). Essa revisão sequencial não equivale a avaliação humana independente. Os exemplos não são partições de treinamento e não devem ser carregados como gold. Antes de treinar:

1. Revisar direitos de cada família, inclusive conteúdo de terceiros e quaisquer dados reais; remover informações sensíveis. O filtro automatizado é limitado e não prova ausência de segredos.
2. Definir tarefas, modelo, hardware, orçamento e métricas; congelar baseline de recuperação e respostas com perguntas representativas e revisadas.
3. Criar exemplos variados com citações e casos de abstenção; agrupar por família de fonte/projeto antes de dividir treino, validação e teste. Detectar duplicações e contaminação entre grupos.
4. Avaliar recall de recuperação, correção, suporte das citações e abstenção, em separado; assinalar explicitamente se a revisão do teste não for humana e independente.
5. Se o baseline mostrar lacuna comportamental que RAG e instruções não resolvem, verificar a documentação oficial atual do modelo escolhido, treinar candidato isolado e comparar contra o mesmo modelo-base no conjunto reservado. Preservar rollback; não promover automaticamente.

O workspace possui `rag-graph-laya-mcp` com fluxo de aquisição e treino próprio: consultar seu README e contratos atuais antes de integrar. O SQLite deste pacote não foi registrado nesse serviço. Não existe modelo ajustado nem qualidade de fine-tuning medida nesta entrega.

Foi preparado [dataset-candidate](dataset-candidate/manifest.json) com 160/30/30 exemplos extrativos sintéticos de treino/validação/teste. A [verificação](dataset-candidate/verification.json) passou para hashes, rastreabilidade, grupos de caminhos e contratos de abstenção. Os grupos derivam do mesmo repositório, os enunciados são templáticos, e as respostas positivas copiam trechos: isso não estabelece generalização nem adequação para treinar um modelo de produção. Não se trata do formato completo exigido por `Training.verify_dataset` no serviço, que exige artefatos e auditoria para ambos os fluxos Laya e LLM. A GPU estava em uso intenso por outros processos e nenhum experimento foi iniciado.
