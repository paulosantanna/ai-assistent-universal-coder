<!-- Package: 00_skills/(tooling)/voiceai; relative command/resource examples resolve from that package or workspace root. -->

## 14. Completion

Complete only when:

- requested audio/video transcript or voice-intent output exists;
- literal transcript is preserved separately from normalized intent;
- language segmentation and relevance classification are present or the limitation is explicitly marked as BLOCKED or REVIEW;
- jokes and out-of-scope segments are preserved but excluded from actionable execution;
- generated AEOS handoff or artifact brief matches the requested target;
- output validates against `schemas/output.schema.json`;
- evidence refs and residual risks are reported;
- no blocking finding remains.
