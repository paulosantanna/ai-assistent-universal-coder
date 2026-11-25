# Examples

## Request

User: "Fine-tune a Hugging Face model with TAO."

## Actions

1. Inspect the model id and dataset the user is allowed to train on.
2. Read the procedure gates and stop if evidence or permission is missing.
3. Run only the authorized command, or return that command unrun.

## Result

The artifact or command output, plus what was not executed.

## Out of scope

- Megatron training
- clinical ASR
- RAG blueprint deploy
