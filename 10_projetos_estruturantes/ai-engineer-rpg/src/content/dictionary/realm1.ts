// Fragmento de dicionário do Reino 1 (Porto dos Dados): fórmula central e
// exemplo prático de cada termo. Mesclado no glossário por src/content/dictionary/index.ts.

export const realm1Fill: Record<string, { formula: string; example: string }> = {
  'g-version-control': {
    formula: 'resultado ← f(código@commit, dados@hash, seed, ambiente@imagem); 3⁸ = 6.561 combinações sem pinar, 1 com lockfile',
    example: 'Duas máquinas, mesma seed 42: 0,82 contra 0,79 — sem container e lockfile, cada uma escolheu livremente entre as 6.561 combinações; a imagem pinada derruba para 1.',
  },
  'g-container': {
    formula: 'mesma imagem → mesmo runtime: notebook, cluster e produção idênticos; combinações de ambiente = 1',
    example: 'O treino roda com a mesma imagem no notebook e no cluster: as versões pinadas eliminam o "funciona na minha máquina" e a divergência de acurácia entre máquinas.',
  },
  'g-rest-api': {
    formula: 'contrato = recursos + verbos + status honestos (2xx/4xx/5xx) + schema; idempotência: n chamadas = 1 efeito',
    example: 'Retry após timeout sem chave de idempotência registra 3 × R$ 50 = R$ 150; com a chave, o efeito único fica em R$ 50 — e a entrada inválida sai em 422, não em 200.',
  },
  'g-data-leakage': {
    formula: 'ajuste ← treino; aplicação ← treino e teste; fold temporal: treino {t ≤ t₀}, validação {t > t₀}',
    example: 'Normalizar com μ = 50 e σ = 10 do treino: o valor 70 do teste vira (70 − 50)/10 = 2,0 — calcular μ com treino+teste misturados vaza o teste para dentro do treino.',
  },
  'g-etl': {
    formula: 'ETL: extrair → transformar → carregar; ELT: carregar primeiro, transformar no warehouse; idempotência: estado(2 execuções) = estado(1)',
    example: 'A falha de infraestrutura rodou a carga 2×: 100.000 linhas viram 200.000; o dedupe por chave única devolve exatamente 100.000 — rerun seguro.',
  },
  'g-data-privacy': {
    formula: 'processamento permitido ⇔ base legal; coletado ≤ justificado (minimização); titular: acesso, correção, exclusão',
    example: 'Dataset de treino com dados pessoais sem base legal é violação desde a coleta — apagar os dados depois do treino não desfaz o processamento já feito.',
  },
  'g-data-contract': {
    formula: 'contrato = (schema, domínio de valores, nulidade ≤ teto, faixa, semântica, prazo); violação → bloqueio na porteira',
    example: 'Campo "preço" (decimal, 0 a 100.000) recebe texto com símbolo em 2% de 50.000 registros = 1.000 violações: a carga quebra na entrada e o alerta acorda o dono da fonte.',
  },
  'g-schema-validation': {
    formula: 'registro entra sse tipo ∧ domínio ∧ nulidade ∧ faixa ok; fail-closed: violar = bloquear + alertar',
    example: 'O contrato permite 1% de faltantes e a carga chega com 10%: bloqueada na doca, com mensagem apontando o campo — nada corrompido chega ao treino.',
  },
  'g-feature-store': {
    formula: 'features(exemplo) = valores com t ≤ t₀ (point-in-time); uma única definição de código para treino e serving',
    example: 'Reclamações nos 30 dias: o join sem carimbo pega 5 reais + 3 futuras = 8; com carimbo em t₀, o exemplo vê só 5 — o futuro não entra como sinal.',
  },
  'g-data-versioning': {
    formula: 'commit ↔ hash do dataset (ponteiro DVC); dataset(hash) devolve os mesmos bytes',
    example: 'O experimento anota o hash do dataset na linha do commit: reexecutar o download repõe exatamente aqueles bytes, não uma prima semelhante de outro disco.',
  },
}
