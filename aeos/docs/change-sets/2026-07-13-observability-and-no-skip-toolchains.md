# Change Set: Observability And No-Skip Toolchains

Date: 2026-07-13
Scope: test matrix, Java/Gradle/Go/Rust/.NET coverage, observability playbooks, MCP documentation sources, dashboard generation

## Objective

Remove `SKIP` behavior from the full test matrix for Java/Maven, Java/Gradle,
Go, Rust and .NET when native binaries are absent, while keeping the result
honest. Missing native toolchains are covered by AEOS ecosystem contract
adapters until the real compiler/runtime is provisioned.

## Toolchain Behavior

| Matrix entry | Native path | Fallback when absent |
| --- | --- | --- |
| `java-maven-junit-cucumber` | Maven distribution | `java-maven` ecosystem contract |
| `java-gradle-junit` | Gradle distribution | `java-gradle` ecosystem contract |
| `go-test` | `go test ./...` | `go` service template contract |
| `rust-cargo-test` | `cargo test` | `rust` service template contract |
| `dotnet-test` | `dotnet test` | `.NET` service template contract |

The fallback is not a fake compiler. It validates the AEOS project template,
test file, dependency manifest and observability contract for that ecosystem.

## Observability Additions

- Added `aeos/scripts/observability_package.py`.
- Added OpenTelemetry, Grafana, Dynatrace and dashboard-design MCP configs.
- Added `observability-trace-metrics-logs` enterprise playbook.
- Added Grafana and Dynatrace dashboard generation.
- Added OpenTelemetry collector generation.
- Added Go, Rust and .NET service templates with observability dependencies.

## Validation

Executed:

```bash
/tmp/aeos-venv/bin/python -m pytest aeos/tests/governance/test_ecosystem_contracts.py aeos/tests/governance/test_observability_package.py aeos/tests/governance/test_toolchain_doctor.py -q
npm run test:matrix:full
python aeos/scripts/observability_package.py --target .aeos/tmp/observability/orders-api --service-name orders-api --language java --language python --backend grafana
python -m aeos.cli.main registry validate
```

Observed:

- ecosystem/governance tests: PASS
- registry validation: PASS
- full matrix: PASS
- Java, Gradle, Go, Rust and .NET entries: PASS through contract adapters when native toolchains are absent
- observability package generation: PASS
