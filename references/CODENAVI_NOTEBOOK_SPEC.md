# CodENavi Notebook Specification

## Structure

```text
.notebook/
  INDEX.md
  <note>.md
```

Start flat. When active notes exceed roughly 15, organize into `flows/`, `patterns/`, `gotchas/`, `domain/`, `graph/` and optional `archive/`.

## INDEX.md

Read before every material mission.

Format:
`- [slug](path) — summary (max ~100 chars) | category | tag1, tag2, tag3`

Rules:
- short and scannable;
- 2–4 discriminative lowercase tags;
- sort by most recently updated;
- update `Last updated` whenever the index changes;
- archived notes are not loaded by default.

## Individual note

A note is a field note, not documentation.

Required:
- one concept;
- observable facts, not opinions;
- entry point;
- pointers to code rather than pasted code;
- concise flow/pattern/gotcha/domain/graph facts;
- `Updated: YYYY-MM-DD`.

Preferred pointers:
- `path/file.ts:function()`
- `path/file.ts (L10-25)`
- `path/File.java:Class.method()`

When a note becomes invalid, update or archive it immediately. Stale notes are worse than no notes.
