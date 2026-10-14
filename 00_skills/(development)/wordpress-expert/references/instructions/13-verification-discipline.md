<!-- Package: 00_skills/(development)/wordpress-expert; relative command/resource examples resolve from that package or workspace root. -->

## Verification discipline

Use project tooling that actually exists. Typical applicable checks include PHP syntax, PHPCS/WordPress Coding Standards, PHPUnit/plugin tests, JS lint/tests, block/theme builds, WP-CLI activation/runtime smoke, REST permission/nonce behavior, visual/browser smoke, keyboard/focus checks and performance sanity checks.

Never fabricate test, lint, build or runtime evidence. If a tool is absent, report it as absent instead of claiming an equivalent pass.

Generated code is not considered verified until the relevant WordPress behavior is exercised or otherwise deterministically proven.
