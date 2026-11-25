# Examples

## Request

User: "Preflight a DICOM series before training."

## Actions

1. Confirm the series path and the training use the user intends.
2. Read the procedure gates and stop if evidence or permission is missing.
3. Run only the authorized command, or return that command unrun.

## Result

The artifact or command output, plus what was not executed.

## Out of scope

- metadata-only extract
- diagnosis
- MRI generation
