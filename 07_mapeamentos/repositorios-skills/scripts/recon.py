"""Show bounded evidence pointers without environment files or private data."""
import json
import re
from pathlib import Path
from inventory import ROOT, OUT

PATHS = {
 'AIHealthResearch': ['README.md','docs/ARCHITECTURE.md','src/aihealthresearch/interfaces/http.py','src/aihealthresearch/application/research.py','src/aihealthresearch/infrastructure/database.py','src/aihealthresearch/infrastructure/trainer.py','infra/render_stack.py'],
 'dark-videos': ['README.md','backend/pyproject.toml','frontend/package.json','backend/app/main.py','backend/app/db/base.py','backend/app/modules/mining/metadata_policy.py','backend/app/modules/publishing/service.py','laya-mcp.md'],
 'dark-videos-mining-fix': ['README.md','CONFIGURATION.md','package.py','run_checks.py'],
 'DiabeticsresearchJEV': ['README.md','src/diabeticsresearchjev/interfaces/api.py','src/diabeticsresearchjev/application/pipeline/full_cycle.py','src/diabeticsresearchjev/application/rag/retriever.py','src/diabeticsresearchjev/application/training/trainer.py','docker-compose.yml'],
 'Engenharia-Reversa': ['README.md','src/main.ts','src/cli.ts','src/composition/server.ts','docs/architecture.mermaid','bridge/ghidra/ReaGhidraBridge.java','native/windows/binding.gyp'],
 'FreePDFReader': ['README.md','src/main.rs','crates/freepdfreader-ai/src/engine.rs','crates/freepdfreader-core/src/document.rs','crates/freepdfreader-ui/src/app.rs','PORTABLE.md'],
 'ibunny': ['README.md','docs/product/ALPHA.md','apps/client/pubspec.yaml','services/api/go.mod','services/api/cmd/api/main.go','services/api/internal/adapters/http/server.go','services/api/internal/adapters/postgres/store.go','services/runner/cmd/runner/main.go'],
 'laya': ['README.md','engine/requirements.txt','ui/package.json','ui/src-tauri/Cargo.toml','engine/laya/main.py','engine/laya/db/sqlite.py','engine/laya/db/fts.py','engine/laya/mcp/server.py','docs/architecture.md'],
 'pdfcraft': ['README.md','apps/pdfcraft-cli/src/main.rs','crates/automation/src/lib.rs','crates/engine/src/lib.rs','apps/pdfcraft/src/main.rs','crates/automation/README.md'],
 'remove-onedrive': ['README.md','Remove-OneDrive.ps1','docs/verification.md'],
 'RemoveWindowsAI': ['README.md','Documentation.md','RemoveWindowsAi.ps1','RemoveAI-UpdateCleanup.ps1']}
PATTERN = re.compile(r'(^#|FastAPI|[Rr]outer|[Rr]oute|def |pub fn |fn main|func |class |CREATE TABLE|SQLite|Postgre|Mongo|Chroma|OpenSearch|GraphQL|LoRA|QLoRA|BM25|SageMaker|/health|FastMCP|mcp|Tauri|Svelte|Flame|Go |Python|Rust|Node|ONNX|Pdfium|PDFium|Ollama|function |Remove-Item|Stop-Process|Uninstall|Restore|restore|rollback|backup|Transcript|template|WORKFLOW|pipeline|version|requires-python|next\"|react\"|go 1|flame:|flutter:)',re.I)
if __name__ == '__main__':
    import sys
    names = sys.argv[1:] or PATHS
    for name in names:
        print('\nREPOSITORY',name)
        for rel in PATHS[name]:
            p=ROOT/'02_repositorios'/name/rel
            if not p.is_file():
                print('MISSING',rel)
                continue
            raw=p.read_bytes()
            encoding='utf-16' if raw.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8-sig'
            try:
                lines=raw.decode(encoding).splitlines()
            except UnicodeDecodeError:
                print('ENCODING fallback cp1252:',rel)
                lines=raw.decode('cp1252').splitlines()
            found=[f'{i}: {line[:240]}' for i,line in enumerate(lines,1) if PATTERN.search(line) and not re.search(r'password|token|secret|cookie|auth.*key|\w+://[^\s/]*@',line,re.I)]
            print(rel+'\n'+'\n'.join(found[:18]))
