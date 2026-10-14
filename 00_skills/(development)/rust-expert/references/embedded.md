# Embedded Reference

Updated: 2026-10-10

---

## no_std Basics

```rust
#![no_std]
#![no_main]

use cortex_m_rt::entry;
use panic_halt as _;

#[entry]
fn main() -> ! {
    loop {
        // Your embedded code here
    }
}
```

---

## cortex-m

### Peripheral Access
```rust
use cortex_m::peripheral::{Peripheral, SCB, SYST};

fn init() {
    let p = cortex_m::Peripherals::take().unwrap();
    let mut syst = p.SYST;
    syst.set_reload(16_000_000);
    syst.enable_counter();
    syst.enable_interrupt();
}
```

---

## Embassy (Async Embedded)

```toml
embassy-executor = { version = "0.4", features = ["nightly"] }
embassy-time = { version = "0.4", features = ["nightly"] }
embassy-stm32 = { version = "0.4", features = ["stm32f4", "nightly"] }
```

```rust
#[embassy_executor::main]
async fn main(spawner: Spawner) {
    let p = embassy_stm32::init(Default::default());
    spawner.spawn(blink_task(p.PA5)).unwrap();
}

#[embassy_executor::task]
async fn blink_task(pin: AnyPin) {
    let mut led = Output::new(pin, Level::Low, Speed::Low);
    loop {
        led.set_high();
        Timer::after(Duration::from_millis(500)).await;
        led.set_low();
        Timer::after(Duration::from_millis(500)).await;
    }
}
```

---

## RTIC

```rust
#[rtic::app(device = stm32f4xx_hal::pac)]
mod app {
    #[shared] struct Shared { counter: u32 }
    #[local] struct Local { led: PA5<Output<PushPull>> }
    
    #[init]
    fn init(cx: init::Context) -> (Shared, Local, init::Monotonics) { ... }
    
    #[task(binds = SysTick, shared = [counter], local = [led])]
    fn sys_tick(cx: sys_tick::Context) { ... }
}
```

---

## defmt (Logging)

```rust
use defmt::{info, warn, error};
info!("Value: {}", 42);
```

---

## References

- [Embedded Rust Book](https://docs.rust-embedded.org/book/)
- [Embassy](https://embassy.dev/)
- [RTIC](https://rtic.rs/)
- [defmt](https://defmt.ferrous-systems.com/)