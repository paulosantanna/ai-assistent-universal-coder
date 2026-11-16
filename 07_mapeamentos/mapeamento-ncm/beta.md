# Mapeamento Beta — NCM: estrutura e componentes

**Nível:** 2 de 3 (como está construído) · **Updated:** 2026-10-21
**Alvo:** `02_repositorios/ncm` @ `c702742` · **Pacote:** [`README`](README.md) → [`Alpha`](alpha.md) → **Beta** → [`Celta`](celta.md)

> Pressupõe o Alpha. Aqui cada módulo é aberto com responsabilidade, símbolos principais e ponteiros `arquivo:linha`. A mecânica matemática fica para o Celta.

---

## 1. Mapa de módulos

| Módulo | Papel | Símbolos principais | Ponteiros |
|--------|-------|---------------------|-----------|
| `models/quant.py` | **Estágio 1** — hierarquia residual multiescala | `MultiscaleResidualVectorQuantizer`, `Phi`, `PhiConvStack`, `z_to_idx`, `idx_to_zhats`, `get_next_autoregressive_input` | `models/quant.py:11-143` (Phi/samplers), `:228-343` (init), `:448-549` (forward), `:573-726` (encode/decode) |
| `models/vqvae.py` | Empacota Encoder + quantizador + Decoder | `VQVAE.encode/decode/get_ncm_inputs/reconstruct_multiscales` | `models/vqvae.py:10-141` |
| `models/vae.py` | Encoder/Decoder (embedding lookup + blocos leves) | `Encoder`, `Decoder`, `forward_nopos` | `models/vae.py:102-258` |
| `models/common.py` | Backbone transformer do gerador | `SelfAttention` (GQA, qk-norm, KV-cache), `MLP`, `Block`, `precompute_rope_cos_sin` | `models/common.py:13-237` |
| `models/next_concept.py` | **Estágio 2** — gerador por níveis | `NextConceptTransformer.generate`, `forward`, `_decode_level_logits`, `_TiedCodebookHead` | `models/next_concept.py:9-34` (head), `:65-337` (init/masks), `:376-518` (fwd/decode), `:520-703` (generate) |
| `tokenization/vqvae_tokenizer.py` | Liga pré-tokenizer + VQVAE; chunking | `VQVAETokenizer` | `tokenization/vqvae_tokenizer.py:7-86` |
| `tokenization/hf_tokenizer.py` | Wrapper HF (GPT-2, Qwen3, BERT) | `HFTokenizer` | `tokenization/hf_tokenizer.py:5-36` |
| `tokenization/bpe_tokenizer.py` | BPE próprio (bytes/merges pickle) | `BPETokenizer` | `tokenization/bpe_tokenizer.py:6-100` |
| `tokenization/sudoku_tokenizer.py` | Alfabeto 12 símbolos (`_1..9|B`) | `SudokuTokenizer` | `tokenization/sudoku_tokenizer.py:4-26` |
| `utils/registry.py` | Registries: tokenizer, quantizador, **level schedulers** | `tokenizers`, `vector_quantizers`, `level_schedulers` | `utils/registry.py:4-23` |
| `utils/misc.py` | Utilidades | `count_params`, `round_levels` | `utils/misc.py:4-29` |
| `scripts/eval_shard.py` | Geração por shard + decodificação + penalidades | `pick_tokens`, `run`, `prefix` | `scripts/eval_shard.py:29-173` |
| `scripts/eval_merge.py` | Merge + métricas | `bleu`, `rouge`, `exact`, `genppl`, `genppl_flm` | `scripts/eval_merge.py:24-154` |
| `evaluation/gen_ppl.py` | genPPL (só tokens gerados) | `generation_perplexity` | `evaluation/gen_ppl.py:19-148` |

**Grafo de dependências (imports):** `evaluate.py` → `scripts/eval_shard.py`/`eval_merge.py` → `models.next_concept` → `models.common` + `models.vqvae` → `models.vae` + `utils.registry` → `models.quant`. `eval_merge` também usa `evaluation.gen_ppl` e libs externas (`sacrebleu`, `rouge_score`, `transformers`). Tudo é parametrizado por `OmegaConf` a partir de `config/eval/*.yaml` (`scripts/eval_shard.py:29-49`).

## 2. O tokenizer em dois estágios

### 2.1 Pré-tokenizers (a "camada 0", tokens do mundo LLM)

| Nome | Uso nas configs | Detalhe | Ponteiro |
|------|-----------------|---------|----------|
| `hf` | XSum (GPT-2), WMT14 (Qwen3-0.6B), OWT/LM1B (GPT-2 / BERT-base) | wrapper `AutoTokenizer`; injeta `eos`/`pad` especiais | `tokenization/hf_tokenizer.py:5-36` |
| `bpe` | TinyStories | BPE de bytes com merges ordenados; vocabs em pickle (`bpe_vocab_8192.pickle`, `bpe_merges_8192.pickle`) | `tokenization/bpe_tokenizer.py:20-85` |
| `sudoku` | Sudoku ×3 | fixo: `_`=0, `1..9`, `|`=10, `B`=11; `seq_len=89`, `prompt_len=91` | `tokenization/sudoku_tokenizer.py:4-21` |

### 2.2 `VQVAETokenizer` (ponte com o VQVAE)

- `_adjust_length`: quebra a sequência em chunks de `context_length` do VQVAE, com **padding** quando o último chunk é curto (`:21-28`).
- `encode_pre_tokenized` → `vqvae.encode` → achata a hierarquia num vetor de índices (`:36-39`).
- `decode` faz o caminho inverso: `vqvae.decode(idx)` → argmax → ids do pré-tokenizer (`:47-52`).
- `reconstruct_multiscales` / `decode_multiscales`: reconstruções parciais por nível (útil para visualizar o coarse-to-fine) (`:68-86`; `models/vqvae.py:126-141`).

## 3. `MultiscaleResidualVectorQuantizer` (o coração do Estágio 1)

**Construção** (`models/quant.py:228-343`):
- `levels`: lista de comprimentos por nível. Configs liberadas usam `levels.use_manual_levels` (ex. XSum `[4,6,10,14,20,26,32,40,48]`); alternativamente há **level schedulers** (linear/cubic/exp/sqrt/sine/log/quadratic) em `utils/registry.py:15-22` + `round_levels` (`utils/misc.py:17-29`) — não usados nos modelos liberados `[C]`.
- `embeddings`: `ModuleList` de `nn.Embedding`, um **codebook por nível** com tamanho próprio; atualizados por **EMA**, não por gradiente (`:294-304`).
- `quant_resi` (`Phi`): conv residual 1-D pós-upsample, mistura `h*(1-r) + Conv1d(h)*r` com `r=0.5` típico; variantes `PhiConvStack`, `PhiShared`, `PhiPartiallyShared` (`:11-143`). Configuração comum: `share_mode=0` (um `Phi` por nível).
- `learned_l1_sampling`: troca o*down/up-sampling* do nível 0 por convs aprendidos (`stride = L/levels[0]`, init == area-pool / repeat) com variante em cascata (`:145-204`, `:310-328`).
- `learned_all_sampling` (não usado nos liberados): refinamentos zero-init para todos os níveis (`:330-342`).
- `fine_drop` (**implementado**): no treino, trunca o `z_hat` em um nível aleatório ≥ `min_keep`, ensinando o decoder a reconstruir de hierarquias incompletas (`:262-269`, `:429-434`, `:457-462`, `:525-530`).
- `kmeans_init` e `_restart_dead_codes` (anti-colapso de código) disponíveis (`:279-283`, `:344-378`, `:436-446`).

**Codificação** — `z_to_idx` (`:573-632`): laço por nível; *downsample* do resíduo → código mais próximo (argmin de distância) → *upsample* + `Phi` → acumula em `z_hat`, subtrai de `z_rest`; opção de amostragem estocástica de códigos (`set_stochastic_encode`, `:551-571`).

**Decodificação / montagem para o gerador**:
- `idx_to_z_q` / `idx_to_zhats` (`:634-668`, `:711-726`): reconstrói `z_hat` acumulado (e versões por nível).
- `idx_to_ncm_input` (`:670-694`): concatena o `z_hat` acumulado reamostrado para o comprimento de **cada** nível seguinte — usado para pré-computar insumos de treino.
- `get_next_autoregressive_input` (`:696-709`): versão de inferência — acumula a contribuição do nível `i`, devolve o `z_hat` e a entrada para o nível `i+1` (área-interp para `levels[i+1]`).

**Perdas (treino, apenas código de referência):** `forward` soma `commitment_cost * MSE(z_hat.detach(), z)` + `MSE(z_hat, z_no_grad)` por nível e divide por nº de níveis (`:519-524`); straight-through **só no nível 0** com `learned_l1_sampling` (comentário no código: nos níveis altos ele diverge em ~100 passos) (`:503-505`). Estatísticas de utilização de codebook são retornadas por nível (`:533-541`).

## 4. `VQVAE` e os blocos `Encoder`/`Decoder`

- **Encoder** (`models/vae.py:102-179`): `wte` (embedding de ids do pré-tokenizer) + `wpe` opcional; `conv_blocks` (`enc_conv_layers`); `blocks` (`enc_layers`); compressão opcional `down` (init == average pool, `compression_factor`).
- **Decoder** (`models/vae.py:198-258`): `up` opcional (init == repeat) → `middle_block` + `extra_blocks` (`dec_layers`) → `output_layer` Linear p/ vocabulário. **Nota de nomenclatura:** nos blocos, `n_layers` do VQVAE é usado como **nº de heads** dos blocos internos, não como profundidade (`models/vae.py:131-134`, `:224-227`).
- **`forward_nopos`** do Encoder (`:181-195`): embedding + senoides fixas — caminho usado quando o prefixo é "contextual" no gerador.
- `pre_quant_norm` GroupNorm `affine=False` — justificativa no código: `||z-e||²` não é invariante a escala, gamma aprendível divergiria (`models/vqvae.py:59-67`).
- Configs liberadas usam `compression_factor: 1` em todas as tasks → a compressão de sequência existe mas **não é usada** nos checkpoints publicados `[C]`.

## 5. `NextConceptTransformer` (o gerador)

**Construção** (`models/next_concept.py:65-310`):
- Referencia o VQVAE congelado numa tupla (fora do `state_dict`) (`:80-84`); `levels` e `L = sum(levels)` vêm do quantizador.
- `query_level0`: nível 0 gerado por **queries aprendidas** (1 pass em paralelo); `l0_ar` (opcional) faz nível 0 autoregressivo; `predict_level0`: nível 0 previsto do **fim do prefixo** (`:88-91`, `:239-242`, `:249-264`, `_level0_slice :427-435`).
- **RoPE por nível**: buffers `rope_cos_gen_k` com posições `[0..P-1]` para o prefixo e `[0..l_k-1]` **resetando por nível** no alvo (`:94-117`); fallback posicional absoluto (`wpe`) se `use_rope=false`.
- `wte` é um `nn.Linear(embed_dim → n_embd)` que projeta `z` (do VQVAE) para o espaço do transformer (`:129-133`).
- **Level encoding**: `wle` soma o índice do nível à entrada (`:197-200`).
- **Cabeças de saída** (3 modos): `shared_output_head`, `tie_heads_to_codebook` (head atada ao codebook = classificador em forma de distância `2z·E − ||E||²`, com escala aprendida — `_TiedCodebookHead :9-34`) ou Linear por nível (`:214-237`).
- **Máscaras** (`:266-301`): `block_diagonal` (alvo vê prefixo + **o próprio nível**; prefixo não vê alvos) ou `block_causal` (vê níveis anteriores também); variante `use_flex_attention` com `create_block_mask` equivalente (`:312-337`).
- `ctx_encoder` opcional (T5 pré-treinado ou pequeno transformer interno; inicialização a partir de GPT-2/wte do VQVAE) — **desabilitado em todas as configs liberadas** `[C]` (`:135-181`).
- `post_upsample_conv` zero-init (usado no LM1B): conv por nível após o upsample implícito (`:183-195`, `:339-355`).

**Forward** (`:376-406`, `:437-464`): monta `[prefixo; todos os níveis]`, aplica o stack, e produz logits por nível; modo `predict_level0` acrescenta o logit do nível 0 lido do fim do prefixo.

**Decodificação por nível:**
- Eager: `_decode_level_logits` (`:501-518`) roda o stack no par `[prefixo; nível k]` com máscara "alvo vê prefixo, dentro do nível tudo visível".
- KV-cache: cache do prefixo reutilizado por nível (`:645-657`, `:680-688`); exclusivo com `query_level0` (assert `:523-524`).

**`generate`** (`:520-703`): 
1. CFG opcional: duplica o batch com um prefixo "nulo" (tudo `pad`, com `eos` na posição 0) e mistura `(1+t)·logits_doc − t·logits_nulo` com `t` **crescendo linearmente por nível** (`:529-540`, `:477-485`).
2. Codifica o prefixo: `raw_token_prefix` → lookup `encoder.wte` (ou `forward_nopos` se `contextual_prefix`); senão `encode_z` — o prefixo é embutido do **encoder do VQVAE**, não do `wte` do gerador (`:546-560`).
3. Nível 0: dado (`idx`), por queries (`:581-627`), ou previsto (`:629-641`).
4. Laço `for level_idx in range(len(levels)-1)`: pega a contribuição do nível atual (`get_next_autoregressive_input`), projeta, soma level-embedding, roda o stack com RoPE/máscara do nível, amostra **todas as posições do nível de uma vez** (`:659-694`).
5. Retorna a concatenação de todos os níveis (códigos) (`:699-703`).

**Amostragem de código:** `_sample_level*/_sample_level_raw` (`:477-499`): temperature (0 = argmax), top-k, top-p; a mistura CFG acontece antes do sampling.

## 6. `models/common.py` (backbone)

- RoPE pré-computado e aplicado (`:13-30`); atenção com **GQA** (`n_kv_heads`, `:60-62`), **qk-norm** estilo Llama 3 sobre head_dim antes do RoPE (`:76-81`, `:99-101`), **KV-cache** com rotação apenas das posições novas (`:83-118`), `flex_attention` opcional (`:120-125`).
- MLP variantes: GELU padrão, SwiGLU/GeGLU, ReLU² e `mlp_ratio` (`:135-165`).
- Blocos: residual padrão, `parallel_block`, `normformer`, `layerscale`, `rezero` (`:167-213`).
- `Transformer` base apenas define interface (`:215-237`).

## 7. Configs por task (todas as 10, campos-chave)

| Config | n_layer/n_head/n_embd | K | levels (comprimentos) | codebook/nível | prefix_len (fonte) | nível 0 | cabeças | sampling (geração) | métrica |
|--------|----------------------|---|-----------------------|----------------|--------------------|---------|---------|--------------------|---------|
| `xsum` | 12/12/768 | 9 | 4→48 | 4096 | 512 (GPT-2 raw) | queries | atadas ao codebook | top_k=1, freq 2.0, adj 5,4,0.5 | ROUGE |
| `wmt14` | 12/12/768 | 11 | 1→64 | 4096 | 96 (Qwen3-0.6B raw) | previsto | Linear (sem bias) | top_k=1 | BLEU |
| `sudoku-easy` | 8/8/512 | 12 | 1→89 | 16 | 91 (sudoku) | queries | Linear | temp 0 (argmax) | exact |
| `sudoku-medium` | 8/8/512 | 12 | 1→89 | 16 | 91 (sudoku) | queries | Linear | temp 0 | exact |
| `sudoku-hard` | 8/8/512 | 12 | 1→89 | 16 | 91 (sudoku) | queries | Linear | temp 0 | exact |
| `tinystories` | 12/12/768 | 12 | 1→128 | 4096 | 1 (BPE próprio) | unigrama | atadas ao codebook | top_p=1.0 | genPPL |
| `owt` | 16/16/1024 | 32 | 1…1024 (quadrados) | 8192 | 1 (GPT-2) | unigrama | atadas (com bias) | top_p=1.0, `cut_at_eos:false` | genPPL |
| `lm1b-small` | 12/12/768 | 12 | 1→128 | 8192 | 1 (BERT) | unigrama/queries | shared + bias por nível | freq 11.5, adj 10,4,0.5 | genPPL FLM |
| `lm1b-medium` | 24/16/1024 | 12 | 1→128 | 8192 | 1 (BERT) | unigrama/queries | shared + bias por nível | idem | genPPL FLM |
| `lm1b-large` | 36/20/1280 | 12 | 1→128 | 8192 | 1 (BERT) | unigrama/queries | shared + bias por nível | idem | genPPL FLM |

`[C]` `config/eval/*.yaml`. Observações transversais:
- Todos usam `attn_pattern: block_diagonal`, `use_rope: true`, `use_qk_norm: true`, `use_level_encoding: true`, `ctx_encoder.enabled: false`.
- O tokenizer do LM1B é **compartilhado** entre small/medium/large (`../tokenizer.pt`); o gerador difere por tamanho.
- `generation.frequency_penalty`, `frequency_deficit`, `adjacency_penalty`, `frequency_allowance` e `level0_unigram` são **knobs de avaliação** (aplicados em `eval_shard.py`), não do modelo.
- `aux.code_corruption` (LM1B) e `aux.fine_drop.dual/w_full/w_trunc` aparecem **nas configs mas não têm implementação** no código liberado (grep: só configs) — são resíduos do pipeline de treino `[C]`.

## 8. Pipeline de avaliação

**Orquestração** — `evaluate.py`: carrega a config, escolhe GPUs, dispara **1 processo por GPU** (`CUDA_VISIBLE_DEVICES`), grava `shard_k.log`, e roda o merge (`evaluate.py:9-42`). Sem GPU visível: `sys.exit` (`:20-22`).

**Shard** — `scripts/eval_shard.py`:
- Carrega tokenizer + gerador com `strict=True` (`:45-54`); resolve `level0_unigram`/`token_unigram` do checkpoint por especificação `arquivo:chave` (`load_allowance :59-66`); modos de unigrama: `unigram|active|uniform|smooth:<eps>` via `--l0` (`:70-78`).
- Condicional: monta prefixo truncando/padronizando para `prefix_len` (`prefix :94-96`). Incondicional: amostra o nível 0 do unigrama salvo e usa `eos` como prefixo (`:150-159`).
- `run()`: `generate` → `idx_to_zhats` → **decoder do VQVAE** → argmax → `pick_tokens` (só quando freq/adj ativos; senão argmax) → corta no EOS → texto (`:140-146`, `:127-134`).
- `pick_tokens` (`:99-124`): decodificação **gulosa com correções** — penalidade de frequência acima de uma "cota" (allowance por token), bônus por déficit, e penalidade de adjacência sobre os últimos `w` tokens com decaimento `d^j` (formato `strength,window,decay`).
- `RAW` guarda os ids sem corte para o protocolo FLM (`:144-145`).

**Merge/métricas** — `scripts/eval_merge.py`:
- `bleu`: sacreBLEU cased/lowercase + chrF + length ratio (`:24-32`).
- `rouge`: ROUGE-1/2/L (stemmer) + genPPL com GPT-2 (`:35-55`).
- `exact`: sudoku — `solved %` (igualdade exata), `cell %`, `valid %` (valida linhas/colunas/caixas) (`:58-76`).
- `genppl`: genPPL por seed + entropia unigrama dos tokens; média ± desvio sobre 5 seeds (`:79-107`).
- `genppl_flm`: protocolo FLM — re-escora os **primeiros 128 tokens GPT-2** do texto bruto decodificado, perplexidade de corpus (`:110-151`).
- `gen_ppl.generation_perplexity` (`evaluation/gen_ppl.py:19-148`): NLL apenas nos tokens gerados (offset mapping) para prompts não vazios.

## 9. O que o repositório NÃO libera

- **Treino do tokenizer e do gerador**: não há scripts/flags de treino; `forward()` e as perdas existem como referência, mas o loop de treino, dados intermediários e receitas não estão no clone (`[C]` árvore; `.gitignore:199-224` ignora `experiments/`, `outputs/`, `staging/`, `ablations/`, `logs/`).
- **Baselines**: `.gitignore:219-221` menciona explicitamente "baseline ckpts (29G) and vendored MDLM clone (own .git)" — os baselines de diffusion (MDLM) não vieram.
- **Checkpoints/datasets**: vivem no Hugging Face (`hazyresearch/ncm-checkpoints`, `ncm-datasets`); não baixados (`README.md:38-56,70-75` [R]).
- **Testes/CI/empacotamento**: não há `tests/`, `.github/`, `setup.py`/`pyproject.toml`. `requirements.txt` sem pinos de versão (exceto `transformers>=4.51`).
- Knobs de treino citados (§7) sem implementação liberada.

## 10. Gotchas e observações de engenharia

- `NCP Transformer` no print de parâmetros (`models/next_concept.py:309-310`) — nome interno divergente do branding NCM.
- `frequency_penalty` no YAML é lida como `--freq` na CLI; a "temperatura" só atua no sampling **de códigos** dentro de `generate`; o texto é decodificado por argmax + penalidades.
- Prefixos raw usam embeddings do **encoder do VQVAE** (`raw_token_prefix`), então o vocabulário do prefixo precisa pertencer ao VQVAE (`prefix_pad_token_id` da config).
- Sudoku easy/medium/hard compartilham o mesmo desenho de config; a diferença visível é `model.dropout` (0.2 no easy; 0.1 no medium/hard) — a dificuldade vem dos dados/pesos, não de mudança estrutural `[C]` `config/eval/sudoku-*.yaml:12`.
- Uses de `flash`/`flex_attention` e KV-cache existem mas nenhuma config liberada ativa `use_flex_attention`; o cache é só para o caminho sem `query_level0`.
- `evaluate.py` exige CUDA; não há caminho CPU documentado.
- As configs do repo são declaradas idênticas às `config.yaml` publicadas no HF (`README.md:93` [R]) — duplicação que pode derivar.

## 11. Ponteiros consolidados (evidência do Beta)

- Estágio 1: `models/quant.py` (tudo), `models/vqvae.py:10-141`, `models/vae.py:102-258`.
- Estágio 2: `models/next_concept.py:65-703`, `models/common.py:13-237`.
- Dados/interface: `tokenization/*`, `utils/registry.py`, `utils/misc.py`.
- Avaliação: `evaluate.py`, `scripts/eval_shard.py`, `scripts/eval_merge.py`, `evaluation/gen_ppl.py`.
- Configs: `config/eval/*.yaml` (10 arquivos).
