# Project shape and idioms

Entry: [Language versioning](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/language-versioning)
Updated: 2026-10-09

## Detect

Read `TargetFramework`, `TargetFrameworks`, and `LangVersion` from each SDK-style `.csproj` the change touches.

- `LangVersion` absent: use the TFM default below.
- `LangVersion` set to `14.0`, `latest`, or `latestMajor`: C# 14 syntax is allowed on that project.
- `LangVersion` set to `preview`: do not add preview syntax.
- `LangVersion` set to `default` is the compiler's latest major, which can exceed the TFM default. Honor the explicit value. Do not add that property yourself.

## TFM default

| TFM | C# default |
| --- | --- |
| `net11.0` | 15 |
| `net10.0` | 14 |
| `net9.0` | 13 |
| `net8.0` | 12 |
| `net7.0` | 11 |
| `net6.0` | 10 |
| `net5.0` | 9.0 |
| `netcoreapp3.*` | 8.0 |
| `netstandard2.1` | 8.0 |
| `netstandard2.0` | 7.3 |
| `net48` and other .NET Framework | 7.3 |

## New project

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>
</Project>
```

Leave `LangVersion` unset.

## Idioms gated by language version

- File-scoped namespace: C# 10.
- `record` class: C# 9. `record struct`: C# 10.
- `required` members: C# 11.
- Primary constructors on a class or struct: C# 12.
- Collection expressions: C# 12.
- Every feature in `csharp-14.md`: C# 14.

Use the newest idiom the detected language version allows. Keep the surrounding file's namespace style.
