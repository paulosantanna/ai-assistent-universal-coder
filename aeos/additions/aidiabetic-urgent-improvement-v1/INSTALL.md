# Instalação e ativação

## 1. Pré-condições

- Python 3 disponível por `py -3`;
- Git instalado;
- AEOS e AIDiabetic Research em diretórios separados;
- working tree conhecida antes da instalação;
- nenhuma credencial real dentro do pack.

## 2. Validar o pack

```powershell
py -3 .\scripts\validate_package.py
py -3 -m pytest .\tests -ra
```

## 3. Dry-run da instalação

```powershell
py -3 .\scripts\install_overlay.py `
  --aeos-root "E:\GitHub\aeos\AEOS_CHIEF_STAFF_v1" `
  --target-root "E:\GitHub\aidiabetic-research" `
  --dry-run
```

## 4. Instalar overlay

```powershell
py -3 .\scripts\install_overlay.py `
  --aeos-root "E:\GitHub\aeos\AEOS_CHIEF_STAFF_v1" `
  --target-root "E:\GitHub\aidiabetic-research"
```

Arquivos instalados:

```text
<AEOS>\aeos\additions\aidiabetic-urgent-improvement-v1\
<AEOS>\aeos\overlays\aidiabetic-urgent-improvement-v1.index.yaml
<TARGET>\.aeos\aidiabetic-improvement-pack.yaml
```

## 5. Executar

```powershell
.\commands\RUN_FULL.ps1 `
  -AeosRoot "E:\GitHub\aeos\AEOS_CHIEF_STAFF_v1" `
  -TargetRoot "E:\GitHub\aidiabetic-research"
```

## 6. Remover o overlay

```powershell
py -3 .\scripts\install_overlay.py `
  --aeos-root "E:\GitHub\aeos\AEOS_CHIEF_STAFF_v1" `
  --target-root "E:\GitHub\aidiabetic-research" `
  --uninstall
```

A remoção não desfaz alterações já aplicadas no projeto alvo. Essas alterações
devem ser revertidas pelo mecanismo de rollback registrado na execução.
