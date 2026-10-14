<!-- Package: 00_skills/(tooling)/excalidraw-studio; relative command/resource examples resolve from that package or workspace root. -->

## Troubleshooting

| Issue                         | Solution                                                                                      |
| ----------------------------- | --------------------------------------------------------------------------------------------- |
| Text not showing in shapes    | Use `boundElements` + separate text element with `containerId`, `originalText`, `lineHeight`  |
| Text hidden behind arrows     | Move text elements to end of `elements` array (after all arrows)                             |
| Arrows don't move with shapes | Use `startBinding`/`endBinding` with `elementId`, `focus: 0`, `gap: 1`                       |
| Shape not moving with arrows  | Add the arrow to the shape's `boundElements` array                                            |
| Elements overlap              | Increase spacing between coordinates                                                          |
| Text doesn't fit              | Increase shape width or reduce font size                                                      |
| Too many elements             | Break into multiple diagrams                                                                  |
| Colors look inconsistent      | Define color palette upfront, apply consistently                                              |
