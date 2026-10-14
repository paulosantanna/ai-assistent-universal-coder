# PATTERNS.md

- **Bridge pattern:** Ao conectar dois sistemas de simulação (digital_twin ↔ physiological_kernel), usar adapter separado que computa campos derivados (HOMA-IR, pancreatic_function) em vez de exigir correspondência exata de schemas.
- **Longitudinal simulation:** TrialSimulator deve sempre iterar por `duration_weeks * 7` dias com `MealSequenceGenerator` para refeições realistas.
- **ODE safety:** RK4 em modelos fisiológicos requer clamping nos estados e taxas intermediárias para evitar overflow sob condições extremas (alta IR, T2DM avançado).
