# Examples

## Request

User: "Optimize MoE training from measured evidence."

## Actions

1. Freeze batch, sequence, precision, and the metric before changing flags.
2. Read the procedure gates and stop if evidence or permission is missing.
3. Run only the authorized command, or return that command unrun.

## Result

The artifact or command output, plus what was not executed.

## Out of scope

- hardware seed tables alone
- dispatcher pick without a profile
- lint
