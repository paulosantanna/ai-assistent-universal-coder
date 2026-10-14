<!-- Package: 00_skills/(tooling)/nx-generate; relative command/resource examples resolve from that package or workspace root. -->

## Generator Discovery Flow

### Step 1: List Available Generators

Use the Nx CLI to discover available generators:

- List all generators for a plugin: `npx nx list @nx/react`
- View available plugins: `npx nx list`

This includes:

- Plugin generators (e.g., `@nx/react:library`, `@nx/js:library`)
- Local workspace generators (defined in the repo's own plugins)

### Step 2: Match Generator to User Request

Based on the user's request, identify which generator(s) could fulfill their needs. Consider:

- What artifact type they want to create (library, application, etc.)
- Which framework or technology stack is relevant
- Whether they mentioned specific generator names

**IMPORTANT**: When both a local workspace generator and an external plugin generator could satisfy the request, **always prefer the local workspace generator**. Local generators are customized for the specific repo's patterns and conventions.

It's possible that the user request is something that no Nx generator exists for whatsoever. In this case, you can stop using this skill and try to help the user another way. HOWEVER, the burden of proof for this is high. Before aborting, carefully consider each and every generator that's available. Look into details for any that could be related in any way before making this decision.
