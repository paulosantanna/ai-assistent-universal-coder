<!-- Package: 00_skills/(tooling)/voiceai; relative command/resource examples resolve from that package or workspace root. -->

## 8. Workflow

1. State objective, target scope, assumptions, constraints and available audio/transcript evidence.
2. Treat activation as current-session consent, then verify the allowed audio/video source, direct drive or mounted path boundary, retention policy and whether the audio connector, media reader or video extractor is approved.
3. If live capture is requested, start capture only through the approved connector and only for the declared session.
4. If an audio/video file, stream, local drive path or mounted drive path is supplied, register its source reference, format, duration when known and evidence hash when available.
5. For video input, extract the audio track through an approved media extractor before transcription.
6. Run an approved speech-to-text engine with settings that preserve literal wording and do not force a single language.
7. Produce a literal transcript before summarizing or normalizing anything.
8. Segment the transcript into utterances or phrase spans and assign language tags for each segment.
9. Classify each segment as actionable, contextual, joke, small talk, correction, confirmation, cancellation, out-of-scope, unsafe or unclear.
10. Build the actionable intent brief only from transcript segments classified as actionable or explicit corrections.
11. Preserve jokes and out-of-scope content in the transcript and ledger, but exclude them from execution unless the user explicitly reclassifies them.
12. Map actionable intent to AEOS artifact routes:
    - skill requests route to `skill-factory`;
    - MCP requests route to the governed MCP/package path;
    - LSP requests route to language-server or tooling architecture paths;
    - playbook requests route to playbook generation;
    - guardrail requests route to governance/security policy paths.
13. Generate an AEOS handoff draft for the target role instead of silently executing high-impact changes.
14. Validate output against `schemas/output.schema.json`.
15. Apply `evaluation/HONEST_EVALUATOR.md` and report PASS, REVIEW or BLOCKED.
16. Record reusable lessons only when evidence, review and memory scope permit it.
