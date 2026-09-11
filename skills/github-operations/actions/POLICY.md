# GitHub Actions Recovery Policy

## Authority

This subtree specializes `skills/github-operations` and `devops-pipeline-engineering` under the single `codenavi-agent`.

## Recursive recovery

A recovery cycle may continue only if:

- the target is the latest head SHA;
- the root cause has evidence;
- the patch is within authorized scope;
- Chief/Staff lens verdict is not `REJECTED`;
- focused verification and secret scan satisfy policy;
- Judge allows progression;
- cycle/time/token limits remain;
- progress detector shows useful progress or genuinely new evidence.

## Anti-cheating

Never gain green CI by deleting/weakening tests, unjustified skip/xfail, `continue-on-error` on required checks, reduced coverage, disabled security scanning, removed branch protection or invented credentials.

## Human-only blockers

Stop for missing secret values, insufficient PAT scope, required reviewer/environment approval, billing/platform outage, external service outage, destructive migration, clinical/regulatory approval or unauthorized deployment.

## Permanent deny

Repository deletion is manual-only and `DENY_PERMANENT`; recursive recovery cannot delegate or override it.
