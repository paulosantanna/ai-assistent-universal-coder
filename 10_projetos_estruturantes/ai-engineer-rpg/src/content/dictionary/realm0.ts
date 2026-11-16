// Fragmento de dicionário do Reino 0 (Ilha dos Alicerces): fórmula central e
// exemplo prático de cada termo. Mesclado no glossário por src/content/dictionary/index.ts.

export const realm0Fill: Record<string, { formula: string; example: string }> = {
  'g-linear-algebra': {
    formula: 'cos(u, v) = (u · v) / (‖u‖ × ‖v‖); ‖u‖₂ = √Σuᵢ²',
    example: 'Dois documentos viram vetores (3, 4) e (4, 3): cosseno 24/25 = 0,96 — quase a mesma direção, mesmo com escalas diferentes.',
  },
  'g-gradient': {
    formula: '∇f(x) = (∂f/∂x₁, …, ∂f/∂xₙ); passo: w ← w − η·∇L(w)',
    example: 'Para f(x) = x², o gradiente em x = 3 vale 6; com passo η = 0,05, o próximo ponto é 3 − 0,05×6 = 2,7 — mais perto do fundo do vale.',
  },
  'g-chain-rule': {
    formula: 'dL/dx = (dL/da) × (da/db) × (db/dx) — derivadas locais multiplicadas de trás para frente',
    example: 'Numa rede de 3 camadas, o backward multiplica três derivadas locais e repassa o resultado: é por isso que o código pede apenas loss.backward().',
  },
  'g-bayes-theorem': {
    formula: 'P(H|D) = P(D|H) × P(H) / P(D), com P(D) = P(D|H)·P(H) + P(D|¬H)·P(¬H)',
    example: '1% de fraude e detector de 90%: P(fraude|alerta) = 0,009/0,108 ≈ 8% — dos cem alertas, só nove são fraude de verdade.',
  },
  'g-hypothesis-test': {
    formula: 'p-valor = P(dados tão extremos | hipótese nula verdadeira)',
    example: 'p = 0,03 diz: se a melhoria fosse puro ruído, dados tão bons sairiam em 3% das vezes — não diz que há 97% de chance de melhoria real.',
  },
  'g-entropy': {
    formula: 'H(p) = −Σ pᵢ log₂ pᵢ; máxima na distribuição uniforme',
    example: 'Uniforme em 4 classes: 2 bits de surpresa; concentrada 0,7/0,1/0,1/0,1: só ≈ 1,36 bits — a concentração derruba a incerteza.',
  },
  'g-kl-divergence': {
    formula: 'KL(P‖Q) = Σ pᵢ log(pᵢ/qᵢ) = H(P,Q) − H(P); assimétrica',
    example: 'Aproximar (0,5, 0,5) por (0,9, 0,1) custa ≈ 0,51 nats; o caminho de volta dá outro número — por isso a KL tem seta.',
  },
  'g-numerical-stability': {
    formula: 'softmax estável: e^(zᵢ−m)/Σⱼ e^(zⱼ−m), com m = max(z); ε de float32 ≈ 1,19·10⁻⁷',
    example: 'Logits (1000, 1001, 999) explodem em NaN; subtraindo o máximo viram (−1, 0, −2) e o softmax sai (0,245, 0,665, 0,090) sem estourar.',
  },
  'g-ann': {
    formula: 'busca exaustiva: O(n·d); IVF: lê ~nprobe/nlist do espaço',
    example: '10⁷ vetores de 768 dims na mão: ~7,7·10⁹ distâncias (segundos); IVF com nprobe 10/1000 lê 1% — dezenas de milissegundos.',
  },
  'g-hnsw': {
    formula: 'memória do grafo ≈ n × M × 4 bytes, mais n × d × 4 bytes de vetores',
    example: '2 milhões de vetores de 768 dims: ≈ 5,7 GB de vetores + 256 MB de grafo com M = 32 (512 MB com M = 64).',
  },
  'g-random-seed': {
    formula: 'mesmo seed → mesma sequência do gerador (PCG, Philox, Mersenne)',
    example: 'Duas corridas com seed 42: pesos iniciais, shuffle e curva idênticos — métrica igual até o último dígito.',
  },
  'g-reproducibility': {
    formula: 'checkpoint completo = pesos + otimizador + scheduler + estado RNG; determinismo custa 10–30%',
    example: 'Retomar o treino com checkpoint só de pesos diverge: sem o estado RNG, o shuffle segue outra trajetória.',
  },
}
