# Runtime/module boundaries

Read `package.json` type/exports/imports, lockfile and build config before changing module syntax. Treat Node, browser, workers and edge runtimes as distinct API surfaces. Verify exact API availability from the target runtime, not local machine behavior.
