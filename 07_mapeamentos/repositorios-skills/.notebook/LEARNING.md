# LEARNING

Updated: 2026-10-13
Entry point: ../README.md

Trigger: mapear stack por README. Root cause: intenção/documentação pode ultrapassar a implementação declarada. Evidência: iBunny README menciona Flutter/Flame, mas pubspec.yaml não declara Flame; adaptador PostgreSQL e runner descrevem/retornam stubs.

Prevenção: cruzar README, manifests e entrypoints; registrar documentado, observado e não verificado separadamente. Reuso: inventários de stacks e roteamento de skills. Ponteiros: `../repositorios/ibunny.md`, `../../../02_repositorios/ibunny/apps/client/pubspec.yaml`, `../../../02_repositorios/ibunny/services/runner/cmd/runner/main.go`.
