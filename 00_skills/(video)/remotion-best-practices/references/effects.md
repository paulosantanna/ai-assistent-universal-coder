# Effect names

Confirm every name against the installed `@remotion/effects` before use. This list is the inventory described by the Remotion 4.0.547 markup guidance, not a measurement that the installed package still exports each one.

These components accept `effects` directly:

- `remotion`: `<Img>`, `<CanvasImage>`, `<AnimatedImage>`, `<Solid>`, `<HtmlInCanvas>`
- `@remotion/media`: `<Video>`
- `@remotion/gif`: `<Gif>`
- `@remotion/rive`: `<RemotionRiveCanvas>`
- `@remotion/shapes`: `<Arrow>`, `<Callout>`, `<Circle>`, `<Ellipse>`, `<Heart>`, `<Pie>`, `<Polygon>`, `<Rect>`, `<Spark>`, `<Star>`, `<Triangle>`

Ordinary HTML, `<Interactive.*>`, `<AbsoluteFill>`, and `<Sequence>` do not. Wrap them in `<HtmlInCanvas>`.

Built-in names named in that guidance:

- Color and tone: `brightness`, `colorCorrection`, `colorKey`, `contrast`, `curves`, `duotone`, `exposure`, `grayscale`, `hue`, `invert`, `levels`, `linearGradient`, `linearGradientTint`, `lut`, `saturation`, `shadowsHighlights`, `thermalVision`, `tint`, `vibrance`, `whiteBalance`
- Blur and trails: `blur`, `lightTrail`, `linearProgressiveBlur`, `radialProgressiveBlur`, `regionBlur`, `zoomBlur`
- Lighting: `dropShadow`, `longShadows`, `glow`, `lightLeak`, `shine`, `starburst`, `vignette`
- Distortion: `barrelDistortion`, `chromaticAberration`, `cornerPin`, `fisheye`, `mirror`, `noiseDisplacement`, `scale`, `skew`, `tile`, `uvTranslate`, `wave`, `xyTranslate`
- Texture: `burlap`, `checkerboard`, `contourLines`, `dotGrid`, `emboss`, `flannel`, `gridlines`, `halftone`, `halftoneLinearGradient`, `lines`, `liquidContours`, `noise`, `paper`, `pattern`, `rings`, `scanlines`, `speckle`, `tvSignalOff`, `waves`, `whiteNoise`, `zigzag`
- Edges: `outline`, `roughenEdges`, `shrinkwrap`, `tear`
- Pixel and transition: `evolve`, `linearProgressivePixelate`, `pixelate`, `pixelDissolve`, `radialProgressivePixelate`, `venetianBlinds`

Prefer a built-in effect on the target component over a CSS approximation. Use `createEffect()` only after checking that no built-in matches. Read the package's current effect page for parameters.
