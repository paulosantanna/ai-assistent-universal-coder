<!-- Package: 00_skills/(tooling)/mermaid-studio; relative command/resource examples resolve from that package or workspace root. -->

## Troubleshooting Quick Reference

| Symptom               | Likely Cause       | Fix                                                    |
| --------------------- | ------------------ | ------------------------------------------------------ |
| Diagram won't render  | Syntax error       | Run validate.mjs, check brackets/quotes                |
| Labels cut off        | Text too long      | Shorten labels or use line breaks `<br/>`              |
| Layout looks wrong    | Wrong direction    | Try different TD/LR/BT/RL                              |
| Nodes overlap         | Too many nodes     | Split into subgraphs or multiple diagrams              |
| Lines too dark/thick  | No init directive  | Add `%%{init}` with `lineColor: '#94a3b8'`             |
| C4 lines overlapping  | No styling applied | Add `UpdateRelStyle` with offsets to each Rel          |
| AWS icons not showing | No icon pack       | Use `--icons logos` flag or fallback to built-in icons |
| `mmdc` not found      | Not installed      | Run `setup.sh`                                         |
| Theme not applied     | Wrong engine       | beautiful-mermaid themes only work with that engine    |

For comprehensive troubleshooting, read `references/troubleshooting.md`.
