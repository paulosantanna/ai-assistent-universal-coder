<!-- Package: 00_skills/(tooling)/excalidraw-studio; relative command/resource examples resolve from that package or workspace root. -->

## Best Practices

### Element Count

| Diagram Type          | Recommended | Maximum |
| --------------------- | ----------- | ------- |
| Flowchart steps       | 3-10        | 15      |
| Relationship entities | 3-8         | 12      |
| Mind map branches     | 4-6         | 8       |
| Sub-topics per branch | 2-4         | 6       |

If the user's request exceeds maximum, suggest breaking into multiple diagrams:

> "Your request includes 15 components. For clarity, I recommend: (1) High-level architecture diagram with 6 main components, (2) Detailed sub-diagrams for each subsystem. Want me to start with the high-level view?"

### Layout

- **Flow direction**: Left-to-right for processes, top-to-bottom for hierarchies
- **Spacing**: 200-300px horizontal, 100-150px vertical between elements
- **Grid alignment**: Position on multiples of 20px for clean alignment
- **Margins**: Minimum 50px from canvas edge
- **Text sizing**: 28-36px titles, 18-22px labels, 14-16px annotations
- **Font**: Use `fontFamily: 5` (Excalifont) for hand-drawn consistency. Fallback to `1` (Virgil) if 5 is not supported.
- **Background zones**: For architecture diagrams, add semi-transparent dashed zone rectangles (`opacity: 35`, `strokeStyle: "dashed"`, `roughness: 0`) as the first elements in the array to create visual grouping regions. See `references/excalidraw-schema.md` → Background Zones.
- **Element order**: zones first → shapes → arrows → text elements (ensures correct z-index and text always renders on top)

### Common Mistakes to Avoid

- ❌ Using `label: { text: "..." }` shorthand on shapes or arrows — not supported by the Excalidraw parser
- ❌ Putting `text` directly on shape elements without `containerId`
- ❌ Using `start`/`end` for arrow bindings — use `startBinding`/`endBinding` with `elementId`/`focus`/`gap`
- ❌ Forgetting to add arrows to their connected shapes' `boundElements` arrays
- ❌ Omitting `originalText`, `lineHeight`, `autoResize`, or `backgroundColor: "transparent"` from text elements inside containers
- ❌ Omitting required base properties (`angle`, `strokeStyle`, `opacity`, `groupIds`, `frameId`, `index`, `isDeleted`, `seed`, `version`, `versionNonce`, `updated`, `link`, `locked`) — elements will not render
- ❌ Missing `"files": {}` at the top level of the JSON
- ❌ Using `roundness: { "type": 3 }` on ellipses — ellipses must use `roundness: null`
- ❌ Missing `lastCommittedPoint`, `startArrowhead`, `endArrowhead` on arrows
- ❌ Declaring text elements before arrows — text renders underneath and gets obscured
- ❌ Floating arrows without bindings (won't move with shapes)
- ❌ Overlapping elements (increase spacing)
- ❌ Inconsistent color usage (define palette upfront)
- ❌ Too many elements on one diagram (break into sub-diagrams)
