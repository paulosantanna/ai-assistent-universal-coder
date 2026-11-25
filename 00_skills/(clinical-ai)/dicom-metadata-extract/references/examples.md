# Examples

## Request

User: "Extract DICOM metadata without pixels."

## Actions

1. Confirm authorization to read the DICOM and that the output may not leave the machine.
2. Read the procedure gates and stop if evidence or permission is missing.
3. Run only the authorized command, or return that command unrun.

## Result

The artifact or command output, plus what was not executed.

## Out of scope

- diagnosis
- series preflight
- model training
