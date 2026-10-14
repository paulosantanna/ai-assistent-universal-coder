<!-- Package: 00_skills/(development)/architecturally-significant-requirement; relative command/resource examples resolve from that package or workspace root. -->

## Troubleshooting

- `BLOCKED` with `UNKNOWN_CRITERION`: use ids C1 to C7 or the keys listed in `references/asr-test.md`.
- `BLOCKED` with `INVALID_CRITERION_VALUE`: use Y, N, ?, H, M, L, n/a, true, false or a non-negative count.
- Stakeholders disagree on a criterion: mark it `?`, record both positions in the rationale, and keep the ASR open.
- Everything looks significant: compare against the examples in `references/asr-test.md`; criteria C6 and C7 are context-specific and should not alone justify an ADR.
- `measurable_response: false`: replace adjectives such as "fast" with a threshold, unit and condition.
