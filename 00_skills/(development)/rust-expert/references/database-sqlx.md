# Database (SQLx) Reference

Updated: 2026-10-10

---

## SQLx Setup

### Cargo.toml
```toml
[dependencies]
sqlx = { version = "0.8", features = [
    "runtime-tokio-rustls",  # or "runtime-tokio" / "runtime-async-std"
    "postgres",              # or "mysql", "sqlite", "mssql"
    "chrono",                # DateTime support
    "uuid",                  # UUID support
    "json",                  # JSON/JSONB support
    "macros",                # compile-time checked queries
    "migrate",               # migration support
] }
```

### Connection Pool
```rust
use sqlx::{PgPool, Pool, Postgres};

pub type DbPool = Pool<Postgres>;

pub async fn create_pool(database_url: &str) -> Result<DbPool, sqlx::Error> {
    let pool = PgPool::connect_with(
        sqlx::postgres::PgConnectOptions::new()
            .host("localhost")
            .port(5432)
            .username("user")
            .password("pass")
            .database("mydb")
            .ssl_mode(sqlx::postgres::PgSslMode::Prefer)
    )
    .max_connections(20)
    .min_connections(5)
    .acquire_timeout(Duration::from_secs(30))
    .idle_timeout(Duration::from_secs(600))
    .test_before_acquire(true)
    .build();

    // Run migrations
    sqlx::migrate!("./migrations").run(&pool).await?;

    Ok(pool)
}

// Or from DATABASE_URL
let pool = PgPool::connect(&std::env::var("DATABASE_URL")?).await?;
```

---

## Compile-Time Checked Queries

### `query!` — Returns `Vec<Row>`
```rust
use sqlx::query;

// SELECT with parameters
let rows = query!(
    "SELECT id, email, name, created_at FROM users WHERE email = $1",
    email
)
.fetch_all(&pool)
.await?;

for row in rows {
    println!("User: {} ({})", row.name, row.email);
}
```

### `query_as!` — Returns Typed Struct
```rust
use sqlx::query_as;
use uuid::Uuid;
use chrono::{DateTime, Utc};

#[derive(Debug, sqlx::FromRow)]
struct User {
    id: Uuid,
    email: String,
    name: String,
    created_at: DateTime<Utc>,
}

let users = query_as!(
    User,
    "SELECT id, email, name, created_at FROM users WHERE active = $1",
    true
)
.fetch_all(&pool)
.await?;

let user = query_as!(
    User,
    "SELECT id, email, name, created_at FROM users WHERE id = $1",
    user_id
)
.fetch_optional(&pool)
.await?;  // Returns Option<User>
```

### `query_scalar!` — Single Column
```rust
use sqlx::query_scalar;

let count: i64 = query_scalar!("SELECT COUNT(*) FROM users WHERE active = $1", true)
    .fetch_one(&pool)
    .await?;

let emails: Vec<String> = query_scalar!("SELECT email FROM users WHERE active = $1", true)
    .fetch_all(&pool)
    .await?;
```

### `query_file!` — SQL from File
```rust
// queries/get_user.sql
// SELECT id, email, name, created_at FROM users WHERE id = $1

let user = query_file_as!(User, "queries/get_user.sql", user_id)
    .fetch_optional(&pool)
    .await?;
```

---

## Transactions

```rust
use sqlx::Transaction;

async fn transfer(
    pool: &DbPool,
    from: Uuid,
    to: Uuid,
    amount: i64,
) -> Result<(), sqlx::Error> {
    let mut tx: Transaction<'_, Postgres> = pool.begin().await?;

    // Deduct from source
    query!(
        "UPDATE accounts SET balance = balance - $1 WHERE id = $2 AND balance >= $1",
        amount, from
    )
    .execute(&mut *tx)
    .await?;

    // Add to destination
    query!(
        "UPDATE accounts SET balance = balance + $1 WHERE id = $2",
        amount, to
    )
    .execute(&mut *tx)
    .await?;

    // Record transfer
    query!(
        "INSERT INTO transfers (from_id, to_id, amount) VALUES ($1, $2, $3)",
        from, to, amount
    )
    .execute(&mut *tx)
    .await?;

    tx.commit().await?;
    Ok(())
}

// Automatic rollback on error
async fn with_transaction<F, T>(pool: &DbPool, f: F) -> Result<T, sqlx::Error>
where
    F: for<'c> FnOnce(&mut Transaction<'c, Postgres>) -> Result<T, sqlx::Error>,
{
    let mut tx = pool.begin().await?;
    let result = f(&mut tx).await;
    match result {
        Ok(v) => { tx.commit().await?; Ok(v) }
        Err(e) => { tx.rollback().await?; Err(e) }
    }
}
```

---

## Migrations

### Creating Migrations
```bash
# Create migration files
sqlx migrate add create_users_table
# Creates: migrations/20240101000000_create_users_table.sql

# Run migrations
sqlx migrate run

# Revert last migration
sqlx migrate revert

# Check migration status
sqlx migrate info
```

### Migration Files
```sql
-- migrations/20240101000000_create_users_table.sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_active ON users(active);

-- Add trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

### Migration Source (for `sqlx::migrate!`)
```rust
// Include migrations in binary
sqlx::migrate!("./migrations").run(&pool).await?;

// Or embedded (for single binary deployment)
sqlx::migrate!().run(&pool).await?;
```

### Offline Migration Preparation
```bash
# Generate sqlx-data.json for compile-time checking without DB
cargo sqlx prepare --workspace

# Check queries without DB
cargo sqlx prepare --check
```

---

## Repository Pattern

```rust
use sqlx::PgPool;
use uuid::Uuid;
use chrono::{DateTime, Utc};
use thiserror::Error;

#[derive(Error, Debug)]
pub enum UserRepoError {
    #[error("not found")]
    NotFound,
    #[error("duplicate email")]
    DuplicateEmail,
    #[error("database error: {0}")]
    Database(#[from] sqlx::Error),
}

#[derive(Clone)]
pub struct UserRepo {
    pool: PgPool,
}

impl UserRepo {
    pub fn new(pool: PgPool) -> Self {
        Self { pool }
    }

    pub async fn create(&self, email: &str, name: &str, password_hash: &str) -> Result<User, UserRepoError> {
        let user = query_as!(
            User,
            r#"
            INSERT INTO users (email, name, password_hash)
            VALUES ($1, $2, $3)
            RETURNING id, email, name, created_at
            "#,
            email, name, password_hash
        )
        .fetch_one(&self.pool)
        .await
        .map_err(|e| match e {
            sqlx::Error::Database(db_err) if db_err.constraint() == Some("users_email_key") => {
                UserRepoError::DuplicateEmail
            }
            e => UserRepoError::Database(e),
        })?;
        Ok(user)
    }

    pub async fn find_by_id(&self, id: Uuid) -> Result<User, UserRepoError> {
        let user = query_as!(
            User,
            "SELECT id, email, name, created_at FROM users WHERE id = $1",
            id
        )
        .fetch_optional(&self.pool)
        .await?
        .ok_or(UserRepoError::NotFound)?;
        Ok(user)
    }

    pub async fn find_by_email(&self, email: &str) -> Result<User, UserRepoError> {
        let user = query_as!(
            User,
            "SELECT id, email, name, created_at FROM users WHERE email = $1",
            email
        )
        .fetch_optional(&self.pool)
        .await?
        .ok_or(UserRepoError::NotFound)?;
        Ok(user)
    }

    pub async fn list(&self, limit: i64, offset: i64) -> Result<Vec<User>, UserRepoError> {
        let users = query_as!(
            User,
            "SELECT id, email, name, created_at FROM users WHERE active = true ORDER BY created_at DESC LIMIT $1 OFFSET $2",
            limit, offset
        )
        .fetch_all(&self.pool)
        .await?;
        Ok(users)
    }

    pub async fn update(&self, id: Uuid, name: Option<&str>, email: Option<&str>) -> Result<User, UserRepoError> {
        // Build dynamic query
        let mut query = "UPDATE users SET updated_at = now()".to_string();
        let mut params: Vec<Box<dyn sqlx::Encode<'_, Postgres> + Send + Sync>> = vec![];

        if let Some(name) = name {
            query.push_str(", name = $");
            query.push_str(&(params.len() + 1).to_string());
            params.push(Box::new(name.to_string()));
        }
        if let Some(email) = email {
            query.push_str(", email = $");
            query.push_str(&(params.len() + 1).to_string());
            params.push(Box::new(email.to_string()));
        }

        query.push_str(" WHERE id = $");
        query.push_str(&(params.len() + 1).to_string());
        query.push_str(" RETURNING id, email, name, created_at");
        params.push(Box::new(id));

        // Execute with dynamic query (loses compile-time checking)
        // Better: use separate typed queries for each combination
        // This is a simplified example
        todo!("Use typed queries per field combination")
    }

    pub async fn delete(&self, id: Uuid) -> Result<(), UserRepoError> {
        let result = query!("DELETE FROM users WHERE id = $1", id)
            .execute(&self.pool)
            .await?;

        if result.rows_affected() == 0 {
            return Err(UserRepoError::NotFound);
        }
        Ok(())
    }
}
```

---

## Advanced Patterns

### JSON/JSONB
```rust
use serde::{Deserialize, Serialize};
use sqlx::types::Json;

#[derive(Debug, Serialize, Deserialize, sqlx::FromRow)]
struct UserProfile {
    id: Uuid,
    user_id: Uuid,
    preferences: Json<UserPreferences>,
    metadata: Json<serde_json::Value>,
}

#[derive(Debug, Serialize, Deserialize)]
struct UserPreferences {
    theme: String,
    notifications: bool,
    language: String,
}

// Query JSON fields
let users = query_as!(
    UserProfile,
    "SELECT id, user_id, preferences, metadata FROM user_profiles WHERE preferences->>'theme' = $1",
    "dark"
)
.fetch_all(&pool)
.await?;

// Update JSON field
query!(
    "UPDATE user_profiles SET preferences = jsonb_set(preferences, '{theme}', $1) WHERE user_id = $2",
    Json(serde_json::json!("light")),
    user_id
)
.execute(&pool)
.await?;
```

### Array Types
```rust
use sqlx::types::Uuid;

#[derive(Debug, sqlx::FromRow)]
struct Post {
    id: Uuid,
    title: String,
    tags: Vec<String>,  // TEXT[]
}

let posts = query_as!(
    Post,
    "SELECT id, title, tags FROM posts WHERE $1 = ANY(tags)",
    "rust"
)
.fetch_all(&pool)
.await?;

// Insert with array
query!(
    "INSERT INTO posts (title, tags) VALUES ($1, $2)",
    "My Post",
    &vec!["rust".to_string(), "web".to_string()] as &[String]
)
.execute(&pool)
.await?;
```

### Custom Types
```rust
use sqlx::postgres::{PgTypeInfo, PgValueRef};
use sqlx::{Decode, Encode, Postgres, Type};
use std::fmt;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum UserStatus {
    Active,
    Inactive,
    Banned,
}

impl Type<Postgres> for UserStatus {
    fn type_info() -> PgTypeInfo {
        PgTypeInfo::with_name("user_status")
    }
}

impl<'r> Decode<'r, Postgres> for UserStatus {
    fn decode(value: PgValueRef<'r>) -> Result<Self, sqlx::error::BoxDynError> {
        let s = <&str as Decode<Postgres>>::decode(value)?;
        match s {
            "active" => Ok(UserStatus::Active),
            "inactive" => Ok(UserStatus::Inactive),
            "banned" => Ok(UserStatus::Banned),
            _ => Err("invalid user_status".into()),
        }
    }
}

impl Encode<'_, Postgres> for UserStatus {
    fn encode_by_ref(&self, buf: &mut sqlx::postgres::PgArgumentBuffer) -> Result<sqlx::encode::IsNull, sqlx::error::BoxDynError> {
        let s = match self {
            UserStatus::Active => "active",
            UserStatus::Inactive => "inactive",
            UserStatus::Banned => "banned",
        };
        <&str as Encode<Postgres>>::encode_by_ref(&s, buf)
    }
}
```

---

## Connection Pool Tuning

```rust
let pool = PgPool::connect_with(
    sqlx::postgres::PgConnectOptions::new()
        .host("localhost")
        .port(5432)
        .username("user")
        .password("pass")
        .database("mydb")
)
.max_connections(20)           // Max pool size
.min_connections(5)            // Min idle connections
.acquire_timeout(Duration::from_secs(30))  // Wait for connection
.idle_timeout(Duration::from_secs(600))    // Close idle after 10min
.max_lifetime(Duration::from_secs(1800))   // Recycle after 30min
.test_before_acquire(true)     // Validate before use
.build();
```

### Pool Monitoring
```rust
// Health check
async fn health_check(pool: &DbPool) -> Result<(), sqlx::Error> {
    query!("SELECT 1").fetch_one(pool).await?;
    Ok(())
}

// Pool stats
let size = pool.size();
let idle = pool.num_idle();
```

---

## Testing with SQLx

### Test Database per Test
```rust
#[cfg(test)]
mod tests {
    use super::*;
    use sqlx::PgPool;

    async fn setup_test_db() -> PgPool {
        let pool = PgPool::connect(&std::env::var("TEST_DATABASE_URL").unwrap()).await.unwrap();
        
        // Create unique schema per test
        let schema = format!("test_{}", uuid::Uuid::new_v4().simple());
        query(&format!("CREATE SCHEMA {}", schema))
            .execute(&pool)
            .await.unwrap();
        
        // Set search_path
        query(&format!("SET search_path TO {}", schema))
            .execute(&pool)
            .await.unwrap();
        
        // Run migrations
        sqlx::migrate!("./migrations").run(&pool).await.unwrap();
        
        pool
    }

    #[tokio::test]
    async fn test_user_repo() {
        let pool = setup_test_db().await;
        let repo = UserRepo::new(pool.clone());

        let user = repo.create("test@example.com", "Test", "hash").await.unwrap();
        assert_eq!(user.email, "test@example.com");

        let found = repo.find_by_id(user.id).await.unwrap();
        assert_eq!(found.id, user.id);
    }
}
```

### Testcontainers (Integration Tests)
```toml
# Cargo.toml
[dev-dependencies]
testcontainers = { version = "0.16", features = ["postgres"] }
testcontainers-modules = { version = "0.16", features = ["postgres"] }
```

```rust
use testcontainers_modules::postgres::Postgres;
use testcontainers::runners::AsyncRunner;

#[tokio::test]
async fn test_with_real_postgres() {
    let container = Postgres::default().start().await.unwrap();
    let port = container.get_host_port_ipv4(5432).await.unwrap();
    let url = format!("postgres://postgres:postgres@localhost:{}/postgres", port);
    
    let pool = PgPool::connect(&url).await.unwrap();
    sqlx::migrate!("./migrations").run(&pool).await.unwrap();
    
    // Run tests...
}
```

---

## Common Issues

| Issue | Solution |
|-------|----------|
| `sqlx::Error::RowNotFound` | Use `fetch_optional` for optional results |
| Compile-time query fails | Run `cargo sqlx prepare` with DB, or check `sqlx-data.json` |
| Migration checksum mismatch | `sqlx migrate revert` then `sqlx migrate run`, or fix migration file |
| Pool exhausted | Increase `max_connections`, check for connection leaks |
| SSL error | Set `.ssl_mode(PgSslMode::Prefer)` or `Require` |
| Type mismatch | Ensure Rust types match PostgreSQL types (use `sqlx::types` for special types) |

---

## References

- [SQLx GitHub](https://github.com/launchbadge/sqlx)
- [SQLx Docs](https://docs.rs/sqlx/latest/sqlx/)
- [SQLx Migrate](https://github.com/launchbadge/sqlx/tree/main/sqlx-cli)
- [PostgreSQL Types](https://www.postgresql.org/docs/current/datatype.html)