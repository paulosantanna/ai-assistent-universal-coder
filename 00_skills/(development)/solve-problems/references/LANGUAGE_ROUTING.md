# LANGUAGE_ROUTING.md

Use repository-native evidence before generic heuristics.

## Discovery Order

1. Error report file paths, stack frames and compiler output.
2. Manifest and lock files.
3. Test runner configuration.
4. File extension and shebang.
5. Existing CI commands.
6. Existing formatter, linter and type checker settings.

## Common Signals

| Language | Files | Manifests | Common checks |
|---|---|---|---|
| Python | `.py` | `pyproject.toml`, `requirements.txt`, `pytest.ini` | `pytest`, `ruff`, `mypy`, `bandit` |
| JavaScript | `.js`, `.cjs`, `.mjs` | `package.json`, lockfiles | `npm test`, `jest`, `vitest`, `eslint` |
| TypeScript | `.ts`, `.tsx` | `tsconfig.json`, `package.json` | `tsc`, `vitest`, `jest`, `eslint` |
| Java | `.java` | `pom.xml`, `build.gradle`, `build.gradle.kts` | `mvn test`, `gradle test`, `javac` |
| Go | `.go` | `go.mod` | `go test ./...`, `go vet ./...` |
| Rust | `.rs` | `Cargo.toml`, `Cargo.lock` | `cargo test`, `cargo clippy` |
| C# | `.cs` | `.csproj`, `.sln` | `dotnet test`, `dotnet build` |
| C/C++ | `.c`, `.cc`, `.cpp`, `.h`, `.hpp` | `CMakeLists.txt`, `Makefile` | `cmake`, `make`, compiler tests |
| Ruby | `.rb` | `Gemfile` | `bundle exec rspec`, `rubocop` |
| PHP | `.php` | `composer.json` | `composer test`, `phpunit`, `phpstan` |

## Repair Rules

- Use the language of the changed file.
- Prefer existing utilities and patterns over new abstractions.
- Add no source-code comments.
- Remove unused imports and orphan variables before verification.
- Preserve public contracts unless the error report proves the contract is wrong and approval exists.
