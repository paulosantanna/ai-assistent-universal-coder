---
name: csharp-expert
description: "Writes and reviews production C# on the current stable .NET release (C# 14, .NET 10). Use when the user says c#-expert, C#, csharp, .NET, csproj, dotnet, or asks to implement, fix, or review .cs code. Do NOT use for F#, Visual Basic, non-.NET languages, or work that is not C#/.NET source."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
---

# C# Expert

Governance: CodENavi Full Workspace v2. A skill of `codenavi-agent`. It creates no other agent identity.

Write and review C# source on the current stable .NET release. Module map: `references/INDEX.md`.

## Mission

New C# uses C# 14 on `net10.0`. An existing project keeps the `TargetFramework` and `LangVersion` it already declares. Do not retarget because a newer SDK exists. Version pin and refresh rule: `references/current-release.md`.

## Workflow

1. Read every `TargetFramework` and `LangVersion` in the SDK-style `.csproj` files this change touches. Map and idiom rules: `references/project-and-idioms.md`.
2. For a new project, set `TargetFramework` to `net10.0` and leave `LangVersion` unset so the default is C# 14. For an existing project, write only syntax that its TFM and `LangVersion` accept.
3. Apply C# 14 features only when step 2 allows them. Feature rules: `references/csharp-14.md`.
4. Keep the change inside C# source, the `.csproj` that compiles it, and the C# test project that covers it.
5. Verify with the commands in `references/verify.md`. A compile failure blocks any claim that the code is done.

## Rules

1. Enable nullable on a new file when the project sets `<Nullable>enable</Nullable>`, and on every file of a project this skill creates.
2. Do not set `LangVersion` to `preview`. Do not use C# 15 or `net11.0` unless the repository already declares that target.
3. Prefer the BCL or a package the project already references. Add a package only when the user asked for that dependency.
4. Match the project's namespace style, file layout, and analyzer settings.

## Example

User says: "adicione um contador com get customizado neste tipo."
Result: a `field`-backed property when the project is C# 14.

```csharp
public int Count
{
    get => field;
    set => field = value < 0 ? 0 : value;
}
```

On `net8.0` the same request uses an explicit backing field. The TFM stays `net8.0`.

## Stop

Stop when the change is not C#/.NET source, the `.csproj` TFM cannot be read, or `dotnet` is absent and the syntax must be compiled to confirm. Say which input is missing.

## Output

Report the detected TFM, the language version used, the files changed, and the `dotnet build` or `dotnet test` result from `references/verify.md`.
