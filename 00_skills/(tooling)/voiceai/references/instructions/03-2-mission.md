<!-- Package: 00_skills/(tooling)/voiceai; relative command/resource examples resolve from that package or workspace root. -->

## 2. Mission

Provide an evidence-backed voice interface for AEOS. Activating this skill is treated as explicit current-session consent for `voiceai` to record user audio or transcribe audio from user-authorized audio/video media within the declared scope. The skill can:

- capture or receive user speech audio through an approved audio connector after the user activates the skill;
- access direct local-drive or mounted-drive media paths supplied by the user, limited to the declared audio/video files or directories;
- extract and transcribe speech audio from authorized video files;
- transcribe speech literally, including filler words, interruptions, code-switching and mixed-language phrases;
- tag language spans at segment level when one utterance mixes two or more languages;
- classify each segment as actionable, contextual, joke, small talk, correction, confirmation, cancellation, out-of-scope or unsafe;
- preserve jokes and out-of-context speech in the literal transcript while excluding them from the actionable task brief unless the user explicitly makes them part of the task;
- transform actionable spoken intent into AEOS-compatible briefs for new skills, MCPs, LSPs, playbooks, guardrails, prompts, reports or implementation tasks;
- generate handoff-ready outputs that another AEOS role can inspect, validate and execute.
