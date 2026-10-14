<!-- Package: 00_skills/(cloud)/kinghost-site-publish-ftp-expert; relative command/resource examples resolve from that package or workspace root. -->

## Non-negotiable production gates

1. Resolve the exact KingHost domain/environment with `domain.list` + `domain.select`.
2. Bind only already-provisioned FTP credentials as opaque refs.
3. Inventory the current remote tree and the candidate local tree.
4. Compute a bounded publish manifest/diff before any upload.
5. Reject path traversal and any destination outside the approved remote root.
6. Create/verify a backup or equivalent rollback point before destructive or overwrite publication.
7. Dry-run when supported and record the intended create/update/delete set.
8. Require approval/change id for production mutation.
9. Never upload credentials, raw cookies, private keys, local `.env`, editor metadata, build secrets or unintended database dumps.
10. Do not delete remote files merely because they are absent locally unless deletion is explicitly requested, reviewed and rollback-safe.
11. FTP transfer success is not deployment success. HTTP/application smoke is mandatory.
