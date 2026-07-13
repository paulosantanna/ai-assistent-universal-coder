# Skill Factory — `create --prompt`

Substitua o arquivo existente por `skill_factory.py`.

## Comando

```powershell
py -3 .\skill_factory.py create `
  --prompt "Create a Java Bug Solver skill that analyzes stack traces, searches for root causes, generates fixes, validates them and stores lessons learned." `
  --output "..\..\..\..\..\skills"
```

O comando infere automaticamente:

- nome;
- descrição;
- regra de ativação;
- categoria;
- nível de arquitetura;
- risco.

Os parâmetros inferidos ainda podem ser sobrescritos manualmente com `--name`, `--category`, `--level`, `--risk`, `--activation` e `--description`.
