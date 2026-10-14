<!-- Package: 00_skills/(quality)/web-accessibility; relative command/resource examples resolve from that package or workspace root. -->

## Testing checklist

### Automated testing

```bash
# Lighthouse accessibility audit
npx lighthouse https://example.com --only-categories=accessibility

# axe-core
npm install @axe-core/cli -g
axe https://example.com
```

### Manual testing

- [ ] **Keyboard navigation:** Tab through entire page, use Enter/Space to activate
- [ ] **Screen reader:** Test with VoiceOver (Mac), NVDA (Windows), or TalkBack (Android)
- [ ] **Zoom:** Content usable at 200% zoom
- [ ] **High contrast:** Test with Windows High Contrast Mode
- [ ] **Reduced motion:** Test with `prefers-reduced-motion: reduce`
- [ ] **Focus order:** Logical and follows visual order

### Screen reader commands

| Action        | VoiceOver (Mac)     | NVDA (Windows) |
| ------------- | ------------------- | -------------- |
| Start/Stop    | ⌘ + F5              | Ctrl + Alt + N |
| Next item     | VO + →              | ↓              |
| Previous item | VO + ←              | ↑              |
| Activate      | VO + Space          | Enter          |
| Headings list | VO + U, then arrows | H / Shift + H  |
| Links list    | VO + U              | K / Shift + K  |

---
