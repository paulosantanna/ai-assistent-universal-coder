---
name: rust-expert
description: "Use for Rust Expert. Implement, diagnose, modernize and migrate production Rust projects with version-correct APIs, minimal diffs, and evidence-backed verification. Use when user mentions Rust, Cargo, tokio, axum, sqlx, serde, or asks for Rust code review, migration, performance optimization, or async patterns. Do NOT use for general programming questions without Rust context."
license: CC-BY-4.0
metadata:
  author: Tech Lead's Club / CodENavi
  version: 1.0.0
---

# Rust Expert

Governance: CodENavi Full Workspace v2

## Mission

Implement, diagnose, modernize and migrate real Rust projects with version-correct APIs, minimal diffs and evidence-backed verification.

## Routing

1. Detect Rust edition (`rust-version` in `Cargo.toml`), MSRV, `cargo --version`, CI matrix and container base image.
2. Query `docs-rust-current` (MCP) narrowly for signatures, release behavior, edition changes and migration deltas.
3. Route to domain-specific skills when applicable: `rust-async-expert`, `rust-web-expert`, `rust-cli-expert`, `rust-embedded-expert`.
4. Preserve repository conventions: formatting (`rustfmt.toml`), linting (`clippy.toml`), feature flags, dependency versions. Never upgrade editions or deps merely because newer versions exist.

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

## Token Discipline

Read `references/INDEX.md`; then load only the version/reference modules required by the mission. Follow `TOKEN_PROFILE.yaml`.

## Domain Expertise (Reference Index)

See `references/INDEX.md` for deep-dive modules; read only the module(s) relevant to the mission. Key areas with load conditions:

| Domain | Core Crates / Concepts | Reference Module |
|--------|------------------------|------------------|
| **Editions & Toolchain** | 2015/2018/2021/2024, MSRV policy, `cargo fix --edition`, `rustup`, CI matrix | `references/editions-toolchain.md` |
| **Workspaces** | Flat `crates/*` layout, `resolver = "2"`, feature unification, `[workspace.dependencies]`, `[patch]` | `references/workspaces.md` |
| **Async & Tokio** | `tokio::spawn`, `select!`, `join!`, cancellation safety, `AsyncRead/Write`, backpressure, `tower` middleware | `references/async-tokio.md` |
| **Web (Axum/Actix)** | Router, extractors, State, layers, `tower::Service`, WebSocket, SSE, OpenAPI (utoipa) | `references/web-axum.md` |
| **Database (SQLx)** | Compile-time checked queries, migrations, `sqlx::query!`, `sqlx::FromRow`, connection pools, transactions | `references/database-sqlx.md` |
| **Serialization** | `serde` derives, `serde_json`/`bincode`/`postcard`, `#[serde(rename_all = "camelCase")]`, custom serializers | `references/serialization.md` |
| **Error Handling** | `thiserror` (libraries), `anyhow`/`eyre` (apps), `?` operator, `Result<T, E>` vs `Option<T>`, error contexts | `references/error-handling.md` |
| **Testing** | Unit (`#[cfg(test)]`), integration (`tests/`), doc tests, `proptest`/`quickcheck`, `mockall`/`wiremock`, `testcontainers` | `references/testing.md` |
| **Observability** | `tracing`/`tracing-subscriber`, `tracing-opentelemetry`, `metrics`/`prometheus`, structured logging, spans | `references/observability.md` |
| **Performance** | `cargo bench` + `criterion`, `perf`/`flamegraph`/`pprof`, zero-cost abstractions, `#[inline]`, PGO, `jemalloc`/`mimalloc` | `references/performance.md` |
| **Macros** | Declarative (`macro_rules!`), procedural (`proc-macro`, `syn`/`quote`), derive macros, attribute macros | `references/macros.md` |
| **Security** | `cargo audit`, `cargo deny`, supply chain, `unsafe` audit, `rust-secure-code`, fuzzing (`cargo-fuzz`, `libfuzzer`) | `references/security.md` |
| **FID/FFI** | `bindgen`, `cc`, `cxx`, `rust-bindgen`, `abi_stable`, `safer_ffi`, C/C++ interop | `references/ffi.md` |
| **Embedded** | `no_std`, `cortex-m`, `embassy`, `rtic`, `probe-run`, `defmt`, `panic-probe` | `references/embedded.md` |
| **WASM** | `wasm-bindgen`, `wasm-pack`, `web-sys`/`js-sys`, `leptos`/`yew`/`dioxus`, `wasm-opt` | `references/wasm.md` |

## Examples

### Example 1: Modernize to Rust 2024 Edition

**User says:** "Upgrade our workspace to Rust 2024 edition"

**Actions:**

1. Recon: `cargo metadata` → detect current edition, MSRV, workspace layout
2. Check compatibility: `cargo fix --edition --dry-run --workspace`
3. Plan: staged migration per crate, update `Cargo.toml` edition field, resolve new warnings
4. Execute: `cargo fix --edition --workspace`, address manual fixes (async closures, `IntoIterator` changes)
5. Verify: full test suite, clippy, fmt, bench regression check
6. Document: update `README.md` MSRV, changelog, CI matrix

**Result:** Workspace compiles on 2024 edition, all tests pass, no performance regression.

### Example 2: Add SQLx with Compile-Time Checked Queries

**User says:** "Add PostgreSQL persistence with SQLx to our Axum service"

**Actions:**

1. Recon: detect Axum version, Tokio runtime, existing `Cargo.toml` features
2. Add deps: `sqlx = { version = "0.8", features = ["runtime-tokio-rustls", "postgres", "chrono", "uuid", "macros"] }`
3. Create `sqlx-data.json` via `cargo sqlx prepare --workspace`
4. Implement repository pattern with `sqlx::query!`/`query_as!`, migrations in `migrations/`
5. Configure connection pool via `sqlx::PgPoolOptions`, integrate with Axum `State`
6. Verify: `cargo check`, `cargo test`, `sqlx migrate run`, integration tests with `testcontainers`

**Result:** Type-safe DB layer, migrations versioned, compile-time query verification.

### Example 3: Diagnose Async Cancellation Bug

**User says:** "Our tokio task drops data on shutdown — fix the graceful shutdown"

**Actions:**

1. Recon: locate `tokio::spawn` sites, `Shutdown` signal handling, `JoinHandle` management
2. Identify: missing `AbortHandle`/`CancellationToken`, unguarded `select!` branches
3. Fix: wrap critical sections in `tokio::select!` with shutdown token, use `graceful_shutdown` crate or custom signal handler
4. Verify: stress test with `tokio::time::timeout`, simulate SIGTERM, assert no data loss

**Result:** Clean shutdown on SIGTERM/SIGINT, in-flight requests complete, no panics.

## Troubleshooting

### Error: `error[E0554]: #![feature] may not be used on the stable release channel`

**Cause:** Using nightly-only features on stable toolchain.

**Solution:**

1. Check `rust-toolchain.toml` or CI for `nightly`/`beta` channel
2. Either: switch to nightly (`rustup override set nightly`), OR remove `#![feature(...)]` and use stable alternatives
3. For `type_ascription`, `generic_const_exprs`, `async_fn_in_trait` — check if stabilized in current edition

### Error: `error: failed to run custom build command for \`openssl-sys\``

**Cause:** Missing system OpenSSL dev headers.

**Solution:**

1. Install: `apt-get install libssl-dev pkg-config` (Debian/Ubuntu), `brew install openssl@3` (macOS)
2. Set env: `export OPENSSL_DIR=/usr/local/opt/openssl@3` (macOS)
3. Or use `rustls`/`aws-lc-rs` instead of `openssl` crate

### Error: `cargo test` hangs / deadlocks in async tests

**Cause:** Blocking on async runtime, missing `tokio::test` attribute, shared state.

**Solution:**

1. Use `#[tokio::test]` (not `#[test]`) for async tests
2. Avoid `.block_on()` in tests; use `tokio::test` with `await`
3. Isolate runtime per test: `#[tokio::test(flavor = "multi_thread")]`
4. Use `tokio::sync::oneshot` for synchronization instead of `std::sync`

### Error: `cargo build --release` produces much larger binary

**Cause:** Debug symbols, LTO not enabled, panic=unwind.

**Solution:**

1. `Cargo.toml`: `[profile.release] lto = true, codegen-units = 1, panic = "abort", strip = true`
2. `cargo strip` post-build (if `cargo-strip` installed)
3. Consider `cargo build --release --target=x86_64-unknown-linux-musl` for static linking

### Error: `error[E0277]: the trait bound \`...: Send\` is not satisfied`

**Cause:** Future not `Send` due to non-Send types in async block (e.g., `Rc`, `RefCell`, `*const T`).

**Solution:**

1. Use `Arc`/`Mutex`/`RwLock` instead of `Rc`/`RefCell`
2. Avoid holding non-Send guards across `.await`
3. Use `tokio::task::spawn_local` for !Send futures on single-threaded runtime
4. Enable `#![warn(clippy::future_not_send)]` for early detection

## Common Issues

### MCP Connection Failed

If `docs-rust-current` MCP unavailable:

1. Fallback: `https://doc.rust-lang.org/stable/` + `https://doc.rust-lang.org/cargo/` + `https://docs.rs/`
2. Use `cargo doc --open --no-deps` for local docs
3. Check `rustup doc --std` for offline stdlib docs

### Dependency Resolution Fails

1. `cargo update -p <crate> --precise <version>` to pin
2. Check `[patch]` / `[replace]` in `Cargo.toml` for overrides
3. `cargo tree -d` to find version conflicts
4. Use `cargo minimal-versions` to test lower bounds

### Compile Times Too Slow

1. `cargo build --timings` → analyze `cargo-timing.html`
2. Enable `sccache`/`rust-cache` in CI
3. Split large crates, reduce monomorphization, avoid excessive generics
4. Use `cargo check` instead of `cargo build` during development