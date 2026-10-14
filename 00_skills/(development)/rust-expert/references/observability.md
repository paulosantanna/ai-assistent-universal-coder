# Observability Reference

Updated: 2026-10-10

---

## Tracing Setup

### Basic Subscriber
```rust
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt, EnvFilter};

fn init_tracing() {
    tracing_subscriber::registry()
        .with(EnvFilter::from_default_env())  // RUST_LOG=info,my_crate=debug
        .with(tracing_subscriber::fmt::layer()
            .with_target(true)
            .with_thread_ids(true)
            .with_file(true)
            .with_line_number(true)
            .json()  // JSON output for log aggregation
        )
        .init();
}
```

### Production Subscriber
```rust
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt, EnvFilter, fmt, Layer};

fn init_tracing() {
    let fmt_layer = fmt::layer()
        .json()
        .with_current_span(true)
        .with_span_list(true)
        .with_target(true)
        .with_filter(EnvFilter::from_default_env());

    let otel_layer = tracing_opentelemetry::layer()
        .with_tracer(opentelemetry_sdk::trace::TracerProvider::default().tracer("my-service"))
        .with_filter(EnvFilter::new("info"));

    tracing_subscriber::registry()
        .with(fmt_layer)
        .with(otel_layer)
        .init();
}
```

---

## Structured Logging

### Event Logging
```rust
use tracing::{info, warn, error, debug, trace, instrument};

#[instrument(skip(password), fields(user_id = %user.id))]
async fn login(user: &User, password: &str) -> Result<Session, AuthError> {
    info!("login attempt");
    
    let valid = verify_password(password, &user.password_hash).await?;
    if !valid {
        warn!(reason = "invalid_password", "login failed");
        return Err(AuthError::InvalidCredentials);
    }
    
    let session = create_session(user).await?;
    info!(session_id = %session.id, "login successful");
    Ok(session)
}
```

### Span Attributes
```rust
use tracing::{info_span, Instrument};

async fn process_order(order: Order) -> Result<()> {
    let span = info_span!("process_order", 
        order_id = %order.id,
        customer_id = %order.customer_id,
        total = %order.total,
    );

    async move {
        // All logs in this block inherit span context
        info!("validating order");
        validate(&order).await?;
        
        info!("charging payment");
        charge_payment(&order).await?;
        
        info!("fulfilling order");
        fulfill(&order).await?;
        
        Ok(())
    }.instrument(span).await
}
```

---

## Metrics (Prometheus)

### Setup
```toml
# Cargo.toml
metrics = "0.22"
metrics-exporter-prometheus = "0.15"
```

### Basic Metrics
```rust
use metrics::{counter, gauge, histogram, Unit};

fn record_metrics() {
    // Counter (monotonically increasing)
    counter!("http_requests_total", "method" => "GET", "status" => "200").increment(1);
    
    // Gauge (can go up/down)
    gauge!("active_connections", 42);
    
    // Histogram (for latencies, sizes)
    histogram!("http_request_duration_seconds", 0.123)
        .record(Unit::Seconds);
}

// Macro for common HTTP metrics
macro_rules! record_http_metrics {
    ($method:expr, $status:expr, $duration:expr) => {
        counter!("http_requests_total", 
            "method" => $method, 
            "status" => $status
        ).increment(1);
        
        histogram!("http_request_duration_seconds", $duration.as_secs_f64())
            .record(metrics::Unit::Seconds);
    };
}
```

### Prometheus Exporter
```rust
use metrics_exporter_prometheus::{PrometheusBuilder, PrometheusHandle};

fn init_metrics() -> PrometheusHandle {
    let builder = PrometheusBuilder::new()
        .set_buckets_for_metric(
            metrics::Matcher::Full("http_request_duration_seconds".into()),
            &[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
        ).unwrap()
        .install()
        .unwrap();
    
    builder.handle()
}

// In Axum
async fn metrics_handler(State(handle): State<PrometheusHandle>) -> String {
    handle.render()
}

let app = Router::new()
    .route("/metrics", get(metrics_handler))
    .with_state(init_metrics());
```

---

## OpenTelemetry Integration

### Cargo.toml
```toml
[dependencies]
opentelemetry = { version = "0.27", features = ["trace"] }
opentelemetry-sdk = { version = "0.27", features = ["trace", "metrics"] }
tracing-opentelemetry = { version = "0.27", features = ["trace"] }
opentelemetry-otlp = { version = "0.27", features = ["tonic", "trace", "metrics"] }
```

### Tracer Setup
```rust
use opentelemetry::{global, KeyValue};
use opentelemetry_sdk::trace::{self, Sampler};
use opentelemetry_otlp::WithExportConfig;

fn init_tracer() -> opentelemetry_sdk::trace::Tracer {
    let exporter = opentelemetry_otlp::new_exporter()
        .tonic()
        .with_endpoint("http://localhost:4317");

    let provider = opentelemetry_sdk::trace::TracerProvider::builder()
        .with_sampler(Sampler::ParentBased(Box::new(Sampler::TraceIdRatioBased(0.1))))
        .with_batch_exporter(exporter)
        .with_resource(
            opentelemetry_sdk::Resource::new(vec![
                KeyValue::new("service.name", "my-service"),
                KeyValue::new("service.version", env!("CARGO_PKG_VERSION")),
                KeyValue::new("deployment.environment", "production"),
            ])
        )
        .build();

    global::set_tracer_provider(provider.clone());
    provider.tracer("my-service")
}
```

### Span Creation
```rust
use opentelemetry::{trace::Tracer, Context, KeyValue};
use tracing_opentelemetry::OpenTelemetrySpanExt;

fn traced_operation() {
    let tracer = global::tracer("my-service");
    let span = tracer.start("my_operation");
    let cx = Context::current_with_span(span);
    
    // Do work...
    
    cx.span().end();
}

// Or with tracing
#[instrument]
async fn traced_async() {
    // Automatically creates OTel span
}
```

---

## Health Checks

### Basic Health Endpoint
```rust
use axum::{Router, routing::get, response::Json};
use serde_json::json;

async fn health() -> Json<serde_json::Value> {
    Json(json!({
        "status": "healthy",
        "version": env!("CARGO_PKG_VERSION"),
        "uptime_seconds": uptime(),
    }))
}

async fn readiness(State(pool): State<DbPool>) -> Result<Json<serde_json::Value>, StatusCode> {
    // Check dependencies
    sqlx::query("SELECT 1").fetch_one(&pool).await
        .map_err(|_| StatusCode::SERVICE_UNAVAILABLE)?;
    
    Ok(Json(json!({"status": "ready"})))
}

let app = Router::new()
    .route("/health", get(health))
    .route("/ready", get(readiness));
```

### Kubernetes Probes
```yaml
# k8s deployment
livenessProbe:
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 10
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: 3000
  initialDelaySeconds: 5
  periodSeconds: 5
```

---

## Distributed Tracing Context Propagation

### HTTP Headers
```rust
use opentelemetry::global;
use opentelemetry_http::HeaderInjector;

fn inject_context(req: &mut http::Request<()>) {
    global::get_text_map_propagator(|propagator| {
        propagator.inject_context(&tracing::Span::current().context(), &mut HeaderInjector(req.headers_mut()))
    });
}

fn extract_context(headers: &http::HeaderMap) -> opentelemetry::Context {
    global::get_text_map_propagator(|propagator| {
        propagator.extract(&HeaderExtractor(headers))
    })
}
```

---

## Log Correlation

### Request ID Middleware
```rust
use axum::middleware::{self, Next};
use axum::extract::Request;
use axum::response::Response;
use uuid::Uuid;

async fn request_id_middleware(mut req: Request, next: Next) -> Response {
    let request_id = req.headers()
        .get("x-request-id")
        .and_then(|h| h.to_str().ok())
        .map(|s| s.to_string())
        .unwrap_or_else(|| Uuid::new_v4().to_string());

    // Add to extensions for handlers
    req.extensions_mut().insert(RequestId(request_id.clone()));

    let mut response = next.run(req).await;
    response.headers_mut().insert("x-request-id", request_id.parse().unwrap());
    response
}

struct RequestId(String);

// In handlers
async fn handler(Extension(request_id): Extension<RequestId>) {
    tracing::info!(request_id = %request_id.0, "processing request");
}
```

---

## Alerting Rules (Prometheus)

```yaml
# alerts.yml
groups:
  - name: rust-service
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) 
          / sum(rate(http_requests_total[5m])) > 0.05
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "High error rate on {{ $labels.service }}"
          
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95, 
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
          ) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency on {{ $labels.service }}"
          
      - alert: HighMemoryUsage
        expr: |
          (process_resident_memory_bytes / process_max_memory_bytes) > 0.85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
```

---

## References

- [tracing](https://docs.rs/tracing/latest/tracing/)
- [tracing-subscriber](https://docs.rs/tracing-subscriber/latest/tracing_subscriber/)
- [metrics](https://docs.rs/metrics/latest/metrics/)
- [metrics-exporter-prometheus](https://docs.rs/metrics-exporter-prometheus/latest/metrics_exporter_prometheus/)
- [opentelemetry-rust](https://github.com/open-telemetry/opentelemetry-rust)
- [tracing-opentelemetry](https://docs.rs/tracing-opentelemetry/latest/tracing_opentelemetry/)