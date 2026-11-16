# post_training_llms — beta 3.0.0

Updated: 2026-10-27
Entry point: [índice](../README.md) · [mapa estruturado](../mapa.json)

Arquivos com hash: 36; fingerprint: `1477870652bf2696c237458f1293cf54533484c1093cf49477348c7c270631f1`.
Git próprio: True; HEAD: `f17d16b8965396103f243566f13b45dadebd5e26`; branch: `main`.
Estado local: limpo; detalhes em inventory.json.

## Atualizações e reconciliação

SFT/DPO/GRPO locais confirmados estaticamente; funcionalidade, métricas e compatibilidade não revalidadas.

## Dimensões e evidências

### Propósito

**código presente** — Implementações educacionais de SFT, preferências e aprendizado por reforço.

[post_training_llms/src/training/sft_trainer.py:10](../../../02_repositorios/post_training_llms/src/training/sft_trainer.py)

### Arquitetura

**código presente** — Módulos de treinamento SFT/DPO/RL separados e utilitários compartilhados.

[post_training_llms/src/training/rl_trainer.py:15](../../../02_repositorios/post_training_llms/src/training/rl_trainer.py)

### Fluxo

**código presente** — GRPO prepara prompts matemáticos, calcula recompensa por resposta e delega ao TRL.

[post_training_llms/src/training/rl_trainer.py:50](../../../02_repositorios/post_training_llms/src/training/rl_trainer.py)

### Dados

**código presente** — Ground truth é extraído do campo answer para recompensas matemáticas.

[post_training_llms/src/training/rl_trainer.py:50](../../../02_repositorios/post_training_llms/src/training/rl_trainer.py)

### Interfaces

**código presente** — Exemplo de uso de DPO disponível via módulo Python.

[post_training_llms/examples/run_dpo.py:13](../../../02_repositorios/post_training_llms/examples/run_dpo.py)

### Configuração/deploy

**declarado** — Dependências Python declaradas em requirements; ambiente não executado.

[post_training_llms/requirements.txt:6](../../../02_repositorios/post_training_llms/requirements.txt)

### Operação

**não demonstrado na amostra** — Sem conclusão positiva nesta revisão estática; não equivale a ausência universal.


### Fine-tuning

**código presente** — Pipeline SFT delega ao TRL.

[post_training_llms/src/training/sft_trainer.py:10](../../../02_repositorios/post_training_llms/src/training/sft_trainer.py)

### RAG

**não demonstrado na amostra** — Sem conclusão positiva nesta revisão estática; não equivale a ausência universal.


### Pós-treino

**código presente** — DPO e GRPO com recompensa matemática têm implementações locais; nenhuma execução nesta missão.

[post_training_llms/src/training/rl_trainer.py:9](../../../02_repositorios/post_training_llms/src/training/rl_trainer.py)

### Inferência

**não demonstrado na amostra** — Sem conclusão positiva nesta revisão estática; não equivale a ausência universal.


### Tecnologias/versões

**declarado** — Ver declarações extraídas e manifests; versões instaladas e compatibilidade não verificadas.

[post_training_llms/requirements.txt:10](../../../02_repositorios/post_training_llms/requirements.txt)
[post_training_llms/requirements.txt:13](../../../02_repositorios/post_training_llms/requirements.txt)
[post_training_llms/requirements.txt:14](../../../02_repositorios/post_training_llms/requirements.txt)
[post_training_llms/requirements.txt:15](../../../02_repositorios/post_training_llms/requirements.txt)
[post_training_llms/requirements.txt:16](../../../02_repositorios/post_training_llms/requirements.txt)
[post_training_llms/requirements.txt:19](../../../02_repositorios/post_training_llms/requirements.txt)
[post_training_llms/requirements.txt:2](../../../02_repositorios/post_training_llms/requirements.txt)
[post_training_llms/requirements.txt:20](../../../02_repositorios/post_training_llms/requirements.txt)

### Vulnerabilidades

**não verificado** — Sem consulta de CVE/EOL nesta missão.


### Obsolescência

**não verificado** — Sem consulta de CVE/EOL nesta missão.


## Declarações de versão

| Manifest / declaração | Valor | Evidência |
|---|---|---|
| dependency | torch>=2.0.0 | [post_training_llms/requirements.txt:2](../../../02_repositorios/post_training_llms/requirements.txt) |
| dependency | numpy>=1.24.0 | [post_training_llms/requirements.txt:3](../../../02_repositorios/post_training_llms/requirements.txt) |
| dependency | transformers>=4.40.0 | [post_training_llms/requirements.txt:4](../../../02_repositorios/post_training_llms/requirements.txt) |
| dependency | datasets>=2.0.0 | [post_training_llms/requirements.txt:5](../../../02_repositorios/post_training_llms/requirements.txt) |
| dependency | trl>=0.8.0 | [post_training_llms/requirements.txt:6](../../../02_repositorios/post_training_llms/requirements.txt) |
| dependency | pandas>=1.5.0 | [post_training_llms/requirements.txt:9](../../../02_repositorios/post_training_llms/requirements.txt) |
| dependency | scikit-learn>=1.2.0 | [post_training_llms/requirements.txt:10](../../../02_repositorios/post_training_llms/requirements.txt) |
| dependency | pyyaml>=6.0 | [post_training_llms/requirements.txt:13](../../../02_repositorios/post_training_llms/requirements.txt) |
| dependency | tqdm>=4.64.0 | [post_training_llms/requirements.txt:14](../../../02_repositorios/post_training_llms/requirements.txt) |
| dependency | jinja2>=3.1.0 | [post_training_llms/requirements.txt:15](../../../02_repositorios/post_training_llms/requirements.txt) |
| dependency | markupsafe>=2.0.0 | [post_training_llms/requirements.txt:16](../../../02_repositorios/post_training_llms/requirements.txt) |
| dependency | rouge-score>=0.1.2 | [post_training_llms/requirements.txt:19](../../../02_repositorios/post_training_llms/requirements.txt) |
| dependency | evaluate>=0.4.0 | [post_training_llms/requirements.txt:20](../../../02_repositorios/post_training_llms/requirements.txt) |
| dependency | jupyter>=1.0.0 | [post_training_llms/requirements.txt:23](../../../02_repositorios/post_training_llms/requirements.txt) |
| dependency | ipywidgets>=8.0.0 | [post_training_llms/requirements.txt:24](../../../02_repositorios/post_training_llms/requirements.txt) |
| dependency | matplotlib>=3.5.0 | [post_training_llms/requirements.txt:27](../../../02_repositorios/post_training_llms/requirements.txt) |
| dependency | seaborn>=0.11.0 | [post_training_llms/requirements.txt:28](../../../02_repositorios/post_training_llms/requirements.txt) |
| dependency | accelerate>=0.20.0 | [post_training_llms/requirements.txt:31](../../../02_repositorios/post_training_llms/requirements.txt) |
| dependency | black>=22.0.0 | [post_training_llms/requirements.txt:34](../../../02_repositorios/post_training_llms/requirements.txt) |
| dependency | flake8>=5.0.0 | [post_training_llms/requirements.txt:35](../../../02_repositorios/post_training_llms/requirements.txt) |
| dependency | pytest>=7.0.0 | [post_training_llms/requirements.txt:36](../../../02_repositorios/post_training_llms/requirements.txt) |

## Qualidade e limites

Workflows: 0; arquivos candidatos a testes: 6. Não executados.

- Amostra semântica seletiva; hash e busca textual não equivalem a auditoria integral.
- Nenhum runtime, treino, publicação ou sincronização remota executado.
- Fontes modificadas/não rastreadas fazem parte deste snapshot local.
