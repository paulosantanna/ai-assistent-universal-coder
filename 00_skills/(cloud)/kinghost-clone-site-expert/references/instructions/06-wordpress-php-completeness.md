<!-- Package: 00_skills/(cloud)/kinghost-clone-site-expert; relative command/resource examples resolve from that package or workspace root. -->

## WordPress/PHP completeness

For WordPress/PHP, FTP clone represents the filesystem layer only. Report separately:

- filesystem clone status;
- database clone/snapshot status;
- secrets/config status;
- uploads/media status;
- application verification readiness.

A full WordPress site clone requires both filesystem and the appropriate MySQL state. Never label an FTP-only copy as a complete application clone when database-backed content exists.
