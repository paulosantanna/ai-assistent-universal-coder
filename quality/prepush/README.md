# Portão antes do push

Updated: 2026-11-09
Entry point: `quality/prepush/prepush.py`

O mesmo comando vale no Git local e no workflow `.github/workflows/prepush-gate.yml`. Sem rede, com base velha ou com achado, o push não passa. Não há modo offline que aprove.

```powershell
python quality/prepush/prepush.py --repo .
python quality/prepush/prepush.py --install-hook
```

O hook instalado fica em `.git/hooks/pre-push` e chama esse comando. A saída resumida aparece no terminal. O relatório completo vai para `.aeos/prepush/report.json` (pasta local, fora do Git).

Códigos: `0` passou, `1` achado, `2` fonte indisponível ou desatualizada.

## O que os workflows já faziam

Leitura em 2026-11-09, só do texto dos workflows:

| Repositório | O que o workflow executa | O que não executa |
| --- | --- | --- |
| ai-assistent-universal-coder | gates de skill/MCP em `quality/validate.py`; Python 3.12 e Node 24 | OSV, SAST, moeda de biblioteca, PE |
| AIHealthResearch | `bandit` e `pip-audit` nos locks; Python 3.12 | `osv-scanner` e CodeQL, embora `deploy-expert-unique` os cite |
| MyDigitalBuddy | OSV 2.6.0, RustSec, Rust stable atual, `Cargo.lock` seco, SLSA no release | SAST de aplicação além do Clippy |
| iDentifyer | `npm audit` high, Node 24, Cargo com Clippy | OSV; `rustc` só é impresso; actions em `@v4` |
| pdfcraft | Rust stable pinado, recurso de versão do EXE no Windows, Clippy | OSV e auditoria de dependência |
| FreePDFReader | Rust em `@master` e `@stable` | OSV, SAST e pin de toolchain |
| laya, Engenharia-Reversa, ibunny, DiabeticsresearchJEV | linguagem declarada no workflow | sem OSV, Bandit, CodeQL, npm audit ou Semgrep no texto buscado |

## Backends

Cada um consulta a fonte na hora. Exceção permanente não existe: `exceptions.json` só vale com `expires` futuro e `reason`.

| Backend | Fonte | Bloqueia quando |
| --- | --- | --- |
| `cve_google` | export OSV da Google e `api.osv.dev` | export com mais de 72 h, consulta falha, ou CVE/GHSA não retirado |
| `libraries` | PyPI, npm, crates.io, proxy Go | dependência direta sem pin, atrás do estável atual, ou índice que não é o público |
| `language` | endoflife.date | ciclo declarado, piso ou interpretador fora do ciclo suportado mais novo; patch pinado atrás do `latest` |
| `executables` | recurso de versão do PE | `.exe` sem `CompanyName` ou `FileVersion`, ou compilado há mais de 90 dias |
| `sast` | regras locais alinhadas ao commit atual de `semgrep/semgrep-rules` `develop` | regras atrás do upstream, upstream fora do ar, ou padrão perigoso |
| `security` | regras locais alinhadas ao release atual do gitleaks | segredo, action sem commit de 40 caracteres, `pull_request_target`, `write-all`, catálogo atrás do release |

`security` confere o que está no arquivo. Não invade serviço, não envia payload e não substitui um pentest autorizado.

`00_skills/`, `02_repositorios/`, `07_mapeamentos/`, `.work/`, `.tools/`, `.venv/`, `venv/` e `.state/` ficam de fora: são catálogo, espelho, ambiente ou runtime local, não o código que este portão publica. Arquivo maior que 1 MB não entra na busca de segredo.

Para apontar outro clone: `python quality/prepush/prepush.py --repo E:\Github\MyDigitalBuddy`.
