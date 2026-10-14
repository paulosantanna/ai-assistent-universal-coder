<!-- Package: 00_skills/(development)/specs; relative command/resource examples resolve from that package or workspace root. -->

## 14. Failure behavior

Return `BLOCKED` when a downstream skill would otherwise create or alter artifacts without a valid `specs` evidence reference.

Return `REVIEW` when the spec is useful but requires human judgment before mutation.

Return `PASS` only when the spec package is coherent, traceable and sufficient for the next skill to execute within scope.
