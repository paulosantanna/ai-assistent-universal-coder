# Mixed apply plan (Track C)

> Run dir: `E:\Github\ai-assistent-universal-coder\.harness-eval\runs\2026-11-16-abc`
> Judges: J1 model=`gpt-5.6-sol-medium` · J2 model=`gpt-5.6-sol-medium`
> **This file is the only Mixed apply input.** Do not re-judge usefulness.

## What these words mean

| Word | Meaning | Apply must |
|------|---------|------------|
| **KEEP** | Text from judge Keep-core columns | Remain in the harness surface as rule/snippet |
| **CUT** | Text from judge Slim columns | Delete or compress only this bulk |
| **Apply** | Mechanical edit | Not a new design pass |

## Hard rules for apply agents

1. For each Mixed ID below, edit **only** that path.
2. **KEEP** items must survive (same contract — concern/module/section/checklist).
   Do not replace a KEEP teaching snippet with a weaker pattern.
3. **CUT** only what both judges' Slim columns describe (or the union when both
   clearly name the same bulk). If KEEP and CUT conflict, **skip that path** (Hold).
4. Never replace a fenced teaching snippet with `See app/...` / `lib/...` / `test/...`.
5. Never defer KEEP content to AGENTS.md or another surface unless CUT explicitly
   names OVERLAP with that path **and** KEEP still retains the behavior contract.
6. Do not open the repo to invent a different convention than KEEP states.
7. After edits: every KEEP bullet must still be satisfied by the file text.

## Paths (4)

### S058 — `.agents/skills/critical-thinking-governor/SKILL.md`

- Tier: `T1` · Name: `critical-thinking-governor`
- Overall: J1 `MIXED` · J2 `MIXED`

#### KEEP (do not remove or degrade)

- **J1:** BEHAVIOR-CHANGING: keep proportional lens selection, high-risk premortem, critical ethical lens, and fail-closed plan validation
- **J2:** BEHAVIOR-CHANGING: risk-proportional lens selection, critical pre-mortem and fail-closed plan integrity

#### CUT (only this bulk)

- **J1:** OVERLAP: cut repeated single-agent, lifecycle, secret, and Judge statements already mandated by AGENTS.md
- **J2:** OVERLAP: cut duplicated lifecycle, one-agent and generic evidence language

#### Overlap cites (context only; cut OVERLAP here only if listed under CUT)

- **J1:** AGENTS.md
- **J2:** AGENTS.md

---

### S209 — `.agents/skills/packaging/SKILL.md`

- Tier: `T1` · Name: `packaging`
- Overall: J1 `MIXED` · J2 `MIXED`

#### KEEP (do not remove or degrade)

- **J1:** BEHAVIOR-CHANGING: package manifest and checksum mission, restricted output locations, mutation denials and required artifact hashing
- **J2:** BEHAVIOR-CHANGING: manifest, checksum, secret and permission gates

#### CUT (only this bulk)

- **J1:** OVERLAP: generic audit scaffold duplicates repository scanner
- **J2:** OVERLAP: cut generic mapping and evidence boilerplate

#### Overlap cites (context only; cut OVERLAP here only if listed under CUT)

- **J1:** `.agents/skills/repo-scanner/SKILL.md`
- **J2:** `.agents/skills/package-trust-engineer/SKILL.md`; `.agents/skills/evidence-integrity-engineer/SKILL.md`

---

### S263 — `.agents/skills/security-audit/SKILL.md`

- Tier: `T1` · Name: `security-audit`
- Overall: J1 `MIXED` · J2 `MIXED`

#### KEEP (do not remove or degrade)

- **J1:** BEHAVIOR-CHANGING: security-risk and secret-detection mission, secret-value prohibition, authorized outputs and evidence hashing
- **J2:** BEHAVIOR-CHANGING: authorized scope, secret non-exposure and evidence gates

#### CUT (only this bulk)

- **J1:** OVERLAP: generic audit scaffold duplicates architecture mapper
- **J2:** OVERLAP: cut generic report and artifact boilerplate shared with broad audit skills

#### Overlap cites (context only; cut OVERLAP here only if listed under CUT)

- **J1:** `.agents/skills/architecture-mapper/SKILL.md`
- **J2:** `.agents/skills/enterprise-security-auditor/SKILL.md`; `.agents/skills/security-best-practices/SKILL.md`

---

### S303 — `.agents/skills/threat-modeler/SKILL.md`

- Tier: `T1` · Name: `threat-modeler`
- Overall: J1 `MIXED` · J2 `MIXED`

#### KEEP (do not remove or degrade)

- **J1:** BEHAVIOR-CHANGING: keep AEOS-specific injection, tool-poisoning, package and Tool Router checks
- **J2:** BEHAVIOR-CHANGING: keep AEOS-specific prompt-injection, tool-poisoning, secret-leakage and package-tampering scope

#### CUT (only this bulk)

- **J1:** OVERLAP: cut generic threat-model framing and risk boilerplate
- **J2:** OVERLAP: cut generic audit prompt and gate boilerplate

#### Overlap cites (context only; cut OVERLAP here only if listed under CUT)

- **J1:** .agents/skills/security-threat-model/SKILL.md
- **J2:** 00_skills/(security)/security-threat-model/SKILL.md

---

