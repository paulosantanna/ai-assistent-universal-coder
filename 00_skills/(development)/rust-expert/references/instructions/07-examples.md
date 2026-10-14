<!-- Package: 00_skills/(development)/rust-expert; relative command/resource examples resolve from that package or workspace root. -->

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
