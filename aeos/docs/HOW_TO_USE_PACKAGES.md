# How to Use AEOS ZIP Packages

## Create

```powershell
aeos package create --execution-id <id> --target <path> --type full-review
```

## Verify

```powershell
aeos package verify --package <zip_path>
```

## Inspect

```powershell
aeos package inspect --package <zip_path>
```

## Extract Safely

```powershell
aeos package extract --package <zip_path> --to <safe_staging_path>
```

## Rules

- Never extract unverified packages.
- Never extract directly over project root.
- Never include secrets.
- Never include `.env` real files.
- Never include browser profiles or credential stores.
