# Approved Science Studio original → YouTube through Dark-videos

Updated: 2026-10-27. User explicitly authorized implementation and publication after the
legacy Shorts reviewer rejected the approved landscape/1 GB documentary.

Inputs: registered UUID-owned Science Studio project, matching five-check human approval,
exported MP4 and SRT, active YouTube account, policy-valid copy. Output: durable original-job
receipt in existing AppSetting storage, native video identity and confirmed public permalink.

The original flow is distinct from mined/reframed Shorts. It must not forge a mined source,
change Shorts checks, export cookies, use a second uploader, create agents or overwrite originals.
The same publishing.dispatch upload transport and global publish lock remain mandatory.

Original review: bounded project paths; exact approval/project/media/SRT fingerprints; actual
H.264/AAC 1920×1080/30 fps, scene sums and <=6600 s, max 2 GiB; real frame thumbnail; complete
decode before upload. Missing/stale approval, malformed sources, unsafe paths, account mismatch,
text-policy rejection or media errors fail closed.

Durability: one job per project fingerprint/account; persist claim before upload, never
automatically reupload after an ambiguous result; retain native ID for readback-only recovery.
Only confirmed public identity/metadata gives published state. Queue/status API authenticates
operators; caller cannot supply executable commands or absolute project paths.

Verification: baseline existing validation preserved; real fixture tests for original approval,
tampering, path escape, media geometry/size, idempotency and upload-failure identity retention;
lint/compile; live final-video review; exact installed hashes and backups. No migration or new
dependency is planned. External checkout writes require the filesystem tool approval.
