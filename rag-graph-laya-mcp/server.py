"""Portable entrypoint; use the isolated Python before importing native dependencies."""
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
INTERPRETER = ROOT / '.venv' / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
if INTERPRETER.exists() and Path(sys.executable).resolve() != INTERPRETER.resolve():
    os.execv(str(INTERPRETER), [str(INTERPRETER), str(__file__), *sys.argv[1:]])

if __name__ == '__main__':
    from app.server import main
    main()
