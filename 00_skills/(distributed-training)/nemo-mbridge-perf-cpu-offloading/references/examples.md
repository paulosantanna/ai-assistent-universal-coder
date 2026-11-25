# Examples

## Request

User: "Offload optimizer or activations to CPU."

## Actions

1. Choose optimizer offload for large models or activation offload only where the procedure allows it.
2. Read the procedure gates and stop if evidence or permission is missing.
3. Run only the authorized command, or return that command unrun.

## Result

The artifact or command output, plus what was not executed.

## Out of scope

- CUDA graphs
- sequence packing
- Slurm conversion
