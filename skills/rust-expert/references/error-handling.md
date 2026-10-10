# Error Handling Reference

Updated: 2026-10-10

---

## Error Handling Philosophy

| Context | Recommended Crate | Reason |
|---------|-------------------|--------|
| **Libraries** | `thiserror` | Callers need typed errors to handle |
| **Applications** | `anyhow` / `eyre` | Easy context, backtraces, less boilerplate |
| **FFI / C API** | Custom `Error` + `Into<c_int>` | Control ABI |

---

## thiserror (Libraries)

### Basic Usage
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ConfigError {
    #[error("missing required field: {field}")]
    MissingField { field: String },

    #[error("invalid value for {field}: {value}")]
    InvalidValue { field: String, value: String },

    #[error(transparent)]
    Io(#[from] std::io::Error),

    #[error(transparent)]
    Toml(#[from] toml::de::Error),

    #[error("validation failed: {0}")]
    Validation(String),
}
```

### From Trait for Conversions
```rust
#[derive(Error, Debug)]
pub enum AppError {
    #[error("database error")]
    Database(#[from] sqlx::Error),

    #[error("config error")]
    Config(#[from] ConfigError),

    #[error("serialization error")]
    Serialization(#[from] serde_json::Error),

    #[error("not found: {0}")]
    NotFound(String),
}

// Automatic conversion: sqlx::Error -> AppError::Database
let user = db.get_user(id).await?;  // ? converts sqlx::Error
```

### Custom Error with Source
```rust
#[derive(Error, Debug)]
#[error("failed to process request: {source}")]
struct ProcessError {
    #[source]
    source: Box<dyn std::error::Error + Send + Sync>,
    request_id: Uuid,
}
```

### Display vs Debug
```rust
#[derive(Error, Debug)]
enum MyError {
    #[error("user-friendly message: {msg}")]
    UserFacing { msg: String },

    #[error("internal error: {source}")]
    Internal {
        #[source]
        source: Box<dyn std::error::Error + Send + Sync>,
    },
}

// User sees: "user-friendly message: invalid email"
// Debug shows full chain: Internal { source: Io(...), ... }
```

---

## anyhow (Applications)

### Basic Usage
```rust
use anyhow::{Context, Result, anyhow};

async fn process_user(id: Uuid) -> Result<User> {
    let user = db.get_user(id)
        .await
        .context("failed to fetch user")?;

    let profile = fetch_profile(&user)
        .await
        .with_context(|| format!("failed to fetch profile for user {}", user.id))?;

    Ok(user)
}

// Main returns Result
#[tokio::main]
async fn main() -> Result<()> {
    let user = process_user(id).await?;
    println!("{:?}", user);
    Ok(())
}
```

### Backtraces
```bash
# Enable backtraces
RUST_BACKTRACE=1 cargo run

# Full backtraces
RUST_BACKTRACE=full cargo run

# In code
use anyhow::Context;
fn main() -> Result<()> {
    std::env::set_var("RUST_BACKTRACE", "1");
    // ...
}
```

### Error Chains
```rust
use anyhow::{Context, Result};

fn read_config() -> Result<Config> {
    let content = std::fs::read_to_string("config.toml")
        .context("failed to read config file")?;
    
    let config: Config = toml::from_str(&content)
        .context("failed to parse config")?;
    
    config.validate()
        .context("config validation failed")?;
    
    Ok(config)
}

// Result:
// Error: config validation failed
// Caused by: failed to parse config
// Caused by: failed to read config file
// Caused by: No such file or directory (os error 2)
```

---

## eyre (Applications - Richer Backtraces)

### Setup
```toml
# Cargo.toml
eyre = "0.6"
color-eyre = "0.6"  # Optional: pretty backtraces
```

### Usage
```rust
use eyre::{Result, Context, WrapErr};
use color_eyre::config::HookBuilder;

fn main() -> Result<()> {
    // Install pretty handler (optional)
    HookBuilder::default().install()?;

    let config = read_config().wrap_err("startup failed")?;
    // ...
    Ok(())
}
```

---

## Custom Error Types (Advanced)

### Full Implementation
```rust
use std::fmt;
use std::error::Error as StdError;

#[derive(Debug)]
pub struct MyError {
    kind: ErrorKind,
    source: Option<Box<dyn StdError + Send + Sync>>,
    context: Vec<String>,
}

#[derive(Debug)]
enum ErrorKind {
    NotFound,
    InvalidInput,
    Internal,
    Unavailable,
}

impl MyError {
    pub fn not_found(msg: impl Into<String>) -> Self {
        Self {
            kind: ErrorKind::NotFound,
            source: None,
            context: vec![msg.into()],
        }
    }

    pub fn invalid_input(msg: impl Into<String>) -> Self {
        Self {
            kind: ErrorKind::InvalidInput,
            source: None,
            context: vec![msg.into()],
        }
    }

    pub fn with_source(mut self, source: impl StdError + Send + Sync + 'static) -> Self {
        self.source = Some(Box::new(source));
        self
    }

    pub fn context(mut self, msg: impl Into<String>) -> Self {
        self.context.push(msg.into());
        self
    }
}

impl fmt::Display for MyError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{:?}: ", self.kind)?;
        for (i, ctx) in self.context.iter().rev().enumerate() {
            if i > 0 { write!(f, ": ")?; }
            write!(f, "{}", ctx)?;
        }
        if let Some(src) = &self.source {
            write!(f, " (caused by: {})", src)?;
        }
        Ok(())
    }
}

impl StdError for MyError {
    fn source(&self) -> Option<&(dyn StdError + 'static)> {
        self.source.as_ref().map(|e| e.as_ref() as _)
    }
}
```

---

## Result Type Aliases

```rust
// Library crate
pub type Result<T> = std::result::Result<T, MyError>;

// Application crate
pub type Result<T> = anyhow::Result<T>;
```

---

## Error Handling Patterns

### Pattern: Match on Error Kind
```rust
match repo.find_user(id).await {
    Ok(user) => { /* ... */ }
    Err(AppError::NotFound(_)) => { /* 404 */ }
    Err(AppError::Database(e)) => {
        tracing::error!(error = %e, "database error");
        /* 500 */
    }
    Err(e) => { /* other */ }
}
```

### Pattern: Convert to HTTP Response
```rust
impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, message) = match self {
            AppError::NotFound(msg) => (StatusCode::NOT_FOUND, msg),
            AppError::Validation(msg) => (StatusCode::BAD_REQUEST, msg),
            AppError::Unauthorized => (StatusCode::UNAUTHORIZED, "Unauthorized".into()),
            AppError::Database(e) => {
                tracing::error!(error = %e, "database error");
                (StatusCode::INTERNAL_SERVER_ERROR, "Internal error".into())
            }
        };
        (status, Json(json!({ "error": message }))).into_response()
    }
}
```

### Pattern: Retry with Backoff
```rust
use tokio::time::{sleep, Duration};

async fn with_retry<F, T, E>(mut f: F, max_retries: u32) -> Result<T, E>
where
    F: FnMut() -> Result<T, E>,
    E: std::fmt::Display,
{
    let mut delay = Duration::from_millis(100);
    for attempt in 0..=max_retries {
        match f() {
            Ok(v) => return Ok(v),
            Err(e) if attempt == max_retries => return Err(e),
            Err(e) => {
                tracing::warn!(attempt, %e, "retrying after delay");
                sleep(delay).await;
                delay *= 2; // exponential backoff
            }
        }
    }
    unreachable!()
}
```

### Pattern: Fallback
```rust
async fn get_data() -> Result<Data> {
    primary_source()
        .await
        .or_else(|e| {
            tracing::warn!(%e, "primary failed, trying fallback");
            fallback_source().await
        })
        .context("both sources failed")
}
```

---

## Common Patterns Comparison

| Pattern | Crate | Use Case |
|---------|-------|----------|
| `#[error("...")]` | `thiserror` | Library errors with messages |
| `#[from]` | `thiserror` | Automatic conversion |
| `.context("...")` | `anyhow`/`eyre` | Add context to error chain |
| `.with_context(|| ...)` | `anyhow`/`eyre` | Lazy context (avoids allocation) |
| `?` operator | std | Propagate errors |
| `Result<T, E>` | std | Function return type |
| `anyhow::Result<T>` | `anyhow` | Application return type |

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| `.unwrap()` in production | Panics on error | Use `?` or proper error handling |
| `.expect("msg")` in library | Panics, no recovery | Return `Result` |
| `Box<dyn Error>` everywhere | Loses type info | Use `thiserror` for typed errors |
| `anyhow` in public library API | Callers can't match on errors | Use `thiserror` for libraries |
| Ignoring `Result` | Silent failures | Always handle or propagate |
| `panic!` for expected errors | Not recoverable | Return `Result` with proper error type |

---

## Testing Errors

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_error_display() {
        let err = ConfigError::MissingField { field: "database_url".into() };
        assert_eq!(err.to_string(), "missing required field: database_url");
    }

    #[test]
    fn test_error_conversion() {
        let io_err = std::io::Error::new(std::io::ErrorKind::NotFound, "file missing");
        let app_err: AppError = io_err.into();
        matches!(app_err, AppError::Io(_));
    }

    #[tokio::test]
    async fn test_error_propagation() {
        let result = process_user(uuid!("00000000-0000-0000-0000-000000000000")).await;
        assert!(result.is_err());
        let err = result.unwrap_err();
        assert!(err.to_string().contains("failed to fetch user"));
    }
}
```

---

## References

- [thiserror](https://docs.rs/thiserror/latest/thiserror/)
- [anyhow](https://docs.rs/anyhow/latest/anyhow/)
- [eyre](https://docs.rs/eyre/latest/eyre/)
- [Rust Error Handling](https://doc.rust-lang.org/book/ch09-00-error-handling.html)
- [Error Handling in Rust (2024)](https://rustify.rs/articles/rust-error-handling-result-option)