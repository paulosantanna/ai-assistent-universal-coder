"""Reviewed additions to the historical profiles; source locators fail closed."""

def c(summary, path, needle, state='código presente'):
    return {'summary': summary, 'source': [path, needle], 'state': state}


EXTRA = {
 'Awesome-LLM-Post-training': {
  'purpose': c('Curadoria bibliográfica de pós-treino, raciocínio e avaliação de LLMs.', 'README.md', 'curated collection', 'documentado'),
  'architecture': c('Organização por taxonomia e links externos; não é implementação local dos trabalhos listados.', 'README.md', 'taxonomy', 'documentado'),
  'flow': c('Entrada de consulta pelo README e suas seções; papers e implementações citados precisam de inspeção própria.', 'README.md', 'post-training approaches', 'documentado'),
 },
 'enterprise-llm-finetuning': {
  'purpose': c('Pipeline de fine-tuning com casos de uso e adaptadores configuráveis.', 'src/application/usecases/train_pipeline.py', 'class TrainPipeline'),
  'architecture': c('Casos de uso dependem de interfaces de domínio; factories selecionam trainers.', 'src/infrastructure/factories/trainer_factory.py', 'class TrainerFactory'),
  'flow': c('Configuração → dados → modelo/adaptador → treino opcional → avaliação opcional → resultado.', 'src/application/usecases/train_pipeline.py', 'def run('),
  'data': c('Schemas Pydantic incluem treinamento, DPO, PPO e RAG.', 'src/domain/schemas/config_schema.py', 'class RAGConfig'),
  'interfaces': c('CLI inclui opções de execução RAG.', 'src/presentation/cli.py', '--rag-query'),
  'deployment': c('Manifest Python declara dependências; instalação e compatibilidade não verificadas.', 'pyproject.toml', '[project]', 'declarado'),
  'operation': c('Pipeline mede duração e publica métricas de avaliação no caminho W&B quando ativo.', 'src/application/usecases/train_pipeline.py', 'wandb.log'),
 },
 'post_training_llms': {
  'purpose': c('Implementações educacionais de SFT, preferências e aprendizado por reforço.', 'src/training/sft_trainer.py', 'SFTTrainer'),
  'architecture': c('Módulos de treinamento SFT/DPO/RL separados e utilitários compartilhados.', 'src/training/rl_trainer.py', 'class RLTrainingPipeline'),
  'flow': c('GRPO prepara prompts matemáticos, calcula recompensa por resposta e delega ao TRL.', 'src/training/rl_trainer.py', 'math_reward_function'),
  'data': c('Ground truth é extraído do campo answer para recompensas matemáticas.', 'src/training/rl_trainer.py', 'ground_truth'),
  'interfaces': c('Exemplo de uso de DPO disponível via módulo Python.', 'examples/run_dpo.py', 'import'),
  'deployment': c('Dependências Python declaradas em requirements; ambiente não executado.', 'requirements.txt', 'trl', 'declarado'),
 },
 'rag-and-fine-tuning-demo': {
  'purpose': c('Demonstração de RAG e ajuste LoRA de Gemma, com wrapper híbrido conceitual.', 'hybrid/hybrid_system.py', 'Conceptually'),
  'architecture': c('Diretórios rag, fine_tuning e hybrid; wrapper hybrid chama somente a cadeia RAG.', 'hybrid/hybrid_system.py', 'qa_rag.invoke'),
  'flow': c('Carrega documento → chunks 1000/200 → embeddings → FAISS → cadeia de recuperação e Ollama.', 'rag/rag_system.py', 'CharacterTextSplitter(chunk_size=1000'),
  'data': c('Caminho do corpus é resolvido por argumento, ambiente ou caminho relativo.', 'rag/rag_system.py', 'GEMMA_PROFILE_MD'),
  'interfaces': c('Consulta invoca a cadeia com entrada input.', 'rag/rag_system.py', 'def query_rag'),
  'deployment': c('Inferência RAG depende do modelo Ollama gpt-oss:20b; disponibilidade não sondada.', 'rag/rag_system.py', 'OllamaLLM(model='),
 },
 'rag-finetuning': {
  'purpose': c('Treino de embeddings para recuperação usando SentenceTransformer e Kubeflow.', 'kubeflow_embedding_training.py', 'def hybrid_embedding_training'),
  'architecture': c('Função de treinamento, definições Feast e serviços de recuperação descritos separadamente.', 'feature_repo/__init__.py', 'wiki_features'),
  'flow': c('Configura execução distribuída quando WORLD_SIZE existe e instancia SentenceTransformer.', 'kubeflow_embedding_training.py', 'SentenceTransformer(model_path'),
  'data': c('Dataset próprio lê Feast ou fallback Parquet; dados não inspecionados.', 'kubeflow_embedding_training.py', 'class FeastTrainingDataset'),
  'interfaces': c('Imports de feature views existentes substituem os módulos fine_tuned ausentes do relato antigo.', 'feature_repo/__init__.py', 'training_data_features'),
  'deployment': c('Docker Compose está presente; serviços não iniciados.', 'docker-compose.yml', 'services:', 'declarado'),
  'operation': c('Treinamento inicializa SummaryWriter no rank zero.', 'kubeflow_embedding_training.py', 'writer = SummaryWriter'),
 },
 'ncm': {
  'purpose': c('Geração coarse-to-fine por conceitos multiescala; release de avaliação/inferência.', 'README.md', 'evaluation entry point', 'documentado'),
  'architecture': c('Tokenizer VQ-VAE e gerador NextConceptTransformer são módulos distintos.', 'models/next_concept.py', 'class NextConceptTransformer'),
  'flow': c('Entrypoint de avaliação coordena geração e medição; não é pipeline completo de treino.', 'evaluate.py', 'def '),
  'data': c('Quantizador residual multiescala representa sequências por níveis e codebooks.', 'models/quant.py', 'class MultiscaleResidualVectorQuantizer'),
  'interfaces': c('Tokenizador liga pré-tokenização e VQ-VAE.', 'tokenization/vqvae_tokenizer.py', 'class VQVAETokenizer'),
  'deployment': c('README recomenda Python/CUDA e download separado de checkpoints e dados.', 'README.md', 'Python 3.10', 'documentado'),
  'operation': c('Avaliação reporta métricas por tarefa, incluindo Sudoku, tradução e linguagem.', 'README.md', 'valid-grid', 'documentado'),
 },
}

OVERRIDES = {
 'AIHealthResearch': {
  'flow': c('Pesquisa revalida versão das evidências; treino candidato valida snapshot e limita método a LoRA/DoRA.', 'src/aihealthresearch/infrastructure/trainer.py', 'unapproved fine-tuning method'),
 },
 'dark-videos': {
  'interfaces': c('Cliente Laya/Jev e retrieval remoto/local existem; nome não identifica integração com o app laya desta coleção.', 'backend/app/modules/learning/retrieval.py', 'LayaJevClient'),
  'data': c('Recupera Lesson e KnowledgeChunk por distância cosseno; pondera confiança e recência, com fallback local.', 'backend/app/modules/learning/retrieval.py', 'cosine_distance'),
  'operation': c('LangGraph opcional recupera lições, diagnostica resultados e persiste; o fallback preserva funções existentes.', 'backend/app/modules/learning/langgraph_flow.py', 'StateGraph = None'),
 },
 'DiabeticsresearchJEV': {
  'flow': c('Ciclo coleta, extrai grafo, indexa, treina candidato e avalia; smoke é distinto de QLoRA.', 'src/diabeticsresearchjev/application/pipeline/full_cycle.py', 'train = run_training'),
  'operation': c('Hardening documenta direitos de treino, separação por família e recibo de avaliação para promoção; resultados históricos não reexecutados.', 'FLOW-HARDENING.md', 'training_allowed=true', 'documentado'),
 },
 'Engenharia-Reversa': {
  'flow': c('Runtime MCP foi separado em composição e transporte; eagerRuntime é fonte atual.', 'src/main/eagerRuntime.ts', 'startMcpTransport'),
  'architecture': c('CLI e MCP compartilham workflows; protocolos de engine ficam fora de domain/application.', 'AGENTS.md', 'Dependencies flow inward', 'documentado'),
 },
 'laya': {
  'data': c('Retrieval compartilhado contém extração de palavras-chave e Reciprocal Rank Fusion; FTS5 permanece na camada db.', 'engine/laya/retrieval.py', 'def reciprocal_rank_fusion'),
 },
}

LLM = {
 'AIHealthResearch': {
  'fine_tuning': c('LoRA/DoRA causal LM implementados; artefato candidato permanece promoted=false e validação científica pendente.', 'src/aihealthresearch/infrastructure/trainer.py', '"promoted": False'),
  'rag': c('Recuperação BM25/vetorial com evidências versionadas.', 'src/aihealthresearch/infrastructure/search.py', 'def '),
 },
 'Awesome-LLM-Post-training': {
  'fine_tuning': c('Cobertura bibliográfica; links não equivalem a trainers locais.', 'README.md', 'Fine-tuning', 'bibliográfico'),
  'rag': c('RAG listado como trabalho externo.', 'README.md', 'RAG', 'bibliográfico'),
  'post_training': c('Pós-treino e reinforcement learning tratados em survey/curadoria.', 'README.md', 'Reinforcement Learning', 'bibliográfico'),
 },
 'dark-videos': {
  'rag': c('RAG de lições/chunks via embeddings e fallback; grafo reúne memória local e fatos remotos.', 'backend/app/modules/learning/retrieval.py', 'def _local_lessons'),
  'inference': c('Seleção NCM por conceitos e shortlist aplica paradigma; não carrega o modelo NCM externo.', 'backend/app/modules/learning/ncm.py', 'def '),
 },
 'DiabeticsresearchJEV': {
  'fine_tuning': c('QLoRA/SFT real separado de smoke; smoke não é elegível para promoção.', 'src/diabeticsresearchjev/application/training/trainer.py', '"promotion_eligible": False'),
  'rag': c('GraphRAG combina recuperação e evidência de grafo; acesso depende de serviços e corpus.', 'src/diabeticsresearchjev/application/knowledge/graphrag.py', 'def '),
  'post_training': c('DPO não fabrica preferências; retorna not_run no caminho ainda não executável.', 'src/diabeticsresearchjev/application/training/trainer.py', 'not_run'),
 },
 'enterprise-llm-finetuning': {
  'fine_tuning': c('SFT/LoRA/quantização têm adaptadores locais; treino não executado.', 'src/infrastructure/llm_model_loader/transformers_llm_model_loader.py', 'LoraConfig'),
  'rag': c('FAISS IndexFlatIP, embeddings normalizados e chunking. query retorna contexto concatenado em answer; não gera resposta com LLM.', 'src/infrastructure/rag/faiss_rag_pipeline.py', '"answer": context'),
  'post_training': c('Adaptadores DPO e PPO presentes na árvore local modificada; funcionamento fim a fim não comprovado.', 'src/infrastructure/trainer/ppo_trainer.py', 'class PPOTrainerAdapter'),
  'inference': c('Pipeline padrão passa ppo_config mas não reward_model ao caso de uso; comparar a exigência do adaptador PPO antes de executar.', 'src/application/usecases/train_pipeline.py', 'ppo_config=config.ppo'),
 },
 'laya': {
  'rag': c('Contexto híbrido semântico/FTS5 e fusão RRF compartilhada.', 'engine/laya/retrieval.py', 'def reciprocal_rank_fusion'),
  'inference': c('Backends locais e cloud descritos; instruções do produto não criam agentes do workspace.', 'README.md', 'OpenAI-compatible', 'documentado'),
 },
 'ncm': {
  'inference': c('Gerador NextConceptTransformer prediz níveis; não presumir código completo de treino nesta release.', 'models/next_concept.py', 'def generate'),
 },
 'post_training_llms': {
  'fine_tuning': c('Pipeline SFT delega ao TRL.', 'src/training/sft_trainer.py', 'SFTTrainer'),
  'post_training': c('DPO e GRPO com recompensa matemática têm implementações locais; nenhuma execução nesta missão.', 'src/training/rl_trainer.py', 'GRPOTrainer'),
 },
 'rag-and-fine-tuning-demo': {
  'fine_tuning': c('Gemma 270m com LoRA/SFT; dataset agora usa argumento/ambiente/caminho relativo.', 'fine_tuning/train_gemma.py', 'GEMMA_TRAINING_DATA'),
  'rag': c('Embeddings MiniLM + FAISS + Ollama gpt-oss:20b.', 'rag/rag_system.py', 'FAISS.from_documents'),
  'inference': c('Wrapper hybrid simula integração FT; executa somente RAG, sem carregar adaptador Gemma.', 'hybrid/hybrid_system.py', 'simulate the integration'),
 },
 'rag-finetuning': {
  'fine_tuning': c('Treino de embeddings SentenceTransformer, não de LLM causal.', 'kubeflow_embedding_training.py', 'SentenceTransformer(model_path'),
  'rag': c('Feature store Feast e Milvus declarados para recuperação.', 'feature_repo/feature_store.yaml', 'milvus', 'declarado'),
 },
}

UPDATES = {
 'AIHealthResearch': 'Correção de precisão do beta 2: há implementação LoRA/DoRA, não apenas intenção PEFT. Promoção continua separada do treino.',
 'Awesome-LLM-Post-training': 'Curadoria mantida como bibliografia; nenhum trainer local inferido dos links.',
 'dark-videos': 'Mapa amplia pgvector para retrieval de lições/chunks, grafo, NCM e LangGraph opcional. Checkout E: tem HEAD 440a5b2 e mudanças locais; atualizações de D: não são herdadas.',
 'dark-videos-mining-fix': 'Continua pacote sem Git próprio; README histórico de aplicação não prova sincronização com dark-videos atual.',
 'DiabeticsresearchJEV': 'Registra hardening local: direitos de treinamento, smoke separado, DPO not_run e promoção condicionada. Relatos de testes/runtime são históricos.',
 'Engenharia-Reversa': 'Manifest atual rea-agents 6.8.0; composição MCP em eagerRuntime/transporte. Documentação local não rastreada separada do estado commitado.',
 'enterprise-llm-finetuning': 'DPO/PPO/retrieval FAISS estão na árvore local modificada. query devolve contexto, sem geração LLM; adaptador PPO exige reward_model e o pipeline padrão não o fornece. Presença de código não comprova execução fim a fim.',
 'FreePDFReader': 'Diretório tem .git, mas HEAD não resolvido e arquivos não rastreados. Não atribuir commit ou versão de release a esse estado.',
 'ibunny': 'Branch develop registrada; arquitetura Flutter/Go mantida. Nenhum pipeline LLM demonstrado na amostra.',
 'laya': 'Snapshot atual 052bc55; retrieval RRF/FTS5 compartilhado e backends CLI constam do código/docs atuais. App laya não é o serviço Laya/Jev por semelhança nominal.',
 'ncm': 'Novo em relação à lista de 16 do beta 2; já possuía estudo separado. Incorporado ao mapa geral com tokenizer e gerador, mantendo treino completo não demonstrado.',
 'pdfcraft': 'Workspace Rust/CLI/MCP opt-in mantido; regras de clean-room/licença devem acompanhar reutilização.',
 'post_training_llms': 'SFT/DPO/GRPO locais confirmados estaticamente; funcionalidade, métricas e compatibilidade não revalidadas.',
 'rag-and-fine-tuning-demo': 'Correções locais de caminhos confirmadas; wrapper híbrido é conceitual. CUDA no treino depende de use_cuda=True; o entrypoint chama o padrão False.',
 'rag-finetuning': 'Imports fine_tuned ausentes removidos do __init__ local; preserva imports absolutos que dependem do contexto Feast. Integração fim a fim e arquivos ainda citados precisam de validação.',
 'remove-onedrive': 'Utilitário de remoção de alto impacto permanece apenas lido; não confundir presença de IA no nome de outros projetos com pipeline LLM.',
 'RemoveWindowsAI': 'Scripts e documentação do Windows permanecem leitura estática; nenhum efeito no SO ou binário foi exercitado.',
}
