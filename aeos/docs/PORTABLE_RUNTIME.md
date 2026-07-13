# AEOS Portable Runtime

This document defines the minimum portable runtime contract for running AEOS from
a cloned folder, external SSD or USB drive.

## Goals

- Keep local state inside the repository by default.
- Avoid hard-coded workstation paths.
- Allow a moved folder to keep working after the drive letter or mount point
  changes.
- Preserve honest diagnostics when optional toolchains are missing.

## Portable State

By default AEOS uses:

```text
.aeos/
├── venv/
├── tmp/
├── cache/
├── evidence/
└── reports/
```

The directory is ignored by git and can travel with the repository when desired.

Environment overrides:

| Variable | Purpose |
| --- | --- |
| `AEOS_PORTABLE_HOME` | Overrides the `.aeos` state directory. |
| `AEOS_PYTHON_VENV` | Points to a specific Python virtual environment. |
| `AEOS_PYTHON` | Points to a specific Python executable. |
| `AEOS_TMP` | Overrides temporary output location. |

## Bootstrap

Prepare local portable state:

```bash
npm run aeos:bootstrap
```

Create the portable Python environment and install development dependencies:

```bash
npm run aeos:bootstrap:deps
```

The bootstrap is intentionally repository-local. It does not require a global
Python virtualenv path such as `/tmp/aeos-venv`.

## Verification

Quick verification:

```bash
npm run aeos:verify
```

Full verification:

```bash
npm run aeos:verify:full
```

Full matrix with optional toolchains:

```bash
npm run test:matrix:full
```

Missing Java, Go, Rust or .NET binaries are reported as optional skips unless a
specific host is expected to provide them.

## Operational Rules

- Do not write generated state to loose root folders.
- Do not add host-specific absolute paths to versioned scripts.
- Prefer `aeos/scripts/portable_env.py` for script path resolution.
- Keep optional downloaded tools under `.tools/`.
- Keep runtime evidence, reports, caches and temporary output under `.aeos/`.
