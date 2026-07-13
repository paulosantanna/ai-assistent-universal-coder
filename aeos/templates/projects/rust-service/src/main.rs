fn greeting(name: &str) -> String {
    format!("hello {name}")
}

#[tokio::main]
async fn main() {
    let _tracer_name = "opentelemetry-aeos-rust-service";
    println!("{}", greeting("aeos"));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn greets_aeos() {
        assert_eq!(greeting("aeos"), "hello aeos");
    }
}
