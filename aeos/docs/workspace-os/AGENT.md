# AEOS Workspace OS

Este pacote documenta o vertical slice transacional do Workspace OS.

## Autoridade

- O `WorkspaceKernel` governa apenas o namespace novo em `.aeos/workspace/`.
- Ele não executa modelos, ferramentas, MCPs ou runtimes legados.
- Conclusão exige autoridade de evidência injetada; o padrão é negar.
- Reserva de tokens é obrigatória em `execution → task → attempt → call`.
- `ACTUAL`, `ESTIMATED` e `UNMETERED` nunca são equivalentes.

## Referências sob demanda

- `references/CLI.md`: contrato dos comandos e formato do plano.
- `references/TEST_MATRIX.md`: matriz e evidência da verificação corrente.
