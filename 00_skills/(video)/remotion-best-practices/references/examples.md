# Examples

## New title card

User: "Make a Remotion title card that fades in."

1. Inspect the folder. Scaffold only if no Remotion project exists.
2. Open Studio.
3. Add a small component whose `opacity` is an inline `interpolate()` from frame 0 to `2 * fps`, clamped, using `useVideoConfig()`.
4. Register one `<Composition>` with a string `id`.
5. Do not render an MP4 unless the user asks.

Result: a composition id and a Studio URL, or the command that could not be started.

## Explicit export

User: "Render the video to an MP4."

1. `npx remotion compositions`
2. `npx remotion render <id> out/video.mp4`
3. Pass `--license-key` only when the user already has a key outside the chat. Use `--is-production=false` for a test.

Result: the output path and the command status. A missing key stops the company-license path; it does not invent `free-license`.

## Out of scope

- A normal React page that is not a Remotion composition.
- An FFmpeg-only trim with no Remotion project.
- A Lambda or Cloudflare render the user did not choose.
