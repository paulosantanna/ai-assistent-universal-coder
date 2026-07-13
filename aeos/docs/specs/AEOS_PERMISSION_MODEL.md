# AEOS Permission Model

## Default

Deny-all by default.

Every action requires explicit capability and policy allowance.

## Capability Examples

```text
READ_REPOSITORY
READ_FILES
WRITE_SANDBOX_FILES
GENERATE_REPORT
CREATE_BRANCH
APPLY_PATCH
RUN_TESTS
CREATE_COMMIT
CREATE_PR
PACKAGE_CREATE
PACKAGE_VERIFY
PACKAGE_EXTRACT
READ_RUNTIME_SECRET
```

## Approval Required

```text
filesystem.delete
filesystem.write_outside_sandbox
patch.apply
git.commit
git.push
git.merge
git.pr.create
shell.run
secrets.read
deploy.run
database.schema_change
package.extract_over_existing
```

## Prohibited by Default

```text
force_push
merge_auto
deploy_production_auto
read_secret_values
commit_on_protected_branch
write_to_main_master_develop
shell_unrestricted
```
