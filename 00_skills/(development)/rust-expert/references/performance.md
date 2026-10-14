# Performance Reference

Updated: 2026-10-10

---

## Profiling

### cargo-flamegraph
```bash
# Install
cargo install flamegraph

# Profile (Linux)
sudo cargo flamegraph --bin my-bin

# Profile with specific args
sudo cargo flamegraph --bin my-bin -- --my-arg value

# Open flamegraph.svg in browser
```

### perf (Linux)
```bash
# Build with debug info
cargo build --release

# Record
perf record -g --call-graph dwarf target/release/my-bin

# Report
perf report

# Or with flamegraph
perf script | flamegraph.pl > perf.svg
```

### pprof (Cross-platform)
```toml
# Cargo.toml
[dependencies]
pprof = { version = "0.12", features = ["flamegraph"] }
```

```rust
// In main
fn main() {
    let guard = pprof::ProfilerGuardBuilder::default()
        .frequency(1000)
        .blocklist(&["libc", "libgcc", "pthread", "vdso"])
        .build()
        .unwrap();

    // ... run your program ...

    if let Ok(report) = guard.report().build() {
        let mut file = std::fs::File::create("flamegraph.svg").unwrap();
        report.flamegraph(&mut file).unwrap();
    }
}
```

```bash
# Run
cargo run --release

# View
open flamegraph.svg
```

### Heap Profiling (dhat)
```bash
# Install
cargo install dhat

# Run with dhat
cargo build --release
valgrind --tool=dhat target/release/my-bin

# View
dh_viewer dhat.out.xxxx
```

---

## Benchmarking (criterion)

### Setup
```toml
# Cargo.toml
[[bench]]
name = "benchmarks"
harness = false

[dev-dependencies]
criterion = "0.5"
```

### Basic Benchmark
```rust
// benches/benchmarks.rs
use criterion::{black_box, criterion_group, criterion_main, Criterion, BenchmarkId};
use my_crate::{process_data, Data};

fn bench_process(c: &mut Criterion) {
    let small = Data::generate(100);
    let large = Data::generate(10000);

    c.bench_function("process_small", |b| {
        b.iter(|| process_data(black_box(&small)))
    });

    c.bench_function("process_large", |b| {
        b.iter(|| process_data(black_box(&large)))
    });

    // Parameterized benchmarks
    let mut group = c.benchmark_group("process_sizes");
    for size in [10, 100, 1000, 10000] {
        let data = Data::generate(size);
        group.bench_with_input(BenchmarkId::from_parameter(size), &data, |b, data| {
            b.iter(|| process_data(black_box(data)))
        });
    }
    group.finish();
}

criterion_group!(benches, bench_process);
criterion_main!(benches);
```

### Running Benchmarks
```bash
# Run all
cargo bench

# Specific benchmark
cargo bench process_small

# Save baseline
cargo bench -- --save-baseline main

# Compare with baseline
cargo bench -- --baseline main

# HTML report
open target/criterion/report/index.html
```

---

## Compiler Optimizations

### Release Profile
```toml
# Cargo.toml
[profile.release]
opt-level = 3           # Maximum optimization
lto = true              # Link-time optimization (thin by default)
lto = "fat"             # Full LTO (slower compile, better runtime)
codegen-units = 1       # Single codegen unit (better optimization)
panic = "abort"         # No unwinding (smaller, faster)
strip = true            # Strip symbols (requires cargo-strip)
debug = false           # No debug info

# For maximum size reduction
[profile.release.size]
opt-level = "z"         # Optimize for size
lto = true
codegen-units = 1
panic = "abort"
strip = true
```

### Profile-Guided Optimization (PGO)
```bash
# 1. Build with instrumentation
rustup component add llvm-tools-preview
cargo install cargo-pgo

# 2. Generate profile data
cargo pgo build --release
# Run workload to generate profile
./target/release/my-bin --workload

# 3. Build with profile
cargo pgo optimize --release
```

---

## Memory Optimization

### Allocator Choice
```toml
# Cargo.toml
# jemalloc (good for multi-threaded)
[dependencies]
jemallocator = { version = "0.5", optional = true }

# mimalloc (good all-rounder)
mimalloc = { version = "0.1", optional = true }

# tikv-jemallocor (jemalloc with better defaults)
tikv-jemallocator = { version = "0.6", optional = true }
```

```rust
// main.rs - use one allocator
#[global_allocator]
static GLOBAL: jemallocator::Jemalloc = jemallocator::Jemalloc;

// Or mimalloc
#[global_allocator]
static GLOBAL: mimalloc::MiMalloc = mimalloc::MiMalloc;
```

### Avoiding Allocations
```rust
// ❌ Allocates new String each call
fn format_name(first: &str, last: &str) -> String {
    format!("{} {}", first, last)
}

// ✅ Reuses buffer
fn format_name<'a>(first: &str, last: &str, buf: &'a mut String) -> &'a str {
    buf.clear();
    buf.push_str(first);
    buf.push(' ');
    buf.push_str(last);
    buf
}

// ✅ Cow for conditional allocation
use std::borrow::Cow;

fn maybe_uppercase(s: &str) -> Cow<'_, str> {
    if s.chars().any(|c| c.is_lowercase()) {
        Cow::Owned(s.to_uppercase())
    } else {
        Cow::Borrowed(s)
    }
}
```

### Zero-Cost Abstractions
```rust
// ✅ Iterators optimize to loops
let sum: i32 = (0..100).filter(|x| x % 2 == 0).sum();

// ✅ Inlining hint
#[inline(always)]
fn hot_path(x: i32) -> i32 {
    x * 2 + 1
}

// ❌ Avoid in hot paths
// - Box<dyn Trait> (dynamic dispatch)
// - RefCell/Rc (runtime borrow checking)
// - String::from in loops
// - format! in hot loops
```

---

## Async Performance

### Avoid Blocking in Async
```rust
// ❌ Blocks executor thread
async fn bad() {
    std::thread::sleep(Duration::from_secs(1));
    let data = std::fs::read_to_string("file.txt")?;
}

// ✅ Use spawn_blocking
async fn good() -> Result<String> {
    tokio::task::spawn_blocking(|| {
        std::thread::sleep(Duration::from_secs(1));
        std::fs::read_to_string("file.txt")
    }).await?
}

// ✅ Use async alternatives
async fn better() -> Result<String> {
    tokio::time::sleep(Duration::from_secs(1)).await;
    tokio::fs::read_to_string("file.txt").await
}
```

### Connection Pooling
```rust
// Reuse connections, don't create per request
let pool = PgPool::connect_with(options)
    .max_connections(20)
    .min_connections(5)
    .build();

// In handler - borrow from pool
let row = sqlx::query("SELECT ...")
    .fetch_one(&pool)  // Borrows connection, returns to pool
    .await?;
```

### Backpressure
```rust
// Bounded channel = backpressure
let (tx, mut rx) = tokio::sync::mpsc::channel::<Request>(1000);

// Sender waits when full
tx.send(request).await?;

// Receiver processes at own pace
while let Some(req) = rx.recv().await {
    process(req).await;
}
```

---

## Binary Size Optimization

```toml
# Cargo.toml
[profile.release]
opt-level = "z"        # Optimize for size
lto = true
codegen-units = 1
panic = "abort"
strip = true
debug = false

# Disable default features
default-run = "my-bin"

# In dependencies
[dependencies]
serde = { version = "1.0", features = ["derive"], default-features = false }
tokio = { version = "1.0", features = ["rt-multi-thread", "macros"], default-features = false }
```

```bash
# Strip after build
cargo install cargo-strip
cargo strip --release

# Check size
ls -lh target/release/my-bin

# Analyze with bloaty
cargo install cargo-bloat
cargo bloat --release -n 20
```

---

## SIMD Optimization

```rust
// Explicit SIMD (requires target_feature)
#[target_feature(enable = "avx2")]
unsafe fn dot_product_avx2(a: &[f32], b: &[f32]) -> f32 {
    // Uses AVX2 instructions
    std::arch::x86_64::_mm256_dp_ps(...)
}

// Portable SIMD (stable)
use std::simd::{f32x8, SimdFloat};

fn dot_product_simd(a: &[f32], b: &[f32]) -> f32 {
    let mut sum = f32x8::splat(0.0);
    for (a_chunk, b_chunk) in a.chunks(8).zip(b.chunks(8)) {
        let a_vec = f32x8::from_slice(a_chunk);
        let b_vec = f32x8::from_slice(b_chunk);
        sum += a_vec * b_vec;
    }
    sum.reduce_sum()
}

// Enable in Cargo.toml
[profile.release]
# RUSTFLAGS="-C target-cpu=native" cargo build --release
```

---

## Database Performance

### Query Optimization
```rust
// ✅ Select only needed columns
query!("SELECT id, email FROM users WHERE active = $1", true)

// ❌ Selects all columns
query!("SELECT * FROM users WHERE active = $1", true)

// ✅ Use indexes (check with EXPLAIN ANALYZE)
query!("SELECT * FROM users WHERE email = $1", email)  // Needs index on email

// ✅ Batch inserts
query!(
    "INSERT INTO users (email, name) VALUES $1",
    &vec![("a@b.com", "A"), ("c@d.com", "C")] as &[(&str, &str)]
)

// ✅ Prepared statements (sqlx does this automatically with query!)
// ❌ Avoid N+1 queries
for user in users {
    let posts = get_posts(user.id).await?;  // N queries!
}
// ✅ Use JOIN or batch
let posts = get_posts_for_users(&user_ids).await?;  // 1 query
```

### Connection Pool Sizing
```rust
// Rule of thumb: pool_size = CPU_cores * 2 + effective_spindle_count
// For SSD: pool_size = CPU_cores * 4
// For async: smaller pools (connections yield on await)

let pool = PgPool::connect_with(options)
    .max_connections(num_cpus::get() * 4)
    .min_connections(num_cpus::get())
    .build();
```

---

## Common Performance Anti-Patterns

| Anti-Pattern | Impact | Fix |
|--------------|--------|-----|
| `String::from` in loop | Allocations | Reuse `String` with `clear()` |
| `format!` in hot path | Allocations | Use `write!` to buffer |
| `Vec::new()` + `push` in loop | Reallocations | `Vec::with_capacity(n)` |
| `Box<dyn Trait>` in hot path | Dynamic dispatch | Use generics/enums |
| `clone()` on large data | Memory copy | Use `Arc`/references |
| `collect()` to Vec then iterate | Double allocation | Use iterators directly |
| `Mutex` in async (std) | Blocks thread | Use `tokio::sync::Mutex` |
| Unbounded channels | OOM | Use bounded channels |

---

## Measuring Performance

### Timing
```rust
use std::time::Instant;

let start = Instant::now();
// ... operation ...
let elapsed = start.elapsed();
println!("Took: {:?}", elapsed);
```

### Throughput
```rust
let start = Instant::now();
for _ in 0..10000 {
    process_item().await;
}
let elapsed = start.elapsed();
let throughput = 10000.0 / elapsed.as_secs_f64();
println!("Throughput: {:.0} ops/sec", throughput);
```

### Custom Metrics
```rust
use metrics::histogram;

let start = Instant::now();
let result = process().await;
histogram!("process_duration_seconds").record(start.elapsed().as_secs_f64());
```

---

## References

- [Rust Performance Book](https://nnethercote.github.io/perf-book/)
- [criterion](https://docs.rs/criterion/latest/criterion/)
- [flamegraph](https://github.com/flamegraph-rs/flamegraph)
- [pprof-rs](https://github.com/tokio-rs/pprof)
- [Portable SIMD](https://doc.rust-lang.org/std/simd/)