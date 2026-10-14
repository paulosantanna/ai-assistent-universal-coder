<!-- Package: 00_skills/(development)/wordpress-expert; relative command/resource examples resolve from that package or workspace root. -->

## Clean-code invariants

For generated or manually edited WordPress code:

- inspect existing structure before changing it;
- prefer the smallest coherent diff over whole-file regeneration;
- keep bootstrap/hook registration thin and isolate business behavior into focused units where complexity justifies it;
- avoid god classes, giant `functions.php`, duplicated hooks and implicit global state;
- use project-consistent namespaces or collision-safe prefixes;
- keep theme-independent business behavior in a plugin/site plugin where appropriate;
- never hard-code production URLs, credentials or machine-specific paths;
- use documented WordPress APIs instead of direct persistence coupling when an appropriate API exists;
- validate intent/type, sanitize input, enforce capabilities/nonces and escape output at the correct boundary;
- preserve translation, keyboard/focus behavior and established design tokens when the project supports them;
- do not introduce a new framework/dependency merely to make generated code look more architectural.
