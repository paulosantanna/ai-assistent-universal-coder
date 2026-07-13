# FAILURES.md

- **2026-07-12:** `TrialSimulator.simulate_outcomes` não usava `duration_weeks` nem refeições — simulava 1 dia apenas, ignorando o objetivo de simulação longitudinal.
- **2026-07-12:** `TestDigitalTwinAdapter` quebrou porque `generate_virtual_subject` aceita `rng`, não `seed`, e `VirtualSubject` não tem `homa_ir`.
- **2026-07-12:** HovorkaModel produzia NaN em cenários de alta resistência insulínica — ODE sem clamping.
