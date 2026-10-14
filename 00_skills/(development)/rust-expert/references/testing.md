# Testing Reference

Updated: 2026-10-10

---

## Test Organization

### Unit Tests (Inline)
```rust
// src/lib.rs
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
    }

    #[test]
    fn test_add_negative() {
        assert_eq!(add(-1, 1), 0);
    }
}
```

### Integration Tests (tests/ directory)
```rust
// tests/integration_test.rs
use my_crate::UserRepo;

#[tokio::test]
async fn test_user_repo() {
    let pool = setup_test_db().await;
    let repo = UserRepo::new(pool);

    let user = repo.create("test@example.com", "Test", "hash").await.unwrap();
    assert_eq!(user.email, "test@example.com");
}
```

### Doc Tests
```rust
/// Adds two numbers.
/// 
/// # Examples
/// 
/// ```
/// let result = my_crate::add(2, 3);
/// assert_eq!(result, 5);
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

---

## Running Tests

```bash
# All tests (unit + integration + doc)
cargo test --workspace

# Unit tests only
cargo test --lib

# Integration tests only
cargo test --test integration_test

# Specific test
cargo test test_user_repo

# With output
cargo test -- --nocapture

# Filter by pattern
cargo test user

# Run ignored tests
cargo test -- --ignored

# Threads
cargo test -- --test-threads=4

# List tests without running
cargo test -- --list
```

---

## Async Testing

### Tokio Test Attribute
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_async_function() {
        let result = my_async_fn().await;
        assert_eq!(result, expected);
    }

    #[tokio::test(flavor = "multi_thread", worker_threads = 2)]
    async fn test_concurrent() {
        // Uses multi-threaded runtime
    }

    #[tokio::test]
    async fn test_with_time_control() {
        // Pause time for deterministic tests
        tokio::time::pause();
        
        let handle = tokio::spawn(async {
            tokio::time::sleep(Duration::from_secs(1)).await;
            "done"
        });

        // Advance time
        tokio::time::advance(Duration::from_secs(1)).await;
        
        let result = handle.await.unwrap();
        assert_eq!(result, "done");
    }
}
```

---

## Property-Based Testing (proptest)

### Cargo.toml
```toml
[dev-dependencies]
proptest = "1.0"
```

### Basic Usage
```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn test_add_commutative(a: i32, b: i32) {
        prop_assert_eq!(add(a, b), add(b, a));
    }

    #[test]
    fn test_add_assoc(a: i32, b: i32, c: i32) {
        prop_assert_eq!(add(add(a, b), c), add(a, add(b, c)));
    }

    #[test]
    fn test_string_reverse_twice(s in ".*") {
        let reversed: String = s.chars().rev().collect();
        let twice: String = reversed.chars().rev().collect();
        prop_assert_eq!(s, twice);
    }
}

// Custom strategies
fn arb_user_id() -> impl Strategy<Value = Uuid> {
    prop::collection::vec(any::<u8>(), 16)
        .prop_map(|bytes| Uuid::from_slice(&bytes).unwrap())
}

proptest! {
    #[test]
    fn test_user_id_roundtrip(id in arb_user_id()) {
        let encoded = id.to_string();
        let decoded = Uuid::parse_str(&encoded).unwrap();
        prop_assert_eq!(id, decoded);
    }
}
```

---

## Mocking (mockall)

### Cargo.toml
```toml
[dev-dependencies]
mockall = "0.13"
```

### Mocking Traits
```rust
use mockall::automock;

#[automock]
trait UserService {
    async fn get_user(&self, id: Uuid) -> Result<User, AppError>;
    async fn create_user(&self, email: &str, name: &str) -> Result<User, AppError>;
}

// In tests
#[tokio::test]
async fn test_with_mock() {
    let mut mock = MockUserService::new();
    
    mock.expect_get_user()
        .with(eq(test_id))
        .returning(|_| Ok(User { ... }));

    mock.expect_create_user()
        .with(eq("test@example.com"), eq("Test"))
        .returning(|_, _| Ok(User { ... }));

    let service = mock;
    let user = service.get_user(test_id).await.unwrap();
}
```

### Mocking Structs (via trait)
```rust
// Define trait for your struct
trait Database {
    async fn query(&self, sql: &str) -> Result<Vec<Row>>;
}

// Mock the trait
mockall::mock! {
    Database {}
    impl Database for Database {
        async fn query(&self, sql: &str) -> Result<Vec<Row>>;
    }
}
```

---

## HTTP Mocking (wiremock)

### Cargo.toml
```toml
[dev-dependencies]
wiremock = "0.5"
```

### Usage
```rust
use wiremock::{MockServer, Mock, ResponseTemplate};
use wiremock::matchers::{method, path};

#[tokio::test]
async fn test_external_api() {
    let mock_server = MockServer::start().await;

    Mock::given(method("GET"))
        .and(path("/api/users/1"))
        .respond_with(ResponseTemplate::new(200).set_body_json(json!({
            "id": 1,
            "name": "Test User"
        })))
        .mount(&mock_server)
        .await;

    let client = MyClient::new(mock_server.uri());
    let user = client.get_user(1).await.unwrap();
    assert_eq!(user.name, "Test User");
}
```

---

## Testcontainers (Real Database)

### Cargo.toml
```toml
[dev-dependencies]
testcontainers = { version = "0.16", features = ["postgres"] }
testcontainers-modules = { version = "0.16", features = ["postgres"] }
```

### Usage
```rust
use testcontainers_modules::postgres::Postgres;
use testcontainers::runners::AsyncRunner;

async fn setup_test_db() -> PgPool {
    let container = Postgres::default()
        .with_db_name("testdb")
        .with_user("test")
        .with_password("test")
        .start()
        .await
        .unwrap();

    let port = container.get_host_port_ipv4(5432).await.unwrap();
    let url = format!("postgres://test:test@localhost:{}/testdb", port);
    
    let pool = PgPool::connect(&url).await.unwrap();
    sqlx::migrate!("./migrations").run(&pool).await.unwrap();
    
    // Keep container alive for test duration
    // (Drop container after test)
    pool
}

#[tokio::test]
async fn test_with_real_postgres() {
    let pool = setup_test_db().await;
    let repo = UserRepo::new(pool);
    // ...
}
```

---

## Snapshot Testing (insta)

### Cargo.toml
```toml
[dev-dependencies]
insta = "1.34"
```

### Usage
```rust
use insta::assert_json_snapshot;

#[test]
fn test_user_serialization() {
    let user = User {
        id: uuid!("..."),
        email: "test@example.com".into(),
        name: "Test".into(),
    };
    
    let json = serde_json::to_value(&user).unwrap();
    assert_json_snapshot!(json);
}

// Update snapshots: cargo insta review
```

---

## Fuzzing (cargo-fuzz)

### Setup
```bash
cargo install cargo-fuzz
cargo fuzz init
```

### Fuzz Target
```rust
// fuzz/fuzz_target_1.rs
#![no_main]
use libfuzzer_sys::fuzz_target;
use my_crate::parse_input;

fuzz_target!(|data: &[u8]| {
    if let Ok(input) = std::str::from_utf8(data) {
        let _ = parse_input(input);
    }
});
```

```bash
# Run fuzzer
cargo fuzz run fuzz_target_1

# With corpus
cargo fuzz run fuzz_target_1 corpus/
```

---

## Benchmark Testing (criterion)

### Cargo.toml
```toml
[[bench]]
name = "my_bench"
harness = false

[dev-dependencies]
criterion = "0.5"
```

### Benchmark
```rust
// benches/my_bench.rs
use criterion::{black_box, criterion_group, criterion_main, Criterion};
use my_crate::process_data;

fn bench_process(c: &mut Criterion) {
    c.bench_function("process_data", |b| {
        b.iter(|| process_data(black_box(large_input())))
    });
}

criterion_group!(benches, bench_process);
criterion_main!(benches);
```

```bash
cargo bench
```

---

## Test Utilities

### Test Helpers
```rust
// tests/common/mod.rs
pub mod common {
    use sqlx::PgPool;

    pub async fn setup_test_db() -> PgPool {
        // ...
    }

    pub fn test_user() -> CreateUser {
        CreateUser {
            email: "test@example.com".into(),
            name: "Test User".into(),
        }
    }
}
```

```rust
// tests/integration_test.rs
mod common;

#[tokio::test]
async fn test_something() {
    let pool = common::setup_test_db().await;
    // ...
}
```

### Test Macros
```rust
// tests/macros.rs
macro_rules! assert_ok {
    ($expr:expr) => {
        match $expr {
            Ok(val) => val,
            Err(e) => panic!("Expected Ok, got Err: {:?}", e),
        }
    };
}

macro_rules! assert_err {
    ($expr:expr, $pattern:pat) => {
        match $expr {
            Err($pattern) => {},
            Ok(val) => panic!("Expected Err, got Ok: {:?}", val),
            Err(e) => panic!("Expected {:?}, got {:?}", stringify!($pattern), e),
        }
    };
}
```

---

## CI Configuration

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Rust
        uses: dtolnay/rust-toolchain@stable
        with:
          components: rustfmt, clippy
      
      - name: Cache
        uses: Swatinem/rust-cache@v2
      
      - name: Check formatting
        run: cargo fmt --all --check
      
      - name: Clippy
        run: cargo clippy --workspace --all-targets -- -D warnings
      
      - name: Test
        run: cargo test --workspace --all-features
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
      
      - name: Doc tests
        run: cargo test --workspace --doc
```

---

## Test Coverage

```bash
# Install
cargo install cargo-llvm-cov

# Run with coverage
cargo llvm-cov --workspace --all-features --html

# Open report
open target/llvm-cov/html/index.html

# LCOV for CI
cargo llvm-cov --workspace --all-features --lcov --output-path lcov.info
```

---

## Common Patterns

| Pattern | Use Case |
|---------|----------|
| `#[tokio::test]` | Async tests |
| `tokio::time::pause()` | Deterministic time |
| `mockall` | Unit test isolation |
| `wiremock` | HTTP service mocking |
| `testcontainers` | Real DB integration tests |
| `proptest` | Property-based testing |
| `insta` | Snapshot testing |
| `criterion` | Performance benchmarks |
| `cargo-fuzz` | Fuzzing |

---

## References

- [Rust Testing](https://doc.rust-lang.org/book/ch11-00-testing.html)
- [proptest](https://docs.rs/proptest/latest/proptest/)
- [mockall](https://docs.rs/mockall/latest/mockall/)
- [wiremock](https://docs.rs/wiremock/latest/wiremock/)
- [testcontainers](https://docs.rs/testcontainers/latest/testcontainers/)
- [insta](https://docs.rs/insta/latest/insta/)
- [criterion](https://docs.rs/criterion/latest/criterion/)
- [cargo-fuzz](https://github.com/rust-fuzz/cargo-fuzz)