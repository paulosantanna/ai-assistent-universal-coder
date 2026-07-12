#!/usr/bin/env python3
from pathlib import Path
import sys
required=['SKILL.md','README.md']
missing=[x for x in required if not (Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()/x).exists()]
print('PASS' if not missing else 'FAIL: '+', '.join(missing))
raise SystemExit(0 if not missing else 1)
