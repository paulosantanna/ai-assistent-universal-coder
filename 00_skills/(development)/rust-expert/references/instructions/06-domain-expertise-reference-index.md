<!-- Package: 00_skills/(development)/rust-expert; relative command/resource examples resolve from that package or workspace root. -->

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
