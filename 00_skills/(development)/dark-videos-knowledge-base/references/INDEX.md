# INDEX - Dark Videos Knowledge Base

## Reference Notes Available

- `mining.md` - Connectors, synthetic sample, lookback widening
- `frame.md` - Framing and copy generation (one frame per video, one description + max 5 tags)
- `heat.md` - Heat scoring and top 20 (sort: `0.65 * baseline velocity + 0.35 * LAYA signal`, heat >= 9.5 badge does not remove from top 20)
- `publish.md` - Publishing dispatch and accounts (dispatch is the only publisher)
- `usage-and-verification.md` - Example usage and failure handling
- `provenance.md` - Provenance and source freshness

## Skill Routing

This skill is routed by mission type:

- **Mining operations** → Open `references/mining.md`
- **Framing/generation** → Open `references/frame.md`
- **Heat/ranking** → Open `references/heat.md`
- **Publishing** → Open `references/publish.md`
- **Usage guidance** → Open `references/usage-and-verification.md`
- **Provenance/source** → Open `references/provenance.md`

## Cache TTL

- Status: 5s
- Mining: 10s
- Enqueue: 3s

## Provenance

- Original repository: `D:\Git\dark-videos`
- Mapped: Mon Oct 12 2026
- Mapping version: 3.0.0 (Full Alpha)
- Category: development
- Owner: codenavi-agent