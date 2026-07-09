# Evidence Cache Guide

## Rule

Cache accelerates analysis. It does not replace evidence.

## Strong cache key must include

- AEOS version
- config hash
- policy hash
- permission hash
- playbook version
- skill versions
- LCP versions
- target file hashes
- command inputs

## Never cache

- secrets
- raw credentials
- approval authorization
- production mutation
- browser session
- cookies/tokens/API keys
