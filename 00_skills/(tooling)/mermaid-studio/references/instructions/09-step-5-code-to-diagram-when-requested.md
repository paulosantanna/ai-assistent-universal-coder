<!-- Package: 00_skills/(tooling)/mermaid-studio; relative command/resource examples resolve from that package or workspace root. -->

## Step 5: Code-to-Diagram (When Requested)

When the user asks to visualize existing code or architecture:

1. Read `references/code-to-diagram.md` for the analysis methodology
2. Analyze the codebase to identify the right diagram type:
   - Module dependencies → Flowchart or Class diagram
   - API routes and handlers → Sequence diagram
   - Database models/schemas → ERD
   - Service architecture → C4 Container or Architecture diagram
   - State machines in code → State diagram
3. Generate the .mmd file **with proper init directives** (Golden Rule 1)
4. Validate and render as usual
