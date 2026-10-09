# C# 14 features

Entry: [What's new in C# 14](https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-14)
Updated: 2026-10-09

Use a feature below only when `references/project-and-idioms.md` says the project language is C# 14. Read the official page before emitting syntax this file does not show.

## Extension members

Instance members use a receiver parameter. Static members use the type only.

```csharp
extension<TSource>(IEnumerable<TSource> source)
{
    public bool IsEmpty => !source.Any();
}
```

Call site: `sequence.IsEmpty`. A static block is `extension<TSource>(IEnumerable<TSource>)`.

## `field`

Use `field` for the compiler-generated backing field. A type that already has a symbol named `field` needs `@field` or `this.field`.

```csharp
public string Message
{
    get;
    set => field = value ?? throw new ArgumentNullException(nameof(value));
}
```

## Null-conditional assignment

`customer?.Order = GetCurrentOrder();` evaluates the right side only when `customer` is not null. Compound assignment is allowed. `++` and `--` are not.

## `nameof` of an unbound generic

`nameof(List<>)` evaluates to `List`.

## Span conversions

`Span<T>`, `ReadOnlySpan<T>`, and `T[]` gain implicit conversions, including as extension receivers. The conversion list is the language reference. Do not add a conversion that page does not list.

## Lambda modifiers

Modifiers `scoped`, `ref`, `in`, `out`, and `ref readonly` may appear without a parameter type: `(text, out result) => int.TryParse(text, out result)`. `params` still needs an explicit type.

## Partial constructors and events

One defining declaration and one implementing declaration. Only the implementing constructor may use `this()` or `base()`. Only one partial declaration may use a primary constructor. The implementing event declares `add` and `remove`. The defining event is field-like.

## User-defined compound assignment

A type may define its own compound assignment operator. Copy the signature from the feature specification or from an operator already in the repository. This file does not inline that signature.

## File-based app directives

C# 14 adds preprocessor directives for file-based apps. Read the what's new page before emitting a directive this repository does not already use.
