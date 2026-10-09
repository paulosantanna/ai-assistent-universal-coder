# HANDOFF

Updated: 2026-10-09

## Objective
- Add `csharp-expert`: a TLC skill of at most 100 lines that writes and reviews production C# on the current stable .NET release.

## Last Verified State
- `skills/csharp-expert/SKILL.md` is 56 lines. `skills/skill-architect/scripts/validate_skill.py` PASS (26 checks, 0 warnings).
- Pin: .NET 10.0.12, SDK 10.0.401, C# 14. End of support 2028-11-14. .NET 11.0.0-rc.1 / C# 15 is not the default.
- `loadActiveSkills()` resolves `csharp-expert` from `aeos/registries/skills.csharp-expert.additions.yaml`, owner `codenavi-agent`, risk `high`.
- Cursor activation entry: `.agents/skills/csharp-expert/SKILL.md`.

## Working Set
- `skills/csharp-expert/`
- `.agents/skills/csharp-expert/SKILL.md`
- `aeos/registries/skills.csharp-expert.additions.yaml`
- `aeos/registries/overlay.registry.index.yaml`

## Decisions Already Made
- Folder id is `csharp-expert`. The description keeps the trigger `c#-expert`.
- Existing projects keep their declared `TargetFramework` and `LangVersion`.
- No C# documentation MCP in this change.

## Blockers And Risks
- The AEOS skill router scores tokenized request terms. A request that only says `C#` drops the `#` before matching, so ranking depends on words such as `csharp`, `dotnet`, or `csproj`. Cursor loads the skill from the description, which includes `c#-expert` and `C#`.
- The version pin is a snapshot of the 2026-09-08 patch. A later patch requires a refresh of `references/current-release.md` from the official download page.

## Evidence Pointers
- `skills/csharp-expert/SKILL.md`
- `skills/csharp-expert/references/current-release.md`
- `skills/skill-architect/scripts/validate_skill.py`

## Exact Next Actions
- None for this skill. On C#/.NET source work, load `csharp-expert` and follow `skills/csharp-expert/SKILL.md`.

## Validation Still Required
- None for structure, line count, or overlay resolution. This mission did not compile a sample C# project.
