// Fragmento de dicionário do Reino 3 (Caverna das Redes): fórmula central e
// exemplo prático de cada termo. Mesclado no glossário por src/content/dictionary/index.ts.

export const realm3Fill: Record<string, { formula: string; example: string }> = {
  'g-backpropagation': {
    formula: 'por nó: ∂L/∂x = ∂L/∂y × ∂y/∂x — derivada local × gradiente upstream, percorrendo o grafo em ordem topológica',
    example: 'Nó y = z² com z = 3 e ∂L/∂y = 4 chegando de cima: derivada local 2×3 = 6, e 6 × 4 = 24 repassado para baixo — a regra da cadeia em uma multiplicação.',
  },
  'g-batch-normalization': {
    formula: 'lote no treino: (x − μ_B)/√(σ²_B + ε); inferência usa running stats congeladas (modo eval)',
    example: 'Batch de 32: média e variância do lote normalizam cada passo do treino; na inferência, amostra única sai pelas estatísticas acumuladas — normalizar por lote de tamanho 1 instabiliza a saída.',
  },
  'g-attention': {
    formula: 'Atenção(Q, K, V) = softmax(Q·Kᵀ/√d_k)·V; custo O(n²·d) na janela de n tokens',
    example: 'Scores (16, 8, 0) com d_k = 64: divididos por √64 = 8 viram (2, 1, 0) → softmax (0,665, 0,245, 0,090) — a saída do token é essa mistura dos Values.',
  },
  'g-transformer': {
    formula: 'bloco = atenção multi-cabeça + FFN por posição (interna 4 × d_model), ambos com residual e normalização; h cabeças: d_k = d_model/h',
    example: 'd_model = 512 com 8 cabeças: d_k = 512 ÷ 8 = 64 e concatenação de 8 × 64 = 512; as projeções Q, K, V e saída somam 4 × 512² ≈ 1 milhão de pesos.',
  },
  'g-tokenization': {
    formula: 'texto → IDs pelo vocabulário; BPE funde o par mais frequente; vocabulário maior = menos tokens por texto, matrizes 2 × V × d maiores',
    example: 'Palavra comum sai em 1 token, rara em 3 pedaços — a fatura da API e o erro de contagem de letras nascem desse recorte, não do modelo.',
  },
  'g-scaling-law': {
    formula: 'Chinchilla (compute-optimal): tokens ≈ 20 × parâmetros; perda cai como lei de potência em parâmetros, dados e computação',
    example: 'Modelo de 220M de parâmetros pede ≈ 20 × 220M = 4,4 bilhões de tokens; treinar com 440M é subalimentar em dez vezes — plateau cedo, antes de suspeitar da arquitetura.',
  },
  'g-temperature': {
    formula: 'softmax(z/T): T < 1 afia, T > 1 aplana, T → 0 vira argmax',
    example: 'Logits (2, 1, 0): com T = 1 sai (0,665, 0,245, 0,090); com T = 2 abre a roleta para (0,506, 0,307, 0,186) — mais surpresa, mais risco de divagação.',
  },
  'g-bpe': {
    formula: 'a cada passo, funde o par de símbolos mais frequente até o vocabulário alvo; frequente → 1 token, raro → fragmentos',
    example: '"th" com 500 ocorrências vence o par com 3 e funde primeiro; "the" vira token único — letras e dígitos contados sobre IDs, não sobre caracteres visíveis.',
  },
  'g-positional-encoding': {
    formula: 'RoPE: gira Q e K por θ_m = m·ω; o produto interno depende de m − n (distância relativa); sinusoidal soma sin/cos; aprendida é tabela limitada ao treino',
    example: 'Passo de 30°: Q na posição 5 gira 150°, K na 3 gira 90° — produto cos(150° − 90°) = cos 60° = 0,5; mover a Key para a posição 4 muda para cos 30° = 0,866.',
  },
  'g-sampling-strategies': {
    formula: 'greedy: argmax; top-k: corte fixo de k; top-p: menor conjunto com Σpᵢ ≥ p; penalidade de repetição divide o logit dos tokens usados',
    example: 'Distribuição (0,60, 0,25, 0,10, 0,05) com top-p 0,90: 0,60 → 0,85 → 0,95 fecha com 3 candidatos; um top-k = 2 jogaria fora 0,15 de cauda sem olhar a forma.',
  },
  'g-masking': {
    formula: 'causal: score futuro ← −∞ antes do softmax (peso 0); padding: tokens falsos fora da atenção e da perda; MLM: buracos no meio ao estilo BERT',
    example: 'No passo 3 do decoder, os scores dos passos 4 e 5 recebem −∞ e saem peso zero — sem a máscara causal, o treino espiaria a resposta que deve prever.',
  },
}
