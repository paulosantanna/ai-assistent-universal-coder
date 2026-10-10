# Serialization Reference

Updated: 2026-10-10

---

## serde Basics

```toml
# Cargo.toml
[dependencies]
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
```

### Derive Macros
```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
struct User {
    id: Uuid,
    email: String,
    name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    bio: Option<String>,
    #[serde(rename = "createdAt")]
    created_at: DateTime<Utc>,
    #[serde(flatten)]
    metadata: HashMap<String, serde_json::Value>,
}
```

### Field Attributes
```rust
#[derive(Serialize, Deserialize)]
struct Config {
    #[serde(default = "default_port")]
    port: u16,
    
    #[serde(rename = "max-connections")]
    max_connections: usize,
    
    #[serde(skip)]
    internal: String,
    
    #[serde(serialize_with = "serialize_duration")]
    timeout: Duration,
}

fn default_port() -> u16 { 8080 }

fn serialize_duration<S>(duration: &Duration, serializer: S) -> Result<S::Ok, S::Error>
where
    S: serde::Serializer,
{
    serializer.serialize_u64(duration.as_secs())
}
```

---

## Formats

### JSON
```rust
use serde_json::{json, to_string, from_str};

let user = User { ... };
let json_string = to_string(&user)?;
let user: User = from_str(&json_string)?;
```

### Binary (bincode)
```toml
# Cargo.toml
bincode = "1.3"
```
```rust
use bincode::{serialize, deserialize};

let bytes = serialize(&user)?;
let user: User = deserialize(&bytes)?;
```

### MessagePack (rmp-serde)
```toml
# Cargo.toml
rmp-serde = "1.1"
```
```rust
use rmp_serde::{to_vec, from_slice};

let bytes = to_vec(&user)?;
let user: User = from_slice(&bytes)?;
```

### Postcard (no_std)
```toml
# Cargo.toml
postcard = "1.0"
```
```rust
use postcard::{to_stdvec, from_bytes};

let bytes = to_stdvec(&user)?;
let user: User = from_bytes(&bytes)?;
```

---

## Custom Serialization

### Serialize Trait
```rust
use serde::ser::{Serialize, Serializer};

impl Serialize for MyType {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        // Custom serialization logic
        serializer.serialize_str(&self.to_string())
    }
}
```

### Deserialize Trait
```rust
use serde::de::{Deserialize, Deserializer, Visitor};

impl<'de> Deserialize<'de> for MyType {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        struct MyVisitor;
        impl<'de> Visitor<'de> for MyVisitor {
            type Value = MyType;
            fn expecting(&self, f: &mut fmt::Formatter) -> fmt::Result {
                write!(f, "a MyType")
            }
            fn visit_str<E>(self, v: &str) -> Result<Self::Value, E>
            where
                E: serde::de::Error,
            {
                MyType::from_str(v).map_err(E::custom)
            }
        }
        deserializer.deserialize_str(MyVisitor)
    }
}
```

---

## Serde With (Helper Crates)

```toml
# Cargo.toml
serde_with = "3.0"
```

```rust
use serde_with::{serde_as, DisplayFromStr};

#[serde_as]
struct Data {
    #[serde_as(as = "DisplayFromStr")]
    id: Uuid,
    
    #[serde_as(as = "Vec<DisplayFromStr>")]
    tags: Vec<Uuid>,
}
```

---

## References

- [serde](https://serde.rs/)
- [serde_json](https://docs.rs/serde_json/latest/serde_json/)
- [bincode](https://docs.rs/bincode/latest/bincode/)
- [rmp-serde](https://docs.rs/rmp-serde/latest/rmp_serde/)
- [postcard](https://docs.rs/postcard/latest/postcard/)
- [serde_with](https://docs.rs/serde_with/latest/serde_with/)