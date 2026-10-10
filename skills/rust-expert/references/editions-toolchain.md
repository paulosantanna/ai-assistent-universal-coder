# Editions & Toolchain Reference

Updated: 2026-10-10

---

## Edition Overview

| Edition | Rust Version | Key Changes | Migration |
|---------|--------------|-------------|-----------|
| 2015 | 1.0+ | Baseline | — |
| 2018 | 1.31+ | Module system, `?` in `main`, `async/await` (1.39), NLL | `cargo fix --edition` |
| 2021 | 1.56+ | Prelude changes, `IntoIterator` for arrays, disjoint capture, `cargo` features | `cargo fix --edition` |
| 2024 | 1.85+ | Async closures, `gen` blocks, `Future::poll` ergonomics, `..` patterns, `use` in macros | `cargo fix --edition` |

---

## Detecting Edition & MSRV

```toml
# Cargo.toml (package root)
[package]
name = "my-crate"
version = "0.1.0"
edition = "2024"          # 2015, 2018, 2021, 2024
rust-version = "1.85"     # MSRV (Minimum Supported Rust Version)
```

```toml
# Cargo.toml (workspace root)
[workspace]
resolver = "2"            # Required for edition 2021+
members = ["crates/*"]
```

```bash
# CLI detection
cargo metadata --format-version=1 | jq '.packages[] | {name, edition, rust_version}'
rustc --version
cargo --version
rustup show
```

---

## Migration Commands

```bash
# Dry run (see what would change)
cargo fix --edition --dry-run --workspace

# Actual migration
cargo fix --edition --workspace

# Specific edition
cargo fix --edition 2024 --workspace

# With idiomatic lints
cargo fix --edition --workspace -- --edition2024
```

---

## 2024 Edition Key Changes

### Async Closures
```rust
// Before: manual Future implementation or async block
let fut = async move { do_work().await };

// 2024: async closures (stabilized)
let fut = async || do_work().await;
```

### Gen Blocks (Generators)
```rust
// 2024: gen blocks for iterators/async streams
let iter = gen {
    yield 1;
    yield 2;
    yield 3;
};

let stream = async gen {
    yield fetch_data().await;
};
```

### Future::poll Ergonomics
```rust
// 2024: poll methods take Pin<&mut Self> automatically in more contexts
// Less manual Pin::new(&mut future) boilerplate
```

### Range Patterns with `..`
```rust
// 2024: rest patterns in matches
match slice {
    [first, .., last] => { /* ... */ }
    [single] => { /* ... */ }
    [] => { /* ... */ }
}
```

### `use` in Macro Rules
```rust
// 2024: use declarations inside macro_rules!
macro_rules! example {
    () => {
        use std::collections::HashMap;
        // ...
    };
}
```

---

## MSRV Policy

### Recommended MSRV Strategy

```toml
# Cargo.toml
[package]
rust-version = "1.80"  # Update every 6 months (2 releases)

# CI: test MSRV and latest stable
# .github/workflows/ci.yml
jobs:
  test:
    strategy:
      matrix:
        rust: [1.80, "stable"]  # MSRV + latest
```

### MSRV Compatibility Checks

```bash
# Test with MSRV
rustup install 1.80
rustup override set 1.80
cargo test --workspace

# Use cargo-msrv for automated MSRV detection
cargo install cargo-msrv
cargo msrv find
cargo msrv verify
```

---

## Toolchain Management

### rust-toolchain.toml (Preferred)
```toml
[toolchain]
channel = "stable"        # or "1.85", "nightly-2024-10-01"
components = ["rustfmt", "clippy", "rust-src"]
targets = ["x86_64-unknown-linux-gnu", "wasm32-unknown-unknown"]
profile = "minimal"
```

### rustup Commands
```bash
# Install specific version
rustup install 1.85.0

# Set default
rustup default stable

# Per-project override
rustup override set 1.85.0

# Show active toolchain
rustup show

# Update
rustup update
```

### CI Matrix Example
```yaml
# .github/workflows/ci.yml
strategy:
  matrix:
    rust:
      - 1.80    # MSRV
      - stable  # Latest
      - beta    # Pre-release testing
    os: [ubuntu-latest, macos-latest, windows-latest]
```

---

## Cargo Profiles

```toml
# Cargo.toml
[profile.dev]
opt-level = 0
debug = true
split-debuginfo = "unpacked"  # Faster linking on Linux

[profile.release]
opt-level = 3
lto = true                    # Link-time optimization
codegen-units = 1             # Better optimization
panic = "abort"               # Smaller binaries, no unwinding
strip = true                  # Strip symbols (requires cargo-strip)

[profile.bench]
opt-level = 3
lto = true
debug = false
```

---

## Common Edition Migration Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| `extern crate` required | 2015 edition | Remove `extern crate` (2018+) |
| `try!` macro | Pre-`?` operator | Replace with `?` |
| Module paths | 2018 module system | Use `crate::`, `super::`, `self::` |
| `IntoIterator` for arrays | 2021 edition | `for x in array` works directly |
| Async fn in traits | Pre-1.75 | Use `async_trait` crate or upgrade |
| Capture disjoint fields | 2021 edition | Automatic, but may change borrowck |
| `format_args!` in macros | 2024 edition | Use `use` in macro_rules! |

---

## References

- [Edition Guide](https://doc.rust-lang.org/edition-guide/)
- [Rust 2024 Release Notes](https://blog.rust-lang.org/2025/02/20/Rust-1.85.0/)
- [cargo-fix Documentation](https://doc.rust-lang.org/cargo/commands/cargo-fix.html)
- [cargo-msrv](https://github.com/foresterre/cargo-msrv)