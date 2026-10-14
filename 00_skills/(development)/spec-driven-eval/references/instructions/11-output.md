<!-- Package: 00_skills/(development)/spec-driven-eval; relative command/resource examples resolve from that package or workspace root. -->

## Output

Produce a markdown report following the template in [reference.md](../tlc/references/reference.md). It must separate the **two subjects** and contain: per-AC implementation checklist table (I-checks, MET/UNMET, evidence); the Elicitation `E` block (category-rubric recall table + added-requirement ledger with verdicts → `E_recall` / `E_precision` / `E_justified`); the Scope `S` traceability verdict; per-requirement unit/e2e test checklist table (T-checks over the **sanctioned set = PRD ACs ∪ valid E-additions**); extra-tests inventory; the test-distribution `D` table (tiers with counts + %); the computed `Final` (+ `Adjusted Final` if a gate is ✗); `R` / `G` / `D`; a ranked gap list; and concrete fixes to reach 1.00.

Save the report to `<spec-folder>/evaluations/<priority>-<story-slug>-<timestamp>.md` when a `.specs`/spec folder exists; otherwise present it inline. The `<timestamp>` is a UTC instant in `YYYYMMDDTHHMMSSZ` form (e.g. `20260606T143012Z`), obtained from the system clock at write time (`date -u +%Y%m%dT%H%M%SZ`). The timestamp makes every report filename unique so **multiple agents evaluating the same story in parallel never overwrite each other** — each run produces its own file. If a same-second collision is still possible (many parallel runs), append a short run id: `<priority>-<story-slug>-<timestamp>-<run-id>.md`.

Note: only the **report** filename is timestamped. The frozen `_ac-baseline.md` is deliberately **not** timestamped — it is a single shared artifact that every run reads from to stay comparable; never fork it per run.
