<!-- Package: 00_skills/(development)/rust-expert; relative command/resource examples resolve from that package or workspace root. -->

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
