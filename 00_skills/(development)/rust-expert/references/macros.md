# Macros Reference

Updated: 2026-10-10

---

## Declarative Macros (macro_rules!)

### Basic Syntax
```rust
macro_rules! vec {
    () => { Vec::new() };
    ($($x:expr),+ $(,)?) => {{
        let mut temp_vec = Vec::new();
        $(temp_vec.push($x);)+
        temp_vec
    }};
}
```

### Metavariables
| Fragment | Matches |
|----------|---------|
| `expr` | Expression |
| `ty` | Type |
| `pat` | Pattern |
| `ident` | Identifier |
| `path` | Path (e.g., `std::vec::Vec`) |
| `tt` | Token tree (any single token) |
| `block` | Block `{ ... }` |
| `stmt` | Statement |
| `item` | Item (fn, struct, etc.) |
| `meta` | Attribute (`#[...]`) |
| `lifetime` | Lifetime (`'a`) |
| `literal` | Literal (`"hello"`, `42`) |

### Repetition
```rust
// Zero or more
$( $x:expr ),*

// One or more
$( $x:expr ),+

// Optional (zero or one)
$( $x:expr )?
```

### Hygiene
```rust
// $crate for absolute paths in macros
macro_rules! my_macro {
    () => { $crate::my_function() };
}

// Variable capture
macro_rules! create_fn {
    ($name:ident) => {
        fn $name() { println!("{}", stringify!($name)); }
    };
}
```

---

## Procedural Macros

### Cargo.toml Setup
```toml
[lib]
proc-macro = true

[dependencies]
syn = { version = "2.0", features = ["full", "extra-traits"] }
quote = "1.0"
proc-macro2 = "1.0"
```

### Derive Macro
```rust
// src/lib.rs
use proc_macro::TokenStream;
use quote::quote;
use syn::{parse_macro_input, DeriveInput};

#[proc_macro_derive(Hello)]
pub fn hello_derive(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as DeriveInput);
    let name = &input.ident;
    
    let expanded = quote! {
        impl #name {
            pub fn hello(&self) {
                println!("Hello, {}!", stringify!(#name));
            }
        }
    };
    
    TokenStream::from(expanded)
}
```

### Attribute Macro
```rust
#[proc_macro_attribute]
pub fn my_attribute(attr: TokenStream, item: TokenStream) -> TokenStream {
    let input = parse_macro_input!(item as ItemFn);
    // Transform function...
    TokenStream::from(quote! { #input })
}
```

### Function-like Macro
```rust
#[proc_macro]
pub fn sql(input: TokenStream) -> TokenStream {
    let query = parse_macro_input!(input as LitStr);
    // Parse SQL at compile time...
    TokenStream::from(quote! { ... })
}
```

---

## Syn & Quote

### Parsing with Syn
```rust
use syn::{parse_quote, ItemFn, ReturnType};

fn process_fn(input: TokenStream) -> TokenStream {
    let mut item: ItemFn = parse_macro_input!(input);
    
    // Modify return type
    item.sig.output = parse_quote! { -> Result<#output, MyError> };
    
    // Add attribute
    item.attrs.push(parse_quote! { #[instrument] });
    
    quote! { #item }.into()
}
```

### Quoting with Quote
```rust
use quote::{quote, format_ident};

let struct_name = format_ident!("MyStruct");
let field_name = format_ident!("field_{}", 42);

let expanded = quote! {
    struct #struct_name {
        #field_name: i32,
    }
    
    impl #struct_name {
        fn new() -> Self {
            Self { #field_name: 0 }
        }
    }
};
```

---

## Common Patterns

### Generate Implementations
```rust
macro_rules! impl_display {
    ($($t:ty),+) => {
        $(impl std::fmt::Display for $t {
            fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
                write!(f, "{}", self.0)
            }
        })+
    };
}

impl_display!(UserId, PostId, CommentId);
```

### Compile-time Validation
```rust
macro_rules! assert_const {
    ($cond:expr, $msg:literal) => {
        const _: () = assert!($cond, $msg);
    };
}

assert_const!(std::mem::size_of::<MyType>() <= 64, "MyType too large");
```

---

## Testing Macros

```rust
#[test]
fn test_macro() {
    let result = my_macro!(1, 2, 3);
    assert_eq!(result, vec![1, 2, 3]);
}

// For procedural macros, use trybuild
// tests/compile_fail/invalid_input.rs
// #![feature(proc_macro_hygiene)]
// use my_crate::my_macro;
// my_macro!(invalid); // Should fail to compile
```

---

## References

- [macro_rules!](https://doc.rust-lang.org/reference/macros-by-example.html)
- [Procedural Macros](https://doc.rust-lang.org/reference/procedural-macros.html)
- [syn](https://docs.rs/syn/latest/syn/)
- [quote](https://docs.rs/quote/latest/quote/)
- [The Little Book of Rust Macros](https://veykril.github.io/tlborm/)