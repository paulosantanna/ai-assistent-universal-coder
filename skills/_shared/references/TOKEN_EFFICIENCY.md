# Token Efficiency — measurable progressive disclosure

Use measurable context limits, not claims of “optimized prompts”.

1. Load the skill entry file and its `references/INDEX.md` only.
2. Select references by detected stack/version + mission keywords.
3. Default: open at most 3 reference files; hard limit: 5 unless the mission explicitly requires more.
4. Prefer symbol/file/line pointers over copied source.
5. Reuse verified evidence by hash/path instead of re-reading identical content.
6. Do not load vendor, build, generated, binary or dependency trees unless the mission targets them.
7. Ask MCP/doc providers for narrow symbol/control queries with bounded result counts and byte limits.
8. Keep evidence matrices compact: claim → pointer → verification.
9. Measure loaded files, characters/bytes and evidence items in Debrief. Token estimates are advisory only because tokenizer/model differs.
10. If context exceeds the profile hard limit, summarize verified evidence and discard duplicate raw text before loading more.
