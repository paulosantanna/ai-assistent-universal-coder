# Publishing recovery checks

Profile: light
Plan: `.specs/features/publishing-recovery/plan.md`

14 checks in 3 slices · 2 one-way doors · 0 open

## Checks

### S1 - the YouTube upload actually attaches the file · 1 file · 82 KB

**C1** - A menu item that renders after "Criar" is still clicked, so the upload reaches the details dialog (PUBREC-01, AC 1)
Proof: `python -m pytest tests/modules/publishing/test_youtube_studio_upload.py -k test_upload_menu_renders_after_criar`

**C2** - A dialog input that appears after the dialog opens is found by polling and receives the file (PUBREC-02, AC 2)
Proof: `python -m pytest tests/modules/publishing/test_youtube_studio_upload.py -k test_dialog_input_appears_after_open`

**C3** - When no input or chooser ever appears, `youtube_upload_dialog_missing` is raised (PUBREC-01, AC 4)
Proof: `python -m pytest tests/modules/publishing/test_youtube_studio_upload.py -k test_attach_without_input_raises_dialog_missing`

**C4** - When the file is accepted but the details dialog never opens, `youtube_upload_unconfirmed` is raised and the file is set exactly once (PUBREC-03, AC 3)
Proof: `python -m pytest tests/modules/publishing/test_youtube_studio_upload.py -k test_details_never_open_raises_unconfirmed_once`

### S2 - a failed pre-upload row replays from the queue · 2 files · 44 KB

**C5** - `include_failed` adds a failed row carrying `youtube_upload_dialog_missing` and no native id, and re-arms it to `scheduled` with no error (PUBREC-04, AC 5)
Proof: `python -m pytest tests/modules/publishing/test_immediate.py -k test_include_failed_replays_preupload_row`

**C6** - A failed row with a native id, or with any other error, is never selected (PUBREC-05, AC 6)
Proof: `python -m pytest tests/modules/publishing/test_immediate.py -k test_include_failed_skips_ambiguous_rows`

**C7** - Without the flag the selection is exactly the eligible set it selects today (PUBREC-04, AC 7)
Proof: `python -m pytest tests/modules/publishing/test_immediate.py -k test_batch_without_flag_keeps_eligible_selection`

**C8** - The route answers `202` with the flag, `409` when the lock is held and `503` when the worker refuses to start (PUBREC-04, AC 5)
Proof: `python -m pytest tests/modules/publishing/test_immediate.py -k test_include_failed_route_contract`

### S3 - submitted items are confirmed read-only · 3 files · 61 KB

**C9** - Instagram confirmation keeps its existing Business Suite path and still maps the native id (PUBREC-09, AC 11)
Proof: `python -m pytest tests/modules/publishing/test_immediate.py -k test_confirm_existing_instagram_path_is_unchanged`

**C10** - TikTok confirmation scrolls the Studio list and returns `PUBLIC` only for the owned link with an `Everyone` privacy cell (PUBREC-06, AC 8)
Proof: `python -m pytest tests/modules/publishing/test_studio_immediate_readback.py -k test_tiktok_confirm_scrolls_to_owned_public_row`

**C11** - YouTube confirmation returns `PUBLIC` for a public row and `SCHEDULED` for a `Programado` row after proving identity on the edit page (PUBREC-07, AC 9)
Proof: `python -m pytest tests/modules/publishing/test_studio_immediate_readback.py -k test_youtube_confirm_reads_public_and_scheduled`

**C12** - A confirmation that finds nothing raises `publish_now_unconfirmed` and leaves the persisted status untouched (PUBREC-09, AC 11)
Proof: `python -m pytest tests/modules/publishing/test_studio_immediate_readback.py -k test_confirm_missing_native_row_preserves_status`

**C13** - A `confirm_only` read that returns `SCHEDULED` keeps `platform_scheduled` with no error and never re-uploads (PUBREC-08, AC 10)
Proof: `python -m pytest tests/modules/publishing/test_immediate.py -k test_scheduled_confirm_keeps_platform_state`

**C14** - The new error value has an operator label and the existing labels are untouched (PUBREC-10, AC 12)
Proof: `npx vitest run src/lib/api/publishing.test.ts -t "youtube_upload_unconfirmed"`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| replayable `last_error` allowlist (1) | `youtube_upload_dialog_missing` C5 | - |
| batch selection inputs (4) | eligible row C7 · replayable failed row C5 · failed row with native id C6 · failed row with another error C6 | - |
| YouTube attach outcome (4) | late menu C1 · late input C2 · no input C3 · details never open C4 | - |
| `confirm_existing` platform (3) | instagram C9 · tiktok C10 · youtube C11 | - |
| `POST /api/publishing/publish-now` statuses (3) | 202 C8 · 409 C8 · 503 C8 | - |
| `last_error` label map addition (1) | `youtube_upload_unconfirmed` C14 | - |
| confirm result state (3) | public C11 · scheduled C13 · absent C12 | - |

- Claims naming a status code, a route or a persisted status: C8, C12, C13 - each proof crosses the boundary it claims
- No other check claims more than the single case its proof exercises

## Swept

- validation: C6 - only a null native id plus the single allowlisted error may enter the batch
- failure modes: C4, C12 - the two ways an attach can half-succeed stay distinct
- idempotency: C4, C13 - a second file is never attached and a scheduled read never re-uploads
- authorization: existing - `require_operator` on the route plus the publishing advisory lock, unchanged
- concurrency: existing - `publishing_lock` already serializes the batch and returns `409 publishing_busy`
- data lifecycle: n/a - no row is deleted or archived by this change
- dependency failure: C3 - a missing Studio control fails the row with its own cause instead of hanging
- state transitions: C5, C13 - `failed` to `scheduled` only through the allowlist, `platform_scheduled` keeps its clock
- observability: C14 - the new error is readable to the operator in the existing label map

## Handoff

Intended split, with the arithmetic, written before any code:

- S1 = 1 file, S2 = 2 files, S3 = 3 files plus tests; no slice crosses a module boundary that needs a separate handoff
- S1 must land before the S2 replay runs, because the replay is only safe once `youtube_upload_dialog_missing` means no bytes were handed to Studio

- **Boundary:** pending

## Verification

Run on 2026-10-21, after S1-S3 and the S4 settle fix.

| Check | Result | Evidence |
| --- | --- | --- |
| C1-C13 | pass | same pytest node set, three files, `13 passed` |
| C14 | pass | `npx vitest run src/lib/api/publishing.test.ts` -> `4 passed` |

S4 was added after the first live publish produced a duplicate. `_settle_youtube_publication` polls the row for ~100 s and, when it never settles, raises `youtube_upload_unconfirmed` **with** `external_media_id`, so the next step is a confirmation instead of a second upload. `immediate._retry_records` gained `upload_retry` (YouTube, failed, that error, native id) so such a row is re-armed to `platform_scheduled` with `retry_native`. Proofs: `test_settle_state_reads_the_row_the_same_way_for_every_locale` (4 params) and `test_unsettled_publication_keeps_the_native_identity`.

Live rollout evidence:

- `dc11a6b6` settled through `_publish_now(confirm_only=True)` -> `published`, `zeYgV9k22hs`, `https://youtu.be/zeYgV9k22hs`.
- `8b9cfdcb` settled through the same readback -> `published`, `https://www.instagram.com/topvideosbrasil_oficial/reel/Defuo__DcOd/`.
- Remaining queue rows are blocked on human re-authentication (Google identity confirmation on the YouTube profile, TikTok Studio session logged out), not on a code path.

- **Boundary:** pending - the queue is not drained while those two sessions stay unavailable.
