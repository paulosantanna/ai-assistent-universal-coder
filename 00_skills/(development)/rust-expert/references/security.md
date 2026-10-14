# Security Reference

Updated: 2026-10-10

---

## Dependency Auditing

### cargo-audit
```bash
# Install
cargo install cargo-audit

# Run audit
cargo audit

# JSON output
cargo audit --json

# Ignore specific advisories (use sparingly)
cargo audit --ignore RUSTSEC-2024-XXXX

# In CI
cargo audit --deny warnings
```

### cargo-deny
```toml
# Cargo.toml
[dev-dependencies]
cargo-deny = "0.14"
```

```bash
# Generate config
cargo deny init
```

```toml
# deny.toml
[advisories]
# Vulnerability database
db = "https://github.com/RustSec/advisory-db"
# Ignore specific advisories with justification
ignore = [
    # { id = "RUSTSEC-2024-XXXX", reason = "transitive, no upgrade path" }
]

[licenses]
# Allow/deny licenses
allow = ["MIT", "Apache-2.0", "BSD-3-Clause", "ISC"]
deny = ["GPL-3.0", "AGPL-3.0"]
# Exceptions
exceptions = [
    # { name = "problematic-crate", allow = "GPL-3.0" }
]

[bans]
# Ban specific crates/versions
multiple-versions = "warn"
wildcards = "deny"
deny = [
    # { name = "old-crate", version = "< 1.0" }
]

[sources]
# Allowed registries
allow-registry = ["https://github.com/rust-lang/crates.io-index"]
# Unknown registries
unknown-registries = "deny"

[advisories.vulnerability]
# Severity threshold
severity = "medium"
```

```bash
# Run checks
cargo deny check
cargo deny check advisories
cargo deny check licenses
cargo deny check bans
cargo deny check sources
```

---

## Supply Chain Security

### Verifying Dependencies
```bash
# Check for typosquatting
cargo install cargo-supply-chain
cargo supply-chain check

# Verify checksums
cargo verify-project

# Lockfile integrity
cargo generate-lockfile
# Commit Cargo.lock!
```

### Private Registries
```toml
# .cargo/config.toml
[registries]
my-private = { index = "sparse+https://my-registry.example.com/index/" }

[source.crates-io]
replace-with = "my-private"
```

### Sigstore/Cosign (Experimental)
```bash
# Sign artifacts
cargo install cargo-sigstore
cargo sigstore sign --registry crates-io my-crate 1.0.0

# Verify
cargo sigstore verify --registry crates-io my-crate 1.0.0
```

---

## Unsafe Code Audit

### Finding Unsafe
```bash
# Find all unsafe blocks
cargo install cargo-geiger
cargo geiger

# Or use clippy
cargo clippy -- -W clippy::unwrap_used -W clippy::expect_used
```

### Unsafe Guidelines
```rust
// ✅ Document safety requirements
/// # Safety
/// Caller must ensure `ptr` is valid and aligned for `T`
unsafe fn read_ptr<T>(ptr: *const T) -> T {
    ptr.read()
}

// ✅ Encapsulate unsafe in safe API
pub fn get_element(vec: &Vec<i32>, index: usize) -> Option<&i32> {
    if index < vec.len() {
        // SAFETY: index checked above
        Some(unsafe { vec.get_unchecked(index) })
    } else {
        None
    }
}

// ✅ Use safe abstractions when possible
// Instead of manual pointer arithmetic:
let slice = &vec[start..end];

// ✅ FFI boundaries
#[no_mangle]
pub extern "C" fn c_api(input: *const c_char) -> c_int {
    // Validate input
    if input.is_null() {
        return -1;
    }
    // Convert safely
    let c_str = unsafe { CStr::from_ptr(input) };
    // ...
    0
}
```

### Miri (Undefined Behavior Detection)
```bash
# Install
rustup component add miri
cargo miri setup

# Run tests under Miri
cargo miri test

# With specific features
cargo miri test --features "std"
```

---

## Fuzzing

### cargo-fuzz
```bash
# Install
cargo install cargo-fuzz

# Initialize
cargo fuzz init

# Add target
# fuzz/fuzz_target_1.rs
#![no_main]
use libfuzzer_sys::fuzz_target;
use my_crate::parse;

fuzz_target!(|data: &[u8]| {
    if let Ok(s) = std::str::from_utf8(data) {
        let _ = parse(s);
    }
});
```

```bash
# Run
cargo fuzz run fuzz_target_1

# With corpus
cargo fuzz run fuzz_target_1 corpus/

# Minimize corpus
cargo fuzz cmin fuzz_target_1 corpus/ minimized/

# Triage crash
cargo fuzz tmin fuzz_target_1 crash-file
```

### libFuzzer Options
```bash
# Run with options
cargo fuzz run fuzz_target_1 -- -max_len=10000 -runs=1000000

# Parallel
cargo fuzz run fuzz_target_1 -- -workers=4

# Dictionary
cargo fuzz run fuzz_target_1 -- -dict=dictionary.txt
```

---

## Secure Coding Practices

### Input Validation
```rust
use validator::Validate;

#[derive(Validate, Deserialize)]
struct CreateUser {
    #[validate(email)]
    email: String,
    
    #[validate(length(min = 1, max = 100))]
    name: String,
    
    #[validate(length(min = 8))]
    password: String,
}

async fn create_user(Json(payload): Json<CreateUser>) -> Result<Json<User>, AppError> {
    payload.validate()?;
    // ...
}
```

### SQL Injection Prevention
```rust
// ✅ Parameterized queries (sqlx)
query!("SELECT * FROM users WHERE email = $1", email)

// ✅ Parameterized with sqlx::query
query("SELECT * FROM users WHERE email = $1")
    .bind(email)
    .fetch_all(&pool)

// ❌ String interpolation (VULNERABLE)
// query(&format!("SELECT * FROM users WHERE email = '{}'", email))
```

### Secrets Management
```rust
// ❌ Never hardcode secrets
// const API_KEY: &str = "sk-...";

// ✅ Environment variables
let api_key = std::env::var("API_KEY")
    .context("API_KEY not set")?;

// ✅ Secret manager (AWS Secrets Manager, Vault, etc.)
use aws_sdk_secretsmanager::Client;

async fn get_secret(client: &Client, name: &str) -> Result<String> {
    let resp = client.get_secret_value()
        .secret_id(name)
        .send()
        .await?;
    resp.secret_string().ok_or_eyre("no secret string")
}
```

### Cryptography
```toml
# Cargo.toml
# Use well-maintained crates
ring = "0.17"           # Low-level crypto
rustls = "0.23"         # TLS
argon2 = "0.5"          # Password hashing
aes-gcm = "0.10"        # AEAD encryption
x25519-dalek = "2.0"    # Key exchange
ed25519-dalek = "2.0"   # Signatures
```

```rust
// Password hashing
use argon2::{Argon2, PasswordHasher, PasswordVerifier};
use argon2::password_hash::{SaltString, rand_core::OsRng};

fn hash_password(password: &str) -> String {
    let salt = SaltString::generate(&mut OsRng);
    Argon2::default()
        .hash_password(password.as_bytes(), &salt)
        .unwrap()
        .to_string()
}

fn verify_password(password: &str, hash: &str) -> bool {
    let parsed = argon2::PasswordHash::new(hash).unwrap();
    Argon2::default()
        .verify_password(password.as_bytes(), &parsed)
        .is_ok()
}

// Encryption
use aes_gcm::{Aes256Gcm, Key, Nonce, aead::Aead};
use rand::RngCore;

fn encrypt(data: &[u8], key: &[u8; 32]) -> Vec<u8> {
    let cipher = Aes256Gcm::new(Key::from_slice(key));
    let mut nonce = [0u8; 12];
    rand::thread_rng().fill_bytes(&mut nonce);
    let mut ciphertext = cipher.encrypt(Nonce::from_slice(&nonce), data).unwrap();
    // Prepend nonce for decryption
    let mut result = nonce.to_vec();
    result.append(&mut ciphertext);
    result
}
```

### HTTP Security Headers
```rust
use axum::response::Response;
use axum::middleware::{self, Next};
use axum::extract::Request;

async fn security_headers(req: Request, next: Next) -> Response {
    let mut response = next.run(req).await;
    
    let headers = response.headers_mut();
    headers.insert("X-Content-Type-Options", "nosniff".parse().unwrap());
    headers.insert("X-Frame-Options", "DENY".parse().unwrap());
    headers.insert("X-XSS-Protection", "1; mode=block".parse().unwrap());
    headers.insert("Referrer-Policy", "strict-origin-when-cross-origin".parse().unwrap());
    headers.insert(
        "Content-Security-Policy",
        "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'".parse().unwrap()
    );
    headers.insert(
        "Permissions-Policy",
        "geolocation=(), microphone=(), camera=()".parse().unwrap()
    );
    
    response
}
```

### Rate Limiting
```rust
use axum::extract::State;
use std::sync::Arc;
use tokio::sync::Mutex;
use std::collections::HashMap;
use std::time::Instant;

struct RateLimiter {
    requests: Mutex<HashMap<String, Vec<Instant>>>,
    max_requests: usize,
    window: Duration,
}

impl RateLimiter {
    async fn check(&self, key: &str) -> bool {
        let mut map = self.requests.lock().await;
        let now = Instant::now();
        let window_start = now - self.window;
        
        let entries = map.entry(key.to_string()).or_default();
        entries.retain(|&t| t > window_start);
        
        if entries.len() >= self.max_requests {
            false
        } else {
            entries.push(now);
            true
        }
    }
}

async fn rate_limit_middleware(
    State(limiter): State<Arc<RateLimiter>>,
    req: Request,
    next: Next,
) -> Result<Response, StatusCode> {
    let ip = req.headers()
        .get("x-forwarded-for")
        .or_else(|| req.headers().get("x-real-ip"))
        .and_then(|h| h.to_str().ok())
        .unwrap_or("unknown");
    
    if !limiter.check(ip).await {
        return Err(StatusCode::TOO_MANY_REQUESTS);
    }
    
    Ok(next.run(req).await)
}
```

---

## TLS Configuration

### rustls Server
```rust
use rustls::{ServerConfig, Certificate, PrivateKey};
use rustls_pemfile::{certs, pkcs8_private_keys};
use std::fs::File;
use std::io::BufReader;

fn load_tls_config(cert_path: &str, key_path: &str) -> ServerConfig {
    let cert_file = File::open(cert_path).unwrap();
    let mut cert_reader = BufReader::new(cert_file);
    let cert_chain = certs(&mut cert_reader).unwrap()
        .into_iter()
        .map(Certificate)
        .collect();

    let key_file = File::open(key_path).unwrap();
    let mut key_reader = BufReader::new(key_file);
    let mut keys = pkcs8_private_keys(&mut key_reader).unwrap();
    let private_key = PrivateKey(keys.remove(0));

    ServerConfig::builder()
        .with_safe_defaults()
        .with_no_client_auth()
        .with_single_cert(cert_chain, private_key)
        .unwrap()
}
```

### Client TLS
```rust
use rustls::{ClientConfig, RootCertStore};
use rustls_pemfile::certs;
use std::fs::File;
use std::io::BufReader;

fn load_client_tls(ca_path: &str) -> ClientConfig {
    let ca_file = File::open(ca_path).unwrap();
    let mut ca_reader = BufReader::new(ca_file);
    let ca_certs = certs(&mut ca_reader).unwrap();

    let mut root_store = RootCertStore::empty();
    for cert in ca_certs {
        root_store.add(&Certificate(cert)).unwrap();
    }

    ClientConfig::builder()
        .with_safe_defaults()
        .with_root_certificates(root_store)
        .with_no_client_auth()
}
```

---

## Security Checklist

### Pre-Release
- [ ] `cargo audit` passes
- [ ] `cargo deny check` passes
- [ ] No `unwrap()`/`expect()` in production paths
- [ ] All `unsafe` blocks documented and reviewed
- [ ] `cargo miri test` passes
- [ ] Fuzzing run on parsers/decoders
- [ ] Dependencies pinned in `Cargo.lock`
- [ ] `Cargo.lock` committed
- [ ] Secrets not in code (use env vars/secret manager)
- [ ] TLS configured correctly
- [ ] Security headers on HTTP responses
- [ ] Rate limiting on public endpoints
- [ ] Input validation on all user data
- [ ] SQL queries parameterized
- [ ] Error messages don't leak internals
- [ ] Logging doesn't include secrets

### Runtime
- [ ] Monitor `cargo audit` advisories
- [ ] Update dependencies regularly
- [ ] Rotate secrets periodically
- [ ] Review access logs for anomalies
- [ ] Alert on high error rates

---

## References

- [RustSec Advisory DB](https://github.com/RustSec/advisory-db)
- [cargo-audit](https://github.com/RustSec/cargo-audit)
- [cargo-deny](https://github.com/EmbarkStudios/cargo-deny)
- [cargo-geiger](https://github.com/rust-secure-code/cargo-geiger)
- [Miri](https://github.com/rust-lang/miri)
- [cargo-fuzz](https://github.com/rust-fuzz/cargo-fuzz)
- [OWASP Rust](https://github.com/OWASP/www-project-rust-security)
- [Rust TLS](https://github.com/rustls/rustls)