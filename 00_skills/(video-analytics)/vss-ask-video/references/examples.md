# Examples

## Examples

- **Hot conversation:** The previous turn says, "A forklift crossed the loading
  aisle at 10:14 UTC." Answer `10:14 UTC` directly; search nothing.
- **Markdown sufficient:** Native agent Markdown memory search finds a note that
  directly answers the question -> answer from it; call no VSS command.
- **Markdown incomplete:** Retain its `job_id`, inspect known/configured state,
  then introspect by that job when enabled.
- **Explicit stored parent:** "Show me the summary from job `sum-01JXYZ`." ->
  `vss memory get --job-id sum-01JXYZ`.
- **Disabled introspection:** Search Markdown, then structured memory. Do not
  introspect, enable it, or escalate automatically to VLM.
- **Exact fresh verification:** "Freshly verify whether the worker wore a hard
  hat on `dock_cam` from `2026-08-13T20:00:00Z` to
  `2026-08-13T20:00:30Z`." -> `vss vlm run` with that exact sensor/window.
- **Search handoff:** a user-confirmed vss-search-archive handoff with a pre-resolved bounded VIDEO_URL -> Path A `--media-url`.
- **No memory with scope:** Introspection returns `no_memory`, while trusted
  context provides `dock_cam` and `2026-08-13T20:00:00Z` through
  `2026-08-13T20:00:30Z` -> run one `vss vlm run` for exactly that interval.
- **No memory without scope:** "Did a forklift enter the loading area last
  week?" returns `no_memory`, with no exact sensor/window -> explain no matching
  memory/window exists and ask for the sensor and exact UTC window; do not run
  the VLM.

## Out of scope

- archive search
- full-recording summary
- covert surveillance
