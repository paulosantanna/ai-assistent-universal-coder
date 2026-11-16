# Portão antes do push

Updated: 2026-11-09
Entry point: `quality/prepush/prepush.py`

- Fact: os workflows locais não cobrem o mesmo conjunto. MyDigitalBuddy consulta a OSV e exige Rust stable. AIHealthResearch roda Bandit e pip-audit. O texto de `deploy-expert-unique` cita OSV e CodeQL, e `AIHealthResearch/.github/workflows/ci.yml` não tem esses passos. iDentifyer faz `npm audit` com actions em tag. pdfcraft exige recurso de versão no EXE do Windows.
- Decision: um comando só, `python quality/prepush/prepush.py`, é o pré-requisito local e o job `.github/workflows/prepush-gate.yml`. Seis backends: OSV Google, registro de biblioteca, endoflife.date, PE, SAST alinhado ao commit de `semgrep/semgrep-rules`, segurança estática alinhada ao release do gitleaks. Fonte velha ou fora do ar bloqueia. Exceção só com data e motivo.
- Fact: em 2026-11-09 a corrida neste repositório terminou `fail` com as fontes frescas (export OSV do mesmo dia). CVE em certifi 2026.7.22, pypdf 6.20.1, axios 1.18.1, undici 7.28.0 e follow-redirects 1.16.0. Bibliotecas diretas atrás ou sem pin. Python declarado 3.12 e Node 24; ciclos atuais lidos na hora: Python 3.15.2 e Node 26.13.0. Interpretador local Python 3.14.7 e Node v24.22.1. SAST, segredo e EXE de aplicação passaram depois de excluir `.venv` e `.state`.
- Evidence: `quality/prepush/tests/test_prepush.py` (15 testes); `.aeos/prepush/report.json`.
