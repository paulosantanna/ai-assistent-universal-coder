<!-- Package: 00_skills/(architecture)/architecture-decision-record; relative command/resource examples resolve from that package or workspace root. -->

## Critical rules

1. One ADR records one decision. Its title is a noun phrase that states the decision, never a question.
2. Accepted and rejected ADRs are immutable. A changed decision is a new ADR that supersedes the old one; on the old record only the status line changes.
3. Never invent context, options, deciders or evidence. Ask, in the user's language, only for missing mandatory fields; state every assumption you make.
4. Follow the target log's existing directory, filename pattern, template and heading language. Defaults apply only when no log exists.
5. Write prose in the user's language; keep technical terms such as ADR, API and SLA in English.
6. Before delivering an authored ADR, `node "00_skills/(architecture)/architecture-decision-record/scripts/adr_lint.mjs" <file> --strict` must exit 0.
7. Never put secrets, credentials or personal data in an ADR.
