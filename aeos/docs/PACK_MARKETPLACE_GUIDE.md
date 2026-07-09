# Pack Marketplace Guide

## Goal

Safely import/export AEOS skill/playbook/LCP/MCP packs.

## Flow

```powershell
aeos pack verify --package <zip>
aeos pack import --package <zip> --to quarantine
aeos pack inspect --pack-id <id>
aeos pack promote --pack-id <id> --to staging
aeos pack activate --pack-id <id>
```

## Never import directly into active registry.

All packs must pass:

- manifest check
- checksum check
- secret scan
- contract validation
- capability validation
- policy compatibility
