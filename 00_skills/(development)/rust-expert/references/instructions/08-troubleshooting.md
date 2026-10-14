<!-- Package: 00_skills/(development)/rust-expert; relative command/resource examples resolve from that package or workspace root. -->

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
