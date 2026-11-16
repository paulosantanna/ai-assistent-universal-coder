# Mapeamento Celta — NCM por dentro: mecanismo, comparação e crítica

**Nível:** 3 de 3 (o mais profundo) · **Updated:** 2026-10-21
**Alvo:** `02_repositorios/ncm` @ `c702742` · **Pacote:** [`README`](README.md) → [`Alpha`](alpha.md) → [`Beta`](beta.md) → **Celta**

> Pressupõe Alpha e Beta. Aqui: (1) a mecânica matemática dos dois estágios como evidenciada no código, (2) a contagem real de avaliações por geração, (3) a comparação honesta com LLMs autoregressivos e diffusion LMs, e (4) vantagens e desvantagens etiquetadas por tipo de evidência (`[C]` código · `[R]` README · `[X]` paper/blog oficiais · `[I]` inferência · `[REP]` reprodução local). O mapeamento foi somente leitura; a reprodução de sudoku-hard (86,25%) está registrada em `.work/ncm-repro/RESULTADO.md`.

---

## 1. Estágio 1 — como a hierarquia coarse-to-fine é construída

### 1.1 A recursão residual multiescala

Sejam `z ∈ R^{L×C}` a saída do encoder do VQ-VAE (sequência completa, ex. L=48 em XSum) e níveis `ℓ₁ < ℓ₂ < … < ℓ_K` (ex. `[4,6,…,48]`). O quantizador constrói a hierarquia iterando (`models/quant.py:573-632`):

```
z_hat ← 0                      (reconstrução acumulada, resolução L)
z_rest ← z                     (resíduo a explicar)

para cada nível i = 1..K:
    a_i  = down_i(z_rest)                  # p/ nível no comprimento ℓ_i
    c_i  = argmin_j || a_i − E_i[j] ||²    # código mais próximo no codebook i
    q_i  = up_i(E_i[c_i])  →  Phi_i(q_i)   # volta à resolução L + conv residual
    z_hat ← z_hat + q_i                    # acumula
    z_rest ← z_rest − q_i                  # sobra o que ainda não foi explicado
```

- `down_i`: nível 0 usa **convolução aprendida** (cascata, init = average-pool) quando `learned_l1_sampling: true`; níveis > 0 usam `F.interpolate(mode="area")` (`:395-402`).
- `up_i`: nível 0 usa convolução transposta aprendida (init = repetição); níveis > 0 usam interpolação linear (`:404-411`).
- `Phi_i`: conv 1-D com "mistura residual" `h·(1−r) + Conv1d(h)·r`, `r = 0.5` nas configs liberadas (`:11-38`, `:380-386`) — dá ao código quantizado uma correção local suave antes de somar.
- **O último nível não faz down/up**: quantiza o resíduo final já na resolução plena (`:472-475`, `:507-510`).

**Leitura:** cada nível responde à pergunta "o que ainda falta explicar, nesta escala?" — é *residual* no sentido de que cada codebook só é responsável pelo erro remanescente dos anteriores. `z_hat` após o nível i é a reconstrução acumulada (é isso que o decoder do VQ-VAE usa para reconstruir texto em qualquer ponto da hierarquia).

### 1.2 Treino do quantizador (o que o código mostra)

- Codebooks **não são treinados por gradiente**: são atualizados por EMA de atribuições (`:485-500`); há suporte a `kmeans_init` e reinício de códigos mortos (`:344-378`, `:436-446`).
- Perda por nível: `commitment_cost·MSE(z_hat.detach(), z) + MSE(z_hat, z_no_grad)`, média sobre níveis (`:519-524`).
- **Straight-through só no nível 0** (quando `learned_l1_sampling`); comentário do próprio código: nos níveis altos o estimador "diverge em ~100 passos" (`:503-505`).
- **`fine_drop` ≈ nested dropout do paper/blog**: com probabilidade `p` (0.5 nas configs), o `z_hat` de treino é truncado num nível aleatório ≥ `min_keep`, forçando o decoder a funcionar com hierarquias parciais (`:457-462`, `:525-530`). É o que garante que níveis grossos sejam "autossuficientes" e que a geração possa parar antes do fim sem colapsar.
- Objetivo de reconstrução é **token-level** (o decoder prevê os ids do pré-tokenizer; argmax na decodificação) — blog [X]; código `models/vae.py:233-258`, `models/vqvae.py:107-118`.

### 1.3 O que o paper/blog acrescentam (e o repo não contém)

- Herança do **VAR** (geração visual coarse-to-fine): adaptação para texto = codebook por nível + nested dropout + reconstrução de tokens [X, blog].
- O treino completo do tokenizer **não está no clone**; as fórmulas acima são as que o código de referência implementa, e as perdas/losses existem para serem usadas por um loop de treino não liberado `[C]`+`[I]`.
- Consequência estrutural: o tokenizer é **congelado** no estágio 2 (`models/next_concept.py:80-84`) e treinado só por reconstrução — não pela utilidade da geração. O próprio time lista "treinar tokenizer e gerador conjuntamente" como trabalho futuro [X, blog] `[I]`.

## 2. Estágio 2 — como o gerador prevê a hierarquia

### 2.1 Condicionamento: "próximo conceito" = reconstrução acumulada reamostrada

Para prever o nível `i+1`, o modelo não vê os *códigos* anteriores, e sim a **reconstrução contínua acumulada** `z_hat(i)` reamostrada para `ℓ_{i+1}` posições (`get_next_autoregressive_input`, `models/quant.py:696-709`; treino equivalente em `idx_to_ncm_input :670-694`). O transformer projeta esse sinal com `wte` (Linear `embed_dim → n_embd`) e soma um **level embedding** (`models/next_concept.py:129-133`, `:197-200`, `:664-670`).

- **RoPE reinicia por nível**: prefixo em `[0..P-1]`, cada nível-alvo em `[0..ℓ_i-1]` (`:94-117`). O modelo compara posições *relativas dentro do nível corrente*, não posições absolutas num fluxo único — coerente com a ideia de que um nível é uma "imagem" da mesma sequência em outra resolução.
- **Atenção block-diagonal**: cada nível-alvo vê o prefixo e **apenas a si mesmo** (paralelo intra-nível) (`:266-292`, `:312-337`). A variante `block_causal` (ver níveis anteriores) existe, mas nenhuma config liberada a usa.

### 2.2 Treino em um único forward (e robustez a erro)

- O `forward()` monta `[prefixo; todos os níveis]` e computa logits de todos os níveis numa passada, com a máscara block-diagonal (`:376-464`) — "train on all levels in a single forward pass" [X, blog].
- **Corrupção de códigos condicionantes** no treino (robustez a erros de geração nos níveis anteriores): blog [X]; a config LM1B carrega `aux.code_corruption` (`random_rate`, `low/high`, `skip_level0`), mas **não há implementação no código liberado** — evidência de configuração de treino fora do release `[C]` `config/eval/lm1b-*.yaml:118-124`.
- Erros de geração se **acumulam** por construção (cada nível condiciona o próximo sobre a própria geração anterior); `code_corruption` é a defesa declarada contra isso [X] `[I]`.

### 2.3 Inferência: K avaliações, paralelismo intra-nível

Laço `generate()` (`:659-694`): para cada nível, monta a entrada condicionada, roda o stack, e **amostra todas as posições do nível simultaneamente**. O custo sequencial é o nº de níveis, não o nº de tokens. Contagem efetiva por task (código `[C]` + blog Sudoku=12 NFE `[X]`):

| Task | K níveis | Nível 0 | Forwards do gerador |
|------|----------|---------|---------------------|
| Sudoku (e/m/h) | 12 | queries (`query_level0`) | **12** (confere com o blog) |
| XSum | 9 | queries | 9 |
| WMT14 | 11 | previsto do prefixo (`predict_level0`) | 11 |
| TinyStories / LM1B | 12 | dado (unigrama) ou queries | 11–12 |
| OpenWebText | 32 | dado (unigrama) | 31 |

Para comparação: um LLM autoregressivo gasta ~1 avaliação por token (XSum gera até ~60 tokens → dezenas–centenas de passos); diffusion LMs gastam M passos de sequência cheia [X].

### 2.4 Detalhes que definem qualidade na prática

- **Cabeças atadas ao codebook** (XSum/TinyStories/OWT): o logit de um código é calculado como `2·(Wz)·E_i − ||E_i||²` escalado (`_TiedCodebookHead`, `:9-34`) — um **classificador geométrico** (softmax sobre similaridade), reutilizando os próprios vetores do codebook. Em Sudoku/LM1B usam-se cabeças Lineares/shared.
- **CFG com rampa por nível**: duplica o batch com um prefixo nulo; a mistura `(1+t)·doc − t·nulo` cresce linearmente com o nível (`t = scale·i/(K−1)`, `:477-485`, `:529-540`). Efeito de desenho: **forte orientação nos níveis grossos** (planejamento global) e fraca nos finos (liberdade de detalhe).
- **Estratégias de nível 0**: queries aprendidas (1 pass paralelo), previsão do fim do prefixo (WMT14) ou amostragem do **unigrama salvo no checkpoint** (`inference.level0_unigram`, tasks incondicionais) — o nível 0 não é "texto", é o esboço latente.
- **Sampling em dois lugares**: códigos são amostrados no `generate` (temperature/top-k/top-p por task); o **texto final** é decodificado por argmax do decoder + **penalidades empíricas** aplicadas na avaliação (`pick_tokens`, `scripts/eval_shard.py:99-124`): penalidade de frequência acima de cota por token (`frequency_allowance` do checkpoint; 11.5 no LM1B, 2.0 no XSum) + penalidade de adjacência por janela com decaimento (`10,4,0.5` no LM1B; `5,4,0.5` no XSum) `[C]` `[I]`. Penalidades agressivas sugerem tendência a repetição/colapso quando se amostra cru de código `[I]`.

## 3. Comparação estrutural: LLM autoregressivo × Diffusion LM × NCM

| Dimensão | Autoregressivo (LLM) | Diffusion LM | NCM |
|----------|----------------------|--------------|-----|
| Unidade de geração | 1 token | sequência inteira (ruído→dado) | 1 nível coarse-to-fine (ℓ_i códigos paralelos) |
| Ordem | estritamente causal (token a token) | global, iterativa | grosso→fino, hierárquica |
| Passos sequenciais | L (nº tokens) | M (dezenas–centenas) | **K (nº níveis: 9–32 nas tasks)** `[C]` |
| Custo por passo | cresce com contexto (KV-cache ajuda) | **sequência inteira em todo passo** [X] | cresce com o nível; passos iniciais curtíssimos [X] |
| Planejamento global | emergente, sem etapa de "plano" | refino global pode ajudar | **explícito**: esboço latente antes do detalhe [X] |
| Robustez a erro local | erro contamina o que vem depois | revisível em passos seguintes | erro no nível contamina níveis finos; mitigado por corrupção no treino [X] |
| Treino | next-token, altíssima inércia de ecossistema | exige pacotes de dados maiores [X] | tokenizer + gerador; **4–5× menos tokens** que DLM fortes [X] |
| Ecossistema de inferência | maduro (batching, KV-cache, serving) | menos maduro | **imatura**; repo é pesquisa `[C]` |
| Alinhamento (RLHF/instrução/chat) | extenso | emergente | **inexistente** no release [C] |
| Escala demonstrada | centenas de bilhões | bilhões | **97M–725M** (blog) `[X]` |
| Natureza dos "tokens" | vocabulário de texto | vocabulário de texto | **códigos latentes por nível** (não são palavras) |

Números de qualidade reportados [X] (sudoku-hard conferido localmente `[REP]`; os demais não reproduzidos):

| Métrica | Baseline forte | NCM |
|---------|----------------|-----|
| genPPL LM1B (mesma escala) | DLM forte | melhor, **21× mais rápido** (H100 SXM) |
| genPPL OWT | DLM forte | comparável, **10× mais rápido** |
| ROUGE-L XSum | DLM forte | igualado, **31× mais rápido** |
| Sudoku easy / medium / hard (% resolvido) | AR: 14.6/5.1/1.0 · MDLM: 92.0/77.1/30.2 · DUO: 96.3/84.7/58.4 · FMLM+: 97.7/92.8/81.3 | **99.5 / 96.5 / 86.1** (12 NFE) |
| Treino (tokens) vs DLM | — | **~4.9× (LM1B) / ~4× (OWT) menos** |

> Divergência registrada: `README.md:30` diz "9–31×"; paper/blog dizem 21×/10×/31× ("10–31×") [X] `[C]`. Números de **velocidade** não reproduzidos.

## 4. Vantagens do NCM (com base de evidência)

1. **Latência de geração muito menor** em escala de pesquisa: K passos em vez de dezenas–centenas; e os primeiros passos são baratíssimos (sequências de 1–16 posições) `[X]` `[C]`.
2. **Paralelismo intra-nível**: cada nível é gerado de uma vez; não há dependência token a token dentro do nível `[C]`.
3. **Planejamento global explícito**: o esboço de baixa resolução é decidido antes dos detalhes — casa com o ganho grande em Sudoku (86.1% hard vs 1.0% AR, 30.2% MDLM) `[X]`.
4. **Eficiência de treino**: ~4–5× menos tokens que DLMs fortes, contando tokenizer + gerador `[X]`.
5. **Curva de qualidade × custo melhor que DLM** nas tasks avaliadas (mesma escala de parâmetros) `[X]`.
6. **Escala de tempo de teste amigável**: geração rápida ⇒ mais candidatos dentro do mesmo orçamento; MBR melhora BLEU/ROUGE e vence baselines no mesmo wall-clock `[X]`.
7. **Arquitetura simples e reaproveitável**: transformer padrão (RoPE, qk-norm, GQA, SDPA/flex) + VQ-VAE; sem kernels exóticos; roda 1 GPU por shard `[C]`.
8. **Refinamento interpretável**: dá para decodificar cada nível e ver o texto "ganhando forma" (ex. BLEU 77.8 no nível 11/11 no exemplo alemão→inglês) `[X]` `[C]`.
9. **Sem dependência de alinhamento/texto**: funciona com alfabetos não-textuais (Sudoku usa "alfabeto" de 12 símbolos e codebooks de 16) `[C]`.
10. **Licença MIT e checkpoints públicos** (HF) — barreira baixa para pesquisa `[R]` `[X]`.

## 5. Desvantagens, limitações e riscos (com base de evidência)

1. **Pipeline de dois estágios acoplado**: tokenizer congelado, treinado só por reconstrução; representações não otimizadas para a geração; treino conjunto é explicitamente "trabalho futuro" `[X]` `[C]`.
2. **Sem código de treino**: o release é inferência/avaliação; reproduzir os checkpoints exige reimplementar tokenizer, gerador, dados e corrupção `[C]`.
3. **Escala não demonstrada**: resultados até 725M parâmetros em bancos pequenos; nada indica que o paradigma se sustenta em escala LLM (questão aberta nº 1 do próprio time) `[X]`.
4. **Sem alinhamento/instrução/chat**: nenhuma pista de SFT, RLHF, diálogo ou seguimento de instruções; não é concorrente direto de um LLM de produto `[C]` `[I]`.
5. **Computação fixa por exemplo**: sempre K níveis; não há parada/realocação adaptativa por dificuldade (também trabalho futuro) `[X]`. Outputs curtos pagam a hierarquia inteira `[I]`.
6. **Qualidade depende de heurísticas de sampling**: penalidades de frequência/adjacência calibradas por task (2.0/5,4,0.5 no XSum; 11.5/10,4,0.5 no LM1B) e unigramas salvos no checkpoint — indicador forte de fragilidade da amostragem crua `[C]` `[I]`.
7. **Erros compõem entre níveis**: condicionamento na própria geração anterior; a mitigação (corruption) não está no código liberado `[X]` `[C]`.
8. **Sem ecossistema de serving**: sem batching contínuo/KV-cache eficiente para o caminho de queries (o KV-cache é proibido com `query_level0`, `:523-524`), sem quantização documentada, sem API `[C]`.
9. **Avaliação cara e específica de GPU**: exige CUDA; protocolos próprios (genPPL, FLM de 128 tokens, exact de Sudoku); comparações com AR limitadas a Sudoku e a baselines pré-instrução `[C]` `[X]`.
10. **Reprodutibilidade frouxa**: dependências sem pinos (exceto `transformers>=4.51`), sem testes/CI, configs duplicadas (repo e HF podem divergir), knobs de treino sem implementação `[C]`.
11. **Comprimento fixo por task**: a hierarquia (e o comprimento máximo) é definida em config; não há geração aberta de comprimento variável como num LLM (EOS é tratado no texto decodificado) `[C]` `[I]`.
12. **Ganho em linguagem ≠ ganho em tudo**: genPPL é reconhecidamente imperfeito; o próprio blog cita essa crítica; XSum/OWT são "comparáveis" (não superiores) aos DLMs `[X]`.

## 6. Quando usar / quando não usar (leitura prática)

- **Faz sentido explorar**: geração rápida em tarefas fechadas/de domínio (sumarização curta, tradução, formatos estruturados como Sudoku), pesquisa em alternativas a AR/diffusion, cenários com orçamento de treino pequeno, laboratório com 1 H100/GPU equivalente.
- **Não é substituto hoje de**: LLM de chat/instruções, geração longa aberta, ecossistema de produção com serving maduro, qualquer deploy sem GPU.
- **Barreira prática principal**: ausência de treino + tooling; usar NCM "de verdade" significa (a) consumir checkpoints por task como estão, ou (b) reimplementar o pipeline de treino `[I]`.

## 7. Estado e próximos passos do projeto (como o time enquadra)

Trabalho futuro declarado [X, blog]: (1) escalar (parâmetros, FLOPs, tokens); (2) treinar tokenizer+gerador conjuntamente; (3) computação adaptativa por dificuldade. Implicação `[I]`: o próprio time trata o estado atual como **prova de conceito promissora**, não como arquitetura fechada.

## 8. Perguntas abertas e incertezas deste mapeamento

- Latência **não reproduzida**; qualidade **parcialmente reproduzida**: sudoku-hard = **86,25% (1725/2000)** vs 86,1% do blog (2026-10-21) `[REP]`; demais tasks não executadas.
- A implementação da `code_corruption` (treino) e do `fine_drop dual` (LM1B) não está no clone — o impacto real desses mecanismos não pode ser medido localmente.
- O comportamento fora das 8 tasks liberadas (contexto longo, texto livre, instruções) é desconhecido.
- A divergência "9–31×" (README) vs "10–31×"/21–10–31× (paper/blog) não foi resolvida — provavelmente versões diferentes do texto `[I]`.

## 9. Resumo executivo (o que reter)

1. NCM troca "próximo token" por "próximo conceito": hierarquia residual multiescala (VQ-VAE) + geração de um nível inteiro em paralelo por passo; **K passos, não L tokens** `[C]`.
2. Ganha em **velocidade (10–31×)** e **eficiência de treino (4–5× menos tokens)** com qualidade comparável/melhor que DLMs; salto grande em raciocínio estruturado (Sudoku) `[X]` — hard conferido localmente: **86,25%** `[REP]`.
3. É **pesquisa em estágio inicial**: escala até 725M, sem instrução/chat, sem treino no repo, dependente de heurísticas de sampling `[C]` `[X]`.
4. O que o NCM ensina ao campo: hierarquia coarse-to-fine + paralelismo intra-nível é uma terceira via viável entre AR e diffusion, e o "planejamento antes do detalhe" tem efeito real em tarefas com restrições globais `[X]` `[I]`.
5. Para este workspace: ótimo objeto de estudo de *arquiteturas alternativas de geração*; adoção prática condicionada a checkpoints por task + GPU + aceitação da ausência de pipeline de treino `[I]`.
