# WASM Reference

Updated: 2026-10-10

---

## wasm-bindgen

### Cargo.toml
```toml
[lib]
crate-type = ["cdylib", "rlib"]

[dependencies]
wasm-bindgen = "0.2"
js-sys = "0.3"
web-sys = { version = "0.3", features = ["console", "window", "document"] }
```

### Rust Code
```rust
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

#[wasm_bindgen]
pub struct Counter {
    value: i32,
}

#[wasm_bindgen]
impl Counter {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Self {
        Self { value: 0 }
    }
    
    pub fn increment(&mut self) {
        self.value += 1;
    }
    
    pub fn value(&self) -> i32 {
        self.value
    }
}
```

---

## wasm-pack

### Build
```bash
# Install
cargo install wasm-pack

# Build for web
wasm-pack build --target web --out-dir pkg

# Build for Node.js
wasm-pack build --target nodejs --out-dir pkg

# Build for bundler (webpack, rollup)
wasm-pack build --target bundler --out-dir pkg
```

### package.json (generated)
```json
{
  "name": "my-crate",
  "version": "0.1.0",
  "type": "module",
  "files": ["pkg"],
  "main": "pkg/my_crate.js",
  "module": "pkg/my_crate.js"
}
```

---

## JavaScript Usage

### ES Modules
```javascript
import init, { greet, Counter } from './pkg/my_crate.js';

await init();

console.log(greet("World"));

const counter = new Counter();
counter.increment();
console.log(counter.value());
```

### HTML
```html
<script type="module">
  import init, { greet } from './pkg/my_crate.js';
  await init();
  document.body.textContent = greet('WASM');
</script>
```

---

## Frontend Frameworks

### Leptos
```toml
[dependencies]
leptos = { version = "0.6", features = ["csr"] }
```

```rust
use leptos::*;

#[component]
fn Counter() -> impl IntoView {
    let (count, set_count) = create_signal(0);
    view! {
        <button on:click=move |_| set_count.update(|n| *n += 1)>
            "Count: " {count}
        </button>
    }
}
```

### Yew
```toml
[dependencies]
yew = "0.21"
```

```rust
use yew::prelude::*;

#[function_component]
fn Counter() -> Html {
    let count = use_state(|| 0);
    let onclick = {
        let count = count.clone();
        Callback::from(move |_| count.set(*count + 1))
    };
    html! {
        <button {onclick}>{ "Count: " }{ *count }</button>
    }
}
```

### Dioxus
```toml
[dependencies]
dioxus = "0.5"
```

```rust
use dioxus::prelude::*;

fn Counter(cx: Scope) -> Element {
    let count = use_state(cx, || 0);
    cx.render(rsx! {
        button { onclick: move |_| count += 1, "Count: {count}" }
    })
}
```

---

## wasm-opt (Optimization)

```bash
# Install
npm install -g wasm-opt
# or
cargo install wasm-opt

# Optimize
wasm-opt -Oz pkg/my_crate_bg.wasm -o pkg/my_crate_bg.wasm

# With debug info
wasm-opt -Oz -g pkg/my_crate_bg.wasm -o pkg/my_crate_bg.wasm
```

---

## wasm-pack CI

```yaml
# .github/workflows/wasm.yml
name: WASM
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions-rs/toolchain@v1
        with:
          toolchain: stable
          target: wasm32-unknown-unknown
      - uses: jetli/wasm-pack-action@v0.4.0
        with:
          version: 'latest'
      - run: wasm-pack build --target web --out-dir pkg
      - uses: actions/upload-artifact@v4
        with:
          name: pkg
          path: pkg/
```

---

## Interop Patterns

### Rust -> JS (Export)
```rust
#[wasm_bindgen]
extern "C" {
    #[wasm_bindgen(js_namespace = console)]
    fn log(s: &str);
    
    #[wasm_bindgen(js_namespace = window)]
    fn alert(s: &str);
}

#[wasm_bindgen]
pub fn call_js() {
    log("From Rust");
    alert("Hello from Rust!");
}
```

### JS -> Rust (Import)
```rust
#[wasm_bindgen(module = "/js/api.js")]
extern "C" {
    fn fetchData(url: &str) -> Promise<JsValue>;
}

#[wasm_bindgen]
pub async fn get_data() -> Result<JsValue, JsValue> {
    fetchData("/api/data").await
}
```

---

## References

- [wasm-bindgen](https://rustwasm.github.io/wasm-bindgen/)
- [wasm-pack](https://rustwasm.github.io/wasm-pack/)
- [Leptos](https://leptos.dev/)
- [Yew](https://yew.rs/)
- [Dioxus](https://dioxuslabs.com/)
- [wasm-opt](https://github.com/WebAssembly/binaryen)