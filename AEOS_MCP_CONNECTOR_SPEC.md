# AEOS MCP Connector Specification

## Connector Categories

```text
filesystem-readonly
filesystem-write-sandbox
git-readonly
git-controlled
test-runner-controlled
package-local
browser-readonly-future
database-readonly-future
secrets-runtime-future
```

## Connector Naming

MCP IDs must follow:

```text
<domain>-<mode>
```

Examples:

```text
filesystem-readonly
filesystem-write-sandbox
git-readonly
test-runner-controlled
package-local
```

## Tool Naming

Tools must follow:

```text
<domain>.<verb>
```

Examples:

```text
filesystem.list
filesystem.read
filesystem.write_sandbox
git.status
git.diff
test.run
package.verify
```

## Forbidden Tool Names

```text
shell.exec
secrets.dump
browser.export_cookies
git.force_push
git.merge
deploy.production
database.write
```
