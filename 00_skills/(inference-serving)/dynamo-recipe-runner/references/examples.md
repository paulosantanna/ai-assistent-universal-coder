# Examples

## Examples

List sglang recipes that fit a single 8xB200 node:

```bash
python3 scripts/recipe_tool.py list --framework sglang --format table
```

Validate a specific recipe and resolve blockers before applying:

```bash
python3 scripts/recipe_tool.py validate recipes/nemotron-3-super-fp8/sglang/agg
```

Equivalent through the agent protocol:

```python
run_script("scripts/recipe_tool.py", args=["validate", "recipes/nemotron-3-super-fp8/sglang/agg"])
```

## Out of scope

- model training
- RAG evaluation
- video analytics
