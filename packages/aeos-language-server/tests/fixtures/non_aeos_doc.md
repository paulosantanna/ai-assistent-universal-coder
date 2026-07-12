# Regular Markdown Document

This is a standard markdown document. It does NOT contain any AEOS front
matter or configuration. The LSP's `is_aeos_document` function should
reject this file and NOT attempt schema validation.

## Features

- Lists
- **Bold text**
- `inline code`

### Code blocks are also fine:

```typescript
function hello(): string {
  return "world";
}
```

### Even YAML code blocks:

```yaml
key: value
another:
  - list
  - of
  - items
```

But note: this is NOT AEOS configuration. It's just documentation.

### Regular HTML

<div class="note">
  This is a regular HTML div, not an AEOS artifact.
</div>

### Table

| Column A | Column B |
|----------|----------|
| Value 1  | Value 2  |
| Value 3  | Value 4  |

This file exists to verify that the LSP correctly distinguishes
between AEOS documents and normal files.

No `$schema`, no `$id`, no `aeos:` top-level key, no YAML front
matter delimiters (`---`). Just a plain markdown file.
