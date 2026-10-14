<!-- Package: 00_skills/(architecture)/architecture-decision-record; relative command/resource examples resolve from that package or workspace root. -->

## Examples

### Example 1: New decision in Portuguese

User says: "Escreva um ADR: decidimos usar PostgreSQL em vez de MongoDB no serviço de pedidos."
Actions: confirm significance (transactions, external dependency); check START; find `docs/decisions/` with next number 0004; fill the MADR template in Portuguese; lint with `--strict`; refresh the index.
Result: `docs/decisions/0004-usar-postgresql-no-servico-de-pedidos.md`, status `accepted`, lint PASS.

### Example 2: Supersede a decision

User says: "We are moving sessions from PostgreSQL to Redis, supersede ADR-0002."
Actions: write ADR-0007 with `Supersedes ADR-0002`; change only ADR-0002's status to `superseded by ADR-0007`; lint both; the log index shows the chain.
Result: two consistent records; ADR-0002's decision text is unchanged.

### Example 3: Review

User says: "Review ADR-0012 before the architecture board."
Actions: non-strict lint; seven review questions; ecADR check.
Result: findings table with H/M/L priority and one recommendation per finding.
