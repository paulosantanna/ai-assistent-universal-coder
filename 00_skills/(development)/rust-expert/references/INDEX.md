# Rust Expert — Reference Index

Progressive disclosure: SKILL.md loads this index; the agent reads ONLY the module(s) relevant to the current mission.

Updated: 2026-10-10

---

## Module Map

| Module | Path | When to Read |
|--------|------|--------------|
| **Editions & Toolchain** | `editions-toolchain.md` | Edition migration, MSRV policy, CI matrix, `rustup` |
| **Workspaces** | `workspaces.md` | Multi-crate layout, resolver v2, feature unification, `[patch]` |
| **Async & Tokio** | `async-tokio.md` | `tokio::spawn`, `select!`, cancellation safety, backpressure, Tower |
| **Web (Axum)** | `web-axum.md` | Router, extractors, State, layers, WebSocket, OpenAPI (utoipa) |
| **Database (SQLx)** | `database-sqlx.md` | Compile-time queries, migrations, `sqlx::query!`, pools, transactions |
| **Serialization** | `serialization.md` | `serde` derives, formats, custom serializers, `serde_with` |
| **Error Handling** | `error-handling.md` | `thiserror`/`anyhow`/`eyre`, `?` operator, error contexts |
| **Testing** | `testing.md` | Unit, integration, doc tests, property testing, mocking, testcontainers |
| **Observability** | `observability.md` | `tracing`, OpenTelemetry, metrics, structured logging, spans |
| **Performance** | `performance.md` | `criterion`, `perf`/`flamegraph`, PGO, allocators, inline hints |
| **Macros** | `macros.md` | Declarative, procedural, derive, attribute, `syn`/`quote` |
| **Security** | `security.md` | `cargo audit`, `cargo deny`, supply chain, `unsafe` audit, fuzzing |
| **FFI** | `ffi.md` | `bindgen`, `cxx`, `rust-bindgen`, C/C++ interop, `safer_ffi` |
| **Embedded** | `embedded.md` | `no_std`, `cortex-m`, `embassy`, `rtic`, `defmt` |
| **WASM** | `wasm.md` | `wasm-bindgen`, `wasm-pack`, `leptos`/`yew`, `wasm-opt` |

---

## Quick Reference: Edition Features

| Edition | Key Features | Migration Command |
|---------|--------------|-------------------|
| 2015 | Baseline | — |
| 2018 | Module system, `?` in main, `async/await` (later) | `cargo fix --edition` |
| 2021 | Prelude changes, `IntoIterator` for arrays, disjoint capture | `cargo fix --edition` |
| 2024 | Async closures, `gen` blocks, `Future::poll` ergonomics, `..` patterns | `cargo fix --edition` |

---

## Quick Reference: Common Crate Versions (2024-2025)

| Category | Crate | Typical Version | Notes |
|----------|-------|-----------------|-------|
| Async Runtime | `tokio` | 1.40+ | `features = ["full"]` or minimal: `["rt-multi-thread", "macros", "sync", "time"]` |
| Web Framework | `axum` | 0.7+ | `features = ["default"]` |
| Database | `sqlx` | 0.8+ | `features = ["runtime-tokio-rustls", "postgres", "macros", "chrono", "uuid"]` |
| Serialization | `serde` | 1.0+ | `features = ["derive"]` |
| Error Handling | `thiserror` | 1.0+ | Libraries |
| Error Handling | `anyhow` | 1.0+ | Applications |
| Error Handling | `eyre` | 0.6+ | Applications (richer backtraces) |
| Observability | `tracing` | 0.1+ | `features = ["std"]` |
| Observability | `tracing-subscriber` | 0.3+ | `features = ["env-filter", "json", "fmt"]` |
| Observability | `tracing-opentelemetry` | 0.27+ | OTel bridge |
| Metrics | `metrics` | 0.22+ | `features = ["default"]` |
| Metrics | `metrics-exporter-prometheus` | 0.15+ | Prometheus exporter |
| Testing | `proptest` | 1.0+ | Property-based testing |
| Testing | `mockall` | 0.13+ | Mocking |
| Testing | `wiremock` | 0.5+ | HTTP mocking |
| Testing | `testcontainers` | 0.16+ | Integration tests with real containers |
| Fuzzing | `cargo-fuzz` | 0.12+ | `cargo fuzz` subcommand |
| Performance | `criterion` | 0.5+ | Benchmarking |
| Profiling | `pprof` | 0.12+ | `pprof` integration |

---

## Load Condition Reference

**Read `editions-toolchain.md` when:**
- User asks about edition migration, MSRV, or CI toolchain
- `Cargo.toml` has `rust-version` or `edition` field
- Build fails with edition-related errors

**Read `workspaces.md` when:**
- Project has `Cargo.workspace` or `[workspace]` in root `Cargo.toml`
- User mentions multi-crate, monorepo, or feature unification
- Dependency conflicts across workspace members

**Read `async-tokio.md` when:**
- Code uses `tokio::spawn`, `select!`, `join!`, `tokio::sync`
- Cancellation safety concerns, graceful shutdown
- Backpressure, `AsyncRead`/`AsyncWrite` implementation

**Read `web-axum.md` when:**
- Project uses `axum` (check `Cargo.toml`)
- User asks about routing, extractors, middleware, State, WebSocket
- OpenAPI/utoipa integration needed

**Read `database-sqlx.md` when:**
- Project uses `sqlx` (check `Cargo.toml`)
- Compile-time checked queries, migrations needed
- Connection pool configuration, transactions

**Read `serialization.md` when:**
- `serde` derives, custom serialization formats
- `serde_json`, `bincode`, `postcard`, `rmp-serde`
- Field renaming, flattening, default values, skip_serializing_if

**Read `error-handling.md` when:**
- User asks about `thiserror` vs `anyhow` vs `eyre`
- Error context, backtraces, error conversion
- Library vs application error handling patterns

**Read `testing.md` when:**
- Writing/running tests: unit, integration, doc tests
- Property-based testing with `proptest`/`quickcheck`
- Mocking with `mockall`/`wiremock`
- Testcontainers for integration tests

**Read `observability.md` when:**
- `tracing`/`tracing-subscriber` setup
- OpenTelemetry integration (traces, metrics, logs)
- Structured logging, span correlation, sampling

**Read `performance.md` when:**
- Benchmarking with `criterion`
- Profiling with `perf`/`flamegraph`/`pprof`
- PGO, allocator tuning (`jemalloc`/`mimalloc`)
- Binary size optimization

**Read `macros.md` when:**
- Writing `macro_rules!` or procedural macros
- Derive macros with `syn`/`quote`
- Attribute macros, function-like macros

**Read `security.md` when:**
- `cargo audit` / `cargo deny` integration
- Supply chain security, `unsafe` audit
- Fuzzing with `cargo-fuzz`/`libfuzzer`

**Read `ffi.md` when:**
- C/C++ interop via `bindgen`/`cxx`/`safer_ffi`
- `extern "C"` functions, `#[no_mangle]`
- Shared library creation, `abi_stable`

**Read `embedded.md` when:**
- `no_std` development, `cortex-m`, `embassy`, `rtic`
- `defmt` logging, `probe-run`, `panic-probe`
- Memory-constrained environments

**Read `wasm.md` when:**
- `wasm-bindgen`, `wasm-pack` workflow
- Frontend frameworks: `leptos`, `yew`, `dioxus`, `sycamore`
- `wasm-opt` optimization, `web-sys`/`js-sys`