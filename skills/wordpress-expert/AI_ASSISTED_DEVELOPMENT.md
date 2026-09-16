# AI-Assisted WordPress Development Protocol

This protocol turns AI-assisted coding into a governed WordPress engineering workflow. It is editor-agnostic: Cursor, Codex, Copilot, IDE agents or other assistants may implement it, but none of them replaces WordPress architecture, review, verification or rollback discipline.

## External learning provenance

Learning source used to derive this protocol:

- WordPress.com — **Revolutionize Your WordPress Development with Cursor AI** (Nick Diego, 2025-01-21): https://youtu.be/3_TiyKdPNq4

The source demonstrates the value of project-specific AI instructions, explicit WordPress coding rules, documentation grounding, chat/planning before code generation, incremental implementation and human review. These concepts are generalized here into an AEOS/Codenavi workflow rather than coupling the skill to Cursor-specific files or UI.

## Objective

Create and alter WordPress projects so that generated changes are:

- architecturally native to WordPress;
- clean, readable and maintainable;
- easy to test, review, deploy and roll back;
- grounded in the actual project instead of generic AI assumptions;
- secure, accessible and performance-aware by construction.

## 1. Project Context Contract

Before generating or changing code, build a non-secret `Development Context` from the Beta Map plus repository inspection. At minimum capture:

- WordPress version and target PHP version;
- block theme, classic theme or hybrid architecture;
- active theme plus parent/child relationship;
- complete regular and must-use plugin inventory;
- relevant custom post types, taxonomies, blocks, REST namespaces and hooks;
- build tooling and package manager, if present;
- existing coding conventions, namespaces, prefixes and directory structure;
- runtime/environment constraints;
- feature objective and explicit non-goals;
- acceptance criteria;
- authoritative documentation references;
- rollback strategy.

Do not include cookies, nonces, passwords, API secrets, customer/order data or other sensitive production values.

## 2. Instruction Contract

Translate the request into deterministic engineering instructions before code generation.

The instruction contract must state:

1. **Goal** — what user-visible or system behavior must exist.
2. **Scope** — files/components expected to change.
3. **Constraints** — versions, APIs, compatibility, accessibility, performance, security and deployment limits.
4. **Architecture** — theme, plugin, block, REST or integration boundary selected and why.
5. **Acceptance criteria** — observable conditions that define completion.
6. **Verification plan** — lint, tests, WordPress runtime checks, browser checks and rollback validation.
7. **Stop conditions** — ambiguity or missing evidence that must block implementation rather than trigger invention.

A vague prompt is not an implementation plan.

## 3. Normative Grounding

Before material WordPress API, lifecycle or security decisions:

- query the `wordpress-knowledge` MCP;
- prefer official WordPress Developer Resources and handbooks;
- link or record the specific reference used for non-trivial APIs;
- verify third-party plugin/provider behavior against current official documentation;
- treat community examples as experience, not normative truth.

Never generate an API, hook, REST route, option name or plugin behavior from memory when authoritative verification is available.

## 4. Plan Before Mutation

Use analysis/chat/planning capability to review the context and produce a short implementation sequence before editing files.

For each step define:

- files affected;
- expected behavior change;
- dependency on prior steps;
- test or observable proving the step works.

Prefer a sequence of small coherent changes over one giant generated rewrite. AI is used to accelerate implementation, not to remove engineering checkpoints.

## 5. Diff-First Execution

For existing projects:

- inspect the current implementation before editing;
- preserve established architecture unless there is a documented reason to refactor;
- generate the smallest coherent diff that satisfies the requirement;
- review generated code before applying follow-up steps;
- do not replace whole files merely because regeneration is easier;
- do not silently remove hooks, filters, REST behavior or plugin compatibility paths.

For new projects, scaffold the minimum viable WordPress-native structure first, verify it loads, then add behavior incrementally.

## 6. Clean Code Rules

### PHP / WordPress

- Follow WordPress Coding Standards where compatible with the existing project.
- Use descriptive names and small focused functions/methods.
- Keep bootstrap code thin; move domain behavior into focused modules/classes where complexity justifies it.
- Avoid god classes, giant `functions.php` files and duplicated hook registration.
- Use namespaces or collision-safe prefixes consistently.
- Keep WordPress hooks at the integration boundary and business rules in testable units where practical.
- Prefer dependency injection or explicit collaborators for testable services; do not introduce an IoC framework without need.
- Never hard-code production URLs, credentials, filesystem paths or environment-specific values.
- Use Settings API, Options API, Metadata API, REST API and documented extension points instead of direct table coupling when appropriate.
- Validate intent and type, sanitize input, check capabilities/nonces, and escape at output.
- Make strings translatable when the surrounding project is internationalized.

### JavaScript / Blocks

- Respect the repository's existing build toolchain.
- Prefer WordPress packages and block APIs already used by the project.
- Keep editor and frontend concerns separated.
- Avoid global mutable state and undocumented DOM coupling.
- Preserve keyboard operation, focus behavior and accessible names.

### CSS / UI

- Reuse the theme/design-system tokens before adding new constants.
- Scope selectors to avoid leaking into admin/site-wide surfaces.
- Avoid `!important` as a routine conflict-resolution strategy.
- Maintain responsive behavior and reduced-motion/accessibility expectations.

## 7. WordPress-Native Architecture Selection

Prefer the narrowest supported extension point:

1. existing plugin/theme configuration;
2. block/pattern/template/theme.json customization;
3. child theme or site-specific plugin;
4. custom plugin or block using documented APIs;
5. direct database/file mutation only when safer supported paths do not exist.

Never edit WordPress core for product behavior.

When a feature can live independently of the theme, prefer a plugin/site plugin so theme replacement does not destroy business behavior.

## 8. Creation Mode

When creating a WordPress project, plugin, theme or block:

1. define context and compatibility matrix;
2. choose WordPress-native project boundary;
3. scaffold minimal loadable structure;
4. add activation/setup logic only when required;
5. implement one functional slice at a time;
6. verify in WordPress after every meaningful slice;
7. add automated tests/lint where the project supports them;
8. document public hooks, settings, REST routes and operational requirements;
9. run final security/accessibility/performance review;
10. package/deploy only after rollback is proven.

## 9. Modification Mode

When altering an existing project:

1. inspect repository plus Beta Map;
2. identify current feature ownership and integration points;
3. reproduce the current behavior before changing it when risk is non-trivial;
4. create a minimal change plan;
5. apply a narrow diff;
6. run targeted tests first, then broader regression checks;
7. compare resulting frontend/admin behavior against acceptance criteria;
8. preserve backward compatibility unless breaking behavior is explicitly approved;
9. record migration/rollback implications.

## 10. Verification Matrix

Use the checks that exist in the project; do not fabricate tooling. Typical checks include:

- `php -l` for changed PHP files;
- PHPCS with WordPress Coding Standards when configured;
- PHPUnit or project-specific PHP tests;
- WordPress/plugin test suites when available;
- JavaScript lint/unit tests when configured;
- build verification for block/theme assets;
- WP-CLI/runtime activation smoke test;
- REST endpoint permission/nonce behavior;
- visual/browser smoke checks;
- keyboard/focus/accessibility verification;
- query count/cache/performance sanity checks for changed hot paths;
- production rollback rehearsal for high-risk changes.

Do not claim a check passed unless it was actually executed and evidence exists.

## 11. AI Failure Guards

Block or return `REVIEW` when the assistant:

- invents a WordPress hook/API/plugin capability;
- ignores the existing project structure;
- proposes core edits for feature work;
- generates code without capability, nonce, validation/sanitization/escaping requirements where applicable;
- introduces hidden network calls or new dependencies without justification;
- replaces large areas of code without a requirement-driven reason;
- cannot explain the generated architecture and verification path;
- cannot identify a rollback path for a production mutation.

## 12. Maintainability Definition of Done

A change is not complete merely because it renders correctly once. Completion requires:

- code understandable by another WordPress engineer without reconstructing AI prompts;
- responsibilities and integration points are clear;
- no secret or environment-specific coupling;
- tests/checks appropriate to the project pass;
- public extension points/configuration are documented when relevant;
- support/diagnostic path is obvious;
- rollback exists for production risk;
- resulting behavior is verified in WordPress, not inferred from generated code alone.
