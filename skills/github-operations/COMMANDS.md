# GitHub Operations Commands

These are governed command intents resolved by AEOS. They are not unrestricted shell aliases.

## Read-only

- `aeos github auth status`
- `aeos github repo inspect`
- `aeos github branch list`
- `aeos github pr inspect`
- `aeos github workflow list`
- `aeos github workflow inspect`
- `aeos github actions status`
- `aeos github bundle verify`

## Governed mutation

- `aeos github branch create`
- `aeos github commit create`
- `aeos github fetch`
- `aeos github pull`
- `aeos github push`
- `aeos github pr create`
- `aeos github pr update`
- `aeos github actions rerun-failed`
- `aeos github actions rerun-job`
- `aeos github bundle create`

## Explicit approval required

- `aeos github branch delete`
- `aeos github protection apply`
- `aeos github release publish`
- `aeos github workflow dispatch`
- `aeos github merge execute`

Merge execution must include the expected current head SHA and revalidate it immediately before mutation.

## Permanent deny command

`aeos github repo delete` exists only as a policy surface and must return `DENY_PERMANENT: REPOSITORY_DELETION_MANUAL_ONLY`. It must not invoke Git, GitHub CLI or GitHub API.

## Input safety

All implementation adapters must use structured arguments, validated repository roots/refs and bounded timeouts. User-controlled command strings, `shell=true`, control operators and credential-bearing command arguments are forbidden.
