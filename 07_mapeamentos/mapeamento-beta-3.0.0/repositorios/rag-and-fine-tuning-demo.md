# rag-and-fine-tuning-demo — beta 3.0.0

Updated: 2026-10-27
Entry point: [índice](../README.md) · [mapa estruturado](../mapa.json)

Arquivos com hash: 13; fingerprint: `40690ff616f3435434c8ef6be2207086f3d4903af196326a7349d6db3f107c81`.
Git próprio: True; HEAD: `b912236e585f438889dd6d242e94161ed4dc1a30`; branch: `main`.
Estado local: há alterações/não rastreados; detalhes em inventory.json.

## Atualizações e reconciliação

Correções locais de caminhos confirmadas; wrapper híbrido é conceitual. CUDA no treino depende de use_cuda=True; o entrypoint chama o padrão False.

## Dimensões e evidências

### Propósito

**código presente** — Demonstração de RAG e ajuste LoRA de Gemma, com wrapper híbrido conceitual.

[rag-and-fine-tuning-demo/hybrid/hybrid_system.py:13](../../../02_repositorios/rag-and-fine-tuning-demo/hybrid/hybrid_system.py)

### Arquitetura

**código presente** — Diretórios rag, fine_tuning e hybrid; wrapper hybrid chama somente a cadeia RAG.

[rag-and-fine-tuning-demo/hybrid/hybrid_system.py:23](../../../02_repositorios/rag-and-fine-tuning-demo/hybrid/hybrid_system.py)

### Fluxo

**código presente** — Carrega documento → chunks 1000/200 → embeddings → FAISS → cadeia de recuperação e Ollama.

[rag-and-fine-tuning-demo/rag/rag_system.py:23](../../../02_repositorios/rag-and-fine-tuning-demo/rag/rag_system.py)

### Dados

**código presente** — Caminho do corpus é resolvido por argumento, ambiente ou caminho relativo.

[rag-and-fine-tuning-demo/rag/rag_system.py:16](../../../02_repositorios/rag-and-fine-tuning-demo/rag/rag_system.py)

### Interfaces

**código presente** — Consulta invoca a cadeia com entrada input.

[rag-and-fine-tuning-demo/rag/rag_system.py:63](../../../02_repositorios/rag-and-fine-tuning-demo/rag/rag_system.py)

### Configuração/deploy

**código presente** — Inferência RAG depende do modelo Ollama gpt-oss:20b; disponibilidade não sondada.

[rag-and-fine-tuning-demo/rag/rag_system.py:43](../../../02_repositorios/rag-and-fine-tuning-demo/rag/rag_system.py)

### Operação

**não demonstrado na amostra** — Sem conclusão positiva nesta revisão estática; não equivale a ausência universal.


### Fine-tuning

**código presente** — Gemma 270m com LoRA/SFT; dataset agora usa argumento/ambiente/caminho relativo.

[rag-and-fine-tuning-demo/fine_tuning/train_gemma.py:21](../../../02_repositorios/rag-and-fine-tuning-demo/fine_tuning/train_gemma.py)

### RAG

**código presente** — Embeddings MiniLM + FAISS + Ollama gpt-oss:20b.

[rag-and-fine-tuning-demo/rag/rag_system.py:40](../../../02_repositorios/rag-and-fine-tuning-demo/rag/rag_system.py)

### Pós-treino

**não demonstrado na amostra** — Sem conclusão positiva nesta revisão estática; não equivale a ausência universal.


### Inferência

**código presente** — Wrapper hybrid simula integração FT; executa somente RAG, sem carregar adaptador Gemma.

[rag-and-fine-tuning-demo/hybrid/hybrid_system.py:20](../../../02_repositorios/rag-and-fine-tuning-demo/hybrid/hybrid_system.py)

### Tecnologias/versões

**declarado** — Ver declarações extraídas e manifests; versões instaladas e compatibilidade não verificadas.

[rag-and-fine-tuning-demo/requirements.txt:1](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt)
[rag-and-fine-tuning-demo/requirements.txt:10](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt)
[rag-and-fine-tuning-demo/requirements.txt:11](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt)
[rag-and-fine-tuning-demo/requirements.txt:12](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt)
[rag-and-fine-tuning-demo/requirements.txt:13](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt)
[rag-and-fine-tuning-demo/requirements.txt:14](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt)
[rag-and-fine-tuning-demo/requirements.txt:15](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt)
[rag-and-fine-tuning-demo/requirements.txt:16](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt)

### Vulnerabilidades

**não verificado** — Sem consulta de CVE/EOL nesta missão.


### Obsolescência

**não verificado** — Sem consulta de CVE/EOL nesta missão.


## Declarações de versão

| Manifest / declaração | Valor | Evidência |
|---|---|---|
| dependency | langchain | [rag-and-fine-tuning-demo/requirements.txt:1](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| dependency | langchain-ollama | [rag-and-fine-tuning-demo/requirements.txt:2](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| dependency | langchain-huggingface | [rag-and-fine-tuning-demo/requirements.txt:3](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| dependency | langchain-community | [rag-and-fine-tuning-demo/requirements.txt:4](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| dependency | langchain-text-splitters | [rag-and-fine-tuning-demo/requirements.txt:5](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| dependency | faiss-cpu | [rag-and-fine-tuning-demo/requirements.txt:6](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| dependency | transformers | [rag-and-fine-tuning-demo/requirements.txt:7](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| dependency | peft | [rag-and-fine-tuning-demo/requirements.txt:8](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| dependency | accelerate | [rag-and-fine-tuning-demo/requirements.txt:9](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| dependency | datasets | [rag-and-fine-tuning-demo/requirements.txt:10](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| dependency | trl | [rag-and-fine-tuning-demo/requirements.txt:11](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| dependency | sentence-transformers | [rag-and-fine-tuning-demo/requirements.txt:12](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| dependency | torch | [rag-and-fine-tuning-demo/requirements.txt:13](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| dependency | torchvision | [rag-and-fine-tuning-demo/requirements.txt:14](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| dependency | torchaudio | [rag-and-fine-tuning-demo/requirements.txt:15](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| dependency | pandas | [rag-and-fine-tuning-demo/requirements.txt:16](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| dependency | tqdm | [rag-and-fine-tuning-demo/requirements.txt:17](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |
| dependency | gradio | [rag-and-fine-tuning-demo/requirements.txt:18](../../../02_repositorios/rag-and-fine-tuning-demo/requirements.txt) |

## Qualidade e limites

Workflows: 0; arquivos candidatos a testes: 0. Não executados.

- Amostra semântica seletiva; hash e busca textual não equivalem a auditoria integral.
- Nenhum runtime, treino, publicação ou sincronização remota executado.
- Fontes modificadas/não rastreadas fazem parte deste snapshot local.
