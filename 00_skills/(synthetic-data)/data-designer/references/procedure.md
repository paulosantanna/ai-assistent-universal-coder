# Procedure

## Contents

- TLC gates
- Adapted upstream instructions
- Upstream modules

## TLC gates

These gates win when the adapted text disagrees.

- Inspect the workspace before writing a new dataset script. Do not overwrite an existing one without confirmation.
- Do not install packages or submit a paid or shared-cluster job without confirmation.
- Do not synthesize real people, customers, or patient records the user did not authorize.
- Missing source, tool, permission, or checkout blocks the dependent step. Continue only independent authorized work.
- Do not create another agent identity. A role in the upstream text is a lens of `codenavi-agent`.

## Adapted upstream instructions

# Before You Start

Inspect the workspace for an existing dataset script before writing a new one.

# Goal

Build a synthetic dataset using the Data Designer library that matches this description:

the user-supplied dataset description

# Workflow

Use **Autopilot** mode if the user implies they don't want to answer questions — e.g., they say something like "be opinionated", "you decide", "make reasonable assumptions", "just build it", "surprise me", etc. Otherwise, use **Interactive** mode (default).

Read **only** the workflow file that matches the selected mode, then follow it:

- **Interactive** → read `workflows/interactive.md`
- **Autopilot** → read `workflows/autopilot.md`

# Rules

- Keep all columns in the output by default. The only exceptions for dropping a column are: (1) the user explicitly asks, or (2) it is a helper column that exists solely to derive other columns (e.g., a sampled person object used to extract name, city, etc.). When in doubt, keep the column.
- Do not suggest or ask about seed datasets. Only use one when the user explicitly provides seed data or asks to build from existing records. When using a seed, read `references/seed-datasets.md`.
- When the dataset requires person data (names, demographics, addresses), read `references/person-sampling.md`.
- If a dataset script that matches the dataset description already exists, ask the user whether to edit it or create a new one.

# Usage Tips and Common Pitfalls

- **Sampler and validation columns need both a type and params.** E.g., `sampler_type="category"` with `params=dd.CategorySamplerParams(...)`.
- **Jinja2 templates** in `prompt`, `system_prompt`, and `expr` fields: reference columns with `{{ column_name }}`, nested fields with `{{ column_name.field }}`.
- **`SamplerColumnConfig`:** Takes `params`, not `sampler_params`.
- **LLM judge score access:** `LLMJudgeColumnConfig` produces a nested dict where each score name maps to `{reasoning: str, score: int}`. To get the numeric score, use the `.score` attribute. For example, for a judge column named `quality` with a score named `correctness`, use `{{ quality.correctness.score }}`. Using `{{ quality.correctness }}` returns the full dict, not the numeric score.

# Troubleshooting

- **`data-designer` CLI not found:** Tell the user that `data-designer` is not installed in this environment (requires Python >= 3.11). Ask if they would like you to create a virtual environment and install it, or if they prefer to do it themselves. Do not install anything without the user's permission.
- **Network errors during preview:** A sandbox environment may be blocking outbound requests. Ask the user for permission to retry the command with the sandbox disabled. Only as a last resort, if retrying outside the sandbox also fails, tell the user to run the command themselves.

# Output Template

Write a Python file to the current directory with a `load_config_builder()` function returning a `DataDesignerConfigBuilder`. Name the file descriptively (e.g., `customer_reviews.py`). Use PEP 723 inline metadata for dependencies.

```python
# /// script
# dependencies = [
#   "data-designer", # always required
#   "pydantic", # only if this script imports from pydantic
#   # add additional dependencies here
# ]
# ///
import data_designer.config as dd
from pydantic import BaseModel, Field


# Use Pydantic models when the output needs to conform to a specific schema
class MyStructuredOutput(BaseModel):
    field_one: str = Field(description="...")
    field_two: int = Field(description="...")


# Use custom generators when built-in column types aren't enough
@dd.custom_column_generator(
    required_columns=["col_a"],
    side_effect_columns=["extra_col"],
)
def generator_function(row: dict) -> dict:
    # add custom logic here that depends on "col_a" and update row in place
    row["name_in_custom_column_config"] = "custom value"
    row["extra_col"] = "extra value"
    return row


def load_config_builder() -> dd.DataDesignerConfigBuilder:
    config_builder = dd.DataDesignerConfigBuilder()

    # Seed dataset (only if the user explicitly mentions a seed dataset path)
    # config_builder.with_seed_dataset(dd.LocalFileSeedSource(path="path/to/seed.parquet"))

    # config_builder.add_column(...)
    # config_builder.add_processor(...)

    return config_builder
```

Only include Pydantic models, custom generators, seed datasets, and extra dependencies when the task requires them.

## Upstream modules

Read a module only when the request matches that mode.

- [references/person-sampling.md](upstream/person-sampling.md)
- [references/preview-review.md](upstream/preview-review.md)
- [references/seed-datasets.md](upstream/seed-datasets.md)
- [workflows/autopilot.md](upstream/workflows/autopilot.md)
- [workflows/interactive.md](upstream/workflows/interactive.md)
