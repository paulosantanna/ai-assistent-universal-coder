# Cargo Workspaces Reference

Updated: 2026-10-10

---

## Workspace Structure

### Recommended Layout
```
my-workspace/
├── Cargo.toml              # Workspace root
├── Cargo.lock              # Workspace lockfile
├── crates/
│   ├── core/               # Library crate
│   │   ├── Cargo.toml
│   │   └── src/lib.rs
│   ├── cli/                # Binary crate
│   │   ├── Cargo.toml
│   │   └── src/main.rs
│   └── web/                # Library crate
│       ├── Cargo.toml
│       └── src/lib.rs
├── tests/                  # Integration tests (optional)
│   └── integration_test.rs
└── rust-toolchain.toml     # Shared toolchain
```

### Root Cargo.toml
```toml
[workspace]
resolver = "2"                    # Required for edition 2021+
members = ["crates/*"]            # Glob pattern for all members
exclude = ["crates/deprecated-*"] # Optional: exclude patterns

[workspace.package]
version = "0.1.0"
edition = "2024"
rust-version = "1.85"
license = "MIT OR Apache-2.0"
repository = "https://github.com/org/repo"

[workspace.dependencies]
# Shared dependency versions
tokio = { version = "1.40", features = ["full"] }
axum = "0.7"
sqlx = { version = "0.8", features = ["runtime-tokio-rustls", "postgres"] }
serde = { version = "1.0", features = ["derive"] }
thiserror = "1.0"
anyhow = "1.0"
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter", "json"] }
metrics = "0.22"
metrics-exporter-prometheus = "0.15"

[workspace.lints]
rust = "2024"
clippy = "2024"
rustdoc = "2024"

[workspace.lints.clippy]
# Shared clippy config
pedantic = true
nursery = true
```

### Member Cargo.toml
```toml
# crates/core/Cargo.toml
[package]
name = "my-core"
version = { workspace = true }
edition = { workspace = true }
rust-version = { workspace = true }
license = { workspace = true }
repository = { workspace = true }

[dependencies]
# Inherit version from workspace
tokio = { workspace = true, features = ["rt-multi-thread", "macros", "sync"] }
serde = { workspace = true }
thiserror = { workspace = true }
# Local dependencies
my-utils = { path = "../utils" }

[features]
default = []
extra = ["tokio/fs"]
```

---

## Dependency Management

### Workspace Dependencies (Recommended)
```toml
# Root Cargo.toml
[workspace.dependencies]
tokio = { version = "1.40", features = ["full"] }

# Member Cargo.toml
[dependencies]
tokio = { workspace = true }  # Inherits version + features
# Or override features:
tokio = { workspace = true, features = ["rt-multi-thread"] }
```

### Feature Unification
```toml
# Root Cargo.toml - features are unified across workspace
[workspace]
resolver = "2"  # Enables feature unification

# If crate A depends on tokio with features=["macros"]
# and crate B depends on tokio with features=["rt-multi-thread"]
# Both get features=["macros", "rt-multi-thread"]
```

### Overriding Features
```toml
# Member Cargo.toml - disable feature unification for specific dep
[dependencies]
tokio = { workspace = true, features = [], default-features = false }
```

### Patch & Replace
```toml
# Root Cargo.toml - for local fixes or forks
[patch.crates-io]
tokio = { git = "https://github.com/tokio-rs/tokio", branch = "master" }
my-forked-crate = { path = "../my-forked-crate" }

[replace]
"crates.io:old-crate@1.0" = { git = "https://github.com/user/new-crate" }
```

---

## Common Patterns

### Flat Layout (Recommended)
```toml
# Root Cargo.toml
[workspace]
members = ["crates/*"]
```
- All crates in `crates/` directory
- Easy to discover, flat hierarchy
- Scales well to 100+ crates

### Hierarchical Layout
```toml
# Root Cargo.toml
[workspace]
members = [
    "crates/core/*",
    "crates/web/*",
    "crates/cli/*",
]
```
- Group by domain
- Useful for very large workspaces

### Binary + Library Split
```toml
# crates/my-app/Cargo.toml
[[bin]]
name = "my-app"
path = "src/main.rs"

[lib]
name = "my_app_lib"
path = "src/lib.rs"

# Allows: cargo run --bin my-app
# And: other crates can depend on my_app_lib
```

---

## Build & Test Commands

```bash
# Build all
cargo build --workspace

# Build specific crate
cargo build -p my-core

# Test all (unit + integration + doc)
cargo test --workspace

# Test specific crate
cargo test -p my-core

# Test with all features
cargo test --workspace --all-features

# Check all (faster than build)
cargo check --workspace --all-targets

# Format all
cargo fmt --all --check

# Clippy all
cargo clippy --workspace --all-targets -- -D warnings

# Doc all
cargo doc --workspace --no-deps --open

# Tree with duplicates
cargo tree -d --workspace

# Metadata for tooling
cargo metadata --format-version=1 > metadata.json
```

---

## CI Considerations

```yaml
# .github/workflows/ci.yml
jobs:
  build:
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: rustfmt, clippy
      - name: Cache
        uses: Swatinem/rust-cache@v2
      - name: Check
        run: cargo check --workspace --all-targets
      - name: Format
        run: cargo fmt --all --check
      - name: Clippy
        run: cargo clippy --workspace --all-targets -- -D warnings
      - name: Test
        run: cargo test --workspace --all-features
      - name: Doc
        run: cargo doc --workspace --no-deps
```

---

## Troubleshooting

### Version Conflicts
```bash
# Find duplicate dependencies
cargo tree -d --workspace

# Show full tree for specific crate
cargo tree -p my-core --workspace

# Resolve: align versions in [workspace.dependencies]
```

### Feature Unification Issues
```bash
# Check what features are unified
cargo metadata --format-version=1 | jq '.packages[] | select(.name=="tokio") | .features'

# Disable for specific crate
# In member Cargo.toml:
# tokio = { workspace = true, features = [], default-features = false }
```

### Circular Dependencies
```bash
# Detect
cargo tree -p crate-a -i crate-b  # Shows path from a to b
# Fix: extract common code to new crate, use trait objects, or redesign
```

### Slow Builds
```bash
# Timing analysis
cargo build --timings --workspace
# Open cargo-timing.html in browser

# Solutions:
# - Split large crates
# - Reduce monomorphization (less generics)
# - Use sccache in CI
# - Enable parallel frontend (nightly): RUSTC_BOOTSTRAP=1 cargo build -Zparallel-frontend
```

---

## References

- [Cargo Workspaces](https://doc.rust-lang.org/cargo/reference/workspaces.html)
- [Workspace Dependencies](https://doc.rust-lang.org/cargo/reference/workspaces.html#workspace-dependencies)
- [Resolver v2](https://doc.rust-lang.org/cargo/reference/resolver.html#resolver-versions)
- [Large Rust Workspaces](https://matklad.github.io/2021/08/22/large-rust-workspaces.html)