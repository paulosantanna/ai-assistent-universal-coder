<!-- Package: 00_skills/(tooling)/excalidraw-studio; relative command/resource examples resolve from that package or workspace root. -->

## Workflow

```
UNDERSTAND → CHOOSE TYPE → EXTRACT → GENERATE → SAVE
```

### Step 1: Understand the Request

Analyze the user's description to determine:

1. **Diagram type** — Use the decision matrix below
2. **Key elements** — Entities, steps, concepts, actors
3. **Relationships** — Flow direction, connections, hierarchy
4. **Complexity** — Number of elements (target: under 20 for clarity)

### Step 2: Choose the Diagram Type and Visual Mode

**Diagram type:**

| User Intent                | Diagram Type         | Keywords                                      |
| -------------------------- | -------------------- | --------------------------------------------- |
| Process flow, steps        | **Flowchart**        | "workflow", "process", "steps"                |
| Connections, dependencies  | **Relationship**     | "relationship", "connections", "dependencies" |
| Concept hierarchy          | **Mind Map**         | "mind map", "concepts", "breakdown"           |
| System design              | **Architecture**     | "architecture", "system", "components"        |
| Data movement              | **Data Flow (DFD)**  | "data flow", "data processing"                |
| Cross-functional processes | **Swimlane**         | "business process", "swimlane", "actors"      |
| Object-oriented design     | **Class Diagram**    | "class", "inheritance", "OOP"                 |
| Interaction sequences      | **Sequence Diagram** | "sequence", "interaction", "messages"         |
| Database design            | **ER Diagram**       | "database", "entity", "data model"            |

**Visual mode** — decide upfront and apply consistently to all elements:

| Mode       | `roughness` | `fontFamily` | When to use                                          |
| ---------- | ----------- | ------------ | ---------------------------------------------------- |
| **Sketch** | `1`         | `5`          | Default — informal, approachable, Excalidraw-native  |
| **Clean**  | `0`         | `2`          | Executive presentations, formal specs                |
| **Mixed**  | zones: `0`, shapes: `1` | `5` | Architecture diagrams (structural zones + sketchy shapes) |

### Step 3: Extract Structured Information

Extract the key components based on diagram type. For each type, identify:

- **Nodes/entities** — What are the boxes/shapes?
- **Connections** — What connects to what, and with what label?
- **Hierarchy** — What contains what, what comes before what?
- **Decision points** — Where does the flow branch?

For detailed extraction guidelines per diagram type, read `references/element-types.md`.

### Step 4: Generate the Excalidraw JSON

**CRITICAL: Read `references/excalidraw-schema.md` before generating your first diagram.** It contains the correct element format, text container model, and binding system.

Key rules for generation:

1. **Text inside shapes** — Use `boundElements` on the shape and a separate text element with `containerId`. Never use a `label` shorthand:

   ```json
   [
     {
       "id": "step-1",
       "type": "rectangle",
       "x": 100, "y": 100, "width": 200, "height": 80,
       "boundElements": [{ "type": "text", "id": "text-step-1" }]
     },
     {
       "id": "text-step-1",
       "type": "text",
       "x": 130, "y": 128, "width": 140, "height": 24,
       "text": "My Step", "originalText": "My Step",
       "fontSize": 20, "fontFamily": 5,
       "textAlign": "center", "verticalAlign": "middle",
       "containerId": "step-1", "lineHeight": 1.25, "roundness": null
     }
   ]
   ```

2. **Arrow labels** — Also use `boundElements` + separate text element with `containerId`. Never use a `label` shorthand on arrows:

   ```json
   [
     {
       "id": "arrow-1",
       "type": "arrow",
       "x": 100, "y": 150,
       "points": [[0, 0], [200, 0]],
       "boundElements": [{ "type": "text", "id": "text-arrow-1" }]
     },
     {
       "id": "text-arrow-1",
       "type": "text",
       "x": 160, "y": 132, "width": 80, "height": 18,
       "text": "sends data", "originalText": "sends data",
       "fontSize": 14, "fontFamily": 5,
       "textAlign": "center", "verticalAlign": "middle",
       "containerId": "arrow-1", "lineHeight": 1.25, "roundness": null
     }
   ]
   ```

3. **Arrow bindings** — Use `startBinding`/`endBinding` (not `start`/`end`). Connected shapes must list the arrow in their `boundElements`:

   ```json
   {
     "id": "shape-1",
     "boundElements": [
       { "type": "text", "id": "text-shape-1" },
       { "type": "arrow", "id": "arrow-1" }
     ]
   }
   ```
   ```json
   {
     "id": "arrow-1",
     "type": "arrow",
     "startBinding": { "elementId": "shape-1", "focus": 0, "gap": 1 },
     "endBinding": { "elementId": "shape-2", "focus": 0, "gap": 1 }
   }
   ```

4. **Element order for z-index** — Always declare shapes first, arrows second, text elements last. This guarantees text renders on top and is never obscured by arrows or other shapes.

5. **Positioning** — Use grid-aligned coordinates (multiples of 20px when `gridSize: 20`). Leave 200-300px horizontal gap, 100-150px vertical gap between elements.

6. **Unique IDs** — Every element must have a unique `id`. Use descriptive IDs like `"step-1"`, `"decision-valid"`, `"arrow-1-to-2"`, `"text-step-1"`.

7. **Colors** — Use a consistent palette:

   | Role | Color | Hex |
   |------|-------|-----|
   | Primary entities | Light blue | `#a5d8ff` |
   | Process steps | Light green | `#b2f2bb` |
   | Important/Central | Yellow | `#ffd43b` |
   | Warnings/Errors | Light red | `#ffc9c9` |
   | Secondary | Cyan | `#96f2d7` |
   | Default stroke | Dark | `#1e1e1e` |

### Step 5: Save and Present

1. Save as `<descriptive-name>.excalidraw`
2. Provide a summary:

   ```
   Created: user-workflow.excalidraw
   Type: Flowchart
   Elements: 7 shapes, 6 arrows, 1 title
   Total: 14 elements

   To view:
   1. Visit https://excalidraw.com → Open → drag and drop the file
   2. Or use the Excalidraw VS Code extension
   3. Or open in Obsidian with the Excalidraw plugin
   ```
