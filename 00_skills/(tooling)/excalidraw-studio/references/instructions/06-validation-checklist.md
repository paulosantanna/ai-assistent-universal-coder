<!-- Package: 00_skills/(tooling)/excalidraw-studio; relative command/resource examples resolve from that package or workspace root. -->

## Validation Checklist

Before delivering the diagram, verify:

- [ ] All elements have unique IDs
- [ ] Every element has ALL required base properties: `angle`, `strokeStyle`, `opacity`, `groupIds`, `frameId`, `index`, `isDeleted`, `link`, `locked`, `seed`, `version`, `versionNonce`, `updated`
- [ ] `index` values are assigned in order (`"a0"`, `"a1"`, …) with text elements getting higher values than shapes/arrows
- [ ] Top-level JSON includes `"files": {}`
- [ ] Shapes with text use `boundElements` + separate text element with `containerId`
- [ ] Text elements inside containers have `containerId`, `originalText`, `lineHeight: 1.25`, `autoResize: true`, `roundness: null`, `backgroundColor: "transparent"`
- [ ] Arrows use `startBinding`/`endBinding` (with `elementId`, `focus`, `gap`) when connecting shapes, plus `lastCommittedPoint: null`, `startArrowhead: null`, `endArrowhead: "arrow"`
- [ ] Connected shapes list the arrow in their `boundElements` arrays
- [ ] Element order: shapes → arrows → text elements (text always on top)
- [ ] Ellipses use `roundness: null` (not `{ "type": 3 }`)
- [ ] Coordinates prevent overlapping (check spacing)
- [ ] Text is readable (font size 16+)
- [ ] Colors follow consistent scheme
- [ ] File is valid JSON
- [ ] Element count is reasonable (<20 for clarity)
