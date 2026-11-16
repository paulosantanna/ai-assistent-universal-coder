# Mapeamento beta 3.0.0 — 02_repositorios

Updated: 2026-10-27
Entry point: este índice → nota por repositório → fonte local.

Cobertura: **17 diretórios**, 16 com Git próprio e 1 pacote sem Git; **9152 arquivos com SHA-256**. 7 árvores Git têm alterações locais/não rastreados.

Novo em relação à lista do beta 2.0: **ncm**. A versão 3.0.0 identifica o mapa; não altera versões dos projetos.

## Repositórios

| Alvo | Arquivos | Git/HEAD local | Atualização do conhecimento |
|---|---:|---|---|
| [AIHealthResearch](repositorios/AIHealthResearch.md) | 97 | 5878719f17 | Correção de precisão do beta 2: há implementação LoRA/DoRA, não apenas intenção PEFT. Promoção continua separada do treino. |
| [Awesome-LLM-Post-training](repositorios/Awesome-LLM-Post-training.md) | 3 | d95a308fd9 | Curadoria mantida como bibliografia; nenhum trainer local inferido dos links. |
| [dark-videos](repositorios/dark-videos.md) | 618 | 440a5b2188 | Mapa amplia pgvector para retrieval de lições/chunks, grafo, NCM e LangGraph opcional. Checkout E: tem HEAD 440a5b2 e mudanças locais; atualizações de D: não são herdadas. |
| [dark-videos-mining-fix](repositorios/dark-videos-mining-fix.md) | 449 | sem Git | Continua pacote sem Git próprio; README histórico de aplicação não prova sincronização com dark-videos atual. |
| [DiabeticsresearchJEV](repositorios/DiabeticsresearchJEV.md) | 137 | 05b346419d | Registra hardening local: direitos de treinamento, smoke separado, DPO not_run e promoção condicionada. Relatos de testes/runtime são históricos. |
| [Engenharia-Reversa](repositorios/Engenharia-Reversa.md) | 6237 | f89b03e738 | Manifest atual rea-agents 6.8.0; composição MCP em eagerRuntime/transporte. Documentação local não rastreada separada do estado commitado. |
| [enterprise-llm-finetuning](repositorios/enterprise-llm-finetuning.md) | 101 | c0fac5a162 | DPO/PPO/retrieval FAISS estão na árvore local modificada. query devolve contexto, sem geração LLM; adaptador PPO exige reward_model e o pipeline padrão não o fornece. Presença de código não comprova execução fim a fim. |
| [FreePDFReader](repositorios/FreePDFReader.md) | 56 | HEAD não resolvido | Diretório tem .git, mas HEAD não resolvido e arquivos não rastreados. Não atribuir commit ou versão de release a esse estado. |
| [ibunny](repositorios/ibunny.md) | 101 | 0e1c4ae893 | Branch develop registrada; arquitetura Flutter/Go mantida. Nenhum pipeline LLM demonstrado na amostra. |
| [laya](repositorios/laya.md) | 697 | 052bc5533a | Snapshot atual 052bc55; retrieval RRF/FTS5 compartilhado e backends CLI constam do código/docs atuais. App laya não é o serviço Laya/Jev por semelhança nominal. |
| [ncm](repositorios/ncm.md) | 32 | c70274273f | Novo em relação à lista de 16 do beta 2; já possuía estudo separado. Incorporado ao mapa geral com tokenizer e gerador, mantendo treino completo não demonstrado. |
| [pdfcraft](repositorios/pdfcraft.md) | 543 | 7437bde378 | Workspace Rust/CLI/MCP opt-in mantido; regras de clean-room/licença devem acompanhar reutilização. |
| [post_training_llms](repositorios/post_training_llms.md) | 36 | f17d16b896 | SFT/DPO/GRPO locais confirmados estaticamente; funcionalidade, métricas e compatibilidade não revalidadas. |
| [rag-and-fine-tuning-demo](repositorios/rag-and-fine-tuning-demo.md) | 13 | b912236e58 | Correções locais de caminhos confirmadas; wrapper híbrido é conceitual. CUDA no treino depende de use_cuda=True; o entrypoint chama o padrão False. |
| [rag-finetuning](repositorios/rag-finetuning.md) | 19 | d33d2f5e7f | Imports fine_tuned ausentes removidos do __init__ local; preserva imports absolutos que dependem do contexto Feast. Integração fim a fim e arquivos ainda citados precisam de validação. |
| [remove-onedrive](repositorios/remove-onedrive.md) | 3 | 4066b4a292 | Utilitário de remoção de alto impacto permanece apenas lido; não confundir presença de IA no nome de outros projetos com pipeline LLM. |
| [RemoveWindowsAI](repositorios/RemoveWindowsAI.md) | 10 | fd90ea37fb | Scripts e documentação do Windows permanecem leitura estática; nenhum efeito no SO ou binário foi exercitado. |

## Artefatos

- [Conhecimento consolidado e reutilização](CONHECIMENTO.md).
- [Diferenças e limites da comparação](ATUALIZACOES.md), com detalhes em diferencas.json.
- [Matriz por dimensão](matriz-conhecimento.csv) e mapa.json para consulta estruturada.
- inventory.json: arquivos, exclusões, hashes, fingerprint e estado Git local.
- evidencias.json: locadores de fatos e declarações, sem cópia de trechos.
- verificacao.json: resultado dos gates executados; checksums.json: hashes dos artefatos.

## Método, escopo e limites

BRIEFING/RECON: continuidade, mapas anteriores e fontes locais. PLAN: cobrir cada diretório e revalidar evidências. EXECUTE: inventário limitado, revisão seletiva e geração de notas. VERIFY: cobertura, referências, hashes e preservação do estado Git. DEBRIEF: conhecimento e continuidade.

Leitura autorizada por ferramentas do ambiente. Os skills históricos citam um Tool Router AEOS removido na reorganização (MEMORY: Runtime pointer reconciliation); sua instalação não é presumida. O pedido e o AGENTS.md autorizam fontes locais e persistência em 07_mapeamentos/.

Hash/busca textual em todos os arquivos do inventário não significa revisão semântica de todas as linhas. As notas distinguem código presente, documentação, bibliografia, não demonstrado e não verificado. A presença de testes/workflows não indica aprovação.

Escopo exclui credenciais por nome, links/junctions, árvores de dados/cache/dependências/runtime, binários e arquivos acima de 2 MB; ver lista efetiva em inventory.json e regras em scripts/scan.py. Conteúdo do corpus, pesos, sessões e serviços externos não foram inspecionados. Nenhum fetch, pull, script dos alvos, treino, deploy, publicação, commit ou push foi executado.

A comparação beta 2→3 é de conhecimento e cobertura: o beta 2 não tem snapshot completo com hashes. A comparação de conteúdo verificável usa os hashes pontuais do beta 1 (2026-10-13); novos caminhos de inventário podem refletir filtros diferentes. Histórico Git por data não identifica o momento em que um checkout local foi atualizado.

## Atualizar e verificar

Na raiz do workspace:

```powershell
python 07_mapeamentos/mapeamento-beta-3.0.0/scripts/scan.py
# Revisar scripts/profiles.py contra as fontes antes de gerar novos fatos.
python 07_mapeamentos/mapeamento-beta-3.0.0/scripts/build.py
python 07_mapeamentos/mapeamento-beta-3.0.0/scripts/verify.py
```

A verificação é estática e sequencial pelo mesmo codenavi-agent; não é revisão independente. APIs, compatibilidade de bibliotecas, CVE/EOL e eficácia dos modelos não foram validadas. Os mapas beta 1, beta 2 e NCM permanecem como histórico.
