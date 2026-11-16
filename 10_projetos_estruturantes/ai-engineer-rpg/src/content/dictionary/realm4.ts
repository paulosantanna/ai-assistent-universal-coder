// Fragmento de dicionário do Reino 4 (Braço de Mar): fórmula central e
// exemplo prático de cada termo. Mesclado no glossário por src/content/dictionary/index.ts.

export const realm4Fill: Record<string, { formula: string; example: string }> = {
  'g-prompt-engineering': {
    formula: 'saída ← f(especificação: papel, tarefa, formato, restrições, exemplos); temperatura afia a distribuição: pᵢ(τ) = e^(zᵢ/τ)/Σⱼ e^(zⱼ/τ)',
    example: 'Extração de fatura a τ = 0,5: logits (2,0, 1,0) afiam de p ≈ 0,73 para ≈ 0,88 no formato certo — menos sorteio, mais JSON estável chamada após chamada.',
  },
  'g-structured-output': {
    formula: 'contrato: campo presente ∧ tipo correto ∧ faixa ok; falha na porta vira métrica: taxa de parse = falhas ÷ chamadas',
    example: 'valor = "12,50" como texto reprova no schema e é contado: 200 falhas em 10.000 chamadas = 2%, com dono e causa — nada de conversão silenciosa.',
  },
  'g-rag': {
    formula: 'resposta ← gerador(instruções + trechos recuperados); documento → chunks → embeddings → índice ANN; trocar chunk atualiza a verdade sem tocar pesos',
    example: 'Norma atualizada na semana: substituir o chunk vencido pelo novo atualiza a resposta do sistema em minutos — re-treinar pesos levaria dias e pagaria esquecimento catastrófico.',
  },
  'g-embedding': {
    formula: 'texto → vetor denso de d dimensões; cos(u, v) = (u · v)/(‖u‖ × ‖v‖) — alinhamento de sentido, imune à escala',
    example: '"Onde está minha encomenda" casa com "como rastrear o pedido" por cosseno alto, sem palavra em comum — o sentido mora na direção do vetor, não na grafia.',
  },
  'g-vector-database': {
    formula: 'busca exaustiva: O(n·d) por consulta; índice ANN lê ~nprobe/nlist do espaço, com recall medido contra o vizinho verdadeiro',
    example: '2 milhões de chunks em float32: a exaustiva lê tudo a cada pergunta; o índice ANN lê 1% dos candidatos e responde em dezenas de milissegundos, com recall auditado offline.',
  },
  'g-hybrid-search': {
    formula: 'híbrido(q) = α × BM25(q, d) + (1 − α) × cos(q, d) — concordância lexical + vizinhança de sentido',
    example: 'SKU-83812: o denso traz paráfrases e perde o código; o BM25 acerta a sequência exata — com α = 0,5 os dois caminhos alimentam o mesmo pool de candidatos.',
  },
  'g-reranking': {
    formula: 'score = cross-encoder(query, passagem) lendo o par no mesmo contexto; reordena os k candidatos do índice barato',
    example: 'Top-50 do índice: o cross-encoder relê os 50 pares e sobe quem presta — os 12 acertos do rank 2 elevados ao rank 1 levam o MRR de 0,552 para 0,672.',
  },
  'g-agent-loop': {
    formula: 'passo t: plano → ação(ferramenta, argumentos) → observação → próximo; freios: t ≤ B, ferramenta ∈ lista fechada, estado final definível',
    example: 'Sem freio, 40 chamadas repetidas × US$ 0,006 = US$ 0,24 numa sessão; com orçamento B = 8, o teto é 8 × 0,006 = US$ 0,048 — cinco vezes menos, parado por design.',
  },
  'g-model-context-protocol': {
    formula: 'catálogo: nome, propósito, argumentos tipados e papel autorizado; descoberta + escopo declarado + auditoria de cada chamada',
    example: 'O agente de reembolso expõe 6 ferramentas pelo MCP: o cliente descobre o catálogo, e cada chamada sai registrada — quem chamou, quando, com quais argumentos e qual resultado.',
  },
  'g-lora': {
    formula: 'W ← W₀ + B × A, com base congelada; treináveis = r × (d_in + d_out) contra d_in × d_out da camada cheia',
    example: 'Camada 4096 × 4096 com rank r = 16: 16 × 8.192 = 131.072 parâmetros treináveis — 0,78% (exatamente 1/128) da camada, checkpoint do adaptador em megabytes.',
  },
  'g-quantization': {
    formula: 'memória = N × bytes por peso: FP16 = 2, INT8 = 1, 4 bits = 0,5 — de FP16 para 4 bits, divisão por 4',
    example: 'Base de 7 bilhões de parâmetros: 14 GB em FP16 → 3,5 GB em 4 bits; a QLoRA quantiza a base e treina os adaptadores numa única GPU de consumidor.',
  },
  'g-kv-cache': {
    formula: 'K e V de atenção ficam em cache entre tokens: cada token novo paga só o próprio passo, sem recomputar o passado',
    example: 'Resposta de 500 tokens sobre um prefixo de 30.000: com cache, o prefixo é processado uma vez e cada token da resposta consulta o estoque; sem cache, cada um dos 500 recomputaria atenção sobre o contexto inteiro.',
  },
  'g-mixture-of-experts': {
    formula: 'roteador escolhe top-k entre E especialistas por token: fração ativa k/E dos blocos por inferência; memória residente = modelo inteiro',
    example: '8 especialistas com top-2: cada token paga 2/8 = 25% do bloco — mais capacidade total com menos FLOPs por token; a RAM, porém, continua a do modelo cheio.',
  },
  'g-distillation': {
    formula: 'aluno imita professor: FLOPs por token do aluno ≈ (N_aluno ÷ N_professor) × FLOPs do professor; queda de qualidade medida na régua',
    example: 'Professor de 70B destilado para 7B: o aluno paga 7/70 = 10% dos FLOPs por token — a troca só entra se o conjunto-ouro aceitar a perda.',
  },
  'g-json-schema': {
    formula: 'schema = campos, tipos, faixas e obrigatoriedade; a decodificação restrita limita a amostragem aos tokens compatíveis com o contrato',
    example: 'valor {tipo: número, obrigatório}: o texto "12,50" reprova na validação com campo e valor registrados; a decodificação restrita impede a chave aberta de sair.',
  },
  'g-golden-set': {
    formula: 'nota = casos aprovados ÷ casos curados; toda mudança de prompt, modelo, índice ou guardrail roda na régua antes de ir ao ar',
    example: 'Régua de 200 casos: versão anterior 180/200 = 90% e candidata 178/200 = 89% — dois casos de regressão detectados antes do deploy, não no e-mail do usuário.',
  },
  'g-dpo': {
    formula: 'RLHF: reward model + loop de RL com trava β × KL(π_nova ‖ π_ref); DPO: política ajustada direto sobre pares (preferida, rejeitada)',
    example: '1.000 pares rotulados: 800 para treino e 200 de validação — a adesão às preferências sobe de 60% para 78% (156/200), sem reward model nem fase de RL.',
  },
  'g-prompt-caching': {
    formula: 'sem cache: N chamadas × P tokens de préfill; com cache: P pago uma vez; economia ≈ (N − 1) × P × (1 − desconto)',
    example: 'Prefixo de 30.000 tokens × 5.000 chamadas/dia = 150 milhões de tokens; a US$ 3/M dá US$ 450 — com cache a 10%, ≈ US$ 45: 90% de economia no dia.',
  },
}
