<!-- Package: 00_skills/(tooling)/girl-voice-composer-simulation-expert; relative command/resource examples resolve from that package or workspace root. -->

## 7. Inputs

Required:

- `language`: `pt-BR` | `en-US`
- `target_age`: integer in 6..8
- `engine`: engine identifier + its available parameter controls
  (or `agnostic` for a reference-only spec)

Optional:

- `text`: the utterance(s) to be voiced
- `style`: e.g. `neutral`, `cheerful`, `storytelling`, `calm`
- `consent_ref`: pointer to a consent artifact (only when real recordings inform tuning)

---
