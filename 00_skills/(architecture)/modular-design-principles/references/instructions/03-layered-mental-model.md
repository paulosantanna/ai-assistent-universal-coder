<!-- Package: 00_skills/(architecture)/modular-design-principles; relative command/resource examples resolve from that package or workspace root. -->

## Layered mental model

- **Composition roots** (applications, hosts, runners): wire modules together; keep orchestration thin.
- **Modules / bounded contexts**: cohesive units of behavior and data ownership; each should be understandable and testable on its own.
- **Shared kernels** (use sparingly): only stable, truly cross-cutting concepts; resist turning them into a grab-bag of “everything everyone needs.”

How you physically lay this out (mono repo, multi repo, packages, libraries) is a **delivery choice**, not the definition of modularity. The principles below still apply.

---
