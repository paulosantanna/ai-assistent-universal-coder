# Atualizações verificadas — beta 3.0.0

Updated: 2026-10-27
Entry point: [README](README.md).

O beta 2 tinha 16 diretórios; agora são 17. Suas notas internas divergiam em alguns estados; este pacote prevalece como snapshot local de 27/10. Sem baseline completo não se atribui toda mudança ao período de 20→27/10.

## AIHealthResearch

Correção de precisão do beta 2: há implementação LoRA/DoRA, não apenas intenção PEFT. Promoção continua separada do treino.

Comparação dos locadores hashados do beta 1 (podem repetir arquivos): {'unchanged': 25}.

## Awesome-LLM-Post-training

Curadoria mantida como bibliografia; nenhum trainer local inferido dos links.

Comparação dos locadores hashados do beta 1 (podem repetir arquivos): {}.

## dark-videos

Mapa amplia pgvector para retrieval de lições/chunks, grafo, NCM e LangGraph opcional. Checkout E: tem HEAD 440a5b2 e mudanças locais; atualizações de D: não são herdadas.

Comparação dos locadores hashados do beta 1 (podem repetir arquivos): {'unchanged': 8, 'changed': 44}.

## dark-videos-mining-fix

Continua pacote sem Git próprio; README histórico de aplicação não prova sincronização com dark-videos atual.

Comparação dos locadores hashados do beta 1 (podem repetir arquivos): {'unchanged': 32}.

## DiabeticsresearchJEV

Registra hardening local: direitos de treinamento, smoke separado, DPO not_run e promoção condicionada. Relatos de testes/runtime são históricos.

Comparação dos locadores hashados do beta 1 (podem repetir arquivos): {'changed': 48, 'unchanged': 5}.

## Engenharia-Reversa

Manifest atual rea-agents 6.8.0; composição MCP em eagerRuntime/transporte. Documentação local não rastreada separada do estado commitado.

Comparação dos locadores hashados do beta 1 (podem repetir arquivos): {'outside_current_scope': 2, 'changed': 78, 'unchanged': 8}.

## enterprise-llm-finetuning

DPO/PPO/retrieval FAISS estão na árvore local modificada. query devolve contexto, sem geração LLM; adaptador PPO exige reward_model e o pipeline padrão não o fornece. Presença de código não comprova execução fim a fim.

Comparação dos locadores hashados do beta 1 (podem repetir arquivos): {}.

## FreePDFReader

Diretório tem .git, mas HEAD não resolvido e arquivos não rastreados. Não atribuir commit ou versão de release a esse estado.

Comparação dos locadores hashados do beta 1 (podem repetir arquivos): {'unchanged': 58}.

## ibunny

Branch develop registrada; arquitetura Flutter/Go mantida. Nenhum pipeline LLM demonstrado na amostra.

Comparação dos locadores hashados do beta 1 (podem repetir arquivos): {'unchanged': 19}.

## laya

Snapshot atual 052bc55; retrieval RRF/FTS5 compartilhado e backends CLI constam do código/docs atuais. App laya não é o serviço Laya/Jev por semelhança nominal.

Comparação dos locadores hashados do beta 1 (podem repetir arquivos): {'changed': 68, 'unchanged': 4}.

## ncm

Novo em relação à lista de 16 do beta 2; já possuía estudo separado. Incorporado ao mapa geral com tokenizer e gerador, mantendo treino completo não demonstrado.

Comparação dos locadores hashados do beta 1 (podem repetir arquivos): {}.

## pdfcraft

Workspace Rust/CLI/MCP opt-in mantido; regras de clean-room/licença devem acompanhar reutilização.

Comparação dos locadores hashados do beta 1 (podem repetir arquivos): {'unchanged': 117}.

## post_training_llms

SFT/DPO/GRPO locais confirmados estaticamente; funcionalidade, métricas e compatibilidade não revalidadas.

Comparação dos locadores hashados do beta 1 (podem repetir arquivos): {}.

## rag-and-fine-tuning-demo

Correções locais de caminhos confirmadas; wrapper híbrido é conceitual. CUDA no treino depende de use_cuda=True; o entrypoint chama o padrão False.

Comparação dos locadores hashados do beta 1 (podem repetir arquivos): {}.

## rag-finetuning

Imports fine_tuned ausentes removidos do __init__ local; preserva imports absolutos que dependem do contexto Feast. Integração fim a fim e arquivos ainda citados precisam de validação.

Comparação dos locadores hashados do beta 1 (podem repetir arquivos): {}.

## remove-onedrive

Utilitário de remoção de alto impacto permanece apenas lido; não confundir presença de IA no nome de outros projetos com pipeline LLM.

Comparação dos locadores hashados do beta 1 (podem repetir arquivos): {'unchanged': 7}.

## RemoveWindowsAI

Scripts e documentação do Windows permanecem leitura estática; nenhum efeito no SO ou binário foi exercitado.

Comparação dos locadores hashados do beta 1 (podem repetir arquivos): {'unchanged': 6}.

## Limites históricos

Os caminhos adicionados/ausentes estão em diferencas.json. Fora de escopo não significa removido. O beta 2 é preservado sem reescrever a história; suas alegações de pipelines funcionais e de runtime não são usadas como prova atual.

Git sem HEAD resolvido em FreePDFReader é registrado como limitação de proveniência. O pacote dark-videos-mining-fix não recebe o HEAD do repositório pai. Nenhuma referência remota local é tratada como prova do estado remoto atual.
