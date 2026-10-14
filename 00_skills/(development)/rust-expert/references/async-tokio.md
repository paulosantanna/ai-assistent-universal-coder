# Async & Tokio Reference

Updated: 2026-10-10

---

## Tokio Runtime Setup

### Basic Runtime
```rust
// Single-threaded (lightweight)
#[tokio::main(flavor = "current_thread")]
async fn main() {
    // ...
}

// Multi-threaded (default, for CPU-bound work)
#[tokio::main]
async fn main() {
    // ...
}

// Manual runtime (for libraries, tests, custom config)
fn main() {
    let rt = tokio::runtime::Builder::new_multi_thread()
        .worker_threads(4)
        .thread_name("my-worker")
        .enable_all()
        .build()
        .unwrap();
    rt.block_on(async {
        // ...
    });
}
```

### Runtime Configuration
```rust
tokio::runtime::Builder::new_multi_thread()
    .worker_threads(num_cpus::get())  // Default: CPU cores
    .max_blocking_threads(512)        // For spawn_blocking
    .thread_stack_size(2 * 1024 * 1024)  // 2MB stacks
    .thread_name("my-app-worker")
    .enable_io()                       // Enable I/O driver
    .enable_time()                     // Enable time driver
    .build()
```

---

## Spawning Tasks

### `tokio::spawn` — Fire-and-Forget
```rust
// Returns JoinHandle<T> for await/abort
let handle: tokio::task::JoinHandle<Result<(), MyError>> = tokio::spawn(async move {
    do_work().await
});

// Await result (propagates panic)
let result = handle.await?;

// Abort if needed
handle.abort();
```

### `tokio::task::spawn_blocking` — Blocking Operations
```rust
// For CPU-heavy or blocking syscalls
let result = tokio::task::spawn_blocking(|| {
    heavy_computation()
}).await?;

// Dedicated blocking thread pool (max_blocking_threads)
```

### `tokio::task::spawn_local` — !Send Futures
```rust
// Single-threaded runtime only
// For futures containing Rc, RefCell, *const T
let handle = tokio::task::spawn_local(async {
    // !Send future
});
```

---

## Concurrency Primitives

### `tokio::join!` — Join Multiple Futures
```rust
// Runs concurrently, waits for all
let (a, b, c) = tokio::join!(
    fetch_user(),
    fetch_posts(),
    fetch_comments()
);

// All must complete; first error doesn't cancel others
```

### `tokio::select!` — Race Futures
```rust
// Returns when FIRST future completes
tokio::select! {
    msg = rx.recv() => {
        // Handle message
    }
    _ = shutdown_signal() => {
        // Graceful shutdown
        break;
    }
    _ = timeout => {
        // Timeout handling
    }
}

// Pattern: cancellation token
let (tx, rx) = tokio::sync::oneshot::channel();
tokio::select! {
    result = do_work() => { /* ... */ }
    _ = rx => { /* cancelled */ }
}
// Drop tx to cancel
```

### `futures::future::join_all` — Dynamic List
```rust
use futures::future::join_all;

let futures: Vec<_> = items.iter().map(|item| process(item)).collect();
let results = join_all(futures).await;
```

### `tokio::task::JoinSet` — Managed Task Group
```rust
use tokio::task::JoinSet;

let mut set = JoinSet::new();
for item in items {
    set.spawn(async move { process(item).await });
}

while let Some(result) = set.join_next().await {
    match result {
        Ok(Ok(value)) => { /* ... */ }
        Ok(Err(e)) => { /* task error */ }
        Err(e) => { /* panic/join error */ }
    }
}

// Abort all on drop
```

---

## Synchronization

### Channels

```rust
// MPSC (Multi-Producer, Single-Consumer)
let (tx, mut rx) = tokio::sync::mpsc::channel(100);

// Bounded: blocks when full (backpressure)
// Unbounded: tokio::sync::mpsc::unbounded_channel()

// Oneshot (single send, single recv)
let (tx, rx) = tokio::sync::oneshot::channel();

// Broadcast (multi-producer, multi-consumer)
let (tx, rx) = tokio::sync::broadcast::channel(16);
let rx2 = tx.subscribe();
```

### Mutex & RwLock
```rust
use tokio::sync::{Mutex, RwLock};

// Async-aware: yields instead of blocking thread
let mutex = Mutex::new(0);
let mut guard = mutex.lock().await;
*guard += 1;

// RwLock: multiple readers, single writer
let rwlock = RwLock::new(vec![]);
let read_guard = rwlock.read().await;
let write_guard = rwlock.write().await;
```

### Semaphore & Permit
```rust
use tokio::sync::Semaphore;

let semaphore = Semaphore::new(10);  // Max 10 concurrent
let permit = semaphore.acquire().await?;
// permit dropped -> releases slot

// Acquire multiple
let permits = semaphore.acquire_many(3).await?;
```

### Barrier
```rust
use tokio::sync::Barrier;

let barrier = Barrier::new(3);
let handles: Vec<_> = (0..3).map(|_| {
    let b = barrier.clone();
    tokio::spawn(async move {
        do_work().await;
        b.wait().await;  // All 3 meet here
    })
}).collect();
```

### Watch Channel (Configuration/State)
```rust
use tokio::sync::watch;

let (tx, mut rx) = watch::channel(initial_config);
tokio::spawn(async move {
    while rx.changed().await.is_ok() {
        let config = rx.borrow().clone();
        // React to config change
    }
});

// Update
tx.send(new_config)?;
```

---

## Cancellation Safety

### What Is Cancellation Safety?
A future is **cancellation safe** if dropping it mid-execution leaves no side effects (no partial writes, no locks held, no inconsistent state).

### Cancellation-Safe Patterns
```rust
// ✅ Reading from channel
let msg = rx.recv().await;

// ✅ Waiting for notification
notified.await;

// ✅ Timeout
tokio::time::sleep(duration).await;

// ✅ join! / select! (if all branches are safe)
tokio::select! {
    _ = rx.recv() => {},
    _ = shutdown => {},
}
```

### NOT Cancellation-Safe
```rust
// ❌ Writing to socket (partial write possible)
stream.write_all(&buf).await;

// ❌ Mutex lock (lock held across await)
let mut guard = mutex.lock().await;
do_io().await;  // If cancelled, lock held!

// ❌ File write (partial file)
tokio::fs::write(&path, data).await;

// ❌ Transaction commit (partial commit)
tx.commit().await;
```

### Making Operations Cancellation-Safe
```rust
// Use scoped tasks or cleanup on drop
struct Guard<F: FnOnce()> {
    f: Option<F>,
}
impl<F: FnOnce()> Drop for Guard<F> {
    fn drop(&mut self) {
        if let Some(f) = self.f.take() { f(); }
    }
}

async fn safe_write(path: &Path, data: &[u8]) -> Result<()> {
    let temp = path.with_extension("tmp");
    tokio::fs::write(&temp, data).await?;
    tokio::fs::rename(temp, path).await?;
    Ok(())
}

// Or use tokio::select! with cleanup branch
tokio::select! {
    result = do_work() => result,
    _ = shutdown => {
        cleanup().await;
        Err(Cancelled)
    }
}
```

### CancellationToken Pattern
```rust
use tokio_util::sync::CancellationToken;

let token = CancellationToken::new();
let child_token = token.child_token();

tokio::spawn(async move {
    tokio::select! {
        _ = do_work() => {},
        _ = child_token.cancelled() => {
            cleanup().await;
        }
    }
});

// Signal cancellation
token.cancel();
```

---

## Backpressure

### Channel Backpressure
```rust
// Bounded channel = natural backpressure
let (tx, mut rx) = tokio::sync::mpsc::channel(100);

// send() waits when full (async)
tx.send(item).await?;

// try_send() returns error if full
tx.try_send(item)?;  // Err(TrySendError::Full(item))

// Reserve permit for batching
let permit = tx.reserve().await?;
permit.send(item);
```

### Stream Backpressure
```rust
use tokio_stream::{StreamExt, wrappers::ReceiverStream};

let stream = ReceiverStream::new(rx);
stream
    .for_each_concurrent(10, |item| process(item))  // Max 10 concurrent
    .await;
```

### TCP Backpressure
```rust
use tokio::net::TcpStream;
use tokio::io::{AsyncReadExt, AsyncWriteExt};

let mut stream = TcpStream::connect("...").await?;
// TCP flow control handles backpressure automatically
// But: don't buffer unbounded in application!
```

---

## Graceful Shutdown

### Signal Handling
```rust
use tokio::signal;

async fn shutdown_signal() {
    let ctrl_c = async {
        signal::ctrl_c().await.expect("failed to install Ctrl+C handler");
    };

    #[cfg(unix)]
    let terminate = async {
        signal::unix::signal(signal::unix::SignalKind::terminate())
            .expect("failed to install signal handler")
            .recv()
            .await;
    };

    #[cfg(not(unix))]
    let terminate = std::future::pending::<()>();

    tokio::select! {
        _ = ctrl_c => {},
        _ = terminate => {},
    }
}
```

### Graceful Shutdown Pattern
```rust
use tokio::sync::mpsc;
use tokio_util::sync::CancellationToken;

async fn run_server(shutdown: CancellationToken) {
    let (tx, mut rx) = mpsc::channel(1);

    // Spawn server
    let server = tokio::spawn(async move {
        // ... server loop
        tokio::select! {
            _ = shutdown.cancelled() => {
                // Stop accepting new connections
                // Wait for in-flight requests
                drain_connections().await;
            }
        }
    });

    // Wait for shutdown signal
    shutdown_signal().await;
    shutdown.cancel();

    // Wait for server to finish
    server.await?;
}
```

### `graceful_shutdown` Crate
```toml
# Cargo.toml
graceful_shutdown = "0.2"
```
```rust
use graceful_shutdown::{GracefulShutdown, SubsystemHandle};

let mut gs = GracefulShutdown::new();

gs.spawn_subsystem("http-server", |handle: SubsystemHandle| async move {
    let server = axum::Server::bind(&addr).serve(app.into_make_service());
    tokio::select! {
        _ = handle.on_shutdown_requested() => {
            server.graceful_shutdown(Some(Duration::from_secs(30))).await;
        }
        result = server => result?,
    }
});

gs.shutdown().await;
```

---

## Time & Timers

```rust
use tokio::time::{sleep, timeout, interval, Instant, Duration};

// Sleep
sleep(Duration::from_secs(1)).await;

// Timeout (cancellation-safe)
let result = timeout(Duration::from_secs(5), do_work()).await?;

// Interval (for periodic tasks)
let mut interval = interval(Duration::from_secs(10));
while let Some(_) = interval.tick().await {
    do_periodic_work().await;
}

// Instant (monotonic)
let start = Instant::now();
// ...
let elapsed = start.elapsed();
```

---

## Async I/O Traits

```rust
use tokio::io::{AsyncRead, AsyncWrite, AsyncReadExt, AsyncWriteExt};

// Implement for custom types
impl AsyncRead for MyType {
    fn poll_read(
        self: Pin<&mut Self>,
        cx: &mut Context<'_>,
        buf: &mut ReadBuf<'_>,
    ) -> Poll<io::Result<()>> {
        // ...
    }
}

impl AsyncWrite for MyType {
    fn poll_write(
        self: Pin<&mut Self>,
        cx: &mut Context<'_>,
        buf: &[u8],
    ) -> Poll<io::Result<usize>> {
        // ...
    }
    fn poll_flush(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<io::Result<()>> { ... }
    fn poll_shutdown(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<io::Result<()>> { ... }
}
```

---

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| `.await` in loop without yield | Starves other tasks | Add `tokio::task::yield_now().await` |
| Holding lock across `.await` | Deadlock, cancellation unsafe | Restructure: lock → copy → drop → await |
| `spawn_blocking` for async I/O | Wastes blocking threads | Use native async I/O instead |
| Unbounded channels | OOM under load | Always use bounded channels |
| Missing `Send` bound | Compile error in `spawn` | Use `Arc<Mutex<_>>` not `Rc<RefCell<_>>` |
| Forgetting `JoinHandle` | Task dropped silently | Always `.await` or `.abort()` handles |
| `select!` without cancellation | Tasks leak on early return | Use `CancellationToken` or `select!` with cleanup |

---

## Testing Async Code

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
        // Multi-threaded test runtime
    }

    #[tokio::test]
    async fn test_with_time() {
        // Use tokio::time::pause() for deterministic time
        tokio::time::pause();
        // ...
        tokio::time::advance(Duration::from_secs(1)).await;
    }
}
```

---

## References

- [Tokio Tutorial](https://tokio.rs/tokio/tutorial)
- [Tokio API Docs](https://docs.rs/tokio/latest/tokio/)
- [Async Rust Book](https://rust-lang.github.io/async-book/)
- [Cancellation Safety](https://doc.rust-lang.org/async-book/cancellation-safety.html)
- [Tokio Select](https://docs.rs/tokio/latest/tokio/macro.select.html)