# Examples

## Request

User: "Turn a single-node run into a Slurm sbatch job."

## Actions

1. Prefer the srun-native layout unless the checkout already uses torch.distributed.
2. Read the procedure gates and stop if evidence or permission is missing.
3. Run only the authorized command, or return that command unrun.

## Result

The artifact or command output, plus what was not executed.

## Out of scope

- single-GPU lint
- Kubernetes Dynamo recipes
- clinical fine-tune
