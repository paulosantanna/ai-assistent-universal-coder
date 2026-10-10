# Publish

`default_params` stores `effective_dry_run`. The desktop (`DARKVIDEOS_DESKTOP=1` and fakes off) forces `dry_run` false. Outside the desktop, a saved simulation flag still simulates: dispatch writes `SIMULATED` and does not call the network.

Schedule rows are persisted only for an active connected account. A platform with no account stays on the last-run plan with the "sem conta" badge and does not enter the queue.

Dispatch is the only publisher. It composes the framed file, posts, then deletes the local media. The classified file lives in `~/.local/share/dark-videos/media` (also the default of `PUBLISHING_MEDIA_TMP_DIR`). Dispatch copies that file before it asks a data provider. ffmpeg must be on PATH or under the WinGet Gyan.FFmpeg package; a missing binary is `compose_unavailable`.

Browser Instagram accounts post in a visible window: click "Novo post", wait for the file input, then click Avançar and Compartilhar only inside the create dialog. The home feed also has a Compartilhar control; clicking that does not publish the reel. `publications.last_error` is the code the Agenda translates. TikTok privacy stays `SELF_ONLY` until the app audit. Instagram API posting still needs the public media base URL and the signing key.

Do not post from the MCP. `pipeline.start_run` only asks the local API to enqueue the same pipeline.
