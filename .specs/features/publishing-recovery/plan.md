# Publishing recovery

Sources:

- conversation - operator asks to fix the publisher and upload every video that already failed
- `.work/publishing-recovery/census.json` - 131 queued rows (94 `failed`, 37 `platform_scheduled`) with the exact `last_error` vocabulary and native ids
- `C:\Users\paulo\AppData\Local\Temp\dark-videos-file.png` - the failure screenshot: the Studio dialog sits at "Selecionar arquivos" with no file ever set
- `.work/publishing-recovery/yt_census.py` + `youtube-shorts.json` - read-only Studio census proving no `youtube_upload_dialog_missing` caption exists natively
- `.work/publishing-recovery/yt_set_probe.py` - live probe of the working sequence: Criar, menu item, embedded input, details dialog

## Problem

The queue reports 94 videos as failed and 37 as scheduled-but-unconfirmed, and the operator cannot tell which of them already reached the network. Three separate defects produce that state.

The YouTube upload never attaches the file. `browser_post._open_youtube_upload` clicks "Criar" and immediately looks for the "Enviar vídeos" menu item, which the Studio renders a moment later, so the lookup returns `False`; `_attach_youtube_video` then waits 1.5 s once for the dialog input and falls through to a `page.expect_file_chooser` that this dialog never fires. Nineteen rows are parked on `youtube_upload_dialog_missing` with the file never set, and the error text tells the operator to "use Enviar vídeos and wait for the title" - a manual step the code itself fails to perform.

A failed row cannot be retried. `immediate.start_batch` selects only `ELIGIBLE` statuses and `dispatch._publish_now` refuses anything outside them, so `failed` is terminal from the UI: the 19 YouTube rows plus the other pre-upload failures can only be re-uploaded by hand. No bulk path exists.

A submitted row cannot be confirmed. `studio_immediate.confirm_existing` rejects TikTok and YouTube outright, so 42 rows that may already be live (37 TikTok, 5 YouTube) can only be resolved by manual Studio reading. Because a wrong retry on those is a duplicate public post, the operator either duplicates content or leaves the queue permanently red.

When this ships the operator clicks one control and the queue drains: pre-upload failures replay, submitted items are confirmed read-only, and anything genuinely ambiguous stays failed with its own cause.

## Out of scope

| Excluded | Why |
| --- | --- |
| Deleting or replacing an existing TikTok schedule | `tiktok_schedule_change_unavailable` is a deliberate guard; replacement needs per-item operator approval, not a bulk control |
| Re-uploading any row that already carries a native id | No mechanism can prove the network did not accept it; those rows go through confirmation instead |
| Instagram Story confirmation after 24 h | `_meta_active_stories` can only see active stories; expired ones have no read path, so they stay failed and are flagged to the operator |
| Meta Business Suite date-range filtering | An operational investigation of an existing read, not a change to this flow |
| New retry UI | The existing publish-now control gains one flag; no screen is redesigned |

## Assumptions

| Assumption | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Which failures are safe to replay | Only `youtube_upload_dialog_missing`, gated on no native id | After the S1 fix this error is raised only on paths that never handed bytes to Studio, so replay cannot duplicate; every other error is ambiguous and stays failed | y - user said blocked items and failures needing review are preserved |
| Rows with a native id but a failed status | Confirm read-only, never re-upload | The id exists, so the network may already hold the media | y - user asked for no duplicate uploads |
| Where the bulk control lives | `include_failed` on the existing `POST /api/publishing/publish-now` | Reuses the batch, the lock and the progress reporting that already exist | n - user delegated the placement |
| What confirms a scheduled item | Native state plus the row's existing local clock, never a parsed date | Parsing localized Studio dates is fragile; the local clock is already the operator's intent | n - chosen to avoid inventing a value |
| The 19 historical `youtube_upload_dialog_missing` rows | Replayed once, after the read-only census already taken | The census found none of their captions in Studio; the fix makes the error truthful from now on | y - census evidence recorded in `.work/publishing-recovery/` |

**Open questions:** none - all resolved or logged above.

## Criteria

### S1: the YouTube upload actually attaches the file (P1)

**Acceptance Criteria**

1. WHEN `browser_post._open_youtube_upload` clicks "Criar" THEN the system SHALL poll for the "Enviar vídeos" menu item for up to 10 attempts of 500 ms before answering `False`
2. WHEN the upload dialog is open THEN `_attach_youtube_video` SHALL poll for the embedded `input[type=file]` for up to 10 s instead of requiring a `filechooser` event
3. IF the file input accepted the file and the details dialog did not appear within the existing 45 s budget THEN the system SHALL raise `youtube_upload_unconfirmed` and SHALL NOT try to attach a second file
4. IF neither the embedded input nor a file chooser yields the details dialog THEN the system SHALL raise `youtube_upload_dialog_missing`

**Independent test:** drive the fake Studio page in a mode where the menu item and the dialog input render one tick late; the upload reaches the details dialog, and a mode where the details never appear raises `youtube_upload_unconfirmed` with `set_input_files` called exactly once.

### S2: a failed pre-upload row replays from the queue (P1)

**Acceptance Criteria**

5. WHEN `POST /api/publishing/publish-now` receives `include_failed: true` THEN the system SHALL add every `failed` row whose `last_error` is `youtube_upload_dialog_missing` and whose `external_media_id` is null, and SHALL re-arm each one to `scheduled` with `last_error` null
6. IF a `failed` row has a native id or a `last_error` outside that single value THEN the system SHALL NOT include it in the batch
7. WHILE `include_failed` is absent or `false` the system SHALL select exactly the rows it selects today

**Independent test:** seed four failed rows - replayable, replayable-with-id, other error, blocked - and assert one record is created and only that row is re-armed.

### S3: submitted items are confirmed read-only (P2)

**Acceptance Criteria**

8. WHEN `confirm_existing` is called for TikTok with a native id THEN it SHALL scan the Studio content list by scrolling up to 30 times and return `PUBLIC` only for a row whose owned video link matches that id and whose privacy reads `Todos`/`Everyone`
9. WHEN `confirm_existing` is called for YouTube with a native id THEN it SHALL prove identity on the edit page through title and description, then read the Studio content row and return `PUBLIC` for a public row, `SCHEDULED` for a `Programado`/`Agendado` row, and raise `publish_now_unconfirmed` otherwise
10. WHEN a `confirm_only` read returns `SCHEDULED` with the row's existing clock and the same native id THEN `_publish_now` SHALL persist `platform_scheduled` with `last_error` null and SHALL return `waiting_platform` without replaying the upload
11. IF a confirmation cannot match the native row or the identity THEN the system SHALL raise `publish_now_unconfirmed` and leave the persisted status unchanged
12. The system SHALL map `youtube_upload_unconfirmed` to an operator-facing label alongside the existing `last_error` labels

**Independent test:** call `confirm_existing` against fake pages in public, scheduled and absent states for both platforms, and assert the persisted status and `last_error` after each.

## Traceability

| ID | Slice | Criteria | Status |
| --- | --- | --- | --- |
| PUBREC-01 | S1 | 1, 4 | Pending |
| PUBREC-02 | S1 | 2 | Pending |
| PUBREC-03 | S1 | 3 | Pending |
| PUBREC-04 | S2 | 5, 7 | Pending |
| PUBREC-05 | S2 | 6 | Pending |
| PUBREC-06 | S3 | 8 | Pending |
| PUBREC-07 | S3 | 9 | Pending |
| PUBREC-08 | S3 | 10 | Pending |
| PUBREC-09 | S3 | 11 | Pending |
| PUBREC-10 | S3 | 12 | Pending |

## Observable

| Surface | Decision | Landing |
| --- | --- | --- |
| API `POST /api/publishing/publish-now` | request shape gains `include_failed` | AC 5 |
| API `POST /api/publishing/publish-now` | empty state - nothing selectable | AC 7 - existing `batch.status == completed` with zero records |
| API `POST /api/publishing/publish-now` | error shape and codes | existing - `409 publishing_busy`, `503 publisher_unavailable`, unchanged |
| API `POST /api/publishing/publish-now` | who may call it | existing - `require_operator` dependency, unchanged |
| API `POST /api/publishing/publish-now` | versioning | n/a - single-consumer internal route, no version prefix in this app |
| command `run_batch` | what it prints when one record fails halfway | AC 11 - the refused record carries the row's own `last_error` |
| document `last_error` labels | tone and next action for the new value | AC 12 |

## Flow

Reuses the existing batch, publishing lock, record states and `_publish_now`; no new module, queue or job is introduced.

1. `POST /api/publishing/publish-now {include_failed}` -> `api` (exists) - validates the operator and takes the publishing lock
2. -> `immediate.start_batch` (exists) - selects eligible rows plus replayable failed rows, re-arms those rows to `scheduled`, persists the batch record list
3. -> `immediate.run_batch` (exists) - per record calls `dispatch._publish_now`, either live or `confirm_only`
4. -> `studio_immediate.confirm_existing` (exists) - read-only native read for Instagram, TikTok or YouTube
5. -> `dispatch._keep_native_clock` (exists) - persists `platform_scheduled` when the readback proves a schedule
6. out: `Publication.status` + `Publication.last_error`, and the frontend label map (exists) reads `last_error` on the next render
7. `browser_post.publish_browser_session` (exists) - the live YouTube path attaches the file through the polling open/attach pair

## Relations

`None - no stored-data shape change`

## Surface

| Route | In | Out | Status |
| --- | --- | --- | --- |
| `POST /api/publishing/publish-now` | `retry_existing`, `replace_tiktok`, `include_failed` | `batch` · `batch.records` | `202`, `409`, `503` |

## Landing

| One-way door | Literal shape | Alternative rejected |
| --- | --- | --- |
| a new persisted `Publication.last_error` value | `"youtube_upload_unconfirmed"` in the `last_error` vocabulary, consumed by `immediate.REPLAYABLE` and `frontend/src/lib/api/publishing.ts` | reuse `"youtube_upload_dialog_missing"` for both cases: it cannot express "bytes were handed to Studio", so the replay allowlist would duplicate uploads |
| the default of the new batch flag | `include_failed: bool = False` on `ImmediateStartIn` | default `True`: the ordinary publish button would silently replay every failed row |

- Nothing else in this change is hard to reverse

## Impact

| Front | What changes |
| --- | --- |
| domain | existing term: `youtube_upload_dialog_missing` meant "the upload dialog did not open", now means "the dialog opened and no file was ever handed to it" - branched on today by `immediate.REPLAYABLE` and the frontend label map |
| domain | new term: `youtube_upload_unconfirmed` - bytes reached Studio but the details dialog never appeared, lives in `browser_post` and the frontend label map |
| stored data | nothing to migrate; historical rows keep their strings and `include_failed` re-arms them at read time |
| contract | `confirm_existing` accepts TikTok and YouTube, so `publish_now_unconfirmed` stops being the only answer for a submitted row |
