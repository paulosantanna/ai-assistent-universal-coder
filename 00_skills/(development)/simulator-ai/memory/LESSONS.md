# LESSONS.md

## 2026-07-12 — Simulador AIDiabetic: bridge digital_twin ↔ novo kernel fisiológico

- **Problema:** `TrialSimulator.simulate_outcomes()` simulava apenas 1 dia sem refeições, ignorando `trial.duration_weeks`.
- **Solução:** Integrar `MealSequenceGenerator` no loop de simulação com refeições diárias repetidas por `duration_weeks * 7` dias.
- **Evidência:** Testes PASS (87 sim + 409 engines = 496 total), ruff clean.
- **Prevenção:** Ao estender `TrialSimulator`, sempre verificar se `duration_weeks` está sendo usado e se refeições são aplicadas em simulações multi-dia.

- **Problema:** `generate_virtual_subject()` aceita `rng` (np.random.Generator), não `seed` — causou TypeError nos testes.
- **Solução:** Usar `np.random.default_rng(seed)` ou passar `rng` existente.
- **Prevenção:** Verificar API real antes de assumir parâmetros; `VirtualPopulation.generate()` é `@classmethod` com `seed`.

- **Problema:** `VirtualSubject` não tem `homa_ir` nem `pancreatic_function_pct` — adapter quebrou com AttributeError.
- **Solução:** Computar HOMA-IR = (G_fasting_mmol * C_peptide_nmol) / 22.5; estimar pancreatic_function_pct por tipo de diabetes.
- **Prevenção:** Adaptadores devem mapear campos ausentes com computação derivada, não assumir correspondência 1:1.

## 2026-07-12 — Overflow numérico no HovorkaModel com alta resistência insulínica

- **Problema:** ODE do Hovorka produzia overflow (NaN) sob T2DM com alta IR.
- **Solução:** Clamping nos estados ODE (Q1/Q2 capped 10000, G capped 50 mmol/L) e nas taxas (xi1/xi2/EGP modulation clamped [0,1]).
- **Evidência:** `test_episode_completion` com Hovorka PASS sem warnings de overflow.
- **Prevenção:** Sempre aplicar clamping em modelos ODE fisiológicos antes da integração RK4.
