# Procedure

## Contents

- Gates
- Route
- Scaffold and Studio
- Markup
- Timing
- Elements, captions, maps, and media metadata
- Render, SaaS, upgrade, and license

## Gates

These gates win when a remembered example disagrees.

- The rules below were checked against Remotion skills `4.0.547`. Read `package.json` and the official `.md` page before using an API that may have moved.
- Do not overwrite a surprising edit. Ask if it is unclear whether the user made it.
- Do not delete `.git`, `.env`, or other meaningful hidden files to satisfy `create-video`.
- Do not print, commit, or pass a Remotion license key, Mapbox token, MapTiler key, or Cesium token on a command line that will be logged. An empty license key is invalid.
- Do not run `npx skills update` in this workspace. That command reinstalls upstream skill files over this TLC package.
- A missing binary, project, or permission blocks only the dependent step.

## Route

| Request | Section |
| --- | --- |
| New project or composition | Scaffold and Studio |
| React markup, animation, audio, captions layout | Markup and Timing |
| Element page or library URL | Elements |
| Map, route, GeoJSON, flyover | Maps |
| Transcribe, SRT, or on-screen captions | Captions |
| Duration or dimensions of a media file | Media metadata |
| Preview | Studio |
| MP4, still, or image sequence the user explicitly requested | Render |
| `<Player>` or a hosted renderer | SaaS |
| Bump Remotion | Upgrade |
| Price, terms, or whether a company needs a seat | License |

## Scaffold and Studio

If the user asked to create a video and no Remotion project exists:

- Empty folder, or only disposable OS metadata such as `.DS_Store`: remove that metadata, then `npx create-video@latest --yes --blank --no-tailwind .`
- Meaningful files already present: scaffold a named subfolder, `npx create-video@latest --yes --blank --no-tailwind <name>`, then `cd` into it. Confirm first when the folder is not an obvious scratch directory.
- If dependency install fails, run the project's package manager install once. Do not switch package managers.

Open Studio before further video edits once the project can run:

```bash
npx remotion studio
```

Use `--no-open` only when an in-app browser will open the printed URL. Visit `/<composition-id>` for one composition. `--port` requests a port; `--force-new` starts another instance. Studio is long-running. If it is already up, use the printed URL instead of starting a second server.

Add Tailwind only when the user asks. Animation still comes from `useCurrentFrame()`. Do not use Tailwind `transition-*` or `animate-*` classes. Enable Tailwind with the current docs at `https://www.remotion.dev/docs/tailwind`.

Design a frame, not a page. One primary subject per scene. On a 1080px-wide frame, keep key text at least 80px from the sides and 100px from the top and bottom. Rough minimums at that width: headline 84px, supporting text 44px. Scale both with the composition width.

## Markup

- Call `useCurrentFrame()` in the smallest component that needs the frame.
- Take `fps` from `useVideoConfig()` and write seconds as expressions on the JSX node, such as `trimBefore={2 * fps}`.
- Drive motion with `interpolate()`. CSS transitions, CSS animations, and Tailwind animation classes do not render frame by frame.
- Prefer `Easing.bezier()` or `Easing.spring()`. Clamp with `extrapolateLeft` and `extrapolateRight` when the value must stay inside the range.
- For Studio-editable motion, keep `interpolate()` inline on `style`. Use `scale`, `translate`, and `rotate`. For `scale`, set `output: "perceptual-scale"`. Do not hide the value in a `transform` string.
- New markup is editable unless it is generated from external data or computed per frame. Say so when a part cannot be selected. Text the agent writes is not external data.
- Put assets in `public/` and reference them with `staticFile()`. Remote URLs may be passed directly.
- Import `<Video>` and `<Audio>` from `@remotion/media`. Use `<CanvasImage>` for still images and `<AnimatedImage>` for animated GIF, APNG, WebP, or AVIF. Use `@remotion/gif` when not rendering in Chrome.
- Give each composition or still its own JSX node with a string-literal `id` when it should be edited alone. Programmatic registration is for one template that is not edited item by item.
- Each substantial scene gets its own component. Non-overlapping scenes with independent starts go on a `Track`. Adjacent scenes that must stay adjacent go in `TransitionSeries`, one scene per `TransitionSeries.Sequence`.
- Apply `effects` only on components that accept them. Wrap ordinary HTML, `<Interactive.*>`, `<AbsoluteFill>`, or `<Sequence>` in `<HtmlInCanvas>` and put `effects` on the wrapper. Read [effects](effects.md) and confirm the name against the installed package.
- Three.js motion also comes from `useCurrentFrame()` inside `<ThreeCanvas>`. Fetch `https://www.remotion.dev/docs` for the current 3D page before adding a canvas.
- Fetch the matching page in [topics](topics.md) before trimming media, building captions UI, color grades, Lottie, fonts, or transitions.

## Timing

Put timing on the interactive item or on `<Audio>` when that item is edited alone. Use one `<Sequence>` when several layers share a trim, a speed, or a start, or when the child has no timing props. `layout="none"` avoids an extra layout box.

Order: `from`, then `trimBefore`, then `durationInFrames`, then `playbackRate`, then `loop`. Children see `trimBefore + (frame - from) * playbackRate`. `<Img>`, `<CanvasImage>`, `<Solid>`, and shapes do not loop. A component without these props is wrapped in `<Sequence>`.

`Track` items must not overlap. `TransitionSeries` owns the shared boundary even if a child also accepts timing props.

## Elements, captions, maps, and media metadata

Elements:

1. Fetch `https://www.remotion.dev/elements/libraries.md` unless the user gave a URL.
2. `npx remotion elements add-library <library-url>` before adding from that library. This needs Remotion 4.0.547 or a manual `Config.addElementLibrary({url})` on older versions.
3. Dry-run: `npx remotion elements use <element-page-url> --composition <id> --dry-run`.
4. Install with `--yes` only after the dry run lists the files. Then preview in Studio.

Captions use `@remotion/captions` `Caption`: `text`, `startMs`, `endMs`, `timestampMs`, `confidence`, optional `pageBreakAfter`. Transcription uses `@remotion/whisper-webgpu` locally at 16 kHz mono. Check `canUseWhisperWebGpu()` first. ONNX Runtime does not run on Linux arm64. Do not send the audio to a hosted model unless the user chooses that path. Fetch the current transcribe and caption pages before writing the script.

Maps: pick one technique and load only that one. Static map is a satellite image in `<Img>` plus overlays. MapLibre needs no key and has no 3D buildings. Mapbox needs a key, a globe, and 3D buildings. MapTiler is for annotations on geographic features. CesiumJS is a terrain flyover. Keys stay in the environment. Fetch the current technique page before writing the camera loop. Do not claim a map render is stable until the project has been previewed.

Media duration and dimensions in the browser go through Mediabunny. Read `https://mediabunny.dev/llms.txt` and the project's existing helper before adding a parser.

## Render, SaaS, upgrade, and license

Render only for an explicit export request. Prefer Studio's render UI when the user is already previewing. Otherwise:

```bash
npx remotion compositions
npx remotion render <composition-id> out/video.mp4
```

Always pass the composition id. Props are inline JSON or a JSON file via `--props`. Use Remotion's bundled browser. Do not set a browser executable unless the user asks. Stills use `npx remotion still`. Selected frames use `npx remotion render <id> out/frames --frames=0,30,90 --image-format=png`; list the output directory instead of guessing padded names.

Pass `--license-key` only when a real key or the literal `free-license` is justified. Add `--is-production=false` for test renders. Company license questions go to the official license, FAQ, terms, and pricing pages. Do not decide that the user qualifies for the free license.

One-off output stays on the CLI or Studio. `<Player>` is the in-app preview. Programmatic server render bundles once with `@remotion/bundler`, then `selectComposition` and `renderMedia`. Lambda, Vercel, Azure, GitHub Actions, and Cloudflare need an explicit host choice and a cost confirmation. Read `https://www.remotion.dev/docs/compare-ssr.md` first.

Upgrade with `npx remotion upgrade` when `@remotion/cli` is installed. Otherwise set every `remotion` and `@remotion/*` package to the same version from `npm view remotion version`, and align `zod`, `mediabunny`, and `@huggingface/transformers` with `npm view @remotion/studio@<version> dependencies --json`. Review the lockfile. `npx remotion versions` is a check, not proof that the app still renders.
