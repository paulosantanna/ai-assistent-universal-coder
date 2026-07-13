# Change Set: Portable Runtime Foundation

Date: 2026-07-13
Scope: AEOS portable execution, local state, verification scripts, test matrix

## Objective

Make AEOS safer to run from a moved repository, external SSD or USB drive by
removing hard-coded `/tmp/aeos-venv` assumptions from the public script entry
points.

## Changes

- Added `aeos/scripts/portable_env.py` as the central path resolver.
- Added `aeos/scripts/bootstrap_portable.py` to prepare `.aeos` local state and
  a repository-local Python virtual environment.
- Updated `aeos/scripts/verify.py` to use the portable Python resolver and
  repository-local performance output.
- Updated `aeos/scripts/test_matrix.py` to resolve Python, Behave, Robot and
  output paths portably.
- Updated `aeos/scripts/toolchain_doctor.py` to report Python through the
  portable resolver.
- Added `aeos/scripts/run_portable_python.py` for package scripts that need to
  run Python module commands through the same resolver.
- Updated `package.json` scripts to call repository scripts instead of fixed
  `/tmp` executables.
- Added `aeos/docs/PORTABLE_RUNTIME.md`.
- Added governance tests for portable path behavior.

## Compatibility

The resolver still accepts the legacy `/tmp/aeos-venv` environment when it
exists. This keeps the current worktree green while allowing future portable
installations to use `.aeos/venv`.

## Rollback

Revert these files:

- `aeos/scripts/portable_env.py`
- `aeos/scripts/bootstrap_portable.py`
- `aeos/scripts/verify.py`
- `aeos/scripts/test_matrix.py`
- `aeos/scripts/toolchain_doctor.py`
- `aeos/scripts/run_portable_python.py`
- `aeos/tests/governance/test_portable_env.py`
- `aeos/tests/governance/test_toolchain_doctor.py`
- `aeos/docs/PORTABLE_RUNTIME.md`
- `aeos/docs/change-sets/2026-07-13-portable-runtime-foundation.md`
- `package.json`
