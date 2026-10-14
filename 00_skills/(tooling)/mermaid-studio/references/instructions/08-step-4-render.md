<!-- Package: 00_skills/(tooling)/mermaid-studio; relative command/resource examples resolve from that package or workspace root. -->

## Step 4: Render

### 4.1 — Setup (First Run Only)

```bash
bash $SKILL_DIR/scripts/setup.sh
```

This auto-installs both rendering engines and icon pack dependencies. Run once per environment.

### 4.2 — Single Diagram Rendering

```bash
# SVG (default — best quality)
node $SKILL_DIR/scripts/render.mjs -i diagram.mmd -o diagram.svg

# PNG (for documents/presentations)
node $SKILL_DIR/scripts/render.mjs -i diagram.mmd -o diagram.png --width 1200

# ASCII (for terminals/READMEs)
node $SKILL_DIR/scripts/render-ascii.mjs -i diagram.mmd

# With icon packs (architecture-beta with AWS/tech icons)
node $SKILL_DIR/scripts/render.mjs -i diagram.mmd -o diagram.svg --icons logos,fa
```

The `--icons` flag registers Iconify packs before rendering. Packs: `logos` (AWS/tech), `fa` (Font Awesome). Use `logos` for AWS.

### 4.3 — Batch Rendering

For multiple diagrams at once:

```bash
node $SKILL_DIR/scripts/batch.mjs \
  --input-dir ./diagrams \
  --output-dir ./rendered \
  --format svg \
  --theme default \
  --workers 4
```

### 4.4 — Available Themes

**beautiful-mermaid (15):** `tokyo-night` | `tokyo-night-storm` | `tokyo-night-light` | `dracula` | `nord` | `nord-light` | `catppuccin-mocha` | `catppuccin-latte` | `github-dark` | `github-light` | `solarized-dark` | `solarized-light` | `one-dark` | `zinc-dark` | `zinc-light`

**mermaid-cli native (5):** `default` | `forest` | `dark` | `neutral` | `base`

Custom theme: `--theme base --config '{"theme":"base","themeVariables":{"primaryColor":"#4f46e5","lineColor":"#94a3b8"}}'`

For the full theme catalog, read `references/themes.md`. The render script auto-selects the best engine (mmdc primary, beautiful-mermaid fallback, Puppeteer for icon packs).
