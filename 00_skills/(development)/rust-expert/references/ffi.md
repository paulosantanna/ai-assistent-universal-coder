# FFI Reference

Updated: 2026-10-10

---

## Basic FFI

### extern "C" Functions
```rust
// Called from C
#[no_mangle]
pub extern "C" fn add(a: i32, b: i32) -> i32 {
    a + b
}

// Calling C from Rust
extern "C" {
    fn c_function(x: i32) -> i32;
}

fn call_c() {
    unsafe { c_function(42) };
}
```

### Type Mapping
| Rust | C |
|------|---|
| `i8` / `u8` | `int8_t` / `uint8_t` |
| `i16` / `u16` | `int16_t` / `uint16_t` |
| `i32` / `u32` | `int32_t` / `uint32_t` |
| `i64` / `u64` | `int64_t` / `uint64_t` |
| `f32` | `float` |
| `f64` | `double` |
| `bool` | `_Bool` / `bool` (C99) |
| `*const T` | `const T*` |
| `*mut T` | `T*` |
| `&T` | `const T*` (reference) |
| `&mut T` | `T*` (mutable reference) |

### Strings
```rust
use std::ffi::{CStr, CString};
use std::os::raw::c_char;

// Rust -> C
fn to_c_string(s: &str) -> *mut c_char {
    CString::new(s).unwrap().into_raw()
}

// C -> Rust
unsafe fn from_c_string(ptr: *const c_char) -> String {
    CStr::from_ptr(ptr).to_string_lossy().into_owned()
}

// Free C string allocated by Rust
#[no_mangle]
pub extern "C" fn free_string(ptr: *mut c_char) {
    if !ptr.is_null() {
        unsafe { drop(CString::from_raw(ptr)) };
    }
}
```

---

## bindgen

### Cargo.toml
```toml
[build-dependencies]
bindgen = "0.69"

[dependencies]
libc = "0.2"
```

### build.rs
```rust
use std::env;
use std::path::PathBuf;

fn main() {
    let bindings = bindgen::Builder::default()
        .header("wrapper.h")
        .parse_callbacks(Box::new(bindgen::CargoCallbacks::new()))
        .generate()
        .expect("Unable to generate bindings");

    let out_path = PathBuf::from(env::var("OUT_DIR").unwrap());
    bindings
        .write_to_file(out_path.join("bindings.rs"))
        .expect("Couldn't write bindings!");
}
```

### wrapper.h
```c
// Include C headers
#include <mylib.h>
#include <stdint.h>
```

### Using Generated Bindings
```rust
// src/lib.rs
include!(concat!(env!("OUT_DIR"), "/bindings.rs"));

pub fn use_c_lib() {
    unsafe {
        let result = my_c_function(42);
        println!("Result: {}", result);
    }
}
```

---

## cxx (Safe C++ Interop)

### Cargo.toml
```toml
[dependencies]
cxx = "1.0"
cxx-build = "1.0"
```

### build.rs
```rust
fn main() {
    cxx_build::bridge("src/bridge.rs")
        .file("src/cpp_impl.cpp")
        .compile("mycpp");
    println!("cargo:rerun-if-changed=src/bridge.rs");
    println!("cargo:rerun-if-changed=src/cpp_impl.cpp");
}
```

### bridge.rs
```rust
#[cxx::bridge]
mod ffi {
    extern "Rust" {
        fn rust_function(x: i32) -> i32;
    }

    unsafe extern "C++" {
        include!("cpp_header.h");
        fn cpp_function(x: i32) -> i32;
        type MyCppClass;
        fn create_my_class() -> UniquePtr<MyCppClass>;
        fn do_something(self: &MyCppClass, x: i32) -> i32;
    }
}
```

### cpp_impl.cpp
```cpp
#include "cpp_header.h"
#include "bridge.rs.h"

int cpp_function(int x) {
    return x * 2;
}

// MyCppClass implementation...
```

---

## safer_ffi

### Cargo.toml
```toml
[dependencies]
safer_ffi = "0.4"
```

### FFI Definition
```rust
use safer_ffi::prelude::*;

#[ffi_export]
fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[ffi_export]
fn process_string(input: char_p::Ref<'_>) -> char_p::Box {
    let s = input.to_str().unwrap();
    let result = format!("Processed: {}", s);
    char_p::Box::new(result)
}

#[ffi_export]
struct MyStruct {
    value: i32,
}

#[ffi_export]
impl MyStruct {
    #[ffi_export]
    pub fn new(value: i32) -> Self {
        Self { value }
    }
    
    #[ffi_export]
    pub fn get_value(&self) -> i32 {
        self.value
    }
}

// Generate header
safer_ffi::generate::generate_to_file(
    "include/my_ffi.h",
    safer_ffi::gen_config::Config::default()
).unwrap();
```

---

## CMake Integration

### CMakeLists.txt
```cmake
cmake_minimum_required(VERSION 3.10)
project(my_rust_lib)

find_program(RUSTC rustc)
find_program(CARGO cargo)

add_custom_target(rust_lib
    COMMAND ${CARGO} build --release
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/rust
)

add_library(rust_lib STATIC IMPORTED)
set_target_properties(rust_lib PROPERTIES
    IMPORTED_LOCATION ${CMAKE_SOURCE_DIR}/rust/target/release/libmy_rust_lib.a
)

add_dependencies(rust_lib rust_lib)
```

---

## Callbacks

### Rust Callback to C
```rust
type Callback = extern "C" fn(i32);

#[no_mangle]
pub extern "C" fn register_callback(cb: Callback) {
    CALLBACK.with(|c| *c.borrow_mut() = Some(cb));
}

thread_local! {
    static CALLBACK: RefCell<Option<Callback>> = RefCell::new(None);
}

fn trigger_callback(value: i32) {
    CALLBACK.with(|c| {
        if let Some(cb) = *c.borrow() {
            cb(value);
        }
    });
}
```

---

## References

- [Rust FFI Omnibus](https://github.com/mozilla/rust-ffi-omnibus)
- [bindgen](https://docs.rs/bindgen/latest/bindgen/)
- [cxx](https://cxx.rs/)
- [safer_ffi](https://docs.rs/safer_ffi/latest/safer_ffi/)
- [The Rustonomicon - FFI](https://doc.rust-lang.org/nomicon/ffi.html)