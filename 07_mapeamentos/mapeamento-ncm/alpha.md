# Mapeamento Alpha — NCM (Next-Concept Modeling)

**Nível:** 1 de 3 (panorama e orientação) · **Updated:** 2026-10-21
**Alvo:** `02_repositorios/ncm` — clone de `https://github.com/HazyResearch/ncm.git`
**Pacote:** [`README`](README.md) → **Alpha** → [`Beta`](beta.md) → [`Celta`](celta.md) · matriz: [`matriz-comparativa-ncm.csv`](matriz-comparativa-ncm.csv)

> Objetivo deste nível: saber **o que é, onde está e o que promete** sem entrar na mecânica fina (isso é o Beta) nem na análise crítica (isso é o Celta). Pontos marcados `[?]` viram pergunta do próximo nível.

---

## 1. Identidade e procedência

| Item | Valor | Evidência |
|------|-------|-----------|
| Projeto | **Next-Concept Modeling (NCM)** — "Fast, Parallel Coarse-to-Fine Text Generation" | `README.md:1-14` [R] |
| Origem | Hazy Research (Stanford) — `github.com/HazyResearch/ncm` | `git remote -v`; paper arXiv:2610.14162 [X] |
| Commit local | `c70274273f489abc73832b2b98584a8483b6b203` (2026-10-14, "update bibtex") | `git log` |
| Histórico | 5 commits, todos de 13–14/10/2026 (release → links → fix → configs → bibtex) | `git log --reverse` |
| Estado | branch `main`, working tree limpo, sem alterações locais | `git status -sb` |
| Licença | MIT | `LICENSE` via `README.md:110` [R] |
| Autores | Kumbong, Khare, Mlauzi, Woen, Ding, Buchanan, Arora, Mirhoseini, Ré | `README.md:99-107` [R]; paper [X] |
| Contatos externos | Collection HF `hazyresearch/ncm`; blog Hazy `2026-10-12-ncm`; blog SAIL `/blogs/ncm/` | `README.md:7-10` [R] |

**Contexto no workspace:** é o 17º repositório de `02_repositorios` e o primeiro mapeado que **não** é um LLM/RAG/fine-tuning — é uma proposta de *arquitetura alternativa* aos LLMs atuais. Não estava no pacote `mapeamento-beta-2.0` (16 repos, 2026-10-20).

## 2. O que é o NCM (resumo de orientação)

NCM é um framework de **dois estágios** para geração de texto:

1. **Estágio 1 — Tokenizer multiescala:** um VQ-VAE residual multiescala comprime o texto numa **hierarquia de códigos discretos**: o nível 1 tem poucos códigos (esboço grosso), cada nível seguinte tem mais códigos (refinamento) até o nível K na resolução fina.
2. **Estágio 2 — Gerador de conceitos:** um transformer **prevê um nível por vez**, gerando **todas as posições de um nível em paralelo** (uma avaliação forward por nível), condicionado à reconstrução acumulada dos níveis anteriores. O decoder do tokenizer converte a hierarquia final em texto.

Em uma frase: em vez de "próximo **token**" (autoregressivo) ou "refinar a **sequência inteira** repetidamente" (diffusion), o NCM faz "**próximo conceito**" — coarse-to-fine, com paralelismo *dentro* de cada nível.

### Onde ele se posiciona

| Abordagem | O que gera por passo | Passos até o fim | Paralelismo |
|-----------|----------------------|------------------|-------------|
| LLM autoregressivo | 1 token | L (tokens) passos | nenhum entre tokens |
| Diffusion LM | *todos* os tokens, ruidosos→limpos | M passos (dezenas–centenas) sobre a sequência inteira | sim, mas custo de passo cheio |
| **NCM** | **1 nível inteiro de códigos** | **K passos** (nº de níveis, ex. 9–32) | sim, dentro do nível; seq. curtas no início |

`[C]` `models/next_concept.py:520-703` (loop de geração por nível) · `[X]` paper/blog.

## 3. Inventário físico (o que há no clone)

```
ncm/
├── evaluate.py                  (37↑)  entry point de avaliação: 1 shard por GPU → merge/score
├── requirements.txt             (9↑)   torch, numpy, omegaconf, hydra-core, transformers>=4.51, …
├── README.md · LICENSE · .gitignore
├── assets/                      (4)    logo + figuras do README (overview, quality_speed, coarse_to_fine.gif)
├── config/eval/                 (10)   1 YAML por task: xsum, wmt14, sudoku-easy/medium/hard,
│                                       tinystories, owt, lm1b-small/medium/large
├── models/                      (5 módulos, ~1.844 linhas)
│   ├── next_concept.py          (615)  NextConceptTransformer — o gerador (estágio 2)
│   ├── quant.py                 (632)  MultiscaleResidualVectorQuantizer — a hierarquia (estágio 1)
│   ├── vqvae.py                 (152)  VQVAE = Encoder + quantizador + Decoder (tokenizer)
│   ├── vae.py                   (237)  Encoder/Decoder usados pelo VQVAE
│   └── common.py                (208)  Transformer/Block/atenção com RoPE, GQA, qk-norm, KV-cache
├── tokenization/                (5 módulos, ~260 linhas)
│   ├── vqvae_tokenizer.py       (83)   VQVAETokenizer: camada que liga pré-tokenizer + VQVAE
│   ├── bpe_tokenizer.py         (97)   BPE próprio (bytes/merges em pickle)
│   ├── hf_tokenizer.py          (29)   wrapper HuggingFace (GPT-2, Qwen, BERT…)
│   ├── sudoku_tokenizer.py      (21)   alfabeto de 12 símbolos para tabuleiros
│   └── tokenizer.py             (30)   interface base
├── evaluation/gen_ppl.py        (119)  generative perplexity (NLL só nos tokens gerados)
├── scripts/
│   ├── eval_shard.py            (150)  gera para N inputs num shard, aplica penalidades, decodifica
│   └── eval_merge.py            (129)  merge dos shards + métricas (BLEU/ROUGE/exact/genPPL/FLM)
└── utils/
    ├── registry.py              (23)   registries: tokenizers, quantizadores, level schedulers
    └── misc.py                  (25)   count_params, round_levels
```

Total: ~2.580 linhas de Python — projeto **enxuto e focado** (é um release de paper: inferência + avaliação).

**Entry points de execução:** `evaluate.py` → `scripts/eval_shard.py` → `scripts/eval_merge.py` (`README.md:68-94` [R]). Flagram: exige **GPU CUDA** (`evaluate.py:20-22`) e baixa checkpoints/datasets do Hugging Face.

## 4. Fluxo ponta a ponta (visão de orientação)

```
texto ──► pré-tokenizer          ids (GPT-2/Qwen/BERT/Sudoku)
          (hf|bpe|sudoku)
      ──► encoder do VQ-VAE      z  (contínuo, L posições)
      ──► quantizador multiescala z_to_idx()
             nível 1  ▸ poucos códigos (grosso)          ┐
             nível 2  ▸ mais códigos                     │  K níveis
             ...                                         │  (codebooks próprios,
             nível K  ▸ resolução máxima (fino)          ┘   residual acumulado)
      ──► TOKENS DA HIERARQUIA (índices por nível)

geração (estágio 2):
prefixo ─► gerador prevê nível 1 ... nível K   (1 forward por nível; paralelo DENTRO do nível)
      ──► índices gerados ─► idx_to_zhats ─► decoder do VQ-VAE ─► ids ─► texto
```

`[C]` encode: `tokenization/vqvae_tokenizer.py:31-45`, `models/quant.py:573-632`; geração: `models/next_concept.py:520-703`; decodificação: `scripts/eval_shard.py:140-146`.

## 5. Claims principais e status

| Claim | Fonte | Status neste mapeamento |
|-------|-------|-------------------------|
| Geração coarse-to-fine com refinamento visível nível a nível | `README.md:22-26` [R]; blog [X] | **Estruturalmente confirmado no código** (loop por nível) `[C]` |
| "9–31× mais rápido" que baselines de diffusion | `README.md:28-30` [R] | Não reproduzido. Paper diz 21× (LM1B), 10× (OWT), 31× (XSum); blog diz 10–31× — a faixa "9–31×" do README diverge ligeiramente `[X]` |
| Melhora genPPL vs DLM no LM1B | paper/blog [X] | Não reproduzido (exige checkpoints/GPU) |
| Sudoku: supera AR e diffusion em todas as dificuldades | blog [X] | **Hard reproduzido em 2026-10-21**: 86,25% (1725/2000) vs 86,1% do blog; easy/medium não executados — `.work/ncm-repro/RESULTADO.md` |
| 4–5× menos tokens de treino | blog [X] | Não reproduzido; sem código de treino no clone |
| Cada modelo = tokenizer congelado + gerador | `README.md:38` [R] | Confirmado: `vq` congelado no gerador `[C]` `models/next_concept.py:80-84` |
| 8 tasks/modos liberados (XSum, WMT14, Sudoku×3, TinyStories, OWT, LM1B×3) | `README.md:40-56` [R] | Confirmado: 10 configs locais `config/eval/` `[C]` |

## 6. Modelos liberados (checkpoints no HF)

| Task | Família | Níveis (K) | Estratégia do nível 1 | Métrica de avaliação |
|------|---------|-----------|------------------------|----------------------|
| XSum | sumarização extrema | 9 | queries aprendidas | ROUGE-1/2/L + genPPL |
| WMT14 De–En | tradução | 11 | previsto do fim do prefixo | BLEU/cased, chrF, length ratio |
| Sudoku easy/medium/hard | raciocínio | 12 | queries aprendidas | solved %, cell %, valid % |
| TinyStories | geração incondicional | 12 | amostrado de unigrama | genPPL (GPT-2 large) |
| OpenWebText | geração incondicional | 32 | amostrado de unigrama | genPPL |
| LM1B small/medium/large | geração incondicional | 12 | unigrama / queries | genPPL (protocolo FLM) |

`[C]` cada linha vem de `config/eval/<task>.yaml`; detalhes completos no Beta §7.

## 7. Glossário inicial

| Termo | Significado (neste repo) |
|-------|--------------------------|
| **Nível / concepto** | Uma das K etapas da hierarquia; tem comprimento próprio (ex. 4, 6, …, 48 posições) e um codebook próprio |
| **Codebook** | Tabela de vetores de código (ex. 4096 entradas por nível no texto) |
| **Residual multiescala** | Cada nível quantiza o *resíduo* não capturado pelos níveis anteriores |
| **VQ-VAE** | Autoencoder vetorial-quantizado: comprime ids → z → códigos → reconstrói ids |
| **Coarse-to-fine** | Geração grosso→fino: esboço primeiro, detalhes depois |
| **NFE** | Number of Function Evaluations — nº de forwards do gerador usados na geração (no NCM ≈ nº de níveis) |
| **CFG** | Classifier-free guidance: mistura com uma ramificação "nula" para reforçar o condicionamento |
| **Prefixo** | Contexto de entrada (ex. texto a sumarizar/traduzir), tokenizado e embutido no lugar de um z gerado |
| **Unigrama** | Distribuição de frequência de códigos salva no checkpoint; usada para inicializar o nível 1 incondicional |
| **`fine_drop`** | Dropout de níveis finos no treino do tokenizer (o decoder aprende a reconstruir de hierarquias truncadas) |
| **Atenção block-diagonal** | Padrão de máscara: cada nível só enxerga o prefixo e a si mesmo |
| **MBR** | Minimum Bayes Risk — decodificação por consenso sobre múltiplos candidatos (test-time scaling) |

## 8. Perguntas que o Beta responde

- `[?]` Como exatamente o quantizador constrói a hierarquia (down/up-sampling, resíduo, `Phi`)? → Beta §3
- `[?]` Como o gerador sabe "onde" está cada nível (RoPE por nível, máscara block-diagonal, level embedding)? → Beta §5
- `[?]` De onde vêm as "queries" do nível 1 e o unigrama? → Beta §3/§7
- `[?]` Por que existem penalidades de frequência/adjacência e para que servem? → Beta §8
- `[?]` O que é exatamente medido em cada métrica (genPPL, FLM, exact)? → Beta §8
- `[?]` O que o repo **não** libera (treino, dados, baselines)? → Beta §9
