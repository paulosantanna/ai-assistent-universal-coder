// Fragmento de dicionário do Reino 5 (Fossa Abissal): fórmula central e
// exemplo prático de cada termo. Mesclado no glossário por src/content/dictionary/index.ts.

export const realm5Fill: Record<string, { formula: string; example: string }> = {
  'g-drift': {
    formula: 'PSI = Σ (pᵢ − qᵢ) × ln(pᵢ/qᵢ); < 0,1 estável, 0,1–0,25 alerta, > 0,25 deriva forte',
    example: 'Referência (0,2, 0,5, 0,3) contra produção (0,35, 0,4, 0,25): PSI ≈ 0,12 — zona de alerta; e 95% do tráfego em 92,8% de acerto com 5% caído para 77,6% mantém a média em 92% sem acusar nada.',
  },
  'g-observability': {
    formula: 'observabilidade = traces + métricas + logs com atributos consistentes (modelo, versão, rota, tokens)',
    example: 'Painel de três eixos: trace de 2,4 s decompõe em retrieve 0,9 s + modelo 1,2 s + parser 0,3 s — cada eixo (qualidade, custo, latência) lê os mesmos atributos.',
  },
  'g-guardrails': {
    formula: 'validação de entrada/saída (PII, tópicos, formato, teto de custo); disparo → métrica → alarme',
    example: 'Teto de US$ 0,02 por requisição: resposta de 2.000 tokens custa US$ 0,01 e passa; requisição de 10.000 tokens custa US$ 0,05 — 2,5× o teto — e é bloqueada com registro.',
  },
  'g-green-ai': {
    formula: 'emissão (kg CO₂e) = energia (kWh) × fator do grid (kg CO₂e/kWh); joules por resposta = FLOPs × joules por FLOP',
    example: 'Treino de 1.000 kWh no grid de 0,4 emite 400 kg CO₂e; na janela limpa (fator 0,1), 100 kg — mesma energia, quatro vezes menos emissão.',
  },
  'g-flops': {
    formula: 'FLOPs por token gerado ≈ 2 × N (N = parâmetros); custo = FLOPs × joules por FLOP',
    example: 'Modelo de 7B gera uma resposta de 500 tokens: 2 × 7 × 10⁹ × 500 = 7 × 10¹² FLOPs por resposta — a moeda física que os joules cobram.',
  },
  'g-function-calling': {
    formula: 'modelo emite {nome da função, argumentos tipados}; código determinístico valida o schema e executa',
    example: 'O modelo devolve {"cidade": "Recife", "dias": 3} para a função previsão(clima); o runtime valida o JSON e chama a API — o modelo nunca executa nada.',
  },
  'g-context-window': {
    formula: 'orçamento de tokens = prompt + contexto recuperado + resposta ≤ janela; custo ∝ tokens usados',
    example: 'Janela de 128.000 tokens: prompt fixo de 20.000 + RAG de 8.000 sobram 100.000 para a resposta — e o cache de prefixo evita reprocessar os 20.000 fixos.',
  },
  'g-distributed-tracing': {
    formula: 'trace = linha do tempo da requisição inteira, composta de spans com duração e atributos',
    example: 'Trace de 2,4 s: retrieve 0,9 s (37,5%), chamada ao modelo 1,2 s (50%), parser 0,3 s (12,5%) — o span engordado aponta onde a resposta engasgou.',
  },
  'g-span': {
    formula: 'span = início + fim + atributos (tokens, modelo e versão, rota/feature, resultado do parser)',
    example: 'Span de retrieve com 0,9 s e 500 tokens recuperados num trace de 2,4 s: 37,5% da latência mora ali, com a conta carimbada no atributo.',
  },
  'g-cost-attribution': {
    formula: 'custo por feature = Σ (tokens de entrada × preço de entrada + tokens de saída × preço de saída) agrupado pela rota',
    example: 'Agente de vendas: 5.000 requisições × (1.200 × US$ 3/M + 400 × US$ 15/M) = US$ 48 no mês — 20% da fatura de US$ 240 para 2% do tráfego.',
  },
  'g-ai-slo': {
    formula: 'SLO de IA = p99 de latência ≤ L, taxa de erro ≤ E (parse, guardrail, timeout), qualidade ≥ piso no golden set',
    example: '10.000 requisições com 300 erros (120 parse + 80 guardrail + 100 timeout) = 3% contra o alvo de 2% — estourado em 1,5 vez, com dono por termo da soma.',
  },
  'g-guardrail-alarm': {
    formula: 'alarme = métrica com limite declarado; disparo → alerta com dono + congelamento do deploy',
    example: 'Flood de 20 requisições/min × 8.000 tokens = 160.000 tokens/min contra o teto de 100.000 por chave — o alarme corta a chave antes de a conta crescer.',
  },
}
