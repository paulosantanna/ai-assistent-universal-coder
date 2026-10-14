<!-- Package: 00_skills/(development)/nestjs-modular-monolith; relative command/resource examples resolve from that package or workspace root. -->

## Quick Anti-Pattern Detection

Before finalizing any module, run `scripts/validate-isolation.sh` or verify manually:

```bash
# Check duplicate entity names across modules
grep -r "@Entity.*name:" libs/ | grep -o "name: '[^']*'" | sort | uniq -d

# Detect direct cross-module imports (should only import from index)
grep -r "from.*@company.*/" libs/ | grep -v shared | grep -v index

# Find shared mutable state
grep -r "export.*=.*new" libs/ | grep -v test

# Check for synchronous inter-module calls
grep -r "await.*\..*Service" libs/ | grep -v "this\."
```

If any check finds violations, fix them before proceeding.
