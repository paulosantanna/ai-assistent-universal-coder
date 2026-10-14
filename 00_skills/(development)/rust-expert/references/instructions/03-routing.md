<!-- Package: 00_skills/(development)/rust-expert; relative command/resource examples resolve from that package or workspace root. -->

## Routing

1. Detect Rust edition (`rust-version` in `Cargo.toml`), MSRV, `cargo --version`, CI matrix and container base image.
2. Query `docs-rust-current` (MCP) narrowly for signatures, release behavior, edition changes and migration deltas.
3. Route to domain-specific skills when applicable: `rust-async-expert`, `rust-web-expert`, `rust-cli-expert`, `rust-embedded-expert`.
4. Preserve repository conventions: formatting (`rustfmt.toml`), linting (`clippy.toml`), feature flags, dependency versions. Never upgrade editions or deps merely because newer versions exist.
