<!-- Package: 00_skills/(cloud)/kinghost-clone-site-expert; relative command/resource examples resolve from that package or workspace root. -->

## Safety contract

1. Select the exact environment/domain with `domain.list` + `domain.select` before transfer.
2. Bind an already-provisioned FTP identity through `kinghost_control.credential.bind`; passwords remain opaque/runtime-only.
3. Remote clone operations are read-only. This skill must never call upload/delete/mkdir or any mutation tool while in clone mode.
4. Inventory the entire reachable remote root before downloading.
5. Preserve relative paths exactly; reject path traversal and writes outside the approved local destination.
6. Transfer binary files as binary data; never normalize line endings or rewrite payloads during clone.
7. Detect and report inaccessible files, permission errors, symlink-like entries, unsupported node types, interrupted transfers and name collisions.
8. `wp-config.php`, `.env`, private keys and other secret-bearing files are not exposed to the model/evidence. If policy excludes them from materialization, record them as `SECRET_EXCLUDED`, not as silently missing.
9. Never overwrite a non-empty local destination unless an explicit destination policy and rollback/snapshot exist.
10. A successful FTP status is not PASS. Completion requires inventory reconciliation and integrity evidence.
