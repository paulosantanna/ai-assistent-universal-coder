# Web (Axum) Reference

Updated: 2026-10-10

---

## Axum Basics

### Minimal Server
```rust
use axum::{Router, routing::get, response::Html};

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/", get(|| async { "Hello, World!" }))
        .route("/health", get(health_check));

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

async fn health_check() -> &'static str {
    "OK"
}
```

### Router Composition
```rust
let app = Router::new()
    .route("/users", get(list_users).post(create_user))
    .route("/users/:id", get(get_user).patch(update_user).delete(delete_user))
    .nest("/api", api_router())
    .nest("/admin", admin_router())
    .layer(middleware::from_fn(logging_middleware))
    .with_state(AppState::new());

fn api_router() -> Router<AppState> {
    Router::new()
        .route("/v1/users", get(list_users_v1))
        .route("/v1/posts", get(list_posts))
}
```

---

## Extractors

### Path Parameters
```rust
use axum::extract::Path;

async fn get_user(Path(id): Path<Uuid>) -> Result<Json<User>, AppError> {
    let user = db.get_user(id).await?;
    Ok(Json(user))
}

// Multiple params
async fn get_post(Path((user_id, post_id)): Path<(Uuid, Uuid)>) { ... }

// With validation
use axum::extract::Path;
use serde::Deserialize;

#[derive(Deserialize)]
struct Params {
    id: Uuid,
    #[serde(rename = "postId")]
    post_id: Uuid,
}

async fn get_post(Path(Params { id, post_id }): Path<Params>) { ... }
```

### Query Parameters
```rust
use axum::extract::Query;
use serde::Deserialize;

#[derive(Deserialize)]
struct Pagination {
    page: Option<u32>,
    per_page: Option<u32>,
    #[serde(rename = "sortBy")]
    sort_by: Option<String>,
}

async fn list_users(Query(pagination): Query<Pagination>) -> Json<Vec<User>> {
    let page = pagination.page.unwrap_or(1);
    let per_page = pagination.per_page.unwrap_or(20).min(100);
    // ...
}
```

### JSON Body
```rust
use axum::extract::Json;
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
struct CreateUser {
    email: String,
    name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    bio: Option<String>,
}

#[derive(Serialize)]
struct UserResponse {
    id: Uuid,
    email: String,
    name: String,
    created_at: DateTime<Utc>,
}

async fn create_user(Json(payload): Json<CreateUser>) -> Result<Json<UserResponse>, AppError> {
    let user = db.create_user(payload).await?;
    Ok(Json(user.into()))
}
```

### State
```rust
use axum::extract::State;
use std::sync::Arc;

#[derive(Clone)]
struct AppState {
    db: Arc<Database>,
    config: Arc<Config>,
}

async fn get_user(State(state): State<AppState>, Path(id): Path<Uuid>) -> Result<Json<User>> {
    let user = state.db.get_user(id).await?;
    Ok(Json(user))
}

// In main:
let state = AppState { db: Arc::new(db), config: Arc::new(config) };
let app = Router::new().route("/users/:id", get(get_user)).with_state(state);
```

### Headers & Extensions
```rust
use axum::extract::{Request, HeaderMap, Extension};
use axum::http::{HeaderValue, StatusCode};

async fn with_headers(headers: HeaderMap) {
    let auth = headers.get("authorization");
    let content_type = headers.get("content-type");
}

async fn with_extension(Extension(user): Extension<AuthenticatedUser>) { ... }

// Full request access
async fn with_request(req: Request) {
    let method = req.method();
    let uri = req.uri();
    let version = req.version();
}
```

### Form & Multipart
```rust
use axum::extract::{Form, Multipart};

#[derive(Deserialize)]
struct LoginForm {
    username: String,
    password: String,
}

async fn login(Form(form): Form<LoginForm>) { ... }

// Multipart file upload
async fn upload(mut multipart: Multipart) {
    while let Some(field) = multipart.next_field().await.unwrap() {
        let name = field.name().unwrap().to_string();
        let data = field.bytes().await.unwrap();
        // Save file...
    }
}
```

---

## Responses

### Built-in Response Types
```rust
use axum::response::{Html, Json, Redirect, IntoResponse};
use axum::http::StatusCode;

// JSON (implements IntoResponse)
async fn json_response() -> Json<Value> {
    Json(json!({ "status": "ok" }))
}

// HTML
async fn html_response() -> Html<&'static str> {
    Html("<h1>Hello</h1>")
}

// Redirect
async fn redirect() -> Redirect {
    Redirect::permanent("/new-location")
}

// Status code
async fn created() -> (StatusCode, Json<Value>) {
    (StatusCode::CREATED, Json(json!({ "id": 1 })))
}

// Tuple responses
async fn tuple_response() -> (StatusCode, HeaderMap, Json<Value>) {
    let mut headers = HeaderMap::new();
    headers.insert("X-Custom", "value".parse().unwrap());
    (StatusCode::OK, headers, Json(json!({})))
}
```

### Custom Response Types
```rust
use axum::response::{IntoResponse, Response};
use axum::http::{StatusCode, HeaderMap};

struct ApiResponse<T> {
    status: StatusCode,
    data: T,
    headers: HeaderMap,
}

impl<T: Serialize> IntoResponse for ApiResponse<T> {
    fn into_response(self) -> Response {
        let mut response = Json(self.data).into_response();
        *response.status_mut() = self.status;
        response.headers_mut().extend(self.headers);
        response
    }
}

// Usage
async fn custom_response() -> ApiResponse<User> {
    ApiResponse {
        status: StatusCode::CREATED,
        data: user,
        headers: HeaderMap::new(),
    }
}
```

---

## Error Handling

### Error Type with IntoResponse
```rust
use axum::response::{IntoResponse, Response};
use axum::http::StatusCode;
use thiserror::Error;

#[derive(Error, Debug)]
enum AppError {
    #[error("not found: {0}")]
    NotFound(String),
    #[error("database error: {0}")]
    Database(#[from] sqlx::Error),
    #[error("validation error: {0}")]
    Validation(String),
    #[error("unauthorized")]
    Unauthorized,
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, message) = match self {
            AppError::NotFound(msg) => (StatusCode::NOT_FOUND, msg),
            AppError::Database(e) => {
                tracing::error!(error = %e, "database error");
                (StatusCode::INTERNAL_SERVER_ERROR, "Internal server error".to_string())
            }
            AppError::Validation(msg) => (StatusCode::BAD_REQUEST, msg),
            AppError::Unauthorized => (StatusCode::UNAUTHORIZED, "Unauthorized".to_string()),
        };

        let body = Json(json!({ "error": message }));
        (status, body).into_response()
    }
}

// Usage in handlers
async fn get_user(Path(id): Path<Uuid>) -> Result<Json<User>, AppError> {
    let user = db.get_user(id).await
        .map_err(|_| AppError::Database(sqlx::Error::RowNotFound))?;
    Ok(Json(user))
}
```

### Global Error Handling (axum-extra)
```toml
# Cargo.toml
axum-extra = { version = "0.9", features = ["routing"] }
```
```rust
use axum_extra::routing::RouterExt;

let app = Router::new()
    .route("/users", get(list_users))
    .route_with_error_handler(|error: AppError| async move {
        // Custom error handling middleware
        error.into_response()
    });
```

---

## Middleware (Tower Layers)

### Custom Middleware
```rust
use axum::middleware::{self, Next};
use axum::response::Response;
use axum::extract::Request;
use std::time::Instant;

async fn logging_middleware(req: Request, next: Next) -> Response {
    let start = Instant::now();
    let method = req.method().clone();
    let uri = req.uri().clone();
    
    let response = next.run(req).await;
    
    let latency = start.elapsed();
    tracing::info!(
        method = %method,
        uri = %uri,
        status = %response.status(),
        latency_ms = latency.as_millis(),
        "request completed"
    );
    
    response
}

// Apply to router
let app = Router::new()
    .route("/users", get(list_users))
    .layer(middleware::from_fn(logging_middleware));

// Apply to specific routes
let app = Router::new()
    .route("/public", get(public))
    .route("/private", get(private).layer(middleware::from_fn(auth_middleware)));
```

### Tower Layers
```rust
use tower::{ServiceBuilder, ServiceExt};
use tower_http::{
    cors::CorsLayer,
    trace::TraceLayer,
    compression::CompressionLayer,
    limit::RequestBodyLimitLayer,
    timeout::TimeoutLayer,
    sensitive_headers::SetSensitiveHeadersLayer,
};

let app = Router::new()
    .route("/api/users", get(list_users))
    .layer(
        ServiceBuilder::new()
            .layer(TraceLayer::new_for_http())
            .layer(CompressionLayer::new())
            .layer(RequestBodyLimitLayer::new(1024 * 1024)) // 1MB
            .layer(TimeoutLayer::new(Duration::from_secs(30)))
            .layer(CorsLayer::permissive())
            .layer(SetSensitiveHeadersLayer::new(std::iter::once("authorization")))
    );
```

### CORS
```rust
use tower_http::cors::{CorsLayer, Any};

let cors = CorsLayer::new()
    .allow_origin(Any)  // Or specific: "https://example.com".parse().unwrap()
    .allow_methods([Method::GET, Method::POST, Method::PUT, Method::DELETE])
    .allow_headers([header::CONTENT_TYPE, header::AUTHORIZATION])
    .allow_credentials(true)
    .max_age(Duration::from_secs(3600));

let app = Router::new().layer(cors);
```

---

## WebSocket

```rust
use axum::extract::ws::{WebSocket, WebSocketUpgrade, Message};
use axum::response::IntoResponse;
use futures::{sink::SinkExt, stream::StreamExt};

async fn ws_handler(ws: WebSocketUpgrade) -> impl IntoResponse {
    ws.on_upgrade(handle_socket)
}

async fn handle_socket(mut socket: WebSocket) {
    while let Some(msg) = socket.recv().await {
        match msg {
            Ok(Message::Text(text)) => {
                socket.send(Message::Text(format!("Echo: {}", text))).await.ok();
            }
            Ok(Message::Binary(data)) => {
                socket.send(Message::Binary(data)).await.ok();
            }
            Ok(Message::Close(_)) => break,
            Ok(Message::Ping(data)) => {
                socket.send(Message::Pong(data)).await.ok();
            }
            Ok(Message::Pong(_)) => {}
            Err(e) => {
                tracing::error!(error = %e, "websocket error");
                break;
            }
        }
    }
}
```

---

## Server-Sent Events (SSE)

```rust
use axum::response::sse::{Event, Sse};
use futures::stream::{self, Stream};
use std::convert::Infallible;
use tokio::time::interval;

async fn sse_handler() -> Sse<impl Stream<Item = Result<Event, Infallible>>> {
    let stream = stream::unfold(interval(Duration::from_secs(1)), |mut interval| async move {
        interval.tick().await;
        let data = format!("{{\"time\": \"{}\"}}", Utc::now().to_rfc3339());
        Some((Ok(Event::default().data(data)), interval))
    });
    Sse::new(stream).keep_alive(axum::response::sse::KeepAlive::new())
}
```

---

## OpenAPI (utoipa)

```toml
# Cargo.toml
utoipa = { version = "5.0", features = ["axum_extras"] }
utoipa-swagger-ui = "5.0"
```

```rust
use utoipa::{OpenApi, ToSchema};
use utoipa_swagger_ui::SwaggerUi;

#[derive(OpenApi)]
#[openapi(
    paths(get_user, create_user, list_users),
    components(schemas(User, CreateUser, ErrorResponse)),
    tags((name = "users", description = "User management"))
)]
struct ApiDoc;

#[derive(Serialize, ToSchema)]
struct User {
    id: Uuid,
    email: String,
    name: String,
}

#[derive(Deserialize, ToSchema)]
struct CreateUser {
    email: String,
    name: String,
}

#[utoipa::path(
    get,
    path = "/api/users/{id}",
    params(
        ("id" = Uuid, Path, description = "User ID")
    ),
    responses(
        (status = 200, description = "User found", body = User),
        (status = 404, description = "Not found", body = ErrorResponse)
    )
)]
async fn get_user(Path(id): Path<Uuid>) -> Result<Json<User>, AppError> { ... }

let app = Router::new()
    .merge(SwaggerUi::new("/swagger-ui").url("/api-docs/openapi.json", ApiDoc::openapi()))
    .route("/api/users/:id", get(get_user));
```

---

## Testing

```rust
#[cfg(test)]
mod tests {
    use axum_test::TestServer;
    use super::*;

    #[tokio::test]
    async fn test_get_user() {
        let app = create_app(test_state());
        let server = TestServer::new(app).unwrap();

        let response = server.get("/users/123").await;
        response.assert_status_ok();
        let user: User = response.json();
        assert_eq!(user.id, uuid!("..."));
    }

    #[tokio::test]
    async fn test_create_user() {
        let app = create_app(test_state());
        let server = TestServer::new(app).unwrap();

        let response = server
            .post("/users")
            .json(&CreateUser { email: "test@example.com", name: "Test" })
            .await;
        response.assert_status_created();
    }
}
```

---

## Performance Tuning

```rust
// Connection pooling handled by hyper
// Tune via:
let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await?;
listener.set_nonblocking(true)?;

// SO_REUSEPORT (Linux) - multiple listeners
#[cfg(target_os = "linux")]
{
    use socket2::{Socket, Domain, Type, Protocol, SockRef};
    let socket = Socket::new(Domain::IPV4, Type::STREAM, Some(Protocol::TCP))?;
    socket.set_reuse_address(true)?;
    socket.set_reuse_port(true)?;  // Requires Linux 3.9+
    socket.bind(&"0.0.0.0:3000".parse().unwrap().into())?;
    socket.listen(1024)?;
    let listener: tokio::net::TcpListener = socket.into();
}

// Run multiple workers (behind load balancer)
// Each process binds to same port with SO_REUSEPORT
```

---

## References

- [Axum Docs](https://docs.rs/axum/latest/axum/)
- [Axum Examples](https://github.com/tokio-rs/axum/tree/main/examples)
- [Tower Docs](https://docs.rs/tower/latest/tower/)
- [Tower HTTP](https://docs.rs/tower-http/latest/tower_http/)
- [utoipa](https://docs.rs/utoipa/latest/utoipa/)