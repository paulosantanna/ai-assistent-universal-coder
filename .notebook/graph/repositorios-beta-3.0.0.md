# Repositórios — mapeamento beta 3.0.0

Updated: 2026-10-27
Entry point: `07_mapeamentos/mapeamento-beta-3.0.0/README.md`.

- Escopo: todos os 17 diretórios imediatos de `02_repositorios`; inclui ncm, ausente da lista de 16 do beta 2. São 16 diretórios com Git próprio e um pacote sem Git (`dark-videos-mining-fix`). FreePDFReader possui Git, mas HEAD não resolvido no snapshot.
- Fontes: `inventory.json` guarda SHA-256, fingerprint, estado Git local e exclusões; `evidencias.json` liga fatos a arquivo/linha/hash; `mapa.json`, `matriz-conhecimento.csv` e `repositorios/*.md` contêm conhecimento por dimensão.
- Entrada para reutilização: `CONHECIMENTO.md`; mudanças de interpretação e comparação histórica em `ATUALIZACOES.md`/`diferencas.json`. Beta 2 não tem baseline completo com hashes; diff de conteúdo comprovável usa os locadores hashados do beta 1, com escopos de inventário distintos.
- Distinções verificadas em fonte: AIHealthResearch implementa candidato LoRA/DoRA; enterprise possui DPO/PPO/retrieval FAISS locais, porém query devolve contexto e o pipeline padrão não injeta reward_model exigido pelo PPO; hybrid do demo chama só RAG; rag-finetuning treina embeddings; DPO biomédico retorna not_run.
- Cópia E: de dark-videos não herda estado de D:/Git/dark-videos. Laya app de notificações não é identificado como serviço Laya/Jev por semelhança nominal.
- Limites: revisão semântica seletiva e inventário estático local; sem atualização remota, execução/treino, comprovação de testes/runtime dos alvos ou análise CVE/EOL. Não promove bibliografia, smoke ou código presente a eficácia comprovada.
- Revalidar pelos scripts do pacote antes de reutilizar fatos após drift; `verificacao.json` delimita a prova executada, sem revisão independente.
