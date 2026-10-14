<!-- Package: 00_skills/(tooling)/voiceai; relative command/resource examples resolve from that package or workspace root. -->

## 12. Classification Policy

Segment classifications:

- `actionable`: spoken instruction that should become task scope or a handoff requirement.
- `contextual`: background information useful for understanding the task.
- `joke`: humorous or playful speech not intended as task scope.
- `small_talk`: conversational filler unrelated to the work.
- `correction`: a replacement, clarification or rollback of earlier spoken intent.
- `confirmation`: an approval, denial or selection.
- `cancellation`: an instruction to stop or discard scope.
- `out_of_scope`: content unrelated to the active AEOS objective.
- `unsafe`: content requiring refusal, approval or security review.
- `unclear`: ambiguous content requiring clarification or a conservative handoff note.

The literal transcript remains the source of truth. The actionable brief is an interpretation and must cite the transcript segments it uses.
