<!-- Package: 00_skills/(development)/rust-expert; relative command/resource examples resolve from that package or workspace root. -->

## Execution

BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF

### Recon (Mandatory First Pass)

- Read `Cargo.toml` / `Cargo.lock` / `Cargo.workspace` for: edition, resolver, workspace members, features, MSRV, profiles, `[patch]`, `[replace]`.
- Detect toolchain: `rustup show`, `rustc --version`, CI matrix, devcontainer/base image.
- Map crate graph: `cargo tree -d`, `cargo metadata --format-version=1`.
- Identify async runtime (tokio/async-std/custom), web framework (axum/actix/warp/rocket), DB driver (sqlx/diesel/sea-orm), serialization (serde/bincode/postcard).
- Locate `rustfmt.toml`, `clippy.toml`, `deny.toml`, `.cargo/config.toml`, `Makefile`/`justfile`/`Taskfile.yml`.
- Baseline: `cargo check`, `cargo test --workspace`, `cargo clippy --workspace -- -D warnings`, `cargo fmt --check`.

### Plan

- Target the detected edition/MSRV; avoid edition migration unless explicitly requested.
- Prefer surgical changes: single crate, single module, minimal public API surface.
- For migrations: baseline build/tests/perf → dependency compatibility → staged edition/toolchain change → behavior/security/perf verification → rollback/docs.
- For new code: follow project's error handling style (thiserror/anyhow/eyre), async patterns, module structure, testing conventions.

### Execute

- Use idiomatic code for the declared edition; preserve project conventions.
- Avoid dependency additions if an existing crate suffices (`cargo tree -i <crate>`).
- Make changes surgical: one logical change per commit/PR.
- Handle realistic errors: never `.unwrap()`/`.expect()` in production paths without justification.
- Comments explain non-obvious WHY, not WHAT.

### Verify

Project-native checks in order:

1. `cargo check --workspace --all-targets`
2. `cargo test --workspace --all-targets` (unit + integration + doc tests)
3. `cargo clippy --workspace --all-targets -- -D warnings`
4. `cargo fmt --check`
5. `cargo audit` (if `cargo-audit` installed)
6. `cargo deny check` (if `cargo-deny` configured)
7. Build/release profile smoke test: `cargo build --release --workspace`
8. Benchmarks if affected: `cargo bench --workspace`
