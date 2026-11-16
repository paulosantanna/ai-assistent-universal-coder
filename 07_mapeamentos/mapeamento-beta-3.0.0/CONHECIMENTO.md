# Conhecimento consolidado — beta 3.0.0

Updated: 2026-10-27
Entry point: [índice](README.md) → [notas por repositório](repositorios/) → fonte.

Este conhecimento descreve as cópias locais de `02_repositorios`. As notas individuais guardam locadores, linhas, versões declaradas e hashes. As indicações de reutilização abaixo são sugestões para futuras missões, condicionadas a escopo, direitos e verificação; não indicam integração instalada.

## Onde procurar cada conhecimento

| Necessidade | Fontes locais | Limite confirmado na revisão |
|---|---|---|
| Pesquisa com proveniência e candidato LoRA/DoRA | [AIHealthResearch](repositorios/AIHealthResearch.md) | Treinar candidato não promove nem comprova validade científica. |
| GraphRAG biomédico e treino QLoRA | [DiabeticsresearchJEV](repositorios/DiabeticsresearchJEV.md) | Direitos explícitos, separação por família e avaliação são gates distintos; DPO retorna not_run. |
| Adapters SFT/DPO/PPO e retrieval configurável | [enterprise-llm-finetuning](repositorios/enterprise-llm-finetuning.md) | Alterações locais; PPO precisa de reward_model; retrieval não é geração. |
| Estudo de SFT, DPO e GRPO | [post_training_llms](repositorios/post_training_llms.md) | Implementação educacional não executada nesta missão. |
| Taxonomia e bibliografia de pós-treino | [Awesome-LLM-Post-training](repositorios/Awesome-LLM-Post-training.md) | Links para outros projetos não são implementações desta árvore. |
| RAG mínimo FAISS/Ollama e LoRA Gemma | [rag-and-fine-tuning-demo](repositorios/rag-and-fine-tuning-demo.md) | Wrapper hybrid só executa RAG; integração do adaptador é conceitual. |
| Fine-tuning do espaço de embeddings | [rag-finetuning](repositorios/rag-finetuning.md) | SentenceTransformer/Feast/Kubeflow, sem inferir ajuste de LLM causal. |
| Memória de resultados, lições e seleção coarse-to-fine | [dark-videos](repositorios/dark-videos.md) | Paradigma NCM aplicado à seleção não usa pesos do modelo NCM. |
| Retrieval híbrido e RRF, eventos e aprovação de ações | [laya](repositorios/laya.md) | App de notificações é distinto do serviço Laya/Jev; backends precisam de pré-requisitos próprios. |
| Tokenização multiescala e inferência por níveis | [ncm](repositorios/ncm.md) | Release de avaliação; não presumir pipeline de treino completo. |
| CLI/MCP de engenharia reversa e proveniência de análise | [Engenharia-Reversa](repositorios/Engenharia-Reversa.md) | rea-agents 6.8.0 declarado; engines e autoridade para alvos são pré-requisitos. |
| Leitura PDF nativa e IA ONNX local | [FreePDFReader](repositorios/FreePDFReader.md) | Modelos/DLLs e execução não verificados; HEAD não resolvido. |
| Engine/workbench PDF e automação opt-in | [pdfcraft](repositorios/pdfcraft.md) | Regras de assets, licenças e clean-room devem ser preservadas. |
| Jogo Flutter e serviços Go | [ibunny](repositorios/ibunny.md) | Não presumir execução completa do runner nem integração LLM. |
| Referência de patch de mineração | [dark-videos-mining-fix](repositorios/dark-videos-mining-fix.md) | Pacote sem Git próprio; não reaplicar sem comparar com o alvo atual. |
| Administração Windows/OneDrive | [remove-onedrive](repositorios/remove-onedrive.md), [RemoveWindowsAI](repositorios/RemoveWindowsAI.md) | Operações de alto impacto no SO; nenhum utilitário foi executado. |

## Reconciliações que afetam o uso futuro

`enterprise-llm-finetuning` tem classes/configurações DPO, PPO e FAISS, mas `FaissRAGPipeline.query()` monta o contexto em `answer`, sem chamar um gerador. O caminho padrão de `TrainPipeline._execute_training()` passa `ppo_config` e não passa `reward_model`; `PPOTrainerAdapter.train()` rejeita sua ausência. Esta conclusão é estática e limitada a esse caminho: outros chamadores podem fornecer o modelo. Evidência: [query](../../02_repositorios/enterprise-llm-finetuning/src/infrastructure/rag/faiss_rag_pipeline.py), [pipeline](../../02_repositorios/enterprise-llm-finetuning/src/application/usecases/train_pipeline.py), [PPO](../../02_repositorios/enterprise-llm-finetuning/src/infrastructure/trainer/ppo_trainer.py).

No demo Gemma, os caminhos absolutos foram substituídos por argumento/ambiente/relativo. Entretanto, `train_gemma(use_cuda=False)` só seleciona explicitamente CUDA se receber `True`; o entrypoint usa o padrão. O cálculo de `bf16` usa disponibilidade CUDA/MPS separadamente. Registrar seleção de dispositivo não comprova que todas as combinações executam corretamente. Evidência: [train_gemma.py](../../02_repositorios/rag-and-fine-tuning-demo/fine_tuning/train_gemma.py).

`rag-finetuning/feature_repo/__init__.py` já não importa os dois módulos `fine_tuned_*` ausentes apontados no beta 2. Os imports remanescentes são absolutos: a resolução depende do contexto de execução do Feast/Python. Essa correção local não comprova `feast apply` ou o pipeline distribuído. Evidência: [__init__.py](../../02_repositorios/rag-finetuning/feature_repo/__init__.py).

`DiabeticsresearchJEV` separa smoke de QLoRA e impede tratar DPO não executado como sucesso. `FLOW-HARDENING.md` contém resultados de testes e endpoints verificados em uma missão anterior; os PIDs e a saúde desses serviços não foram revalidados agora. Evidência: [trainer.py](../../02_repositorios/DiabeticsresearchJEV/src/diabeticsresearchjev/application/training/trainer.py), [FLOW-HARDENING.md](../../02_repositorios/DiabeticsresearchJEV/FLOW-HARDENING.md).

## Relações e fronteiras

- `dark-videos-mining-fix` → `dark-videos`: relação de pacote de correção documentada no [README do pacote](../../02_repositorios/dark-videos-mining-fix/README.md). Não é dependência de runtime nem prova de sincronização atual.
- `dark-videos` → paradigma NCM: [learning/ncm.py](../../02_repositorios/dark-videos/backend/app/modules/learning/ncm.py). O projeto [ncm](repositorios/ncm.md) é a referência arquitetural, sem inferir carregamento de seus checkpoints por dark-videos.
- `dark-videos` ↔ `laya`: [cliente Laya/Jev](../../02_repositorios/dark-videos/backend/app/modules/learning/laya_jev_client.py) não demonstra conexão com o [app de notificações laya](../../02_repositorios/laya/README.md). Nomes semelhantes não estabelecem identidade.
- `AIHealthResearch` e `DiabeticsresearchJEV` compartilham domínio de pesquisa, porém código, dados, checkpoints e gates têm autoridades próprias. Nenhuma troca de corpus ou promoção cruzada foi executada.
- `E:/Github/.../02_repositorios/dark-videos` e `D:/Git/dark-videos` são cópias distintas. Esta missão guarda somente o snapshot E:, com HEAD e mudanças locais em inventory.json. Notas de publicação/Stories da cópia D: não comprovam os mesmos arquivos na E:.

O estudo NCM separado e a reprodução histórica de Sudoku permanecem em [mapeamento-ncm](../mapeamento-ncm/README.md) e na [nota NCM](../../.notebook/ncm-next-concept-modeling.md). Não foram repetidos nem ampliados nesta missão.

## Regra de atualização

Antes de reutilizar uma conclusão, consulte a nota do alvo, compare HEAD **e** fingerprint, e confira a evidência da dimensão necessária. Se houver drift, remapeie os arquivos afetados. Não derive validade científica, qualidade de treino, compatibilidade de APIs, ausência de CVE, suporte de versões ou implantação a partir deste inventário.
