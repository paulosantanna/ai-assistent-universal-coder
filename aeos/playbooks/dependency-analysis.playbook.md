# Dependency Analysis Playbook

**ID:** dependency-analysis
**Version:** 1.0.0
**Risk Level:** medium
**Required Agents:** root, architect, security, judge
**Required Skills:** dependency-analyzer, compatibility-analyzer, risk-classifier, code-analyzer
**Required LCPs:** global-rules, security-governance
**Allowed MCPs:** filesystem-readonly, git-readonly

## Flow

### Step 1: Detect Dependency Files
- Scan target for: package.json, pyproject.toml, requirements.txt, pom.xml, build.gradle, Cargo.toml, go.mod
- Parse each file to extract direct dependencies

### Step 2: Classify Direct Dependencies
- For each dependency: name, version, type (prod/dev), license (if detectable)
- Risk classification: stable, active, deprecated, unmaintained
- Evidence: dependency declaration file content (SHA-256)

### Step 3: Map Transitive Dependencies (Read-Only)
- Parse lock files: package-lock.json, poetry.lock, requirements-lock.txt
- Extract transitive dependency tree
- Do NOT install or resolve — analysis only

### Step 4: Identify Obsolete Dependencies
- Check version age against current latest (via registry indicators)
- Flag: major versions behind, unmaintained, deprecated
- Risk: breaking change probability

### Step 5: Check Possible CVEs
- Scan dependency names and versions for known CVE patterns
- Do NOT access external CVE database (read-only analysis)
- Flag high-risk packages based on name and version patterns

### Step 6: Check Incompatibilities
- Compare dependency versions for known incompatibilities
- Check peer dependency conflicts
- Check platform/OS constraints

### Step 7: Assess Breaking Change Risk
- For each upgrade: classify as patch, minor, major
- Major = high risk, requires test evidence
- Minor = medium risk
- Patch = low risk

### Step 8: Generate Reports
- dependency-risk-report.md: full analysis with Facts, Assumptions, Risks, Recommendations
- upgrade-candidates.md: list of dependencies that could be upgraded
- compatibility-matrix.md: table of dependency versions and compatibility status
- dependency-evidence.json: structured data of all findings

### Step 9: Evidence Registration
- Register all reports in evidence-manifest.json
- Each report gets SHA-256
- Append to hash-chain.jsonl

## Outputs

| Artifact | Path | Required |
|----------|------|----------|
| Risk report | `.aeos/reports/{execution_id}/dependency-risk-report.md` | Yes |
| Upgrade candidates | `.aeos/reports/{execution_id}/upgrade-candidates.md` | Yes |
| Compatibility matrix | `.aeos/reports/{execution_id}/compatibility-matrix.md` | Yes |
| Evidence JSON | `.aeos/reports/{execution_id}/dependency-evidence.json` | Yes |
| Evidence manifest | `.aeos/evidence/{execution_id}/evidence-manifest.json` | Yes |
| Hash chain | `.aeos/evidence/{execution_id}/hash-chain.jsonl` | Yes |

## Prohibitions
- Do NOT update any dependency
- Do NOT run npm install, pip install, or any package manager
- Do NOT modify package.json, pyproject.toml, or any dependency file
- Do NOT access external CVE databases (future version)

## Blocking Conditions
- Dependency file modified
- Compatibility matrix missing
- Upgrade candidate without risk assessment