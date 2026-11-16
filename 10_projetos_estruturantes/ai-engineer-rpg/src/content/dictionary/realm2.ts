// Fragmento de dicionário do Reino 2 (Floresta dos Modelos): fórmula central e
// exemplo prático de cada termo. Mesclado no glossário por src/content/dictionary/index.ts.

export const realm2Fill: Record<string, { formula: string; example: string }> = {
  'g-overfitting': {
    formula: 'diagnóstico nas curvas: treino desce, validação abre e sobe = superajuste; freio: L(θ) = perda(θ) + λ·Ω(θ)',
    example: 'Treino cai de 0,40 a 0,10 enquanto a validação sobe de 0,55 a 0,90 — o modelo decorou; early stopping encerra na época em que a validação parou de melhorar.',
  },
  'g-regularization': {
    formula: 'L(θ) = perda(θ) + λ·Ω(θ), com λ ajustado na validação; árvores: profundidade limitada e mínimo por folha; redes: dropout p no treino',
    example: 'Peso w = 0,01 com λ = 0,1 e η = 0,1: o freio L2 retira 0,0002 por passo (nunca zera); o L1 retira 0,01 e escreve w = 0 — o atributo sai do modelo.',
  },
  'g-cross-validation': {
    formula: 'μ = (1/k) Σ métricaᵢ; σ = √((1/k) Σ (métricaᵢ − μ)²); split por grupo: grupos(treino) ∩ grupos(validação) = ∅',
    example: 'Quatro folds: 0,72, 0,68, 0,71, 0,69 → 0,70 ± 0,016 — reporte a dupla, não o fold mais bonito; cliente com 20 linhas e split 80/20 fica dos dois lados da cerca em ~99% dos casos.',
  },
  'g-precision-recall': {
    formula: 'precisão = VP/(VP+FP); recall = VP/(VP+FN); F1 = 2·(P×R)/(P+R)',
    example: '10.000 transações com 20 fraudes: VP 12, FP 40, FN 8 → precisão 12/52 ≈ 0,23 e recall 12/20 = 0,60 — mais de três falsos alertas por fraude real.',
  },
  'g-roc-auc': {
    formula: 'área sob TPR × FPR, com FPR = FP/(FP+VN); qualidade de ordenação independente de corte',
    example: 'Fraude de 0,2%: FPR = 40/9.980 ≈ 0,4% deixa a ROC ótima enquanto a precisão fica em 0,23 — a curva PR é a régua honesta com poucos positivos.',
  },
  'g-calibration': {
    formula: 'risco prometido p → frequência observada ≈ p; Brier = média de (p − y)²',
    example: '100 clientes prometidos a 0,8 de risco: 80 deveriam inadimplir; inadimpliram 30 — superestimação de 0,5, corrigível com isotônica ou Platt.',
  },
  'g-gradient-boosting': {
    formula: 'resíduo rᵢ = yᵢ − Fₘ₋₁(xᵢ); estágio: Fₘ = Fₘ₋₁ + η·hₘ(x); parada pela validação, não pela exaustão',
    example: 'Alvos 50, 80, 110 e base 80: resíduos −30/0/+30; com η = 0,1, F₁ = 77/80/83 e o erro residual vira −27/0/+27 — a conta anda em passos pequenos.',
  },
  'g-pca': {
    formula: 'componentes = autovetores da matriz de covariância; variância explicada = λᵢ/Σλⱼ',
    example: 'Autovalores 4, 2, 1, 1 (total 8): PC1 explica 4/8 = 50%, PC2 2/8 = 25% — os dois primeiros preservam 75% da variância.',
  },
  'g-class-imbalance': {
    formula: 'acurácia engana: em 99/1, responder "não" já dá 99%; peso balanced: wᶜ = n/(k·nᶜ); métricas medidas sobre a classe rara',
    example: '10.000 linhas com 100 fraudes: peso da fraude 10.000/(2×100) = 50 contra ≈ 0,51 da legítima — cada raro pesa 99× na perda.',
  },
  'g-smote': {
    formula: 'sintético ← xᵢ + λ·(v − xᵢ), com λ ∈ [0,1] e v vizinho k-NN da mesma classe; só dentro do fold de treino',
    example: 'Raro (30, 4) com vizinho (36, 2) e λ = 0,5 → sintético (33, 3); no dataset inteiro antes do split, os sintéticos cruzam treino e validação e a estimativa infla.',
  },
  'g-shap': {
    formula: 'φᵢ = média da contribuição marginal sobre as coalizões; a soma fecha a conta: f(x) = v(∅) + Σᵢ φᵢ',
    example: 'Baseline 0,30, renda +0,20, idade −0,05, demais +0,10 → predição 0,55 — a soma das contribuições explica a decisão do caso.',
  },
  'g-permutation-importance': {
    formula: 'impᵢ = métrica original − métrica com a coluna i embaralhada, medida na validação',
    example: 'AUC 0,85 na validação: embaralhar "renda" → 0,70 (queda de 0,15); embaralhar "idade" → 0,845 (queda de 0,005) — renda pesa 30× a idade.',
  },
  'g-l1': {
    formula: '‖w‖₁ = Σ|wᵢ|; freio: gradiente λ·sign(w) — passo constante que cruza o zero → esparsidade',
    example: 'w = 0,01 com λ = 0,1 e η = 0,1: o freio retira 0,01 e escreve w = 0 — o atributo sai do modelo; o L2, no mesmo caso, deixaria 0,0098.',
  },
  'g-l2': {
    formula: '‖w‖₂ = √Σwᵢ²; freio: gradiente 2λw — encolhe proporcional ao peso, nunca zera',
    example: 'w = 0,01: o freio retira 2×0,1×0,01×0,1 = 0,0002 por passo — w desliza para 0,0098 e continua vivo no modelo.',
  },
}
