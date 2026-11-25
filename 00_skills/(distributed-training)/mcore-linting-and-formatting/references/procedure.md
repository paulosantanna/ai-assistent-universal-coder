# Procedure

## Contents

- TLC gates
- Adapted upstream instructions
- Upstream modules

## TLC gates

These gates win when the adapted text disagrees.

- Confirm account, partition, node count, and the exact command before sbatch, torchrun on a shared cluster, or a container launch.
- Measured tables in the upstream text are NVIDIA point-in-time reports. Re-read the checkout and do not present them as results from this workspace.
- A destructive delete runs only when the user names the generated path and it sits inside the authorized work tree.
- Missing source, tool, permission, or checkout blocks the dependent step. Continue only independent authorized work.
- Do not create another agent identity. A role in the upstream text is a lens of `codenavi-agent`.

## Adapted upstream instructions

# Linting and Formatting

---

## Running the Formatter

Run before opening a PR:

```bash
# Check mode (no changes applied)
BASE_REF=main CHECK_ONLY=true SKIP_DOCS=false bash tools/autoformat.sh

# Fix mode
BASE_REF=main CHECK_ONLY=false bash tools/autoformat.sh
```

Tools invoked: `black`, `isort`, `pylint`, `ruff`, `mypy`.

---

## Import Ordering

After editing imports in any Python files, always run `uv run isort` on those
files before committing:

```bash
uv run isort <file1>.py <file2>.py
```

---

## Setting Up the Linting Group

Inside the container:

```bash
uv sync --locked --only-group linting
```

This installs `ruff`, `black`, `isort`, `pylint` — the same tools used by
`tools/autoformat.sh` and CI's `linting` job.

---

## Code Style Rules

- **Type hints**: required on all public API functions. Use `X | None`, not `Optional[X]`.
- **Docstrings**: Google-style on all public classes and functions.
- **Naming**: follow Python conventions — `snake_case` for functions and variables, `PascalCase` for classes.
- **Line length**: 119 characters (configured in `pyproject.toml`).
- **No bare `except`**: always catch specific exception types.

## Upstream modules

Read a module only when the request matches that mode.

- No additional upstream notes were part of this package.
