<!-- Package: 00_skills/(tooling)/girl-voice-composer-simulation-expert; relative command/resource examples resolve from that package or workspace root. -->

## 10. Workflow

```text
Request
→ Classify intent (allowed generic direction vs forbidden cloning)
→ Preconditions / consent gate (fail closed)
→ Select language profile (pt-BR | en-US)
→ Select age point (6..8) and interpolate base parameters
→ Apply style modifiers (neutral/cheerful/storytelling/calm)
→ Map generic params → target engine controls
→ Emit voice_params.json + direction notes + engine mapping + limitations
→ Deterministic validation (scripts/validate_profile.py)
→ Report (with limitations); STOP if blocking issue
```

---
