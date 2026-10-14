<!-- Package: 00_skills/(tooling)/chrome-devtools; relative command/resource examples resolve from that package or workspace root. -->

## Best Practices

- **Context Awareness**: Always run `list_pages` and `select_page` if you are unsure which tab is currently active.
- **Snapshots**: Take a new snapshot after any major navigation or DOM change, as `uid` values may change.
- **Timeouts**: Use reasonable timeouts for `wait_for` to avoid hanging on slow-loading elements.
- **Screenshots**: Use `take_screenshot` sparingly for visual verification, but rely on `take_snapshot` for logic.
