// Fragmento de dicionário do Reino 6 (Laboratório de Otimização): fórmula central e
// exemplo prático de cada termo. Mesclado no glossário por src/content/dictionary/index.ts.

export const realm6Fill: Record<string, { formula: string; example: string }> = {
  'g-ab-test': {
    formula: 'n por braço ≈ 16σ²/Δ² (α = 5%, poder 80%); aprovação = primária melhora E guardas dentro do limite',
    example: 'σ = 400 ms e Δ = 100 ms no p99: n ≈ 16 × 400²/100² = 256 consultas por braço — a 20 por dia, uns 13 dias de teste.',
  },
  'g-statistical-power': {
    formula: 'poder = 1 − β; com a amostra fixada, MDE ∝ 1/√n',
    example: 'Poder 40% afoga 6 de cada 10 efeitos reais; dobrar a amostra encolhe o MDE para ≈0,71 do valor (1/√2).',
  },
  'g-carbon-budget': {
    formula: 'kg CO₂ = kWh × fator da matriz; kWh = FLOPs / (FLOPs por joule × 3,6·10⁶)',
    example: 'Treino de 4·10¹⁹ FLOPs a 10¹² FLOPs por joule: 11,1 kWh; a 0,4 kg/kWh emite 4,4 kg — na janela limpa (0,1), 1,1 kg.',
  },
  'g-cost-model': {
    formula: 'custo por consulta = (t_in/1000) × p_in + (t_out/1000) × p_out + ferramentas + infra',
    example: '1.000 tokens de entrada × R$ 0,002/1k + 300 de saída × R$ 0,006/1k + ferramenta R$ 0,001 + infra R$ 0,0004 = R$ 0,0052 por resposta satisfeita.',
  },
  'g-mde': {
    formula: 'MDE ∝ 1/√n: Δ₂ = Δ₁ × √(n₁/n₂)',
    example: 'MDE 8% com 200 consultas por braço; para detectar 0,3%, n = 200 × (8/0,3)² ≈ 142 mil por braço — quase dois anos a 200 por dia.',
  },
}
