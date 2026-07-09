# AEOS v0.95 — Local Pack Marketplace

## Mission

Allow AEOS to manage skill packs, playbook packs, LCP packs, MCP profiles and environment packs safely.

## Pack Types

```text
skill-pack
playbook-pack
lcp-pack
mcp-profile-pack
environment-pack
security-policy-pack
observability-pack
```

## Rules

- import to quarantine first;
- verify manifest;
- verify checksums;
- scan for secrets;
- validate contracts;
- validate capabilities;
- validate policies;
- require promotion step;
- never import directly to active registry;
- support rollback of pack promotion.

## Directories

```text
aeos/packs/quarantine/
aeos/packs/staging/
aeos/packs/active/
aeos/packs/archived/
aeos/packs/rejected/
```

## Pack Promotion

```powershell
aeos pack verify --package <zip>
aeos pack import --package <zip> --to quarantine
aeos pack inspect --pack-id <id>
aeos pack promote --pack-id <id> --to staging
aeos pack activate --pack-id <id>
aeos pack rollback --pack-id <id>
```
